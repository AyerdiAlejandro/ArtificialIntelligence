# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()
        print legalMoves

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"
            
        print legalMoves[chosenIndex]
        #while legalMoves[chosenIndex] == "Stop":
         #   chosenIndex = 2
        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        print "/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/"
        print successorGameState.getScore()
        print newPos
        print newFood
        print newGhostStates[0].getPosition()
        print newScaredTimes[0]
        print len(newFood[0])
        print successorGameState.getWalls()[newPos[0]+1][newPos[1]]
    
        if newScaredTimes[0]==0:
            if manhattanDistance(newPos,newGhostStates[0].getPosition()) < 2:
                return 10
            else:
                if len(successorGameState.getCapsules()) != 0:
                    return successorGameState.getScore()-manhattanDistance(newPos,newGhostStates[0].getPosition())-manhattanDistance(newPos,successorGameState.getCapsules()[0])
                else:
                    return successorGameState.getScore()-manhattanDistance(newPos,newGhostStates[0].getPosition()) 
        elif newScaredTimes[0]<40 and newScaredTimes[0]>10:
            return successorGameState.getScore()-manhattanDistance(newPos,newGhostStates[0].getPosition())
        
        
     
        
        return successorGameState.getScore()
       
        
     

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
    
        bestScore,bestAction=self.maxFunction(gameState,self.depth)

        return bestAction

    def maxFunction(self,gameState,depth):
        if depth==0 or gameState.isLose() or gameState.isWin():
            return self.evaluationFunction(gameState),

        legalMoves=gameState.getLegalActions()
        scores=[]
        for action in legalMoves:
            scores.append([self.minFunction(gameState.generateSuccessor(self.index,action),1,depth)])              
        bestScore=max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = bestIndices[0]
        return bestScore,legalMoves[chosenIndex]

    def minFunction(self,gameState,agent, depth):  
        if depth==0 or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState),
        legalMoves=gameState.getLegalActions(agent)
        scores=[]
        if(agent!=gameState.getNumAgents()-1):
            for action in legalMoves:
                scores.append([self.minFunction(gameState.generateSuccessor(agent,action),agent+1,depth)])
        else:
            for action in legalMoves:
                scores.append([self.maxFunction(gameState.generateSuccessor(agent,action),(depth-1))])
        minScore=min(scores)
        worstIndices = [index for index in range(len(scores)) if scores[index] == minScore]
        chosenIndex = worstIndices[0]
        return minScore, legalMoves[chosenIndex]
    

class AlphaBetaAgent(MultiAgentSearchAgent):
    

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
    
        bestScore,bestAction=self.maxFunction(gameState,self.depth,-999999,999999)

        return bestAction

    def maxFunction(self,gameState,depth,alpha,beta):
        if depth==0 or gameState.isLose() or gameState.isWin():
            return self.evaluationFunction(gameState),

        legalMoves=gameState.getLegalActions()
        scores=[]
        for action in legalMoves:
            scores.append([self.minFunction(gameState.generateSuccessor(self.index,action),1,depth,alpha,beta)])              
            
        bestScore=max(scores)
        if bestScore>=beta:
            bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
            chosenIndex = bestIndices[0]
            return bestScore,legalMoves[chosenIndex]            
        alpha=max(alpha,bestScore)           
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = bestIndices[0]
        return bestScore,legalMoves[chosenIndex]

    def minFunction(self,gameState,agent, depth,alpha,beta):  
        if depth==0 or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState),
        legalMoves=gameState.getLegalActions(agent)
        scores=[]
        if(agent!=gameState.getNumAgents()-1):
            for action in legalMoves:
                scores.append([self.minFunction(gameState.generateSuccessor(agent,action),agent+1,depth,alpha,beta)])                   
        else:
            for action in legalMoves:
                scores.append([self.maxFunction(gameState.generateSuccessor(agent,action),(depth-1),alpha,beta)])
        minScore=min(scores)
        
        if minScore<=alpha:
            worstIndices = [index for index in range(len(scores)) if scores[index] == minScore]
            chosenIndex = worstIndices[0]
            return minScore, legalMoves[chosenIndex]
        beta=min(beta,minScore)
        worstIndices = [index for index in range(len(scores)) if scores[index] == minScore]
        chosenIndex = worstIndices[0]
        return minScore, legalMoves[chosenIndex]
   

   
        
        
    

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
    
        bestScore,bestAction=self.maxFunction(gameState,self.depth)

        return bestAction

    def maxFunction(self,gameState,depth):
        if depth==0 or gameState.isLose() or gameState.isWin():
            return self.evaluationFunction(gameState),

        legalMoves=gameState.getLegalActions()
        scores=[]
        for action in legalMoves:
            scores.append([self.minFunction(gameState.generateSuccessor(self.index,action),1,depth)])   
        
        print scores
        bestScore=max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = bestIndices[0]
        return bestScore,legalMoves[chosenIndex]

    def minFunction(self,gameState,agent, depth):  
        if depth==0 or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState),
        legalMoves=gameState.getLegalActions(agent)
        scores=[]
        if(agent!=gameState.getNumAgents()-1):
            for action in legalMoves:
                scores.append([self.minFunction(gameState.generateSuccessor(agent,action),agent+1,depth)])
        else:
            for action in legalMoves:
                scores.append([self.maxFunction(gameState.generateSuccessor(agent,action),(depth-1))])
                       
        minScore=min(scores)
        worstIndices = [index for index in range(len(scores)) if scores[index] == minScore]
        chosenIndex = worstIndices[0]
        return minScore, legalMoves[chosenIndex]

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

