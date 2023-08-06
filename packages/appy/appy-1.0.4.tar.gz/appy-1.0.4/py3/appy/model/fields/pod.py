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
import time, os, os.path
from DateTime import DateTime

import appy
from appy.px import Px
from appy.utils import path as putils
from appy.pod.renderer import Renderer
from appy.model.searches import Search
from appy.utils import string as sutils
from appy.utils.string import Normalize
from appy.model.utils import Object as O
from appy.model.fields import Field, Show
from appy.ui.layout import Layouts, Layout
from appy.model.fields.file import FileInfo
from appy.pod import PodError, styles_manager

# Messages - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
POD_ERROR = 'An error occurred while generating the document. Please contact ' \
  'the system administrator.'
NO_TEMPLATE = 'Please specify a pod template in field "template".'
UNAUTHORIZED = 'You are not allowed to perform this action.'
TEMPLATE_NOT_FOUND = 'Template not found at %s.'
FREEZE_ERROR = 'Error while trying to freeze a "%s" file in pod field "%s" ' \
  '(%s).'
FREEZE_FATAL_ERROR = 'Server error. Please contact the administrator.'
RENDERING = "rendering pod %s :: %s (in %s)..."
RENDERED = "pod %s:%s (%s) rendered in %.2fsec."
MAIL_NO_RECIPIENT = 'mailing "%s" contains no recipient.'
MAIL_NO_USER = 'mailing "%s": inexistent user or no email for "%s".'
MAIL_NO_RECIPIENT_FINALLY = 'mailing "%s" contains no recipient (after ' \
  'removing wrong entries, see above).'
