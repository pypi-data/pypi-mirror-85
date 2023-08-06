'''Appy HTTP server'''

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
from itertools import count
from http.server import HTTPServer
import os, sys, time, socket, logging, pathlib, queue, atexit, threading, ctypes

from appy.px import Px
from appy.model import Model
from appy import utils, version
from appy.database import Database
from appy.utils import url as uutils
from appy.model.utils import Object as O
from appy.server.static import Config as StaticConfig
from appy.server.handler import HttpHandler, InitHandler

# Constants  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
START_CLASSIC = ':: Starting server ::'
START_CLEAN   = ':: Starting clean mode ::'
START_RUN     = ':: Starting run mode (%s) ::'
READY         = '%s:%s ready (process ID %d).'
STOP_CLASSIC  = ':: %s:%s stopped ::'
STOP_CLEAN    = ':: Clean end ::'
STOP_RUN      = ':: Run end ::'
APPY_VERSION  = 'Appy is "%s".'

# Server errors  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
CONN_RESET    = 'Connection reset by peer (client port %d).'
BROKEN_PIPE   = 'Broken pipe (client port %d).'

#  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#                        Pool of threads errors
#  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

#           THR = thread * WK = worker * SHUTD = shutdown

MIN_THR_KO    = 'At least one thread must be in use.'
THR_LIMITS_KO = 'killThreadLimit (%d) should be > hungThreadLimit (%d)'
SPAWN_IF_KO   = 'spawnIfUnder (%d) should be < than the number of threads (%d)'

INITIAL_WK    = 'Initial worker'
ADDED_WK      = 'Worker added in response to lack of idle workers'
WK_KILLED     = 'Worker added for replacing killed thread %s'
WK_REPLACED   = 'Voluntary replacement for thread %s'
WORK_DONE     = ' > handled by thread %s (%i tasks queued).'
CHECK_ADD_THR = 'No idle workers for task; checking if we need to make ' \
                'more workers'
SPAWNING      = 'No idle tasks and only %d busy task(s): adding %d more workers'
NO_SPAWNING   = 'No extra workers needed (%d busy worker(s))'
CULL_WORKERS  = 'Culling %s extra workers. %s idle workers present: %s'
CULL_KILLED   = 'Killed thread %s no longer around'
KILL_KO       = 'PyThreadState_SetAsyncExc failed'
KILLING_THR   = 'Killing thread with ID=%s...'
KILLED_HUNGED = 'Workers killed forcefully'
WK_TO_KILL    = 'Killing worker %s... (working on task for %i seconds)'
HUNG_STATUS   = "killHungThreads status: %d threads (%d working, %d idle, " \
                "%d starting), average time %s, maxTime %.2fsec, killed %d " \
                "worker(s)."
