import re
import json
from os import listdir
from os import path
from xml.etree.ElementTree import SubElement
from obmenu.Config import Ignore
from obmenu.Config import Language
from obmenu.Builder import MenuItem
from xdg import DesktopEntry
from xdg import IconTheme
from xdg import Config
from hashlib import md5


def make(root, paths):
    applicationElements = {}
    desktopEntriesInfo = __getDesktopEntriesInformation(paths)

    for desktopEntryInfo in desktopEntriesInfo:
        categories = [category for category in desktopEntryInfo['categories']
                      if category not in Ignore.list]
        for category in categories:
            if category not in applicationElements:
                categoryName = category in Language.list and Language.list[category] or category
                applicationElements[category] = SubElement(root, "menu",
                                                           {"id": category,
                                                            "icon": "",
                                                            "label": categoryName})
            MenuItem.make(applicationElements[category], desktopEntryInfo['name'], desktopEntryInfo['exec'],
                          desktopEntryInfo['iconPath'])


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


def __loadFromCache(cacheName):
    info = None
    if path.isfile(cacheName):
        file = open(cacheName, 'r')
        info = json.load(file)
        file.close()
    return info


def __saveToCache(cacheName, info):
    if not path.isfile(cacheName):
        file = open(cacheName, 'w')
        json.dump(info, file)
        file.close()


def __getDesktopEntriesInformation(paths):
    fileList = __getDesktopFileList(paths)
    desktopEntriesInfo = __loadFromCache(md5(''.join(fileList).encode()).hexdigest())
    desktopEntriesInfo = desktopEntriesInfo or [__getItemInfo(desktopEntryPath) for desktopEntryPath in fileList]
    __saveToCache(md5(''.join(fileList).encode()).hexdigest(), desktopEntriesInfo)
    return desktopEntriesInfo
