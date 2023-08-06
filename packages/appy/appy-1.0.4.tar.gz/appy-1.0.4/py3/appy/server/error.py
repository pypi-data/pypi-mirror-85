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
from appy.px import Px
from appy.ui.js import Quote
from appy.utils import Traceback
from appy.ui.template import Template

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Error:
    '''Represents a server error'''

    byCode = {
     # Error 404: page not found
     404: {'label': 'not_found', 'px':
       Px('''<div>::msg</div>
           <div if="not isAnon and not popup">
            <a href=":tool.computeHomePage()">:_('app_home')</a>
           </div>''', template=Template.px, hook='content')},

     # Error 403: unauthorized
     403: {'label': 'unauthorized', 'px':
       Px('''<div><img src=":url('password.svg')" class="iconM"
                       style="margin-right: 5px"/><x>::msg</x></div>''',
          template=Template.px, hook='content')},

     # Error 500 server error
     500: {'label': 'server_error', 'px':
       Px('''<div><img src=":url('warning.svg')" class="iconM"
                       style="margin-right: 5px"/><x>::msg</x></div>''',
          template=Template.px, hook='content')},

     # Error 503: service unavailable. This error code is used by Appy when, due
     # to too many conflict errors (heavy load), the server cannot serve the
     # request.
     503: {'label': 'conflict_error',
         'px': Px('''<div>::msg</div>''', template=Template.px, hook='content')}
    }

    @classmethod
    def get(class_, resp, traversal):
        '''A server error just occurred. Try to return a nice error page. If it
           fails (ie, the error is produced in the main PX template), dump a
           simple traceback.'''
        # When managing an error, ensure no database commit will occur
        handler = traversal.handler
        handler.commit = False
        # Log the error
        code = resp.code if resp.code in Error.byCode else 500
        handler.log('app', 'error', message='%s on %s' % (code, handler.path))
        if code in (500, 503):
            handler.log('app', 'error', Traceback.get().strip())
        # For an admin, show a traceback. For normal humans, show a readable
        # error message.
        if traversal.user.hasRole('Manager'):
            content = Traceback.get(html=True)
        else:
            content = handler.tool.translate(Error.byCode[code]['label'])
        # If we are called by an Ajax request, return only the error message,
        # and set the return code to 200; else, browsers will complain.
        context = traversal.context
        if context and context.ajax:
            resp.code = 200
            return '<p>%s</p>' % content
        # Return the PX corresponding to the error code. For rendering it, get
        # the last PX context, or create a fresh one if there is no context.
        if not context:
            # Remove some variables from the request to minimise the possibility
            # that an additional error occurs while creating the PX context.
            req = handler.req
            if 'search' in req: del(req.search)
            traversal.context = context = traversal.createContext()
        context.msg = content
        try:
            return Error.byCode[code]['px'](context)
        except Exception as err:
            return '<p>%s</p>' % content
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
