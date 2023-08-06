'''A "request" stores HTTP GET request parameters and/or HTTP POST form
   values.'''

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
import urllib.parse

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
BROKEN_PIPE = 'Broken pipe while serving %s.'

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Response:
    '''Represents the response that will be sent back to the client after having
       received a HTTP request.'''

    # Types of responses. Default is "html"
    types = {'html': 'text/html;charset=UTF-8',
             'xml':  'text/xml;charset=UTF-8',
             'json': 'application/json;charset=UTF-8'}

    def __init__(self, handler):
        # A link to the p_handler
        self.handler = handler
        # The HTTP code for the response
        self.code = 200
        # The message to be returned to the user
        self.message = None
        # Response headers
        if handler.fake:
            headers = {}
        else:
            headers = {'Server': handler.version_string(),
                       'Date': handler.date_time_string(),
                       'Content-type': Response.types['html'],
                       'Cache-Control': 'no-cache, no-store, must-revalidate',
                       'Expires': '0', 'Accept-Ranges': 'none',
                       'Connection': 'close'}
        self.headers = headers
        # The following attribute will become True as soon as this response
        # object will be built.
        self.built = False

    def setContentType(self, type):
        '''Sets the content type for this response'''
        self.headers['Content-type'] = Response.types.get(type) or type

    def setHeader(self, name, value):
        '''Adds (or replace) a HTTP header among response headers'''
        self.headers[name] = value

    def setCookie(self, name, value):
        '''Adds a cookie among response headers, in special key "Cookies" that
           will be converted to as many "Set-Cookie" HTTP header entries as
           there are entries at this key.

           If p_value is "deleted", the cookie is built in such a way that it
           will be immediately disabled by the browser.'''
        # Create entry "Cookies" in response headers if it does not exist
        if 'Cookies' not in self.headers:
            self.headers['Cookies'] = {}
        # Set the value for the cookie. A special value is defined if the
        # objective is to disable the cookie.
        if value == 'deleted': value = '%s; Max-Age=0' % value
        self.headers['Cookies'][name] = '%s; Path=/' % value

    def addMessage(self, message):
        '''Adds a message to p_self.message'''
        if self.message is None:
            self.message = message
        else:
            self.message = '%s<br/>%s' % (self.message, message)

    def goto(self, url=None, message=None):
        '''Redirect the user to p_url'''
        if message: self.addMessage(message)
        self.code = 303
        # Redirect to p_url or to the referer URL if no p_url has been given
        self.headers['Location'] = url or self.handler.headers['Referer']

    def build(self, content=None, complete=True):
        '''Build and sent the response back to the browser'''
        hasContent = content is not None
        # Convert p_content to bytes
        if hasContent: content = content.encode('utf-8')
        # If p_complete is False, this response object is not the main object
        # for producing the response to the browser. In that case, we will only
        # build selected sub-elements (the message and cookies) but not a
        # complete response.
        handler = self.handler
        # 1. The status line, including the response code
        if complete:
            handler.send_response_only(self.code)
        # 2. Add HTTP headers
        # 2.1. Add p_self.message as a cookie if present
        if self.message is not None:
            quoted = urllib.parse.quote(self.message)
            self.setCookie('AppyMessage', quoted)
        # 2.2. Add all headers
        for name, value in self.headers.items():
            # Manage special key containing cookies
            if name == 'Cookies':
                for key, v in value.items():
                    handler.send_header('Set-Cookie', '%s=%s' % (key, v))
            elif complete:
                # Manage any other key
                handler.send_header(name, value)
        # Add key "Content-Length"
        if complete:
            length = len(content) if hasContent else 0
            handler.send_header('Content-Length', length)
            handler.end_headers()
        # 3. Content, as bytes
        if complete and hasContent:
            try:
                handler.wfile.write(content)
            except BrokenPipeError:
                handler.log('app', 'error', BROKEN_PIPE % handler.path)
        if not complete:
            # Note this response as already been built
            self.built = True
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
