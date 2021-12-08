from commonClasses import *

class StackFrontier(QueueFrontier):
    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node

class IdsBoard(Board):
    def iterate(self, depth, seen, unique):
        seenStateCount = seen
        uniqueStateCount = unique
        firstState = Node(self.state, None, None)
        frontier = StackFrontier()
        frontier.add(firstState)
        nodeDepth = [0]
        explored = Explored()
        new = ExploredNode(0, firstState.state.toString())
        explored.add(new)

        while True:

            if frontier.empty():
                return seenStateCount, uniqueStateCount

            node = frontier.remove()
            actualDepth = nodeDepth.pop()
            if actualDepth < depth:
                result = self.findChildsFromPossibleMoves(node)
                for child in result:
                    state = child.state
                    seenStateCount += 1
                    if not explored.contains(ExploredNode(actualDepth+1, state.toString())):
                        if len(child.state.oneScore) == 0 and len(child.state.twoScore) == 0:
                            return child, seenStateCount, uniqueStateCount
                        frontier.add(child)
                        nodeDepth.append(actualDepth+1)
                        explored.add(ExploredNode(actualDepth+1, state.toString()))
                        if actualDepth == depth - 1:
                            uniqueStateCount += 1
            else:
                continue

    def solve(self):
        depth = 1
        seen = 0
        unique = 0
        while True:
            result = self.iterate(depth, seen, unique)
            if len(result) == 2:
                depth += 1
                seen = result[0]
                unique = result[1]
            else:
                return result

def main():
    m = IdsBoard(sys.argv[1])
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
    print("Time with IDS : %f s" % (totalTime))
 
main()