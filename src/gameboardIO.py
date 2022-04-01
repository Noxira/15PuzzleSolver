from typing import List
from typing import Tuple
import random

def stringToRow(string) -> List[int]:
    """
        converts a string consisting of integers spaced out into a list of those integers
    """
    return [int(i) for i in string.replace("\n", "").split(' ')]


def readGameboard(filename: str) -> List[List[int]]:
    """
        Reads a 15-puzzle gameboard from a file.\n
        returns a list of a list of integers representing the gameboard.\n
        with the integer 16 as the empty slot
    """
    gameboard = []                              # initializes list
    file = open(filename, "r")                  # opens file
    lines = file.readlines()                    # turns files into list of strings
    for row in lines:                          # turns list of strings into  of list of ints
        gameboard.append(stringToRow(row))
    file.close()                                # close file
    return gameboard                            # return

def printGameboard(board: List[List[int]]) -> None:
    """
        Prints a given gameboard to the console. \n
        converts the number "16" into blank spaces.
    """
    for row in board:
        for el in row:
            if(el == 16):
                el = "  "
            elif (el < 10):
                el = str(str(el) + " ")
            print(el, end=" ")
        print("")

def getFlatBoard(board):
    """
        transforms the board into a flat board
    """
    flatBoard = []
    for row in board:
        for el in row:
            flatBoard.append(el)
    return flatBoard

def randomGameboard():
    """
        Generates a random gameboard with the integer 16 as the empty slot.\n
        NEVER USED IN END PRODUCT SINCE IT IS UNRELIABLE
    """
    flatBoard = [int(i) for i in range(1, 17)]
    random.shuffle(flatBoard)
    gameboard = []
    for i in range(4):
        gameboard.append(flatBoard[i * 4:i * 4 + 4])
    return gameboard