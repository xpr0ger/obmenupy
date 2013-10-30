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
    regexp = re.compile('.*?\.desktop$')
    for dirName in paths:
        for desktopEntryPath in listdir(dirName):
            if re.match(regexp, desktopEntryPath):
                desktopEntry = DesktopEntry.DesktopEntry(dirName + desktopEntryPath)
                for category in desktopEntry.getCategories():
                    if category in Ignore.list:
                        continue
                    if category not in applicationElements:
                        categoryName = category in Language.list and Language.list[category] or category
                        applicationElements[category] = SubElement(root, "menu",
                                                                   {"id": category, "icon": "", "label": categoryName})
                    iconPath = IconTheme.getIconPath(desktopEntry.getIcon(), 32, Config.icon_theme)
                    MenuItem.make(applicationElements[category], desktopEntry.getName(), desktopEntry.getExec(),
                                  iconPath)