import sys
import operator
import time
import math
import heapq
import copy

from commonClasses import State, Snake, QueueFrontier, Board, Explored, ExploredNode

class Node():
    def __init__(self, state, parent, action, guess, pathCost):
        self.state = state
        self.parent = parent
        self.action = action
        self.guess = guess
        self.pathCost = pathCost
        self.heuristic = self.guess + self.pathCost

    def __lt__(self, other):
        return self.heuristic < other.heuristic

class SortedFrontier(QueueFrontier):
    def add(self, node):
        heapq.heappush(self.frontier, node)

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = heapq.heappop(self.frontier)
            return node

class AstarBoard(Board):
    def findMinDistance(self, seed, head):
        x = min(abs(seed[0] - head[0]) , abs(self.width-abs(seed[0] - head[0])))
        return x
    
    def guessCost(self, state, alpha):
        headPos = state.snake.getHead()
        length = len(state.snake.getPos())
        oneScore = state.oneScore
        twoScore = state.twoScore
        heuristic = -math.inf
        for seed in oneScore.union(twoScore):
            distance = self.findMinDistance(seed, headPos)
            if distance > heuristic:
                heuristic = distance
        return alpha * heuristic

    def findChildsFromPossibleMoves(self, node, alpha):
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
                child = self.initChild(newState, node, action, self.guessCost(newState, alpha), node.pathCost+1)
                result.append(child)
        return result

    def initChild(self, newState, node, action, guess, pathCost):
        return Node(newState, node, action, guess, pathCost)

    def solve(self, alpha):
        seenStateCount = 0
        uniqueStateCount = 0
        firstState = Node(self.state, None, None, self.guessCost(self.state, alpha), 0)
        frontier = SortedFrontier()
        frontier.add(firstState)
        explored = Explored()
        new = ExploredNode(0, firstState.state.toString())
        explored.add(new)
        while True:

            if frontier.empty():
                return

            node = frontier.remove()
            if len(node.state.oneScore) == 0 and len(node.state.twoScore) == 0:
                return child, seenStateCount, uniqueStateCount
            cost = node.pathCost
            result = self.findChildsFromPossibleMoves(node, alpha)
            for child in result:
                state = child.state
                seenStateCount += 1
                if not explored.contains(ExploredNode(cost+1, state.toString())):
                    frontier.add(child)
                    explored.add(ExploredNode(cost+1, state.toString()))
                    uniqueStateCount += 1

def main():
    m = AstarBoard(sys.argv[1])
    startTime = time.time()
    node, seenStateCount, uniqueStateCount = m.solve(float(sys.argv[2]))
    endTime = time.time()
    totalTime = endTime - startTime
    actions = []
    while node.parent is not None:
        actions.append(node.action)
        node = node.parent
    actions.reverse()
    solution = (actions)
    print(solution)
    print("Steps to goal :: ", len(solution))
    print("Count of seen states :: ",seenStateCount)
    print("Count of unique states ::",uniqueStateCount)
    print("Time with ASTAR : %f s" % (totalTime))

main()