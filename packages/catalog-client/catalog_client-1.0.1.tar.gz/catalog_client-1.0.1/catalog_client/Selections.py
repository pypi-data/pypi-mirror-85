import sys
sys.path.append('.')

# This code is needed is pyxml if installed
pyxml=None
index = 0
for p in sys.path:
    if -1 != p.find('pyxml'):
         pyxml = p
    index += 1
if None != pyxml:
    sys.path.remove(pyxml)


import datetime
INTEGER_TYPE = type(0)
FLOAT_TYPE = type(0.0)
STRING_TYPE = type("")
DATETIME_TYPE = type(datetime.datetime.strptime('1970-01-01T00:00:00',
                                                '%Y-%m-%dT%H:%M:%S' ))
LIST_TYPE = type([])
SLICE_TYPE = type(slice(0))

import xml.etree.ElementTree as ET

def _append_value(parent,
                value):
    valueElement = ET.Element('value')
    if DATETIME_TYPE == type(value):
        valueElement.text = str(value.isoformat() + 'Z')
        valueElement.set('type', 'java.util.Date')
    else:
        valueElement.text = str(value)
        if FLOAT_TYPE == type(value):
            valueElement.set('type', 'java.lang.Float')
        elif INTEGER_TYPE == type(value):
            valueElement.set('type', 'java.lang.Integer')
        else:
            valueElement.set('type', 'java.lang.String')
    parent.append(valueElement)


def _append_item(parent,
               name,
               value):
    nameElement = ET.Element('name')
    nameElement.text = name
    parent.append(nameElement)
    _append_value(parent, value)


def _append_tag(parent,
              tag,
              values):
    tagElement = ET.Element('or')
    for value in values:
        if SLICE_TYPE == type(value):
            sliceElement = ET.Element('and')
            begin = ET.Element('gte')
            _append_item(begin, tag, value.start)
            sliceElement.append(begin)
            end = ET.Element('lt')
            _append_item(end, tag, value.stop)
            sliceElement.append(end)
            tagElement.append(sliceElement)
        else:
            equals = ET.Element('eq')
            _append_item(equals, tag, value)
            tagElement.append(equals)
    if 1 == len(tagElement):
        for child in tagElement:
            parent.append(child)
        return
    parent.append(tagElement)


def _create_attachment(selections):
    attachment = ET.Element('and')
    for tag in selections.keys():
        _append_tag(attachment, tag, selections[ tag ])
    if 1 == len(attachment):
        for child in attachment:
            return child
        return
    return attachment


def resolve_selection(catalog, attachment, element = 'url', triggers = None):
    conjunction = ''
    if None == element:
        tags = ''
    else:
        tags = conjunction + 'tag=' + element
        conjunction = "&"
    if None != triggers and len(triggers) != 0:
        for trigger in triggers:
            tags = tags + conjunction + 'tag=' + trigger
            conjunction = '&'
    print("tags=" + tags)
    query = '?ordering=begin_time&' + tags
    entries = catalog.get_selection(attachment, query)
    entrySeq = entries.findall('entry')
    result = []
    for entry in entrySeq:
        xmlElement = entry.find('tags/tag/[name="' + element + '"]')
        if None != xmlElement:
            value = xmlElement.find('value').text
            if 'url' == element and value.startswith('file:'):
                value = value[5:]
                if value.startswith('///'):
                    value = value [2:]
            result.append(value)
    return result


class Selections(object):
    """
    This class captures on or more selections to be sent to the Catalog.
    """

    def __init__(self, catalog, tag, value, element = None, triggers = None ):
        if STRING_TYPE != type(tag):
            # Assume this is a copy operation
            self.selections = tag.selections.copy()
            return
        self.catalog = catalog
        self.element = element
        self.selections = {}
        self.select(tag, value)
        self.triggers = triggers


    def typeToUse(self, value):
        if None == value:
            return value
        if SLICE_TYPE == type(value):
    	    return slice(self.typeToUse(value.start),
    	                 self.typeToUse(value.stop),
    	                 self.typeToUse(value.step))
        if LIST_TYPE == type(value):
        	result = []
        	for v in value:
        	    result.append(self.typeToUse(v))
        	return result
        if STRING_TYPE != type(value):
            return value
        try:
            return datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%S" )
        except ValueError:
            pass
        try:
            return datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M" )
        except ValueError:
            pass
        try:
            return datetime.datetime.strptime(value, "%Y-%m-%dT%H" )
        except ValueError:
            pass
        try:
            return datetime.datetime.strptime(value, "%Y-%m-%d" )
        except ValueError:
            pass
        return value


    def __add__(self, rhs):
        result = Selections(self, self.catalog, None)
        result += rhs
        return result


    def __iadd__(self, rhs):
        for tag in self.selections:
            if tag in rhs.selections:
                self.selections[ tag ].extend(rhs.selections[ tag ])
        for tag in self.selections:
            if not tag in self.selections:
                self.selections[ tag ] = last(rhs.selections[ tag ])
        return self


    def __getitem__(self, key):
        self.resolve()
        return self.resolution[key]


    def __len__(self):
        self.resolve()
        return len(self.resolution)


    def __repr__(self):
        try:
            self.resolve()
        except TypeError as e:
            if 'Response is "text/html", not "text/xml"' == e.message:
                raise IOError('Failed to get correct reponse from Web Service')
        return str(self.resolution)


    def __str__(self):
        return str(self.selections)


    def select(self, tag, value):
        valueToUse = self.typeToUse(value)
        if tag in self.selections:
            existing = self.selections[ tag ]
        else:
            existing = self.selections[ tag ] = []
        if LIST_TYPE == type(valueToUse):
            self.selections[ tag ].extend(valueToUse)
        else:
            self.selections[ tag ].append(valueToUse)
        self.resolution = None
        return self


    def resolve(self):
        if hasattr(self, 'resolution') and None != self.resolution:
            return self.resolution
        attachment = _create_attachment(self.selections)
        self.resolution = resolve_selection(self.catalog, attachment,
                                            self.element, self.triggers)
