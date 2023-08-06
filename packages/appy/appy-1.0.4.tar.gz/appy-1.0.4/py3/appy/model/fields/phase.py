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
import collections
from appy.px import Px
from appy.utils import iconParts
from appy.model.utils import Object

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
NO_CUR_PAGE = 'There is no current page to show. The default page for this ' \
              'object is probably invisible. Please define method ' \
              'getDefaultViewPage and / or getDefaultEditPage To overcome ' \
              'the problem.'

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Page:
    '''Used for describing a page, its related phase, show condition, etc.'''
    subElements = ('save', 'cancel', 'edit')

    def __init__(self, name, phase='main', show=True, showSave=True,
                 showCancel=True, showEdit=True, label=None, icon=None,
                 sticky='edit'):
        # A short, camel-cased unique page, that must be unique across all
        # phases within the same class
        self.name = name
        # The name of the phase containing this page
        self.phase = phase
        # When must the page be shown ? The following attribute can hold values
        # True, False, "view" or "edit", or a method producing such a value,
        # accepting the current object, as unique arg.
        self.show = show
        # When editing the page, must the "save" button be shown ?
        self.showSave = showSave
        # When editing the page, must the "cancel" button be shown ?
        self.showCancel = showCancel
        # When viewing the page, must the "edit" icon be shown ?
        self.showEdit = showEdit
        # The i18n label may be forced here instead of being deduced from the
        # page name.
        self.label = label
        # The icon to display. If you want to use:
        # * one of the standard Appy icons, residing in appy/ui/static, use
        #   string "appy/<icon_name>", for example "appy/help.svg";
        # * an icon being in your app's "static" folder, use string
        #   "<app_name>/<icon_name>";
        # * an icon that is chosen dynamically, set a method from the class
        #   where this page is defined. It will be called without arg and must
        #   return the icon URL, or None if the icon is not available (yet).
        #   Here are some tips.
        #   1) If you want to build the URL to a standard Appy icon, use, ie:
        #      o.buildUrl('help.svg')
        #      ("o" being any instance of any Appy class)
        #   2) If you want to build the URL to an icon being in your app's
        #      "static" folder, use, ie:
        #      o.buildUrl('myIcon.png', base='MyApp')
        #   3) If you want to build the URL to an icon that was uploaded in a
        #      File field, use:
        #      '%s/<field_name>/download' % o.url
        self.setIcon(icon or 'page.svg')
        # Stickyness refers to the complete block of controls that is shown for
        # the current object, when this page is shown. Attribute "sticky" may
        # hold True, False, "edit" or "view", and determines if the block must
        # be sticky when this page is shown on "edit", "view" or both layouts.
        # When sticky, the block remains visible, even when scrollling down the
        # page. It is enabled by default on "edit" layouts only, because
        # stickyness of the block of controls may be in conflict with stickyness
        # of parts of fields shown on the the same page, ie, headers of tables
        # for Ref or List fields. If several sticky elements are present, when
        # scrolling, they will unsightly overlap.
        self.sticky = sticky

    def clone(self):
        '''Create a clone of p_self'''
        r = Page(self.name)
        for k, v in self.__dict__.items(): setattr(r, k, v)
        return r

    def setIcon(self, icon):
        '''Sets this p_icon for p_self'''
        if callable(icon):
            self.icon = icon
            self.iconBase = None
        else:
            self.icon, self.iconBase = iconParts(icon)

    @staticmethod
    def get(pageData):
        '''Produces a Page instance from p_pageData. User-defined p_pageData
           can be:
           (a) a string containing the name of the page;
           (b) a string containing <pageName>_<phaseName>;
           (c) a Page instance.
           This method returns always a Page instance.'''
        r = pageData
        if r and isinstance(r, str):
            # Page data is given as a string
            pageElems = pageData.rsplit('_', 1)
            if len(pageElems) == 1: # We have case (a)
                r = Page(pageData)
            else: # We have case (b)
                r = Page(pageData[0], phase=pageData[1])
        return r

    def isShowable(self, o, layout, elem='page'):
        '''Is this page showable for p_o on p_layout ("view" or "edit")?

           If p_elem is not "page", this method returns the fact that a
           sub-element is viewable or not (buttons "save", "cancel", etc).'''
        # Define what attribute to test for "showability"
        attr = 'show' if elem == 'page' else 'show%s' % elem.capitalize()
        # Get the value of the "show" attribute as identified above
        r = getattr(self, attr)
        if callable(r):
            r = o.H().methods.call(o, r)
        if isinstance(r, str): return r == layout
        return r

    def nextName(self):
        '''If this page has a name being part of a series (ie numeric:
           1, 2, 3... or alphabetical like a, b, c...), this method returns the
           next name in the series.'''
        name = self.name
        if name.isdigit():
            # Increment this number by one and get the result as a string
            r = str(int(name) + 1)
        elif (len(name) == 1) and name.islower() and (name != 'z'):
            r = chr(ord(name) + 1)
        else:
            # Repeat the same name
            r = name
        return r

    def __repr__(self): return '<Page %s - phase %s>' % (self.name, self.phase)

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class UiPage:
    '''A page object built at run time, containing only information tied to the
       execution context.'''

    def __init__(self, uiPhase, page, showOnView, showOnEdit):
        # The link to the container phase
        self.uiPhase = uiPhase
        # The corresponding Page instance
        self.page = page
        self.name = page.name
        # Must the page be shown on view/edit layouts ?
        self.showOnView = showOnView
        self.showOnEdit = showOnEdit
        # Must sub-elements (buttons "save", "cancel", etc) be shown ?
        phases = uiPhase.container
        o = phases.o
        layout = phases.layout
        for elem in Page.subElements:
            showable = page.isShowable(o, layout, elem)
            setattr(self, 'show%s' % elem.capitalize(), showable)
        # Define the icon to display
        self.iconUrl = self.getIconUrl(o)

    def __repr__(self):
        '''p_self's string representation'''
        return '<UiPage %s>' % self.name

    def getLabel(self):
        '''Returns the translated label for this page, potentially based on a
           fixed label if p_self.label is not empty.'''
        page = self.page
        o = self.uiPhase.container.o
        label = page.label or '%s_page_%s' % (o.class_.name, page.name)
        return o.translate(label)

    def showable(self, layout):
        '''Return True if this page is showable on p_layout'''
        return self.showOnEdit if layout == 'edit' else self.showOnView

    def getIconUrl(self, o):
        '''Compute the URL to the icon to display for this page'''
        page = self.page
        # The icon to show
        if callable(page.icon):
            url = page.icon(o)
            if url: return url
            # The icon may not be available yet. For example, we may be creating
            # an object having a field that will be used to store the page icon,
            # but no image has been uploaded yet.
            base = 'appy'
            icon = 'page.svg'
        else:
            base, icon = page.iconBase, page.icon
        return o.buildUrl(icon, base)

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Phase:
    '''A phase is a group of pages within a class'''

    # This class is used only in order to generate phase- and page-related i18n
    # labels, and as general information about all phases and pages defined for
    # a class in the app's model.

    # It is not used by the Appy developer: if a phase must be defined by him in
    # an app, he will do it via a phase name specified as a string, in attribute
    # "phase" of class Page hereabove.

    # It is not used by Appy at run-time neither: class UiPhases is used
    # instead. Indeed, at run-time, the set of phases and pages which are
    # visible by the logged user can be a sub-set of all statically-defined
    # phases and pages.

    def __init__(self, name):
        self.name = name
        # A phase is made of pages ~{p_name: appy.model.fields.page.Page}~
        self.pages = collections.OrderedDict()

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class UiPhase:
    '''A phase object built at run time, containing only the visible pages
       depending on user's permissions.'''

    view = Px('''
     <div class=":'phase phaseC' if compact else 'phase'"
          if="phase.showPages(singlePhase, isEdit)">

      <!-- Siblings navigation -->
      <div var="nav=req.nav"
           if="not isEdit and (phase.name=='main') and (nav) and (nav != 'no')"
           var2="self=ui.Siblings.get(nav, tool, _ctx_)">:self.pxNavigate</div>

      <!-- Page(s) within the phase -->
      <div if="not isEdit" for="pag in phase.pages.values()"
           var2="isCurrent=pag.name == page"
           id=":'currentPage' if isCurrent else ''"
           class=":'currentPage' if isCurrent else ''">

       <!-- This additional div is used to vertically align its content -->
       <div var="viewUrl=o.getUrl(sub='view',page=pag.name,popup=popup,nav=nav)\
                  if pag.showOnView else None;
                 pictoUrl=pag.iconUrl">
        <!-- The edit or lock icon -->
        <x var="locked=o.Lock.isSet(o, user, pag.name);
               editable=mayEdit and mayAct and pag.showOnEdit and pag.showEdit">
         <a if="editable and not locked"
            href=":o.getUrl(sub='edit', page=pag.name, popup=popup, nav=nav)">
          <img src=":url('edit.svg')" class="pictoT shake"
               title=":_('object_edit')"/></a>
         <x var="page=pag.name; lockStyle='iconM pictoT'">::o.Lock.px</x>
        </x>

        <!-- Main icon -->
        <div><a if="viewUrl" href=":viewUrl">
              <img src=":pictoUrl" class=":picto"/></a>
         <img if="not viewUrl" src=":pictoUrl" class=":picto"/>
        </div>

        <!-- Page name and icons -->
        <x var="label=Px.truncateText(pag.getLabel(), 25)">
         <a if="viewUrl" href=":viewUrl">::label</a>
         <x if="not viewUrl">::label</x>
        </x>
       </div>
      </div>

      <!-- Additional object controls -->
      <x>:o.pxButtons</x>
     </div>''',

     # Class names ending with "C" are used when controls are *C*ompact
     css='''
      .phase { margin: 0 0 30px -30px; display: flex; flex-wrap: wrap;
               width: fit-content }
      .phase > div { height: 115px; width: 125px; text-align: center;
        text-transform: uppercase; font-weight: bold; font-size: 90%;
        display: flex; align-items: center; justify-content: center;
        background-color: white; position: relative; padding: 0 5px;
        border-right: 1px solid |linkColor|; border-top: 1px solid |linkColor|;
        border-bottom: 1px solid |linkColor| }

      .phaseC { margin: 0 0 20px 0; border-left: 1px solid |linkColor| }
      .phaseC > div { height: 80px; width: 110px; font-size: 9pt }

      .picto { width: 55px; height: 55px; margin-bottom: 6px }
      .pictoT { position: absolute; top: 8px; right: 8px; width: 22px }
      .pictoC, .pictoB { width: 35px; height: 35px; margin-bottom: 4px }
      .inverted { filter: invert(66%) }

      .currentPage { background-color: |darkColor| !important;
                     color: |brightColor| }
      .currentPage img { filter: invert(66%) }
      .currentPage a { color: |brightColor| }

      // Animation for the "edit" icon
      @keyframes shakeImage {
        0% { transform: rotate(0deg); filter: sepia(0) }
        95% { transform: rotate(0deg); filter: sepia(0) }
        97% { transform: rotate(10deg); filter: sepia(1) }
        99% { transform: rotate(-10deg); filter: sepia(0.6) }
        100% { transform: rotate(0deg); filter: sepia(0.3) }
      }
      .shake { animation: shakeImage 10s infinite }''')

    def __init__(self, name, phases):
        # The name of the phase
        self.name = name
        # Its translated label
        o = phases.o
        self.label = o.translate('%s_phase_%s' % (o.class_.name, name))
        # A link to the global UiPhases object
        self.container = phases
        # The included pages, as a dict of UiPage instances
        self.pages = collections.OrderedDict()
        # The pages that were already walked, but that must not be shown
        self.hidden = {}

    def addPage(self, page):
        '''Adds page-related information in the phase'''
        # If the page is already there, we have nothing more to do
        if (page.name in self.pages) or (page.name in self.hidden): return
        # Add the page only if it must be shown
        o = self.container.o
        currentPage = self.container.currentPage
        showOnView = page.isShowable(o, 'view')
        showOnEdit = page.isShowable(o, 'edit')
        if showOnView or showOnEdit:
            # The page must be added
            self.pages[page.name] = self.container.lastPage = \
              UiPage(self, page, showOnView, showOnEdit)
            # Set it as current page when relevant
            if currentPage is None and \
               (page.name == self.container.currentPageName):
                self.container.currentPage = self.container.lastPage
        else:
            # The page must be hidden, and we must remember that fact
            self.hidden[page.name] = None

    def showPages(self, singlePhase, isEdit):
        '''Pages for this phase must not be shown if there is a single,
           not-editable page within a single phase.'''
        # If we are on an "edit" layout, the "pages" zone must always be shown
        # because it will contain at least the "save" and "cancel" buttons.
        if isEdit: return True
        if singlePhase and (len(self.pages) == 1):
            for page in self.pages.values():
                return page.showOnEdit
        return True

    def __repr__(self):
        if self.pages:
            pages = ': page(s) %s' % ','.join(list(self.pages.keys()))
        else:
            pages = ' (empty)'
        return '<phase %s%s>' % (self.name, pages)

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class UiPhases:
    '''Represents the (sub-)set of phases and pages for some object that the
       currently logged user may see or edit.'''

    # PX displaying all phases of a given object
    view = Px('''
     <x var="mayEdit=guard.mayEdit(o);
             singlePhase=phases.singlePhase();
             id=o.iid">

      <!-- Single phase: display its pages -->
      <x if="singlePhase or isEdit"
         var2="phase=phases.default">:phase.view</x>

      <!-- Several phases: add a tab for every phase -->
      <x if="not singlePhase and not isEdit">
       <table cellpadding="0" cellspacing="0">
        <!-- First row: the tabs -->
        <tr><td class="tabSep">
         <table class="tabs" id=":'tabs_%d' % id">
          <tr valign="middle">
           <x for="phase in phases.all.values()"
              var2="suffix='%d_%s' % (id, phase.name);
                    tabId='tab_%s' % suffix">
            <td id=":tabId" class="tab">
             <a onclick=":'showTab(%s)'% q(suffix)"
                class="clickable">:phase.label</a>
            </td>
           </x>
          </tr>
         </table>
        </td></tr>
        <!-- Other rows: the fields -->
        <tr for="phase in phases.all.values()"
            id=":'tabcontent_%d_%s' % (id, phase.name)"
          style=":(loop.phase.nb==0) and 'display:table-row' or 'display:none'">
         <td>:phase.view</td>
        </tr>
       </table>
       <script>:'initTab(%s,%s)' % \
             (q('tab_%d' % id), q('%d_%s' % (id, phases.default.name)))</script>
      </x>
      <script>:'initPages(%d)' % phases.getStickyIndex(table)</script>
     </x>''',

     js = '''
      function invertPage(div, on) {
        // Do nothing if p_div correspond to the currently selected page
        if (div.id == 'currentPage') return;
        // Switch the page to dark mode
        var classes = div.classList,
            inverted = classes.contains('currentPage');
        if (on && !inverted) classes.add('currentPage');
        else if (!on && inverted) classes.remove('currentPage');
      }

      function initPages(rowIndex) {
        // Inject code allowing to switch between the (un)selected page view
        var phases = document.getElementsByClassName('phase'),
            divs=null, div=null;
        for (var i=0; i < phases.length; i++) {
          divs = phases[i].childNodes;
          for (var j=0; j < divs.length; j++) {
            div = divs[j];
            if (div.tagName == 'DIV') {
              div.addEventListener('mouseenter',
                                   function(){invertPage(this,true)});
              div.addEventListener('mouseleave',
                                   function(){invertPage(this,false)});
            }
          }
        }
        if (rowIndex != -1) {
          // Make the controls sticky
          var table = document.getElementById('pageLayout'),
              firstCell = table.childNodes[0].rows[rowIndex].cells[0];
          firstCell.classList.add('sticky');
        }
      }''')

    def __init__(self, page, o, layout):
        '''Initialises a structure allowing to render currently visible phases
           for p_o, for which the page named p_page is currently shown.'''
        # The object for which phases must be produced
        self.o = o
        # The layout
        self.layout = layout
        # The involved phases will be stored here, as UiPhase instances
        self.all = collections.OrderedDict()
        # The default phase (= the first encountered one)
        self.default = None
        # The currently shown page
        self.currentPageName = page
        self.currentPage = None
        # p_o's default page on p_layout
        self.defaultPageName = o.getDefaultPage(layout)
        # The last inserted page
        self.lastPage = None

    def singlePhase(self):
        '''Returns True if there is a single phase'''
        return len(self.all) == 1

    def singlePage(self):
        '''Returns True if there is a single page within a single phase'''
        if not self.singlePhase(): return
        return len(self.default.pages) == 1

    def addField(self, field):
        '''A new p_field has been encountered: it implies updating phases and
           pages.'''
        # Insert p_fields' phase and page into p_self.all
        phase = field.page.phase
        if phase not in self.all:
            uiPhase = self.all[phase] = UiPhase(phase, self)
            # Set it as default phase if there is no default phase yet
            if self.default is None:
                self.default = uiPhase
        else:
            uiPhase = self.all[phase]
        uiPhase.addPage(field.page)

    def unshowableCurrentPage(self):
        '''Return True if the current page can't be shown'''
        # The default page is always supposed to be showable
        if self.currentPageName == self.defaultPageName: return
        current = self.currentPage
        return not current or not current.showable(self.layout)

    def finalize(self):
        '''Finalize phases, ie, by removing phases without any visible page'''
        # Remove phases without page
        toDelete = None
        for name in self.all.keys():
            if not self.all[name].pages:
                if toDelete is None: toDelete = []
                toDelete.append(name)
        if toDelete is not None:
            for name in toDelete:
                del(self.all[name])
        # If p_self.currentPage is None, it will crash. Set, as current page,
        # the first visible page, just to avoid a crash.
        if not self.currentPage:
            raise Exception(NO_CUR_PAGE)

    def getStickyIndex(self, table):
        '''Returns the index of the element, within the page layout represented
           by p_table, that must be made sticky.'''
        # If stickyness must not be enabled for the current page, return -1
        sticky = self.currentPage.page.sticky
        sticky = (sticky == self.layout) if isinstance(sticky, str) else sticky
        return table.getRowIndex('b') if sticky else -1
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
