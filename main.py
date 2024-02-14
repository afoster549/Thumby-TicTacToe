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

player = "x"

multiplayer = False
host = False
playing = False

end = False
draw = False
winner = ""

def drawBoard():
    thumby.display.fill(0)
    
    thumby.display.drawLine(31, 6, 31, 34, 1)
    thumby.display.drawLine(41, 6, 41, 34, 1)
    thumby.display.drawLine(22, 15, 50, 15, 1)
    thumby.display.drawLine(22, 25, 50, 25, 1)
    
    thumby.display.drawFilledRectangle(22, 6, 9, 9, 1)
    
    thumby.display.drawText(player, 0, 0, 1)
    
    thumby.display.update()

def waitForPlayer():
    global player
    global playing
    
    while True:
        recived = thumby.link.receive()
        
        if recived != None:
            if recived[1] == 0:
                player = "o"
                
                host = False
                
                thumby.link.send(bytearray([1, 1]))
            else:
                playing = True
                
            break
        else:
            thumby.link.send(bytearray([1, 0]))
            
            host = True

def modeSelect():
    global multiplayer
    global playing
    
    thumby.display.fill(0)
    
    thumby.display.drawText("Mode Select", 2, 5, 1)
    thumby.display.drawText("A: 1 player", 2, 21, 1)
    thumby.display.drawText("B: 2 player", 2, 30, 1)
    
    thumby.display.update()
    
    while True:
        if thumby.buttonA.justPressed():
            print("1 player")
            
            multiplayer = False
            playing = True
            
            break
        elif thumby.buttonB.justPressed():
            multiplayer = True
            
            thumby.display.fill(0)
            thumby.display.drawText("Waiting...", 8, 18, 1)
            
            thumby.display.update()
            
            waitForPlayer()
            
            break
        
    drawBoard()

def hideCursor():
    global playing
    global draw
    global end
    global winner
    
    if playing and not draw:
        winner = player
    
    playing = False
    end = True
    
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
    global player
    global draw
    
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
    
    draw = True
        
    for row in board:
        for cell in row:
            if cell == "":
                draw = False
    
    if draw == True:
        hideCursor()

def place(player, x, y):
    board[y][x] = player
    
    if player == "x":
        bmp = None
        
        if activeCell["x"] == x and activeCell["y"] == y:
            bmp = bitmapXSelected
        else:
            bmp = bitmapX
        
        cellSprite = thumby.Sprite(9, 9, bmp, 22 + (x * 10), 6 + (y * 10))
        
        thumby.display.drawSprite(cellSprite)
    else:
        bmp = None
        
        if activeCell["x"] == x and activeCell["y"] == y:
            bmp = bitmapOSelected
        else:
            bmp = bitmapO
        
        cellSprite = thumby.Sprite(9, 9, bmp, 22 + (x * 10), 6 + (y * 10))
        
        thumby.display.drawSprite(cellSprite)
    
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
    global player
    global playing
    global multiplayer
    
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
    elif thumby.buttonA.justPressed() and playing:
        if board[activeCell["y"]][activeCell["x"]] == "":
            place(player, activeCell["x"], activeCell["y"])
            
            if multiplayer:
                playing = False
                
                thumby.link.send(bytearray(
                    [
                        0,
                        activeCell["x"],
                        activeCell["y"]
                    ]
                ))
            else:
                thumby.display.drawText(player, 0, 0, 0)
                
                if player == "x":
                    player = "o"
                else:
                    player = "x"
                
                thumby.display.drawText(player, 0, 0, 1)
    
                thumby.display.update()
            
def checkResponse():
    global playing
    
    recived = thumby.link.receive()
    
    if recived != None and recived[0] == 0:
        if player == "x":
            playing = True
            
            place("o", recived[1], recived[2])
        else:
            playing = True
            
            place("x", recived[1], recived[2])

def endGame():
    global board
    global activeCell
    
    global player
    
    global multiplayer
    global host
    global playing
    
    global end
    global draw
    global winner
    
    time.sleep(2)

    thumby.display.fill(0)
        
    if draw:
        thumby.display.drawText("Draw!", 23, 10, 1)
    else:
        thumby.display.drawText(f"{winner} Won!", 20, 10, 1)
            
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
            
            playing = True
            
            player = "x"
    
            multiplayer = False
            host = False
            playing = False
            
            end = False
            draw = False
            winner = ""
            
            modeSelect()
            
            break
        elif thumby.buttonB.justPressed():
            thumby.reset()

modeSelect()

while True:
    checkInput()
        
    checkResponse()
    
    if end:
        endGame()
