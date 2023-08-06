'''A guard is responsible for authenticating and authorizing app users, be they
   humans or other apps. A guard will ensure that any action is performed in the
   respect of security rules defined: workflows, permissions, etc.'''

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Copyright (C) 2007-2020 Gaetan Delannay

# This file is part of Appy.

# Appy is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.

# Appy is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with
# Appy. If not, see <http://www.gnu.org/licenses/>.

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
from pathlib import Path

from DateTime import DateTime

from appy.px import Px
from appy.utils import multicall
from appy.model.user import User
from appy.server.cookie import Cookie
from appy.utils import path as putils
from appy.model.utils import Object as O
from appy.model.fields.string import String
from appy.model.fields.password import Password

# Errors - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
KO_LOG_TFM  = 'Invalid value "%s" for attribute "loginTransform".'
KO_PERM     = '%s "%s": "%s" disallowed.'

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Config:
    '''Security configuration'''
    # Allowed value for field "loginTransform"
    transformValues = ('lower', 'upper', 'capitalize')

    def __init__(self):
        # Activate or not the button on home page for asking a new password
        self.activateForgotPassword = True
        # By default, when creating a local user, Appy generates a password for
        # him. If you want to disable this and manage yourself, in your app's
        # User.onEdit method, generation and sending of passwords, set the
        # following attribute to False.
        self.generatePassword = True
        # On user log on, you may want to ask them to choose their
        # "authentication context" in a list. Such a context may have any
        # semantics, is coded as a string and will be accessible on the Handler
        # object in attribute "authContext". In order to activate authentication
        # contexts, place here an instance of a sub-class of class
        # appy.server.context.AuthenticationContext. Consult this class'
        # docstring for more information.
        self.authContext = None
        # Allow self-registering ?
        self.selfRegister = False
        # When a login is encoded by the user, a transform can be applied (one
        # among Config.transformValues).
        self.loginTransform = None
        # When using a LDAP for authenticating users, place an instance of class
        # appy.server.ldap.Config in the field below.
        self.ldap = None
        # When using, in front of an Appy server, a reverse proxy for
        # authentication for achieving single-sign-on (SSO), place an instance
        # of appy.server.sso.Config in the field below.
        self.sso = None

    def getLdap(self):
        '''Returns the LDAP config if it exists'''
        # The LDAP config can be found either in attribute "ldap" or in the
        # context of a SSO system. This method returns a tuple
        #                     (ldapConfig, context)
        # "context" being None if the global LDAP config is returned, or being
        # the SSO config if the LDAP is the one embedded in the SSO config.
        if self.ldap:
            r = self.ldap, None
        else:
            sso = self.sso
            if not sso or not sso.ldap:
                r = None, None
            else:
                r = sso.ldap, sso
        return r

    def check(self):
        '''Check this config'''
        # Check attribute "loginTransform"
        transform = self.loginTransform
        if transform and (transform not in self.transformValues):
            raise Exception(KO_LOG_TFM % transform)
        return True

    def transformLogin(self, login):
        '''Return p_login as potentially transformed via
           p_self.loginTransform.'''
        return getattr(login, self.loginTransform)() \
               if self.loginTransform else login

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Unauthorized(Exception):
    '''Error that is raised when a security problem is encountered'''

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Guard:
    '''Implements security-related functionality'''
    Error = Unauthorized
    Cookie = Cookie
    traverse = {}

    def __init__(self, handler):
        # The handler that has instantiated this guard
        self.handler = handler
        # Unwrap some useful objects
        self.model = handler.server.model
        self.config = handler.server.config
        # Authenticate the currently logged user and get its User instance
        self.user = User.authenticate(self)
        # Remember that this user hits the server now
        if not handler.fake:
            handler.onlineUsers[self.user.login] = DateTime()
        # Info about the currently selected authentication context
        self.authContext = None
        # Cache info about this user
        self.cache()

    def cache(self):
        '''Pre-compute, for performance, heavily requested information about the
           currently logged user.'''
        u = self.user
        self.userLogin = u.login
        self.userLogins = u.getLogins(compute=True, guard=self)
        self.userRoles = u.getRoles(compute=True, guard=self)
        self.userAllowed = u.getAllowedFrom(self.userRoles, self.userLogins)
        self.userLanguage = u.getLanguage() if not self.handler.fake else 'en'

    # In the remaining of this class, when talking about "the user", we mean
    # "the currently logged user".

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Security checks on classes
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    def mayInstantiate(self, class_, checkInitiator=False, initiator=None,
                       raiseOnError=False):
        '''May the user create instances of p_class_ ?'''
        # This information can be defined on p_class_.python, in static
        # attribute "creators". If this attribute holds...
        #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # a list    | we consider it to be a list of roles, and we check that
        #           | the user has at least one of those roles;
        # a boolean | we consider that the user can create instances of this
        #           | class if the boolean is True;
        # a method  | we execute the method, and via its result, we fall again
        #           | in one of the above cases.
        #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # If p_class_.python does not define such an attribute, a default list
        # of roles defined in the config will be used.
        #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # An initiator object may dictate his own rules for instance creation
        if checkInitiator:
            # No need to check for an initiator in the context of a root class
            init = initiator or self.user.getInitiator()
            if init and getattr(init.field, 'creators', None):
                return self.user.hasRole(init.field.creators, init.o)
        # Get the Python class defined in the app
        class_ = class_.python
        # Get attribute "creators" on the class, or use the config
        creators = class_.creators if hasattr(class_, 'creators') \
                   else self.config.model.defaultCreators
        # If "creators" is a method, execute it
        if callable(creators): creators = creators(self.handler.tool)
        # Manage the "boolean" case
        if isinstance(creators, bool) or not creators: return creators
        # Manage the "roles" case
        for role in self.userRoles:
            if role in creators:
                return True

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Security checks on objects
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    def allows(self, o, permission='read', raiseError=False):
        '''Has the user p_permission on p_o ?'''
        r = self.user.hasPermission(permission, o)
        if not r and raiseError: raise Unauthorized()
        return r

    def mayAct(self, o):
        '''m_mayAct allows to hide the whole set of actions for an p_o(bject).
           Indeed, beyond workflow security, it can be useful to hide controls
           like "edit" icons/buttons. For example, if a user may only edit some
           Ref fields with add=True on an object, when clicking on "edit", he
           will see an empty edit form.'''
        return multicall(o, 'mayAct', True)

    def mayDelete(self, o):
        '''May the currently logged user delete this p_o(bject) ?'''
        r = self.allows(o, 'delete')
        if not r: return
        # An additional, user-defined condition, may refine the base permission
        return multicall(o, 'mayDelete', True)

    def mayEdit(self, o, permission='write', permOnly='specific',
                raiseError=False):
        '''May the user edit this object ? p_permission can be a field-specific
           permission. If p_permOnly is True, the additional user-defined
           condition (custom m_mayEdit) is not evaluated. If p_permOnly is
           "specific", this condition is evaluated only if the permission is
           specific (=not "write") If p_raiseError is True, if the user may not
           edit p_o, an error is raised.'''
        r = self.allows(o, permission, raiseError=raiseError)
        if not r: return
        if (permOnly == True) or \
           ((permOnly == 'specific') and (permission != 'write')): return r
        # An additional, user-defined condition, may refine the base permission
        r = multicall(o, 'mayEdit', True)
        if not r and raiseError:
            o.raiseUnauthorized(KO_PERM % (o.class_.name, o.id, permission))
        return r

    def mayView(self, o, permission='read', raiseError=False):
        '''May the user view this p_o(bject) ? p_permission can be a field-
           specific permission. If p_raiseError is True, if the user may not
           view p_o, an error is raised.'''
        r = self.allows(o, permission, raiseError=raiseError)
        if not r: return
        # An additional, user-defined condition, may refine the base permission
        r = multicall(o, 'mayView', True)
        if not r and raiseError:
            o.raiseUnauthorized(KO_PERM % (o.class_.name, o.id, permission))
        return r

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Login / logout
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    traverse['enter'] = True
    def enter(self, tool):
        '''Perform login'''
        user = self.user
        req = tool.req
        handler = tool.H()
        if user.isAnon():
            # Authentication failed
            label = 'login_ko'
            success = False
            msg = 'Authentication failed with login %s.' % (req.login or '')
        else:
            # Authentication succeeded
            label = 'login_ok'
            success = True
            msg = 'Logged in.'
        # Log the action
        tool.log(msg)
        # Redirect the user to the appropriate page
        if success:
            if user.changePasswordAtNextLogin:
                # Redirect to the page where the user can change its password
                back = '%s/edit?page=password' % user.url
                label = 'login_ok_change_password'
            elif req.goto:
                # The user came to its home page for authenticating: he must now
                # be redirected to the page at request key "goto".
                back = req.goto
            else:
                # Redirect to the app's home page
                back = user.tool.computeHomePage()
                info = req.authInfo
                # Carry custom authentication data when appropriate
                if info: back = '%s?authInfo=%s' % (back, info)
        else:
            # Stay on the same page
            back = tool.H().headers['Referer']
        # Redirect the user to the appropriate page
        tool.resp.goto(back, message=user.translate(label))

    traverse['leave'] = True
    def leave(self, tool):
        '''Perform logout'''
        handler = tool.H()
        # Disable the authentication cookie
        Cookie.disable(handler)
        # Log the action
        handler.log('app', 'info', 'Logged out.')
        # Redirect the user to the app's home page
        back = '%s/public' % tool.url if self.config.ui.discreetLogin \
                                      else self.config.server.getUrl(handler)
        handler.resp.goto(back, message=tool.translate('logout_ok'))

    def getLogoutUrl(self, tool, user):
        '''The "logout" URL may not be the standard Appy one if the app is
           behind a SSO reverse proxy.'''
        if user.source == 'sso': return self.config.security.sso.logoutUrl
        return '%s/guard/leave' % tool.url

    def getSelfRegisterJS(self, tool):
        '''Gets the JS code allowing to create a User instance for the purpose
           of self-registering.'''
        # Compute the URL to post the form to
        url = '%s/new' % tool.url
        return "javascript:post('%s', {'action': 'Create', 'className': " \
               "'User', 'nav': 'ref.tool.users.0.0'})" % url

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Password reinitialisation
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    traverse['askPasswordReinit'] = True
    def askPasswordReinit(self, tool):
        '''A user (anonymous) does not remember its password. Send him a mail
           containing a link that will trigger password re-initialisation.'''
        login = tool.req.rlogin
        _ = tool.translate
        if not login:
            return tool.goto(message=_('action_ko'))
        login = login.strip()
        user = tool.search1('User', login=login)
        message = _('reinit_mail_sent')
        if not user:
            # Return the message nevertheless. This way, malicious users can't
            # deduce information about existing users.
            return tool.goto(message=message)
        # If login is an email, use it. Else, use user.email instead.
        email = user.login
        if not String.EMAIL.match(email):
            email = user.email
        if not email:
            # Impossible to re-initialise the password
            return tool.goto(message=message)
        # Create a temporary file whose name is the user login and whose
        # content is a generated token.
        token = Password().generate()
        with (Path(putils.getOsTempFolder()) / login).open('w') as f:
            f.write(token)
        # Send an email
        initUrl = '%s/guard/doPasswordReinit?login=%s&token=%s' % \
                  (tool.url, login, token)
        subject = _('reinit_password')
        map = {'url':initUrl, 'siteUrl':tool.siteUrl}
        body= _('reinit_password_body', mapping=map, asText=True)
        tool.sendMail(email, subject, body)
        return tool.goto(message=message)

    traverse['doPasswordReinit'] = True
    def doPasswordReinit(self, tool):
        '''Performs the password re-initialisation'''
        req = tool.req
        login = req.login
        token = req.token
        _ = tool.translate
        # Check if such token exists in temp folder
        siteUrl = tool.siteUrl
        tokenFile = Path(putils.getOsTempFolder()) / login
        if tokenFile.exists():
            with tokenFile.open() as f:
                storedToken = f.read()
                if storedToken == token:
                    # A commit is required
                    tool.H().commit = True
                    # Generate a new password for this user
                    user = tool.search1('User', login=login)
                    newPassword = Password().generate()
                    user.password = newPassword
                    # Send the new password by email
                    recipient = user.getMailRecipient()
                    subject = _('new_password')
                    map = {'password': newPassword, 'siteUrl': siteUrl}
                    body = _('new_password_body', mapping=map, asText=True)
                    tool.sendMail(recipient, subject, body)
                    tokenFile.unlink()
                    return tool.goto(siteUrl, _('new_password_sent'))
        # If here, something went wrong
        return tool.goto(siteUrl, _('wrong_password_reinit'))

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # PXs
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # The login form
    pxLogin = Px('''
     <!-- Popup for reinitializing the password -->
     <div if="isAnon and config.security.activateForgotPassword"
          id="askPasswordReinitPopup" class="popup">
      <form id="askPasswordReinitForm" method="post"
            action=":'%s/guard/askPasswordReinit' % tool.url">
       <div align="center">
        <p>:_('app_login')</p>
        <input type="text" size="35" name="rlogin" id="rlogin" value=""/>
        <br/><br/>
        <input type="button" onclick="doAskPasswordReinit()"
               value=":_('ask_password_reinit')"/>
        <input type="button" onclick="closePopup('askPasswordReinitPopup')"
               value=":_('object_cancel')"/>
       </div>
      </form>
     </div>

     <!-- The login box -->
     <div class="loginBox"
          var="cfg=config.security;
               discreet=config.ui.discreetLogin"
          style=":'display:%s' % ('none' if discreet else 'block')">

      <!-- Allow to hide the box when relevant -->
      <img if="discreet" src=":url('close.svg')" style="float:right"
           onclick="toggleLoginBox(false)" class="clickable iconXS"/>

      <h1>:_('app_name')</h1>
      <center>:_('please_connect')</center>
      <div class="loginSpace"></div>
      <form id="loginForm" name="loginForm" method="post" class="login"
            action=":'%s/guard/enter' % tool.url">

       <!-- Login fields  -->
       <center><input type="text" name="login" id="login" value=""
                   placeholder=":_('app_login')" class="loginField"/></center>
       <center><input type="password" name="password" id="password"
                placeholder=":_('app_password')" class="loginField"/></center>

       <!-- The authentication context -->
       <x var="ctx=cfg.authContext"
          if="ctx and ctx.chooseOnLogin">:ctx.pxOnLogin</x>

       <!-- Additional authentification data to carry -->
       <input type="hidden" name="authInfo" id="authInfo"
              value=":req.authInfo or ''"/>

       <!-- Must we go to some page after login ? -->
       <input type="hidden" name="goto" value=":req.get('goto', '')"/>

       <!-- The "submit" button -->
       <div align="right">
         <input type="submit" name="submit" var="label=_('app_connect')"
                class="loginSubmit" value=":label" alt=":label"/></div>

       <!-- Forgot password ? -->
       <div class="lostPassword" if="cfg.activateForgotPassword">
         <a class="clickable"
         onclick="openPopup('askPasswordReinitPopup')">:_('forgot_password')</a>
       </div>

       <!-- Link to self-registration -->
       <p if="cfg.selfRegister">
        <span style="padding-right: 10px">:_('want_register')</span>
          <a style="font-size: 90%" class="clickable"
             onclick=":guard.getSelfRegisterJS(tool)">:_('app_register')</a>
       </p>
      </form>
     </div>''',

     js='''
       // Function triggered when the user asks password reinitialisation
       function doAskPasswordReinit() {
         // Check that the user has typed a login
         var f = document.getElementById('askPasswordReinitForm'),
             login = f.rlogin.value.replace(' ', '');
         if (!login) { f.rlogin.style.background = wrongTextInput; }
         else {
           closePopup('askPasswordReinitPopup');
           f.submit();
         }
       }''',

     css='''
      .loginBox {
         border: 2px solid #9fa8c1; padding: 35px; color: #335256;
         background-color:white; width: 333px; height: 373px;
         position: absolute; top: 50%; left: 50%; z-index: 10;
         transform: translate(-50%,-50%); -ms-transform: translate(-50%,-50%);
         box-shadow: 0 4px 8px 0 rgba(160, 104, 132, 0.2),
                     0 6px 20px 0 rgba(0, 0, 0, 0.19)
      }
      .loginBox a, .loginBox a:visited {
         font-weight: bold; letter-spacing: 1px }
      .loginBox h1 { padding-bottom: 0; text-align: center }
      .loginField { background-color: #4a5f73 !important;
         width: 310px !important; padding: 12px !important;
         margin: 6px 0  !important; color: #f3f3f7 }
      .loginSubmit { margin: 22px 0; padding: 7px }
      .lostPassword { padding: 10px 0 }
      /* Placeholder color for the login form */
      .loginBox ::-webkit-input-placeholder {
        color: white; font-weight: bold }
      .loginBox ::-moz-placeholder {
        color: white; font-weight: bold; font-size:120% }
      .loginBox :-ms-input-placeholder {
        color: white; font-weight: bold; font-size: 120% }
      .loginSpace { height: 35px }
      #rlogin { color: white }
     ''')
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
