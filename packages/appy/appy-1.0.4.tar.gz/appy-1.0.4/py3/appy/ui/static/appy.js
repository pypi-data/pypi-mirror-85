var lsTimeout,  // Timout for the live search
    podTimeout; // Timeout for checking status of pod downloads

// Builds the URL to a static resource named p_name
function buildUrl(name) { return siteUrl + '/static/appy/' + name; }

// Compute a chunk of XHTML code containing a "loading" animated icon
function loading(name, icon) {
 // Get the name of the icon to use: p_icon or a default one, based on p_name
 if (!icon) icon = 'loading_' + name + '.gif';
 var img = `<img src="${buildUrl(icon)}"`, r=null;
 if      (name == 'link')   r = `${img}/>`;
 else if (name == 'button') r = `${img} align="center"/>`;
 else if (name == 'icon')   r = `${img} align="center"/>`;
 else if (name == 'zone')   r = `<div align="center">${img}/></div>`;
 return r
}

// Add to form p_f a hidden field named p_name with this p_value
function addFormField(f, name, value) {
  // If a field named p_name already exists, simply set its value to p_value
  if (name in f.elements) {
    f.elements[name].value = value;
    return;
  }
  var field = document.createElement('input');
  field.setAttribute('type', 'hidden');
  field.setAttribute('name', name);
  field.setAttribute('value', value);
  f.appendChild(field);
}

// Function for performing a HTTP POST request
function post(action, params, target) {
  // Create a form object
  var f = document.createElement('form');
  f.setAttribute('action', action);
  f.setAttribute('method', 'post');
  if (target) f.setAttribute('target', target);
  // Create a (hidden) field for every parameter
  for (var key in params) addFormField(f, key, params[key]);
  document.body.appendChild(f);
  f.submit();
}

function quote(s) { return '\'' + s + '\''}

// Convert HTML text, containing entities and "br" tags, to pure text
function html2text(v) {
  var r = v.replace(/<br\/?>/g, '\n').replace('&amp;', '&');
  return r.replace('&lt;', '<').replace('&gt;', '>')
}

function toggleLoginBox(show) {
  // Hide/show the login icon
  var loginIcon = document.getElementById('loginIcon');
  loginIcon.style.display = (show)? 'none': 'inline';
  // Show/hide the login box
  var loginBox = document.getElementsByClassName('loginBox')[0];
  loginBox.style.display = (show)? 'block': 'none';
}

function goto(url) { window.location = url }
function len(dict) {
  var res = 0;
  for (var key in dict) res += 1;
  return res;
}

var isIe = (navigator.appName == "Microsoft Internet Explorer");

function getElementsHavingName(tag, name, forceTop) {
  if (!isIe) {
    var r = window.document.getElementsByName(name);
    if ((r.length == 0) && forceTop) {
      r = window.top.document.getElementsByName(name);
    }
    return r;
  }
  else {
    var elems = window.document.getElementsByTagName(tag),
        r = new Array(), nameAttr;
    if ((elems.length == 0) && forceTop) {
      elems = window.top.document.getElementsByTagName(tag);
    }
    for (var i=0; i<elems.length; i++) {
      nameAttr = elems[i].attributes['name'];
      if (nameAttr && (nameAttr.value == name)) r.push(elems[i]);
    }
    return r;
  }
}

// AJAX machinery
var xhrObjects = new Array(); // An array of XMLHttpRequest objects
function XhrObject() { // Wraps a XmlHttpRequest object
  this.freed = 1; // Is this xhr object already dealing with a request or not?
  this.xhr = false;
  this.xhr = new XMLHttpRequest();
  this.hook = '';  /* The ID of the HTML element in the page that will be
                      replaced by result of executing the Ajax request. */
  this.onGet = ''; /* The name of a Javascript function to call once we
                      receive the result. */
  this.info = {};  /* An associative array for putting anything else */
}

/* When inserting HTML at some DOM node in a page via Ajax, scripts defined in
   this chunk of HTML are not executed. This function, typically used as "onGet"
   param for the askAjaxChunk function below, will evaluate those scripts. */
function evalInnerScripts(xhrObject, hookElem) {
  if (!hookElem) return;
  var scripts = hookElem.getElementsByTagName('script');
  for (var i=0; i<scripts.length; i++) eval(scripts[i].innerHTML);
}

function injectChunk(elem, content, inner, searchTop){
  var res = elem;
  if (!isIe || (elem.tagName != 'TABLE')) {
    if (inner) res.innerHTML = content;
    else {
      // Replace p_elem with a new node filled with p_content and return it
      if ((elem.tagName == 'TR') && (content.substr(0,3) != '<tr')) {
        /* Replace the whole table instead of the current row: it is probably
           an error page. */
        elem = elem.parentNode.parentNode;
      }
      var id = elem.id;
      if (id && searchTop) id = ':' + id;
      elem.outerHTML = content;
      if (id) res = getNode(id); // Get the new element
    }
  }
  else {
    /* IE doesn't want to replace content of a table. Force it to do so via
       a temporary DOM element. */
    var temp = document.createElement('div');
    temp.innerHTML = content;
    temp.firstChild.id = elem.id;
    elem.parentNode.replaceChild(temp.firstChild, elem);
  }
  return res;
}

function getNode(id, forceTop) {
  /* Gets the DOM node whose ID is p_id. If p_id starts with ':', we search
     the node in the top browser window, not in the current one that can be
     an iframe. If p_forceTop is true, even if p_id does not start with ':',
     if the node is not found, we will search in the top browser window. */
  if (!id) return;
  var container = window.document,
      startIndex = 0;
  if (id[0] == ':') {
    container = window.top.document;
    startIndex = 1;
  }
  var nodeId = id.slice(startIndex),
      res = container.getElementById(nodeId);
  if (!res && forceTop) res = window.top.document.getElementById(nodeId);
  return res;
}

function getAjaxChunk(pos) {
  // This function is the callback called by the AJAX machinery (see function
  // askAjaxChunk below) when an Ajax response is available.
  // First, find back the correct XMLHttpRequest object
  var rq = xhrObjects[pos];
  if ( (typeof(rq) != 'undefined') && (rq.freed == 0)) {
    if ((!rq.hook) || (rq.xhr.readyState != 4)) return;
    // We have received the HTML chunk
    var hookElem = getNode(rq.hook);
    if (hookElem) {
      var content = rq.xhr.responseText,
          searchTop = rq.hook[0] == ':',
          injected = injectChunk(hookElem, content, false, searchTop);
      // Call a custom Javascript function if required
      if (rq.onGet) rq.onGet(rq, injected);
      // Refresh the whole page if requested
      var goto = rq.xhr.getResponseHeader('Appy-Redirect');
      if (goto) window.top.location = goto;
      // Display the Appy message if present
      var msg = readCookie('AppyMessage');
      if (msg) { showAppyMessage(msg); createCookie('AppyMessage', ''); }
    }
    rq.freed = 1;
  }
}

