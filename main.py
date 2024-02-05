import gc
import thumby
import time

gc.enable()

bitmapXSelected = bytearray([255, 125, 187, 215, 239, 215, 187, 125, 255, 1, 1, 1, 1, 1, 1, 1, 1, 1])
bitmapOSelected = bytearray([255, 199, 187, 125, 125, 125, 187, 199, 255, 1, 1, 1, 1, 1, 1, 1, 1, 1])

bitmapX = bytearray([0, 130, 68, 40, 16, 40, 68, 130, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
bitmapO = bytearray([0, 56, 68, 130, 130, 130, 68, 56, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

board = [
    ["", "", ""],
    ["", "", ""],
    ["", "", ""]
]

activeCell = {
    "x": 0,
    "y": 0,
    "xOld": 0,
    "yOld": 0
}

currentPlayer = "x"

playing = True

def drawBoard():
    thumby.display.fill(0)
    
    thumby.display.drawLine(31, 6, 31, 34, 1)
    thumby.display.drawLine(41, 6, 41, 34, 1)
    thumby.display.drawLine(22, 15, 50, 15, 1)
    thumby.display.drawLine(22, 25, 50, 25, 1)
    
    thumby.display.drawFilledRectangle(22, 6, 9, 9, 1)
    
    thumby.display.update()

def hideCursor():
    global playing
    playing = False
    
    cell = board[activeCell["y"]][activeCell["x"]]
    
    if cell == "":
        thumby.display.drawFilledRectangle(22 + (activeCell["x"] * 10), 6 + (activeCell["y"] * 10), 9, 9, 0)
    elif cell == "x":
        cellSprite = thumby.Sprite(9, 9, bitmapX, 22 + (activeCell["x"] * 10), 6 + (activeCell["y"] * 10))
        
        thumby.display.drawSprite(cellSprite)
    elif cell == "o":
        cellSprite = thumby.Sprite(9, 9, bitmapO, 22 + (activeCell["x"] * 10), 6 + (activeCell["y"] * 10))
        
        thumby.display.drawSprite(cellSprite)

def checkWin():
    global currentPlayer
    draw = True
    
    for i in range(0, 3):
        if board[i][0] == board[i][1] and board[i][1] == board[i][2] and board[i][0] != "":
            hideCursor()
            
            thumby.display.drawLine(22, 10 + (i * 10), 50, 10 + (i * 10), 1)
            
            return
    for i in range(0, 3):
        if board[0][i] == board[1][i] and board[1][i] == board[2][i] and board[0][i] != "":
            hideCursor()
            
            thumby.display.drawLine(26 + (i * 10), 6, 26 + (i * 10), 34, 1)
            
            return
    if board[0][0] == board[1][1] and board[1][1] == board[2][2] and board[0][0] != "":
        hideCursor()
        
        thumby.display.drawLine(22, 6, 50, 34, 1)
        
        return
    if board[0][2] == board[1][1] and board[1][1] == board[2][0] and board[0][2] != "":
        hideCursor()
        
        thumby.display.drawLine(22, 34, 50, 6, 1)
        
        return
        
    for row in board:
        for cell in row:
            if cell == "":
                draw = False
                
    if draw == True:
        currentPlayer = ""
        
        hideCursor()

def place():
    global currentPlayer
    
    board[activeCell["y"]][activeCell["x"]] = currentPlayer
    
    if currentPlayer == "x":
        cellSprite = thumby.Sprite(9, 9, bitmapXSelected, 22 + (activeCell["x"] * 10), 6 + (activeCell["y"] * 10))
        
        thumby.display.drawSprite(cellSprite)
        
        currentPlayer = "o"
    else:
        cellSprite = thumby.Sprite(9, 9, bitmapOSelected, 22 + (activeCell["x"] * 10), 6 + (activeCell["y"] * 10))
        
        thumby.display.drawSprite(cellSprite)
        
        currentPlayer = "x"
    
    checkWin()
    
    thumby.display.update()

def update():
    cell = board[activeCell["y"]][activeCell["x"]]
    oldCell = board[activeCell["yOld"]][activeCell["xOld"]]
    
    if cell == "":
        thumby.display.drawFilledRectangle(22 + (activeCell["x"] * 10), 6 + (activeCell["y"] * 10), 9, 9, 1)
    elif cell == "x":
        cellSprite = thumby.Sprite(9, 9, bitmapXSelected, 22 + (activeCell["x"] * 10), 6 + (activeCell["y"] * 10))
        
        thumby.display.drawSprite(cellSprite)
    elif cell == "o":
        cellSprite = thumby.Sprite(9, 9, bitmapOSelected, 22 + (activeCell["x"] * 10), 6 + (activeCell["y"] * 10))
        
        thumby.display.drawSprite(cellSprite)
        
    if oldCell == "":
        thumby.display.drawFilledRectangle(22 + (activeCell["xOld"] * 10), 6 + (activeCell["yOld"] * 10), 9, 9, 0)
    elif oldCell == "x":
        cellSprite = thumby.Sprite(9, 9, bitmapX, 22 + (activeCell["xOld"] * 10), 6 + (activeCell["yOld"] * 10))
        
        thumby.display.drawSprite(cellSprite)
    elif oldCell == "o":
        cellSprite = thumby.Sprite(9, 9, bitmapO, 22 + (activeCell["xOld"] * 10), 6 + (activeCell["yOld"] * 10))
        
        thumby.display.drawSprite(cellSprite)
        
    thumby.display.update()

def checkInput():
    if thumby.buttonU.justPressed():
        if activeCell["y"] - 1 >= 0:
            activeCell["xOld"] = activeCell["x"]
            activeCell["yOld"] = activeCell["y"]
            
            activeCell["y"] -= 1
            
            update()
    elif thumby.buttonD.justPressed():
        if activeCell["y"] + 1 <= 2:
            activeCell["xOld"] = activeCell["x"]
            activeCell["yOld"] = activeCell["y"]
            
            activeCell["y"] += 1
            
            update()
    elif thumby.buttonL.justPressed():
        if activeCell["x"] - 1 >= 0:
            activeCell["xOld"] = activeCell["x"]
            activeCell["yOld"] = activeCell["y"]
            
            activeCell["x"] -= 1
            
            update()
    elif thumby.buttonR.justPressed():
        if activeCell["x"] + 1 <= 2:
            activeCell["xOld"] = activeCell["x"]
            activeCell["yOld"] = activeCell["y"]
            
            activeCell["x"] += 1
            
            update()
    elif thumby.buttonA.justPressed():
        if board[activeCell["y"]][activeCell["x"]] == "":
            place()

def endGame():
    global board
    global activeCell
    global currentPlayer
    global playing
    
    time.sleep(2)

    thumby.display.fill(0)
        
    if currentPlayer == "x":
        thumby.display.drawText("O Won!", 20, 10, 1)
    elif currentPlayer == "o":
        thumby.display.drawText("X Won!", 20, 10, 1)
    else:
        thumby.display.drawText("Draw!", 23, 10, 1)
            
    thumby.display.drawText("A. New Game", 4, 20, 1)
    thumby.display.drawText("B. Exit", 4, 30, 1)
        
    thumby.display.update()
        
    while True:
        if thumby.buttonA.justPressed():
            drawBoard()
                
            board = [
                ["", "", ""],
                ["", "", ""],
                ["", "", ""]
            ]
            
            activeCell = {
                "x": 0,
                "y": 0,
                "xOld": 0,
                "yOld": 0
            }
                
            currentPlayer = "x"
                
            playing = True
            
            break
        elif thumby.buttonB.justPressed():
            thumby.reset()

drawBoard()

while True:
    if playing:
        checkInput()
    else:
        endGame()
