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
        desktopEntry = DesktopEntry.DesktopEntry(desktopEntryPath)
        categories = [category for category in desktopEntry.getCategories()
                      if category not in Ignore.list]
        for category in categories:
            if category not in applicationElements:
                categoryName = category in Language.list and Language.list[category] or category
                applicationElements[category] = SubElement(root, "menu",
                                                           {"id": category,
                                                            "icon": "",
                                                            "label": categoryName})
            iconPath = IconTheme.getIconPath(desktopEntry.getIcon(), 32, Config.icon_theme)
            MenuItem.make(applicationElements[category], desktopEntry.getName(), desktopEntry.getExec(),
                          iconPath)


def __getDesktopFileList(paths):
    regexp = re.compile('.*?\.desktop$')
    desktopEntries = []
    for desktopEntriesPath in paths:
        desktopEntries += [desktopEntriesPath + desktopEntry for desktopEntry in listdir(desktopEntriesPath)
                           if re.match(regexp, desktopEntry)]
    return desktopEntries