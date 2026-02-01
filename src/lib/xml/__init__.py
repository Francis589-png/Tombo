"""
Tombo XML Library - XML Processing
"""
import xml.etree.ElementTree as ET
from xml.dom import minidom

def tombo_parse(xml_string):
    """Parse XML string to element tree."""
    try:
        return ET.fromstring(str(xml_string))
    except Exception as e:
        raise ValueError(f"Invalid XML: {e}")

def tombo_parse_file(file_path):
    """Parse XML from file."""
    try:
        tree = ET.parse(str(file_path))
        return tree.getroot()
    except Exception as e:
        raise IOError(f"Cannot parse XML file: {e}")

def tombo_element(tag, attrib=None):
    """Create an element."""
    if attrib is None:
        attrib = {}
    return ET.Element(str(tag), attrib)

def tombo_subelement(parent, tag, attrib=None):
    """Create subelement."""
    if attrib is None:
        attrib = {}
    return ET.SubElement(parent, str(tag), attrib)

def tombo_tostring(element):
    """Convert element to string."""
    try:
        return ET.tostring(element, encoding='unicode')
    except Exception as e:
        raise ValueError(f"Cannot convert to string: {e}")

def tombo_tofile(element, file_path):
    """Write element to file."""
    try:
        tree = ET.ElementTree(element)
        tree.write(str(file_path), encoding='utf-8', xml_declaration=True)
        return True
    except Exception as e:
        raise IOError(f"Cannot write XML file: {e}")

def tombo_prettify(xml_string):
    """Pretty print XML."""
    try:
        dom = minidom.parseString(str(xml_string))
        return dom.toprettyxml(indent="  ")
    except Exception as e:
        raise ValueError(f"Invalid XML: {e}")

def tombo_find(element, path):
    """Find element by path."""
    try:
        return element.find(str(path))
    except Exception as e:
        raise ValueError(f"Invalid path: {e}")

def tombo_findall(element, path):
    """Find all elements by path."""
    try:
        return element.findall(str(path))
    except Exception as e:
        raise ValueError(f"Invalid path: {e}")

def tombo_findtext(element, path, default=''):
    """Find element text."""
    try:
        return element.findtext(str(path), str(default))
    except Exception as e:
        raise ValueError(f"Invalid path: {e}")

def tombo_get_tag(element):
    """Get element tag."""
    return element.tag if hasattr(element, 'tag') else None

def tombo_get_text(element):
    """Get element text."""
    return element.text if hasattr(element, 'text') else ''

def tombo_get_attrib(element):
    """Get element attributes."""
    return element.attrib if hasattr(element, 'attrib') else {}

def tombo_set_attrib(element, key, value):
    """Set element attribute."""
    if hasattr(element, 'set'):
        element.set(str(key), str(value))
    return element

def tombo_children(element):
    """Get children elements."""
    return list(element) if hasattr(element, '__iter__') else []

def register(env):
    """Register XML library functions."""
    functions = {
        'parse': tombo_parse,
        'parse_file': tombo_parse_file,
        'element': tombo_element,
        'subelement': tombo_subelement,
        'tostring': tombo_tostring,
        'tofile': tombo_tofile,
        'prettify': tombo_prettify,
        'find': tombo_find,
        'findall': tombo_findall,
        'findtext': tombo_findtext,
        'get_tag': tombo_get_tag,
        'get_text': tombo_get_text,
        'get_attrib': tombo_get_attrib,
        'set_attrib': tombo_set_attrib,
        'children': tombo_children,
    }
    for name, func in functions.items():
        env.set(name, func)
