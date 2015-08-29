


class MPCWeight:
    def calculate(self, modelContext):
        classList = modelContext.getClassList()
        mpcTotal = 0
        for clazz in classList:
            methodIdxList = clazz.getMethods()
            for methodIdx in methodIdxList:
                calleeIdxList = modelContext.getCalleeListFromMethod(methodIdx)
                for calleeIdx in calleeIdxList:
                    ownerIdx = modelContext.get(calleeIdx)
                    if ownerIdx == clazz.getIndex():
                        m = modelContext.getMethodCallWeightMatrix()
                        mpcTotal = mpcTotal + m[methodIdx, calleeIdx]

        mpc = (float(mpcTotal)) / len(classList)
        return mpc

    def isAscendingRank(self):
        return True

    def getType(self):
        return "mpcw"
