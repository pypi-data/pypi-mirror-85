'''This module defines classes allowing to store an object's history'''

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
# Most of an object's history is related to its workflow. This is why this
# module lies within appy.model.workflow. That being said, object history also
# stores not-workflow-based events like data changes.

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
import persistent
from DateTime import DateTime
from persistent.list import PersistentList
from persistent.mapping import PersistentMapping

from appy.px import Px
from appy.model.batch import Batch
from appy.utils import string as sutils

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class EventIterator:
    '''Iterator for history events'''

    def __init__(self, history, eventType=None, condition=None,
                 context=None, chronological=False, i=None):
        # The history containing the events to walk
        self.history = history
        # The types of events to walk. None means that all types are walked.
        # When specified, p_eventType must be the name of a concrete Event
        # class, or a list/tuple of such class names.
        self.eventType = (eventType,) if isinstance(eventType, str) \
                                      else eventType
        # An additional condition, as a Python expression (getting "event" in
        # its context) that will dismiss the event if evaluated to False.
        self.condition = condition
        # A context that will be given to the condition
        self.context = context
        # If chronological is True, events are walked in chronological order.
        # Else, they are walked in their standard, anti-chronological order.
        self.chronological = chronological
        # The index of the currently walked event
        if i is None:
            self.i = len(history) - 1 if chronological else 0
        else:
            self.i = i

    def increment(self):
        '''Increment p_self.i, or decrement it if we walk events in
           chronological order.'''
        if self.chronological:
            self.i -= 1
        else:
            self.i += 1

    def typeMatches(self, event):
        '''Has p_event the correct type according to p_self.eventType ?'''
        # If no event type is defined, p_event matches
        if self.eventType is None: return True
        return event.__class__.__name__ in self.eventType

    def conditionMatches(self, event):
        '''Does p_event matches p_self.condition ?'''
        # If no condition is defined, p_event matches
        if self.condition is None: return True
        # Update the evaluation context when appropriate
        if self.context:
            locals().update(context)
        return eval(self.condition)

    def __iter__(self): return self
    def __next__(self):
        '''Return the next matching event'''
        try:
            event = self.history[self.i]
        except IndexError:
            # There are no more events, we have walked them all
            raise StopIteration
        # Does this event match ?
        if self.typeMatches(event) and self.conditionMatches(event):
            # Yes
            self.increment()
            return event
        else:
            # Try to return the next element
            self.increment()
            return self.__next__()

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Event(persistent.Persistent):
    '''An object's history is made of events'''
    # A format for representing dates at various (non ui) places
    dateFormat = '%Y/%m/%d %H:%M'

    # Some events can be deleted from the ui, but most aren't
    deletable = False

    # The PX displaying details about an event (basically the event's comment)
    pxDetail = Px('''
     <x var="eventId=event.getId()">
      <img if="event.mayEditComment(config, user, isManager)"
           class="clickable iconS" style="float:right" src=":url('edit.svg')"
           title=":_('object_edit')"
           onclick=":'onHistoryEvent(%s,%s,%s,%s)' % \
                    (q('Edit'), q(o.iid), q(event.date), q(eventId))"/>
      <span id=":eventId">::event.getComment()</span>
     </x>''')

    def __init__(self, login, state, date, comment=None):
        # The login of the user that has triggered the event
        self.login = login
        # The name of the state into which the object is after the event
        # occurred. It means that an object's current state is stored in this
        # attribute, on the most recent event in its history.
        self.state = state
        # When did this event occur ?
        self.date = date
        # A textual optional comment for the event
        self.comment = comment

    def clone(self):
        '''Create an return a clone from myself'''
        params = self.__dict__.copy()
        login = params.pop('login')
        state = params.pop('state')
        date = params.pop('date')
        return self.__class__(login, state, date, **params)

    def completeComment(self, comment, sep='<br/><br/>'):
        '''Appends p_comment to the existing p_self.comment'''
        if not self.comment:
            self.comment = comment
        else:
            self.comment =  '%s%s%s' % (self.comment, sep, comment)

    def getTypeName(self):
        '''Return the class name, possibly completed with sub-class-specific
           information.'''
        return self.__class__.__name__

    def getLabel(self, o):
        '''Returns the i18n label for this event'''
        # To be overridden

    def getComment(self, empty='-'):
        '''Returns the formatted version of p_self.comment'''
        comment = self.comment
        if not comment: return empty
        return sutils.formatText(comment)

    def mayEditComment(self, config, user, isManager):
        '''May p_user edit the comment on this event ?'''
        if not config.model.editHistoryComments: return
        return isManager or (user.login == self.login)

    def getId(self):
        '''Return an ID for this history p_event, based on its date.'''
        return str(self.date.millis())

    def __repr__(self):
        '''String representation'''
        date = self.date.strftime(Event.dateFormat)
        return '<%s by %s on %s, state %s>' % \
               (self.getTypeName(), self.login, date, self.state)

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Trigger(Event):
    '''This event represents a transition being triggered'''

    def __init__(self, login, state, date, **params):
        # Extract the name of the transition from p_params
        self.transition = params.pop('transition')
        Event.__init__(self, login, state, date, **params)

    def getTypeName(self):
        '''Return the class name and the transition name'''
        return 'Trigger %s' % self.transition

    def getLabel(self, o):
        '''Returns the label for the corresponding transition'''
        if self.transition == '_init_':
            r = 'Base_creator'
        else:
            transition = o.getWorkflow().transitions.get(self.transition)
            r = transition.labelId if transition else self.transition
        return r

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Action(Event):
    '''This event represents an action (field) being performed'''

    def __init__(self, login, state, date, **params):
        # Extract the name of the action from p_params
        self.action = params.pop('action')
        Event.__init__(self, login, state, date, **params)

    def getTypeName(self):
        '''Return the class name and the transition name.'''
        return 'Action %s' % self.action

    def getLabel(self, o):
        '''Returns the label for the corresponding action'''
        return o.getField(self.action).labelId

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Change(Event):
    '''This event represents a data change'''

    # Due to the mess sometimes occurring within XHTML diffs, it may be
    # preferable to forget about the change by allowing the user to delete the
    # corresponding event.
    deletable = True

    # Types of entries in a diff
    diffEntries = ('insert', 'delete')

    # Showing details about a change = displaying the previous values of the
    # fields whose values were modified in this change.
    pxDetail = Px('''
     <table class="changes" width="100%" if="event.changes">
      <tr>
       <th align=":dleft" width="30%">:_('modified_field')</th>
       <th align=":dleft" width="70%">:_('previous_value')</th>
      </tr>
      <tr for="name, value in event.changes.items()" valign="top"
          var2="fname=name if isinstance(name, str) else name[0];
                lg=None if isinstance(name, str) else name[1];
                field=o.getField(fname)">
       <td><x>::_(field.labelId)</x>
           <x if="lg">:' (%s)' % ui.Language.getName(lg)</x></td>
       <td>::value</td>
      </tr>
     </table>''')

    def __init__(self, login, state, date, **params):
        # Extract changed fields from p_params. Attribute "changes" stores, in a
        # dict, the previous values of fields whose values have changed. If the
        # dict's key is of type...
        # ----------------------------------------------------------------------
        # str   | it corresponds to the name of the field;
        # tuple | it corresponds to a tuple (s_name, s_language) and stores the
        #       | part of a multilingual field corresponding to s_language.
        # ----------------------------------------------------------------------
        self.changes = PersistentMapping(params.pop('changes'))
        Event.__init__(self, login, state, date, **params)

    def hasField(self, name, language=None):
        '''Is there, within p_self's changes, a change related to a field whose
           name is p_name ?'''
        if name in self.changes: return True
        # Search for a key of the form (name, language)
        for key in self.changes.keys():
            if isinstance(key, tuple) and (key[0] == name) and \
               (not language or (language == key[1])):
                return True

    def getValue(self, name, language=None):
        '''Gets the value as stored on this change, for field name p_name, or
           its p_language part.'''
        key = (name, language) if language else name
        return self.changes.get(key)

    def getLabel(self, o):
        '''Returns the translated label for a data change'''
        return 'event_Change'

    def getDiffTexts(self, o):
        '''Returns a tuple (insertText, deleteText) containing texts to show on,
           respectively, inserted and deleted chunks of text in a XHTML diff.'''
        user = o.search1('User', login=self.login, secure=False)
        mapping = {'userName': user.getTitle() if user else self.login}
        r = []
        tool = o.tool
        for type in self.diffEntries:
            msg = self.translate('history_%s' % type, mapping=mapping)
            date = tool.formatDate(self.date)
            r.append('%s: %s' % (date, msg))
        return r

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Custom(Event):
    '''Represents a custom event, for which the label is chosen by the
       developer.'''

    def __init__(self, login, state, date, **params):
        # Extract the label to use to name the event
        self.label = params.pop('label')
        Event.__init__(self, login, state, date, **params)

    def getLabel(self, o):
        '''Returns the translated label for a data change'''
        return self.label

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Link(Event):
    '''Represents a link, via a Ref field, between 2 objects. The event is
       stored in the source object's history.'''

    # Although it may seem similar to a Change, it does not inherit from it.
    # Indeed, the complete list of previously linked objects is not stored:
    # instead, the title of the newly linked object is set as comment in this
    # Link event.

    def __init__(self, login, state, date, **params):
        # We may have linked an existing object or a newly created one
        self.addition = params.pop('addition')
        Event.__init__(self, login, state, date, **params)

    def getLabel(self, o):
        '''Returns the translated label for a link'''
        return 'event_%s' % ('Addition' if self.addition else 'Link')

