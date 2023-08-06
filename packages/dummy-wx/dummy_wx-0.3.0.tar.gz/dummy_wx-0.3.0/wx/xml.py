from wx import PyEventBinder

# Based on wxPython
# Copyright: (c) 2018 by Total Control Software
# License:   wxWindows License


def dummy_function(*args, **kwargs):
	return 0


XMLDOC_KEEP_WHITESPACE_NODES = 1
XMLDOC_NONE = 0
XML_ATTRIBUTE_NODE = 2
XML_CDATA_SECTION_NODE = 4
XML_COMMENT_NODE = 8
XML_DOCUMENT_FRAG_NODE = 11
XML_DOCUMENT_NODE = 9
XML_DOCUMENT_TYPE_NODE = 10
XML_ELEMENT_NODE = 1
XML_ENTITY_NODE = 6
XML_ENTITY_REF_NODE = 5
XML_HTML_DOCUMENT_NODE = 13
XML_NOTATION_NODE = 12
XML_NO_INDENTATION = -1
XML_PI_NODE = 7
XML_TEXT_NODE = 3
class XmlAttribute: ...
class XmlDoctype: ...
class XmlDocument: ...
class XmlDocumentLoadFlag: ...
class XmlNode: ...
class XmlNodeType: ...
class XmlProperty: ...
