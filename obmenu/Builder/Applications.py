from os import listdir
import re
from xml.etree.ElementTree import SubElement
from obmenu.Config import Ignore
from obmenu.Config import Language
from obmenu.Builder import MenuItem
from xdg import DesktopEntry
from xdg import IconTheme
from xdg import Config


def make(root, paths):
    applicationElements = {}

    for desktopEntryPath in __getDesktopFileList(paths):
        info = __getItemInfo(desktopEntryPath)
        categories = [category for category in info['categories']
                      if category not in Ignore.list]
        for category in categories:
            if category not in applicationElements:
                categoryName = category in Language.list and Language.list[category] or category
                applicationElements[category] = SubElement(root, "menu",
                                                           {"id": category,
                                                            "icon": "",
                                                            "label": categoryName})
            MenuItem.make(applicationElements[category], info['name'], info['exec'], info['iconPath'])


def __getDesktopFileList(paths):
    regexp = re.compile('.*?\.desktop$')
    desktopEntries = []
    for desktopEntriesPath in paths:
        desktopEntries += [desktopEntriesPath + desktopEntry for desktopEntry in listdir(desktopEntriesPath)
                           if re.match(regexp, desktopEntry)]
    return desktopEntries


def __getItemInfo(desktopEntryPath):
    desktopEntry = DesktopEntry.DesktopEntry(desktopEntryPath)
    return {
        'categories': desktopEntry.getCategories(),
        'name': desktopEntry.getName(),
        'exec': desktopEntry.getExec(),
        'iconPath': IconTheme.getIconPath(desktopEntry.getIcon(), 32, Config.icon_theme)
    }