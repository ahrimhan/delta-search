


class MPC:
    def calculate(self, modelContext):
        classList = modelContext.getClassList()
        mpcTotal = 0
        for clazz in classList:
            mpcSet = set()
            methodIdxList = clazz.getMethods()
            for methodIdx in methodIdxList:
                calleeIdx = modelContext.getCalleeListFromMethod(methodIdx)
                ownerIdx = modelContext.get(calleeIdx)
                if ownerIdx == clazz.getIndex():
                    mpcSet.add(calleeIdx)
            mpcTotal = mpcTotal + len(mpcSet)

        mpc = float(mpcTotal) / len(classList)
        return mpc

    def isAscendingRank(self):
        return True

    def getType(self):
        return "mpc"
