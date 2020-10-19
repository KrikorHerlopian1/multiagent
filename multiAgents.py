# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

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
        if len(newFood.asList()) == currentGameState.getFood().count():
            res = 99999
            for f in newFood.asList():
                if manhattanDistance(f , newPos) < res :
                    res = manhattanDistance(f, newPos)
        else:
            res = 0
        #impact of ghost surges as the distanse get close
        for ghost in newGhostStates:
            res = res + (5 ** (2 - manhattanDistance(ghost.getPosition(), newPos)))
        return -res

        #return successorGameState.getScore()

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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        def miniMax(state, agentIndex, depth):
            #  minimizing
            if agentIndex == state.getNumAgents():
                # evalute the state, if we have reached  our maximum depth
                if depth == self.depth:
                    return self.evaluationFunction(state)
                # if not start new maximizing with higher depth
                else:
                    return miniMax(state, 0, depth + 1)
            # not minimizing
            else:
                moves = state.getLegalActions(agentIndex)  #counts for index
                # evaluate the state, if no moves
                if len(moves) == 0:
                    return self.evaluationFunction(state)
                # obtain all the miniMax values for the next depth with each node representing possible successor states
                nxt = (miniMax(state.generateSuccessor(agentIndex, mov), agentIndex + 1, depth) for mov in moves)
                # return maximum depth of next depth , if maximizing
                if agentIndex == 0:
                    return max(nxt)
                # return minimum depth of next depth ,if minimizing
                else:
                    return min(nxt)
        # make result the action with the optimal miniMax value found
        #using recursion & function
        result = max(gameState.getLegalActions(0), key=lambda y: miniMax(gameState.generateSuccessor(0, y), 1, 1))
        #return the best action
        return result
        #util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """
            
    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        #util.raiseNotDefined()
        alphaValue = float("-inf")  #  small
        betaValue = float("inf")
        maximumValue = float("-inf")  # big
        bestAction = Directions.STOP  # if maximum met, stop running
    
        for action in gameState.getLegalActions(0):
            #in order to compare,set the next state
            nextState = gameState.generateSuccessor(0, action)
            #set next states value
            nextValue = self.getVal(nextState, 0, 1, alphaValue, betaValue)
            
            if nextValue > maximumValue:  #should be
                maximumValue = nextValue  #temporary var for holding value just to compare
                bestAction = action
            alphaValue = max(alphaValue, maximumValue)
        #return the best action
        return bestAction

    def getVal(self, gameState, currentDepth, agentIndex, alphaValue, betaValue):
        #evaluate state, if we are at  an end state
        if currentDepth == self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        #if pacman max value of current depth considering alpha and beta
        elif agentIndex == 0:
            return self.maximumValue(gameState,currentDepth,alphaValue,betaValue)
        else:  #return minimum of depth considering alpha and beta
            return self.minimumValue(gameState,currentDepth,agentIndex,alphaValue,betaValue)

    def minimumValue(self, gameState, currentDepth, agentIndex, alphaValue, betaValue):
        #small value  for comparison
        minimumValue = float("inf")
        for action in gameState.getLegalActions(agentIndex):
            #if we move on to next state lose ghost
            if agentIndex == gameState.getNumAgents()-1:
            # update minimum value to be the minimum of next depth
                minimumValue = min(minimumValue, self.getVal(gameState.generateSuccessor(agentIndex, action), currentDepth+1, 0, alphaValue, betaValue))
            else:  # otherwise minimum for next agent
                minimumValue = min(minimumValue, self.getVal(gameState.generateSuccessor(agentIndex, action), currentDepth, agentIndex+1, alphaValue, betaValue))
            if minimumValue < alphaValue:
                return minimumValue  #optimal value returned
            betaValue = min(betaValue, minimumValue)
        return minimumValue
        
    def maximumValue(self, gameState, currentDepth, alphaValue, betaValue):
        maximumValue = float("-inf")
        for action in gameState.getLegalActions(0):
            maximumValue = max(maximumValue, self.getVal(gameState.generateSuccessor(0, action), currentDepth, 1, alphaValue, betaValue))
            if maximumValue > betaValue:
                return maximumValue
            alphaValue = max(alphaValue, maximumValue)
        return maximumValue



        
class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        #util.raiseNotDefined()
        def expectimax(state, agentIndex, depth):
            # minimizing and only one ghost
            if agentIndex == state.getNumAgents():
                #  evaluate the state, if its maximum depth.
                if depth == self.depth:
                    return self.evaluationFunction(state)
                # else recurse until maximum depth
                else:
                    return expectimax(state, 0, depth + 1)
            #  minimizing or more ghosts
            else:
                moves = state.getLegalActions(agentIndex)
                #  evaluate the state, if it reached the maximum moves
                if len(moves) == 0:
                    return self.evaluationFunction(state)
                # get the minimax values for successor states
                nxt = (expectimax(state.generateSuccessor(agentIndex, m), agentIndex + 1, depth) for m in moves)

                # return max val of next state if maximizing
                if agentIndex == 0:
                    return max(nxt)
                # return new expectimax value if minimizing
                else:
                    k = list(nxt)
                     #where we average our suboptimal moves
                    return sum(k) / len(k)
    
        # make move with optimal minimax value
        result = max(gameState.getLegalActions(0), key=lambda y: expectimax(gameState.generateSuccessor(0, y), 1, 1))
        # return expectimax results
        return result

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    #util.raiseNotDefined()
    foodPosition = currentGameState.getFood().asList()
    fList = []
    #the pacman position
    position = list(currentGameState.getPacmanPosition())

    for f in foodPosition:
        #finding closest food
        distanceToFood = manhattanDistance(position, f)
        #puting it on list to get it  negative value to represent cost
        fList.append(-1 * distanceToFood)

    #append 0 for finished state,if the list is empty.
    if not fList:
        fList.append(0)

    #really lowest cost
    return currentGameState.getScore() + max(fList)


# Abbreviation
better = betterEvaluationFunction
