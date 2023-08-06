# -*- coding: utf-8 -*-

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
from DateTime import DateTime

from appy.px import Px
from appy.model.fields import Field

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
INVALID_MULTILINGUAL_VALUE = 'Multilingual field "%s" accepts a dict whose ' \
  'keys are in field.languages and whose values are strings.'

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Multilingual:
    '''Mixin class injected into any Field whose content can be multilingual'''

    # Default values to render when field values are empty
    emptyDefault = {'view': '-', 'edit': ''}
    # Default top space (in pixels) to apply in pxLanguage
    lgTop = {'view': 1, 'edit': 3}

    # Note that multilinguality is a dynamic feature: field values can be
    # unilingual or multilingual, depending on some condition on the container
    # object itself, or on some site-specific configuration.

    # PX displaying the language code and name besides the part of the
    # multilingual field storing content in this language.
    pxLanguage = Px('''
     <td style=":'padding-top:%dpx' % field.lgTop[layout]" width="25px">
      <span class="language help"
            title=":ui.Language.getName(lg)">:lg.upper()</span>
     </td>''')

    # PX acting as a substitute for the field pxView. This PX determines if the
    # field content is multilingual or not. If the field is unilingual, it
    # simply calls a PX named "<layoutType>Uni" on the field. Else, it renders
    # such a PX for every supported language, calling "<layoutType>Uni" for
    # every language, and assembling the result according to the "languages
    # layout". The "Uni" PX receives the current language as variable "lg". If
    # the field is unilingual, the received "lg" variable is None.
    view = edit = cell = Px('''
     <x var="languages=field.getAttribute(o, 'languages');
             multilingual=len(languages) &gt; 1;
             pxUni=getattr(field, '%sUni' % layout)">

      <!-- Display the uni-lingual version of the field -->
      <x if="not multilingual" var2="lg=None">:pxUni</x>

      <!-- Display the multi-lingual version of the field -->
      <x if="multilingual"
         var2="languageLayout=field.getLanguagesLayout(layout)">

       <!-- Horizontally-layouted multilingual field -->
       <table if="languageLayout == 'horizontal'" width="100%"
              class=":(layout == 'cell') and 'no' or ''"
              var="count=len(languages)">
        <tr valign="top"><x for="lg in languages"><x>:field.pxLanguage</x>
         <td width=":'%d%%' % int(100.0/count)"
             var="requestValue=requestValue[lg]|None;
                  value=value[lg]|field.emptyDefault[layout]">:pxUni</td>
        </x></tr></table>

       <!-- Vertically-layouted multilingual field -->
       <table if="languageLayout == 'vertical'"
              class=":(layout == 'cell') and 'no' or ''">
        <tr valign="top" height="20px" for="lg in languages">
         <x>:field.pxLanguage</x>
         <td var="requestValue=requestValue[lg]|None;
                  value=value[lg]|field.emptyDefault[layout]">:pxUni</td>
       </tr></table>
      </x>
     </x>''')

    def __init__(self, languages, languagesLayouts):
        '''Inject multilingual-specific attributes on p_self'''
        # If "languages" holds more than one language, the field will be
        # multi-lingual and several widgets will allow to edit/visualize the
        # field content in all the supported languages. The field is also used
        # by the CK spell checker.
        self.languages = languages
        # When content exists in several languages, how to render them? Either
        # horizontally (one below the other), or vertically (one besides the
        # other). Specify here a dict whose keys are layouts ("edit", "view")
        # and whose values are either "horizontal" or "vertical".
        self.languagesLayouts = languagesLayouts

    def isMultilingual(self, o, dontKnow=False):
        '''Is this field multilingual ? If we don't know, say p_dontKnow'''
        if not o:
            if callable(self.languages):
                # In that case, it is impossible to know
                return dontKnow
            else: return len(self.languages) > 1
        return len(self.getAttribute(o, 'languages')) > 1

    def getLanguagesLayout(self, layout):
        '''Gets the way to render a multilingual field on p_layoutType.'''
        if self.languagesLayouts and (layout in self.languagesLayouts):
            return self.languagesLayouts[layout]
        # Else, return a default value that depends of the format
        return self.defaultLanguagesLayouts[layout]

    def getCopyValue(self, o):
        '''A value being multilingual is stored in a dict. For such a value,
           standard method Field.getCopyValue must return a distinct copy of the
           value as stored on p_obj.'''
        r = self.getValue(o)
        if isinstance(r, dict): r = r.copy()
        return r

    def updateHistoryValue(self, o, values):
        '''If p_self is multilingual, remove its dict value from p_values and
           set, instead, a key for every language-specific value.'''
        languages = self.getAttribute(o, 'languages')
        if len(languages) > 1:
            # Consider every language-specific value as a first-class value:
            # delete the multi-language dict value and replace it with distinct
            # language-specific values, with a special key including the
            # language.
            value = values[self.name]
            del(values[self.name])
            for lg in languages:
                lgPrev = value.get(lg)
                lgCurr = o.values.get(self.name).get(lg)
                if lgPrev != lgCurr:
                    values[(self.name, lg)] = lgPrev

    def valueIsInRequest(self, o, req, name=None, layout='view'):
        '''Multilingual values are stored in specific input fields with
           specific names.'''
        # If we are on the search layout, p_obj, if not None, is certainly not
        # the p_obj we want here (can be a home object).
        if layout == 'search':
            return Field.valueIsInRequest(self, o, req, name, layout)
        languages = self.getAttribute(o, 'languages')
        if len(languages) == 1:
            return Field.valueIsInRequest(self, o, req, name, layout)
        # Is is sufficient to check that at least one of the language-specific
        # values is in the request.
        return ('%s_%s' % (name, languages[0])) in req

    def getRequestValue(self, o, requestName=None):
        '''The request value may be multilingual'''
        req = o.req
        name = requestName or self.name
        languages = self.getAttribute(o, 'languages')
        # A unilingual field
        if len(languages) == 1: return req[name]
        # A multilingual field
        r = {}
        for language in languages:
            r[language] = req['%s_%s' % (name, language)]
        return r

    def isEmptyValue(self, o, value):
        '''Returns True if the p_value must be considered as an empty value'''
        if not isinstance(value, dict):
            return Field.isEmptyValue(self, o, value)
        # p_value is a dict of multilingual values. For such values, as soon
        # as a value is not empty for a given language, the whole value is
        # considered as not being empty.
        for v in value.values():
            if not Field.isEmptyValue(self, o, v): return
        return True

    def isCompleteValue(self, o, value):
        '''Returns True if the p_value must be considered as complete. For a
           unilingual field, being complete simply means not being empty. For a
           multilingual field, being complete means that a value is present for
           every language.'''
        if not self.isMultilingual(o):
            return Field.isCompleteValue(self, o, value)
        # As soon as a given language value is empty, the global value is not
        # complete. If p_value is a string, we are validating a sub-value for a
        # specific language.
        if not value or isinstance(value, str): return True
        for v in value.values():
            if Field.isEmptyValue(self, o, v): return
        return True

    def getFormattedValue(self, o, value, layout='view', showChanges=False,
                          language=None):
        '''The multilingual and unilingual variants of p_value's formatted
           version differ.'''
        # Note that p_language represents the UI language, while variable
        # "languages" below represents the content language(s) of this field.
        languages = self.getAttribute(o, 'languages')
        uni = self.getUniFormattedValue
        if (len(languages) == 1) or isinstance(value, str):
            # Normally, p_value should not be a string if there is a single
            # language. This can happen in exceptional cases, ie, in a
            # object's history (data change), when an object was transmitted
            # from one App1 to App2, where a field is unilingual in App1 and
            # multilingual in App2.
            return uni(o, value, layout, showChanges, language=language)
        # Return the dict of values whose individual, language-specific values
        # have been formatted via m_getUniFormattedValue.
        if not value and not showChanges: return value
        r = {}
        for lg in languages:
            if not value: val = ''
            else: val = value[lg]
            r[lg] = uni(o, val, layout, showChanges,
                        language=language, contentLanguage=lg)
        return r

    def getShownValue(self, o, value, layout='view', showChanges=False,
                      language=None):
        '''For a multilingual field, this method only shows one specific
           language part.'''
        # Be careful: p_language represents the UI language, while variable
        # "languages" below represents the content language(s) of this field.
        languages = self.getAttribute(o, 'languages')
        uni = self.getUniFormattedValue
        if len(languages) == 1:
            return uni(o, value, layout, showChanges, language=language)
        if not value: return value
        # Try to propose the part that is in the user language, or the part of
        # the first content language else.
        lg = o.guard.userLanguage
        if lg not in value: lg = languages[0]
        return uni(o, value[lg], layout, showChanges, language=lg)

    def getIndexValue(self, o, searchable=False, raw=False):
        '''Multilingual variant of Field::getIndexValue. Language parts must be
           concatenated into a single value before being indexed.'''
        r = Field.getIndexValue(self, o, searchable=searchable, raw=True)
        if not r: return
        # Manage multilinguality
        if isinstance(r, dict):
            vals = []
            for val in r.values():
                if val:
                    vals.append(val)
            r = ' '.join(vals)
        # Get the value corresponding to the internal index representation
        index = self.getIndexType(True)
        return index.toString(o, r) if searchable else index.toIndexed(r, self)

    def getStorableValue(self, o, value, complete=False):
        # If no object is passed, assume the field is unilingual
        if o is None:
            return self.getUniStorableValue(o, value)
        # Check unilinguality
        languages = self.getAttribute(o, 'languages')
        if len(languages) == 1:
            return self.getUniStorableValue(o, value)
        # A multilingual value is stored as a dict whose keys are ISO 2-letters
        # language codes and whose values are strings storing content in the
        # language ~{s_language: s_content}~.
        if not value: return
        # p_value may hold a part of the complete value, in some language
        if isinstance(value, str):
            return self.getUniStorableValue(o, value)
        # Manage a multilingual p_value
        for lg in languages:
            value[lg] = self.getUniStorableValue(o, value[lg])
        return value

    def store(self, o, value):
        '''Stores p_value on p_o for this field'''
        languages = self.getAttribute(o, 'languages')
        if (len(languages) > 1) and value and \
           (not isinstance(value, dict) or (len(value) != len(languages))):
            raise Exception(INVALID_MULTILINGUAL_VALUE % self.name)
        Field.store(self, o, value)

    def storeValueFromAjax(self, o, value, currentValues):
        '''Stores p_value on p_o, taking care of multilinguality'''
        # Call the base method if p_self is not multilingual
        if not self.isMultilingual(o):
            return Field.storeValueFromAjax(self, o, value, currentValues)
        # Manage a multilingual field
        if currentValues is not None:
            # Take a copy of currentValues because it is mutable (dict)
            data = currentValues[self.name]
            if data is not None: data = data.copy()
            currentValues[self.name] = data
        # We get a partial value, for one language only
        language = o.req.languageOnly
        v = self.getUniStorableValue(o, value)
        o.values[self.name][language] = v
        return ' (%s)' % language
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
