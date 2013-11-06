from Application import Application
import re
import json
from os import listdir
from os import path
from xml.etree.ElementTree import Element, SubElement, tostring
from xdg import DesktopEntry, IconTheme, Config
from xdg.BaseDirectory import xdg_data_dirs
from hashlib import md5


class MenuApplication(Application):
    _config = {}
    _desktopEntryPaths = {}
    _configList = [
        'bottom_menu.cfg',
        'top_menu.cfg',
        'ignore_list.cfg',
        'category_aliases.cfg'
    ]

    def __init__(self, args):
        Application.__init__(self, args)
        paths = self.getConfigPaths()
        configFiles = self.getConfigFiles(paths)
        self._config = {fileName[:fileName.rfind('.')]: json.load(open(configFiles[fileName]))
                        for fileName in configFiles}
        self._desktopEntryPaths = [pathPart + '/applications/' for pathPart in xdg_data_dirs
                                   if path.isdir(pathPart + '/applications/')]

    def run(self):
        menuRoot = Element("openbox_pipe_menu")
        if 'top_menu' in self._config and len(self._config['top_menu']):
            self._makeMenuItems(menuRoot, self._config['top_menu'])
            self._makeSeparatorItem(menuRoot)
        self._makeApplicationMenu(menuRoot, self._desktopEntryPaths,
                                  self._config['ignore_list'] if 'ignore_list' in self._config else {},
                                  self._config['category_aliases'] if 'category_aliases' in self._config else {})
        if 'bottom_menu' in self._config and len(self._config['bottom_menu']):
            self._makeSeparatorItem(menuRoot)
            self._makeMenuItems(menuRoot, self._config['bottom_menu'])
        return tostring(menuRoot).decode()

    def _makeMenuItem(self, root, name, pathToExec, iconPath=None):
        itemElement = SubElement(root, 'item', {'label': name})
        if not iconPath is None:
            itemElement.set('icon', iconPath)
        actionElement = SubElement(itemElement, 'action', {'name': 'Execute'})
        executeElement = SubElement(actionElement, 'execute')
        executeElement.text = pathToExec

    def _makeMenuItems(self, root, appsList):
        for app in appsList:
            self._makeMenuItem(root, app['name'], app['command'], app['icon'])

    def _makeSeparatorItem(self, root, text=None):
        separator = SubElement(root, 'separator')
        if not text is None:
            separator.set('label', text)

    def _makeApplicationMenu(self, root, paths, ignoreList, aliasesList):
        applicationElements = {}
        desktopEntriesInfo = self._getDesktopEntriesInformation(paths)

        for desktopEntryInfo in desktopEntriesInfo:
            categories = [category for category in desktopEntryInfo['categories']
                          if category not in ignoreList]
            for category in categories:
                if category not in applicationElements:
                    categoryName = category in aliasesList and aliasesList[category] or category
                    applicationElements[category] = SubElement(root, "menu",
                                                               {"id": category,
                                                                "icon": "",
                                                                "label": categoryName})
                self._makeMenuItem(applicationElements[category], desktopEntryInfo['name'], desktopEntryInfo['exec'],
                                   desktopEntryInfo['iconPath'])

    def _getDesktopEntriesInformation(self, paths):
        fileList = self._getDesktopFileList(paths)
        desktopEntriesInfo = self._loadFromCache(md5(''.join(fileList).encode()).hexdigest())
        desktopExecRegExp = re.compile('(.+?)\s%.+')
        desktopEntriesInfo = desktopEntriesInfo or [self._getItemInfo(desktopEntryPath, desktopExecRegExp) for
                                                    desktopEntryPath
                                                    in fileList]
        self._saveToCache(md5(''.join(fileList).encode()).hexdigest(), desktopEntriesInfo)
        return desktopEntriesInfo

    def _getDesktopFileList(self, paths):
        regexp = re.compile('.*?\.desktop$')
        desktopEntries = []
        for desktopEntriesPath in paths:
            desktopEntries += [desktopEntriesPath + desktopEntry for desktopEntry in listdir(desktopEntriesPath)
                               if re.match(regexp, desktopEntry)]
        return desktopEntries

    def _loadFromCache(self, cacheName):
        info = None
        if path.isfile(cacheName):
            file = open(cacheName, 'r')
            info = json.load(file)
            file.close()
        return info

    def _saveToCache(self, cacheName, info):
        if not path.isfile(cacheName):
            file = open(cacheName, 'w')
            json.dump(info, file)
            file.close()

    def _getItemInfo(self, desktopEntryPath, compiledRegexp):
        desktopEntry = DesktopEntry.DesktopEntry(desktopEntryPath)
        execCommand = desktopEntry.getExec()
        matchResult = re.match(compiledRegexp, execCommand)
        execCommand = execCommand if matchResult is None else matchResult.groups()[0]
        return {
            'categories': desktopEntry.getCategories(),
            'name': desktopEntry.getName(),
            'exec': execCommand,
            'iconPath': IconTheme.getIconPath(desktopEntry.getIcon(), 32, Config.icon_theme)
        }
