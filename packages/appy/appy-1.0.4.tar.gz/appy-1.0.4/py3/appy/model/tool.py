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
import re, urllib.parse
from pathlib import Path

import appy.ui
from appy.tr import po
from appy.px import Px
from appy import Config
from appy.server import Server
from appy.model.base import Base
from appy.model.user import User
from appy.data import nativeNames
from appy.utils.dates import Date
from appy.model.group import Group
from appy.model.fields import Show
from appy.model.query import Query
from appy.database import Database
from appy.ui.layout import Layouts
from appy.utils.mail import sendMail
from appy.ui.template import Template
from appy.model.fields.ref import Ref
from appy.model.searches import Search
from appy.model.fields.rich import Rich
from appy.model.fields import Initiator
from appy.model.carousel import Carousel
from appy.model.fields.phase import Page
from appy.model.page import Page as OPage
from appy.database.catalog import Catalog
from appy.model.fields.string import String
from appy.model.fields.action import Action
from appy.model.translation import Translation
from appy.model.fields.calendar import Calendar
from appy.model.fields.computed import Computed

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Tool(Base):
    '''Base class for the Appy tool, a persistent instance storing configuration
       elements and more, like users, group and translations.'''

    # Make some modules and classes available and/or traversable via the tool
    ui = appy.ui
    Date = Date
    OPage = OPage
    Search = Search
    
    # While most users have generally the read permission on the tool and
    # translations, they must not be allowed to consult tool/view and sub-pages.
    # Traversing tool/view is thus by default restricted to those having the
    # write permission on the tool.
    traverse = Base.traverse.copy()
    traverse.update({'ui':True, 'guard':True, 'Search':True,
                     'Database':True, 'Server':True, 'view': 'perm:write'})

    Initiator = Initiator

    # The tool is not indexed by default
    indexable = False

    @staticmethod
    def update(class_):
        '''Hide pages being not necessary'''
        fields = class_.fields
        for name in ('title', 'record'):
            fields[name].page.show = False

    #  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
    #  Tool initialisation
    #  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

    def checkServers(self, config):
        '''Log the names of servers (LDAP, mail...) this app wants to connect
           to. Servers declared as "testable" are contacted to check the app's
           connection to it.'''
        servers = []
        # Browse connected servers
        for cfg in (config.security.ldap, config.mail, config.security.sso):
            if not cfg: continue
            # Initialise and check this server config
            cfg.init(self)
            enabled = 'enabled' if cfg.enabled else 'disabled'
            # Test the connection to the server
            status = ''
            if cfg.enabled and cfg.testable:
                status = cfg.test(self)
                if status: status = ', ' + status
            servers.append('%s (%s%s)' % (cfg, enabled, status))
        if servers:
            self.log('Server(s) %s configured.' % ', '.join(servers))

    def init(self, handler, poFiles):
        '''Ensure all required tool sub-objects are present and coherent'''
        # Get the root database object from the current request p_handler
        root = handler.dbConnection.root
        # Create the default users if they do not exist
        for login, roles in User.defaultUsers.items():
            # Does this user exist in the database ?
            if login in root.objects:
                # Yes. Do not create it. But ensure, for "anon" and "system",
                # that they have no email.
                user = root.objects.get(login)
                if login != 'admin': user.email = None
            else:
                # No. Create it.
                user = self.create('users', secure=False, id=login, login=login,
                            password=login, roles=roles)
                self.log('User "%s" created.' % login)

        # Ensure group "admins" exists. This group is granted role "Manager",
        # the role with the highest level of prerogatives in Appy.
        if 'admins' not in root.objects:
            self.create('groups', secure=False, id='admins', login='admins',
                        title='Administrators', roles=['Manager'])
            self.log('Group "admins" created.')

        # Load Appy "po" files if we need to inject their values into
        # Translation objects. app's "po" files are already in p_poFiles.
        # Also load ext's "po" files if an ext is defined.
        config = handler.server.config
        ui = config.ui
        load = ui.loadTranslationsAtStartup
        extFiles = None
        if load:
            appyFiles = po.load(pot=False, languages=ui.languages)
            if config.ext:
                extPath = '%s/tr' % __import__(config.ext).__path__[0]
                extFiles = po.load(path=Path(extPath), pot=False,
                                   languages=ui.languages)

        # Ensure a Translation object exists for every supported language
        for language in ui.languages:
            if language not in root.objects:
                # Create a Translation file
                tr = self.create('translations', secure=False, id=language,
                            title='%s (%s)' % (language, nativeNames[language]),
                            sourceLanguage=ui.sourceLanguage)
                tr.updateFromFiles(appyFiles, poFiles, extFiles or {})
            else:
                tr = root.objects[language]
                if load: tr.updateFromFiles(appyFiles, poFiles, extFiles or {})

        # Check connected servers
        self.checkServers(config)

        # Import an Appy 0 site when relevant
        peers = config.peers
        if peers and peers.appy0:
            peers.appy0.pump(self)

        # Call method "onInstall" on the tool when available. This hook allows
        # an app to execute code on server initialisation.
        if hasattr(self, 'onInstall'): self.onInstall()

    #  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
    #  Page "main"
    #  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

    # Methods protecting visibility of tool pages and fields
    def forToolWriters(self):
        '''Some elements are only accessible to tool writers (ie Managers)'''
        if self.allows('write'): return Show.ER_

    def pageForToolWriters(self):
        '''Some tool pages are only accessible to tool writers (ie Managers)'''
        if self.allows('write'): return 'view'

    ta = {'label': 'Tool'}
    # Storing the Appy version on the tool (in the form of a string "x.y.z")
    # allows to trigger automatic migrations at server startup.
    appyVersion = String(show='view', **ta)

    # This hidden calendar is used for searches in "calendar" mode
    def calendarPreCompute(self, first, grid):
        '''Computes pre-computed information for the tool calendar'''
        # If this calendar is used as mode for a search, get this search
        req = self.req
        ctx = self.H().context
        mode = None
        if 'uiSearch' in ctx:
            # The search and related mode are already in the PX context
            mode = ctx.mode
        elif req.has_key('search') and req.has_key('className'):
            # Get the search and its mode from request keys
            className = req['className']
            tool = self.o
            search = self.o.getSearch(className, req['search'], ui=True)
            mode = search.Calendar(tool.getAppyClass(className), className,
                                   search, ctx.popup, tool)
            mode.init(req, ctx.dir)
        # Trigger the search via the mode
        if mode: mode.search(first, grid)
        return O(mode=mode)

    def calendarAdditionalInfo(self, date, preComputed):
        '''Renders the content of a given cell in the calendar used for
           searches' calendar mode.'''
        info = preComputed.mode.dumpObjectsAt(date)
        if info: return info

    calendar = Calendar(preCompute=calendarPreCompute, show=False,
                        additionalInfo=calendarAdditionalInfo, **ta)

    #  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
    #  Page "users"
    #  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

    userPage = Page('users', show=pageForToolWriters, label='Tool_page_users',
                    icon='pageUsers.svg')

    # The "main" page, reserved to technical elements, may be hidden by apps
    def getDefaultViewPage(self): return 'users'

    # Ref(User) will maybe be transformed into Ref(AppUser)
    users = Ref(User, multiplicity=(0,None), add=True, link=False,
      composite=True, back=Ref(attribute='toTool', show=False, layouts='f'),
      page=userPage, queryable=True, queryFields=('searchable','login','roles'),
      show=forToolWriters, showHeaders=True, actionsDisplay='right',
      shownInfo=User.listColumns, **ta)

    def getUserName(self, login=None, normalized=False):
        '''Gets the user name corresponding to p_login (or the currently logged
           user if None), or the p_login itself if the user does not exist
           anymore. If p_normalized is True, special chars in the first and last
           names are normalized.'''
        if not login:
            user = self.user
        else:
            user = self.search1('User', login=login)
            if not user: return login
        return user.getTitle(normalized=normalized)

    def doSynchronizeExternalUsers(self):
        '''Synchronizes the local User copies with a distant LDAP user base'''
        cfg, context = self.config.security.getLdap()
        if not cfg: raise Exception('LDAP config not found.')
        message = cfg.synchronizeUsers(self, sso=context)
        return True, message

    def showSynchronizeUsers(self):
        '''Show this button only if a LDAP connection exists and is enabled'''
        cfg, context = self.config.security.getLdap()
        if cfg and cfg.enabled: return 'buttons'

    synchronizeExternalUsers = Action(action=doSynchronizeExternalUsers,
      show=showSynchronizeUsers, confirm=True, page=userPage, **ta)

    #  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
    #  Page "groups"
    #  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

    # Ref(Group) will maybe be transformed into Ref(AppGroup)
    groups = Ref(Group, multiplicity=(0,None), add=True, link=False,
      composite=True, back=Ref(attribute='toTool', show=False,layouts='f'),
      page=Page('groups', show=pageForToolWriters, label='Tool_page_groups',
                icon='groups.svg'),
      show=forToolWriters, queryable=True, queryFields=('title', 'login'),
      showHeaders=True, actionsDisplay='inline',
      shownInfo=('title', 'login*20%|', 'roles*20%|'), **ta)

    #  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
    #  Page "translations"
    #  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

    pt = Page('translations', show=pageForToolWriters,
              label='Tool_page_translations', icon='pageTranslations.svg')

    # Ref(Translation) will maybe be transformed into Ref(AppTranslation)
    translations = Ref(Translation, multiplicity=(0,None), add=False,
      link=False, composite=True, show='view', page=pt, actionsDisplay='inline',
      back=Ref(attribute='toTool', show=False, layouts='f'), **ta)

    #  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
    #  Page "pages"
    #  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

    def showRootPages(self):
        '''Show root pages if the logged user is allowed to write the tool'''
        # The page may be edited only if there is at least one page defined (in
        # order to select it as default page).
        if not self.allows('write'): return
        return 'view' if self.isEmpty('pages') else True

    pp = Page('pages', show=showRootPages, label='Tool_page_pages',
              icon='pagePages.svg')

    pages = Ref(OPage, multiplicity=(0,None), add=True, link=False,
                composite=True, show=Show.VX, actionsDisplay='inline', page=pp,
                back=Ref(attribute='toTool', show=False, layouts='f'),
                numbered=True, showHeaders=True, shownInfo=OPage.listColumns,
                **ta)

    # Return the visible root pages
    def getRootPages(self): return OPage.getRoot(self)

    # The page, among "pages", being defined as the default one
    defaultPage = Ref(OPage, add=False, link=True, render='links', page=pp,
                      back=Ref(attribute='toTool2', show=False, layouts='f'),
                      show=lambda o: not o.isEmpty('pages'),
                      select=lambda o: o.pages, **ta)

    #  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
    #  Page "carousels"
    #  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

    pc = Page('carousels', show=lambda o: 'view' if o.allows('write') else None,
              label='Tool_page_carousels')

    carousels = Ref(Carousel, multiplicity=(0,None), add=True, link=False,
                    composite=True, show=Show.VX, actionsDisplay='inline',
                    back=Ref(attribute='toTool', show=False, layouts=Layouts.f),
                    layouts=Layouts.dv, page=pc, showHeaders=True, **ta)

    #  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
    #  Page "queries"
    #  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

    pq = Page('queries', show=lambda o: 'view' if o.allows('write') else None,
              label='Tool_page_queries')

    queries = Ref(Query, multiplicity=(0,None), add=True, link=False,
                  composite=True, show=Show.VX, actionsDisplay='inline',
                  back=Ref(attribute='toTool', show=False, layouts=Layouts.f),
                  layouts=Layouts.dv, page=pq, showHeaders=True,
                  shownInfo=Query.listColumns, **ta)

    #  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
    #  "admin" zone
    #  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

    def forAdmin(self):
        '''Returns page visibility for pages from the admin zone'''
        return 'view' if self.user.login == 'admin' else None

    onlineUsers = Computed(method=lambda o: User.getOnline(o), layouts='f',
      show='view', page=Page('online', phase='admin', show=forAdmin,
                             label='Tool_page_online'), **ta)

    serverInfo = Computed(method=Server.view, layouts='f',
      page=Page('server', phase='admin', show=forAdmin,
                label='Tool_page_server'), **ta)

    databaseInfo = Computed(method=Database.view, layouts='f',
      page=Page('database', phase='admin', show=forAdmin,
                label='Tool_page_database'), **ta)

    #  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
    #  Main methods
    #  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

    def sendMail(self, to, subject, body, attachments=None, replyTo=None):
        '''Sends a mail. See doc for appy.utils.mail.sendMail'''
        sendMail(self.config.mail, to, subject, body, attachments=attachments,
                 log=self.log, replyTo=replyTo)

    def computeHomePage(self):
        '''Compute the page that is shown to the user when he hits the app'''
        # Get the currently logged user
        user = self.user
        isAnon = user.isAnon()
        if isAnon and self.config.ui.discreetLogin:
            return '%s/public' % self.url
        # If the app defines a tool method names "getHomePage", call it
        r = None
        if hasattr(self, 'getHomePage'):
            r = self.getHomePage()
        if not r:
            # Bring anonymous users to tool/home, Managers to tool/view and
            # others to user/home.
            if isAnon:
                r = '%s/home' % self.url
            elif user.hasRole('Manager'):
                r = '%s/view' % self.url
            else:
                r = user.url
        return r

    def computeHomeObject(self, user, popup=False):
        '''The concept of "home object" is the object where the user must "be",
           even if he is "nowhere". For example, if the user is on a search
           screen, there is no contextual object (the tool excepted). In this
           case, if we have a home object for him, we will use it as contextual
           object, and its portlet menu will nevertheless appear: the user will
           not have the feeling of being lost.'''
        # If we are in the popup, we do not want any home object in the way
        if popup: return
        if hasattr(self, 'getHomeObject'):
            # If the app defines a method "getHomeObject", call it
            r = self.getHomeObject()
        else:
            # For managers, the home object is the tool. For others, there is
            # no default home object.
            if user.hasRole('Manager'): return self

    def getPageTitle(self, o):
        '''Returns content for tag html > head > title'''
        # Return the app name in some cases
        if not o or (o == self): return self.translate('app_name')
        # The page title is based on p_o's title
        r = o.getShownValue()
        # Ensure this is a string
        r = r if isinstance(r, str) else str(r)
        # Remove <br/> tags
        if '<br/>' in r: r = r[:r.index('<br/>')]
        # Add the page title if found
        if 'page' in self.req:
            label = '%s_page_%s' % (obj.class_.name, self.req.page)
            text = self.translate(label, blankOnError=True)
            if text:
                if r: r += ' :: '
                r += text
        return Px.truncateValue(res, width=100)

    def getGoogleAnalyticsCode(self, handler, config):
        '''If the config defines a Google Analytics ID, this method returns the
           Javascript code to be included in every page, allowing Google
           Analytics to work.'''
        # Disable Google Analytics when we are in debug mode
        if handler.server.mode == 'fg': return
        # Disable Google Analytics if no ID is found in the config.
        gaId = config.googleAnalyticsId
        if not gaId: return
        # Google Analytics must be enabled: return the chunk of Javascript
        # code specified by Google.
        code = "var _gaq = _gaq || [];\n" \
               "_gaq.push(['_setAccount', '%s']);\n" \
               "_gaq.push(['_trackPageview']);\n" \
               "(function() {\n" \
               "  var ga = document.createElement('script'); " \
               "ga.type = 'text/javascript'; ga.async = true;\n" \
               "  ga.src = ('https:' == document.location.protocol ? " \
               "'https://ssl' : 'http://www') + " \
               "'.google-analytics.com/ga.js';\n" \
               "  var s = document.getElementsByTagName('script')[0]; " \
               "s.parentNode.insertBefore(ga, s);\n" \
               "})();\n" % gaId
        return code

    def formatDate(self, date, format=None, withHour=True, language=None):
        '''Check doc in called method'''
        if not date: return
        return self.config.ui.formatDate(self, date, format, withHour, language)

    #  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
    #  PXs
    #  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

    # Hooks for defining a PX that proposes additional links or icons, before
    # and after the links/icons corresponding to top-level pages and icons.
    pxLinks = Px('')
    pxLinksAfter = Px('')

    # PX "home" is the default page shown for a standard Appy site, excepted
    # when discreet logins are enabled. In this latter case, PX "public",
    # hereafter, is more appropriate.
    home = Px('''
     <!-- Redirect the user when appropriate -->
     <x if="not isAnon or cfg.discreetLogin"
        var2="x=tool.goto(tool.computeHomePage())"></x>

     <!-- The home logo and text -->
     <div if="isAnon and not cfg.discreetLogin" class="homeText">
       <img src=":url('homeLogo')"/>
       <x if="not tool.isEmpty('defaultPage')">::tool.defaultPage.content</x>
     </div>''',

     css='''
      .homeText { position:fixed; left:45px; top:25px; color:|homeTextColor| }
      .homeText h1 { font-size: 300%; margin-left: -5px }
      .homeText h2 { font-size: 200% }
      .homeText p { font-size: 120%; margin: 0 }
      .homeText a, .homeText a:visited { color: #ffd8eb }
     ''',

     template=Template.px, hook='content', name='home')

    default = home

    # PX "public" shows one of the root pages (rp), or the default one if none
    # of them is specified . When discreet logins are enabled, the public page
    # is shown, loaded with the default page.
    public = Px('''
     <!-- The home text -->
     <div class="public"
          var="layout='view';
               root=tool.getObject(req.rp) if req.rp else tool.defaultPage">
      <x if="root">
       <x for="o in root.getChain()"
          var2="x=o.initialiseLocalPage(req)">:o.view</x>
      </x>
      <x if="not root">::_('no_default_page')</x>
     </div>''',
     template=Template.px, hook='content', name='public')

    # Disable tool removal
    def mayDelete(self): return
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
