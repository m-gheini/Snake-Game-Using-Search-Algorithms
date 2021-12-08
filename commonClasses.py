import sys
import operator
import time
import math
import heapq
import copy

class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action

class State():
    def __init__(self, snake, oneScore, twoScore):
        self.snake = snake
        self.oneScore = oneScore
        self.twoScore = twoScore

    def isSame(self, state):
        return (self.snake.isSame(state.snake) and self.oneScore == state.oneScore and self.twoScore == state.twoScore)

    def toString(self):
        return (tuple(self.snake.getPos()), tuple(self.oneScore), tuple(self.twoScore))

    def __hash__(self):
        return hash(tuple(self.snake.body)) + hash(tuple(self.oneScore)) + hash(tuple(self.twoScore))

    def __eq__(self, other):
        return self.snake == other.snake and self.oneScore == other.oneScore and self.twoScore == other.twoScore

class Snake():
    def __init__(self, body):
        self.body = body

    def getPos(self):
        return self.body

    def getHead(self):
        return self.body[0]

    def getBody(self):
        return self.body[:-1]

    def getTail(self):
        return self.body[-1]

    def isSame(self, snake):
        return (self.getPos() == snake.getPos())

    def __hash__(self):
        return hash(tuple(self.body))

    def __eq__(self, other):
        return self.getPos() == other.getPos()

class QueueFrontier():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def containsState(self, state):
        return any(node.state.isSame(state) for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node

class Board():
    def __init__(self, filename):
        inFile = open(filename,"r")
        lines = inFile.readlines()
        list = []
        self.oneScore = set()
        self.twoScore = set()
        for line in lines:
            list.append(line.strip())
        self.height = int(list[0][0:list[0].index(",")])
        self.width = int(list[0][list[0].index(",")+1:len(list[0])])
        head = (int(list[1][0:list[1].index(",")]), int(list[1][list[1].index(",")+1:len(list[1])])) 
        self.snake = Snake([head])
        seedCnt = list[2]
        for i in range(int(seedCnt)):
            firstComma = list[i+3].find(",")
            secondComma = list[i+3].find(",", firstComma+1, len(list[i+3]))
            x = list[i+3][0:firstComma]
            y = list[i+3][firstComma+1:secondComma]
            score = list[i+3][secondComma+1:len(list[i+3])]
            if(score == "1"):
                self.oneScore.add((int(x),int(y)))
            else:
                self.twoScore.add((int(x),int(y)))
        self.state = State(self.snake, self.oneScore, self.twoScore)
        self.seeds = self.state.oneScore.union(self.state.twoScore)

    def findChildsFromPossibleMoves(self, node):
        state = node.state
        row, col = state.snake.getHead()
        allMoves = [
            ("U", (row-1, col)),
            ("D", (row + 1, col)),
            ("L", (row, col - 1)),
            ("R", (row, col + 1))
        ]
        result = []
        for action, newHeadPos in allMoves:
            newHeadPos = self.validateNewHeadPos(newHeadPos)
            newSnake = self.move(node, newHeadPos)
            if (newHeadPos not in state.snake.getBody()) and not (newHeadPos == state.snake.getTail() and (len(newSnake.getPos()) == 2)):
                newOneScore, newTwoScore = self.eat(node, newHeadPos)
                newState = State(newSnake, newOneScore, newTwoScore)
                child = self.initChild(newState, node, action)
                result.append(child)
        return result

    def initChild(self, newState, node, action):
        return Node(newState, node, action)

    def validateNewHeadPos(self, newHeadPos):
        if newHeadPos[0] == -1:
            newHeadPos = (self.height - 1, newHeadPos[1])
        elif newHeadPos[0] == self.height:
            newHeadPos = (0, newHeadPos[1])
        elif newHeadPos[1] == -1:
            newHeadPos = (newHeadPos[0], self.width - 1)
        elif newHeadPos[1] == self.width:
            newHeadPos = (newHeadPos[0], 0)
        return newHeadPos

    def move(self, node, newHeadPos):
        if not node.parent == None:
            parentState = node.parent.state
        state = node.state
        newState = State(snake = state.snake, oneScore = state.oneScore.copy(), twoScore = state.twoScore.copy())
        ate = False
        if node.parent == None:
            ate = False
        elif state.snake.getHead() in parentState.oneScore or state.snake.getHead() in parentState.twoScore:
            ate = True

        oldBody = state.snake.getPos().copy()
        oldBody.insert(0, newHeadPos)
        if not ate:
            oldBody.pop(-1)
        return Snake(oldBody)

    def eat(self, node, newHeadPos):
        state = node.state
        newState = State(snake = state.snake, oneScore = state.oneScore.copy(), twoScore = state.twoScore.copy())
        if newHeadPos in state.oneScore:
            newState.oneScore.discard(newHeadPos)
        elif newHeadPos in state.twoScore:
            newState.twoScore.discard(newHeadPos)
            newState.oneScore.add(newHeadPos)
        return newState.oneScore, newState.twoScore

    def solve(self):
        return

    def isGoal(self, state):
        return len(state.oneScore) == 0 and len(state.twoScore) == 0

    def print(self):
        print(self.height)
        print(self.width)
        print(self.snake.getHead())
        print(self.oneScore)
        print(self.twoScore)

class ExploredNode():
    def __init__(self, depth, state):
        self.depth = depth
        self.state = state

    def __hash__(self):
        return hash(tuple(self.state))

    def __eq__(self, other):
        return self.state == other.state and self.depth <= other.depth

class Explored():
    def __init__(self):
        self.explored = set()

    def add(self, exploredOne):
        self.explored.add(exploredOne)

    def contains(self, new):
        return new in self.explored
