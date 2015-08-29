import json
import os
import sys
import time
import datetime
import thread

from ARClass import *
from numpy import *
import scipy.sparse as sp
import array as ar
import copy

class ARModelContext:
    membershipMatrix = None
    ownershipMap = None
    classList = []
    model = None

    def __init__(self, model, membershipMatrix, classList, ownershipMap):
        self.membershipMatrix = membershipMatrix.copy()
        self.classList = []
        self.model = model
        self.ownershipMap = copy.copy(ownershipMap)
        for clazz in classList:
            self.classList.append(clazz.copy())

    def copy(self):
        ret = ARModelContext(self.model, self.membershipMatrix, self.classList, self.ownershipMap)
        return ret

    def moveMethod(self, fromClassIdx, methodIdx, toClassIdx):
        fromClass = self.classList[fromClassIdx]
        toClass = self.classList[toClassIdx]
        fromClass.moveMethod(toClass, methodIdx)
        self.membershipMatrix[methodIdx, fromClassIdx] = 0
        self.membershipMatrix[methodIdx, toClassIdx] = 0
        self.ownershipMap[methodIdx] = toClassIdx

    def applyMoveMethod(self, candidate):
        (fromClassIdx, methodIdx, toClassIdx, _) = candidate
        self.moveMethod(fromClassIdx, methodIdx, toClassIdx)

    def unapplyMoveMethod(self, candidate):
        (fromClassIdx, methodIdx, toClassIdx, _) = candidate
        self.moveMethod(toClassIdx, methodIdx, fromClassIdx)

# accessor
    def getMembershipMatrix(self):
        return self.membershipMatrix
    def getOwnerClass(self, entityIdx):
        return self.ownershipMap[entityIdx]
    def getClassCount(self):
        return len(self.classList)
    def getClassInstance(self, classIdx):
        return self.classList[classIdx]
    def getClassList(self):
        return self.classList

# delegated methods
    def getMethodCallMatrix(self):
        return self.model.getMethodCallMatrix()
    def getMethodCallBiMatrix(self):
        return self.model.getMethodCallBiMatrix()
    def getMethodCallWeightMatrix(self):
        return self.model.getMethodCallWeightMatrix()
    def getFieldAccessMatrix(self):
        return self.model.getFieldAccessMatrix()
    def getFieldAccessBiMatrix(self):
        return self.model.getFieldAccessBiMatrix()
    def getCohesionMatrix(self):
        return self.model.getCohesionMatrix()
    def getMethodCount(self):
        return self.model.getMethodCount()
    def getFieldCount(self):
        return self.model.getFieldCount()
    def getEntityCount(self):
        return self.model.getEntityCount()
    def getEntityName(self, entityIdx):
        return self.model.getEntityName(entityIdx)
    def getEntityList(self):
        return self.model.getEntityList()
    def getCalleeListFromMethod(self, callerIdx):
        return self.model.getCalleeListFromMethod(callerIdx)
    def getFieldListFromMethod(self, methodIdx):
        return self.model.getFieldListFromMethod(methodIdx)
    def getMethodListFromField(self, fieldIdx):
        return self.model.getMethodListFromField(fieldIdx)
    def getProjectName(self):
        return self.model.getProjectName()
