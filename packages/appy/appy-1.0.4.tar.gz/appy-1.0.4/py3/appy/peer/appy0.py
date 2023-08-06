'''Import data from a Appy 0.x site to an Appy 1.x site'''

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
from appy.peer import Peer
from appy.peer.importer import Importer, UserImporter

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
NOT_IMPL_YET = 'Not implemented yet.'

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Importer0(Importer):
    '''Base object importer for Appy 0'''

    def setHistory(self):
        '''Imports Appy 0's history from p_self.distant and populate the
           corresponding Appy 1 data structure on p_self.local.'''
        history = self.local.history
        # History events in Appy 0 are chronologically sorted
        i = -1
        for event in self.distant.history:
            i += 1
            # Creator, created & modified will be set by m_setFields
            if i == 0: continue
            # Get parameters being common to all history events
            params = {'state': event.review_state, 'date': event.time,
                      'login': event.actor, 'comment': event.comments}
            action = event.action
            if action == '_datachange_':
                eventType = 'Change'
                # Convert the "changes" dict to Appy 1
                changes = {}
                for name, vals in event.changes.items():
                    changes[name] = vals[0]
                params['changes'] = changes
            elif action == '_datadelete_':
                print('Data-delete event', event)
                raise Exception(NOT_IMPL_YET)
            elif action == '_dataadd_':
                print('Data-add event', event)
                raise Exception(NOT_IMPL_YET)
            else:
                # A workflow transition
                params['transition'] = action
                eventType = 'Trigger'
            history.add(eventType, **params)

    def setLocalRoles(self):
        '''Sets local roles on p_self.local as defined on p_self.distant'''
        # Delete local role granted to technical user "system" when the local
        # object has been created.
        localRoles = self.local.localRoles
        localRoles.delete('system')
        for login, roles in self.distant.localRoles.items():
            localRoles.add(login, roles)

    def customize(self):
        '''Manage "creator", "created" and "modified" fields, being stored
           differently in Appy 0 and Appy 1.'''
        o = self.local
        d = self.distant
        o.setCreator(d.creator)
        o.history[-1].date = d.created
        o.history.modified = d.modified

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class UserImporter0(Importer0, UserImporter):
    '''Appy 0 User-specific importer'''

    def customize(self):
        '''Perform Appy 0 AND User-specific customization'''
        Importer0.customize(self)
        UserImporter.customize(self)

    @classmethod
    def getAction(class_, distant):
        '''Bypass Python's standard depth-first search inheritance and call
           UserImporter.getAction.'''
        return UserImporter.getAction(distant)

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Appy0(Peer):
    '''Represents a peer Appy 0.x site'''

    # Declare the base object importer for Appy 0
    baseImporter = Importer0

    # In Appy 0, the ID of the tool is 'config' and not 'tool'
    distantToolName = 'config'

    def __init__(self, *args, **kwargs):
        # Call the base constructor
        super().__init__(*args, **kwargs)
        # Update importers
        self.importers['User'] = UserImporter0

    def getSearchUrl(self, tool, className):
        '''Return the URL allowing to retrieve URLs of all instances from a
           given p_className on a distant site.'''
        # Get the name of the distant class corresponding to this local
        # p_className.
        distantName = self.classNames.get(className) or className
        return '%s/config?do=searchAll&className=%s' % (self.url, distantName)
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