class Unlink(Event):
    '''Represents an object being unlinked from another one via a Ref field'''

    def __init__(self, login, state, date, **params):
        # We may have simply unlinked an object or it may have been deleted
        self.deletion = params.pop('deletion')
        Event.__init__(self, login, state, date, **params)

    def getLabel(self, o):
        '''Returns the translated label for an unlink'''
        return 'event_%s' % ('Deletion' if self.addition else 'Unlink')

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class History(PersistentList):
    '''Object history is implemented as a list, sorted in antichronological
       order, of history events.'''

    # This PX displays history events
    events = Px('''
     <div var="history=o.history;
               batchSize=historyMaxPerPage|req.maxPerPage;
               batch=history.getBatch(o, batchSize);
               isManager=user.hasRole('Manager')"
          if="batch.length" id=":batch.hook">
      <script>:history.getAjaxData(batch)</script>

      <!-- Navigate between history pages -->
      <div align=":dright">:batch.pxNavigate</div>

      <!-- History -->
      <table width="100%" class="history">
       <tr>
        <th align=":dleft">:_('object_action')</th>
        <th align=":dleft">:_('object_author')</th>
        <th align=":dleft">:_('action_date')</th>
        <th align=":dleft">:_('action_comment')</th>
       </tr>
       <tr for="event in batch.objects"
           class=":loop.event.odd and 'even' or 'odd'" valign="top">
        <td><x>:_(event.getLabel(o))</x>
         <img if="isManager and event.deletable" class="clickable iconS"
              src=":url('deleteS.svg')"
              onclick=":'onHistoryEvent(%s,%s,%s)' % \
                        (q('Delete'), q(o.iid), q(event.date))"/></td>
        <td var="creator=o.search1('User', login=event.login)">
         <x>:creator.getTitle() if creator else (event.login or '?')</x></td>
        <td>:tool.formatDate(event.date)</td>
        <td>:event.pxDetail</td>
       </tr>
      </table>
     </div>''')

    view = Px('''
     <div if="not o.isTemp()"
       var2="history=o.history; hasHistory=not history.isEmpty()">
      <table width="100%" class="header" cellpadding="0" cellspacing="0">
       <tr>
        <td colspan="2" class="by">
         <!-- Creator and last modification date -->
         <x>:_('Base_creator')</x> 
          <x>:user.getTitleFromLogin(o.creator)</x> 

         <!-- Creation and last modification dates -->
         <x>:_('Base_created')</x> 
         <x var="created=o.created; modified=o.modified">
          <x>:tool.Date.format(tool, created, withHour=True)</x>
          <x if="modified != created">&mdash;
           <x>:_('Base_modified')</x>
           <x>:tool.Date.format(tool, modified, withHour=True)</x>
          </x>
         </x>

         <!-- State -->
         <x> &mdash; <x>:_('Base_state')</x> : 
            <b>:_(o.getLabel(o.state, field=False))</b></x>
        </td>
       </tr>

       <!-- History entries -->
       <tr if="hasHistory"><td colspan="2">:history.events</td></tr>
      </table>
     </div>''',

     css='''
      .header { margin-bottom: 5px; background-color: #f3f3f7;
                border: 3px solid white }
      .by { padding: 7px }
      .history td { padding: 8px }
      .history th { font-style: italic; text-align: left; padding: 10px 5px;
                    background-color: white }
      .changes { margin: 4px 0 }
      .changes td, .changes th { border: 1px solid #e0e0e0 }
     ''')

    def __init__(self, o):
        PersistentList.__init__(self)
        # A reference to the object for which p_self is the history
        self.o = o
        # The last time the object has been modified
        self.modified = None

    def add(self, type, state=None, **params):
        ''''Adds a new event of p_type (=the name one an Event sub-class into
            the history.'''
        # Get the login of the user performing the action
        if 'login' in params:
            login = params.pop('login')
        else:
            login = self.o.user.login
        # Get the date and time of the action
        if 'date' in params:
            date = params.pop('date')
        else:
            date = DateTime()
        # For a trigger event, p_state is the new object state after the
        # transition has been triggered. p_state is a name (string) and not a
        # State instance. The name of the triggering transition must be in
        # p_params, at key "transition".
        # For a change event, no state is given, because there is no state
        # change, but we will copy, on the change event, the state from the
        # previous event. That way, the last event in the history will always
        # store the object's current state.
        state = state or self[0].state
        # Create the event
        event = eval(type)(login, state, date, **params)
        # Insert it at the first place within the anti-chronological list
        self.insert(0, event)
        # Initialise self.modified if still None
        if self.modified is None: self.modified = event.date
        return event

    def iter(self, **kwargs):
        '''Returns an iterator for browsing p_self's events'''
        return EventIterator(self, **kwargs)

    def isEmpty(self, name=None):
        '''Is this history empty ? If p_name is not None, the question becomes:
           has p_self.o an history for field named p_name ?'''
        # An history containing a single entry is considered empty: this is the
        # special _init_ virtual transition representing the object creation.
        if len(self) == 1: return True
        # At this point, the complete history can be considered not empty
        if name is None: return
        # Check if history is available for field named p_name
        empty = True
        for event in self.iter(eventType='Change', \
                               condition="event.hasField('%s')" % name):
            # If we are here, at least one change concerns the field
            empty = False
            break
        return empty

    def getCurrentValues(self, o, fields):
        '''Called before updating p_o, this method remembers, for every
           historized field from p_fields, its current value.'''
        r = {} # ~{s_fieldName: currentValue}~
        # p_fields can be a list of fields or a single field
        fields = fields if isinstance(fields, list) else [fields]
        # Browse fields
        for field in fields:
            if not field.getAttribute(o, 'historized'): continue
            r[field.name] = field.getValue(o)
        return r

    def historize(self, previous):
        '''Records, in self.o's history, potential changes on historized fields.
           p_previous contains the values, before an update, of the historized
           fields, while p_self.o already contains the (potentially) modified
           values.'''
        o = self.o
        # Remove, from p_previous, any value that was not changed
        for name in list(previous.keys()):
            prev = previous[name]
            field = o.getField(name)
            curr = field.getValue(o)
            if (prev == curr) or ((prev is None) and (curr == '')) or \
               ((prev == '') and (curr is None)):
                del(previous[name])
                continue            
            # The previous value may need to be formatted
            field.updateHistoryValue(o, previous)
        # Add the entry in the history (if not empty)
        if previous:
            self.add('Change', changes=previous)

    def getEvents(self, type, notBefore=None):
        '''Gets a subset of history events of some p_type. If specified, p_type
           must be the name of a concrete Event class or a list/tuple of such
           names.'''
        cond = 'not notBefore or (event.date >= notBefore)'
        return [event for event in self.iter(eventType=type, condition=cond, \
                                             context={'notBefore':notBefore})]

    def setEvents(self, other):
        '''Replace p_self's events with clones from p_other's events'''
        # Empty p_self's history first
        while len(self): del(self[0])
        # Create clones from p_other's events and insert them into p_self
        for event in other:
            self.append(event.clone())

    def getBatch(self, o, size):
        '''Returns the Batch instance allowing to navigate within p_o's
           history.'''
        # Compute the batch start and size
        size = int(size) if isinstance(size, str) else (size or 30)
        start = int(o.req.start or 0)
        return Batch(objects=self.data[start:start + size], total=len(self),
                     size=size, start=start, hook='history')

    def getAjaxData(self, batch):
        '''Gets data allowing to ajax-ask paginated history data'''
        params = {'start': batch.start, 'maxPerPage': batch.size}
        # Convert params into a JS dict
        params = sutils.getStringFrom(params)
        hook = batch.hook
        return "new AjaxData('%s/history/events','GET',%s,'%s')" % \
               (self.o.url, params, hook)

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
