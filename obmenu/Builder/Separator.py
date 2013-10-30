from xml.etree.ElementTree import SubElement


def make(root, text=None):
    separator = SubElement(root, 'separator')
    if not text is None:
        separator.set('label', text)
