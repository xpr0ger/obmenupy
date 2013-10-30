from obmenu.Builder import MenuItem


def make(root, appsList):
    for app in appsList:
        MenuItem.make(root, app['name'], app['command'], app['icon'])