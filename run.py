from sys import argv
from MenuApplication import MenuApplication

app = MenuApplication(argv)
result = app.run()
print(result)