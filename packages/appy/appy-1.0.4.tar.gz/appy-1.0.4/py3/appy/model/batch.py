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
from appy.utils import string as sutils

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Batch:
    '''Represents a list of objects being part of a wider list, ie:
        * page 2 displaying objects 30 to 60 from a search matching 1110
          results;
        * page 1 displaying objects 0 to 20 from a list of 43 referred objects.
    '''
    def __init__(self, objects=None, total=0, size=30, start=0, hook=None):
        # The objects being part of this batch
        self.objects = objects
        # The effective number of objects in this batch
        self.length = len(objects) if objects is not None else 0
        # The total number of objects from which this batch is only a part of
        self.total = total
        # The normal size of a batch. If p_size is None, all objects are shown.
        # "length" can be less than "size". Example: if total is 12 and batch
        # size is 10, the batch representing objects 0 to 9 will have
        # length=size=10, but the second batch representing objects 10 to 12
        # will have size (3) < length (10).
        self.size = size
        # The index of the first object in the current batch
        self.start = start
        # When this batch is shown in the ui, the ID of the DOM node containing
        # the list of objects.
        self.hook = hook

    def setObjects(self, objects):
        '''p_objects may no have been added at construction time'''
        self.objects = objects
        self.length = len(objects)

    # Input field for going to element number x
    pxGotoNumber = Px('''
     <x var2="label=_('goto_number');
              gotoName='%d_%s_goto' % (o.iid, field.name)">
      <span class="discreet" style="padding-left: 5px">:label</span> 
      <input type="text" size=":len(str(total)) or 1" onclick="this.select()"
             onkeydown=":'if (event.keyCode==13) document.getElementById' \
                         '(%s).click()' % q(gotoName)"/><img
             id=":gotoName" name=":gotoName"
             class="clickable" src=":url('gotoNumber')" title=":label"
             onclick=":'gotoTied(%s,%s,this.previousSibling,%s,%s)' % \
                 (q(sourceUrl), q(field.name), total, q(popup))"/></x>''')

    pxNavigate = Px('''
     <x if="batch.total &gt; batch.size"
        var2="hook=q(batch.hook); size=q(batch.size)">

      <!-- Go to the first page -->
      <img if="(batch.start != 0) and (batch.start != batch.size)"
           class="clickable iconS" src=":url('arrows.svg')"
           title=":_('goto_first')" style="transform: rotate(90deg)"
           onclick=":'askBunch(%s,%s,%s)'% (hook, q(0), size)"/>

      <!-- Go to the previous page -->
      <img var="sNumber=batch.start - batch.size" if="batch.start != 0"
           class="clickable iconS" src=":url('arrow.svg')"
           title=":_('goto_previous')" style="transform: rotate(90deg)"
           onclick=":'askBunch(%s,%s,%s)' % (hook, q(sNumber), size)"/>

      <!-- Explain which elements are currently shown -->
      <span class="navText"> 
       <x>:batch.start + 1</x> <img src=":url('to')"/> 
       <x>:batch.start + batch.length</x> <span class="navSep">//</span> 
       <x>:batch.total</x>
      </span>

      <!-- Go to the next page -->
      <img var="sNumber=batch.start + batch.size" if="sNumber &lt; batch.total"
           class="clickable iconS" src=":url('arrow.svg')"
           title=":_('goto_next')" style="transform: rotate(270deg)"
           onclick=":'askBunch(%s,%s,%s)' % (hook, q(sNumber), size)"/>

      <!-- Go to the last page -->
      <img var="lastPageIsIncomplete=batch.total % batch.size;
                nbOfCompletePages=int(batch.total / batch.size);
                nbOfCountedPages=lastPageIsIncomplete and \
                                 nbOfCompletePages or nbOfCompletePages-1;
                sNumber= nbOfCountedPages * batch.size"
           if="(batch.start != sNumber) and \
               (batch.start != (sNumber-batch.size))"
           class="clickable iconS" src=":url('arrows.svg')"
           title=":_('goto_last')" style="transform: rotate(270deg)"
           onclick=":'askBunch(%s,%s,%s)' % (hook, q(sNumber), size)"/>

      <!-- Go to the element number... -->
      <x var="gotoNumber=gotoNumber|False" if="gotoNumber"
         var2="sourceUrl=o.url; total=batch.total">:batch.pxGotoNumber</x>
     </x>''')

    def store(self, search):
        '''Returns the Javascript code allowing to store objects from this batch
           in the browser's session storage.'''
        # Get the key at which we will store object IDs in the local storage
        key = search.getSessionKey()
        # Get the dict of IDs to store ~{i_index:i_id}~
        i = self.start
        value = {}
        for o in self.objects:
            value[i] = o.iid
            i += 1
        value = sutils.getStringFrom(value)
        return "sessionStorage.setItem('%s',JSON.stringify(%s))" % (key, value)

    def __repr__(self):
        '''String representation'''
        data = 'start=%d,length=%d,size=%s,total=%d' % \
               (self.start, self.length, self.size, self.total)
        if self.hook: data = 'hook=%s,%s' % (self.hook, data)
        return '<Batch %s>' % data
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
