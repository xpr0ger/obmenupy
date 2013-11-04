__author__ = 'xproger'
from os import path, environ
from re import compile, match


class Application(object):
    defaultArgs = {
        'configDir': '/etc/obmenupy',
        'homeConfigDir': environ['HOME'] + '/.config/obmenupy',
        'cacheDir': '/menuCache',
        'localeDir': '/locale'
    }
    baseDir = None
    args = None

    def __init__(self, args):
        regexp = compile('^-{1,2}.+?=.+?')
        self.baseDir = path.dirname(args[0])
        self.args = {arg.split('=')[0].strip('-'): arg.split('=')[1] for arg in args[1:] if match(regexp, arg)}

    def getArg(self, argName):
        if argName not in self.defaultArgs.keys():
            return None
        if argName in self.args.keys():
            return self.args[argName]
        return self.defaultArgs[argName]

    def run(self):
        pass