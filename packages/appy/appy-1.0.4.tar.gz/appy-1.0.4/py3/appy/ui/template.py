'''Base template for any UI page'''

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
class Template:
    # The global page header
    pxHeader = Px('''
     <div class="topBase"
          style=":cfg.getBackground(_px_, siteUrl, type='header')">
      <div class="top">

       <!-- The burger button for collapsing the portlet -->
       <a if="showPortlet" class="burger"
          onclick="toggleCookie('appyPortlet','block','expanded',\
                'show','hide')"><img src=":url('burger.svg')" class="icon"/></a>

       <!-- Links and icons -->
       <div class="topIcons">

        <!-- Custom links -->
        <x>:tool.pxLinks</x>

        <!-- Header messages -->
        <span class="topText" var="text=cfg.getHeaderText(tool)"
              if="not popup and text">::text</span>

        <!-- The home icon -->
        <a if="not isAnon" href=":tool.computeHomePage()">
          <img src=":url('home.svg')" class="icon"/></a>

        <!-- Connect link if discreet login -->
        <a if="isAnon and cfg.discreetLogin" id="loginIcon"
           name="loginIcon" onclick="toggleLoginBox(true)" class="clickable">
         <img src=":url('login.svg')" class="icon"/>
         <span class="topText">:_('app_connect')</span>
         </a>

        <!-- Root pages -->
        <x var="pages=tool.getRootPages()"
           if="pages">:tool.OPage.pxSelector</x>

        <!-- Language selector -->
        <x if="ui.Language.showSelector(cfg, \
                                           layout)">:ui.Language.pxSelector</x>

        <!-- User info and controls for authenticated users -->
        <x if="not isAnon">
         <!-- Config -->
         <a if="cfg.showTool(tool)" href=":'%s/view' % tool.url"
                title=":_('Tool')">
          <img src=":url('config.svg')" class="icon"/></a>
         <x>:user.pxUserLink</x>
         <!-- Log out -->
         <a href=":guard.getLogoutUrl(tool, user)" title=":_('app_logout')">
          <img src=":url('logout.svg')" class="icon"/></a>
        </x>
        <!-- Custom links at the end of the list -->
        <x>:tool.pxLinksAfter</x>
       </div>

       <!-- The burger button for collapsing the sidebar -->
       <a if="showSidebar" class="burger"
          onclick="toggleCookie('appySidebar','block','expanded',\
             'show','hide')"><img src=":url('burger.svg')" class="icon"/></a>
      </div>
     </div>''',

     css='''
      .topBase { background-color:|headerBgColor|; width:100%; position:fixed;
                 color:|headerColor|; font-weight:lighter; z-index:1 }
      .top { height:|headerHeight|; display:flex; flex-wrap:nowrap;
             justify-content:space-between; align-items:center; margin:0 5px }
      .topIcons { margin-|headerMargin|:auto }
      .topIcons > a, .topIcons > select { margin:0 5px; color:|headerColor| }
      .topText { letter-spacing:1px; padding: 0 8px }
      .burger { cursor:pointer; margin:0 5px }''')

    # The template of all base PXs
    px = Px('''
     <html var="x=handler.customInit(); cfg=config.ui" dir=":dir">

      <head>
       <title>:tool.getPageTitle(home)</title>
       <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1"/>
       <link rel="icon" type="image/x-icon"
             href=":url('favicon.ico', base=appName)"/>
       <link rel="apple-touch-icon" href=":url('appleicon', base=appName)"/>
       <x>::ui.Includer.getGlobal(handler, config, dir)</x>
      </head>

      <body class=":cfg.getClass('body', _px_, _ctx_)"
            var="showPortlet=ui.Portlet.show(tool, _px_, _ctx_);
                 showSidebar=ui.Sidebar.show(tool, o, layout, popup);
                 bi=ui.Browser.getIncompatibilityMessage(tool, handler)">

       <!-- The browser incompatibility message -->
       <div if="bi" class="wrongBrowser">::bi</div>

       <!-- Google Analytics stuff, if enabled -->
       <script var="gaCode=tool.getGoogleAnalyticsCode(handler, config)"
               if="gaCode">:gaCode</script>

       <!-- Popups -->
       <x>::ui.Globals.getPopups(tool, url, _, dleft, dright, popup)</x>

       <div class=":cfg.getClass('main', _px_, _ctx_)"
            style=":cfg.getBackground(_px_, siteUrl, type='home')">

        <!-- The page header -->
        <x if="cfg.showHeader(_px_, _ctx_, popup)">:ui.Template.pxHeader</x>

        <!-- The message zone -->
        <div height="0">:ui.Message.px</div>

        <!-- The login zone -->
        <x if="isAnon and not o.isTemp() and not bi">:guard.pxLogin</x>

        <!-- The main zone: portlet, content and sidebar -->
        <div class=":'payload payloadP' if popup else 'payload'"
             style=":cfg.getBackground(_px_, siteUrl, \
                                       type='popup' if popup else 'base')">

         <!-- The portlet -->
         <x if="showPortlet">:ui.Portlet.px</x>

         <!-- Page content -->
         <div class=":'contentP' if popup or (_px_.name == 'public') \
                                 else 'content'">:content</div>

         <!-- The sidebar -->
         <x if="showSidebar">:ui.Sidebar.px</x>
        </div>

        <!-- Footer -->
        <x if="cfg.showFooter(_px_, _ctx_, popup)">::ui.Footer.px</x>
       </div>
      </body>
     </html>''', prologue=Px.xhtmlPrologue)
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
