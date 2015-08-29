import json
import os
import sys
import time
import datetime
import thread
import array
import json

from ARClass import *
from numpy import *
import scipy.sparse as sp
from ARModelContext import *

class Unbuffered(object):
   def __init__(self, stream):
       self.stream = stream
   def write(self, data):
       self.stream.write(data)
       self.stream.flush()
   def __getattr__(self, attr):
       return getattr(self.stream, attr)

sys.stdout = Unbuffered(sys.stdout)


class ARModel:
    def __init__(self):
        self.methodCallMatrix = None
        self.methodCallBiMatrix = None
        self.methodCallWeightMatrix = None
        self.fieldAccessMatrix = None
        self.fieldAccessBiMatrix = None
        self.cohesionMatrix = None
        self.entityList = []
        self.classList = []
        self.methodCount = 0;
        self.entityCount = 0;

        self.methodCallMap = []
        self.fieldAccessMap = []
        self.fieldAccessReverseMap = []
        self.projectName = "Unknown"

    def getMethodCallMatrix(self):
        return self.methodCallMatrix

    def getMethodCallBiMatrix(self):
        return self.methodCallBiMatrix

    def getMethodCallWeightMatrix(self):
        return self.methodCallWeightMatrix

    def getFieldAccessMatrix(self):
        return self.fieldAccessMatrix

    def getFieldAccessBiMatrix(self):
        return self.fieldAccessBiMatrix

    def getCohesionMatrix(self):
        return self.cohesionMatrix

    def getMethodCount(self):
        return self.methodCount;

    def getFieldCount(self):
        return self.fieldCount;

    def getEntityCount(self):
        return len(self.entityList)

    def getEntityName(self, entityIdx):
        return self.entityList[entityIdx]

    def getEntityList(self):
        return self.entityList

    def getCalleeListFromMethod(self, callerIdx):
        return self.methodCallMap[callerIdx]

    def getFieldListFromMethod(self, methodIdx):
        return self.fieldAccessMap[methodIdx]

    def getMethodListFromField(self, fieldIdx):
        return self.fieldAccessReverseMap[fieldIdx]

    def getProjectName(self):
        return self.projectName

    def load(self, filename):
        raw_data = open(filename)
        head, tail = os.path.split(filename)
        project, jsonfile = tail.rsplit(".", 1)
        print "filename: %s" % filename
        print "project: %s" % project
        self.projectName = project
         
        print "Json parsing...",
        parsed_data = json.load(raw_data)
        raw_data.close()
        print "done"

        classIndex = 0
        classList = []


        print "Creating basic lists...",
        for class_name in parsed_data["classes"]:
            clazz = ARClass()
            clazz.setIndex(classIndex)
            clazz.setName(class_name)
            classList.append(clazz)
            classIndex = classIndex + 1

        self.methodCount = 0
        for i in range(0, len(parsed_data["methods"]), 2):
            self.entityList.append(parsed_data["methods"][i])
            self.methodCount = self.methodCount + 1

        self.fieldCount = 0
        for i in range(0, len(parsed_data["fields"]), 2):
            self.entityList.append(parsed_data["fields"][i])
            self.fieldCount = self.fieldCount + 1
        print "done"


        print "Allocating matrix...",
        membershipMatrix = zeros((len(self.entityList), len(classList)), dtype='int32')
        methodCallMatrix = zeros((len(self.entityList), len(self.entityList)), dtype='int32')
        methodCallBiMatrix = zeros((len(self.entityList), len(self.entityList)), dtype='int32')
        methodCallWeightMatrix = zeros((len(self.entityList), len(self.entityList)), dtype='int32')
        fieldAccessMatrix = zeros((len(self.entityList), len(self.entityList)), dtype='int32')
        fieldAccessBiMatrix = zeros((len(self.entityList), len(self.entityList)), dtype='int32')
        cohesionMatrix = zeros((len(self.entityList), len(self.entityList)), dtype='int32')

        methodCallMap = [set()] * self.methodCount
        fieldAccessMap = [set()] * self.methodCount
        fieldAccessReverseMap = [set()] * len(self.entityList)
        ownershipMap = ar.array('i', [-1] * len(self.entityList))
        print "done"

        print "Setting up relationship between methods and fields...",
        entityIndex = 0
        for i in range(1, len(parsed_data["methods"]), 2):
            classIndex = parsed_data["methods"][i]
            classList[classIndex].addMethod(entityIndex)
            membershipMatrix[entityIndex, classIndex] = 1
            ownershipMap[entityIndex] = classIndex
            entityIndex = entityIndex + 1

        for i in range(1, len(parsed_data["fields"]), 2):
            classIndex = parsed_data["fields"][i]
            classList[classIndex].addField(entityIndex)
            membershipMatrix[entityIndex, classIndex] = 1
            ownershipMap[entityIndex] = classIndex
            entityIndex = entityIndex + 1

        for i in range(0, len(parsed_data["methodCalls"]), 2):
            callerIndex = int(parsed_data["methodCalls"][i])
            calleeIndex = int(parsed_data["methodCalls"][i+1])
            methodCallMatrix[callerIndex, calleeIndex] = 1
            methodCallBiMatrix[callerIndex, calleeIndex] = 1
            methodCallBiMatrix[calleeIndex, callerIndex] = 1
            methodCallWeightMatrix[callerIndex, calleeIndex] = methodCallWeightMatrix[callerIndex, calleeIndex] + 1
            #if not callerIndex in methodCallMap:
            #    methodCallMap[callerIndex] = []
            methodCallMap[callerIndex].add(calleeIndex)

        for i in range(0, len(parsed_data["fieldAccess"]), 2):
            callerIndex = int(parsed_data["fieldAccess"][i])
            calleeIndex = int(parsed_data["fieldAccess"][i+1])
            fieldAccessMatrix[callerIndex, calleeIndex] = 1
            fieldAccessBiMatrix[callerIndex, calleeIndex] = 1
            fieldAccessBiMatrix[calleeIndex, callerIndex] = 1
            #if not callerIndex in fieldAccessMap:
            #    fieldAccessMap[callerIndex] = []
            fieldAccessMap[callerIndex].add(calleeIndex)
            #if not calleeIndex in fieldAccessReverseMap:
            #    fieldAccessReverseMap[calleeIndex] = []
            fieldAccessReverseMap[calleeIndex].add(callerIndex)
        print "done"


        print "Creating cohesive relationships.",
        for i in range(0, self.methodCount - 1, 1):
            if (i % int(self.methodCount/10)) == 0:
                sys.stdout.write('.')
            if i in fieldAccessMap:
                for fieldIndex in fieldAccessMap[i]:
                    for j in fieldAccessReverseMap[fieldIndex]:
                        if i != j:
                            cohesionMatrix[i, j] = 1
                            cohesionMatrix[j, i] = 1
        print " done"

        print "Optimizing matrix.",
        self.methodCallMatrix = sp.coo_matrix(methodCallMatrix).tocsr()
        sys.stdout.write('.')
        self.methodCallBiMatrix = sp.coo_matrix(methodCallBiMatrix).tocsr()
        sys.stdout.write('.')
        self.methodCallWeightMatrix = sp.coo_matrix(methodCallWeightMatrix).tocsr()
        sys.stdout.write('.')
        self.fieldAccessMatrix = sp.coo_matrix(fieldAccessMatrix).tocsr()
        sys.stdout.write('.')
        self.fieldAccessBiMatrix = sp.coo_matrix(fieldAccessBiMatrix).tocsr()
        sys.stdout.write('.')
        self.cohesionMatrix = sp.coo_matrix(cohesionMatrix).tocsr()
        sys.stdout.write('.')
        membershipMatrix = sp.coo_matrix(membershipMatrix).tolil()
        print " done"

        print "Setting up model attributes...",
        self.methodCallMap = methodCallMap
        self.fieldAccessMap = fieldAccessMap
        self.fieldAccessReverseMap = fieldAccessReverseMap
        ret = ARModelContext(self, membershipMatrix, classList, ownershipMap)
        print "done"

        return ret


