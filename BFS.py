from commonClasses import *

class BfsBoard(Board):
    def solve(self):
        seenStateCount = 0
        uniqueStateCount = 0
        firstState = Node(self.state, None, None)
        frontier = QueueFrontier()
        frontier.add(firstState)
        self.explored = set()
        self.explored.add(firstState.state)

        while True:

            if frontier.empty():
                return

            node = frontier.remove()
            
            result = self.findChildsFromPossibleMoves(node)
            for child in result:
                state = child.state
                seenStateCount += 1
                if not state in self.explored:
                    if len(state.oneScore) == 0 and len(state.twoScore) == 0:
                        return child, seenStateCount, uniqueStateCount
                    frontier.add(child)
                    self.explored.add(child.state)
                    uniqueStateCount += 1

def main():
    m = BfsBoard(sys.argv[1])
    startTime = time.time()
    node, seenStateCount, uniqueStateCount = m.solve()
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
    print("Time with BFS : %f s" % (totalTime))

main()