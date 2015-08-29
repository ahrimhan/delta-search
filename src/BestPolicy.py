import config

class BestSelectionPolicyContext:


    def __init__(self, policy):
        self.policy = policy
        self.maxValue = policy.getMaxValue()
        self.isInit = policy.isInit()
        self.maxCandidate = None

    def register(self, fitness, candidate):
        isAscending = self.policy.isAscendingRank()
        if isAscending:
            if self.isInit or (self.maxValue > fitness):
                self.maxValue = fitness
                self.maxCandidate = candidate
        else:
            if self.isInit or (self.maxValue < fitness):
                self.maxValue = fitness
                self.maxCandidate = candidate

        return False

    def elect():
        self.policy.setMaxValue(self.maxValue)
        return (self.maxCandidate, self.maxValue)
        


class BestPolicy:
    def __init__(self):
        self.maxCandidateCount = int(config.best_selection_max_candidate)
        self.isAscendingRankValue = True
        self.isInitValue = False
        self.maxValue = 0

    def getMaxCandidateCount(self):
        return self.maxCandidateCount

    def setAscendingRank(self, isAscendingRankValue):
        self.isAscendingRankValue = isAscendingRankValue

    def isInit(self):
        return self.isInitValue

    def setMaxValue(self, maxValue):
        self.isInitValue = True
        self.maxValue = maxValue

    def getMaxValue(self):
        return self.maxValue

    def isAscendingRank(self):
        return self.isAscendingRankValue


    def createContext(self):
        return BestSelectionPolicyContext(self)
        
    
    def getType(self):
        return "best"

