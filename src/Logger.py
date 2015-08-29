import datetime
import os


class LoggerContext:

    def __init__(self, classList, entityList, basePath, selectionType, searchType, fitnessType):

        path = "%s/%s-%s-%s" % (basePath, selectionType, searchType, fitnessType)

        if not os.path.exists(path):
            os.makedirs(path)

        self.cfile = open("%s/candidate.csv" % path, 'w+')
        self.sfile = open("%s/selection.csv" % path, 'w+')
        self.classList = classList
        self.entityList = entityList

    def logc(self, iteration, cidx, candidate, fitness):
        self.log_internal(self.cfile, iteration, cidx, candidate, fitness)

    def logs(self, iteration, candidate, fitness):
        self.log_internal(self.sfile, iteration, 0, candidate, fitness)

    def log_internal(self, filedesc, iteration, cidx, candidate, fitness):
        (fromClassIdx, methodIdx, toClassIdx, delta) = candidate
        fromClass = self.classList[fromClassIdx].getName()
        toClass = self.classList[toClassIdx].getName()
        methodName = self.entityList[methodIdx]

        nowdt = datetime.datetime.now()
        nowstr = "%s:%f" % (nowdt.strftime("%Y-%m-%d %H:%M"), nowdt.second + nowdt.microsecond / 1000000.0)
        print >>filedesc, "%s %d, %d, \"%s -> %s -> %s\", %f, %f" % (nowstr, iteration, cidx, fromClass, methodName, toClass, delta, fitness)
        #print "%d %d, %d, \"%s -> %s -> %s\", %f, %f" % (nowstr, iteration, cidx, fromClass, methodName, toClass, delta, fitness)
    def close(self):
        close(self.cfile)
        close(self.sfile)
    

class Logger:
    
    def __init__(self, basePath, project, classList, entityList):
        self.classList = classList
        self.entityList = entityList
        nowDt = datetime.datetime.now()
        nowStr = nowDt.strftime("%Y%m%d_%H%M%S")
        self.basePath = "%s/%s-%s" % (basePath, project, nowStr)

    def createContext(self, selectionType, searchType, fitnessType):
        return LoggerContext(self.classList, self.entityList, self.basePath, selectionType, searchType, fitnessType)



