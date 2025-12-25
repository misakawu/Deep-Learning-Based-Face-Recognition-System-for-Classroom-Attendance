import json


class faceInfo:
    def __init__(self):
        self.name = ""
        self.feature = []

    def __init__(self, name, feature):
        self.name = name
        self.feature = feature.tolist()

    def setName(self, name):
        self.name = name

    def setFeature(self, feature):
        self.feature = feature

    def getInfo(self):
        return (self.name, json.dumps(self.feature))