// Displays the waiting icon when an ajax chunk is asked
function showPreloader(hook, waiting) {
  /* p_hook may be null if the ajax result would be the same as what is
     currently shown, as when inline-editing a rich text field). */
  if (!hook || (waiting == 'none')) return;
  // What waiting icon to show ?
  if (!waiting) waiting = 'loading_big.gif';
  injectChunk(getNode(hook), loading('zone', waiting), true);
}

function askAjaxChunk(url, mode, params, hook, beforeSend, onGet, waiting) {
  /* Ask a chunk of XHTML on the server at p_url, through a XMLHttpRequest.
     p_mode can be 'GET' or 'POST'. URL parameters or form data can be specified
     in associative array p_params.

     p_hook is the ID of the XHTML node that will be filled with the XHTML
     result from the server. If it starts with ':', we will find the node in
     the top browser window and not in the current one (that can be an iframe).
     If it starts with '*', it is the name of a key in the session storage, the
     request will be synchronous and its result, expected to be JSON, will be
     stored in the session storage at this key.

     p_beforeSend is a Javascript function to call before sending the request.
     This function will get 2 args: the XMLHttpRequest object and the p_params.
     This method can return, in a string, additional parameters to send, ie:
     "&param1=blabla&param2=blabla".

     p_onGet is a Javascript function to call when we will receive the answer.
     This function will get 2 args, too: the XMLHttpRequest object and the
     HTML node element into which the result has been inserted.

     p_waiting is the name of the animated icon that will be shown while waiting
     for the ajax result. If null, it will be "loading_big.gif". Other values
     can be "loading_link.gif", "loading_button.gif" or "loading_icon.gif".
     If string "none" is passed, there will be no icon at all.
  */
  // First, get a non-busy XMLHttpRequest object
  var sync = hook[0] == '*', pos = -1;
  for (var i=0; i < xhrObjects.length; i++) {
    if (xhrObjects[i].freed == 1) { pos = i; break; }
  }
  if (pos == -1) {
    pos = xhrObjects.length;
    xhrObjects[pos] = new XhrObject();
  }
  xhrObjects[pos].hook = hook;
  xhrObjects[pos].onGet = onGet;
  if (xhrObjects[pos].xhr) {
    var rq = xhrObjects[pos];
    rq.freed = 0;
    // Construct parameters
    var allParams = ['ajax=True'], value = null;
    if (params) {
      for (var name in params) {
        value = params[name];
        if (typeof val == 'string') value = value.replace('+', '%2B');
        allParams.push(name + '=' + value);
      }
    }
    allParams = allParams.join('&');
    // Call beforeSend if required
    if (beforeSend) {
       var res = beforeSend(rq, params);
       if (res) allParams = allParams + res;
    }
    // Build the URL to call
    var urlFull = url;
    if (mode == 'GET') {
      urlFull = urlFull + '?' + allParams;
    }
    // Display the pre-loader when appropriate
    if (!sync) showPreloader(rq.hook, waiting);
    // Perform the asynchronous HTTP GET or POST
    rq.xhr.open(mode, urlFull, !sync);
    if (mode == 'POST') { // Set the correct HTTP headers
      rq.xhr.setRequestHeader('Content-Type',
                              'application/x-www-form-urlencoded');
    }
    else { allParams = null; }
    // For an asynchronous request, define the callback function
    if (!sync) rq.xhr.onreadystatechange = function(){ getAjaxChunk(pos); }
    // Perform the HTTP request
    rq.xhr.send(allParams);
    // Manage a sync request
    if (sync) {
      sessionStorage.setItem(hook.substr(1), rq.xhr.responseText);
      rq.freed = 1;
    }
  }
}

// Object representing all the data required to perform an Ajax request
function AjaxData(url, mode, params, hook, parentHook, beforeSend, onGet) {
  this.url = url;
  this.mode = (!mode)? 'GET': mode;
  this.params = params;
  this.hook = hook;
  /* If a parentHook is specified, this AjaxData must be completed with a parent
     AjaxData instance. */
  this.parentHook = parentHook;
  this.beforeSend = beforeSend;
  this.onGet = onGet;
  // Inject this AjaxData instance into p_hook
  getNode(hook, true)['ajax'] = this;
  if (params && ('criteria' in params)) {
    // Remember these search criteria in the browser's session
    sessionStorage.setItem(params['className'], params['criteria']);
  }
}

function askAjax(hook, form, params, waiting) {
  /* Call askAjaxChunk by getting an AjaxData instance from p_hook, a
      potential action from p_form and additional parameters from p_param. */
  var d = getNode(hook)['ajax'];
  // Complete data with a parent data if present
  if (d['parentHook']) {
    var parentHook = d['parentHook'];
    if (hook[0] == ':') parentHook = ':' + parentHook;
    var parent = getNode(parentHook)['ajax'];
    for (var key in parent) {
      if (key == 'params') continue; // Will get a specific treatment herafter
      if (!d[key]) d[key] = parent[key]; // Override if no value on child
    }
    // Merge parameters
    if (parent.params) {
      for (var key in parent.params) {
        if (key in d.params) continue; // Override if not value on child
        d.params[key] = parent.params[key];
      }
    }
  }
  // Resolve dynamic parameter "cbChecked" if present
  if ('cbChecked' in d.params) {
    var cb = getNode(d.params['cbChecked'], true);
    if (cb) d.params['cbChecked'] = (cb.checked)? 'True': 'False';
    else delete d.params['cbChecked'];
  }
  // Convert the "filter" dict into a string when present
  if ('filters' in d.params) {
    d.params['filters'] = stringFromDict(d.params['filters']);
  }
  // If a p_form id is given, integrate the form submission in the ajax request
  if (form) {
    var f = document.getElementById(form),
        mode = 'POST',
        action = f.action,
        saction = f.getAttribute('data-sub');
    /* Deduce the action from the form action, either via custom field
       "action-sub", already containing the correct action sub-path, or by
       extracting it from the "action" field. */
    if (saction) d.params['action'] = saction;
    else if (action != 'none'){
      var i = (action.indexOf('@') == -1)? 3: 4,
          parts = _rsplit(action, '/', i).slice(1);
      d.params['action'] = parts.join('*');
    }
    // Get the other params
    var name, value, elems = f.elements;
    for (var i=0; i < elems.length; i++) {
      // Ignore unnamed  form elements
      name = elems[i].name;
      if (!name) continue;
      // Escape the value when relevant
      value = elems[i].value;
      if (name == 'popupComment') value = encodeURIComponent(value);
      d.params[name] = value;
    }
  }
  else var mode = d.mode;
  // Get p_params if given. Note that they override anything else.
  if (params) {
    if ('mode' in params) { mode = params['mode']; delete params['mode'] };
    for (var key in params) d.params[key] = params[key];
  }
  askAjaxChunk(d.url, mode, d.params, hook, d.beforeSend, evalInnerScripts,
               waiting);
}

