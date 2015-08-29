import sys

class ARSearchEngine:
        
    def __init__(self, modelContext, selector, policy, fitnessFunc, maxIteration, logger):
        self.modelContext = modelContext
        self.selector = selector
        self.policy = policy
        self.fitnessFunc = fitnessFunc
        self.maxIteration = maxIteration
        self.logger = logger.createContext(selector.getType(), policy.getType(), fitnessFunc.getType())


    def run(self):
        modelContext = self.modelContext        
        selector = self.selector
        policy = self.policy
        fitnessFunc = self.fitnessFunc
        logger = self.logger

        #fitnessFunc.initialize??

        policy.setAscendingRank(fitnessFunc.isAscendingRank())

        for iteration in xrange(self.maxIteration):
            candidateIterator = selector.getIterator(modelContext, policy.getMaxCandidateCount())
            policyContext = policy.createContext()
            sys.stdout.write('?')

            cidx = 0

            while candidateIterator.hasCandidate():
                candidate = candidateIterator.candidate()
                if candidate == None:
                    break
                modelContext.applyMoveMethod(candidate)
                fitness = fitnessFunc.calculate(modelContext)
                sys.stdout.write('.')

                logger.logc(iteration, cidx, candidate, fitness)
                cidx = cidx + 1

                shouldBeStopped = policyContext.register(fitness, candidate)
                modelContext.unapplyMoveMethod(candidate)
                if shouldBeStopped:
                    break

            (winner, fitness) = policyContext.elect()
            sys.stdout.write('!')
            logger.logs(iteration, winner, fitness)

            if winner:
                modelContext.applyMoveMethod(winner)
            else:
                break
