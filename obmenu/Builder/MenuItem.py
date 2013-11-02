from xml.etree.ElementTree import SubElement


def make(root, name, pathToExec, iconPath=None):
    itemElement = SubElement(root, 'item', {'label': name})
    if not iconPath is None:
        itemElement.set('icon', iconPath)
    actionElement = SubElement(itemElement, 'action', {'name': 'Execute'})
    executeElement = SubElement(actionElement, 'execute')
    executeElement.text = pathToExec