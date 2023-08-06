from __future__ import annotations
from xml.etree.ElementTree import Element, tostring, fromstring
from typing import Optional, List, Type

class XmlElement:
    def __init__(self, n: str, a: Optional[dict] = {}, s: Optional[List[XmlElement]] = [], t: Optional[str] = None):
        """Create a new XmlElement.
        Keyword arguments:
        n -- XML tag name
        a -- Dictionary of XML attributes (default {})
        s -- Array of sublements for the XML element (default [])
        t -- Text content of the XML element
        """
        self.name = n
        self.attributes = a
        for attribute_key in a.keys():
            self.__add_xml_attribute_attribute(attribute_key)
        self.subelements = s
        self.__add_subelement_attribute(s)
        self.text = t
    
    def __add_subelement_attribute(self, subelements:List[XmlElement]) -> None:
        """Internal function to allow the shorthand . operator to access findall()"""
        for subelement in subelements:
            setattr(self, subelement.name, self.findall(subelement.name))


    def __add_xml_attribute_attribute(self, attribute_key:str) -> None:
        """Internal function to allow the shorthand . operator to access xml attributes if the attribute is not already used.
        .text, .attributes, .subelements etc. or any subelement with the same name will be paramount.
        """
        if not hasattr(self, attribute_key):
            def get_attribute(self, key:str):
                return self.attributes[key]
            setattr(self, attribute_key, get_attribute(self, attribute_key))


    def set(self, key: str, value:str) -> None:
        """Create or update an attribute
        Keyword arguments:
        key -- XML attribute name
        value -- XML attribute value
        """
        self.__add_xml_attribute_attribute(key)
        self.attributes = { **self.attributes, **{key: value} }


    def append(self, subelement: XmlElement) -> None:
        """Add a new subelement to this XmlElement
        Keyword arguments:
        subelement -- XmlElement
        """
        self.__add_subelement_attribute([subelement])
        self.subelements = [ *self.subelements, subelement]


    def extend(self, subelements: List[XmlElement]) -> None:
        """Add a set of subelements
        Keyword arguments:
        subelement -- Set of XmlElements
        """
        self.__add_subelement_attribute(subelements)
        self.subelements = [ *self.subelements, *subelements ]
        

    def to_etree_element(self) -> Element:
        """Render this XmlElement to an xml.etree.ElementTree.Element object"""
        e = Element(self.name)
        for k, v in self.attributes.items():
            e.set(k, v)
        for s in self.subelements:
            if not s == None:
                e.append(s.to_etree_element())
        e.text = self.text
        return e
    

    def to_string(self, encoding:Optional[str] = "unicode") -> str:
        """Render this XmlElement to string
        Keyword arguments:
        encoding -- The output encoding (default: 'unicode')
        """
        return tostring(self.to_etree_element(), encoding=encoding)


    def find(self, name: Optional[str] = None) -> XmlElement:
        """Return the first subelement with a given name or 
        None if no element with such a name exists
        Keyword arguments:
        name -- Tag name of the subelement searched for
        """
        for s in self.subelements:
            if not s == None:
                if name == None or s.name == name:
                    return s
        return None


    def findall(self, name: Optional[str] = None) -> List[XmlElement]:
        """Return all subelements with a given name or an empty 
        list if no element with such a name exists
        Keyword arguments:
        name -- Tag name of the subelement searched for
        """
        result = []
        for s in self.subelements:
            if not s == None:
                if name == None or s.name == name:
                    result.append(s)
        return result
        

    @staticmethod
    def from_etree_element(element: Type[Element]) -> XmlElement:
        """Recursively create a XmlElement from a given xml.etree.ElementTree.Element object
        Keyword arguments:
        element -- The xml.etree.ElementTree.Element to import
        """
        return XmlElement(
            element.tag, 
            a={k: v for k, v in element.items()},
            s=[XmlElement.from_etree_element(child) for child in element],
            t=element.text
        )


    @staticmethod
    def from_string(xml_string: str) -> XmlElement:
        """Create a XmlElement and its subelements from a XML file string
        Keyword arguments:
        xml_string -- The XML input data to import
        """
        return XmlElement.from_etree_element(fromstring(xml_string))


    def __str__(self) -> str:
        return self.to_string()


    def __repr__(self) -> str:
        return f'XmlElement({self.name})'

    
    def __len__(self) -> int:
        return len(self.subelements)