function askBunch(hook, start, maxPerPage) {
  var params = {'start': start};
  if (maxPerPage) params['maxPerPage'] = maxPerPage;
  askAjax(hook, null, params);
}

function askBunchSorted(hook, sortKey, sortOrder) {
  var data = {'start': '0', 'sortKey': sortKey, 'sortOrder': sortOrder};
  askAjax(hook, null, data);
}

function askBunchFiltered(hook, filterKey) {
  var filter = document.getElementById(hook + '_' + filterKey),
      // Get the filter value
      value = filter.value;
  if (value && (filter.nodeName == 'INPUT')) {
    // Remove reserved chars and ensure it contains at least 3 chars
    value = encodeURIComponent(value.trim()).replace(',','').replace(':','');
    if (value.length < 3) {
      filter.style.background = wrongTextInput;
      return;
    }
  }
  // Add this (key,value) pair to filters
  getNode(hook)['ajax'].params['filters'][filterKey] = value;
  var data = {'start': '0'};
  askAjax(hook, null, data);
}

function askBunchMove(hook, start, id, move){
  var moveTo = move;
  if (typeof move == 'object'){
    // Get the new index from an input field
    var inputId = move.id;
    inputId = inputId.substr(0, inputId.length-4) + '_v';
    var input = document.getElementById(inputId);
    if (isNaN(input.value)) {
      input.style.background = wrongTextInput;
      return;
    }
    moveTo = 'index_' + input.value;
  }
  var data = {'start': start, 'action': 'moveObject', 'tiedId': id,
              'move': moveTo};
  askAjax(hook, null, data);
}

function askBunchSortRef(hook, start, sortKey, reverse) {
  var data = {'start': start, 'action': 'sort', 'sortKey': sortKey,
              'reverse': reverse};
  askAjax(hook, null, data);
}

function askBunchSwitchColset(hook, colset) {
  askAjax(hook, null, {'colset': colset});
}

function askBunchSwitchSearch(hook, name, searchName) {
  var params = {}, key = name + '_view';
  params[key] = searchName;
  askAjax(hook, null, params);
}

function clickOn(node) {
  if (!node) return;
  // If node is a form, disable all form buttons
  if (node.tagName == 'FORM') {
    var i = node.elements.length -1;
    while (i >= 0) {
      if (node.elements[i].type == 'button') { clickOn(node.elements[i]); }
      i = i - 1;
    }
    return;
  }
  // Disable any click on p_node to be protected against double-click
  var cn = (node.className)? 'unclickable ' + node.className : 'unclickable';
  node.className = cn;
  /* For a button, show the preloader directly. For a link, show it only after
     a while, if the target page is still not there. */
  if (node.tagName == 'A') {
    setTimeout(function(){injectChunk(node, loading('link'))}, 700);}
  else {
    var name = (cn.search('buttonIcon') == -1)? 'button' : 'icon';
    injectChunk(node, loading(name));
  }
}

function gotoTied(objectUrl, field, numberWidget, total, popup) {
  // Check that the number is correct
  try {
    var number = parseInt(numberWidget.value);
    if (!isNaN(number)) {
      if ((number >= 1) && (number <= total)) {
        goto(objectUrl + '/' + field + '/gotoTied?number=' + number +
             '&popup=' + popup);
      }
      else numberWidget.style.background = wrongTextInput; }
    else numberWidget.style.background = wrongTextInput; }
  catch (err) { numberWidget.style.background = wrongTextInput; }
}

function askField(hook, url, layout, customParams, showChanges, className,mode){
  // Sends an Ajax request for getting the content of any field
  var fieldName = hook.split('_').pop(),
      // layout may define a host layout
      layouts = layout.split(':'),
      params = {'layout': layouts[0], 'showChanges': showChanges};
  if (layouts.length > 1) params['hostLayout'] = layouts[1];
  if (customParams){for (var key in customParams) params[key]=customParams[key]}
  url = url + '/' + fieldName + '/pxRender';
  mode = mode || 'GET';
  askAjaxChunk(url, mode, params, hook, null, evalInnerScripts);
}

function askTimeoutField(hook, params) {
  // Ask a custom field possibly tied to a timeout and having specific params
  var node = findNode(this, hook),
      data = node['ajax'];
  if ('timeoutId' in node) clearTimeout(node['timeoutId']);
  if (params) {
    // Complete parameters with those specified on the Ajax node
    if (data.params) {for (var key in data.params) params[key]=data.params[key]}
  }
  else params = data.params;
  askField(hook, data.url, 'view', params);
}

function setTimeoutField(hook, fun, interval){
  // Set a timeout that will call p_fun, containing a call to m_askTimeoutField
  var node = findNode(this, hook);
  node['timeoutId'] = setTimeout(fun, interval);
}

function clearTimeoutField(hook){
  // Stop the timeout corresponding to p_hook
  var node = findNode(this, hook);
  if ('timeoutId' in node) clearTimeout(node['timeoutId']);
}

function doInlineSave(id, name, url, layout, ask, content, language, cancel){
  /* Ajax-saves p_content of field named p_name (or only the part corresponding
     to p_language if the field is multilingual) on object whose id is
     p_id and whose URL is p_url. After saving it, display the field on
     p_layout. Ask a confirmation before doing it if p_ask is true. */
  var doIt = true;
  if (ask) doIt = confirm(save_confirm);
  var params = {'action': 'storeFromAjax', 'layout': layout};
  if (language) params['languageOnly'] = language;
  var hook = id + '_' + name;
  if (!doIt || cancel) params['cancel'] = 'True';
  else { params['fieldContent'] = encodeURIComponent(content) }
  askAjaxChunk(url + '/' + name + '/pxRender', 'POST', params, hook, null,
               evalInnerScripts);
}

// Gets the value to send to the server for ajax-storing it
function getFieldValue(tag) {
  /* When "tag" is a checkbox, we do not get its value from the companion's
     hidden field, because, at the time this function is called, the "click"
     event that updates this value may not have been triggered yet. */
  if (tag.name.endsWith('_visible')) return (tag.checked)? 'True': 'False';
  else return tag.value;
}

// Triggered by some event, it calls doInlineSave when relevant
function performInlineSave(event) {
  var tag = event.target, cancel=false;
  if (tag.tagName == 'IMG') {
    // Get the original tag
    var parts = tag.id.split('_'),
        name = parts[0];
    cancel = parts[1] == 'cancel';
    tag = document.getElementById(name);
  }
  var obj = tag.obj;
  if (obj.done) return;
  if ((event.type == 'keydown') && (event.keyCode != 13)) return; // CR
  obj.done = true;
  doInlineSave(obj.id, obj.name, obj.url, obj.layout, false, getFieldValue(tag),
               null, cancel);
}

