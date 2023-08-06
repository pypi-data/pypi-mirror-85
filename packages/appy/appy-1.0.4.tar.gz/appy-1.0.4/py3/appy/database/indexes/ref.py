'''An index for Ref fields'''

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
from appy.database.indexes import Index

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class RefIndex(Index):
    '''Index for a Ref field'''

    @classmethod
    def toIndexed(class_, value, field):
        '''Converts p_value, a list of tied objects, into their internal index
           representation = a list of their IIDs.'''
        # If there is no value at all, nothing must be indexed
        if value is None:
            return
        elif isinstance(value, int):
            # Already an object IID ready to be indexed (probably a default
            # value to index from field.emptyIndexValue).
            return value
        elif not hasattr(value, '__iter__'):
            # An object. Get its IID.
            return value.iid
        else:
            # Convert a list of objects into a list of their IIDs
            return [o.iid for o in value]

    @classmethod
    def toTerm(class_, value, field):
        '''Ensure p_value is an object's IID'''
        return value if isinstance(value, int) else value.iid

    @classmethod
    def toString(class_, o, value):
        '''The string representation for tied objects stored in p_value is the
           concatenation of their titles.'''
        return ' '.join([tied.getShownValue() for tied in value]) if value \
                                                                  else None
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
