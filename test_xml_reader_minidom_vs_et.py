from xml.dom import minidom
import xml.etree.ElementTree as ET
import utils

"""
    Test Minidom versus Element Tree to read .xml file
    Chosen: minidom
    
    Source: http://stackabuse.com/reading-and-writing-xml-files-in-python/
"""


def test_minidom(filename):
    # parse an xml file by name
    mydoc = minidom.parse(filename)

    items = mydoc.getElementsByTagName('item')

    # one specific item attribute
    print('Item #2 attribute:')
    print(items[1].attributes['name'].value)

    # all item attributes
    print('\nAll attributes:')
    for elem in items:
        print(elem.attributes['name'].value)

    # one specific item's data
    print('\nItem #2 data:')
    print(items[1].firstChild.data)
    print(items[1].childNodes[0].data)

    # all items data
    print('\nAll item data:')
    for elem in items:
        print(elem.firstChild.data)


def test_element_tree(filename):
    tree = ET.parse(filename)
    root = tree.getroot()

    # one specific item attribute
    print('Item #2 attribute:')
    print(root[0][1].attrib)

    # all item attributes
    print('\nAll attributes:')
    for elem in root:
        for subelem in elem:
            print(subelem.attrib)

    # one specific item's data
    print('\nItem #2 data:')
    print(root[0][1].text)

    # all items data
    print('\nAll item data:')
    for elem in root:
        for subelem in elem:
            print(subelem.text)


if __name__ == '__main__':
    filename = utils.project_dir_name() + 'data/test.xml'

    # test_minidom(filename)

    test_element_tree(filename)
