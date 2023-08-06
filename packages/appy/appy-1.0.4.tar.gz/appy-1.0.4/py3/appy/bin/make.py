#!/usr/bin/python3

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
import os, shutil
from pathlib import Path

import appy
from appy.tr.po import File
from appy.bin import Program
from appy.utils.path import chown
from appy.utils.loc import Counter
from appy.tr.updater import Updater
from appy.deploy import parseSpecifier
from appy.deploy.subversion import Subversion

# File templates - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# <site>/bin/site
site = """
#!/usr/bin/python3

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
import sys
from pathlib import Path

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
site = Path('{self.folder}')
app  = Path('{self.app}')
ext  = '{self.ext}'
ext  = Path(ext) if ext else None

paths = [site, site/'lib', app.parent]
if ext: paths.append(ext.parent)

for path in paths:
    path = str(path)
    if path not in sys.path:
        sys.path.insert(0, path)

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Import Appy after sys.path has been updated
from appy.bin.run import Run

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
if __name__ == '__main__':
    Run().run(site, app, ext)
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
"""

# <site>/bin/deploy
deploy = """
#!/usr/bin/python3
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
import sys
from appy.bin.deploy import Deploy

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
if __name__ == '__main__':
    sys.argv.insert(1, '{self.folder}')
    sys.argv.insert(1, '{self.app}')
    Deploy().run()
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
"""

# <site>/config.py
config = """
# -*- coding: utf-8 -*-

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
app = '{self.app}'
site = '{self.folder}'

# Complete the config  - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def complete(c):
    c.model.set(app)
    c.server.set(app)
    c.server.port = {self.port}
    c.database.set(site + '/var')
    c.log.set(site + '/var/site.log', site + '/var/app.log')
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
"""

# <app>/__init__.py
appInit = '''
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
from appy.database import log
from appy.server import guard
from appy import database, model, ui, server, deploy, peer

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
import appy
class Config(appy.Config):
    server = server.Config()
    security = guard.Config()
    database = database.Config()
    log = log.Config()
    model = model.Config()
    ui = ui.Config()
    deploy = deploy.Config()
    peers = peer.Config()

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
try: # to import the site-specific configuration file
    import config
    config.complete(Config)
except ImportError:
    # The "config" module may not be present at maketime
    pass
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
'''

# <app>/make
appMake = '''
#!/usr/bin/python3
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
from pathlib import Path
from appy.bin.make import App

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
App(Path('.')).update()
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
'''

# <app>/static/robots.txt
appRobots = '''
# More information about this file on http://robots-txt.com
User-agent: *
Disallow: /
'''