function prepareForAjaxSave(id, objectId, objectUrl, layout, name) {
  // Prepare widget whose ID is p_id for ajax-saving its content
  var tag = getNode(id);
  if (!tag) {
    // A widget made of several input fields (radio or checkboxes)
    var tags = document.getElementsByName(id);
    for (var i=0; i<tags.length; i++)
      prepareForAjaxSave(tags[i].id, objectId, objectUrl, layout, id);
    return;
  }
  // Determine the tag type
  var cr = ['checkbox', 'radio'],
      checkable = cr.includes(tag.type),
      isText = tag.type == 'textarea';
  tag.focus();
  // For input, non-text fields, select all content
  if (!checkable && !isText) tag.select();
  /* Store information on this node. Key "done" is used to avoid saving twice
     (saving is attached to events keydown and blur, see below). */
  tag.obj = {id: objectId, url: objectUrl, done: false, name:name || id,
             layout: layout};
  /* If "save" and "cancel" buttons are there, configure them with the
     appropriate event listeners. Else, configure the tag itself. */
  var save = document.getElementById(id + '_save');
  if (save) {
    var cancel = document.getElementById(id + '_cancel');
    save.addEventListener('click', performInlineSave);
    cancel.addEventListener('click', performInlineSave);
  }
  else {
    tag.addEventListener('keydown', performInlineSave);
    if (checkable) tag.addEventListener('change', performInlineSave);
  }
}

// Used by checkbox widgets for having radio-button-like behaviour
function toggleCheckbox(cb) {
  cb.nextSibling.value = (cb.checked)? 'True': 'False';
}

// Toggle visibility of all elements having p_nodeType within p_node
function toggleVisibility(node, nodeType, css){
  var sNode, className, elements = node.getElementsByTagName(nodeType);
  for (var i=0; i<elements.length; i++){
    sNode = elements[i];
    className = sNode.className || '';
    // Ignore nodes having class "css"
    if (!css || className.includes(css)) {
      // Switch node's visibility
      if (sNode.style.visibility == 'hidden') sNode.style.visibility= 'visible';
      else sNode.style.visibility = 'hidden';
    }
  }
}
// Shorthand for toggling clickable images' visibility 
function itoggle(img) {toggleVisibility(img, 'img', 'clickable');}

// JS implementation of Python ''.rsplit
function _rsplit(s, delimiter, limit) {
  var elems = s.split(delimiter),
      exc = elems.length - limit;
  if (exc <= 0) return elems;
  // Merge back first elements to get p_limit elements
  var head = '',
      res = [];
  for (var i=0; i < elems.length; i++) {
    if (exc > 0) { head += elems[i] + delimiter; exc -= 1 }
    else { if (exc == 0) { res.push(head + elems[i]); exc -= 1 }
           else res.push(elems[i]) }
  }
  return res;
}

function getCbDataFromCbName(name) {
  /* Returns a 2-tuple (nodeId, cbType) allowing to find checkboxes-related
     data from the p_name of a given checkbox. cbType can be "objs" or "poss".

     p_name may have several forms:
     - for a search in a popup:      <objId>_<refName>_popup_objs
     - for a ref:                    <objId>_<refName>_<cbType>
     - for a search outside a popup: <searchName>_objs
  */
  var parts = name.split('_'), cbType=parts.pop(), id=parts.join('_');
  return [id, cbType];
}

// (Un)checks a checkbox corresponding to a linked object
function toggleCb(checkbox) {
  var name = checkbox.getAttribute('name'),
      parts = getCbDataFromCbName(name),
      hook = parts[0],
      cbType = parts[1],
      // Get the DOM node storing checkbox-related data
      node = document.getElementById(hook),
      // Get the array storing checkbox statuses
      statuses = node['_appy_' + cbType + '_cbs'],
      // Get the array semantics
      semantics = node['_appy_' + cbType + '_sem'],
      id = checkbox.value;
  if (semantics == 'unchecked') {
    if (!checkbox.checked) statuses[id] = null;
    else {if (id in statuses) delete statuses[id]};
  }
  else { // semantics is 'checked'
    if (checkbox.checked) statuses[id] = null;
    else {if (id in statuses) delete statuses[id]};
  }
}

function findNode(node, id) {
  /* When coming back from the iframe popup, we are still in the context of the
     iframe, which can cause problems for finding nodes. This case can be
     detected by checking node.window. */
  var container = (node.window)? node.window.document: window.parent.document;
  return container.getElementById(id);
}

// Initialise checkboxes of a Ref or Search
function initCbs(id) {
  var parts = getCbDataFromCbName(id),
      hook = parts[0],
      cbType = parts[1],
      // Get the DOM node storing checkbox-related data
      node = getNode(hook, true),
      // Get the array storing checkbox statuses
      statuses = node['_appy_' + cbType + '_cbs'],
      // Get the array semantics
      semantics = node['_appy_' + cbType + '_sem'],
      value = semantics != 'unchecked',
      // Update visible checkboxes
      checkboxes = getElementsHavingName('input', id, true);
  for (var i=0; i < checkboxes.length; i++) {
    if (checkboxes[i].value in statuses) checkboxes[i].checked = value;
    else checkboxes[i].checked = !value;
  }
}

// Toggle all checkboxes of a Ref or Search
function toggleAllCbs(id) {
  var parts = getCbDataFromCbName(id),
      hook = parts[0],
      cbType = parts[1],
      // Get the DOM node storing checkbox-related data
      node = document.getElementById(hook),
      // Empty the array storing checkbox statuses
      statuses = node['_appy_' + cbType + '_cbs'];
  for (var key in statuses) delete statuses[key];
  // Switch the array semantics
  var semAttr = '_appy_' + cbType + '_sem';
  if (node[semAttr] == 'unchecked') node[semAttr] = 'checked';
  else node[semAttr] = 'unchecked';
  // Update the visible checkboxes
  initCbs(id);
}

// Shows/hides a dropdown menu
function toggleDropdown(container, forcedValue){
  var dropdown = container.getElementsByClassName('dropdown')[0];
  // Force to p_forcedValue if specified
  if (forcedValue) {dropdown.style.display = forcedValue}
  else {
    var displayValue = dropdown.style.display;
    if (displayValue == 'block') dropdown.style.display = 'none';
    else dropdown.style.display = 'block';
  }
}

// Functions used for master/slave relationships between widgets
function getSlaveInfo(slave, infoType) {
  // Returns the appropriate info about slavery, depending on p_infoType
  var masterInfo, cssClasses = slave.className.split(' ');
  // Find the CSS class containing master-related info
  for (var j=0; j < cssClasses.length; j++) {
    if (cssClasses[j].indexOf('slave*') == 0) {
      // Extract, from this CSS class, master name or master values
      masterInfo = cssClasses[j].split('*');
      if (infoType == 'masterName') return masterInfo[1];
      else return masterInfo.slice(2); 
    }
  }
}

