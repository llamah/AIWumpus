import random
import os

# variables
empty = "."
agent = "a"
pit = "p"
gold = "g"
wumpus = "w"
visited = "v"
safe = "s"
breeze = "Br"
stench = "St"
glitter = "Gl"
scream = "Sc"
agentDead = "DEAD"
xSize = 7
ySize = 4
goldCollected = False
running = True
stack = []

envToPercept = {pit: breeze, wumpus: stench}

environment = [
    [empty, empty, empty, pit, empty, pit, wumpus],
    [empty, empty, pit, empty, empty, gold, empty],
    [empty, empty, empty, empty, empty, empty, empty],
    [empty, empty, empty, empty, empty, empty, empty],
]

# This records only breezes, since those are the only environmental factors that remain constant.
recordedPercepts = [
    [empty, empty, empty, empty, empty, empty, empty],
    [empty, empty, empty, empty, empty, empty, empty],
    [empty, empty, empty, empty, empty, empty, empty],
    [empty, empty, empty, empty, empty, empty, empty],
]

agentX = 0
agentY = 0
prevAgentX = 0
prevAgentY = 0


def printEnvironment(env):
    for row in range(len(env)):
        for col in range(len(env[row])):
            if (row, col) == (agentX, agentY):
                print(agent, " ", end="")
            else:
                print(env[row][col], " ", end="")
        print()


def checkPercepts():
    global agentX
    global agentY
    currentPercepts = []
    nearbyCells = [
        (agentX - 1, agentY),  # up
        (agentX, agentY + 1),  # right
        (agentX + 1, agentY),  # down
        (agentX, agentY - 1),  # left
    ]
    if environment[agentX][agentY] == wumpus or environment[agentX][agentY] == pit:
        agentX = 0
        agentY = 0
        running = False
        return agentDead
    for nearby in nearbyCells:
        if validLocation(nearby[0], nearby[1]):
            for percept in envToPercept:
                if environment[nearby[0]][nearby[1]] == percept:
                    currentPercepts.append(envToPercept[percept])
    return currentPercepts


def recordPercepts(percepts):
    if breeze in percepts:
        recordedPercepts[agentX][agentY] = breeze
        #print("Recorded Breeze at ", x, y)
    elif len(percepts) == 0:
        recordedPercepts[agentX][agentY] = visited
        #print("Visited space recorded at ", x, y)
        nearbyCells = [
            (agentX - 1, agentY),  # up
            (agentX, agentY + 1),  # right
            (agentX + 1, agentY),  # down
            (agentX, agentY - 1),  # left
        ]
        for cell in nearbyCells:
            if (
                validLocation(cell[0], cell[1])
                and (recordedPercepts[cell[0]][cell[1]] is empty)
            ):
                recordedPercepts[cell[0]][cell[1]] = safe
                #print("Safe cell recorded at ", cell)


def isDangerous(x, y):
    if recordedPercepts[x][y] is safe or recordedPercepts[x][y] is visited:
        return False
    else:
        return True


def validLocation(x, y):
    return 0 <= x <= len(environment) - 1 and 0 <= y <= len(environment[0]) - 1


def checkGoal():
    global goldCollected
    if environment[agentX][agentY] == gold:
        goldCollected = True
        environment[agentX][agentY] = empty


def moveAgent():
    # Takes CURRENT position, then previous position

    # This is bad, will switch to stack
    global agentX
    global agentY
    global prevAgentX
    global prevAgentY
    newX = agentX
    newY = agentY
    nearbyCells = [
        (agentX - 1, agentY),  # up
        (agentX, agentY + 1),  # right
        (agentX + 1, agentY),  # down
        (agentX, agentY - 1),  # left
    ]
    if not goldCollected:

        if recordedPercepts[agentX][agentY] is breeze:
            loc = stack.pop()
            newX, newY = loc[0], loc[1]
        else:
            shouldMove = False

            while not shouldMove:
                cell = nearbyCells[random.randint(0, 3)]
                if validLocation(cell[0], cell[1]) and not isDangerous(
                    cell[0], cell[1]
                ):
                    newX, newY = cell[0], cell[1]
                    shouldMove = True
                    stack.append((agentX, agentY))
    else:
        newX, newY = stack.pop()
    prevAgentX = agentX
    prevAgentY = agentY
    agentX = newX
    agentY = newY


iter = 0
clear = lambda: os.system("cls")
cont = True
if __name__ == "__main__":
    while running:
        iter += 1
        print("iter", iter)
        printEnvironment(environment)
        print()
        recordPercepts(checkPercepts())
        moveAgent()
        checkGoal()
        #printEnvironment(recordedPercepts)
        #print(stack)
        #print(goldCollected)
        if running:

            if goldCollected and agentX == 0 and agentY == 0:
                print("ESCAPED WITH GOLD")
                running = False
            else:
                clear()
