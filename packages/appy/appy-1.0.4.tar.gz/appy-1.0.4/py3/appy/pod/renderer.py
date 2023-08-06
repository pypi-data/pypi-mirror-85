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
from pathlib import Path
from collections import UserDict
import zipfile, shutil, xml.sax, os, os.path, re, mimetypes, time

import appy.pod
from appy import utils
from appy.xml import Tag
from appy.pod import PodError
from appy.utils.zip import unzip, zip
from appy.pod.buffers import FileBuffer
from appy.utils.path import FolderDeleter
from appy.pod.converter import FILE_TYPES
from appy.pod import styles_manager as sm
from appy.pod import doc_importers as importers
from appy.pod.xhtml2odt import Xhtml2OdtConverter
from appy.pod.pod_parser import PodParser, PodEnvironment, OdInsert

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
BAD_CTX     = 'Context must be either a dict, a UserDict or an instance.'
RES_FOLDER  = 'Result file "%s" is a folder, please remove this.'
RES_EXISTS  = 'Result file "%s" exists.'
TEMP_W_KO   = 'I cannot create temp folder "%s". %s'
NO_PY_PATH  = 'Extension of result file is "%s". In order to perform ' \
              'conversion from ODT to this format we need to call ' \
              'LibreOffice. But the Python interpreter which runs the ' \
              'current script does not know UNO, the library that allows to ' \
              'connect to LibreOffice in server mode. If you can\'t install ' \
              'UNO in this Python interpreter, you can specify, in parameter ' \
              '"pythonWithUnoPath", the path to a UNO-enabled Python ' \
              'interpreter. One such interpreter may be found in ' \
              '<libreoffice_path>/program.'
PY_PATH_KO  = '"%s" is not a file. You must here specify the absolute ' \
              'path of a Python interpreter (.../python, .../python.sh, ' \
              '.../python.exe, .../python.bat...).'
R_TYPE_KO   = 'Result "%s" has a wrong extension. Allowed extensions are: "%s".'
CONV_ERROR  = 'An error occurred during the conversion. %s'
BAD_OO_PORT = 'Bad LibreOffice port "%s". Make sure it is an integer.'
XHTML_ERROR = 'An error occurred while rendering XHTML content.'
WARN_OD_KO  = 'Warning: your OpenDocument file may not be complete (ie ' \
              'imported documents may not be present). This is because we ' \
              'could not connect to LibreOffice in server mode: %s'
DOC_KO      = 'Please specify a document to import, either with a stream ' \
              '(parameter "content") or with a path (parameter "at").'
DOC_FMT_KO  = 'POD was unable to deduce the document format. Please specify ' \
              'it through parameter named "format" (=odt, gif, png, ...).'
DOC_FMT_NS  = 'Format "%s" is not supported.'
WARN_FIN_KO = 'Warning: error while calling finalize function. %s'

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Default styles added by POD in content.xml and styles.xml
POD_STYLES = {}
podFolder = os.path.dirname(appy.pod.__file__)
for name in ('content', 'styles'):
    f = open('%s/%s.xmlt' % (podFolder, name))
    POD_STYLES[name] = f.read()
    f.close()

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class CsvOptions:
    '''When the POD result is of type CSV, use this class to define CSV
       options.'''

    # Available encodings for CSV output files
    encodings = {'utf-8': 76, 'latin-1': 12}

    def __init__(self, fieldSeparator=';', textDelimiter='"', encoding='utf-8'):
        # The delimiter used between every field on a single line
        self.fieldSeparator = fieldSeparator
        # The character used to "wrap" every value. Can be the empty string.
        self.textDelimiter = textDelimiter
        # The ODT result's file encoding. Defaults is "utf-8". "latin-1" is also
        # allowed, or any numeric value as defined at the URL mentioned in
        # appy/pod/converter.py, at variable HELP_CSV_URL.
        self.encoding = encoding

    def asString(self):
        '''Returns options as a string, ready-to-be sent to the Converter'''
        # Manage the optional text delimiter
        delim = ord(self.textDelimiter) if self.textDelimiter else ''
        # Manage encoding
        enc = self.encoding
        if isinstance(enc, int) or enc.isdigit():
            encoding = enc
        else:
            encoding = CsvOptions.encodings.get(enc) or 76
        return '%s,%s,%s,1' % (ord(self.fieldSeparator), delim, encoding)