function getMasterValues(master) {
  // Returns the list of values that p_master currently has
  var res;
  if (master.type == 'checkbox') {
    var value = master.value;
    if (value == 'on') {
      // A single checkbox from a Boolean field
      res = master.checked + '';
      res = res.charAt(0).toUpperCase() + res.substr(1);
      res = [res];
    }
    else {
      // A value from a Select field with render == 'checkbox'
      res = [];
      // "master" is one among several checkboxes. Get them all.
      var checkboxes = document.getElementsByName(master.name);
      for (var i=0; i<checkboxes.length; i++) {
        if (checkboxes[i].checked) res.push(checkboxes[i].value);
      }
    }
  }
  else if (master.type == 'radio') {
    /* Get the selected value among all radio buttons of the group (p_master is
       the first one from this group) */
    var radios = document.getElementsByName(master.name);
    res = [];
    for (var i=0; i < radios.length; i++) {
      if (radios[i].checked) {
        res.push(radios[i].value);
        break;
      }
    }
  }
  else if (master.tagName == 'INPUT') {
    res = master.value;
    if ((res.charAt(0) == '(') || (res.charAt(0) == '[')) {
      // There are multiple values, split it
      var values = res.substring(1, res.length-1).split(',');
      res = [];
      var v;
      for (var i=0; i < values.length; i++){
        v = values[i].replace(' ', '');
        res.push(v.substring(1, v.length-1));
      }
    }
    else res = [res]; // A single value
  }
  else { // SELECT widget
    res = [];
    for (var i=0; i < master.options.length; i++) {
      if (master.options[i].selected) res.push(master.options[i].value);
    }
  }
  return res;
}

function getSlaves(master) {
  // Gets all the slaves of master
  var allSlaves = getElementsHavingName('table', 'slave'),
      res = [],
      masterName = master.attributes['name'].value;
  // Remove leading 'w_' if the master is in a search screen
  if (masterName.indexOf('w_') == 0) masterName = masterName.slice(2);
  if (masterName.endsWith('_visible')) {
    masterName = masterName.replace('_visible', '_hidden');
  }
  var cssClasses, slavePrefix = 'slave*' + masterName + '*';
  for (var i=0; i < allSlaves.length; i++){
    cssClasses = allSlaves[i].className.split(' ');
    for (var j=0; j < cssClasses.length; j++) {
      if (cssClasses[j].indexOf(slavePrefix) == 0) {
        res.push(allSlaves[i]);
        break;
      }
    }
  }
  return res;
}

// Retrieve form values and validation errors in an array
function getFormData() {
  // First, get data from the Appy or search form
  if ((!('appyForm' in document.forms)) &&
      (!('search' in document.forms))) return;
  var r = {},
      appyForm = document.forms['appyForm'] || document.forms['search'],
      elem=null,
      name=null;
  for (var i=0; i < appyForm.elements.length; i++) {
    elem = appyForm.elements[i];
    name = elem.name
    if (name == 'action') continue;
    if (name.startsWith('w_')) name = name.substr(2);
    r[name] = elem.value;
  }
  // Then, add error-related info when present
  if (!errors) return r;
  for (var name in errors) r[name + '_error'] = errors[name];
  return r
}

function updateSlaves(master, slave, objectUrl, layoutType, className, ajax){
  /* Given the value(s) in a master field, we must update slave's visibility or
     value(s). If p_slave is given, it updates only this slave. Else, it updates
     all slaves of p_master. */
  var slaves = (slave)? [slave]: getSlaves(master),
      masterValues = getMasterValues(master),
      slaveryValues;
  for (var i=0; i < slaves.length; i++) {
    slaveryValues = getSlaveInfo(slaves[i], 'masterValues', master.id);
    if (slaveryValues[0] != '+') {
      // Update slaves visibility depending on master values
      var showSlave = false;
      for (var j=0; j < slaveryValues.length; j++) {
        for (var k=0; k < masterValues.length; k++) {
          if (slaveryValues[j] == masterValues[k]) showSlave = true;
        }
      }
      // Is this slave also a master ?
      var subMaster;
      if (!slave) {
        var innerId = slaves[i].id.split('_').pop(),
            innerField = document.getElementById(innerId);
        // Inner-field may be absent (ie, in the case of a group)
        if (innerField && (innerField.className == ('master_' + innerId))) {
          subMaster = innerField;
        }
      }
      // Show or hide this slave
      if (showSlave) {
        // Show the slave
        slaves[i].style.display = '';
        if (subMaster) {
          // Recompute its own slave's visibility
          updateSlaves(subMaster, null, objectUrl, layoutType, className);
        }
      }
      else {
        // Hide the slave
        slaves[i].style.display = 'none';
        if (subMaster && (subMaster.style.display != 'none')) {
          // Hide its own slaves, too
          var subSlaves = getSlaves(subMaster);
          for (var l=0; l < subSlaves.length; l++) {
            subSlaves[l].style.display = 'none';
          }
        }
      }
    }
    else if (ajax) {
      /* Ajax requests are disabled when initializing slaves via m_initSlaves
         below. Update slaves' values depending on master values. */
      var slaveId = slaves[i].id,
          slaveName = slaveId.split('_')[1];
      askField(slaveId, objectUrl, layoutType, getFormData(), false, className,
               'POST');
    }
  }
}

function getMaster(name) {
  // Get the master node from its p_name
  var r = document.getElementById(name);
  // Checkboxes are found by name and not by ID
  if (!r) {
    r = document.getElementsByName(name);
    if (r.length > 0) {
      r = r[0]; // Take the first checkbox from the series
      if ((r.type != 'checkbox') && (r.type != 'radio')) r = null;
    }
    else r = null;
  }
  return r;
}

function initSlaves(objectUrl, layoutType) {
  /* When the current page is loaded, we must set the correct state for all
     slave fields. */
  var slaves = getElementsHavingName('table', 'slave'),
      i = slaves.length -1,
      masterName, master;
  while (i >= 0) {
    masterName = getSlaveInfo(slaves[i], 'masterName');
    master = getMaster(masterName);
    // If master is not here, we can't hide its slaves when appropriate
    if (master) updateSlaves(master,slaves[i],objectUrl,layoutType,null,false);
    i -= 1;
  }
}

function backFromPopup() {
  // Close the iframe popup when required
  var close = readCookie('closePopup');
  if (close == 'no') return;
  // Reset the timer, the cookie and close the popup
  createCookie('closePopup', 'no');
  var popup = closePopup('iframePopup'),
      timer = popup.popupTimer;
  clearInterval(timer);
  if (close != 'yes') {
    // We must load a specific URL in the main page
    window.parent.location = atob(close.slice(1,-1));
  }
  else {
    // We must ajax-refresh, on the main page, the node as defined in the popup
    var nodeId = popup['back'];
    if (nodeId && getNode(':' + nodeId)) askAjax(':' + nodeId);
    else window.parent.location = window.parent.location;
  }
}

