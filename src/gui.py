from multiprocessing import Event
import PySimpleGUI as psg
import os.path
from puzzlesolver import *
from gameboardIO import *

file_select_column = [
    [   
        psg.Push(),
        psg.Text(text="15 Puzzle Solver", font=("Helvetica", 25), justification="center"),
        psg.Push(),
    ],
    [
        psg.Text("Path to txt file"),
        psg.In(size=(25,1), enable_events=True, key="-FILE-"),
        psg.FileBrowse(file_types=(("Text Files", "*.txt"),)),
    ],
    [
        psg.Push(),
        psg.Button("Find Solution", key="-FIND-", disabled=True),
        psg.Button("Show Solution", key="-SHOW-", disabled=True),
        psg.Push(),
    ],
    [
        psg.Push(),
        psg.Text(key = "-KRGDRI-"),
        psg.Text(key = "-KRGDRIX-"),
        psg.Push(),
    ],
    [
        psg.Push(),
        psg.Text(key = "-TIME-"),
        psg.Push(),
    ],
    [
        psg.Push(),
        psg.Text(key = "-NODES-"),
        psg.Push(),
    ],
]

image_viewer_columnA = [
    [psg.Image(key = "-IMAGE1-", filename="./assets/number-1.png")],
    [psg.Image(key = "-IMAGE5-", filename="./assets/number-5.png")],
    [psg.Image(key = "-IMAGE9-", filename="./assets/number-9.png")],
    [psg.Image(key = "-IMAGE13-", filename="./assets/number-13.png")],
]

image_viewer_columnB = [
    [psg.Image(key = "-IMAGE2-", filename="./assets/number-2.png")],
    [psg.Image(key = "-IMAGE6-", filename="./assets/number-6.png")],
    [psg.Image(key = "-IMAGE10-", filename="./assets/number-10.png")],
    [psg.Image(key = "-IMAGE14-", filename="./assets/number-14.png")],
]

image_viewer_columnC = [
    [psg.Image(key = "-IMAGE3-", filename="./assets/number-3.png")],
    [psg.Image(key = "-IMAGE7-", filename="./assets/number-7.png")],
    [psg.Image(key = "-IMAGE11-", filename="./assets/number-11.png")],
    [psg.Image(key = "-IMAGE15-", filename="./assets/number-15.png")],
]

image_viewer_columnD = [
    [psg.Image(key = "-IMAGE4-", filename="./assets/number-4.png")],
    [psg.Image(key = "-IMAGE8-", filename="./assets/number-8.png")],
    [psg.Image(key = "-IMAGE12-", filename="./assets/number-12.png")],
    [psg.Image(key = "-IMAGE16-", filename="./assets/number-16.png")],
]

image_viewer_column =[
    [
        psg.Column(image_viewer_columnA),
        psg.Column(image_viewer_columnB),
        psg.Column(image_viewer_columnC),
        psg.Column(image_viewer_columnD),
    ]
]

layout = [
    [
        psg.Column(file_select_column),
        psg.VSeparator(),
        psg.Column(image_viewer_column),
    ],
]

window = psg.Window("15 Puzzle", layout)

def getKurangDari(gameboard):
    sumKurangDari = int(0)
    flatBoard = []
    for row in gameboard:
        for el in row:
            flatBoard.append(el)
    for i in range(len(flatBoard)):
        for j in range(i, len(flatBoard)):
            if(flatBoard[j] < flatBoard[i]):
                sumKurangDari += 1
    return sumKurangDari

while True:
    event, values = window.read()
    if event == "Exit" or event == psg.WIN_CLOSED:
        break 
    if event == "-FILE-":
        try:
            window["-TIME-"].update("")
            window["-NODES-"].update("")
            window["-FIND-"].update(disabled=False)
            window["-SHOW-"].update(disabled=True)
            gameBoard = readGameboard(values["-FILE-"])
            kurangDari = getKurangDari(gameBoard)
            window["-KRGDRI-"].update("KURANG(i) Value: " + str(kurangDari))
            window["-KRGDRIX-"].update("KURANG(i) + X Value: " + str(kurangDari + sum(list(findIndex(gameBoard, 16))) % 2))
            flatBoard = getFlatBoard(gameBoard)
            for i in range(16):
                window[f"-IMAGE{i+1}-"].update(filename="./assets/number-" + str(flatBoard[i]) + ".png")
        except:
            window["-FIND-"].update(disabled=True)
            window["-SHOW-"].update(disabled=True)
    if event == "-FIND-":
        try:
            solution = solveGameboard(gameBoard)
            steps = solution[0]
            timeTaken = solution[1]
            nodesRaised = solution[2]
            window["-SHOW-"].update(disabled=False)
            window["-TIME-"].update("{:0.4f} seconds".format(timeTaken))
            window["-NODES-"].update("Nodes raised: " + str(nodesRaised))
        except Exception as e:
            psg.popup(e)
    if event == "-SHOW-":
        window["-SHOW-"].update(disabled=True)
        flatBoard = getFlatBoard(gameBoard)
        for move in steps:
            window[f"-IMAGE{flatBoard.index(16) + 1}-"].update(filename="./assets/" + move + ".png")
            gameBoard = moveBlankSlot(gameBoard, move)
            flatBoard = getFlatBoard(gameBoard)
            window.read(timeout=250)
            for i in range(16):
                window[f"-IMAGE{i+1}-"].update(filename="./assets/number-" + str(flatBoard[i]) + ".png")
            window.read(timeout=250)
window.close()