# <ext>/__init__.py
extInit = '''
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Import the app's main Config instance
from %s import Config as c

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Declare this extension
from pathlib import Path
c.declareExt(Path('%s'))

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Apply ext's changes to this instance
# c.<attribute> = ...

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
'''

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Target:
    '''Abstract class representing the artefact to create or update'''

    def createFile(self, path, content, permissions=None):
        '''Create a file on disk @ p_path, with some p_content and
           p_permissions.'''
        folder = path.parent
        # Create the parent folder if it does not exist
        if not folder.exists(): folder.mkdir(parents=True)
        # Patch content with variables
        content = content.format(self=self)[1:]
        # Create the file
        path = str(path)
        f = open(path, 'w')
        f.write(content)
        f.close()
        # Set specific permissions on the created file when required
        if permissions: os.chmod(path, permissions)

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Site(Target):
    '''A site listens to some port and runs an app'''

    # A site is made of 3 sub-folders:
    folders = ('bin', 'lib', 'var')
    # "bin" stores the scripts for controlling the app (start/stop), backuping
    #       or restoring its data, etc;
    # "lib" stores or links the Python modules available to the site. It
    #       contains at least the app;
    # "var" stores the data produced or managed by the site: database files and
    #       folders and log files.

    def __init__(self, folder, app, port, owner, dependencies, ext):
        # The base folder for the site
        self.folder = folder
        # The folder or distant specifier for the app and its ext
        self.app = app
        self.ext = ext
        # The port on which the site will listen
        self.port = port
        # The owner of the site tree (if None, the user executing the script
        # will become owner of the tree).
        if owner:
            if ':' in owner:
                self.owner, self.ownerGroup = owner.split(':')
            else:
                self.owner = owner
                self.ownerGroup = None
        else:
            self.owner = self.ownerGroup = None
        # Site dependencies
        self.dependencies = dependencies

    def create(self):
        '''Creates a fresh site'''
        # Create the root folder (and parents if they do not exist)
        self.folder.mkdir(parents=True)
        # Create the sub-folders
        for name in Site.folders: (self.folder/name).mkdir()
        # If the app or ext are distant, get, in lib/<appOrExtName>, a copy from
        # the server.
        lib = self.folder / 'lib'
        if not isinstance(self.app, Path):
            self.app = Subversion(self.app).checkout(lib)
        ext = self.ext
        if ext:
            self.ext = ext if isinstance(ext, Path) \
                           else Subversion(ext).checkout(lib)
        else:
            self.ext = ''
        # Integrate dependencies into the site
        dependencies = self.dependencies
        if dependencies:
            for dep in dependencies:
                if isinstance(dep, Path):
                    # A dependency to a local package. Symlink it in <site>/lib.
                    os.symlink(dep, lib / dep.name)
                else:
                    # A specifier. Checkout a copy in <site>/lib.
                    Subversion(dep).checkout(lib)
        # Create <site>/bin/site and <site>/bin/deploy
        self.createFile(self.folder/'bin'/'site', site, 0o770)
        self.createFile(self.folder/'bin'/'deploy', deploy, 0o770)
        # Create <site>/config.py
        self.createFile(self.folder/'config.py', config)
        # Chown the tree to p_self.owner if it has been specified
        owner = self.owner
        if owner:
            chown(self.folder, owner, group=self.ownerGroup, recursive=True)

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class App(Target):
    '''An app is a piece of software being Appy-compliant'''

    # Mandatory app sub-folders
    subFolders = (
      'tr',    # Stores "po" and "pot" files (for translations)
      'static' # Stores any static content (images, CSS or Javascript files...)
    )

    # Mandatory files to have in <appFolder>/static
    files = (
      # The icon retrieved by Safari
      'appleicon.png',
      # he icon retrieved by other browsers
      'favicon.ico',
      # The file read by robots
      'robots.txt'
    )

    def __init__(self, folder):
        # The base folder for the app. Ensure it is absolute.
        if not folder.is_absolute():
            folder = folder.resolve()
        self.folder = folder

    def create(self):
        '''Creates a new app'''
        # Create <app>/__init__.py
        path = self.folder / '__init__.py'
        if not path.exists():
            self.createFile(path, appInit)
        # Create <app>/make
        path = self.folder / 'make'
        if not path.exists():
            self.createFile(path, appMake, 0o770)
        # Create base folders
        for name in App.subFolders:
            folder = self.folder / name
            if not folder.exists(): folder.mkdir()
            if name == 'static':
                # Ensure mandatory files are present and create them if not
                robots = folder / 'robots.txt' # The file read by robots
                if not robots.exists():
                    self.createFile(robots, appRobots)
                # The icon retrieved by browsers, shown besides the address bar
                for name in ('favicon.ico', 'appleicon.png'):
                    icon = folder / name
                    if not icon.exists():
                        # Copy the default one in Appy
                        ico = '%s/ui/static/%s' % (str(appy.path), name)
                        shutil.copy(ico, str(icon))

    def update(self):
        '''Updates an existing app'''
        print('Updating %s...' % self.folder)
        # Ensure the base files and folders are created
        self.create()
        # Call the translations updater that will create or update translation
        # files for this app.
        Updater(self.folder / 'tr').run()
        # Count the lines of code in the app
        Counter(self.folder).run()
        print('Done.')

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Ext(App):
    '''An ext is an extension to a given app'''

    def __init__(self, folder, app):
        # Call the base constructor
        App.__init__(self, folder)
        # The app's Path
        self.app = app

    def getAppLanguages(self):
        '''Retrieve the languages supported by the app'''
        # It is done by searching the app's .po files. Doing it by importing the
        # app and reading its Config instance, in order to access attribute
        # Config.languages, has been felt more risky, because importing the app
        # could lead to import errors.
        r = []
        name = self.app.name
        for po in (self.app / 'tr').glob('%s-*.po' % self.app.name):
            r.append(po.stem.rsplit('-')[1])
        return r

    def create(self):
        '''Creates a new ext'''
        # Create <ext>/__init__.py
        path = self.folder / '__init__.py'
        if not path.exists():
            self.createFile(path, extInit % (self.app.name, str(self.folder)))
        # Create base folders
        for name in App.subFolders:
            folder = self.folder / name
            if not folder.exists(): folder.mkdir()
        # Create a "po" file for every app language, in case the ext needs to
        # override some i18n labels.
        for lang in self.getAppLanguages():
            # Create an empty file named <ext>/tr/Custom-<lang>.po
            name = 'Custom-%s.po' % lang
            File(self.folder / 'tr' / name).generate()

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Make(Program):
    '''This program allows to create or update an app or a site'''
    # We can create/update the following artefacts
    allowedTargets = ('app', 'site', 'ext')

    # Help messages
    APP_S        = 'url=<url>, [name=<name>,login=<login>, password=<password>]'
    HELP_TARGET  = 'can be "app" for creating/updating an app, "site" for ' \
                   'creating a site or "ext" for creating an extension to an ' \
                   'app.'
    HELP_FOLDER  = 'folder is the absolute path to the base folder for the ' \
                   'app, site or ext.'
    HELP_A       = 'Mandatory when target is [site] or [ext], specify here ' \
                   'the absolute path to the related app (if the app is to ' \
                   'be found locally), or a distant app specifier of the ' \
                   'form %s. Currently, a distant specifier must point to a ' \
                   'Subversion repository.' % APP_S
    HELP_P       = '[site] the port on which the site will listen. Defaults ' \
                   'to 8000.'
    HELP_O       = "[site, unix/linux only] the owner of the site. If " \
                   "specified, the whole site tree will be chown'ed to this " \
                   "owner. Optionally, you may specify the group by " \
                   "suffixing the owner by a colon and the group name, ie: " \
                   "appy:appy."
    HELP_D       = '[site] dependencies, as a series of local paths or ' \
                   'specifiers. For every local path, a symlink will be ' \
                   'created in <site>/lib. For every specifier, a local copy ' \
                   'will created in <site>/lib.'
    HELP_E       = '[site] The absolute path to the optional extension to ' \
                   'the app specified via option "-a" (if the ext is to be ' \
                   'found locally) or a distant ext specifier of the form ' \
                   '"%s".' % APP_S

    # Error messages
    WRONG_TARGET = 'Wrong target "%s".'
    F_EXISTS     = '%s already exists. You must specify an inexistent path ' \
                   'that this script will create and populate with a fresh %s.'
    NO_APP       = 'No app was specified.'
    WRONG_APP    = '%s does not exist or is not a folder.'
    WRONG_APP_S  = 'Wrong app specifier: %s'
    APP_S_KO     = 'An app specifier must be of the form "%s".' % APP_S
    SPEC_APP_KO  = "In that context, the app's local path must be given."

    def defineArguments(self):
        '''Define the allowed arguments for this program'''
        add = self.parser.add_argument
        # Positional arguments, common to all targets (app and site)
        add('target', help=Make.HELP_TARGET)
        add('folder', help=Make.HELP_FOLDER)
        # Optional arguments specific to "site"
        add('-a', '--app',  dest='app',  help=Make.HELP_A)
        add('-p', '--port', dest='port', help=Make.HELP_P)
        add('-o', '--owner', dest='owner', help=Make.HELP_O)
        add('-d', '--dependencies', dest='dependencies', nargs='+',
            help=Make.HELP_D)
        add('-e', '--ext',  dest='ext',  help=Make.HELP_E)

    def analyseApp(self, app, isExt=False, specifierDisallowed=False):
        '''Get the path to a local app (or ext if p_isExt is True) or the
           distant specifier else.'''
        if not app and not isExt: self.exit(self.NO_APP)
        if ',' in app:
            # A specifier
            if specifierDisallowed: self.exit(self.SPEC_APP_KO)
            r = parseSpecifier(app)
            if not r.url:
                print(self.WRONG_APP_S % app)
                self.exit(self.APP_S_KO % app)
        else:
            # It must be the path to a local folder
            r = Path(app).resolve()
            # This path must exist
            if not r.is_dir():
                self.exit(self.WRONG_APP % r)
        return r

    def analyseDependencies(self, dependencies):
        '''Analyses the specified p_dependencies and converts, in it, paths to
           Path instances and specifiers to Object instances.'''
        if not dependencies: return []
        i = 0
        length = len(dependencies)
        while i < length:
            dep = dependencies[i]
            if ',' in dep:
                # A specifier
                dep = parseSpecifier(dep)
                if not dep.url:
                    print(self.WRONG_APP_S % dep)
                    self.exit(self.APP_S_KO % dep)
            else:
                dep = Path(dep).resolve()
            dependencies[i] = dep
            i += 1
        return dependencies

    def analyseArguments(self):
        '''Check and store arguments'''
        # "folder" will be a Path created from the "folder" argument
        self.folder = None
        # Site/ext-specific attributes
        self.app = None # The result of parsing the '-a' option
        # Check arguments
        args = self.args
        # Check target
        target = args.target
        if target not in self.allowedTargets:
            self.exit(self.WRONG_TARGET % target)
        # Get a Path for the "folder" argument
        self.folder = Path(self.args.folder).resolve()
        # Check site-specific arguments and values
        if target == 'site':
            # The path to the site must not exist
            if self.folder.exists():
                self.exit(self.F_EXISTS % (self.folder, 'site'))
            # Manage the app and its ext
            self.app = self.analyseApp(self.args.app)
            ext = self.args.ext
            self.ext = None if not ext else self.analyseApp(ext, isExt=True)
            # The port must be an integer value
            port = self.args.port
            if port and not port.isdigit():
                self.exit(self.PORT_KO % port)
            self.port = int(port) if port else 8000
            # An owner may be specified
            self.owner = self.args.owner
            # Manage dependencies
            self.dependencies = self.analyseDependencies(self.args.dependencies)
        elif target == 'app':
            # No more check for the moment. The folder can exist or not.
            pass
        elif target == 'ext':
            # The path to the ext must not exist (it is not possible to update
            # an ext, only create it).
            if self.folder.exists():
                self.exit(self.F_EXISTS % (self.folder, 'ext'))
            # The path to the related app must be given
            self.app = self.analyseApp(self.args.app, specifierDisallowed=True)

    def run(self):
        target = self.args.target
        if target == 'site':
            Site(self.folder, self.app, self.port, self.owner,
                 self.dependencies, self.ext).create()
        elif target == 'app':
            action = 'update' if self.folder.exists() else 'create'
            eval('App(self.folder).%s()' % action)
        elif target == 'ext':
            Ext(self.folder, self.app).create()
        print('Done.')

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
if __name__ == '__main__': Make().run()
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