function setChecked(f, checkHook) {
  f.checkedIds.value = '';
  f.checkedSem.value = '';
  // Retrieve, on form p_f, the status of checkboxes from p_checkHook
  if (checkHook) {
    // Collect selected objects possibly defined in this hook
    var node = document.getElementById(checkHook);
    if (node && node.hasOwnProperty('_appy_objs_cbs')) {
      f.checkedIds.value = stringFromDict(node['_appy_objs_cbs'], true);
      f.checkedSem.value = node['_appy_objs_sem'];
    }
  }
}

function submitForm(formId, msg, showComment, back, checkHook, visible) {
  var f = document.getElementById(formId);
  // Initialise the status of checkboxes when appropriate
  if (checkHook) setChecked(f, checkHook);
  if (!msg) {
    /* Submit the form and either refresh the entire page (back is null)
       or ajax-refresh a given part only (p_back corresponds to the id of the
       DOM node to be refreshed. */
    if (back) { askAjax(back, formId); }
    else {
      f.submit();
      if (!visible) clickOn(f);
    }
  }
  else {
    // Ask a confirmation to the user before proceeding
    if (back) {
      var js = "askAjax('" + back + "', '" + formId + "');";
      askConfirm('form-script', formId + '+' + js, msg, showComment,
                 null, null, null, null, visible); }
    else askConfirm('form', formId, msg, showComment,
                    null, null, null, null, visible);
  }
}

function onDeleteObject(objectUrl, back) {
  if (back) {} // Todo
  else askConfirm('url', objectUrl + '/remove', action_confirm);
}

function onHistoryEvent(action, objectId, eventTime, commentId) {
  var f = document.getElementById('eventForm'),
      showComment = action == 'Edit',
      comment = null;
  f.action = 'on' + action + 'Event';
  f.objectId.value = objectId;
  f.eventTime.value = eventTime;
  // Manage comment
  if (commentId) {
    comment = html2text(document.getElementById(commentId).innerHTML);
  }
  askConfirm('script', "askAjax('appyHistory','" + f.id +
             "',{'comment':encodeURIComponent(comment)})",
             action_confirm, showComment, null, null, comment);
}

function onLink(action, url, fieldName, targetId, hook, start, semantics) {
  var params = {'linkAction': action, 'targetId': targetId};
  if (hook) params[hook + '_start'] = start;
  if (semantics) params['semantics'] = semantics;
  post(url + '/' + fieldName + '/onLink', params);
}

function onLinkMany(action, url, id, start) {
  var parts = getCbDataFromCbName(id),
      hook = parts[0],
      cbType = parts[1],
      // Get the DOM node corresponding to the Ref
      node = document.getElementById(hook),
      // Get the ids of (un-)checked objects
      statuses = node['_appy_' + cbType + '_cbs'],
      ids = stringFromDict(statuses, true),
      // Get the array semantics
      semantics = node['_appy_' + cbType + '_sem'];
  // Show an error message if no element is selected
  if ((semantics == 'checked') && (len(statuses) == 0)) {
    openPopup('alertPopup', no_elem_selected);
    return;
  }
  // Ask for a confirmation
  var sep = ',', elems=hook.split('_'), fieldName=elems.pop();
  askConfirm('script', 'onLink(' + quote(action + '_many') + sep +
             quote(url) + sep + quote(fieldName) + sep + quote(ids) + sep +
             quote(id) + sep + quote(start) + sep + quote(semantics) + ')',
             action_confirm);
}

function onAdd(direction, addForm, objectId) {
  // p_direction can be "before" or "after"
  var f = document.getElementById(addForm);
  f.insert.value = direction + '.' + objectId;
  f.submit();
}

function stringFromDict(d, keysOnly) {
  /* Gets a comma-separated string form dict p_d. If p_keysOnly is True, only
     keys are dumped. Else, "key:value" pairs are included. */
  var elem, res = [];
  for (var key in d) {
    elem = (keysOnly)? key: key + ':' + d[key];
    res.push(elem);
  }
  return res.join();
}

function updateFileNameStorer(field, storer) {
  // Get the storer
  var storer = document.getElementById(storer);
  if (!storer || storer.value) return;
  // Remove file path and extension
  var name = field.value;
  name = name.substr(name.lastIndexOf('\\')+1);
  var i = name.lastIndexOf('.');
  if (i != -1) name = name.substring(0, i);
  storer.value = name;
}

function onUnlockPage(objectUrl, page) {
  var code = "post('" + objectUrl + "/unlock', {'page': '" + page + "'})";
  askConfirm('script', code, action_confirm);
}

function createCookie(name, value, days) {
  if (days) {
    var date = new Date();
    date.setTime(date.getTime()+(days*24*60*60*1000));
    var expires = "; expires=" + date.toGMTString();
  } else expires = "";
  document.cookie = name + "=" + encodeURIComponent(value) + expires + "; path=/;";
}

function readCookie(name) {
  var nameEQ = name + "=",
      ca = document.cookie.split(';'), c;
  for (var i=0; i < ca.length; i++) {
    c = ca[i];
    while (c.charAt(0)==' ') { c = c.substring(1,c.length); }
    if (c.indexOf(nameEQ) == 0) {
      return decodeURIComponent(c.substring(nameEQ.length,c.length));
    }
  }
  return null;
}

function switchImage(img, nameA, nameB) {
  // If p_img is named nameA, its name is switched to nameB and vice versa
  var path = img.src.split('/'),
      last = path.length-1,
      name = path[last],
      future = (name == nameA)? nameB: nameA;
  path[last] = future;
  img.src = path.join('/');
}

function changeImage(img, name) {
  // Changes p_img.src to new image p_name, keeping the same image path
  var path = img.src.split('/');
  path[path.length-1] = name;
  img.src = path.join('/');
  // Return the path to the image
  path.pop();
  return path.join('/');
}

function toggleCookie(cookieId,display,defaultValue,expandIcon,collapseIcon) {
  // What is the state of this boolean (expanded/collapsed) cookie ?
  var state = readCookie(cookieId);
  if ((state != 'collapsed') && (state != 'expanded')) {
    // No cookie yet, create it
    createCookie(cookieId, defaultValue);
    state = defaultValue;
  }
  // The hook is the part of the HTML document that needs to be shown or hidden
  var hook = document.getElementById(cookieId),
      displayValue = 'none',
      newState = 'collapsed',
      image = expandIcon + '.png';
  if (state == 'collapsed') {
    // Show the HTML zone
    displayValue = display;
    image = collapseIcon + '.png';
    newState = 'expanded';
  }
  // Update the corresponding HTML element
  hook.style.display = displayValue;
  var img = document.getElementById(cookieId + '_img');
  if (img) changeImage(img, image);
  // Inverse the cookie value
  createCookie(cookieId, newState);
}

