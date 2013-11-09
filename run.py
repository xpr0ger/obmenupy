from sys import argv
from lib import MenuApplication

app = MenuApplication(argv)
result = app.run()
print(result)