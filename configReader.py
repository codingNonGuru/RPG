import re

class ConfigReader(object):
    _instance = None

    @staticmethod
    def Get():
        if ConfigReader._instance is None:
            ConfigReader._instance = ConfigReader()

        return ConfigReader._instance

    @staticmethod
    def GetVariable(key):
        return ConfigReader.Get().variables[key]

    def __init__(self):
        self.variables = dict()
        myFile = open("config.ini", "r")
        lines = myFile.readlines()
        myFile.close()
        
        for line in lines:
            regex = "(.*) = (.*)\n"
            searchResult = re.search(regex, line)

            self.variables[searchResult.group(1)] = searchResult.group(2)

        print(self.variables)