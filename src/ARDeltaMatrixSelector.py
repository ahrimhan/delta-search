import scipy.sparse as sp
import numpy as np
import config
import blist

class ARDeltaCandidateIterator:

    def __init__(self, candidateList):
        self.candidateList = candidateList
        self.index = 0

    def hasCandidate(self):
        return self.index < len(self.candidateList)

    def candidate(self):
        ret = None
        if self.index < len(self.candidateList):
            ret = self.candidateList[self.index]
            self.index = self.index + 1
        return ret


class ARDeltaMatrixSelector:

    def __init__(self):
        self.cohesionOverCoupling = float(config.cohesionFactor) / float(config.couplingFactor)
        self.adjustMatrix = None


    def getInternalExternalLinkMatrix(self, model):
        membershipMatrix = model.getMembershipMatrix()
        linkMatrix = model.getMethodCallBiMatrix() + model.getFieldAccessBiMatrix() + self.cohesionOverCoupling * model.getCohesionMatrix()
        internalLinkMask = membershipMatrix * membershipMatrix.T
        internalLinkMatrix = linkMatrix.multiply(internalLinkMask)
        externalLinkMatrix = linkMatrix - internalLinkMatrix
        return (internalLinkMatrix, externalLinkMatrix)

    def invertedMembershipMatrix(self, M):
        new_matrix = np.zeros(M.shape)
        (rows, cols) = M.nonzero()
        for i in range(len(rows)):
            v = M[rows[i], cols[i]]
            new_matrix[rows[i], :] = new_matrix[rows[i], :] + v
            new_matrix[rows[i], cols[i]] = 0
        ret  = sp.coo_matrix(new_matrix)
        return ret 
    
    def getDeltaMatrix(self, model):
        (internalMatrix, externalMatrix) = self.getInternalExternalLinkMatrix(model) 
        IP = internalMatrix * model.membershipMatrix
        EP = externalMatrix * model.membershipMatrix
        IIP = self.invertedMembershipMatrix(IP)
        D = IIP - EP
        return D


#public methods
    def getIterator(self, modelContext, maxCandidate):
        D = self.getDeltaMatrix(modelContext)

        if not self.adjustMatrix:
            self.adjustMatrix = sp.coo_matrix(np.zeros(D.shape)).tolil()

        D = D + self.adjustMatrix

        self.adjustMatrix = self.adjustMatrix * 0.9

        PD = D[0:modelContext.getMethodCount(), :]
        PD = PD - np.absolute(PD)
        PD = PD / 2
        PD = PD.astype('int32')

        (rows, cols) = PD.nonzero()

        candidateList = blist.sortedlist([], key=lambda (fromClassIdx,methodIdx,toClassIdx,delta): delta)

        for i in xrange(len(rows)):
            val = D[rows[i], cols[i]]
            fromClassIdx = modelContext.getOwnerClass(rows[i])
            candidateList.add( (fromClassIdx, rows[i], cols[i], val) )

            self.adjustMatrix[rows[i], cols[i]] = self.adjustMatrix[rows[i], cols[i]] + 1.31

            if maxCandidate > 0 and len(candidateList) > maxCandidate:
                candidateList.pop(-1)

        candidateIterator = ARDeltaCandidateIterator(candidateList)

        return candidateIterator
    def getType(self):
        return "delta"
