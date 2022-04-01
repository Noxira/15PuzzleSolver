from gameboardIO import *
from copy import deepcopy
import time

def approxDistToSolution(board: List[List[int]]) -> int:
    """
        returns the approximate distance a given gameboard state to the solution state.
    """
    i = int(1)
    invalidElPlaced = int(0)
    for row in board:
        for el in row:
            if(el != 16 and el != i):
                invalidElPlaced += 1
            i += 1
    return invalidElPlaced

def findIndex(board: List[List[int]], search: int) -> Tuple[int, int]:
    """
        finds a given integer "search" in the gameboard and return its index position. \n
        returns a tuple of the form (col, row). \n
        starting index is (0,0).
    """
    x = int(0)
    y = int(0)
    found = bool(False)
    for row in board:
        for el in row:
            if (el == search):
                found = True
                break
            x += 1
        if(found):
            break
        y += 1
        x = int(0)
    return (x, y)

def getPossibleDirection(board: List[List[int]]) -> List[str]:
    """
        returns a list of all possible direction/moves from a given gameboard state.\n
        default list is ["up", "down", "left", "right"]
    """
    direction = []
    blankIdx = findIndex(board, 16)
    if(blankIdx[1] != 0):
        direction.append("up")
    if(blankIdx[1] != 3):
        direction.append("down")
    if(blankIdx[0] != 0):
        direction.append("left")
    if(blankIdx[0] != 3):
        direction.append("right")
    return direction


def moveBlankSlot(prevBoard: List[List[int]], direction: str) -> List[List[int]]:
    """
        DOES NOT CHECK IF A GIVEN DIRECTION/MOVE IS VALID. \n
        moves the blank slot (the integer 16) in the given direction.
    """
    board = deepcopy(prevBoard)
    blankIdx = findIndex(board, 16)
    if(direction == "up"):
        board[blankIdx[1]][blankIdx[0]] = board[blankIdx[1] - 1][blankIdx[0]]
        board[blankIdx[1] - 1][blankIdx[0]] = 16
    elif(direction == "down"):
        board[blankIdx[1]][blankIdx[0]] = board[blankIdx[1] + 1][blankIdx[0]]
        board[blankIdx[1] + 1][blankIdx[0]] = 16
    elif(direction == "left"):
        board[blankIdx[1]][blankIdx[0]] = board[blankIdx[1]][blankIdx[0] - 1]
        board[blankIdx[1]][blankIdx[0] - 1] = 16
    elif(direction == "right"):
        board[blankIdx[1]][blankIdx[0]] = board[blankIdx[1]][blankIdx[0] + 1]
        board[blankIdx[1]][blankIdx[0] + 1] = 16
    return board

def isSolvable(board: List[List[int]]) -> bool:
    """
        returns True if the given gameboard is solvable, False otherwise.
    """
    sumKurangDari = int(0)
    flatBoard = []
    for row in board:
        for el in row:
            flatBoard.append(el)
    for i in range(len(flatBoard)):
        for j in range(i, len(flatBoard)):
            if(flatBoard[j] < flatBoard[i]):
                sumKurangDari += 1
    if(sum(list(findIndex(board, 16))) % 2 == 1):
        sumKurangDari += 1
    return sumKurangDari % 2 == 0

def sortByDistPrio(nodes: List[Tuple[List[List[int]], List[str], int, int]]) -> List[Tuple[List[List[int]], List[str], int, int]]:
    """
        sort the tuple consisting of active nodes with the tuple consisting lowest (depth + approx Dist to goal) goes first. \n
        Tuple content:
            (
                gameboard[[]],
                previous moves[],
                depth,
                distApprox,
            )
    """
    nodes.sort(key = lambda pr: pr[2] + pr[3])

def mirrorMove(prevMove: str) -> str:
    """
        returns the mirror move of the given move.
    """
    if(prevMove == "up"):
        return "down"
    elif(prevMove == "down"):
        return "up"
    elif(prevMove == "left"):
        return "right"
    elif(prevMove == "right"):
        return "left"

def solveGameboard(board: List[List[int]]):
    """
		Main program to solve a given gameboard.\n
		Will either:
			A. if the gameboard is solvable, returns a tuple with the content:
			(
				moveToSolution[],
				timeTakenInSeconds,
                nodesRaised,
			)
			
			B. Raise exception if the gameboard takes too many iteration to solve
			C. Raise exception if the gameboard cannot be solved
    """
    if (isSolvable(board)):
        startTime = time.time()
        solved = bool(False)
        # initialize nodes
        nodes = []

        # add base node (root)
        nodes.append((board, [], 0, approxDistToSolution(board)))

        # iteration limit
        iteration = int(0)

        # initialize nodes raised, from base node = 1
        nodesRaised = int(1)

        # entering loop
        while(not solved):
            iteration += 1

            # get the node we want to check (highest priority, lowest heuristic cost)
            checkNode = nodes.pop(0)

            # get possible moves
            possibleMoves = getPossibleDirection(checkNode[0])
            if (len(checkNode[1]) != 0):
                if mirrorMove(checkNode[1][0]) in possibleMoves:
                    possibleMoves.remove(mirrorMove(checkNode[1][0]))

            # iterate through possible moves to make new active nodes
            for move in possibleMoves:
                newBoard = moveBlankSlot(checkNode[0], move)
                nodes.append((newBoard, [move] + checkNode[1], checkNode[2] + 1, approxDistToSolution(newBoard)))
                nodesRaised += 1
                if (approxDistToSolution(newBoard)) == 0:
                    endTime = time.time()
                    solution = [move] + checkNode[1]
                    solution = solution[::-1]
                    timeTaken = endTime - startTime
                    return (solution, timeTaken, nodesRaised)

            # stop if iteration gets too big
            if (iteration > 20000):
                raise Exception("Iteration limit reached")
                
            # sort       
            sortByDistPrio(nodes)
    else:
        raise Exception("The given board is not solvable")