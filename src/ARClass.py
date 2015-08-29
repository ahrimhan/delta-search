
class ARClass:
    name = None
    index = 0

    def __init__(self):
        self.fields = []
        self.methods = []
        name = None

    def copy(self):
        ret = ARClass()
        ret.name = self.name
        ret.index = self.index
        ret.fields = list(self.fields)
        ret.methods = list(self.methods)
        return ret

    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name

    def addMethod(self, method):
        self.methods.append(method)

    def addField(self, field):
        self.fields.append(field)
    
    def removeMethod(self, method):
        self.methods.remove(method)

    def moveMethod(self, other, method):
        other.addMethod(method)
        self.removeMethod(method)

    def getFields(self):
        return self.fields

    def getMethods(self):
        return self.methods

    def setIndex(self, index):
        self.index = index

    def getIndex(self):
        return self.index