# Create a default instance
CsvOptions.default = CsvOptions()

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Renderer:
    templateTypes = ('odt', 'ods') # Types of POD templates
    # Regular expression for finding the title within metadata
    metaRex = re.compile('<dc:title>.*?</dc:title>', re.S)
    metaHook = '</office:meta>'

    # Make some elements directly available here
    CsvOptions = CsvOptions

    # ODF tags that may hold POD expressions
    allExpressionsHolders = (
      'if',      # Conditional fields
      'change',  # Track-changed text
      'input',   # Text input fields
      'db'       # Database fields
    )
    defaultExpressionsHolders = ('if', 'change', 'input')

    def __init__(self, template, context, result, pythonWithUnoPath=None,
      ooServer='localhost', ooPort=2002, stream='auto', stylesMapping={},
      html=False, forceOoCall=False, finalizeFunction=None,
      overwriteExisting=False, raiseOnError=False, findImage=None,
      stylesTemplate=None, optimalColumnWidths=False, distributeColumns=False,
      script=None, managePageStyles=None, resolveFields=False,
      expressionsHolders=defaultExpressionsHolders, metadata=True,
      pdfOptions='ExportNotes=True', csvOptions=None, deleteTempFolder=True,
      protection=False, pageStart=1, tabbedCR=False, fonts=None):
        '''Base on a document template (whose path is in p_template), which is
           an ODT or ODS file containing special expressions and statements
           written in Python, this renderer generates an ODT file (whose path is
           in p_result), that is a copy of the template whose expressions and
           statements have been replaced with the objects defined in the
           p_context.'''

        # If p_result does not end with .odt or .ods, the Renderer will call
        # LibreOffice (LO) to perform a conversion. If p_forceOoCall is True,
        # even if p_result ends with .odt, LO will be called, not for performing
        # a conversion, but for updating some elements like indexes (table of
        # contents, etc) and sections containing links to external files (which
        # is the case, for example, if you use the default function "document").

        # If the Python interpreter which runs the current script is not
        # UNO-enabled, this script will run, in another process, a UNO-enabled
        # Python interpreter (whose path is p_pythonWithUnoPath) which will call
        # LO. In both cases, we will try to connect to LO in server mode on
        # p_ooServer:p_ooPort.

        # p_stream dictates the communication between the renderer and LO.
        # ----------------------------------------------------------------------
        # p_stream can hold the following values.
        # ----------------------------------------------------------------------
        # "auto"     | if p_ooServer is "localhost", exchanging the ODT result
        # (default)  | produced by the renderer (=the input) and the converted
        #            | file produced by LO (=the output) will be made via files
        #            | on disk. Else, the renderer will consider that LO runs on
        #            | another machine and the exchange will be made via streams
        #            | over the network.
        # ----------------------------------------------------------------------
        # True       | If you want to force communication of the input and
        #            | output files as streams, use stream=True.
        # ----------------------------------------------------------------------
        # False      | If you want to force communication of the input and
        #            | output files via the disk, use stream=False.
        # ----------------------------------------------------------------------
        # "in"       | The input is streamed and the output is written on disk.
        # ----------------------------------------------------------------------
        # "out"      | The input is read from disk and the output is streamed.
        # ----------------------------------------------------------------------

        # If you plan to make "XHTML to OpenDocument" conversions (via the POD
        # function "xhtml"), you may specify a "styles mapping" in
        # p_stylesMapping. Moreover, if the input(s) to this function is valid
        # HTML but not valid XHTML, specify p_html being True.

        # If you specify a function in p_finalizeFunction (or a list/tuple of
        # functions), it will be called by the renderer before re-zipping the
        # ODT/S result. This way, you can still perform some actions on the
        # content of the ODT/S file before it is zipped and potentially
        # converted. Every such function must accept 2 args:
        #  *  the absolute path to the temporary folder, containing the
        #     un-zipped content of the ODT/S result;
        #  *  the Renderer instance.

        # If you set p_overwriteExisting to True, the renderer will overwrite
        # the result file. Else, an exception will be thrown if the result file
        # already exists.

        # If p_raiseOnError is False (the default value), any error encountered
        # during the generation of the result file will be dumped into it, as a
        # Python traceback within a note. Else, the error will be raised.

        # When, in the process of converting a chunk of XHTML code to ODF, a
        # "img" tag is encountered, POD performs a HTTP GET to retrieve it. If
        # the image is stored on the same server running POD, this can be
        # problematic in two ways:
        # 1) regarding performance, it would be better to retrieve the image
        #    from disk;
        # 2) via HTTP, POD may not be allowed to retrieve the image.
        # In order to overcome these problems, place a function in "findImage".
        # While converting chunks of XHTML code, everytime an "img" tag is
        # encountered, this function will be called, with the image URL as
        # unique arg. If the function returns the absolute path to the image, it
        # will be used instead of performing a HTTP GET request. If the function
        # returns None (ie: it has detected that is is a "truly external" URL),
        # the HTTP GET will nevertheless be performed.

        # p_stylesTemplate can be the path to a LibreOffice file (ie, a .ott
        # file) whose styles will be imported within the result.

        # p_optimalColumnWidths corresponds to the homonym option to
        # converter.py, excepted that values "True" or "False" must be boolean
        # values. Note that the POD function "xhtml" requires this parameter to
        # be "OCW_.*" to be fully operational. When p_optimalColumnWidths is not
        # False, forceOoCall is forced to True.

        # p_distributeColumns corresponds to the homonym option to converter.py,
        # excepted that values "True" or "False" must be boolean values. Note
        # that the POD function "xhtml" requires this parameter to be "DC_.*" to
        # be fully operational. When p_distributeColumns is not False,
        # forceOoCall is forced to True.

        # p_script is the absolute path to a Python script containing functions
        # that the converter will call in order to customize the process of
        # manipulating the document via the LibreOffice UNO interface. For more
        # information, see appy/pod/converter.py, option "-s". Note that when
        # such p_script is specified, p_forceOoCall is forced to True.

        # If this document is a sub-document to be included in a master one, it
        # has sense to set a specific value for parameter p_managePageStyles:
        # ----------------------------------------------------------------------
        #  "rename" | will rename all page styles with unique names. This way,
        #           | when imported into a master document, no name clash will
        #           | occur and elements tied to page styles (like headers and
        #           | footers) will be correctly imported for all included
        #           | sub-documents. The "do... pod" statement automatically
        #           | sets this parameter to "rename";
        # ----------------------------------------------------------------------
        #   <int>   | will rename page styles similarly to "rename" and will
        #           | also restart, in the sub-document, page numbering at this
        #           | integer value. It will only work if page styles are
        #           | explicitly applied to pages in the sub-pod template. In
        #           | order to achieve this with LibreOffice, open your
        #           | template, set the cursor somewhere in the first page,
        #           | open the pane with page styles, and double-clic on the
        #           | "default style". To check if it has worked, click inside
        #           | the first paragraph in the page, open its properties and
        #           | check that a page break has been defined on it.
        # ----------------------------------------------------------------------

        # If you want to replace (some) fields with their "hard-coded" values,
        # use p_resolveFields. It can be useful, for instance, if the POD result
        # must be included in a master document (via statement "do ... from
        # pod"), but the total number of pages must be kept as is. If
        # p_resolveFields is True, all fields will be resolved, excepted special
        # ones like PageNumber. Indeed, its value is different from one page to
        # another, so resolving it to a single, hard-coded value has no sense.
        # You can also specify "PageCount" as value for p_resolveField. In this
        # case, only the field(s) containing the total number of pages will be
        # resolved. Use it if it is the only field you need to resolve, it will
        # be more performant. Note that when p_resolveFields is set,
        # p_forceOoCall is forced to True.

        # POD expressions may be defined at various places within a document
        # template. Possible places are listed in static variable
        # "allExpressionsHolders" hereabove. Default places are listed in static
        # variable "defaultExpressionsHolders" hereabove.

        # If p_metadata is True, the result will get a metadata property "title"
        # (in meta.xml) being the result file name, without its extension. If
        # p_metadata is a string, it will be used as title.

        # If the result must be produced in PDF, options being specific to this
        # format can be passed in p_pdfOptions, as a comma-separated string of
        # key=value pairs, as in

        #            ExportNotes=False,PageRange=1-20,Watermark=Sample

        # More info in appy/pod/converter.py.

        # If the result must be produced in CSV, options being specific to this
        # format can be passed in p_csvOptions, as an instance of class
        # CsvOptions, available on class Renderer as Renderer.CsvOptions. If
        # p_csvOptions is None, defauls CSV options will be used from
        # Renderer.CsvOptions.default.

        # If this renderer is called by another one (its "parent"), it may
        # receive an additional parameter, p_deleteTempFolder. If False, the
        # temp folder may be reused by other children of the parent renderer, so
        # we do not delete it (the parent will do it at the end of the whole
        # process).

        # if "protection" is True, you can define variables "cellProtected"
        # and/or "sectionProtected" to determine, respectively, if a cell or a
        # section must be write-protected. It is not enabled by default because
        # it has a little impact on performance and on the size of the p_result
        # (especially large ods results).

        # If p_pageStart is different from 1, the produced document will start
        # page numbering at this number. In that case, p_forceOoCall will be
        # forced to True.

        # By default, the *c*arriage *r*eturn (CR) char is converted to ODF tag
        # <text:line-break/>. This may cause problems with justified text. These
        # problems are overcomed by prefixing the tag with <text:tab/> for
        # producing <text:tab/><text:line-break/>. But beware: "tabbing" the CR
        # that way may cause problems when exporting the POD result to Microsoft
        # Word. This is why attribute "tabbedCR" exists.

        # Attribute "fonts" may hold the name of a font that must exist on the
        # machine running this renderer. If such a name is passed, all base
        # styles defined in the POD template will be redefined with this font.
        # On (most? all?) Linux machines, list the available fonts via a command
        # like:
        #                      fc-list :lang=en family

        self.template = template
        self.result = result
        self.resultType = os.path.splitext(result)[1].strip('.')
        self.contentXml = None # Content (string) of content.xml
        self.stylesXml = None # Content (string) of styles.xml
        self.manifestXml = None # Content (string) of manifest.xml
        self.metaXml = None # Content (string) of meta.xml
        # Manages the styles defined into the ODT template
        self.tempFolder = None
        self.env = None
        self.pythonWithUnoPath = pythonWithUnoPath
        self.ooServer = ooServer
        self.ooPort = ooPort
        self.stream = stream
        # p_forceOoCall may be forced to True
        self.forceOoCall = forceOoCall or bool(optimalColumnWidths) or \
          bool(distributeColumns) or bool(script) or bool(resolveFields) or \
          (pageStart > 1)
        # Must the POD post-processor (ppp) be enabled ?
        self.ppp = False
        self.finalizeFunction = self.formatFinalizeFunction(finalizeFunction)
        self.overwriteExisting = overwriteExisting
        self.raiseOnError = raiseOnError
        self.findImage = findImage
        self.stylesTemplate = stylesTemplate
        self.optimalColumnWidths = optimalColumnWidths
        self.distributeColumns = distributeColumns
        self.script = script
        self.managePageStyles = managePageStyles
        self.resolveFields = resolveFields
        self.expressionsHolders = expressionsHolders
        self.metadata = metadata
        self.pdfOptions = pdfOptions
        self.csvOptions = csvOptions
        self.deleteTempFolder = deleteTempFolder
        self.protection = protection
        self.pageStart = pageStart
        self.tabbedCR = tabbedCR
        self.fonts = fonts
        # If sub-renderers are called, keep a trace of them
        self.children = {} # ~{s_templatePath: Renderer}~
        # Keep trace of the original context given to the renderer
        self.originalContext = context
        # Remember potential files or images that will be included through
        # "do ... from document" statements: we will need to declare them in
        # META-INF/manifest.xml. Keys are file names as they appear within the
        # ODT file (to dump in manifest.xml); values are original paths of
        # included images (used for avoiding to create multiple copies of a file
        # which is imported several times).
        self.fileNames = {}
        self.prepareFolders()
        # Unzip the p_template
        info = unzip(template, self.unzipFolder, odf=True)
        self.contentXml = info['content.xml']
        self.stylesXml = info['styles.xml']
        # Manage the styles defined into the ODT template
        self.stylesManager = sm.StylesManager(self)
        # From LibreOffice 3.5, it is not possible anymore to dump errors into
        # the resulting ods as annotations. Indeed, annotations can't reside
        # anymore within paragraphs. ODS files generated with pod and containing
        # error messages in annotations cause LibreOffice 3.5 and 4.0 to crash.
        # LibreOffice >= 4.1 simply does not show the annotation.
        if info['mimetype'] == utils.mimeTypes['ods']: self.raiseOnError = True
        # Create the parsers for content.xml and styles.xml
        self.createParsers(context)
        # Store the styles mapping
        self.setStylesMapping(stylesMapping)
        # Store the p_html parameter
        self.html = html

    def reinit(self, result, context):
        '''Re-initialise this renderer (p_self) for recycling him and produce
           another p_result with another p_context.'''
        self.result = result
        self.originalContext = context
        # Re-create POD parsers
        self.createParsers(context)
        # Reinitialise attributes being specific to a given result
        smap = self.stylesManager.stylesMapping
        self.stylesManager = sm.StylesManager(self)
        self.stylesManager.stylesMapping = smap

    # Attributes to clone to a sub-renderer when using m_clone hereafter
    cloneAttributes = ('pythonWithUnoPath', 'ooServer', 'ooPort', 'html',
      'raiseOnError', 'findImage', 'stylesTemplate', 'optimalColumnWidths',
      'distributeColumns', 'expressionsHolders', 'protection', 'tabbedCR',
      'fonts')

    def clone(self, template, context, result, **params):
        '''Creates another Renderer instance, similar to p_self, but for
           rendering a different p_result based on another p_context and
           p_template, with possibly different other p_params. Any parameter not
           being in p_params but listed in Renderer.cloneAttributes will be
           copied from p_self to the clone.'''
        # Complete p_params with attributes listed in Renderer.cloneAttributes
        for name in Renderer.cloneAttributes:
            if name not in params:
                params[name] = getattr(self, name)
        # Create and return the clone
        return Renderer(template, context, result, **params)

    def formatFinalizeFunction(self, fun):
        '''Standardize "finalize function" p_fun as a list of functions'''
        if not fun: return
        elif isinstance(fun, list): return fun
        elif isinstance(fun, tuple): return list(fun)
        else: return [fun]

    def enablePpp(self):
        '''Activate the POD post-processor, which is implemented as a series of
           UNO commands.'''
        self.forceOoCall = True
        self.ppp = True

    def getCompleteContext(self, context):
        '''Create and return a complete context, from the one given by the pod
           developer (p_context).'''
        r = {}
        if hasattr(context, '__dict__'):
            r.update(context.__dict__)
        elif isinstance(context, dict) or isinstance(context, UserDict):
            r.update(context)
        else:
            raise PodError(BAD_CTX)
        # Incorporate the default, unalterable, context
        r.update({'xhtml': self.renderXhtml, 'text': self.renderText,
          'document': self.importDocument, 'image': self.importImage,
          'pod': self.importPod, 'cell': self.importCell,
          'shape': self.drawShape, 'TableProperties': sm.TableProperties,
          'BulletedProperties': sm.BulletedProperties,
          'NumberedProperties': sm.NumberedProperties,
          'pageBreak': self.insertPageBreak,
          'columnBreak': self.insertColumnBreak,
          # Variables to use for representing pod-reserved chars
          'PIPE': '|', 'SEMICOLON': ';'})
        # Developer, forget the following line
        if '_ctx_' not in r: r['_ctx_'] = r
        return r

    def createPodParser(self, odtFile, context, inserts=None):
        '''Creates the parser with its environment for parsing the given
           p_odtFile (content.xml or styles.xml). p_context is given by the pod
           user, while p_inserts depends on the ODT file we must parse.'''
        context = self.getCompleteContext(context)
        env = PodEnvironment(context, inserts, self.expressionsHolders)
        fileBuffer = FileBuffer(env, os.path.join(self.tempFolder, odtFile))
        env.currentBuffer = fileBuffer
        return PodParser(env, self)

    def createParsers(self, context):
        '''Creates parsers for content.xml and styles.xml and store them,
           respectively, in p_self.contentParser and p_self.stylesParser.'''
        nso = PodEnvironment.NS_OFFICE
        for name in ('content', 'styles'):
            styleTag = 'automatic-styles' if name == 'content' else 'styles'
            inserts = (OdInsert(POD_STYLES[name], Tag(styleTag, nsUri=nso)),)
            parser = self.createPodParser('%s.xml' % name, context, inserts)
            setattr(self, '%sParser' % name, parser)

    def renderXhtml(self, s, stylesMapping={}, keepWithNext=0,
                    keepImagesRatio=False, imagesMaxWidth='page', html=None,
                    code=False, unwrap=False):
        '''Method that can be used (under the name "xhtml") into a POD template
           for converting a chunk of XHTML content (p_s) into a chunk of ODF
           content.'''

        # For this conversion, beyond the global styles mapping defined at the
        # renderer level, a specific p_stylesMapping can be passed: any key in
        # it overrides its homonym in the global mapping.

        # Parameter p_keepWithNext is used to prevent the last part of a
        # document to be left alone on top of the last page. Imagine your POD
        # template is an official document ending with some director's scanned
        # signature. Just before this signature, the document body is inserted
        # using m_renderXhtml. Depending on p_s's length, in some cases, the
        # scanned signature may end up alone on the last page. When using
        # p_keepWithNext, POD applies a specific style to p_s's last paragraph,
        # such that it will get standard LibreOffice property "keep-with-next"
        # and will thus be "pushed" on the last page, together with the scanned
        # signature, even if there is still space available on the previous one.

        # p_keepWithNext may hold the following values.
        # ----------------------------------------------------------------------
        #  0  | (the default) Keep-with-next functionality is disabled.
        # ----------------------------------------------------------------------
        #  1  | Keep-with-next is enabled as described hereabove: p_s's last
        #     | paragraph receives LibreOffice property "keep-with-next". It
        #     | also works if the last paragraph is a bulleted or numbered item.
        # ----------------------------------------------------------------------
        #  >1 | If p_keepWithNext is higher than 1, it represents a number of
        #     | characters to "keep-with-next". Indeed, in some cases, keeping
        #     | only the last paragraph may not be sufficient: a bit more text
        #     | could produce a better result. Based on this number of
        #     | characters, POD will determine how many paragraphs will get
        #     | property "keep-with-next" and will apply it to all of them. For
        #     | example, suppose p_keepWithNext is defined to 60. The last 3
        #     | paragraphs contain, respectively, 20, 30 and 35 characters. POD
        #     | will apply property "keep-with-next" to the 2 last paragraphs.
        #     | The algorithm is the following: POD walks p_s's paragraphs
        #     | backwards, starting from the last one, counting and adding the
        #     | number of characters for every walked paragraph. POD continues
        #     | the walk until it reaches (or exceeds) the number of characters
        #     | to keep. When it is the case, it stops. All the paragraphs
        #     | walked so far receive property "keep-with-next".
        #     | ~~~
        #     | POD goes even one step further by applying "keep-with-next"
        #     | properties to tables as well. In the previous example, if, when
        #     | counting 60 characters backwards, we end up in the middle of a
        #     | table, POD will apply property "keep-with-next" to the whole
        #     | table. However, with tables spanning more than one page, there
        #     | is a problem: if property "keep-with-next" is applied to such a
        #     | table, LibreOffice will insert a page break at the beginning of
        #     | the table. This can be annoying. While this may be considered a
        #     | bug (maybe because it represents a constraint being particularly
        #     | hard to implement), it is the behaviour implemented in
        #     | LibreOffice, at least >= 3 and <= 6.4. Consequently, at the POD
        #     | level, an (expensive) workaround has been found: when
        #     | p_keepWithNext characters lead us inside a table, POD will split
        #     | it into 2 tables: a first table containing all the rows that
        #     | were not walked by the keep-with-next algorithm, and a second
        #     | containing the remaining, walked rows. On this second table
        #     | only, property "keep-with-next" is applied. Because splitting
        #     | tables that way requires LibreOffice running in server mode, as
        #     | soon as you specify p_keepWithNext > 1, POD wil assume
        #     | LibreOffice runs in server mode.
        # ----------------------------------------------------------------------

        # If p_keepImagesRatio is True, while importing images from "img" tags
        # within p_s, their width/height ratio will be kept. Note that in most
        # cases, it is useless to specify it, because POD computes the image's
        # real width and height.

        # Parameter p_imagesMaxWidth corresponds to parameter p_maxWith from POD
        # function m_document. Being "page" by default, it prevents the images
        # defined in p_s to exceed the ODT result's page width.
        
        # If p_html is not None, it will override renderer's homonym parameter.
        # Set p_html to True if p_s is not valid XHTML but standard HTML, where
        # invalid-XML tags like <br> may appear.

        # If, in p_s, you have inserted special "a" tags allowing to incorporate
        # parts of external Python files, set this parameter to True. In that
        # case, everytime such link will be encountered, POD will retrieve the
        # file via a HTTP request and incorporate the part (class, method..)
        # specified in the link's "title" attribute, into the resulting chunk of
        # ODF code. More information about this functionality, check Appy's Rich
        # field in class appy.model.fields.rich.c_Rich.

        # If you set p_unwrap being True, if the resulting ODF chunk is
        # completely included in a single paragraph (<text:p>), this paragraph's
        # start and end tags will be removed from the result (keeping only its
        # content). Avoid using this. p_unwrap should only be used internally by
        # POD itself.

        stylesMapping = self.stylesManager.checkStylesMapping(stylesMapping)
        if html is None: html = self.html
        return Xhtml2OdtConverter(s, self.stylesManager, stylesMapping,
                                  keepWithNext, keepImagesRatio, imagesMaxWidth,
                                  self, html, code, unwrap).run()

    def renderText(self, s, prefix=None, tags=None, firstCss=None,
                   otherCss=None, lastCss=None, stylesMapping={}):
        '''Renders the pure text p_s in the ODF result. For every carriage
           return character present in p_s, a new paragraph is created in the
           ODF result.'''

        # p_prefix, if passed, must be a string that will be inserted before
        # p_s's first line, followed by a tab.

        # p_tags can be a sequence of XHTML single-letter tags (ie, "bu" for
        # "bold" + "underline"). If passed, formatting as defined by these
        # letters will be applied to the whole p_s (the p_prefix excepted).

        # You may go further by applying CSS classes to the paragraphs produced
        # by p_s's conversion to ODF. For every such class, if a style having
        # the same name is found on the ODF template, it will be applied to the
        # corresponding paragraph. The CSS class:

        # ----------------------------------------------------------------------
        # defined in      | will be
        # attribute ...   | applied to ...
        # ----------------------------------------------------------------------
        # p_firstCss      | the ODF result's first paragraph;
        # p_lastCss       | the ODF result's last paragraph;
        # p_otherCss      | any other paragraph in between.
        # ----------------------------------------------------------------------

        # Moreover, because, internally, p_s is converted to a chunk of XHTML
        # code, and passed to method m_renderXhtml, a p_stylesMapping can be
        # passed to m_renderText, exactly as you would do for m_renderXhtml.
        # ~~~
        # Determine the prefix to insert before the first line
        prefix = '%s<tab/>' % prefix if prefix else ''
        # Split p_s into lines of text
        r = s.split('\n')
        if tags:
            # Prepare the opening and closing sub-tags
            opening = ''.join(['<%s>' % tag for tag in tags])
            closing = ''
            j = len(tags) - 1
            while j >= 0:
                closing += '</%s>' % tags[j]
                j -= 1
        else:
            opening = closing = ''
        i = length = len(r) - 1
        pre = ''
        while i >= 0:
            # Get the CSS class to apply
            if i == 0:
                css = firstCss
                pre = prefix
            elif i == length:
                css = lastCss
            else:
                css = otherCss
            css = ' class="%s"' % css if css else ''
            r[i] = '<p%s>%s%s%s%s</p>' % (css, pre, opening, r[i], closing)
            i -= 1
        return self.renderXhtml(''.join(r), stylesMapping=stylesMapping)

    # Supported image formats. "image" represents any format
    imageFormats = ('png', 'jpeg', 'jpg', 'gif', 'svg', 'image')
    ooFormats = ('odt',)
    convertibleFormats = FILE_TYPES.keys()
    # Constant indicating if a renderer must inherit a value from is parent
    # renderer.
    INHERIT = 1

    def importDocument(self, content=None, at=None, format=None,
      anchor='as-char', wrapInPara=True, size=None, sizeUnit='cm',
      maxWidth='page', style=None, keepRatio=True, pageBreakBefore=False,
      pageBreakAfter=False, convertOptions=None):
        '''Implements the POD statement "do... from document"'''

        # If p_at is not None, it represents a path or url allowing to find the
        # document. It can be a string or a pathlib.Path instance. If p_at is
        # None, the content of the document is supposed to be in binary format
        # in p_content. The document p_format may be: odt or any format in
        # imageFormats.

        # p_anchor, p_wrapInPara, p_size, p_sizeUnit, p_style and p_keepRatio
        # are only relevant for images:
        # * p_anchor defines the way the image is anchored into the document;
        #       Valid values are 'page', 'paragraph', 'char' and 'as-char';
        # * p_wrapInPara, if true, wraps the resulting 'image' tag into a 'p'
        #       tag;
        # * p_size, if specified, is a tuple of float or integers (width,
        #       height) expressing size in p_sizeUnit (see below). If not
        #       specified, size will be computed from image info;
        # * p_sizeUnit is the unit for p_size elements, it can be "cm"
        #       (centimeters), "px" (pixels) or "pc" (percentage). Percentages,
        #       in p_size, must be expressed as integers from 1 to 100.
        # * if p_maxWidth is specified (as a float value representing cm),
        #       image's width will not be greater than it. If p_maxWidth is
        #       "page" (the default), p_maxWidth will be computed as the width
        #       of the main document's page style, margins excluded.
        # * if p_style is given, it is a appy.shared.css.CssStyles instance,
        #       containing CSS attributes. If "width" and "heigth" attributes
        #       are found there, they will override p_size and p_sizeUnit.
        # * If p_keepRatio is True, the image width/height ratio will be kept
        #       when p_size is specified.

        # p_pageBreakBefore and p_pageBreakAfter are only relevant for importing
        # external odt documents, and allows to insert a page break before/after
        # the inserted document. More precisely, each of these parameters can
        # have values:
        # * True     insert a page break;
        # * False    do no insert a page break;
        # moreover, p_pageBreakAfter can have this additional value:
        # * 'duplex' insert 2 page breaks if the sub-document has an odd number
        #            of pages, 1 else (useful for duplex printing).

        # If p_convertOptions are given (for images only), imagemagick will be
        # called with these options to perform some transformation on the image.
        # For example, if you specify
        #                    convertOptions="-rotate 90"

        # pod will perform this command before importing the file into the
        # result:
        #               convert your.image -rotate 90 your.image

        # You can also specify a function in convertOptions. This function will
        # receive a single arg, "image", an instance of
        # appy.pod.doc_importers.Image giving some characteristics of the image
        # to convert, like image.width and image.height in pixels (integers). If
        # your function does not return a string containing the convert options,
        # no conversion will occur.

        # ~~~
        # Is there something to import ?
        if not content and not at: raise PodError(DOC_KO)
        # Convert p_at to a string if it is not the case
        at = str(at) if isinstance(at, Path) else at
        # Guess document format
        if not format:
            # It should be deduced from p_at
            if not at:
                raise PodError(DOC_FMT_KO)
            format = os.path.splitext(at)[1][1:]
        else:
            # If format is a mimeType, convert it to an extension
            if format in utils.mimeTypesExts:
                format = utils.mimeTypesExts[format]
        isImage = isOdt = False
        importer = None
        if format in self.ooFormats:
            importer = importers.OdtImporter
            self.forceOoCall = True
            isOdt = True
        elif (format in self.imageFormats) or not format:
            # If the format can't be guessed, we suppose it is an image
            importer = importers.ImageImporter
            isImage = True
        elif format == 'pdf':
            importer = importers.PdfImporter
        elif format in self.convertibleFormats:
            importer = importers.ConvertImporter
        else:
            raise PodError(DOC_FMT_NS % format)
        imp = importer(content, at, format, self)
        # Initialise image-specific parameters
        if isImage:
            imp.init(anchor, wrapInPara, size, sizeUnit, maxWidth, style,
                     keepRatio, convertOptions)
        elif isOdt: imp.init(pageBreakBefore, pageBreakAfter)
        return imp.run()

    def importImage(self, content=None, at=None, format=None, size=None,
                    sizeUnit='cm', maxWidth='page', style=None, keepRatio=True,
                    convertOptions=None):
        '''While m_importDocument allows to import a document or image via a
           "do ... from document" statement, method m_importImage allows to
           import an image anchored as a char via a POD expression
           ":image(...)", having almost the same parameters.'''

        # Compared to the "document" function, and due to the specific nature of
        # the "image" function, 2 parameters are missing:
        # (1) "anchor" is forced to be "as-char";
        # (2) "wrapInPara" is forced to False.
        return self.importDocument(content=content, at=at, format=format,
          wrapInPara=False, size=size, sizeUnit=sizeUnit, maxWidth=maxWidth,
          style=style, keepRatio=keepRatio, convertOptions=convertOptions)

    def getResolvedNamespaces(self):
        '''Gets a context where mainly used namespaces have been resolved'''
        env = self.stylesParser.env
        return {'text': env.ns(env.NS_TEXT), 'style': env.ns(env.NS_STYLE)}

    def importPod(self, content=None, at=None, format='odt', context=None,
                  pageBreakBefore=False, pageBreakAfter=False,
                  managePageStyles='rename', resolveFields=False,
                  forceOoCall=INHERIT):
        '''Implements the POD statement "do... from pod"'''

        # Similar to m_importDocument, but allows to import the result of
        # executing the POD template whose absolute path is specified in p_at
        # (or, but deprecated, whose binary content is passed in p_content, with
        # this p_format) and include it in the POD result.

        # Renaming page styles for the sub-POD (p_managePageStyles being
        # "rename") ensures there is no name clash between page styles (and tied
        # elements such as headers and footers) coming from several sub-PODs or
        # with styles defined at the master document level. This takes some
        # processing, so you can set it to None if you are sure you do not need
        # it.

        # p_resolveFields has the same meaning as the homonym parameter on the
        # Renderer.

        # By default, if p_forceOoCall is True for p_self, a sub-renderer ran by
        # a c_PodImporter will inherit from this attribute, excepted if
        # parameter p_forceOoCall is different from INHERIT.
        # ~~~
        # Is there a pod template defined ?
        if not content and not at: raise PodError(DOC_KO)
        imp = importers.PodImporter(content, at, format, self)
        self.forceOoCall = True
        # Define the context to use: either the current context of the current
        # POD renderer, or p_context if given.
        context = context or self.contentParser.env.context
        imp.init(context, pageBreakBefore, pageBreakAfter, managePageStyles,
                 resolveFields, forceOoCall)
        return imp.run()

    def importCell(self, content, style='Default'):
        '''Creates a chunk of ODF code ready to be dumped as table cell'''
        # The generated cell will contain this textual p_content and this
        # p_style will be applied.
        return '<table:table-cell table:style-name="%s">' \
               '<text:p>%s</text:p></table:table-cell>' % (style, content)

    def drawShape(self, name, type='rect', stroke='none', strokeWidth='0cm',
                  strokeColor='#666666', fill='solid', fillColor='#666666',
                  anchor='char', width='1.0cm', height='1.0cm',
                  deltaX='0.0cm', deltaY='0.0cm', target='styles'):
        '''Renders a shape within a POD result'''
        # Generate a style for this shape and add it among dynamic styles
        style = self.stylesManager.stylesGenerator.addGraphicalStyle(target,
          stroke=stroke, strokeWidth=strokeWidth, strokeColor=strokeColor,
          fill=fill, fillColor=fillColor)
        # Return the ODF code representing the shape
        return '<draw:%s text:anchor-type="%s" draw:z-index="1" ' \
               'draw:name="%s" draw:style-name="%s" ' \
               'draw:text-style-name="MP1" svg:width="%s" svg:height="%s"' \
               ' svg:x="%s" svg:y="%s"><text:p/></draw:%s>' % \
               (type, anchor, name, style.name, width, height, deltaX, deltaY,
                type)

    def _insertBreak(self, type):
        '''Inserts a page or column break into the result'''
        name = 'podPageBreakAfter' if type == 'page' else 'podColumnBreak'
        return '<text:p text:style-name="%s"></text:p>' % name

    def insertPageBreak(self): return self._insertBreak('page')
    def insertColumnBreak(self): return self._insertBreak('column')

    def prepareFolders(self):
        '''Ensure p_self.result is correct and create, when relevant, the temp
           folder for preparing it.'''
        # Ensure p_self.result is an absolute path
        self.result = os.path.abspath(self.result)
        # Raise an error if the result already exists and we can't overwrite it
        if os.path.isdir(self.result):
            raise PodError(RES_FOLDER % self.result)
        exists = os.path.isfile(self.result)
        if not self.overwriteExisting and exists:
            raise PodError(RES_EXISTS % self.result)
        # Remove the result if it exists
        if exists: os.remove(self.result)
        # Create a temp folder for storing temporary files
        self.tempFolder = '%s.%f' % (self.result, time.time())
        try:
            os.mkdir(self.tempFolder)
        except OSError as oe:
            raise PodError(TEMP_W_KO % (self.result, oe))
        # The "unzip" folder is a sub-folder, within self.tempFolder, where
        # p_self.template will be unzipped.
        self.unzipFolder = os.path.join(self.tempFolder, 'unzip')
        os.mkdir(self.unzipFolder)

    def patchMetadata(self):
        '''Declares, in META-INF/manifest.xml, images or files included via the
           "do... from document" statements if any, and patch meta.xml (field
           "title").'''
        # Patch META-INF/manifest.xml
        j = os.path.join
        if self.fileNames:
            toInsert = ''
            for fileName in self.fileNames.keys():
                mimeType = mimetypes.guess_type(fileName)[0]
                toInsert += ' <manifest:file-entry manifest:media-type="%s" ' \
                            'manifest:full-path="%s"/>\n' % (mimeType, fileName)
            manifestName = j(self.unzipFolder, 'META-INF', 'manifest.xml')
            # Read the the content of this file, if not already in
            # self.manifestXml.
            if not self.manifestXml:
                f = open(manifestName)
                self.manifestXml = f.read()
                f.close()
            hook = '</manifest:manifest>'
            content = self.manifestXml.replace(hook, toInsert + hook)
            # Write the new manifest content
            f = open(manifestName, 'w')
            f.write(content)
            f.close()
        # Patch meta.xml
        metadata = self.metadata
        if metadata:
            metaName = j(self.unzipFolder, 'meta.xml')
            # Read the content of this file, if not already in self.metaXml
            if not self.metaXml:
                f = open(metaName)
                self.metaXml = f.read()
                f.close()
            # Remove the existing title, if it exists
            content = self.metaRex.sub('', self.metaXml)
            # Add a new title, based on the result name
            if isinstance(metadata, str):
                title = metadata
            else:
                title = os.path.splitext(os.path.basename(self.result))[0]
            hook = self.metaHook
            title = '<dc:title>%s</dc:title>%s' % (title, hook)
            content = content.replace(hook, title)
            f = open(metaName, 'w')
            f.write(content)
            f.close()

    # Public interface
    def run(self):
        '''Renders the result'''
        try:
            # Remember which parser is running
            self.currentParser = self.contentParser
            # Create the resulting content.xml
            self.currentParser.parse(self.contentXml)
            self.currentParser = self.stylesParser
            # Create the resulting styles.xml
            self.currentParser.parse(self.stylesXml)
            # Patch metadata
            self.patchMetadata()
            # Re-zip the result
            self.finalize()
        finally:
            if self.deleteTempFolder:
                FolderDeleter.delete(self.tempFolder)

    def getStyles(self):
        '''Returns a dict of the styles that are defined into the template'''
        return self.stylesManager.styles

    def setStylesMapping(self, stylesMapping):
        '''Establishes a correspondence between, on one hand, CSS styles or
           XHTML tags that will be found inside XHTML content given to POD,
           and, on the other hand, ODT styles found into the template.'''
        try:
            manager = self.stylesManager
            # Initialise the styles mapping when relevant
            ocw = self.optimalColumnWidths
            dis = self.distributeColumns
            if ocw or dis:
                sm.TableProperties.initStylesMapping(stylesMapping, ocw, dis)
            manager.stylesMapping = manager.checkStylesMapping(stylesMapping)
        except PodError as po:
            self.contentParser.env.currentBuffer.content.close()
            self.stylesParser.env.currentBuffer.content.close()
            if os.path.exists(self.tempFolder):
                FolderDeleter.delete(self.tempFolder)
            raise po

    def callLibreOffice(self, resultName, outputName=None, format=None):
        '''Call LibreOffice in server mode to convert or update the result'''
        # Here are the valid combinations for parameter's values.
        # ----------------------------------------------------------------------
        # no outputName | The converter will produce a result whose name is
        #   no format   | p_resultName whose file extension has been replaced
        #               | with the one specified in self.resultType.
        # ----------------------------------------------------------------------
        # no outputName | Idem, but the output format is forced to p_format
        #    format     | instead of using self.resultType.
        # ----------------------------------------------------------------------
        #  outputName   | The converter will produce a result whose name is
        #  no format    | p_outputName. The output format will depend on
        #               | p_outputName's file extension.
        # ----------------------------------------------------------------------
        loOutput = ''
        # Determine the "result" to ask to LibreOffice
        if outputName:
            result = outputName
            resultType = os.path.splitext(result)[-1][1:]
        else:
            result = format or self.resultType
            resultType = result
        # Get CSV options if we must produce a CSV file
        if resultType == 'csv':
            csvOptions = (self.csvOptions or CsvOptions.default).asString()
        else:
            csvOptions = None
        try:
            if (not isinstance(self.ooPort, int)) and \
               (not isinstance(self.ooPort, long)):
                raise PodError(BAD_OO_PORT % str(self.ooPort))
            try:
                from appy.pod.converter import Converter
                try:
                    Converter(resultName, result, self.ooServer, self.ooPort,
                      self.stylesTemplate, self.optimalColumnWidths,
                      self.distributeColumns, self.script, self.resolveFields,
                      self.pdfOptions, csvOptions, self.ppp, self.stream,
                      self.pageStart).run()
                except Converter.Error as ce:
                    raise PodError(CONV_ERROR % str(ce))
            except ImportError:
                # I do not have UNO. So try to launch a UNO-enabled Python
                # interpreter which should be in self.pythonWithUnoPath.
                pyPath = self.pythonWithUnoPath
                if not pyPath:
                    raise PodError(NO_PY_PATH % resultType)
                if not os.path.isfile(pyPath):
                    raise PodError(PY_PATH_KO % pyPath)
                convScript = '%s/converter.py' % \
                             os.path.dirname(appy.pod.__file__)
                cmd = [pyPath, convScript, resultName, result,
                       '-e', self.ooServer, '-p', str(self.ooPort)]
                add = cmd.append
                if self.stylesTemplate:
                    add('-t'); add(self.stylesTemplate)
                if self.optimalColumnWidths:
                    add('-o'); add(str(self.optimalColumnWidths))
                if self.distributeColumns:
                    add('-d'); add(str(self.distributeColumns))
                if self.script:
                    add('-s'); add(self.script)
                if self.resolveFields:
                    add('-r'); add(self.resolveFields)
                if self.pdfOptions:
                    add('-f'); add(self.pdfOptions)
                if csvOptions:
                    add('-i'); add(csvOptions)
                if self.ppp: add('-c')
                if self.stream != 'auto':
                    add('-a'); add(str(self.stream))
                if self.pageStart > 1:
                    add('-g'); add(str(self.pageStart))
                out, loOutput = utils.executeCommand(cmd)
        except PodError as pe:
            # When trying to call LO in server mode for producing ODT or ODS
            # (=forceOoCall=True), if an error occurs we have nevertheless
            # an ODT or ODS to return to the user. So we produce a warning
            # instead of raising an error.
            if (resultType in self.templateTypes) and self.forceOoCall:
                print(WARN_OD_KO % str(pe))
            else:
                raise pe
        return loOutput

    def getTemplateType(self):
        '''Identifies the type of the pod template in self.template
           (ods or odt). If self.template is a string, it is a file name and we
           simply get its extension. Else, it is a binary file in a StringIO
           instance, and we seek the mime type from the first bytes.'''
        if isinstance(self.template, str):
            res = os.path.splitext(self.template)[1][1:]
        else:
            # A StringIO instance
            self.template.seek(0)
            firstBytes = self.template.read(90)
            firstBytes = firstBytes[firstBytes.index('mimetype')+8:]
            if firstBytes.startswith(utils.mimeTypes['ods']):
                res = 'ods'
            else:
                res = 'odt' # We suppose this is ODT
        return res

    def finalize(self):
        '''Re-zip the result and potentially call LibreOffice if target format
           is not among self.templateTypes or if forceOoCall is True.'''
        j = os.path.join
        # If an action regarding page styles must be performed, get and modify
        # them accordingly.
        pageStyles = None
        mps = self.managePageStyles
        if mps is not None:
            pageStyles = self.stylesManager.pageStyles.init(mps)
        # Patch styles.xml and content.xml
        dynamic = self.stylesManager.dynamicStyles
        for name in ('styles', 'content'):
            # Copy the [content|styles].xml file from the temp to the zip folder
            fn = '%s.xml' % name
            shutil.copy(j(self.tempFolder, fn), j(self.unzipFolder, fn))
            # Get the file content
            fn = os.path.join(self.unzipFolder, fn)
            f = open(fn)
            content = f.read()
            f.close()
            # Inject self.fonts, when present, in styles.xml
            isStylesXml = name == 'styles'
            if isStylesXml and self.fonts:
                content = sm.FontsInjector(self.fonts).injectIn(content)
            # Inject dynamic styles
            if isStylesXml: content = dynamic.injectIn('styles_base', content)
            content = dynamic.injectIn(name, content)
            # Rename the page styles
            if pageStyles:
                content = pageStyles.renameIn(name, content)
            # Write the updated content to the file
            f = open(fn, 'w')
            f.write(content)
            f.close()
        # Call the user-defined "finalize" function(s) when present
        if self.finalizeFunction:
            try:
                for fun in self.finalizeFunction: fun(self.unzipFolder, self)
            except Exception as e:
                print(WARN_FIN_KO % str(e))
        # Re-zip the result, first as an OpenDocument file of the same type as
        # the POD template (odt, ods...)
        resultExt = self.getTemplateType()
        resultName = os.path.join(self.tempFolder, 'result.%s' % resultExt)
        resultType = self.resultType
        zip(resultName, self.unzipFolder, odf=True)
        if (resultType in self.templateTypes) and not self.forceOoCall:
            # Simply move the ODT result to the result
            os.rename(resultName, self.result)
        else:
            if resultType not in FILE_TYPES:
                raise PodError(R_TYPE_KO % (self.result, FILE_TYPES.keys()))
            # Call LibreOffice to perform the conversion or document update
            output = self.callLibreOffice(resultName, self.result)
            # I (should) have the result in self.result
            if not os.path.exists(self.result):
                if resultType in self.templateTypes:
                    # In this case LO in server mode could not be called (to
                    # update indexes, sections, etc) but I can still return the
                    # "raw" pod result that exists in "resultName".
                    os.rename(resultName, self.result)
                else:
                    raise PodError(CONV_ERROR % output)
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
