import random

class ARRandomCandidateIterator:
    def __init__(self, modelContext, maxCandidate):
        self.modelContext = modelContext
        self.maxCandidate = maxCandidate
        self.index = 0
        self.pastCandidates = set()
        random.seed()

    def hasCandidate(self):
        if self.maxCandidate < 0:
            return True
        else:
            return self.index < self.maxCandidate

    def candidate(self):
        classCount = modelContext.getClassCount()
        methodCount = modelContext.getMethodCount()
        randomIter = 0
        
        ret = None

        for randomIter in xrange(1000):
            fromClassIdx = random.randint(0, classCount-1)
            toClassIdx = random.randint(0, classCount-1)
            if fromClassIdx == toClassIdx:
                continue
            methodIdx = random.randint(0, methodCount-1)

            candidate = (fromClassIdx, methodIdx, toClassIdx, 0)
            if not candidate in self.pastCandidates:
                ret = candidate
                self.pastCandidates.add(ret)
                break

        self.index = self.index + 1
        return ret




class ARRandomSelector:
    #def __init__(self):

    def getIterator(self, modelContext, maxCandidate):
        return ARRandomCandidateIterator(modelContext, maxCandidate)

    def getType(self):
        return "random"

