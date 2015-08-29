class MSC:
    def calculcate(self, modelContext):
        classList = modelContext.getClassList()

        msc = 0
        divFactor = 0
        

        for clazz in classList:
            methodIdxList = clazz.getMethods()

            methodIdxListIdx1 = 0
            methodIdxListIdx2 = 0

            classMsc = 0
            pairCount = 0

            for methodIdxListIdx1 in xrange(len(methodIdxList) - 1):

                methodIdx1 = methodIdxList[methodIdxListIdx1]
                accessedFields1 = set(modelContext.getFieldListFromMethod(methodIdx1))
                methodIdxListIdx2 = 0

                for methodIdxListIdx2 in xrange(methodIdxListIdx1 + 1, len(methodIdxList)):
                    methodIdx2 = methodIdxList[methodIdxListIdx2]
                    accessedFields2 = set(modelContext.getFieldListFromMethod(methodIdx2))
                    intersectionSize = len(accessedFields1.intersection(accessedFields2))
                    unionSize = len(accessedFields1) + len(accessedFields2) - intersectionSize
                    if unionSize != 0:
                        classMsc = classMsc + (intersectionSize / float(unionSize))
                        pairCount = pairCount + 1

            if pairCount != 0:
                classMsc = classMsc / (float(pairCount))
                ml = len(methodIdxList)
                classWeight = len(clazz.getFields()) * ml * (ml - 1)
                msc = msc + classWeight * classMsc
                divFactor = divFactor + classWeight

        return msc / divFactor


    def isAscendingRank(self):
        return False



    def getType(self):
        return "msc"


        
