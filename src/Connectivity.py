


class Connectivity:
    def calculcate(self, modelContext):
        classList = modelContext.getClassList()

        connectivity = 0
        divFactor = 0
        
        for clazz in classList:
            methodIdxList = clazz.getMethods()

            methodIdxListIdx1 = 0
            methodIdxListIdx2 = 0

            classConnectivity = 0

            for methodIdxListIdx1 in xrange(len(methodIdxList) - 1):

                methodIdx1 = methodIdxList[methodIdxListIdx1]
                accessedFields1 = set(modelContext.getFieldListFromMethod(methodIdx1))

                methodIdxListIdx2 = 0
                for methodIdxListIdx2 in xrange(methodIdxListIdx1 + 1, len(methodIdxList)):
                    methodIdx2 = methodIdxList[methodIdxListIdx2]
                    accessedFields2 = set(modelContext.getFieldListFromMethod(methodIdx2))

                    if ((len(accessedFields1.intersection(accessedFields2) > 0)) or
                        (methodIdx1 in modelContext.getCalleeListFromMethod(methodIdx2)) or
                        (methodIdx2 in modelContext.getCalleeListFromMethod(methodIdx1))):
                        classConnectivity = classConnectivity + 1

            ml = len(methodIdxList)
            pairCount = ml * (ml - 1) / 2


            if pairCount != 0:
                classConnectivity = classConnectivity / float(pairCount)
                classWeight = len(clazz.getFields()) * ml * (ml - 1)
                connectivity = connectivity + classWeight * classMsc
                divFactor = divFactor + classWeight

        return connectivity / divFactor


    def isAscendingRank():
        return False

    def getType():
        return "connectivity"
