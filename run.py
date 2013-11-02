def main():
    import gettext
    import json
    from os import path
    basePath = path.dirname(path.realpath(__file__))
    gettext.install('obmenupy', basePath+'/locale')
    from xdg.BaseDirectory import xdg_data_dirs
    from xml.etree.ElementTree import Element, SubElement, tostring
    from obmenu.Builder import Separator
    from obmenu.Builder import Applications
    from obmenu.Builder import MenuItems

    desktopEntryPaths = [pathPart + '/applications/' for pathPart in xdg_data_dirs
                         if path.isdir(pathPart + '/applications/')]

    menuRoot = Element("openbox_pipe_menu")
    MenuItems.make(menuRoot, __parseConfig('top_menu', basePath))
    Separator.make(menuRoot)
    applicationsMenu = SubElement(menuRoot, "menu", {"id": "ApplicationsMenu", "icon": "", "label": u'Программы'})
    Applications.make(applicationsMenu, desktopEntryPaths)
    Separator.make(menuRoot)
    MenuItems.make(menuRoot, __parseConfig('bottom_menu', basePath))

    print(tostring(menuRoot).decode())

def __parseConfig(configName, basePath):
    import json
    file = open(basePath+'/config/'+configName+'.cfg', 'r')
    result = json.load(file)
    file.close()
    return result

main()