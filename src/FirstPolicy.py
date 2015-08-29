import config

class FirstSelectionPolicyContext:
    def __init__(self, policy):
        self.policy = policy
        self.maxValue = policy.getMaxValue()
        self.isInit = policy.isInit()
        self.maxCandidate = None
        self.iteration = 0

    def register(self, fitness, candidate):
        isAscending = self.policy.isAscendingRank()
        if isAscending:
            if self.isInit or (self.maxValue > fitness):
                self.maxValue = fitness
                self.maxCandidate = candidate
                return True
        else:
            if self.isInit or (self.maxValue < fitness):
                self.maxValue = fitness
                self.maxCandidate = candidate
                return True


        if self.iteration < self.policy.getMaxCandidateCount():
            return False
        else:
            return True

    def elect():
        self.policy.setMaxValue(self.maxValue)
        return (self.maxCandidate, self.maxValue)
        

class FirstPolicy:
    def __init__(self):
        self.maxCandidateCount = int(config.first_selection_max_candidate)
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
        return FirstSelectionPolicyContext(self)
        
        
    def getType(self):
        return "first"

