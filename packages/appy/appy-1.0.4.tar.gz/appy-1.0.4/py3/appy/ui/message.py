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
import urllib.parse

from appy.px import Px

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Message:
    '''Manages the "message zone" allowing to display messages coming from the
       Appy server to the end user.'''

    @classmethod
    def consumeAll(class_, handler, unlessRedirect=False):
        '''Returns the list of messages to show to a web page'''
        # Do not consume anything if p_unlessRedirect is True and we are
        # redirecting the user.
        if unlessRedirect and ('Appy-Redirect' in handler.resp.headers): return
        # Try to get messages from the 'AppyMessage' cookie
        message = handler.req.AppyMessage
        if message:
            # Dismiss the cookie
            handler.resp.setCookie('AppyMessage', 'deleted')
            return urllib.parse.unquote(message)

    @classmethod
    def hasValidationErrors(class_, handler):
        '''Returns True if there are validaton errors collected by the
           (handler.)validator.'''
        return handler.validator and handler.validator.errors

    # The message zone
    px = Px('''
     <div var="validErrors=ui.Message.hasValidationErrors(handler)"
          class=":'message fadedOut' if popup else 'message fadedOut'"
          style=":'display:none' if not validErrors else 'display:block'"
          id="appyMessage" onmouseenter="stopFadeout(this)">
      <!-- The icon for closing the message -->
      <img src=":url('close.svg')" class="clickable iconS popupI"
           onclick="this.parentNode.style.display='none'" align=":dright"/>
      <!-- The message content -->
      <div id="appyMessageContent">:validErrors and _('validation_error')</div>
      <div if="validErrors"
           var2="validator=handler.validator">:handler.validator.pxErrors</div>
     </div>
     <script var="messages=ui.Message.consumeAll(handler)"
             if="messages">::'showAppyMessage(%s)' % q(messages)</script>''',

     css='''
      .message { position: fixed; max-height: 50vh; bottom: 30px; right: 0px;
                 background-color: |fillColor|; color: |brightColor|;
                 padding: 10px; z-index: 10; font-weight: bold }
      .messageP { width: 80%; top: 35% }

      @keyframes fade {
        0% { opacity: 0 }
        10% { opacity: 0.9 }
        80% { opacity: 0.6 }
        100% { opacity: 0; display: none; visibility: hidden }
      }
      .fadedOut { animation: fade 5s 1; animation-fill-mode: forwards }''',

     js='''
       function stopFadeout(div) {
         var classes = div.className.split(' '),
             x=classes.pop(),
             clone=div.cloneNode(true);
         // Creating a clone for the p_div will stop the animation
         clone.className = classes.join(' ');
         clone.onmouseenter = null;
         div.parentNode.replaceChild(clone, div);
       }'''
     )
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
