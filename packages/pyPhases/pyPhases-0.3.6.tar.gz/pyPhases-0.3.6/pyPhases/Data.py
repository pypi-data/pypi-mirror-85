import os
from pyPhases import Project
from pyPhases.util.Logger import classLogger
from pyPhases.util.Optionizable import Optionizable


class DataNotFound(Exception):
    pass

class Data(Optionizable):
    project: Project
    dataNames = {}
    version = "current"

    def __init__(self, name, dataTags=[]):
        self.name = name
        self.dataTags = dataTags
        Data.dataNames[name] = self

    def _getTagValue(self, tagname):
        # TODO: circle detection
        if tagname in Data.dataNames:
            self.logDebug("Data %s depends on different dataset %s: %s"%(self.name, tagname, Data.dataNames[tagname].dataTags))
            return self.parseDatanames(Data.dataNames[tagname].dataTags)
        value = self.project.getConfig(tagname)
        if isinstance(value, list):
            return "_".join(map(str, value))

        return str(value)

    def setProject(self, project):
        self.project = project

    def parseDatanames(self, tags):
        return "-".join(map(self._getTagValue, tags))

    def getDataName(self):
        tagStr = self.parseDatanames(self.dataTags)
        return self.name + tagStr

    def __str__(self):
        return self.getDataName()

    def getDataId(self):
        return self.getDataName() + "--" + self.version


    @staticmethod
    def create(val, project):
        dataObj = None
        if isinstance(val, Data):
            dataObj = val
        elif isinstance(val, str):
            dataObj = Data(val)
        else:
            raise Exception("Unsupported type as data identifier")

        dataObj.setProject(project)

        return dataObj

    @staticmethod
    def getFromName(name):
        if not name in Data.dataNames:
            raise Exception(
                "The DataWrapper with name %s was not defined and does not exist in any phase" % (name))
        return Data.dataNames[name]