// Functions for opening and closing a popup
function openPopup(popupId, msg, width, height, css, back, commentLabel) {
  // Put the message into the popup
  if (msg) {
    var msgHook = (popupId == 'alertPopup')? 'appyAlertText': 'appyConfirmText',
        confirmElem = document.getElementById(msgHook);
    confirmElem.innerHTML = msg;
  }
  // Set the comment label if defined
  if (commentLabel) {
    var labelHook = document.getElementById('appyCommentLabel');
    if (labelHook) labelHook.innerHTML = commentLabel;
  }
  // Get the popup
  var popup = document.getElementById(popupId),
      frame = popupId == 'iframePopup'; // Is it the "iframe" popup ?
  /* Define height and width. For non-iframe popups, do not set its height: it
     will depend on its content. */
  if (!width)  { width =  (frame)? window.innerWidth -300: null }
  if (!height) { height = (frame)? window.innerHeight-100: null }
  if (width) popup.style.width = width.toFixed() + 'px';
  if (height) popup.style.height = height.toFixed() + 'px';
  if (frame) {
    // Set the enclosed iframe dimensions and show the mask
    var iframe = document.getElementById('appyIFrame'),
        imask = document.getElementById('iframeMask');
    iframe.style.width = (width - 20).toFixed() + 'px';
    iframe.style.height = (height - 20).toFixed() + 'px';
    popup['back'] = back;
    imask.style.opacity = 0.7;
    imask.style.zIndex = 99;
  }
  // Apply the CSS class to the popup
  popup.className = (css)? 'popup ' + css: 'popup';
  // Show the popup
  popup.style.display = 'block';
}

function closePopup(popupId, clean, tryCancel) {
  // Get the popup
  var container = (popupId == 'iframePopup') ?
                  window.parent.document: window.document,
      popup = container.getElementById(popupId);
  // Close the popup
  popup.style.display = 'none';
  // Clean field "clean" if specified
  if (clean) {
    var elem = popup.getElementsByTagName('form')[0].elements[clean];
    if (elem) elem.value = '';
  }
  if (popupId == 'iframePopup') {
    // Try to click on a cancel button if found
    var canceled = false, icontent=null;
    if (tryCancel) {
      var iframe = popup.getElementsByTagName('iframe')[0];
      // "contentDocument" may be null if the iframe points to an external site
      icontent = iframe.contentDocument;
      var cancels = (icontent)? icontent.getElementsByName('cancel'): [],
          cancel = (cancels.length > 0)? cancels[0]: null;
      if (cancel && (cancel.tagName == 'A')) {
        cancel.click();
        canceled = true;
      }
    }
    if (!canceled) {
      /* Leave the form silently if we are on an edit page. If the iframe
         pointed to a page from an external site, this action will be blocked by
         the browser. */
      if (icontent) iframe.contentWindow.onbeforeunload = null;
    }
    if (icontent) icontent.removeChild(icontent.documentElement);
    // Hide the mask
    var imask = getNode(':iframeMask');
    imask.style.opacity = 0;
    imask.style.zIndex = 0;
  }
  return popup;
}

function showAppyMessage(message) {
  // Fill the message zone with the message to display
  var zone = getNode('appyMessageContent');
  if (!zone) zone = getNode(':appyMessageContent');
  zone.innerHTML = message;
  // Display the message box
  zone.parentNode.style.display = 'block';
}

// Function triggered when an action needs to be confirmed by the user
function askConfirm(actionType, action, msg, showComment, popupWidth,
                    commentLabel, comment, commentRows, visible) {
  /* Store the actionType (send a form, call an URL or call a script) and the
     related action, and shows the confirm popup. If the user confirms, we
     will perform the action. If p_showComment is true, an input field allowing
     to enter a comment will be shown in the popup. */
  var confirmForm = document.getElementById('confirmActionForm');
  confirmForm.actionType.value = actionType;
  confirmForm.action.value = action;
  confirmForm.visible.value = visible;
  if (!msg) msg = action_confirm;
  if (!commentLabel) commentLabel = workflow_comment;
  var commentArea = document.getElementById('commentArea');
  if (showComment) commentArea.style.display = 'block';
  else commentArea.style.display = 'none';
  // Initialise the text area
  var area = document.getElementById('popupComment');
  if (comment) {
    area.value = comment.replace(/<br\/>/g, '\n').replace(/&apos;/g, "'");
  }
  else area.value = '';
  area.rows = (commentRows)? commentRows: 3;
  openPopup('confirmActionPopup', msg, popupWidth, null,null,null,commentLabel);
}

// Function triggered when an action confirmed by the user must be performed
function doConfirm() {
  // The user confirmed: perform the required action
  closePopup('confirmActionPopup');
  var confirmForm = document.getElementById('confirmActionForm'),
      actionType = confirmForm.actionType.value,
      action = confirmForm.action.value,
      visible = confirmForm.visible.value == 'true',
      // Get the entered comment and clean it on the confirm form
      commentField = confirmForm.popupComment,
      comment = ((commentField.style.display != 'none') &&
                 (commentField.value))? commentField.value: '';
  commentField.value = '';
  // Tip: for subsequent "eval" statements, "comment" is in the context
  if (actionType == 'form') {
    /* Submit the form whose id is in "action", and transmit him the comment
       from the popup when relevant. */
    var f = document.getElementById(action);
    if (comment) f.popupComment.value = comment;
    f.submit();
    if (!visible) clickOn(f);
  }
  else if (actionType == 'url') { goto(action) } // Go to some URL
  else if (actionType == 'script') { eval(action) } // Exec some JS code
  else if (actionType == 'form+script') {
    var elems = action.split('+'),
        f = document.getElementById(elems[0]);
    // Submit the form in elems[0] and execute the JS code in elems[1]
    if (comment) f.popupComment.value = comment;
    f.submit();
    if (!visible) clickOn(f);
    eval(elems[1]);
  }
  else if (actionType == 'form-script') {
    /* Similar to form+script, but the form must not be submitted. It will
       probably be used by the JS code, so the comment must be transfered. */
    var elems = action.split('+'),
        f = document.getElementById(elems[0]);
    if (comment) f.popupComment.value = comment;
    eval(elems[1]);
  }
}

/* Finally posts the edit form after the user has confirmed that he really wants
   to post it. */
function postConfirmedEditForm() {
  document.getElementById('appyForm').confirmed.value = "True";
  submitAppyForm('save', 'main', 'view');
}

// Function that shows or hides a tab. p_action is 'show' or 'hide'.
function manageTab(tabId, action) {
  // Manage the tab content (show it or hide it)
  var show = action == 'show',
      content = document.getElementById('tabcontent_' + tabId);
  content.style.display = (show)? 'table-row': 'none';
  // Manage the tab itself (show as selected or unselected)
  var tab = document.getElementById('tab_' + tabId);
  tab.className = (show)? 'tabCur': 'tab';
}