OVERWRITING = '%s: overwriting %s...'
FREEZING_ODT = 'freezing the ODT version...'
FREEZING_OVERWRITING = 'freeze: overwriting %s...'
FROZEN_OK = 'frozen at %s.'
UNFROZEN_OK = 'removed (unfrozen) %s.'
UPLOADED_OK = 'uploaded at %s.'

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Config:
    '''POD-specific configuration'''
    def __init__(self):
        # We suppose the Python interpreter running the Appy has library UNO
        # allowing to contact LibreOffice in server mode. If it is not the case,
        # specify here the absolute path to a UNO-compliant Python interpreter.
        self.unoEnabledPython = None
        # The port for contacting LibreOffice
        self.libreOfficePort = 2002

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Mailing:
    '''Represents a mailing list as can be used by a pod field (see below)'''
    def __init__(self, id, name=None, logins=None, subject=None, body=None):
        # The mailing list ID, an element among available mailings as defined in
        # Pod.mailing.
        self.id = id
        # The mailing list name, as shown in the user interface
        self.name = name
        # The list of logins that will be used as recipients for sending
        # emails.
        self.logins = logins
        # The mail subject
        self.subject = subject
        # The mail body
        self.body = body

    def complete(self, field, o, template, mailing, mailText, forUi):
        '''Complete the mailing information'''
        _ = o.translate
        # Guess the name from the ID if no name is defined
        self.name = self.name or sutils.produceNiceMessage(self.id)
        mapping = None
        # Compute the mail subject when absent
        if not self.subject:
            # Give a predefined subject
            mapping = {'site': o.siteUrl,
                       'title':  o.getValue('title', formatted='shown'),
                       'template': field.getTemplateName(o, template)}
            self.subject = _('podmail_subject', mapping=mapping)
        if forUi:
            self.subject = '<b>%s</b>: %s</br/>' % \
                           (_('email_subject'), self.subject)
        # Compute the mail body when absent
        self.body = self.body or mailText
        if not self.body:
            # Give a predefined body
            if not mapping: mapping = {'site': o.siteUrl}
            fmt = 'html' if forUi else 'text'
            self.body = _('podmail_body', mapping=mapping, format=fmt)

    def getConfirmLabel(self, _):
        '''We misuse the "confirm" popup to allow the user to modify the mail
           body in its "comment" field. We misuse this field's label to
           integrate the mail subject in it (so the user can see it). This
           method returns this "label".'''
        return '%s<br/><b>%s</b>' % (self.subject, _('email_body'))

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class ImageFinder:
    '''Used by the POD renderer (XHTML conversion) to retrieve paths to local
       images instead of performing HTTP GETs to the server running POD.'''

    def __init__(self, o):
        self.o = o
        self.siteUrl = o.siteUrl

    def find(self, url):
        '''If p_url is local to the site running this code, this method returns
           the absolute path to the file on disk. Else, it returns None, letting
           POD perform a HTTP GET request to the "external" web server.'''
        # Return None if the image is not local to this webserver
        base = self.siteUrl
        if not url.startswith(base): return
        # Get the image path on disk. We make the assumption that the file is
        # stored in a File field on some object, so URL is supposed to be of the
        # form
        #               <base>/<objectId>/<fieldName>/download
        o = info = None
        for part in url[len(base):].split('/'):
            # Ignore empty parts
            if not part: continue
            # Get the object on which the File field is defined
            if o is None:
                o = self.o.getObject(part)
                if o is None: return
                continue
            # Get the FileInfo instance on this object
            if info is None:
                info = getattr(o, part)
                if not info: return
                break
        # If we are here, we can determine the path to the file on disk
        return str(info.getFilePath(o))

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Pod(Field):
    '''A pod is a field allowing to produce a (PDF, ODT, Word, RTF...) document
       from data contained in Appy class and linked objects or anything you
       want to put in it. It is the way gen uses pod.'''

    # Some methods wil be traversable
    traverse = Field.traverse.copy()

    # Make some useful classes accessible here
    TableProperties = styles_manager.TableProperties
    BulletedProperties = styles_manager.BulletedProperties
    NumberedProperties = styles_manager.NumberedProperties

    # Default Pod config
    defaultConfig = Config()

    # Default output formats for POD templates, by template type
    allFormats = {'.odt': ('pdf', 'doc', 'docx', 'odt'),
                  '.ods': ('xls', 'xlsx', 'ods')}

    # Getting a pod value is something special: disable the standard Appy
    # machinery for this.
    customGetValue = True

    class Layouts(Layouts):
        '''Pod-specific layouts'''
        # Right-aligned layouts, convenient for pod fields exporting search
        # results or multi-template pod fields.
        r = Layouts(view=Layout('fl!', css_class='podTable')) # "r"ight
        rf= Layouts(view=Layout('f!', css_class='podTable')) # "r"ight, no label
        l = Layouts(view= Layout('fl;', css_class='podTable')) # "l"eft
        # "r"ight "m"ulti-template (where the global field label is not used)
        rm = Layouts(view=Layout('f!', css_class='podTable'))
        # Inline layout
        inline = Layouts(view=Layout('f', width=None, css_class='inline',
                         align=''))

    # Icon allowing to generate a given template in a given format
    pxIcon = Px('''
     <a var="fmtSuffix='●' if frozen else '';
             linkId=field.getLinkId(confirm, id, info, fmt);
             linkGetter='getNode(%s)' % q(linkId) if confirm else 'this';
             js='generatePod(%s,%s,%s,%s,%s,%s,null,%s)' % \
                 (linkGetter, q(o.url), q(name), q(info.template), q(fmt), \
                 q(tool.Search.encodeForReplay(req, layout)), gc)"
        onclick=":confirm and 'askConfirm(%s,%s,%s)' % (q('script'), \
                 q(js,False), field.labelId) or js"
        title=":field.getIconTitle(o, fmt, frozen)" class="clickable"
        style="position: relative" id=":linkId">
      <img src=":url('download.svg')" class="iconS"/>
      <span class="fmt">:fmt.upper() + fmtSuffix</span>
     </a>''')

    view = cell = Px('''
     <script if="field.confirm">::field.getJsConfirmVar(o)</script>
     <x var="id=o.iid;
             gc=field.getCheckHook(o, req);
             onCell=layout == 'cell'"
        for="info in field.getVisibleTemplates(o)"
        var2="mailings=field.getVisibleMailings(o, info.template);
              lineBreak=((loop.info.nb + 1) % field.maxPerRow) == 0;
              confirm=field.getConfirm(o, info.template)">
      <!-- Show the specific template name when relevant -->
      <span if="not onCell and field.useTemplateName"
            class="pod smaller">:field.getTemplateName(o, info.template)</span>
      <x for="fmt in info.formats"
         var2="freezeAllowed=(fmt in info.freezeFormats) and \
                             (field.show != 'result');
               hasMailings=mailings and (fmt in mailings);
               dropdownEnabled=freezeAllowed or hasMailings;
               frozen=fmt in info.frozenFormats">
       <!-- A clickable icon if no freeze action is allowed and no mailing is
            available for this format -->
       <x if="not dropdownEnabled">:field.pxIcon</x>
       <!-- A clickable icon and a dropdown menu else -->
       <span if="dropdownEnabled" class="dropdownMenu"
             onmouseover="toggleDropdown(this)"
             onmouseout="toggleDropdown(this,'none')">
        <x>:field.pxIcon</x>
        <!-- The dropdown menu containing freeze actions -->
        <table class="dropdown" width="110px">
         <!-- Unfreeze -->
         <tr if="freezeAllowed and frozen" valign="top">
          <td width="95px">
           <a onclick=":'freezePod(%s,%s,%s,%s,%s)' % (q(o.url), q(name), \
                        q(info.template), q(fmt), q('unfreeze'))"
              class="smaller">:_('unfreezeField')</a>
          </td>
          <td width="15px"><img src=":url('unfreeze')"/></td>
         </tr>
         <!-- (Re-)freeze -->
         <tr if="freezeAllowed" valign="top">
          <td width="85px">
           <a onclick=":'freezePod(%s,%s,%s,%s,%s)' % (q(o.url), q(name), \
                        q(info.template), q(fmt), q('freeze'))"
              class="smaller">:_('freezeField')</a>
          </td>
          <td width="15px"><img src=":url('freeze')"/></td>
         </tr>
         <!-- (Re-)upload -->
         <tr if="freezeAllowed" valign="top">
          <td width="85px">
           <a onclick=":'uploadPod(%s,%s,%s,%s)' % (q(o.url), q(name), \
                                   q(info.template), q(fmt))"
              class="smaller">:_('uploadField')</a>
          </td>
          <td width="15px"><img src=":url('upload')"/></td>
         </tr>
         <!-- Mailing lists -->
         <x if="hasMailings" var2="sendLabel=_('email_send')">
          <tr for="mailing in mailings[fmt]" valign="top"
              var2="mInfo=field.getMailingInfo(o, info.template, mailing,
                                               None, forUi=True)">
           <td colspan="2">
            <a var="js='generatePod(this,%s,%s,%s,%s,%s,null,%s,%s,comment)' % \
                        (q(id), q(name), q(info.template), q(fmt), \
                         q(tool.Search.encodeForReplay(req, layout)), gc, \
                         q(mailing))"
               onclick=":'askConfirm(%s,%s,null,true,400,%s,%s,6)' % \
                          (q('script'), q(js,False), \
                           q(mInfo.getConfirmLabel(_)), q(mInfo.body))"
               title=":sendLabel">
             <img src=":url('email')" align="left" style="margin-right: 2px"/>
             <x>:mInfo.name</x></a>
            </td>
          </tr>
         </x>
        </table>
       </span>
      </x>
      <br if="lineBreak"/>
     </x>''',

     css='''.phase .fmt { position: absolute; left: 27%; bottom: -80%;
                          font-size: 85% }
            .list .fmt { font-weight: normal; margin-right: -8px }
            @keyframes movedown {
              from { top: 0px  }
              50% { top: -5px }
              to { top: 0px }
            }
            .waiting { animation: movedown 0.7s ease infinite }''',

     js='''
      podDownloadStatus = function(node, data) {
        // Checks the status of cookie "podDownload"
        var status = readCookie('podDownload');
        if (status == 'False') return;
        // The download is complete. Stop the timeout.
        clearInterval(podTimeout);
        for (var key in data) node.setAttribute(key, data[key]);
      }

      // Manage query data, if the POD to produce is tied to a search
      manageQueryData = function(f, queryData, checkHook) {
        if (queryData) {
          /* If "queryData" specifies a custom search, get criteria from the
             browser's session storage. */
          var elems = queryData.split(':');
          if (elems[1] == 'customSearch') {
            f.criteria.value = sessionStorage.getItem(elems[0]);
          }
        }
        else if (checkHook) {
          /* If this hook refers to a Search within a Ref field, get search
             params and build query data from it. */
          var ssel = document.getElementById(checkHook + '_ssel');
          if (ssel && ssel.value) {
            // Get the search params corresponding to this search
            var p = document.getElementById('searchResults')['ajax'].params,
                data=[p['className'], p['search'], p['sortKey'], p['sortOrder'],
                      stringFromDict(p['filters'])].join(':');
            f.queryData.value = data;
          }
        }
      }

      // Generate a document from a POD template
      generatePod = function(node, url, fieldName, template, podFormat,
                       queryData, customParams, checkHook, mailing, mailText) {
        var f = document.getElementById('podForm');
        f.action = url + '/' + fieldName + '/generate';
        f.template.value = template;
        f.podFormat.value = podFormat;
        f.queryData.value = queryData;
        f.customParams.value = customParams || '';
        manageQueryData(f, queryData, checkHook);
        if (mailing) {
          f.mailing.value = mailing;
          if (mailText) f.mailText.value = mailText;
        }
        // Transmit value of cookie "showSubTitles"
        f.showSubTitles.value = readCookie('showSubTitles') || 'True';
        // Initialise the status of checkboxes
        setChecked(f, checkHook);
        // Disable the link to prevent double-clicks
        var data = {'class': node.className,
                    'onclick': node.attributes.onclick.value};
        node.setAttribute('onclick', '');
        node.className = 'waiting';
        // Set the pod download cookie. "False" means: not downloaded yet.
        createCookie('podDownload', 'False');
        // Set a timer that will check the cookie value
        podTimeout = window.setInterval(function(){
          podDownloadStatus(node, data)}, 700);
        f.submit();
      }

      // (Un-)freeze a document from a pod template
      freezePod = function(url, fieldName, template, podFormat, action) {
        var f = document.getElementById('podForm');
        f.action = url + '/' + fieldName + '/onFreeze';
        f.template.value = template;
        f.podFormat.value = podFormat;
        f.freezeAction.value = action;
        askConfirm('form', 'podForm', action_confirm);
      }

      // Upload a file for freezing it in a pod field
      uploadPod = function(url, fieldName, template, podFormat) {
        var f = document.getElementById('uploadForm');
        f.action = url + '/' + fieldName + '/upload';
        f.template.value = template;
        f.podFormat.value = podFormat;
        f.uploadedFile.value = null;
        openPopup('uploadPopup');
      }''')

    edit = search = ''

    def __init__(self, validator=None, show=Show.TR, page='main', group=None,
      layouts=None, move=0, readPermission='read', writePermission='write',
      width=None, height=None, maxChars=None, colspan=1, master=None,
      masterValue=None, focus=False, historized=False, mapping=None,
      generateLabel=None, label=None, template=None, templateName=None,
      useTemplateName=None, showTemplate=None, freezeTemplate=None,
      showFrozenOnly=True, maxPerRow=5, context=None, stylesMapping={},
      formats=None, getChecked=None, mailing=None, mailingName=None,
      showMailing=None, mailingInfo=None, view=None, cell=None, edit=None,
      xml=None, translations=None, downloadName=None,
      downloadDisposition='attachment', forceOoCall=False,
      optimalColumnWidths=False, distributeColumns=None, script=None,
      pdfOptions='ExportNotes=True', tabbedCR=False, fonts=None, confirm=False,
      raiseOnError=False, action=None, beforeAction=None):
        # Param "template" stores the path to the pod template(s). If there is
        # a single template, a string is expected. Else, a list or tuple of
        # strings is expected. Every such path must be relative to your
        # application. A pod template name Test.odt that is stored at the root
        # of your app will be referred as "Test.odt" in self.template. If it is
        # stored within sub-folder "pod", it will be referred as "pod/Test.odt".
        if not template: raise Exception(NO_TEMPLATE)
        if isinstance(template, str):
            self.template = [template]
        elif isinstance(template, tuple):
            self.template = list(template)
        else:
            self.template = template
        # Param "templateName", if specified, is a method that will be called
        # with the current template (from self.template) as single arg and must
        # return the name of this template. If self.template stores a single
        # template, you have no need to use param "templateName" (excepted if
        # you want to render the POD with a name, in the layout "buttons").
        # In most cases, if you have a single template, simply use the field
        # label to name the template. If you have a multi-pod field (with
        # several templates specified as a list or tuple in param "template"),
        # you will probably choose to hide the field label and use param
        # "templateName" to give a specific name to every template. If
        # "template" contains several templates and "templateName" is None, Appy
        # will produce names from template filenames.
        self.templateName = templateName
        # If you want to use "templateName" hereabove even if self.template
        # contains a single template, set "useTemplateName" to True.
        if useTemplateName is None:
            self.useTemplateName = len(self.template) > 1
        else:
            self.useTemplateName = useTemplateName
        # "showTemplate" determines if the current user may generate documents
        # based on this pod field. More precisely, "showTemplate", if specified,
        # must be a method that will be called with the current template as
        # single arg (one among self.template) and that must return the list or
        # tuple of formats that the current user may use as output formats for
        # generating a document. If the current user is not allowed at all to
        # generate documents based on the current template, "showTemplate" must
        # return an empty tuple/list. If "showTemplate" is not specified, the
        # user will be able to generate documents based on the current template,
        # in any format from self.formats (see below).
        # "showTemplate" comes in addition to self.show. self.show dictates the
        # visibility of the whole field (ie, all templates from self.template)
        # while "showTemplate" dictates the visiblity of a specific template
        # within self.template.
        self.showTemplate = showTemplate
        # "freezeTemplate" determines if the current user may freeze documents
        # normally generated dynamically from this pod field. More precisely,
        # "freezeTemplate", if specified, must be a method that will be called
        # with the current template as single arg and must return the (possibly
        # empty) list or tuple of formats the current user may freeze. The
        # "freezing-related actions" that are granted by "freezeTemplate" are
        # the following. When no document is frozen yet for a given
        # template/format, the user may:
        # - freeze the document: pod will be called to produce a document from
        #   the current database content and will store it in the database.
        #   Subsequent user requests for this pod field will return the frozen
        #   doc instead of generating on-the-fly documents;
        # - upload a document: the user will be able to upload a document that
        #   will be stored in the database. Subsequent user requests for this
        #   pod field will return this doc instead of generating on-the-fly
        #   documents.
        # When a document is already frozen or uploaded for a given
        # template/format, the user may:
        # - unfreeze the document: the frozen or uploaded document will be
        #   deleted from the database and subsequent user requests for the pod
        #   field will again generate on-the-fly documents;
        # - re-freeze the document: the frozen or uploaded document will be
        #   deleted, a new document will be generated from the current database
        #   content and will be frozen as a replacement to the deleted one;
        # - upload a document: the frozen or uploaded document will be replaced
        #   by a new document uploaded by the current user.
        self.freezeTemplate = freezeTemplate
        # If "showFrozenOnly" is True, only formats for which a frozen document
        # exists will be available to the user. This mechanism is used to
        # prevent data from being frozen in one format and being available for
        # real-time computation in another format, which could be incoherent.
        # Note that is has sense (and thus applies) only when there is at least
        # one frozen document. When "showFrozenOnly" is applied, and when there
        # is at least one frozen document, it overrides the list of available
        # formats (as determined by self.showTemplate or self.formats).
        self.showFrozenOnly = showFrozenOnly
        # If p_template contains more than 1 template, "maxPerRow" tells how
        # much templates must appear side by side.
        self.maxPerRow = maxPerRow
        # The context is a dict containing a specific pod context, or a method
        # that returns such a dict.
        self.context = context
        # A global styles mapping that would apply to the whole template(s)
        self.stylesMapping = stylesMapping
        # What are the output formats when generating documents from this pod ?
        self.formats = formats or self.getAllFormats(self.template[0])
        # Parameter "getChecked" can specify the name of a Ref field belonging
        # to the same Appy class, or the term "search". If getChecked is...
        # ----------------------------------------------------------------------
        # the name of | The context of the pod template will contain an
        # a Ref field | additional object, named "_checked". On this object, an
        #             | attribute will be set, whose name is the name of the Ref
        #             | field, and whose value will be the list of the objects
        #             | linked via the Ref field that are currently selected in
        #             | the user interface.
        # ----------------------------------------------------------------------
        #   "search"  | The pod context variable "objects", normally containing
        #             | all search results, will only contain objects being
        #             | checked in the user interface.
        # ----------------------------------------------------------------------
        self.getChecked = getChecked
        # Mailing lists can be defined for this pod field. For every visible
        # mailing list, a menu item will be available in the user interface and
        # will allow to send the pod result as attachment to the mailing list
        # recipients. Attribute p_mailing stores a mailing list's id
        # (as a string) or a list of ids.
        self.mailing = mailing
        if isinstance(mailing, str):
            self.mailing = [mailing]
        elif isinstance(mailing, tuple):
            self.mailing = list(mailing)
        # "showMailing" below determines when the mailing list(s) must be shown.
        # It may store a method accepting a mailing list's id (among
        # self.mailing) and a template (among self.template) and returning the
        # list or tuple of formats for which the pod result can be sent to the
        # mailing list. If no such method is defined, the mailing list will be
        # available for all visible templates and formats.
        self.showMailing = showMailing
        # When it it time to send an email (or preview it), "mailingInfo" gives
        # all the necessary information for this email: recipients, subject
        # body. It must be a method accepting 2 args:
        # - "mailing" is the mailing ID (from self.mailing);
        # - "forUi" is a boolean indicating if we must compute mailing info for
        #           displaying it in the user interface (forUi=True) or for
        #           sending the mail (forUi=False). It is important because, if
        #           True (False), you must translate i18n labels with parameter
        #           format="html" (format="text").
        # Displaying info in the user interface allows the user to preview the
        # mail and modify the predefined mail body if necessary. The method must
        # return a Mailing instance (see class hereabove). Note that the
        # returned Mailing instance can be subsequently modified by the
        # framework.
        self.mailingInfo = mailingInfo
        # "downloadName", if specified, is a method that will be called with
        # the current template (from self.template) as single arg and must
        # return the name of the file as the user will get it once he will
        # download the pod result from its browser. This is for people that do
        # not like the default download name. Do not specify any extension: it
        # will be appended automatically. For example, if your method returns
        # "PodResultForSomeObject", and the pod result is a pdf file, the file
        # will be named "PodResultForSomeObject.pdf". If you specify such a
        # method, you have the responsibility to produce a valid,
        # any-OS-and-any-browser-proof file name. For inspiration, see the
        # default m_getDownloadName method hereafter. If you have several
        # templates in self.template, for some of them where you are satisfied
        # with the default download name, return None.
        self.downloadName = downloadName
        # The field below allow to determine the "disposition" when downloading
        # a pod result. "attachment" by default, it can be set to "inline". But
        # with disposition=inline, Google Chrome and IE may launch a PDF viewer
        # that triggers one or many additional crashing HTTP GET requests.
        self.downloadDisposition = downloadDisposition
        # Normally, when you generate a pod result that is in ODT/ODS format,
        # LibreOffice is not called. But if you want it to be called
        # nevertheless, for example to ensure that all the indexes are
        # up-to-date (including the table of contents), set "forceOoCall" to
        # True. When generating pod results in other formats (pdf, doc, xls...),
        # LibreOffice is always called and indexes are always refreshed.
        self.forceOoCall = forceOoCall
        # For these parameters, see appy.pod.renderer.Renderer's docstring
        self.optimalColumnWidths = optimalColumnWidths
        self.distributeColumns = distributeColumns
        # "script" can be used to customize the process of rendering the POD
        # result via LibreOffice UNO. See option "-s" of appy/pod/converter.py
        # for more information. "script" can hold the absolute path to a Python
        # file or a method that returns it. If you specify a method, it will
        # accept 2 parameters:
        # * template     the name of the current template (important when
        #                multiple templates are in use);
        # * context      the context given to the pod template.
        self.script = script
        # When the result is PDF, options for configuring the production of the
        # PDF file can be given in this attribute (ie, for adding a watermark).
        # More information about available options on class
        # appy.pod.renderer.Renderer, which has an homonym attribute.
        # "pdfOptions" can hold a method as well.
        self.pdfOptions = pdfOptions
        # "tabbedCR" determines how the "carriage return" char is rendered on
        # POD results. See appy.pod.renderer.py for more information.
        self.tabbedCR = tabbedCR
        # The name of the font passed in "fonts" will be injected in all styles
        # from the POD template. It must return a string or be a function that
        # will accept the current template (one among self.template) as unique
        # arg and return the name of the font to inject in it.
        self.fonts = fonts
        # If "confirm" is True, a popup will be shown before generating the
        # pod result. "confirm" may also hold a method, that must accept, as
        # single arg, the name of the current template (indeed, self.template
        # may hold several templates), and must return a boolean value.
        self.confirm = confirm
        # If "raiseOnError" is False (the default), no error is raised:
        # traceback(s) is (are) dumped into the pod result within note(s). If
        # you prefer a real exception to be raised, set this parameter to True.
        # This could be important if, for example, an action is tied to this pod
        # field: you want it to be completely executed or rolled back.
        self.raiseOnError = raiseOnError
        # If you want some action to be executed after the pod result has been
        # generated, set a method in parameter "action". This must be a method
        # accepting parameters:
        # * template     the name of the current template (important when
        #                multiple templates are in use);
        # * context      the context given to the pod template;
        # * format       the output format.
        self.action = action
        # If you want some action to be executed just before the pod result is
        # generated, set a method in parameter "beforeAction". This method's
        # signature must be the same as for parameter "action" hereabove.
        self.beforeAction = beforeAction
        # Call the base constructor
        Field.__init__(self, None, (0,1), None, None, show, page, group,
          layouts, move, False, True, None, None, False, None, readPermission,
          writePermission, width, height, None, colspan, master, masterValue,
          focus, historized, mapping, generateLabel, label, None, None, None,
          None, False, False, view, cell, edit, xml, translations)
        # Param "persist" is False, but actual persistence for this field is
        # determined by freezing.
        self.validable = False

    def getExtension(self, template):
        '''Gets a p_template's extension (".odt" or ".ods"). Because a template
           can simply be a pointer to another template (ie, "Item.odt.variant"),
           the logic for getting the extension is a bit more tricky.'''
        elems = os.path.splitext(template)
        if elems[1] in Pod.allFormats: return elems[1]
        # p_template must be a pointer to another template and has one more
        # extension.
        return os.path.splitext(elems[0])[1]

    def getAllFormats(self, template):
        '''Gets all the output formats that are available for a given
           p_template.'''
        return Pod.allFormats[self.getExtension(template)]

    def isRenderable(self, layout):
        '''A single-template POD is renderable on layout "buttons"'''
        return True if layout != 'buttons' else len(self.template) == 1

    def setTemplateFolder(self, folder):
        '''This methods adds a prefix to every template name in self.template'''
        # This can be useful if a plug-in module needs to replace an application
        # template by its own templates. Here is an example: imagine a base
        # application has a pod field with:

        # self.templates = ["Item.odt", "Decision.odt"]

        # The plug-in module, named "PlugInApp", wants to replace it with its
        # own templates Item.odt, Decision.odt and Other.odt, stored in its sub-
        # folder "pod". Suppose the base pod field is in <podField>. The plug-in
        # will write:

        # <podField>.templates = ["Item.odt", "Decision.odt", "Other.odt"]
        # <podField>.setTemplateFolder('../PlugInApp/pod')

        # The following code is equivalent, will work, but is precisely the kind
        # of things we want to avoid.

        # <podField>.templates = ["../PlugInApp/pod/Item.odt",
        #                           "../PlugInApp/pod/Decision.odt",
        #                           "../PlugInApp/pod/Other.odt"]
        for i in range(len(self.template)):
            self.template[i] = os.path.join(folder, self.template[i])

    def getTemplateName(self, o, fileName):
        '''Gets the name of a template given its p_fileName'''
        r = None
        if self.templateName:
            # Use the method specified in self.templateName
            r = self.templateName(o, fileName)
        # Else, deduce a nice name from p_fileName
        if not r:
            name = os.path.splitext(os.path.basename(fileName))[0]
            r = sutils.produceNiceMessage(name)
        return r

    def getTemplatePath(self, diskFolder, template):
        '''Return the absolute path to some pod p_template, by prefixing it with
           the application path. p_template can be a pointer to another
           template.'''
        # Compute the base path
        if template.startswith('/'):
            # An absolute path: search for it in Appy itself
            baseFolder = os.path.dirname(appy.__file__)
            template = template[1:]
        else:
            baseFolder = diskFolder
        # Compute the absolute path
        r = putils.resolvePath(os.path.join(baseFolder, template))
        if not os.path.isfile(r):
            raise Exception(TEMPLATE_NOT_FOUND % template)
        # Unwrap the path if the file is simply a pointer to another one
        elems = os.path.splitext(r)
        if elems[1] not in Pod.allFormats:
            r = elems[0]
        return r

    def getDownloadName(self, o, template, format=None, queryRelated=False,
                        bypassMethod=False):
        '''Gets the name of the pod result as will be seen by the user that will
           download it. Ensure the returned name is not too long for the OS that
           will store the downloaded file with this name.'''
        # Use method self.downloadName if present and if it returns something
        # for p_template.
        if not bypassMethod and self.downloadName:
            name = self.downloadName(o, template)
            if name: return '%s.%s' % (name, format) if format else name
        # Compute the default download name
        fileName = Normalize.fileName(self.getTemplateName(o, template))[:40]
        if not queryRelated:
            # This is a POD for a single object: personalize the file name with
            # the object title.
            title = o.getShownValue('title')
            fileName = '%s-%s' % (Normalize.fileName(title)[:40], fileName)
        return '%s.%s' % (fileName, format) if format else fileName

    def getVisibleTemplates(self, o):
        '''Returns, among self.template, the template(s) that can be shown'''
        r = []
        if not self.showTemplate:
            # Show them all in the formats specified in self.formats
            for template in self.template:
                r.append(O(template=template, formats=self.formats,
                           freezeFormats=self.getFreezeFormats(o, template)))
        else:
            for template in self.template:
                formats = self.showTemplate(o, template)
                if not formats: continue
                elif isinstance(formats, bool):
                    formats = self.getAllFormats(template)
                elif isinstance(formats, str):
                    formats = (formats,)
                r.append(O(template=template, formats=formats,
                           freezeFormats=self.getFreezeFormats(o, template)))
        # Compute the already frozen documents, and update the available formats
        # accordingly when self.showFrozenOnly is True.
        for info in r:
            frozenFormats = []
            for fmt in info.formats:
                if self.isFrozen(o, info.template, fmt):
                    frozenFormats.append(fmt)
            info.frozenFormats = frozenFormats
            # Replace formats with frozenFormats when relevant
            if frozenFormats and self.showFrozenOnly:
                info.formats = frozenFormats
        return r

    def getVisibleMailings(self, o, template):
        '''Gets, among self.mailing, the mailing(s) that can be shown for
           p_template, as a dict ~{s_format:[s_id]}~.'''
        if not self.mailing: return
        r = {}
        for mailing in self.mailing:
            # Is this mailing visible ? In which format(s) ?
            if not self.showMailing:
                # By default, the mailing is available in any format
                formats = True
            else:
                formats = self.showMailing(o, mailing, template)
            if not formats: continue
            if isinstance(formats, bool): formats = self.getAllFormats(template)
            elif isinstance(formats, str): formats = (formats,)
            # Add this mailing to the result
            for fmt in formats:
                if fmt in r: r[fmt].append(mailing)
                else: r[fmt] = [mailing]
        return r

    def getConfirm(self, o, template):
        '''When producing a result from p_template for p_obj, must we ask a
           confirmation to the user ?'''
        confirm = self.confirm
        return confirm(o, template) if callable(confirm) else confirm

    def getCheckHook(self, o, req):
        '''If p_self.getChecked is in use, return the ID of the DOM node
           containing the list of (un)checked objects.'''
        gc = self.getChecked
        if not gc:
            r = 'null'
        elif gc == 'search':
            r = req.search
            r = '"%s"' % r if r else 'null'
        else:
            if o.allows(o.getField(gc).readPermission):
                r = '"%d_%s"' % (o.iid, gc)
            else:
                r = 'null'
        return r

    def getLinkId(self, confirm, objectId, info, fmt):
        '''Returns an identifier for a link allowing to trigger a pod. This
           identifier is long and is not needed when p_confirm is False.'''
        if not confirm: return ''
        return '%s_%s_%s_%s' % (objectId, self.name,
                                Normalize.fileName(info.template), fmt)

    def getMailingInfo(self, o, template, mailing, mailText, forUi=False):
        '''Gets the necessary information for sending an email to p_mailing
           list, or for getting this info for displaying it in the user
           interface if p_forUi is True.'''
        r = self.mailingInfo(o, mailing, forUi)
        r.complete(self, o, template, mailing, mailText, forUi)
        return r

    def sendMailing(self, o, template, mailing, mailText, attachment):
        '''Sends the emails for m_mailing'''
        info = self.getMailingInfo(o, template, mailing, mailText)
        if not info.logins:
            o.log(MAIL_NO_RECIPIENT % mailing)
            return 'action_ko'
        # Collect logins corresponding to inexistent users and recipients
        missing = []
        recipients = []
        for login in info.logins:
            user = o.search1('User', secure=False, login=login)
            if not user:
                missing.append(login)
                continue
            else:
                recipient = user.getMailRecipient()
                if not recipient:
                    missing.append(login)
                else:
                    recipients.append(recipient)
        if missing:
            o.log(MAIL_NO_USER % (mailing, str(missing)))
        if not recipients:
            o.log(MAIL_NO_RECIPIENT_FINALLY % mailing)
            msg = 'action_ko'
        else:
            o.tool.sendMail(recipients, info.subject, info.body, [attachment])
            msg = 'action_done'
        return msg

    def getValue(self, o, name=None, layout=None, template=None, format=None,
                 result=None, queryData=None, computeCustomContext=None,
                 secure=True, executeAction=True):
        '''For a pod field, getting its value means computing a pod document or
           returning a frozen one.'''
        # A pod field differs from other field types because there can be
        # several ways to produce the field value (ie: self.template can hold
        # various templates; output file format can be odt, pdf,.... We get
        # those precisions about the way to produce the file, either from
        # params, or from default values.
        # * p_template is the specific template, among self.template, that must
        #   be used as base for generating the document;
        # * p_format is the output format of the resulting document;
        # * p_result, if given, must be the absolute path of the document that
        #   will be computed by pod. If not given, pod will produce a doc in the
        #   OS temp folder;
        # * if the pod document is related to a query, the query parameters
        #   needed to re-trigger the query are given in p_queryData, and, if it
        #   is a custom search, criteria are in the request, at key "criteria";
        # * if p_computeCustomContext is True, this special context will be
        #   computed (see m_setCustomContext) and will override any other value
        #   available in the context, including values from the field-specific
        #   context.
        start = time.time()
        template = template or self.template[0]
        format = format or 'pdf'
        # Security check
        if secure and not queryData:
            if self.showTemplate and not self.showTemplate(o, template):
                raise Exception(UNAUTHORIZED)
        # Return the possibly frozen document (not applicable for query-related
        # pods).
        if not queryData:
            frozen = self.isFrozen(o, template, format)
            if frozen:
                fileName = self.getDownloadName(o, template, format)
                return FileInfo(frozen, inDb=False, uploadName=fileName)
        # We must call pod to compute a pod document from "template"
        appPath = o.appPath
        # Get the path to the pod template
        templatePath = self.getTemplatePath(str(appPath), template)
        # Get or compute the specific POD context
        specificContext = self.getAttribute(o, 'context')
        # Compute the name of the result file
        if not result:
            result = '%s/%d_%f.%s' % (putils.getOsTempFolder(), o.iid,
                                      time.time(), format)
        # Define parameters to give to the appy.pod renderer
        req = o.req
        tool = o.tool
        podContext = {'tool': tool, 'user': o.user, 'self': o, 'field': self,
                      'now': DateTime(), '_': o.translate, 'appPath': appPath,
                      'template': template, 'req': req, 'config': tool.config}
        # If the pod document is related to a search, replay it and put the
        # result in the pod context.
        if queryData:
            podContext['objects'] = Search.replay(tool, queryData)
            podContext['queryData'] = queryData.split(':')
            podContext['_ref'] = Search.getRefInfo(tool, nameOnly=False)
        # Add the field-specific context if present
        if specificContext: podContext.update(specificContext)
        # Add the custom context when required
        if computeCustomContext:
            self.setCustomContext(podContext, o, req, queryData)
        # Variable "_checked" can be expected by a template but absent (ie,
        # when generating frozen documents).
        if '_checked' not in podContext: podContext['_checked'] = O()
        # Define a potential global styles mapping
        smap = self.stylesMapping
        smap = self.callMethod(o, smap) if callable(smap) else smap
        # Execute the "before" action when relevant
        if executeAction and self.beforeAction:
            self.beforeAction(o, template, podContext, format)
        # Get the optional script to give to the renderer
        script = self.script
        script = script(o, template, podContext) if callable(script) else script
        # Compute PDF options
        options = self.pdfOptions
        options = options(o, template) if callable(options) else options
        # Compute fonts
        fonts = self.fonts
        fonts = fonts(o, template) if callable(fonts) else fonts
        # Compute the renderer's parameters
        rendererParams = {'template': templatePath, 'context': podContext,
          'result': result, 'stylesMapping': smap, 'overwriteExisting': True,
          'forceOoCall': self.forceOoCall, 'raiseOnError': self.raiseOnError,
          'script': script, 'optimalColumnWidths': self.optimalColumnWidths,
          'distributeColumns': self.distributeColumns, 'pdfOptions': options,
          'tabbedCR': self.tabbedCR, 'fonts': fonts,
          'findImage': ImageFinder(o).find}
        config = o.config.pod or Pod.defaultConfig
        if config.unoEnabledPython:
            rendererParams['pythonWithUnoPath'] = config.unoEnabledPython
        if config.libreOfficePort:
            rendererParams['ooPort'] = config.libreOfficePort
        # Launch the renderer
        o.log(RENDERING % (o.id, template, format))
        try:
            renderer = Renderer(**rendererParams)
            renderer.run()
        except PodError as pe:
            if not os.path.exists(result):
                # In some (most?) cases, when OO returns an error, the result is
                # nevertheless generated.
                o.log(str(pe).strip(), type='error')
                return POD_ERROR
        # Give a friendly name for this file
        fileName = self.getDownloadName(o, template, format, queryData)
        # Execute the tied action when relevant
        if executeAction and self.action:
            self.action(o, template, podContext, format)
        # Log the successfull rendering
        o.log(RENDERED % (o.id, self.name, fileName, time.time()-start))
        # Get a FileInfo instance to manipulate the file on the filesystem
        return FileInfo(result, inDb=False, uploadName=fileName)

    def getBaseName(self, template=None):
        '''Gets the "base name" of p_template (or self.template[0] if not
           given). The base name is the name of the template, without path
           and extension. Moreover, if the template is a pointer to another one
           (ie Item.odt.something), the base name integrates the specific
           extension. In the example, the base name will be "ItemSomething".'''
        template = template or self.template[0]
        elems = os.path.splitext(os.path.basename(template))
        if elems[1] in ('.odt', '.ods'):
            r = elems[0] # Item.odt > Item
        else:
            # Item.odt.something > ItemSomething
            r = os.path.splitext(elems[0])[0] + elems[1][1:].capitalize()
        return r

    def getFreezeName(self, template=None, format='pdf', sep='.'):
        '''Gets the name on disk on the frozen document corresponding to this
           pod field, p_template and p_format.'''
        return '%s_%s%s%s' % (self.name,self.getBaseName(template),sep,format)

    def isFrozen(self, o, template=None, format='pdf'):
        '''Is there a frozen document for thid pod field, on p_o, for p_template
           in p_format? If yes, it returns the absolute path to the frozen
           doc.'''
        template = template or self.template[0]
        folder = o.getFolder()
        fileName = self.getFreezeName(template, format)
        r = folder / fileName
        if r.is_file(): return str(r)

    def freeze(self, o, template=None, format='pdf', secure=False, upload=None,
               freezeOdtOnError=True):
        '''Freezes, on p_o, a document for this pod field, for p_template in
           p_format'''
        # If p_secure is False, the security check, based on
        # self.freezeTemplate, is bypassed. If no p_upload file is specified, we
        # re-compute a pod document on-the-fly and we freeze this document.
        # Else, we store the uploaded file.

        # If p_freezeOdtOnError is True and format is not "odt" (has only sense
        # when no p_upload file is specified), if the freezing fails we try to
        # freeze the odt version, which is more robust because it does not
        # require calling LibreOffice.

        # Security check
        if secure and (format not in self.getFreezeFormats(o, template)):
            raise Exception(UNAUTHORIZED)
        # Compute the absolute path where to store the frozen document in the
        # database.
        folder = o.getFolder(create=True)
        fileName = self.getFreezeName(template, format)
        result = folder / fileName
        if result.is_file():
            prefix = 'freeze (upload)' if upload else 'freeze'
            o.log(OVERWRITING % (prefix, result))
            result.unlink()
        if not upload:
            # Generate the document
            doc = self.getValue(o, template=template, format=format,
                                result=str(result))
            if isinstance(doc, str):
                # An error occurred, the document was not generated
                o.log(FREEZE_ERROR % (format, self.name, doc), type='error')
                if not freezeOdtOnError or (format == 'odt'):
                    raise Exception(FREEZE_FATAL_ERROR)
                o.log(FREEZING_ODT)
                # Freeze the ODT version of the document, which does not require
                # to call LibreOffice: the risk of error is smaller.
                fileName = self.getFreezeName(template, 'odt')
                result = folder / fileName
                if result.is_file():
                    o.log(FREEZING_OVERWRITING % result)
                doc = self.getValue(o, template=template, format='odt',
                                    result=result)
                if isinstance(doc, str):
                    self.log(FREEZE_ERROR % ('odt', self.name, doc),
                             type='error')
                    raise Exception(FREEZE_FATAL_ERROR)
                o.log(FROZEN_OK % result)
        else:
            # Store the uploaded file in the database
            result = str(result)
            f = open(result, 'wb')
            doc = FileInfo(result, inDb=False)
            doc.replicateFile(upload.value, f)
            f.close()
            o.log(UPLOADED_OK % result)
        return doc

    def unfreeze(self, o, template=None, format='pdf', secure=False):
        '''Unfreezes, on p_o, the document for this pod field, for p_template
           in p_format.'''
        # Security check
        if secure and (format not in self.getFreezeFormats(o, template)):
            raise Exception(UNAUTHORIZED)
        # Compute the absolute path to the frozen doc
        folder = o.getFolder()
        fileName = self.getFreezeName(template, format)
        frozen = folder / fileName
        if frozen.is_file():
            frozen.unlink()
            putils.FolderDeleter.deleteEmpty(str(folder))
            o.log(UNFROZEN_OK % str(frozen))

    def getFreezeFormats(self, o, template=None):
        '''What are the formats into which the current user may freeze
           p_template?'''
        # One may have the right to edit the field to freeze anything in it
        if not o.allows(self.writePermission): return ()
        template = template or self.template[0]
        # Users (managers included) can perform freeze actions depending on
        # self.freezeTemplate.
        if not self.freezeTemplate: return ()
        r = self.freezeTemplate(o, template)
        if not r:
            return () # Ensure the result is a tuple
        elif r == True:
            return self.getAllFormats(template)
        else:
            return r

    def getIconTitle(self, o, format, frozen):
        '''Get the title of the format icon'''
        r = o.translate(format)
        if frozen:
            r += ' (%s)' % r.translate('frozen')
        return r

    def setCustomContext(self, context, o, req, queryData):
        '''Before calling pod to compute a result, if specific elements must be
           added to the p_context, compute it here. This request-dependent
           method is not called when computing a pod field for freezing it into
           the database.'''
        # Get potential custom params from the request. Custom params must be
        # coded as a string containing a valid Python dict.
        params = req.customParams
        if params:
            context.update(eval(params))
        # Compute the checked objects when relevant
        gc = self.getChecked
        if not gc: return
        # Manage a Ref field
        print('GC is', gc)
        print('Query data is', queryData)
        if gc == 'search':
            # Manage a search. All search results are in p_context['objects'].
            Search.keepCheckedResults(req, context['objects'])
        else:
            # Manage a Ref field
            if queryData:
                # We are in the presence of results from one of the searches
                # defined in Ref.searches. Search results are already in
                # p_context['objects'].
                Search.keepCheckedResults(req, context['objects'])
                objects = context['objects']
            else:
                # The IDs of the tied objects are specified in the request
                ids, unchecked = Search.getCheckedInfo(req)
                objects = []
                tool = o.tool
                for tied in getattr(o, gc):
                    if unchecked: condition = tied.iid not in ids
                    else:         condition = tied.iid in ids
                    if condition and tied.allows('read'):
                        objects.append(tied)
            context['_checked'] = O()
            setattr(context['_checked'], gc, objects)

    def setRequestValue(self, o):
        '''For a Pod field there is not possibility to carry its value in the
           request.'''

    def resetPodCookie(self, o):
        '''Reset the "pod download" cookie indicating that the pod download as
           ended (successfully or not).'''
        o.resp.setCookie('podDownload', 'True')

    def getJsConfirmVar(self, o):
        '''Gets the Javascript variable definition for storing the specific
           confirmation message to show when self.confirm is not False.'''
        prefix = self.labelId
        return 'var %s = "%s";' % (prefix, o.translate('%s_confirm' % prefix))

    traverse['generate'] = 'perm:read'
    def generate(self, o):
        '''Called from the ui for generating a POD result'''
        req = o.req
        template = req.template
        format = req.podFormat
        mailing = req.mailing
        # Generate a (or get a frozen) document
        r = self.getValue(o, template=template, format=format,
                          queryData=req.queryData, computeCustomContext=True)
        if isinstance(r, str):
            # An error has occurred, and "r" contains the error message
            if not mailing: self.resetPodCookie(o)
            return o.goto(o.referer, message=r)
        # "r" contains a FileInfo instance.
        # Return the result to the ui or send a mail with it as attachment ?
        if not mailing:
            self.resetPodCookie(o)
            disposition = self.downloadDisposition
            r.writeResponse(o.H(), disposition=disposition, cache=False)
        else:
            # Send the email(s)
            msg = self.sendMailing(o, template, mailing, req.mailText, r)
            return o.goto(o.referer, message=o.translate(msg))

    traverse['onFreeze'] = 'perm:write'
    def onFreeze(self, o):
        '''UI request to (un)freeze a file for this POD field'''
        req = o.req
        action = req.freezeAction
        if action == 'freeze':
            self.freeze(o, req.template, req.podFormat, secure=True,
                        freezeOdtOnError=False)
        elif action == 'unfreeze':
            self.unfreeze(o, req.template, req.podFormat, secure=True)
        return o.goto(o.referer, message=o.translate('action_done'))

    traverse['upload'] = 'perm:write'
    def upload(self, o):
        '''UI request to upload a file for (re)placing the frozen version of
           this POD field.'''
        # Ensure a file from the correct type has been uploaded
        req = o.req
        format = req.podFormat
        upload = req.uploadedFile
        if not upload or not upload.name.endswith('.%s' % format):
            # A wrong file has been uploaded (or no file at all)
            msg = 'upload_invalid'
        else:
            # Store the uploaded file in the database
            self.freeze(o, req.template, format, secure=True, upload=upload)
            msg = 'action_done'
        return o.goto(o.referer, message=o.translate(msg))
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
