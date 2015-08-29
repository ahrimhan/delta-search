import config
import sys
from ARModel import *
from ARDeltaMatrixSelector import *
from ARRandomSelector import *
from FirstPolicy import *
from BestPolicy import *
from EPM import *
from MPC import *
from MPCWeight import *
from MSC import *
from Connectivity import *
from Logger import *
from ARSearchEngine import *
import datetime

selectorMap = {
    "delta" : ARDeltaMatrixSelector(),
    "random" : ARRandomSelector()
}

policyMap = {
    "first" : FirstPolicy(),
    "best" : BestPolicy()
}

fitnessMap = {
    "epm" : EPM(),
    "mpc" : MPC(),
    "mpcw" : MPCWeight(),
    "msc" : MSC(),
    "connectivity" : Connectivity()
}

def main():
    if not( len(sys.argv) == 3 or len(sys.argv) == 2 ):
        print "Usage: %s [model_json_file] [output_path]" % sys.argv[0]
        exit()
    modelfile = sys.argv[1]

    if len(sys.argv) == 3:
        base_path = sys.argv[2]
    else:
        base_path = "."

    model = ARModel()
    modelContext = model.load(modelfile)
    logger = Logger(base_path, model.getProjectName(), modelContext.getClassList(), modelContext.getEntityList())

    for fitnessList in config.fitnessList:
        for policyName in config.policyList:
            for selectorName in config.selectorList:
                print "Starting for %s %s %s" % (selectorName, policyName, fitnessList)
                selector = selectorMap[selectorName]
                policy = policyMap[policyName]
                fitnessFunc = fitnessMap[fitnessList]
                searchEngine = ARSearchEngine(modelContext.copy(), selector, policy, fitnessFunc, config.maxIteration, logger)
                searchEngine.run()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print "Terminating program..."
