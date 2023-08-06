'''Module managing translations (i18n)'''

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
class FieldTranslations:
    '''Translations, in all supported languages, for a given field.

       Place an instance if this class in attribute "translations" of some field
       if you do not want Appy to generate, for this field, i18n labels in PO
       files. With class FieldTranslations, you manage translations "by hand",
       coding them directly in Python or importing them via a custom tool.
    '''
    # Map label types to label attributes
    labelAttrs = {'label': 'labels', 'descr': 'descriptions', 'help': 'helps'}

    def __init__(self, labels=None, descriptions=None, helps=None,
                 fallback='en'):
        # Every attribute has the form
        #             ~O(en=s_translation, fr=s_translation,...)~
        # Translations for the field label
        self.labels = labels
        # Translations for the field description
        self.descriptions = descriptions
        # Translation for field helps
        self.helps = helps
        # Language to use if the required language is not found
        self.fallback = fallback

    def get(self, label, language, mapping=None):
        '''Returns the translation, in p_language, of the given p_label type.
           A p_mapping may be given.'''
        # Get the set of translations corresponding to the given p_label type
        translations = getattr(self, FieldTranslations.labelAttrs[label])
        # Get, within it, the translation corresponding to p_language, or
        # English if p_language is not found.
        r = getattr(translations, language, None) or \
            getattr(translations, self.fallback, '')
        # Todo: apply p_mapping when given
        return r
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
