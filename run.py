from xdg.BaseDirectory import xdg_data_dirs
from os import path
from xml.etree.ElementTree import Element, SubElement, tostring
from obmenu.Config import DefaultMenu
from obmenu.Builder import Separator
from obmenu.Builder import Applications
from obmenu.Config import ExitMenu
from obmenu.Builder import MenuItems


def main():
    desktopEntryPaths = [pathPart + '/applications/' for pathPart in xdg_data_dirs
                         if path.isdir(pathPart + '/applications/')]

    menuRoot = Element("openbox_pipe_menu")
    MenuItems.make(menuRoot, DefaultMenu.list)
    Separator.make(menuRoot)
    applicationsMenu = SubElement(menuRoot, "menu", {"id": "ApplicationsMenu", "icon": "", "label": u'Программы'})
    Applications.make(applicationsMenu, desktopEntryPaths)
    Separator.make(menuRoot)
    MenuItems.make(menuRoot, ExitMenu.list)

    print(tostring(menuRoot).decode())


main()