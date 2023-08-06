'''Runs a site'''

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
import os, sys, subprocess, signal, time

from appy.bin import Program
from appy.server import Server

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def start(config, action):
    '''Function that starts a HTTP server'''
    server = Server(config, action)
    
class Run(Program):

    # Run-specific exception class
    class Error(Exception): pass

    # Help messages
    HELP_ACTION = 'Action can be "start" (start the site), "stop" (stop it), ' \
                  '"restart" (stop it and directly restart it), "fg" (start ' \
                  'it in the foreground), "clean" (clean temporary objects ' \
                  'and pack the database) or "run" (execute a specific method).'
    HELP_METHOD = 'When action in "run", specify the name of the method to ' \
                  'execute on your app\'s tool.'

    # Error messages
    WRONG_ACTION = 'Unknown action "%s".'
    MISSING_METHOD = 'Please specify a method name via option "-m".'
    NOT_IMPLEMENTED = 'Action "%s" is not implemented yet.'
    PORT_USED = 'Port %d is already in use.'
    PID_EXISTS = 'Existing pid file removed (server not properly shut down).'
    PID_NOT_FOUND = "The server can't be stopped."

    # Other constants
    allowedActions = ('start', 'stop', 'restart', 'fg', 'bg', 'clean', 'run')

    def defineArguments(self):
        '''Define the allowed arguments for this program'''
        parser = self.parser
        parser.add_argument('action', help=Run.HELP_ACTION)
        parser.add_argument('-m', '--method', type=str, help=Run.HELP_METHOD)

    def analyseArguments(self):
        '''Check arguments'''
        # Check that the specified action is valid
        action = self.args.action
        if action not in Run.allowedActions:
            self.exit(self.WRONG_ACTION % action)
        # Check that a method name is given when action is "run"
        method = None
        if action == 'run':
            method = self.args.method
            if method is None:
                self.exit(self.MISSING_METHOD)
        self.action = action
        self.method = method

    def getPid(self, config):
        '''Return a pathlib.Path instance to the "pid" file, which, when the
           server is started in "start" mode, stores its process ID, in order
           to be able to stop him afterwards.'''
        # We have chosen to create the "pid" besides the DB file
        return config.database.filePath.parent / 'pid'

    def checkStart(self, config, exitIfInUse=False):
        '''Checks that the server can be started in "start" mode'''
        # Check if the port is already in use or not
        if config.server.inUse():
            message = self.PORT_USED % config.server.port
            if exitIfInUse:
                print(message)
                sys.exit(1)
            else:
                raise self.Error(message)
        # If a "pid" file is found, it means that the server was not properly
        # stopped. Remove the file and issue a warning.
        pid = self.getPid(config)
        if pid.exists():
            print(self.PID_EXISTS)
            pid.unlink()

    def checkStop(self, pidFile, restart=False):
        '''Checks that the server can be stopped and returns the process ID
           (pid) of the running server.'''
        # Check that the pid file exists
        if not pidFile.exists():
            print(self.PID_NOT_FOUND)
            if not restart:
                sys.exit(1)
            else:
                return
        with pidFile.open() as f: r = f.read().strip()
        return int(r)

    def start(self, config, exitIfInUse=True):
        '''Starts the server'''
        self.checkStart(config, exitIfInUse=exitIfInUse)
        # Spawn a child process and run the server in it, in "bg" mode 
        args = list(sys.argv)
        args[-1] = 'bg'
        # Start the server in the background, in another process
        pid = subprocess.Popen(args).pid
        # Create a file storing the process ID, besides the DB file
        path = self.getPid(config)
        with path.open('w') as f: f.write(str(pid))
        print('Started as process %s.' % pid)
        sys.exit(0)

    def stop(self, config, restart=False):
        '''Stops the server. If p_restart is True, the server will be
           immediately restarted afterwards.'''
        pidFile = self.getPid(config)
        pid = self.checkStop(pidFile, restart=restart)
        wasRunning = True
        if pid is not None:
            try:
                os.kill(pid, signal.SIGINT)
            except ProcessLookupError:
                print('Server was not running (probably abnormally stopped).')
                wasRunning = False
            finally:
                pidFile.unlink()
        if not restart and wasRunning:
            print('Server stopped.')

    def run(self, site, app, ext=None):
        '''Runs the web server'''
        # Get the configuration
        exec('from %s import Config' % app.name)
        config = eval('Config')
        action = self.action

        # Execute the appropriate action
        if action in ('fg', 'bg', 'clean', 'run'):
            # ------------------------------------------------------------------
            #  "fg"     | The user executed command "./site fg" : we continue
            #           | and run the server in this (parent, unique) process.
            # ------------------------------------------------------------------
            #  "bg"     | The user executed command "./site start", the runner
            #           | in the parent process spawned a child process with
            #           | command "./site bg". We continue and run the server in
            #           | this (child) process.
            # ------------------------------------------------------------------
            #  "clean", | Theses cases are similar to the "fg" mode hereabove;
            #  "run"    | they misuse the server to execute a single command and
            #           | return, without actually running the server.
            # ------------------------------------------------------------------
            classic = action in ('fg', 'bg')
            if action == 'fg':
                # For "bg", the check has already been performed
                self.checkStart(config)
            # Create a Server instance
            server = Server(config, action, self.method, ext=ext)
            # In classic modes "fg" or "bg", run the server
            if action in ('fg', 'bg'):
                try:
                    server.serve_forever()
                except KeyboardInterrupt:
                    server.shutdown()
                    server.server_close()
                    sys.exit(0)
            else:
                # Everything has been done during server initialisation
                server.shutdown()
                sys.exit(0)

        elif action == 'start':
            self.start(config)

        elif action == 'stop':
            self.stop(config)

        elif action == 'restart':
            self.stop(config, restart=True)
            time.sleep(0.5)
            try:
                self.start(config, exitIfInUse=False)
            except self.Error as e:
                # The server is probably not stopped yet
                time.sleep(1.0)
                self.start(config)
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