// Function used for displaying/hiding content of a tab
function showTab(tabId) {
  // 1st, show the tab to show
  manageTab(tabId, 'show');
  // Compute the number of tabs
  var idParts = tabId.split('_');
  // Store the currently selected tab in a cookie
  createCookie('tab_' + idParts[0], tabId);
  // Then, hide the other tabs
  var tabs = document.getElementById('tabs_' + idParts[0]),
      tds = tabs.getElementsByTagName('td'), elem;
  for (var i=0; i<tds.length; i++) {
    elem = tds[i];
    if (elem.id != ('tab_' + tabId)) {
      manageTab(elem.id.substring(4), 'hide');
    }
  }
}

// Function that initializes the state of a tab
function initTab(tabsId, defaultValue, forceDefault) {
  if (forceDefault) {
    // Reset the cookie and use the default value
    createCookie(tabsId, defaultValue);
  }
  var selectedTabId = readCookie(tabsId);
  if (!selectedTabId) { showTab(defaultValue) }
  else {
    /* Ensure the selected tab exists (it could be absent because of field
       visibility settings) */
    var selectedTab = document.getElementById('tab_' + selectedTabId);
    if (selectedTab) { showTab(selectedTabId) }
    else { showTab(defaultValue) }
  }
}

function onSelectDate(cal) {
  var p = cal.params,
      update = (cal.dateClicked || p.electric);
  if (update && p.inputField) {
    var fieldName = cal.params.inputField.id,
        // Update day
        dayValue = cal.date.getDate() + '';
    if (dayValue.length == 1) dayValue = '0' + dayValue;
    var dayField = document.getElementById(fieldName + '_day');
    if (dayField) dayField.value = dayValue;
    // Update month
    var monthValue = (cal.date.getMonth() + 1) + '';
    if (monthValue.length == 1) monthValue = '0' + monthValue;
    document.getElementById(fieldName + '_month').value = monthValue;
    // Update year
    var year = document.getElementById(fieldName + '_year');
    if (!year) {
      // On the search screen, the 'from year' field has a special name
      var yearId = 'w_' + fieldName.split('_')[0];
      year = document.getElementById(yearId);
    }
    year.value = cal.date.getFullYear() + '';
  }
  if (update && p.singleClick && cal.dateClicked) {
    cal.callCloseHandler();
  }
}

function onSelectObjects(popupId, initiatorId, objectUrl, mode, onav,
                         sortKey, sortOrder, filters){
  /* Objects have been selected in a popup, to be linked via a Ref with
     link='popup'. Get them. */
  var node = document.getElementById(popupId),
      uids = stringFromDict(node['_appy_objs_cbs'], true),
      semantics = node['_appy_objs_sem'];
  // Show an error message if no element is selected
  if ((semantics == 'checked') && (!uids)) {
    openPopup('alertPopup', no_elem_selected);
    return;
  }
  // Close the popup
  closePopup('iframePopup');
  /* When refreshing the Ref field we will need to pass all those parameters,
     for replaying the popup query. */
  var params = {'selected': uids, 'semantics': semantics,
                'sortKey': sortKey || '', 'sortOrder': sortOrder,
                'filters': filters || ''};
  if (onav) params['nav'] = onav;
  if (mode == 'repl') {
    /* Link the selected objects (and unlink the potentially already linked
       ones) and refresh the Ref edit widget. */
    askField(':'+initiatorId, objectUrl, 'edit', params, false);
  }
  else {
    // Link the selected objects and refresh the Ref view widget
    params['action'] = 'onSelectFromPopup';
    askField(':'+initiatorId, objectUrl, 'view', params, false);
  }
}

function onSelectObject(checkboxId, initiatorId, id, ckNum) {
  // An object, whose ID is p_id, has been selected in a popup
  var checkbox = document.getElementById(checkboxId);
  if (ckNum) {
    // The object has been selected from a popup opened by ckeditor
    var imageUrl = siteUrl + '/' + checkbox.value + '/file/download';
    window.opener.CKEDITOR.tools.callFunction(ckNum, imageUrl);
    window.close();
  }
  else {
    /* The object has been selected from a Ref with link="popup[Ref]", in a
       popup displaying search results or objects from another Ref. A single
       object has been clicked. If multiple objects can be selected, simply
       update the corresponding checkbox status. Else, close the popup and
       return the selected object. */
    var checkbox = document.getElementById(checkboxId),
        visible = checkbox.parentNode.className != 'hide';
    // If the td is visible, simply click the checkbox
    if (visible) checkbox.click();
    else {
      /* Close the popup and directly refresh the initiator field with the
         selected object. */
      var uids = checkbox.value;
      closePopup('iframePopup');
      var params = {'selected': uids, 'semantics': 'checked'};
      askField(':'+initiatorId, siteUrl + '/' + id, 'edit', params, false);
    }
  }
}

function onSelectTemplateObject(checkboxId, formName, insert) {
  // Get the form for creating instances of p_className
  var addForm = window.parent.document.forms[formName];
  addForm.template.value = document.getElementById(checkboxId).value;
  addForm.insert.value = insert;
  closePopup('iframePopup');
  addForm.submit();
}

// Sets the focus on the correct element in some page
function initFocus(pageId){
  var id = pageId + '_title',
      elem = document.getElementById(id);
  if (elem) elem.focus();
}

// Functions for making popups draggable
function dragStart(event) {
  // Create a "drag" object to remember the current popup position
  var drag = new Object(),
      popup = event.target,
      popupRect = popup.getBoundingClientRect();
  if (popup.id != 'iframePopup') return;
  // Initialise the popup with absolute positioning
  popup.style.transform = 'none';
  popup.style.position = 'fixed';
  popup.style.top = popupRect.top + 'px';
  popup.style.left = popupRect.left + 'px';
  drag.top = popupRect.top;
  drag.left = popupRect.left;
  // Also remember where the user clicked
  drag.x = event.clientX;
  drag.y = event.clientY;
  drag.enabled = true;
  // Store the drag object in the popup
  popup['drag'] = drag;
}

function dragStop(event) {
  var drag = event.target['drag'];
  if (drag) drag.enabled = false;
}

function dragIt(event) {
  var popup = event.target,
      drag = popup['drag'];
  if (!drag || !drag.enabled) return;
  // Compute the delta with the initial position
  var deltaX = event.clientX - drag.x,
      deltaY = event.clientY - drag.y;
  // Move the popup
  popup.style.left = drag.left + deltaX + 'px';
  popup.style.top = drag.top + deltaY + 'px';
  event.preventDefault();
}

function dragPropose(event) { event.target.style.cursor = 'move'; }
