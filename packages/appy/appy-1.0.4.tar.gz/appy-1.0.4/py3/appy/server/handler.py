'''A handler is responsible for handling a HTTP request'''

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
import threading, urllib.parse
from http.server import BaseHTTPRequestHandler

from appy.model.base import Base
from appy.server.guard import Guard
from appy.server.error import Error
from appy.server.static import Static
from appy.server.request import Request
from appy.model.utils import Object as O
from appy.server.response import Response
from appy.server.languages import Languages
from appy.server.traversal import Traversal
from appy.pod.actions import EvaluationError

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
TRANS_RETRY = 'Conflict occurred (%s). Replay transaction (#%d)...'
TRANS_ERR   = 'Unresolved conflict occurred (%s).'

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class MethodsCache(dict):
    '''A dict of method results, used to avoid executing more than once the same
       method, while handling a request. Every handler implements such a
       cache.'''

    def call(self, o, method, class_=None, cache=True):
        '''Call p_method on some p_o(bject). m_method can be an instance method
           on p_o; it can also be a static method. In this latter case, p_o is
           the tool and the static method, defined in p_class_, will be called
           with the tool as unique arg.

           If the method result is already in the cache, it will simply be
           returned. Else, the method will be executed, its result will be
           stored in the cache and returned.

           If p_cache is False, caching is disabled and the method is always
           executed.
        '''
        # Disable the cache for lambda functions
        name = method.__name__
        cache = False if name == '<lambda>' else cache
        # Call the method if cache is not needed
        if not cache: return method(o)
        # If first arg of method is named "tool" instead of the traditional
        # "self", we cheat and will call the method with the tool as first arg.
        # This will allow to consider this method as if it was a static method
        # on the tool.
        cheat = False
        if not class_ and (method.__code__.co_varnames[0] == 'tool'):
            prefix = o.class_.name
            o = o.tool
            cheat = True
        # Build the unique key allowing to store method results in the cache.
        # The key is of the form
        #                    <object id>:<method name>
        # In the case of a static method, "object id" is replaced with the class
        # name.
        if not cheat:
            prefix = class_.__name__ if class_ else str(o.iid)
        key = '%s:%s' % (prefix, name)
        # Return the cached value if present in the method cache
        if key in self: return self[key]
        # No cached value: call the method, cache the result and return it
        r = method(o)
        self[key] = r
        return r

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Handler:
    '''Abstract handler'''
    # A handler handles an incoming HTTP request. Class "Handler" is the
    # abstract base class for all concrete handlers, as defined hereafter.
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    #  HttpHandler | Handles HTTP requests. In the Appy HTTP server, every
    #              | request is managed by a thread. At server startup, a
    #              | configurable number of threads are run and are waiting for
    #              | requests. Every time a request hits the server, it is
    #              | assigned to a thread, that instantiates a handler and
    #              | manages the request.
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    #  InitHandler | When the Appy HTTP server starts, it is like if he had to
    #              | handle a virtual request. For that special case, an
    #              | instance of InitHandler is created.
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # In the following static attribute, we maintain a registry of the currently
    # instantiated handlers. Every handler is keyed the thread ID of the thread
    # that is running it.
    registry = {}

    # Make some names available here
    Static = Static

    @classmethod
    def add(class_, handler):
        '''Adds a new p_handler into the registry'''
        id = threading.get_ident()
        if id in class_.registry: return
        class_.registry[id] = handler

    @classmethod
    def remove(class_):
        '''Remove p_handler from the registry'''
        del class_.registry[threading.get_ident()]

    @classmethod
    def get(class_):
        '''Returns the handler for the currently executing thread'''
        return class_.registry[threading.get_ident()]

    # Make the Language class available in the handler namespace
    Languages = Languages

    def init(self):
        '''Define attributes which are common to any handler'''
        # Direct access to the app's configuration
        self.config = self.server.config
        # A lot of object methods are executed while handling a request. Dict
        # "method" hereafter caches method results: it avoids executing more
        # than once the same method. Only methods without args are cached, like
        # methods defined on field attributes such as "show".
        self.methods = MethodsCache()
        # Appy and apps may use the following object to cache any other element
        self.cache = O()
        # Create a guard, a transient object for managing security
        self.guard = Guard(self)

    def customInit(self):
        '''The app can define a method on its tool, named "initialiseHandler",
           allowing to perform custom initialisation on a freshly created
           handler (ie for caching some highly requested info).'''
        if not hasattr(self.tool, 'initialiseHandler'): return
        self.tool.initialiseHandler(self)

    def clientIP(self):
        '''Gets the IP address of the client'''
        # Check header key X-Forwarded-For first
        return self.headers.get('X-Forwarded-For') or self.client_address[0]

    # This dict allows, on a concrete handler, to find the data to log
    logAttributes = O(ip='self.clientIP()', port='str(self.client_address[1])',
      command='self.command', path='self.path', protocol='self.request_version',
      message='message', user='self.guard.userLogin',
      agent='self.headers.get("User-Agent")')

    def log(self, type, level, message=None):
        '''Logs, in the logger determined by p_type, a p_message at some
           p_level, that can be "debug", "info", "warning", "error" or
           "critical". p_message can be empty: in this case, the log entry will
           only contain the predefined attributes as defined by the
           appy.database.log.Config.'''
        server = self.server
        logger = getattr(server.loggers, type)
        cfg = getattr(server.config.log, type)
        # Get the parts of the message to dump
        r = []
        for part in cfg.messageParts:
            try:
                value = eval(getattr(Handler.logAttributes, part))
                if value is not None:
                    r.append(value)
            except AttributeError:
                pass
        # Call the appropriate method on the logger object corresponding to the
        # log p_level.
        getattr(logger, level)(cfg.sep.join(r))

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Inject class Handler on class Base to avoid circular package dependencies
Base.Handler = Handler

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class HttpHandler(Handler, BaseHTTPRequestHandler):
    '''Handles incoming HTTP requests'''

    protocol_version = 'HTTP/1.1'

    # This is a "real" request handler
    fake = False

    # Store, for every logged user, the date/time of its last access
    onlineUsers = {}

    # Every time a HTTP request hits the server, an instance of this class is
    # created to handle it. It inherits from BaseHTTPRequestHandler, the base
    # handler shipped with the Python standard library for handling HTTP
    # requests.

    def determineType(self):
        '''Determines the type of the request and split, in p_self.parts, the
           request path into parts.'''
        self.parsedPath = parsed = urllib.parse.urlparse(self.path.strip('/'))
        parts = parsed.path.split('/')
        # Remove any blank part among self.parts
        i = len(parts) - 1
        while i >= 0:
            if not parts[i]: del parts[i]
            i -= 1
        # No path at all means: dynamic content must be served (with a default
        # object and default method or PX applied on it).
        if not parts:
            self.static = False
        # If the first part of the path corresponds to the root static folder,
        # static content must be served.
        elif parts[0] == self.server.config.server.static.root:
            self.static = True
            del parts[0]
        # If the unique part corresponds to a file (ie, any name containing a
        # dot), it is static content, too (favicon.ico, robots.txt...)
        elif (len(parts) == 1) and ('.' in parts[0]):
            self.static = True
            # This kind of file must exist in the app
            parts.insert(0, self.server.config.model.appName)
        # In any other case, dynamic content must be served
        else:
            self.static = False
        self.parts = parts

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # The complete request handling is done within BaseHTTPRequestHandler's
    # constructor, including calls to methods do_GET and do_POST defined
    # hereafter. This constructor defines the following attributes.
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # request        | This is the low-level socket object that represents
    #                | the connection between the client and the server.
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # client_address | A tuple (client_host, client_port). "client_host" is
    #                | the name of the client host or its IP address, as a
    #                | string. p_client_port, an integer value, is the port
    #                | opened at the client side for the TCP connection.
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # server         | The Appy HTTP server instance, as defined by class
    #                | appy.server.Server.
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # Tell clients the server name and version
    server_version = 'Amnesiac/1.0'

    def init(self):
        '''Appy-specific handler initialisation for handling non-static content
           (called by m_do_GET or m_do_POST).'''
        # Create a Response object
        self.resp = Response(self)
        # An instance of appy.ui.validate.Validator will be created here, when
        # data sent via the ui requires to be validated.
        self.validator = None
        # Search criteria may be cached
        self.criteria = None
        # Must we commit data into the database ?
        self.commit = False
        # Set here a link to the tool. The handler object will be heavily
        # consulted by a plethora of objects during request handling. This is
        # why it is convenient to define such attributes on it.
        self.tool = self.dbConnection.root.objects.get('tool')
        # Call the base handler's method
        Handler.init(self)

    def manageGuardError(self, resp, traversal):
        '''A security-related error has occurred: the logged is not allowed to
           access the desired URL. If the user is anon, redirect him to the
           login page. Else, return an error.'''
        # Return the response content. In the case of a redirect, None will be
        # returned.
        if self.guard.user.isAnon():
            siteUrl = self.config.server.getUrl(self)
            gotoUrl = urllib.parse.quote('%s%s' % (siteUrl, self.path))
            resp.goto(url='%s/tool/home?goto=%s' % (siteUrl, gotoUrl),
                      message=self.tool.translate('please_authenticate'))
            r = None
        else:
            # Return a 403 error: unauthorized
            resp.code = 403
            r = Error.get(resp, traversal)
        return r

    def manageDatabaseRequest(self):
        '''Manage an HTTP request whose response must imply using the
           database and return the response content as a string.'''
        # Initialise p_self's base data structures
        self.init()
        # Run a traversal
        self.traversal = traversal = Traversal(handler=self)
        resp = self.resp
        try:
            r = traversal.run()
        except Traversal.Error as err:
            resp.code = 404
            r = Error.get(resp, traversal)
        except Guard.Error as err:
            r = self.manageGuardError(resp, traversal)
        except EvaluationError as err:
            if isinstance(err.originalError, Guard.Error):
                r = self.manageGuardError(resp, traversal)
            else:
                resp.code = 500
                r = Error.get(resp, traversal)
        return r

    def attemptDatabaseRequest(self):
        '''Tries to m_manageDatabaseRequest. Perform several attempts depending 
           on the occurrence of database conflict errors. Returns the content of
           the page to serve, as a string.'''
        maxAttempts = self.server.config.database.conflictRetries
        attempts = 0
        database = self.server.database
        while True:
            try:
                r = self.manageDatabaseRequest()
                # Perform a database commit when appropriate
                if self.commit: database.commit(self)
            except database.ConflictErrors as err:
                attempts += 1
                # Abort the transaction that could not be committed
                transaction.abort()
                # Return an error if is was the last attempt
                if attempts == maxAttempts:
                    self.log('site', 'error', TRANS_ERR % str(err))
                    self.resp.code = 503
                    r = Error.get(self.resp, self.traversal)
                    break
                else:
                    self.log('site', 'warning',
                             TRANS_RETRY % (str(err), attempts))
            except Exception as err:
                self.resp.code = 500
                r = Error.get(self.resp, self.traversal)
                break
            else:
                break
        return r

    def do_GET(self):
        '''Called when a HTTP GET request hits the server'''
        # Determine the type of the request: static or dynamic (boolean
        # self.static). Static content is any not-database-stored-and-editable
        # image, Javascript, CSS file, etc. Dynamic content is any request
        # reading and/or writing to/from the database.
        self.determineType()
        if self.static:
            # Manage static content
            code = Static.get(self)
        else:
            # Add myself to the registry of handlers
            Handler.add(self)
            # Initialise a database connection
            database = self.server.database
            self.dbConnection = database.openConnection()
            # Extract parameters and create a Request instance in p_self.req
            self.req = Request.create(self)
            # Compute dynamic content
            r = self.attemptDatabaseRequest()   
            # Build the HTTP response (if not done yet)
            try:
                resp = self.resp
                if not resp.built: resp.build(r)
                code = resp.code
            finally:
                # Close the DB connection
                database.closeConnection(self.dbConnection)
                # Remove myself from the registry (for now)
                Handler.remove()
        # Log this hit and the response code on the site log
        self.log('site', 'info', str(code))

    do_POST = do_GET

    def getLayout(self):
        '''Try to deduce the current layout from the traversal, if present'''
        traversal = getattr(self, 'traversal', None)
        if traversal: return traversal.context.layout

    def isAjax(self):
        '''Is this handler handling an Ajax request ?'''
        traversal = getattr(self, 'traversal', None)
        if traversal and traversal.context: return traversal.context.ajax

    def isPublished(self, o):
        '''Is object p_o the currently published object ?'''
        referer = self.headers.get('referer')
        return referer and (('/%s/' % o.id) in referer)

    # Disable standard log
    def log_message(self, format, *args): pass

    # Log base handler errors
    def log_error(self, format, *args):
        '''Called by the base handler to log any error occurring during base
           handler code execution like parsing the request.'''
        self.log('app', 'error', format % args)

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class InitHandler(Handler):
    '''Fake handler handling a virtual request representing server
       initialization.'''
    # Fake handler attributes
    client_address = ('127.0.0.1', 0)
    command = 'GET'
    path = '/'
    request_version = 'Appy/Startup'
    headers = {'User-Agent': 'system'}
    fake = True

    def __init__(self, server):
        '''Tries to define the same, or fake version of, a standard handler's
           attributes.'''
        # The Appy HTTP server instance
        self.server = server
        # Create fake Request and Response objects
        self.req = Request()
        self.resp = Response(self)
        # Call the base handler's method
        Handler.init(self)
        # Add myself to the registry of handlers
        Handler.add(self)
        # The following attributes will be initialised later
        self.dbConnection = None
        self.tool = None
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
