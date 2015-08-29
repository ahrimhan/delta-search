import scipy.sparse as sp
import numpy as np
import numpy.matlib as ml


class EPM:

    def calculate(self, modelContext):

        entityMatrix = modelContext.getMethodCallMatrix() + modelContext.getFieldAccessMatrix()
        membershipMatrix = modelContext.getMembershipMatrix()
        intersectMatrix = entityMatrix * membershipMatrix

        entityCountOnClass = membershipMatrix.sum(0)
        unionMatrix = entityMatrix.sum(1).repeat(modelContext.getClassCount(), 1) + entityCountOnClass.repeat(modelContext.getEntityCount(), 0) - intersectMatrix - membershipMatrix
        unionMatrix = sp.csr_matrix(unionMatrix, dtype=float)

        distanceMatrix = 1. - (intersectMatrix / unionMatrix).todense()

        compensationMatrix = sp.csr_matrix(~np.isfinite(distanceMatrix)).sum(0)

        distanceMatrix[~np.isfinite(distanceMatrix)] = 0
        distanceSumOnClass = sp.csr_matrix(distanceMatrix.sum(0), dtype=float)

        #entityCountOnSystem = ml.repmat([modelContext.getEntityCount()], 1, modelContext.getClassCount())
        entityCountOnOtherClass = modelContext.getEntityCount() - entityCountOnClass + compensationMatrix
        distanceSumOnOtherClass = distanceSumOnClass.sum() - distanceSumOnClass.todense()
        #ml.repmat([distanceMatrix.sum()], 1, modelContext.getClassCount()) - distanceSumOnClass

        #epcMatrix = distanceSumOnClass.multiply(entityCountOnOtherClass) / entityCountSumOnClass / distanceSumOnOtherClass
        epcMatrix = distanceSumOnClass.multiply(entityCountOnOtherClass) / distanceSumOnOtherClass
        infiniteEntriesCount = len(epcMatrix[np.isfinite(epcMatrix)])
        epcMatrix[~np.isfinite(epcMatrix)] = 0
        # / entityCountOnSystem


        
        return epcMatrix.sum() / (modelContext.getClassCount() - infiniteEntriesCount)


    def isAscendingRank(self):
        return True

    def getType(self):
        return "epm"
