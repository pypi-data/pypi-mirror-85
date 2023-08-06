'''Execute commands to a Subversion repository'''

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
import os
from pathlib import Path

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Subversion:
    '''Represents a distant Subversion server'''

    # svn options for non interactive mode
    nonInteractive = '--non-interactive --no-auth-cache'

    def __init__(self, specifier):
        # A p_specifier is an object with attributes such as "url", "name",
        # "login", "password"...
        self.specifier = specifier

    def build(self, command, path):
        '''Builds the Subversion p_command based on info from p_self.specifier
           and the concerned local p_path.'''
        # Returns a tuple (v_command, v_path), v_command being the complete
        # Subversion command (p_command and added args), and v_path being the
        # p_path completed with the local folder name in <site>/lib.
        r = ['svn', command]
        spec = self.specifier
        # Compute the local folder name in <site>/lib
        if spec.name:
            local = spec.name
        else:
            # The name of the app to checkout is the last part of spec.url
            local = Path(spec.url).name
        local = path / local        
        if command == 'checkout':
            # Add the checkout URL and local
            r.append(spec.url)
            # Add the name of the local folder to checkout to, if it is
            # different from the last part of the URL.
            if spec.name: r.append(spec.name)
        elif command == 'update':
            # Add the local folder that must be updated
            r.append(str(local))
        # Add parameters for running commands in a non interactive mode
        r.append(Subversion.nonInteractive)
        # Add authentication-related parameters if found
        if spec.login:
            r.append('--username %s --password %s' % (spec.login,spec.password))
        return ' '.join(r), local

    def checkout(self, path):
        '''Checkout a copy of code retrieved via p_self.specifier, in some local
           p_path.'''
        # Remember the current working directory: we will chdir into p_path
        curdir = os.getcwd()
        os.chdir(path)
        # Build the svn command
        command, local = self.build('checkout', path)
        # Execute the command
        print('Executing %s...' % command)
        os.system(command)
        # chdir to the initial working directory
        os.chdir(curdir)
        # Return the path to the checkouted local copy
        return local
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
