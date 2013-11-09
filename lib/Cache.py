import json
from hashlib import md5


class Cache(object):
    _path = None

    def __init__(self, path):
        self._path = path

    def write(self, hashStr):
        fullPath = self._path + '/' + hashStr
        json.dump(open(fullPath, 'w'))

    def read(self, hashStr):
        fullPath = self._path + '/' + hashStr
        try:
            return json.load(open(fullPath))
        except:
            return {}

    def makeHash(self, stringForHash):
        hashObj = md5(stringForHash)
        hashStr = hashObj.hexdigest()
        return hashStr.encode()