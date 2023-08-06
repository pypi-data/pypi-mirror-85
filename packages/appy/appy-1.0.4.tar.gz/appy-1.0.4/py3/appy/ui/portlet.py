'''Portlet management'''

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

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Portlet:
    '''The portlet, in the standard layout, is a zone from the UI shown as a
       column situated at the left of the screen for left-to-right languages,
       and at the right for right-to-left languages.'''

    @classmethod
    def show(class_, tool, px, ctx):
        '''When must the portlet be shown ?'''
        # Do not show the portlet on 'edit' pages, if we are in the popup or if
        # there is no root class.
        if ctx.popup or (ctx.layout == 'edit') or (px.name == 'home') or \
           (ctx.config.model.rootClasses is None):
            return
        # If we are here, portlet visibility depends on the app, via method
        # "tool::showPortletAt", when defined.
        return tool.showPortletAt(ctx.handler.path) \
               if hasattr(tool, 'showPortletAt') else True

    px = Px('''
     <div var="collapse=ui.Collapsible.get('portlet', dleft, req);
           toolUrl=tool.url;
           queryUrl='%s/Search/results' % toolUrl;
           cfg=config.ui;
           currentSearch=req.search;
           currentClass=req.className;
           currentPage=handler.parts[-1];
           rootClasses=handler.server.model.getRootClasses()"
      id="appyPortlet" class="portlet" style=":collapse.style">

      <!-- The portlet logo when present -->
      <center>
       <img src=":url('portletLogo')" class="portletLogo"/></center>

      <!-- One section for every searchable root class -->
      <x for="class_ in rootClasses" if="class_.maySearch(tool, layout)"
         var2="className=class_.name">

       <!-- A separator -->
       <div class="portletSep"></div>

       <!-- Section title (link triggers the default search) -->
       <div class="portletContent"
            var="searches=class_.getGroupedSearches(tool, _ctx_);
                 labelPlural=_(className + '_plural');
                 indexable=class_.isIndexable();
                 viaPopup=None">
        <div class="portletTitle">
         <a if="indexable"
            var="queryParam=searches.default.name if searches.default else ''"
            href=":'%s?className=%s&amp;search=%s' % \
                   (queryUrl, className, queryParam)"
            onclick="clickOn(this)"
            class=":(not currentSearch and (currentClass==className) and \
                    (currentPage == 'pxResults')) and \
                    'current' or ''">::labelPlural</a>
         <x if="not indexable">::labelPlural</x>
        </div>

        <!-- Create instances of this class -->
        <div if="guard.mayInstantiate(class_)"
             var2="asButton=False; nav='no'">:class_.pxAdd</div>

        <!-- Searches -->
        <x if="indexable and class_.maySearchAdvanced(tool)">

         <!-- Live search -->
         <x var="pre=className; liveCss='lsSearch'">:tool.Search.live</x>

         <!-- Advanced search -->
         <div var="highlighted=(currentClass == className) and \
                               (req.search == 'customSearch')"
              class=":'portletAdv current' if highlighted else 'portletAdv'">
          <img src=":url('search.svg')" class="iconM"/>
          <a var="text=_('search_title')"
             href=":'%s/Search/advanced?className=%s' % (toolUrl, className)"
             title=":text"><x>:text</x>...</a>
         </div>
        </x>

        <!-- Predefined searches -->
        <x for="search in searches.all" var2="field=search">
         <x>:search.px if search.type == 'group' else search.view</x>
        </x>

        <!-- Portlet bottom, potentially customized by the app -->
        <x var="pxBottom=getattr(class_.python, 'portletBottom', None)"
           if="pxBottom">:pxBottom</x>
       </div>
      </x>
     </div>''',

     css='''
       .portlet { padding: 30px 50px 0 0; box-shadow: 2px 2px 5px #002039;
                  position: sticky; position: -webkit-sticky; top: 0;
                  overflow-y:auto; overflow-x: auto; width: 250px;
                  min-width: 140px; font-size: 98%; z-index: 4 }
       .portletSearch a:hover { background-color:|linkColor|;
                                color:|brightColor| }
       .portletContent { padding-left: 18px; width: 200px }
       .portletContent input[type=text] { background-color: white }
       .portletTitle { padding: 5px 0; text-transform: uppercase }
       .portletLogo { margin-bottom: 15px }
       .portletSep { border-top: 1px solid #002039; margin: 25px 0 20px 0 }
       .portletGroup { text-transform: uppercase; padding: 5px 0 0 0;
                  margin: 0.5em 2px 0.3em }
       .portletAdv { margin: 3px 0 10px }
       .portletAdv img { margin: -2px 4px 0 1px; float: left}
       .portletSearch { text-align: left }
       .portletCurrent { font-weight: bold }
       .portlet form { margin-top: 5px }
       input.buttonPortlet { border: 0; background-position: 0 }
     ''')
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