ZOMBIES_FOUND = 'Zombie thread(s) found: %s.'
EXITING       = 'Exiting process because %s zombie threads is more than %s limit.'
NEW_WORKER    = 'Started new worker %s: %s'
STOPPING_THR  = 'Thread %s processed %i requests (limit %s); stopping it'
SHUTD_RECV    = 'Worker %s is asked to shutdown'
SHUTD_POOL    = 'Shutting down the threadpool (%d threads)'
SHUTD_HUNG    = "%s worker(s) didn't stop properly, and %s zombie(s)"
SHUTD_OK      = 'All workers stopped'
SHUTD_FORCED  = 'Forcefully exiting process'
SHUTD_F_OK    = 'All workers eventually killed'

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Config:
    '''HTTP server configuration for a Appy site'''
    def __init__(self):
        # The server address
        self.address = '0.0.0.0'
        # The server port
        self.port = 8000
        # The protocol in use
        self.protocol = 'http'
        # Configuration for static content (set by m_set below)
        self.static = None
        # ~~~
        # Options for the pool of threads
        # ~~~
        # The initial number of threads to run
        self.threads = 5
        # The maximum number of requests a worker thread will process before
        # dying (and replacing itself with a new worker thread).
        self.maxRequests = 100
        # The number of seconds a thread can work on a task before it is
        # considered hung (stuck).
        self.hungThreadLimit = 30
        # The number of seconds a thread can work before you should kill it
        # (assuming it will never finish).
        self.killThreadLimit = 600 # 10 minutes
        # The length of time after killing a thread that it should actually
        # disappear. If it lives longer than this, it is considered a "zombie".
        # Note that even in easy situations killing a thread can be very slow.
        self.dyingLimit = 300 # 5 minutes
        # If there are no idle threads and a request comes in, and there are
        # less than this number of *busy* threads, then add workers to the pool.
        # Busy threads are threads that have taken less than "hungThreadLimit"
        # seconds so far. So if you get *lots* of requests but they complete in
        # a reasonable amount of time, the requests will simply queue up (adding
        # more threads probably wouldn't speed them up). But if you have lots of
        # hung threads and one more request comes in, this will add workers to
        # handle it.
        self.spawnIfUnder = 5
        # If there are more zombies than the following number, just kill the
        # process. This is only good if you have a monitor that will
        # automatically restart the server. This can clean up the mess.
        self.maxZombieThreadsBeforeDie = 0 # Disabled
        # Every X requests (X being the number stored in the following
        # attribute), check for hung threads that need to be killed, or for
        # zombie threads that should cause a restart.
        self.hungCheckPeriod = 100

    def isIPv6(self):
        '''Is IP v6 in use ?'''
        host = self.address
        return (host.count(':') > 1)  or ('[' in host)

    def set(self, appFolder):
        '''Sets site-specific configuration elements'''
        appPath = pathlib.Path(appFolder)
        self.static = StaticConfig(appPath)

    def getUrl(self, handler, relative=False):
        '''Returns the base URL for URLs produced by this Appy server'''
        if relative:
            base = ''
        else:
            # Use, in that order, keys 'X-Forwarded-Host' or 'Host' if found
            # among the HTTP header.
            headers = handler.headers
            host = headers.get('X-Forwarded-Host') or headers.get('Host')
            if not host:
                host = self.address
                if self.port != 80:
                    host += ':%d' % self.port
            # Get protocol from header key 'X-Forwarded-Proto' when present
            protocol = headers.get('X-Forwarded-Proto') or self.protocol
            # Build the base of the URL
            base = '%s://%s' % (protocol, host)
        # Add a potential path prefix to URLs
        prefix = headers.get('X-Forwarded-Prefix')
        prefix = '/%s' % prefix if prefix else ''
        return '%s%s' % (base, prefix)

    def inUse(self):
        '''Returns True if (self.address, self.port) is already in use'''
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Set option "Reuse" for this socket. This will prevent us to get a
        # "already in use" error when TCP connections are left in TIME_WAIT
        # state.
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            s.bind((self.address, self.port))
        except socket.error as e:
            if e.errno == 98:
                return True
        s.close()

    def check(self):
        '''Ensure this config is valid'''
        # At least one thread must be specified
        assert (self.threads > 1), MIN_THR_KO
        # Ensure limits are consistent
        kill = self.killThreadLimit
        hung = self.hungThreadLimit
        assert (not kill or (kill >= hung)), (THR_LIMITS_KO % (kill, hung))
        # Ensure number of threads are consistent
        spawnIf = self.spawnIfUnder
        threads = self.threads
        assert spawnIf <= threads, (SPAWN_IF_KO % (spawnIf, threads))

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class ThreadPool:
    '''Pool of threads for efficiently managing incoming client requests'''

    # This excellent code is copied from the Paste project, many many thanks.
    # https://github.com/cdent/paste/blob/master/paste/httpserver.py

    # This pool manages a list of thread workers managing cliet requests via a
    # queue of callables.

    # The pool keeps a notion of the status of its worker threads.
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # If...  | The worker thread ...
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # idle   | does nothing
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # busy   | is doing its job
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # hung   | has been doing a job for too long
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # dying  | is a hung thread that has been killed, but hasn't died quite yet
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # zombie | that we've tried to kill but isn't dead yet
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # The pool also maintains, in attribute "tracked", a dictionary with these
    # keys and lists of thread IDs that fall in that status. All keys will be
    # present, even if they point to emty lists.

    # Hung threads are threads that have been busy more than
    # config.hungThreadLimit seconds. Hung threads are killed when they live
    # longer than config.killThreadLimit seconds. A thread is then considered
    # dying for config.dyingLimit seconds, if it is still alive after that it is
    # considered a zombie.

    # When there are no idle workers and a request comes in, another worker
    # *may* be spawned. If there are less than config.spawnIfUnder threads in
    # the busy state, another thread will be spawned.  So if the limit is 5, and
    # there are 4 hung threads and 6 busy threads, no thread will be spawned.

    # When there are more than config.maxZombieThreadsBeforeDie zombie threads,
    # a SystemExit exception will be raised, stopping the server. Use 0 or None
    # to never raise this exception. Zombie threads *should* get cleaned up, but
    # killing threads is no necessarily reliable. This is turned off by default,
    # since it is only a good idea if you've deployed the server with some
    # process watching from above (something similar to daemontools or zdaemon).

    # Each worker thread only processes config.maxRequests tasks before it dies
    # and replaces itself with a new worker thread.

    SHUTDOWN = object()

    # This flag specifies if, when the server terminates, all in-progress client
    # connections should be droppped.
    daemon = False

    def __init__(self, server, config):
        '''Initialise the pool's data stuctures'''
        # A reference to the p_server
        self.server = server
        self.logger = server.loggers.app
        # The server config
        self.config = config
        # The Queue object allowing inter-thread communication
        self.queue = queue.Queue()
        # The list of Thread instances
        self.workers = []
        self.workersCount = count()
        # Dict storing info about thread's statuses
        self.tracked = {} # ~{i_threadId: (i_timeStarted, info)}~
        # IDs of threads being idle
        self.idleWorkers = []
        # Dict of threads having been killed, but maybe aren't dead yet
        self.dyingThreads = {} # ~{i_threadId: (i_time, Thread)}~
        # This is used to track when we last had to add idle workers
        # (storing time.time()); we shouldn't cull extra workers until some time
        # has passed (config.hungThreadLimit) since workers were added.
        self.lastAddedNewIdleWorkers = 0
        # Number of requests received since last check for hunged threads
        self.requestsSinceLastHungCheck = 0
        if not ThreadPool.daemon:
            atexit.register(self.shutdown)
        # Create the threads
        for i in range(config.threads):
            self.addWorker(message=INITIAL_WK)

    def debug(self, message):
        '''Logs a message'''
        self.logger.debug(message)

    def addTask(self, task):
        '''Adds a task to the queue'''
        # Kill hung threads if it's time to do it
        cfg = self.config
        if cfg.hungCheckPeriod:
            self.requestsSinceLastHungCheck += 1
            if self.requestsSinceLastHungCheck > cfg.hungCheckPeriod:
                self.requestsSinceLastHungCheck = 0
                self.killHungThreads()
        # Add workers when relevant
        if not self.idleWorkers and cfg.spawnIfUnder:
            # spawnIfUnder can come into effect. Count busy threads.
            busy = 0
            now = time.time()
            self.debug(CHECK_ADD_THR)
            for worker in self.workers:
                # Ignore uninitialized threads
                if not hasattr(worker, 'thread_id'): continue
                started, info = self.tracked.get(worker.thread_id, (None,None))
                if started is not None:
                    if (now - started) < cfg.hungThreadLimit:
                        busy += 1
            if cfg.spawnIfUnder > busy:
                delta = cfg.spawnIfUnder - busy
                self.debug(SPAWNING % (busy, delta))
                self.lastAddedNewIdleWorkers = time.time()
                for i in range(delta):
                    self.addWorker(message=ADDED_WK)
            else:
                self.debug(NO_SPAWNING % busy)
        # Kill supernumerary workers when relevant
        idle = len(self.idleWorkers)
        if (len(self.workers) > cfg.threads) and (idle > 3) and \
           ((time.time()-self.lastAddedNewIdleWorkers) > cfg.hungThreadLimit):
            # We've spawned workers in the past, but they aren't needed anymore;
            # kill off some.
            kill = len(self.workers) - cfg.threads
            self.debug(CULL_WORKERS % (kill, idle, self.idleWorkers))
            for i in range(kill):
                self.queue.put(self.SHUTDOWN)
        # Add the task to the queue
        self.queue.put(task)

    def cullThreadIfDead(self, id):
        '''Cull thread with this p_id if it does not exist anymore. Return True
           if the thread has been culled.'''
        if self.threadExists(id): return
        self.debug(CULL_KILLED % id)
        try:
            del self.dyingThreads[id]
            return True
        except KeyError:
            pass

    def getTracked(self, formatted=True):
        '''Returns a dict summarizing info about the threads in the pool'''
        r = O(idle=[], busy=[], hung=[], dying=[], zombie=[])
        now = time.time()
        cfg = self.config
        for worker in self.workers:
            # Ignore threads not being fully started up
            if not hasattr(worker, 'thread_id'): continue
            started, info = self.tracked.get(worker.thread_id, (None, None))
            if started is not None:
                attr = 'hung' if (now-started) > cfg.hungThreadLimit else 'busy'
            else:
                attr = 'idle'
            getattr(r, attr).append(worker)
        # Add dying and zombies
        for id, (killed, worker) in self.dyingThreads.items():
            culled = self.cullThreadIfDead(id)
            if culled: continue
            attr = 'zombie' if now - killed > cfg.dyingLimit else 'dying'
            getattr(r, attr).append(worker)
        if formatted:
            # Return it as a XHTML table
            rows = []
            for name, threads in r.items():
                info = []
                for thread in threads:
                    info.append('%s - %s' % (thread.getName(), thread.ident))
                rows.append('<tr><th>%s</th><td>%s</td></tr>' % \
                            (name, '<br/>'.join(info)))
            r = '<table class="small"><tr><th>Type</th><th>Threads</th></tr>' \
                '%s</table>' % '\n'.join(rows)
        return r

    def killWorker(self, id):
        '''Removes from the pool, the worker whose thread ID is p_id and
           replaces it with a new worker thread.'''
        # This should only be done for mis-behaving workers
        thread = threading._active.get(id)
        # Kill the thread by raising SystemExit
        tid = ctypes.c_long(id)
        r = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid,
              ctypes.py_object(SystemExit))
        if r == 0:
            pass # Invalid thread id: it has died in the mean time
        elif r != 1:
            # If it returns a number greater than one, you're in trouble,
            # and you should call it again with exc=NULL to revert the effect.
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, 0)
            raise SystemError(KILL_KO)
        # Remove any reference to the thread in the pool
        try:
            del self.tracked[id]
        except KeyError:
            pass
        self.debug(KILLING_THR % id)
        if thread in self.workers:
            self.workers.remove(thread)
        self.dyingThreads[id] = (time.time(), thread)
        self.addWorker(message=WK_KILLED % id)

    def addWorker(self, *args, **kwargs):
        index = next(self.workersCount)
        worker = threading.Thread(target=self.workerMethod, args=args,
                                  kwargs=kwargs, name=("worker %d" % index))
        worker.setDaemon(ThreadPool.daemon)
        worker.start()

    def threadExists(self, id):
        '''Returns True if a thread with this p_id exists'''
        return id in threading._active

    def killHungThreads(self):
        '''Tries to kill any hung thread'''
        cfg = self.config
        # No killing should occur in that case
        if not cfg.killThreadLimit: return
        now = time.time()
        maxTime = totalTime = idle = starting = working = killed = 0
        for worker in self.workers:
            # Ignore uninitialized threads
            if not hasattr(worker, 'thread_id'):
                starting += 1
                continue
            id = worker.thread_id
            started, info = self.tracked.get(id, (None, None))
            if started is None:
                # Must be idle
                idle += 1
                continue
            lifetime = now - started
            working += 1
            maxTime = max(maxTime, lifetime)
            totalTime += lifetime
            if lifetime > cfg.killThreadLimit:
                self.logger.warn(WK_TO_KILL % (id, lifetime))
                self.killWorker(id)
                killed += 1
        average = '%.2fsec' % (totalTime / working) if working else 'N/A'
        self.debug(HUNG_STATUS % ((idle + starting + working), working, idle, \
                                  starting, average, maxTime, killed))
        self.checkMaxZombies()

    def checkMaxZombies(self):
        '''Checks if we've reached cfg.maxZombieThreadsBeforeDie; if so, kill
           the entire process.'''
        cfg = self.config
        if not cfg.maxZombieThreadsBeforeDie: return
        found = []
        now = time.time()
        for id, (killed, worker) in self.dyingThreads.items():
            culled = self.cullThreadIfDead(id)
            if culled: continue
            if now - killed > cfg.dyingLimit:
                found.append(id)
        if found:
            self.debug(ZOMBIES_FOUND % ', '.join(found))
        count = len(found)
        if count > cfg.maxZombieThreadsBeforeDie:
            self.logger.error(EXITING % (count, cfg.maxZombieThreadsBeforeDie))
            self.shutdown(10)
            raise SystemExit(3)

    def workerMethod(self, message=None):
        '''Method executed by a worker thread'''
        cfg = self.config
        thread = threading.currentThread()
        id = thread.thread_id = threading.get_ident()
        self.workers.append(thread)
        self.idleWorkers.append(id)
        processed = 0 # The number of processed requests
        replace = False # Must we replace the thread ?
        self.debug(NEW_WORKER % (id, message))
        try:
            while True:
                # Stop myself if I have managed the maximum number of requests
                max = cfg.maxRequests
                if max and (processed > max):
                    # Replace me then die
                    self.debug(STOPPING_THR % (id, processed, max))
                    replace = True
                    break
                # Get the job I have to do
                runnable = self.queue.get()
                if runnable is ThreadPool.SHUTDOWN:
                    # This is not a job, but a shutdown command
                    self.debug(SHUTD_RECV % id)
                    break
                # Note myself as working
                try:
                    self.idleWorkers.remove(id)
                except ValueError:
                    pass
                self.tracked[id] = [time.time(), None]
                processed += 1
                # Perform my task
                runnable()
                self.debug(WORK_DONE % (id, self.queue.qsize()))
                # Note myself again as being "idle"
                try:
                    del self.tracked[id]
                except KeyError:
                    pass
                self.idleWorkers.append(id)
        finally:
            try:
                del self.tracked[id]
            except KeyError:
                pass
            try:
                self.idleWorkers.remove(id)
            except ValueError:
                pass
            try:
                self.workers.remove(thread)
            except ValueError:
                pass
            try:
                del self.dyingThreads[id]
            except KeyError:
                pass
            if replace:
                self.addWorker(message=WK_REPLACED % id)

    def shutdown(self, forceQuitTimeout=0):
        '''Shutdown the queue (after finishing any pending requests)'''
        count = len(self.workers)
        self.debug(SHUTD_POOL % count)
        # Add a shutdown request for every worker
        for i in range(count):
            self.queue.put(ThreadPool.SHUTDOWN)
        # Wait for each thread to terminate
        hung = []
        for worker in self.workers:
            worker.join(0.5)
            if worker.is_alive():
                hung.append(worker)
        zombies = []
        for id in self.dyingThreads:
            if self.threadExists(id):
                zombies.append(id)
        if hung or zombies:
            self.debug(SHUTD_HUNG % (len(hung), len(zombies)))
            if hung:
                for worker in hung:
                    self.killWorker(worker.thread_id)
                self.debug(KILLED_HUNGED)
            if forceQuitTimeout:
                timedOut = False
                needForceQuit = bool(zombies)
                for worker in self.workers:
                    if not timedOut and worker.is_alive():
                        timedOut = True
                        worker.join(forceQuitTimeout)
                    if worker.is_alive():
                        # Worker won't die
                        needForceQuit = True
                if needForceQuit:
                    # Remove the threading atexit callback
                    for callback in list(atexit._exithandlers):
                        func = getattr(callback[0], 'im_func', None)
                        if not func:
                            continue
                        globs = getattr(func, 'func_globals', {})
                        mod = globs.get('__name__')
                        if mod == 'threading':
                            atexit._exithandlers.remove(callback)
                    atexit._run_exitfuncs()
                    self.debug(SHUTD_FORCED)
                    os._exit(3)
                else:
                    self.debug(SHUTD_F_OK)
        else:
            self.debug(SHUTD_OK)

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Server(HTTPServer):
    '''Appy HTTP server'''

    def logStart(self, method):
        '''Logs the appropriate "ready" message, depending on p_self.mode'''
        # Uncomment this line to get more debug info from the pool of threads
        #self.loggers.app.setLevel(logging.DEBUG)
        if self.classic:
            text = START_CLASSIC
        elif self.mode == 'clean':
            text = START_CLEAN
        elif self.mode == 'run':
            text = START_RUN % method
        logger = self.loggers.app
        logger.info(text)
        logger.info(APPY_VERSION % version.verbose)

    def logShutdown(self):
        '''Logs the appropriate "shutdown" message, depending on p_self.mode'''
        if self.classic:
            cfg = self.config.server
            text = STOP_CLASSIC % (cfg.address, cfg.port)
        elif self.mode == 'clean':
            text = STOP_CLEAN
        elif self.mode == 'run':
            text = STOP_RUN
        self.loggers.app.info(text)

    def __init__(self, config, mode, method=None, ext=None):
        # p_config is the main app config
        self.config = config
        self.appyVersion = version.verbose
        # If an ext is there, load it
        if ext: __import__(ext.name)
        # Ensure the config is valid
        config.check()
        # p_mode can be:
        # ----------------------------------------------------------------------
        # "fg"     | Server start, in the foreground (debug mode)
        # "bg"     | Server start, in the background
        # "clean"  | Special mode for cleaning the database
        # "run"    | Special mode for executing a single p_method on the
        #          | application tool.
        # ----------------------------------------------------------------------
        # Modes "clean" and "run" misuse the server to perform a specific task.
        # In those modes, the server is not really started (it does not listen
        # to a port) and is shutdowned immediately after the task has been
        # performed.
        # ----------------------------------------------------------------------
        self.mode = mode
        self.classic = mode in ('fg', 'bg')
        # Initialise the loggers
        cfg = config.log
        self.loggers = O(site=cfg.getLogger('site'),
                         app=cfg.getLogger('app', mode != 'bg'))
        self.logStart(method)
        try:
            # Load the application model. As a side-effect, the app's po files
            # were also already loaded.
            self.model, poFiles = config.model.get(config, self.loggers.app)
            # Initialise the HTTP server
            cfg = config.server
            self.pool = None
            if self.classic:
                HTTPServer.__init__(self, (cfg.address, cfg.port), HttpHandler)
                family = socket.AF_INET6 if cfg.isIPv6() else socket.AF_INET
                HTTPServer.address_family = family
                # Start the pool of threads when relevant
                if mode == 'bg':
                    self.pool = ThreadPool(self, cfg)
            # Create the initialisation handler
            handler = InitHandler(self)
            # Initialise the database. More precisely, it connects to it and
            # performs the task linked to p_self.mode.
            config.database.getDatabase(self, handler, poFiles, method=method)
            # Initialise the static configuration
            cfg.static.init(config.ui)
            # Remove the initialisation handler
            InitHandler.remove()
        except (Model.Error, Database.Error) as err:
            self.abort(err)
        except Exception:
            self.abort()
        # The current user login
        self.user = 'system'
        # The server is ready
        if self.classic:
            self.loggers.app.info(READY % (cfg.address, cfg.port, os.getpid()))

    def process_request(self, request, client_address):
        '''Processes an incoming p_request'''
        if (self.mode == 'fg') or (self.pool is None):
            # In debug mode, process the request in the single, main thread
            self.process_request_in_thread(request, client_address)
        else:
            # Use the pool of threads. Queue the request to be processed by one
            # of the threads from the pool.
            # ~~~
            # This sets the socket to blocking mode (and no timeout) since it
            # may take the thread pool a little while to get back to it. (This
            # is the default but since we set a timeout on the parent socket so
            # that we can trap interrupts we need to restore this).
            request.setblocking(1)
            self.pool.addTask(
              lambda: self.process_request_in_thread(request, client_address))

    def process_request_in_thread(self, request, client_address):
        '''Processes an incoming p_request'''
        try:
            self.finish_request(request, client_address)
        except ConnectionResetError:
            self.loggers.app.error(CONN_RESET % client_address[1])
        except BrokenPipeError:
            self.loggers.app.error(BROKEN_PIPE % client_address[1])
        except Exception:
            self.handle_error(request, client_address)
        finally:
            self.shutdown_request(request)

    def handle_error(self, request, client_address):
        '''Handles an exception raised while a handler processes a request'''
        self.logTraceback()

    def logTraceback(self):
        '''Logs a traceback'''
        self.loggers.app.error(utils.Traceback.get().strip())

    def shutdown(self):
        '''Normal server shutdown'''
        # Logs the shutdown
        self.logShutdown()
        # Shutdown the pool of threads
        if self.pool:
            self.pool.shutdown()
        # Shutdown the loggers
        logging.shutdown()
        # Shutdown the database
        database = self.database
        if database: database.close()
        # Call the base method
        if self.classic:
            HTTPServer.shutdown(self)

    def abort(self, error=None):
        '''Server shutdown following an error'''
        # Log the error, or the full traceback if requested
        if error:
            self.loggers.app.error(error)
        else:
            self.logTraceback()
        # Shutdown the loggers
        logging.shutdown()
        # If the database was already there, close it
        if hasattr(self, 'database'): self.database.close()
        # Exit
        sys.exit(1)

    def buildUrl(self, handler, name='', base=None, ram=False, bg=False):
        '''Builds the full URL of a static resource, like an image, a Javascript
           or a CSS file, named p_name. If p_ram is True, p_base is ignored and
           replaced with the RAM root. If p_bg is True, p_name is an image that
           is meant to be used in a "style" attribute for defining the
           background image of some XHTML tag.'''
        # Unwrap the server part of the config
        config = self.config
        cfg = config.server
        # Complete the name when appropriate
        if name:
            # If no extension is found in p_name, we suppose it is a PNG image
            name = name if '.' in name else '%s.png' % name
            if base is None:
                # Get the base folder containing the resource
                base = config.ui.images.get(name) or 'appy'
            name = '/%s' % name
        else:
            base = base or 'appy'
        # Patch p_base if the static resource is in RAM
        if ram: base = cfg.static.ramRoot
        r = '%s/%s/%s%s' % (cfg.getUrl(handler), cfg.static.root, base, name)
        if not bg: return r
        suffix = ';background-size:%s' % bg if isinstance(bg, str) else ''
        return 'background-image:url(%s)%s' % (r, suffix)

    def getUrlParams(self, params):
        '''Return the URL-encoded version of dict p_params as required by
           m_getUrl.'''
        # Manage special parameter "unique"
        if 'unique' in params:
            if params['unique']:
                params['_hash'] = '%f' % time.time()
            del(params['unique'])
        return uutils.encode(params, ignoreNoneValues=True)

    def getUrl(self, o, sub=None, relative=False, **params):
        '''Gets the URL of some p_o(bject)'''
        # Parameters are as follows.
        # ----------------------------------------------------------------------
        # sub      | If specified, it denotes a part that will be added to the
        #          | object base URL for getting one of its specific sub-pages,
        #          | like "view" or "edit".
        # ----------------------------------------------------------------------
        # relative | If True, the base URL <protocol>://<domain> will not be
        #          | part of the result.
        # ----------------------------------------------------------------------
        # params   | Every entry in p_params will be added as-is as a parameter
        #          | to the URL, excepted if the value is None or key is
        #          | "unique": in that case, its value must be boolean: if
        #          | False, the entry will be removed; if True, it will be
        #          | replaced with a parameter whose value will be based on
        #          | time.time() in order to obtain a link that has never been
        #          | visited by the browser.
        # ----------------------------------------------------------------------
        # The presence of parameter "popup=True" in the URL will open the
        # corresponding object-related page in the Appy iframe, in a
        # minimalistic way (ie, without portlet, header and footer).
        # ----------------------------------------------------------------------
        # The base app URL
        r = self.config.server.getUrl(o.H(), relative=relative)
        # Add the object ID
        r = '%s/%s' % (r, o.id)
        # Manage p_sub
        r = '%s/%s' % (r, sub) if sub else r
        # Manage p_params
        if not params: return r
        return '%s?%s' % (r, self.getUrlParams(params))

    def patchUrl(self, url, **params):
        '''Modifies p_url and injects p_params into it. They will override their
           homonyms that would be encoded within p_url.'''
        if not params: return url
        # Extract existing parameters from p_url and update them with p_params
        r, parameters = uutils.split(url)
        if parameters:
            parameters.update(params)
        else:
            parameters = params
        return '%s?%s' % (r, self.getUrlParams(parameters))

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    #                                 PXs
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    view = Px('''
     <x var="cfg=config.server; server=handler.server">
      <h2>Server configuration</h2>
      <table class="small">
       <tr><th>Server</th><td>:cfg.address</td></tr>
       <tr><th>Port</th><td>:cfg.port</td></tr>
       <tr><th>Protocol</th><td>:cfg.protocol</td></tr>
       <tr><th>Mode</th><td>:server.mode</td></tr>
       <tr><th>Appy</th><td>:server.appyVersion</td></tr>
      </table>
      <x if="server.pool">
       <h2>Threads status (initial number of threads=<x>:cfg.threads</x>).</h2>
       <x>::server.pool.getTracked()</x>
      </x></x>''')
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
