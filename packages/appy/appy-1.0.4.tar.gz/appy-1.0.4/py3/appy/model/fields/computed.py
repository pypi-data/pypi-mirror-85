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
from appy.px import Px
from appy.model.fields import Field, Show
from appy.ui.layout import Layouts, Layout
from appy.model.searches import Search, UiSearch

# Error messages - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
UNFREEZABLE = 'This field is unfreezable.'
WRONG_METHOD = 'Wrong value "%s". Param "method" must contain a method or a PX.'

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Computed(Field):
    '''Useful for computing a custom field via a Python method'''

    class Layouts(Layouts):
        '''Computed-specific layouts'''
        # Layouts for fields in a grid group, with description
        gd = Layouts('f-drvl')
        # Idem, but with a help icon
        gdh = Layouts('f-dhrvl')

    view = cell = edit = Px('''<x if="field.plainText">:value</x><x
      if="not field.plainText">::value</x>''')

    search = Px('''
     <input type="text" name=":widgetName" maxlength=":field.maxChars"
            size=":field.width" value=":field.sdefault"/>''')

    def __init__(self, multiplicity=(0,1), default=None, defaultOnEdit=None,
      show=None, page='main', group=None, layouts=None, move=0, indexed=False,
      mustIndex=True, indexType=None, indexValue=None, emptyIndexValue=None,
      searchable=False, filterField=None, readPermission='read',
      writePermission='write', width=None, height=None, maxChars=None,
      colspan=1, method=None, formatMethod=None, plainText=False, master=None,
      masterValue=None, focus=False, historized=False, mapping=None,
      generateLabel=None, label=None, sdefault='', scolspan=1, swidth=None,
      sheight=None, context=None, view=None, cell=None, edit=None, xml=None,
      translations=None, unfreezable=False, validable=False):
        # The Python method used for computing the field value, or a PX
        self.method = method
        # A specific method for producing the formatted value of this field.
        # This way, if, for example, the value is a DateTime instance which is
        # indexed, you can specify in m_formatMethod the way to format it in
        # the user interface while m_method computes the value stored in the
        # catalog.
        self.formatMethod = formatMethod
        if isinstance(self.method, str):
            # A legacy macro identifier. Raise an exception
            raise Exception(WRONG_METHOD % self.method)
        # Does field computation produce plain text or XHTML?
        self.plainText = plainText
        if isinstance(method, Px):
            # When field computation is done with a PX, the result is XHTML
            self.plainText = False
        # Determine default value for "show"
        if show is None:
            # XHTML content in a Computed field generally corresponds to some
            # custom XHTML widget. This is why, by default, we do not render it
            # in the xml layout.
            show = Show.E_ if self.plainText else Show.TR
        # If method is a PX, its context can be given in p_context
        self.context = context
        # For any other Field subclass, the type of the index to use is
        # statically determined. But for an indexed Computed field, which may
        # hold any data of any type, the index type must be specified in
        # p_indexType. Choose it in this list, depending on the values that your
        # field will store.
        self.indexType = indexType or 'Index'
        # ----------------------------------------------------------------------
        #   Index type   | Suitable...
        # ----------------------------------------------------------------------
        #     "Index"    | ... in most cases, when none of the following index
        #                |     types are appropriate ;
        # ----------------------------------------------------------------------
        #   "RefIndex"   | ... for storing lists of Appy objects (=instances of
        #                |     Appy classes). You should not use this type of 
        #                |     index and use a Ref field for storing lists of
        #                |     objects ;
        # ----------------------------------------------------------------------
        #   "DateIndex"  | ... if your field stores DateTime instances ;
        # ----------------------------------------------------------------------
        #   "TextIndex"  | ... if your field stores raw text and you want to
        #                |     index words in found in it ;
        # ----------------------------------------------------------------------
        #   "RichIndex"  | ... if your field stores a chunk of XHTML code and 
        #                |     you want to index text extracted from it ;
        # ----------------------------------------------------------------------
        #  "FloatIndex"  | ... if your field stores float values ;
        # ----------------------------------------------------------------------
        # "BooleanIndex" | ... if your field stores boolean values.
        # ----------------------------------------------------------------------
        # Call the base constructor
        Field.__init__(self, None, multiplicity, default, defaultOnEdit, show,
          page, group, layouts, move, indexed, mustIndex, indexValue,
          emptyIndexValue, searchable, filterField, readPermission,
          writePermission, width, height, None, colspan, master, masterValue,
          focus, historized, mapping, generateLabel, label, sdefault, scolspan,
          swidth, sheight, False, False, view, cell, edit, xml, translations)
        # When a custom widget is built from a computed field, its values are
        # potentially editable and validable, so "validable" must be True.
        self.validable = validable
        # One classic use case for a Computed field is to build a custom widget.
        # In this case, self.method stores a PX or method that produces, on
        # view or edit, the custom widget. Logically, you will need to store a
        # custom data structure on the object, in an attribute named according
        # to this field, ie o.[self.name]. Typically, you will set or update a
        # value for this attribute in m_onEdit, by getting, on the o.req object,
        # values encoded by the user in your custom widget (edit mode). This
        # "custom widget" use case is incompatible with "freezing". Indeed,
        # freezing a Computed field implies storing the computed value at
        # o.[self.name] instead of recomputing it as usual. So if you want to
        # build a custom widget, specify the field as being unfreezable.
        self.unfreezable = unfreezable
        # Set a filter PX if this field is indexed with a TextIndex
        if self.indexed and (self.indexType == 'TextIndex'):
            self.filterPx = 'pxFilterText'

    def renderPx(self, o, px):
        '''Renders the p_px and returns the result'''
        traversal = o.traversal
        context = traversal.context or traversal.createContext()
        # Complete the context when relevant
        custom = self.context
        custom = custom if not callable(custom) else custom(o)
        if custom:
            context.update(custom)
        return px(context)

    def renderSearch(self, o, search):
        '''Executes the p_search and return the result'''
        req = o.req
        # This will allow the UI to find this search
        req.search = '%d,%s,view' % (o.iid, self.name)
        req.className = search.container.name
        traversal = o.traversal
        existingContext = traversal.context
        context = traversal.createContext()
        r = context.uiSearch.pxResult(context)
        # Reinitialise the context correctly
        if existingContext:
            traversal.context = existingContext
        return r

    def getSearch(self, o):
        '''Gets the Search instance possibly linked to this Computed field'''
        method = self.method
        if not method: return
        if isinstance(method, Search): return method
        # Maybe a dynamically-computed Search ?
        r = self.callMethod(o, method, cache=False)
        if isinstance(r, Search): return r

    def getValue(self, o, name=None, layout=None, forceCompute=False):
        '''Computes the field value on p_obj or get it from the database if it
           has been frozen.'''
        # Is there a database value ?
        if not self.unfreezable and not forceCompute:
            r = o.values.get(self.name)
            if r is not None: return r
        # Compute the value
        meth = self.method
        if not meth: return
        if isinstance(meth, Px): return self.renderPx(o, meth)
        elif isinstance(meth, Search): return self.renderSearch(o, meth)
        else:
            # self.method is a method that will return the field value
            r = self.callMethod(o, meth, cache=False)
            # The field value can be a dynamically computed PX or Search
            if isinstance(r, Px): return self.renderPx(o, r)
            elif isinstance(r, Search): return self.renderSearch(o, r)
            return r

    def getFormattedValue(self, o, value, layout='view', showChanges=False,
                          language=None):
        if self.formatMethod:
            r = self.formatMethod(o, value)
        else:
            r = value
        if not isinstance(r, str): r = str(r)
        return r

    # If you build a custom widget with a Computed field, Appy can't tell if the
    # value in your widget is complete or not. So it returns True by default.
    # It is up to you, in method obj.validate, to perform a complete validation,
    # including verifying if there is a value if your field is required.
    def isCompleteValue(self, o, value): return True

    def freeze(self, o, value=None):
        '''Normally, no field value is stored for a Computed field: the value is
           computed on-the-fly by p_self.method. But if you freeze it, a value
           is stored: either p_value if not None, or the result of calling
           p_self.method else. Once a Computed field value has been frozen,
           everytime its value will be requested, the frozen value will be
           returned and p_self.method will not be called anymore. Note that the
           frozen value can be unfrozen (see method below).'''
        if self.unfreezable: raise Exception(UNFREEZABLE)
        # Compute for the last time the field value if p_value is None
        if value is None: value = self.getValue(o, forceCompute=True)
        # Freeze the given or computed value (if not None) in the database
        if value is not None: o.values[self.name] = value

    def unfreeze(self, o):
        '''Removes the database value that was frozen for this field on p_o'''
        if self.unfreezable: raise Exception(UNFREEZABLE)
        if self.name in o.values: del(o.values[self.name])
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
