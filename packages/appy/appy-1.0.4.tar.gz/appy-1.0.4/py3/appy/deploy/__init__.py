'''Deployment system for Appy sites and apps'''

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
import os, sys
from pathlib import Path
from appy.model.utils import Object as O
from appy.deploy.subversion import Subversion

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def parseSpecifier(specifier):
    '''Parses a string specifier of the form <attr>=<value>[,<attr>=<value>]'''
    r = O()
    for part in specifier.split(','):
        name, value = part.split('=', 1)
        r[name] = value
    return r

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Target:
    '''Represents a app deployed on a site on a distant machine'''

    def __init__(self, sshHost, sshPort=22, sshLogin='root', sshKey=None,
                 sitePath=None, sitePort=8000, siteApp=None,
                 siteOwner='appy:appy', siteDependencies=None):
        # The name of the distant host, for establishing a SSH connection
        self.sshHost = sshHost
        # The port for the SSH connection
        self.sshPort = sshPort
        # The login used to connect to the host in SSH
        self.sshLogin = sshLogin
        # The private key used to connect to the host in SSH
        self.sshKey = sshKey
        # Information about the Appy site on the target
        # ~~~
        # The path to the site. Typically: /home/appy/<siteName>
        self.sitePath = sitePath
        # The port on which this site will listen
        self.sitePort = sitePort
        # The specifier of the distant app. For example:
        #    url=https://svn.forge.pallavi.be/appy-python-3/trunk,name=appy
        self.siteApp = siteApp
        # The owner of the distant site. Typically: appy:appy.
        self.siteOwner = siteOwner
        # A list of Python dependencies to install on the distant app, in its
        # "lib" folder. For every dependency, a specifier must be used, with the
        # same syntax as attribute "siteApp" hereabove.
        self.siteDependencies = siteDependencies or []

    def __repr__(self):
        '''p_self's string representation'''
        return '<Target %s:%d>' % (self.sshHost, self.sshPort)

    def execute(self, command):
        '''Executes p_command on this target'''
        r = ['ssh', '%s@%s' % (self.sshLogin, self.sshHost), '"%s"' % command]
        # Determine port
        if self.sshPort != 22: r.insert(1, '-p%d' % self.sshPort)
        # Determine "-i" option (path to the private key)
        if self.sshKey: r.insert(1, '-i %s' % self.sshKey)
        # Build the complete command
        r = ' '.join(r)
        print('Executing: %s...' % r)
        os.system(r)

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Config:
    '''Deployment configuration'''

    def __init__(self):
        # This dict stores all the known targets for deploying this app. Keys
        # are target names, values are Target instances. The default target must
        # be defined at key "default".
        self.targets = {}

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
NO_CONFIG = 'The "deploy" config was not found in config.deploy.'
NO_TARGET = 'No target was found on config.deploy.targets.'
TARGET_KO = 'Target "%s" not found. Available target(s): %s.'

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Deployer:
    '''App deployer'''

    # apt command for installing packages non interactively
    apt = 'DEBIAN_FRONTEND=noninteractive apt-get -yq install'

    # OS packages being Appy dependencies
    osDependencies = 'libreoffice subversion python3-pip apache2 imagemagick'

    def __init__(self, appPath, sitePath, command, targetName='default'):
        # The path to the app
        self.appPath = appPath
        # The path to the reference, local site, containing targets definition
        self.sitePath = sitePath
        # The chosen target (name)
        self.targetName = targetName or 'default'
        self.target = None # Will hold a Target instance
        # The command to execute
        self.command = command
        # The app config
        self.config = None

    def quote(self, arg):
        '''Surround p_arg with quotes'''
        r = arg if isinstance(arg, str) else str(arg)
        return "'%s'" % r

    def buildPython(self, statements):
        '''Builds a p_command made of these Python p_statements'''
        return "python3 -c \\\"%s\\\"" % ';'.join(statements)

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    #                              Commands
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # Command for consulting the last lines in a target's app.log file
    tail = 'tail -f -n %d %s/var/app.log'

    def list(self):
        '''Lists the available targets on the config'''
        infos = []
        for name, target in self.config.deploy.targets.items():
            info = '*** Target: %s\n%s' % (name, target)
            infos.append(info)
        infos = '\n\n'.join(infos)
        print('Available target(s) for app "%s", from reference site "%s":\n' \
              '%s' % (self.appPath.name, self.sitePath.name, infos))

    def info(self):
        '''Retrieve info about the target OS'''
        self.target.execute('cat /etc/lsb-release')

    def install(self):
        '''Installs required dependencies on the target via "apt" and "pip3" and
           create special user "appy" on the server.'''
        target = self.target
        commands = [
          # Install required dependencies via Aptitude
          '%s %s' % (self.apt, self.osDependencies),
          # Install Appy and dependencies via pip
          'pip3 install appy',
          # Create special user "appy"
          'adduser --disabled-password --gecos \'\' appy'
        ]
        target.execute(';'.join(commands))

    def site(self):
        '''Creates an Appy site on the distant server'''
        t = self.target
        # Build args to appy/bin/make
        q = self.quote
        args = [q(t.sitePath), q('-a'), q(t.siteApp), q('-p'), q(t.sitePort),
                q('-o'), q(t.siteOwner)]
        if t.siteDependencies:
            args += [q('-d'), q(' '.join(t.siteDependencies))]
        # Build the statements to pass to the distant Python interpreter
        statements = [
          'import sys', 'from appy.bin.make import Make',
          "sys.argv=['make.py','site',%s]" % ','.join(args),
          'Make().run()'
        ]
        command = self.buildPython(statements)
        # Execute it
        t.execute(command)

    def update(self):
        '''Performs an update of all software known to the site and coming from
           external sources (app and dependencies) and (re)starts the site.'''
        target = self.target
        # Build the commands to update the app and dependencies
        commands = []
        svn = Subversion(parseSpecifier(target.siteApp))
        lib = Path(target.sitePath) / 'lib'
        svnUp, local = svn.build('update', lib)
        commands.append(svnUp)
        for dep in target.siteDependencies:
            svn = Subversion(parseSpecifier(dep))
            svnUp, local = svn.build('update', lib)
            commands.append(svnUp)
        # Build the command to restart the distant site
        restart = '%s/bin/site restart' % target.sitePath
        commands.append(restart)
        commands.append(self.tail % (100, target.sitePath))
        # The commands will be ran with target.siteOwner
        owner = target.siteOwner.split(':')[0]
        command = "su %s -c '%s'" % (owner, ';'.join(commands))
        target.execute(command)

    def view(self):
        '''Launch a command "tail -f" on the target's app.log file'''
        target = self.target
        target.execute(self.tail % (200, target.sitePath))

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    #                             Main method
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    def run(self):
        '''Performs p_self.command on the specified p_self.targetName'''
        # Add the relevant paths to sys.path
        for path in (self.sitePath, self.sitePath / 'lib', self.appPath.parent):
            sys.path.insert(0, str(path))
        # Get the config and ensure it is complete
        self.config = __import__(self.appPath.name).Config
        cfg = self.config.deploy
        if not cfg:
            print(NO_CONFIG)
            sys.exit(1)
        targets = cfg.targets
        if not targets:
            print(NO_TARGET)
            sys.exit(1)
        # Get the target
        name = self.targetName
        target = self.target = targets.get(name)
        if not target:
            print(TARGET_KO % (name, ', '.join(targets)))
            sys.exit(1)
        getattr(self, self.command)()
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
