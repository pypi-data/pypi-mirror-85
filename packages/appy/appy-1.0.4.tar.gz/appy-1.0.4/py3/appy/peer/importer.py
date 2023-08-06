'''Takes care of importing one object from one Appy site to another'''

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
from appy.model.utils import Object as O

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
IMPORT_START  = '%s %d %s instances(s) in %s:%s...'
REF_OBJS      = '%s:%s > %s objects'
ADD_DONE      = '%d created ¤ %d ignored ¤ %d linked.'
LINK_DONE     = '%d linked ¤ %d unresolved (yet).'

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Importer:
    '''Imports a single object from one Appy site to another'''

    # Depending on importing needs, sub-classes of this class may be defined and
    # used by sub-classes of class appy.peer.Peer.

    def __init__(self, peer, local=None, distant=None,
                 importHistory=True, importLocalRoles=True):
        # A link to the Peer instance driving the import process
        self.peer = peer
        # The local object. It may already exist prior to the import process
        # (ie, it is a default object like the tool).
        self.local = local
        # The p_distant object, in the form of an instance of
        # appy.model.utils.Object, unmarshalled from the distant site by the
        # appy.xml.unmarshaller.
        self.distant = distant
        # Must object history be imported ?
        self.importHistory = importHistory
        # Must object's local roles be imported ?
        self.importLocalRoles = importLocalRoles

    # During the import process, everytime an object is about to be imported
    # because mentioned in a Ref:add=True, one of the following actions can be
    # performed.
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    CREATE = 0 # Create a local object corresponding to the distant one
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    IGNORE = 1 # Do not do anything, simply ignore the distant object
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    FIND   = 2 # Find a local object corresponding to the distant one, but
    #            ignore distant data.
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    SYNC   = 3 # Find a local object corresponding to the distant one and update
    #            the local object with distant data.
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    @classmethod
    def getAction(class_, distant):
        '''What action must be performed with this p_distant object ?'''

        # The method returns a tuple (action, detail):
        #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # action | must be one of the hereabove constants ;
        #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # detail | if action is CREATE or IGNORE, action is ignored;
        #        |
        #        | if action is FIND or SYNC:
        #        |   * if "detail" is None, the local object will be found based
        #        |     on the distant object's ID ;
        #        |   * if "detail" is a dict, it will be considered as a unique
        #        |     combination of attributes allowing to perform a search
        #        |     and find a unique local object corresponding to the
        #        |     distant one. For example, for a user it could be
        #        |
        #        |                     {'login': 'admin'}
        #        |
        #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # By default, any distant object found via a Ref:add=True must be
        # locally created.
        return class_.CREATE, None

    def addableRef(self, field):
        '''Is this Ref p_field addable ?'''
        if field.add:
            r = True
        elif field.link:
            r = False
        elif field.composite:
            r = True
        else:
            # Check in the peer config
            addable = self.peer.addable.get(self.local.class_.name)
            r = addable and (field.name in addable)
        return r

    def setRef(self, field):
        '''Links distant objects defined @p_self.distant.<p_field.name> to
           p_self.local via this Ref p_field.'''
        # Get the list of distant object URL on p_self.distant
        urls = getattr(self.distant, field.name, None)
        if not urls: return
        # Unwrap some variables
        o = self.local
        imported = self.peer.localObjects
        add = self.addableRef(field)
        name = field.name
        peer = self.peer
        # Browse URLs of distant objects
        verb = 'Creating' if add else 'Linking'
        tiedClass = field.class_.meta
        print()
        o.log(IMPORT_START % (verb, len(urls), tiedClass.name, o.class_.name,
                              field.name))
        # Count the number of objects that will be created, linked, ignored, and
        # those being unresolved at this step.
        counts = O(created=0, linked=0, ignored=0, unresolved=0, current=0)
        for url in urls:
            counts.current += 1
            # Get the distant ID from the URL
            distantId = peer.getIdFromUrl(url)
            if add:
                peer.printSymbol(counts.current)
                # Get the distant object
                distant = peer.get(url)
                # Get an importer class for this type of objects
                importer = peer.getImporter(tiedClass)
                # What to do with this distant object ?
                action, detail = importer.getAction(distant)
                if action == importer.IGNORE:
                    # Ignore it
                    counts.ignored += 1
                    continue
                elif action == importer.CREATE:
                    # Create a local object corresponding to the distant one
                    tied = o.create(name, executeMethods=False)
                    # Add it to the dict of already imported objects
                    imported[distantId] = tied
                    # Fill local object's attributes from distant ones
                    importer(peer, tied, distant).run()
                    counts.created += 1
                elif action in (importer.FIND, importer.SYNC):
                    # Find the local objet corresponding to the distant one
                    tied = o.getObject(distant.id) if detail is None else \
                           o.search1(tiedClass.name, **detail)
                    # Add it to the dict of already imported objects
                    imported[distantId] = tied
                    # Fill, when appropriate, local object's attributes from
                    # distant ones.
                    if action == importer.SYNC:
                        importer(peer, tied, distant).run()
                    counts.linked += 1
            else:
                # Find the object among the already imported objects
                if distantId not in imported:
                    # The object has not been imported yet
                    peer.unresolved.add(o, field, distantId)
                    counts.unresolved += 1
                else:
                    tied = imported[distantId]
                    o.link(name, tied, executeMethods=False)
                    counts.linked += 1
        # Log the end of this operation
        prefix = REF_OBJS % (o.class_.name, field.name, tiedClass.name)
        if add:
            suffix = ADD_DONE % (counts.created, counts.ignored, counts.linked)
        else:
            suffix = LINK_DONE % (counts.linked, counts.unresolved)
        print()
        o.log('%s: %s' % (prefix, suffix))

    def setFields(self):
        '''Copy values from p_self.distant fields'''
        o = self.local
        d = self.distant
        for name, field in self.local.class_.fields.items():
            # Ignore computed fields
            if not field.persist: continue
            if field.type == 'Ref':
                # Ignore back Refs: they will be automatically reconstituted by
                # linking object via forward Refs.
                if field.isBack: continue
                self.setRef(field)
            else:
                # Simply copy the field value
                setattr(o, name, getattr(d, name))

    def setHistory(self):
        '''To implement'''

    def setLocalRoles(self):
        '''To implement'''

    def customize(self):
        '''To be overridden by sub-class to tailor the import of self.p_local'''

    def run(self):
        '''Performs the import from p_self.distant to p_self.local'''
        # Set history and local roles when required
        if self.importHistory: self.setHistory()
        if self.importLocalRoles: self.setLocalRoles()
        # Import values from simple fields
        self.setFields()
        # Perfom custom processing, if any
        self.customize()
        # Reindex the object
        if self.local.class_.isIndexable():
            self.local.reindex()

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class UserImporter(Importer):
    '''Specific importer for importing users'''

    # Logins of users that must not be imported
    unimportable = ('anon', 'system')

    def customize(self):
        '''Manage special field "encrypted" storing the encrypted password'''
        self.local.values['password'] = self.distant.encrypted.encode()

    @classmethod
    def getAction(class_, distant):
        '''Special users "system" and "anon" must not be imported; user "admin"
           must be found locally but not synced.'''
        login = distant.login
        if login in class_.unimportable:
            r = class_.IGNORE, None
        elif login == 'admin':
            r = class_.FIND, {'login': 'admin'}
        else:
            r = class_.CREATE, None
        return r
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
