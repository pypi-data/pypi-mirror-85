# XmlElement

A simpler XML writer.

## Installation

`pip install XmlElement`

## Test

```
>>> from XmlElement import XmlElement as X
>>> xml = X.from_string('<test><x/></test>')
>>> xml
XmlElement(test)
```

## Usage

```python
import XmlElement from XmlElement

xml = XmlElement('RootElement', s=[ # root element without attributes
    X('Child1', {'name': 'child1', 'testattr': 'Example attribute'}, [ # sub element with an attribute
        X('Child2', t='Example text value') # sub-sub element with text value
    ])
])

print(xml)
print(xml.Child1[0].testattr) # Example attribute
print(xml.Child1[0].Child2[0].text) # Example text value
```



