import math
import random
from tkinter import *
import copy

####################################
# customize these functions
####################################
def generalInit(data):
    data.hexesPerSide = 5
    data.hexesAcross = 2*data.hexesPerSide-1
    data.hexSize = data.boardWidth//data.hexesAcross
    data.spotRadius = 23 *data.boardWidth/550
    data.pieceRadius = 26 *data.boardWidth/550
    data.selectionRadius = 30 *data.boardWidth/550
    data.textHeight = 30
    data.turnCount = 1
    data.howToStep = 1
    initMenuButtons(data)
    #minimax image taken from:
    #http://mnemstudio.org/ai/game/images/minimax_move_tree1.gif
    data.turn = "white"
    data.gameOver = False
    data.selectedPieces = {}
    data.lastHex = None
    data.buttonsEnabled = False

    createBoardLists(data)
    setUpBoard(data)
    assign3AxisCoords(data)

    #Make coord 3-axis to 2-axis conversion lookup
    data.convertCoords = dict()
    createConvertCoords(data)
def initMenu(data):
    data.boardWidth = 360 
    data.gameMode = "menu"
    data.buttonOffset = 20 
    data.buttonWidth = 240
    data.buttonHeight = 100
    generalInit(data)

def initGame(data):
    data.boardWidth = 550 #550
    data.buttonOffset = 20 
    data.buttonWidth = 140
    data.buttonHeight = 210

    generalInit(data)
def initLearnAI(data):
    try:
        data.minimaxTree = PhotoImage(file="minimax_move_tree1.gif")
    except:
        data.minimaxTree = None
    generalInit(data)
def setUpBoard(data):
    #white - fill first two lines
    linesToFill = 2
    for i in range(linesToFill):
        for j in range(getRowLength(i,data)):
            data.board[i][j] = "white"
    #white - place front 3 pieces
    data.board[linesToFill][getRowLength(linesToFill,data)//2-1] = "white"
    data.board[linesToFill][getRowLength(linesToFill,data)//2] = "white"
    data.board[linesToFill][getRowLength(linesToFill,data)//2+1] = "white"
    #black - fill first two lines
    linesToFill = 2
    for i in range(linesToFill):
        for j in range(getRowLength(i,data)):
            data.board[data.hexesAcross-1-i][j] = "black"
    #black - place front 3 pieces
    blackFrontRow = data.hexesAcross-1-linesToFill
    data.board[blackFrontRow][getRowLength(blackFrontRow,data)//2-1] = "black"
    data.board[blackFrontRow][getRowLength(blackFrontRow ,data)//2] = "black"
    data.board[blackFrontRow][getRowLength(blackFrontRow ,data)//2+1] = "black"
def getRowLength(i, data): #This helper function gets the length of the ith row
    if(data.hexesPerSide+i >= data.hexesAcross):
        rowLength = data.hexesPerSide+(data.hexesAcross-i)-1
    else:
        rowLength = data.hexesPerSide+i
    return rowLength
def createBoardLists(data):
    data.board = []
    data.boardScreenPos = []
    data.board3AxisCoords = [] #assign each cell a 3-axis hex coordinate
    for i in range(data.hexesAcross):
        rowLength = 0
        row = [None]*getRowLength(i,data)
        data.board.append(row)
        data.boardScreenPos.append(copy.copy(row))
        data.board3AxisCoords.append(copy.copy(row))
def createConvertCoords(data): 
    #makes a lookup table for fast conversions from 3-axis to 2-axis coordinates
    for row in range(len(data.board3AxisCoords)):
        for col in range(len(data.board3AxisCoords[row])):
            curr3Axis = data.board3AxisCoords[row][col]
            data.convertCoords[curr3Axis] = (row,col)
def getColorAtCoords(board,coords,data):
    if(coords in data.convertCoords.keys()):
        (row,col) = data.convertCoords[coords]
        return board[row][col]
    return False
def setColorAtCoords(color,board,coords,data):
    if(coords in data.convertCoords.keys()):
        (row,col) = data.convertCoords[coords]
        board[row][col] = color
def assign3AxisCoords(data):
    #Step 1, fill up 3-axis coords with initial values
    for row in range(len(data.board)):
        for col in range(len(data.board[row])):
            data.board3AxisCoords[row][col] = (col,row,0)
    #Step 2, shift rows so they line up
    startShift = data.hexesAcross//2+1
    shiftCounter = 0
    for row in range(startShift,data.hexesAcross):
        shiftCounter += 1
        for col in range(len(data.board[row])):
            (currX, currY,currZ) = data.board3AxisCoords[row][col]
            currX += shiftCounter
            data.board3AxisCoords[row][col] = (currX, currY,currZ)
    #Step 3, assign the Z-axis values
    for row in range(len(data.board3AxisCoords)):
        for col in range(len(data.board3AxisCoords[row])):
            (currX,currY,currZ) = data.board3AxisCoords[row][col]
            currY = -currY
            currZ = -1*(currX + currY)
            data.board3AxisCoords[row][col] = (currX, currY,currZ)
def mousePressed(event, data):
    print("clicked at: ", event.x, ",",event.y)
    if(data.gameMode == "menu"):
        registerButtonPresses(event,data)
    elif(data.gameMode == "human_game" and data.gameOver == False):
        getMouseInput(event,data)
    elif(data.gameMode == "AI_game" and data.turn == "black"
        and data.gameOver == False):
        getMouseInput(event,data)
    elif(data.gameMode == "how_to_play"):
        getMouseInput(event,data)
def registerButtonPresses(event,data):
    tan30 = math.tan(math.pi/6)
    if(event.x>data.leftX and 
        event.x<data.innerLeftX+data.buttonHeight*tan30 and
        event.y>data.topY and event.y<data.innerTopY):
        humanGameButtonPressed(event,data)
    elif(event.x>data.leftX and 
        event.x<data.innerLeftX+data.buttonHeight*tan30 and
        event.y>data.innerBottomY and event.y<data.bottomY):
            AIGameButtonPressed(event,data)
    elif(event.x>data.innerRightX-data.buttonHeight*tan30 and 
        event.x<data.rightX and event.y>data.topY and event.y<data.innerTopY):
        howToPlayButtonPressed(event,data)
    elif(event.x>data.innerRightX-data.buttonHeight*tan30 and 
        event.x<data.rightX and event.y>data.innerBottomY and 
        event.y<data.bottomY):
        learnAIButtonPressed(event,data)

def getMouseInput(event,data):
    #Selector for making human moves
        for row in range(len(data.boardScreenPos)):
            for col in range(len(data.boardScreenPos[row])):
                if(data.boardScreenPos[row][col] == None):
                    return
                (x,y) = data.boardScreenPos[row][col]
                dist = math.sqrt((event.x-x)**2+(event.y-y)**2)
                if(dist < 25):
                    print("clicked on" , row, col)
                    humanControl(row,col,data)
def keyPressed(event, data):
    if(event.keysym == 'r'):
        data.gameMode == "menu"
        initMenu(data)

def makeAIMove(data):
    data.board = minimax(data,2)
    print("move made!")
    if(data.turn == "black"):
        data.turn = "white"
    else:
        data.turn = "black"
    if(checkLoss(data,data.turn) == True):
        data.gameOver = True
    data.turnCount += 1
        
def humanGameButtonPressed(event,data):
    initGame(data)
    data.gameMode = "human_game"
def AIGameButtonPressed(event,data):
    initGame(data)
    data.gameMode = "AI_game"
def howToPlayButtonPressed(event,data):
    initMenu(data)
    data.gameMode = "how_to_play"
def learnAIButtonPressed(event,data):
    initLearnAI(data)
    data.gameMode = "learn_AI"
def timerFired(data):
    if(data.gameMode == "AI_game" and data.turn == "white"
    and data.gameOver == False):
        makeAIMove(data)
    if(data.gameMode == "how_to_play" and data.howToStep == 1):
        if(data.selectedPieces != {}):
            data.howToStep += 1
    elif(data.gameMode == "how_to_play" and data.howToStep == 2):
        if(len(data.selectedPieces) > 1):
            data.howToStep += 1

def redrawAll(canvas, data):
    if(data.gameMode == "menu"):
        drawPanels(canvas, data, enableButtons = True)
        drawTitleText(canvas, data)
        drawDescription(canvas,data)
        drawBoard(canvas, data, data.width//2, data.height//2)
        drawButtonText(canvas,data)
        drawPieces(canvas, data)
    elif(data.gameMode == "AI_game" ):
        drawBoard(canvas, data)
        drawPieces(canvas, data)
        drawPanels(canvas, data)
        drawAIGameText(canvas,data)
        drawTurnCount(canvas, data)
        if(data.gameOver == True):
            drawGameOverText(canvas, data)
    elif(data.gameMode == "human_game"):
        drawBoard(canvas, data)
        drawPieces(canvas, data)
        drawPanels(canvas, data)
        drawHumanGameText(canvas,data)
        drawTurnCount(canvas, data)
        if(data.gameOver == True):
            drawGameOverText(canvas, data)
    elif(data.gameMode == "how_to_play"):
        drawTitleText(canvas, data)
        drawBoard(canvas, data, data.width//2, data.height//2)
        drawHowToText(canvas,data)
        drawPieces(canvas, data)
    elif(data.gameMode == "learn_AI"):
        drawTitleText(canvas, data)
        drawLearnAI(canvas,data)

def drawTitleText(canvas,data):
    canvas.create_text(data.width//2,data.textHeight,text = "AlphaAbalone",
    font = "System 36")
def drawDescription(canvas,data):
    heightFactor = 2.5
    canvas.create_text(data.width//2,data.textHeight*heightFactor,
    text = "Abalone Board game with AI", font = "System 12")
    canvas.create_text(data.width//2,data.textHeight*(heightFactor+1),
    text="Using Minimax Algorithm with Alpha-Beta Prunning",font ="System 12")
    canvas.create_text(data.width//2,
    data.height-data.textHeight*(heightFactor+1),
    text = "A 15-112 Term Project By Ben Soudry", font = "System 12")
def drawLearnAI(canvas,data):
    heightFactor = 18
    AITextHeight = 60
    try:
        textFile = open('learnAI.txt', 'r')
    except:
        canvas.create_text(data.width//2,AITextHeight+heightFactor,
        text = "Error, could not read learnAI.txt, unzip the project folder",
         font = "System 10")
        return
    AIText = textFile.read()
    AITextLines = AIText.splitlines()
    for i in range(len(AITextLines)):
        canvas.create_text(data.width//2,AITextHeight+(i+1)*heightFactor,
        text = AITextLines[i], font = "System 10")
        pass
    canvas.create_text(data.width//2,data.height-AITextHeight//2,
        text = "Press r to return to the menu", font = "System 12")
    imageHeight =2*data.height//3
    if(data.minimaxTree != None):
        canvas.create_image(data.width//2,imageHeight, image = data.minimaxTree)
    else:
        canvas.create_text(data.width//2,imageHeight,
        text="Error: could not open minimax_move_tree1.gif, unzip the project folder",
        font="System 12")
def drawGameOverText(canvas, data):
    heightFactor = 1.5
    canvas.create_text(data.width//2,data.textHeight*heightFactor,
        text = "Game Over! Press r to return to menu", font = "System 12")
def drawHowToText(canvas, data):
    heightFactor = 18
    howToTextHeight = 60
    try:
        textFile = open('howToText.txt', 'r')
    except:
        canvas.create_text(data.width//2,howToTextHeight+heightFactor,
        text = "Error, could not read howToText.txt, unzip the project folder",
        font = "System 10")
        return
    howToText = textFile.read()
    howToTextLines = howToText.splitlines()
    canvas.create_text(data.width//2,data.height-howToTextHeight,
        text = "Press r to return to the menu", font = "System 12")
    if(data.howToStep == 1):
        canvas.create_text(data.width//2,howToTextHeight+heightFactor,
        text = howToTextLines[0], font = "System 12")
    elif(data.howToStep == 2):
        canvas.create_text(data.width//2,howToTextHeight+heightFactor,
        text = howToTextLines[1], font = "System 12")
        canvas.create_text(data.width//2,howToTextHeight+heightFactor*2,
        text = howToTextLines[2], font = "System 12")
        canvas.create_text(data.width//2,howToTextHeight+heightFactor*3,
        text = howToTextLines[3], font = "System 12")
    elif(data.howToStep == 3):
        canvas.create_text(data.width//2,howToTextHeight+heightFactor,
        text = howToTextLines[4], font = "System 12")
    elif(data.howToStep == 4):
        canvas.create_text(data.width//2,howToTextHeight+heightFactor,
        text = howToTextLines[5], font = "System 12")
        canvas.create_text(data.width//2,howToTextHeight+heightFactor*2,
        text = howToTextLines[6], font = "System 12")
        canvas.create_text(data.width//2,howToTextHeight+heightFactor*3,
        text = howToTextLines[7], font = "System 12")
def drawButtonText(canvas,data):
    textShift = 5
    canvas.create_text(data.leftX+textShift,data.topY, anchor = "nw",
        text = "Play Against a Human", font = "Ariel 20")
    canvas.create_text(data.leftX+textShift,data.innerBottomY, anchor = "nw",
        text = "Play Against an AI", font = "Ariel 20")
    canvas.create_text(data.innerRightX,data.topY, anchor = "nw",
        text = "How to Play", font = "Ariel 20")
    canvas.create_text(data.innerRightX,data.innerBottomY, anchor = "nw",
        text = "Learn about the AI", font = "Ariel 20")
    pass
def drawAIGameText(canvas,data):
    textShift = 5
    statusTextHeight = 45
    canvas.create_text(data.leftX+textShift,data.topY, anchor = "nw",
        text = "AlphaAbalone", font = "System 28")
    canvas.create_text(data.leftX+textShift,data.innerBottomY, anchor = "nw",
        text = "Human", font = "Ariel 28")
    if(data.turn == "black"):
        canvas.create_text(data.leftX+textShift,
        data.innerBottomY+statusTextHeight, anchor = "nw",
        text = "Your Move", font = "Ariel 20")
    elif(data.turn == "white"):
        canvas.create_text(data.leftX+textShift,
        data.topY+statusTextHeight, anchor = "nw",
        text = "Thinking...", font = "System 20")
    drawPieceCount(canvas,data)

def drawHumanGameText(canvas,data):
    textShift = 5
    statusTextHeight = 45
    canvas.create_text(data.leftX+textShift,data.topY, anchor = "nw",
        text = "Player1", font = "Ariel 28")
    canvas.create_text(data.leftX+textShift,data.innerBottomY, anchor = "nw",
        text = "Player2", font = "Ariel 28")
    if(data.turn == "white"):
        canvas.create_text(data.leftX+textShift,
        data.topY+statusTextHeight, anchor = "nw",
        text = "Your Move", font = "Ariel 20")
    elif(data.turn == "black"):
        canvas.create_text(data.leftX+textShift,
        data.innerBottomY+statusTextHeight, anchor = "nw",
        text = "Your Move", font = "Ariel 20")
    drawPieceCount(canvas,data)
    pass
def drawPieceCount(canvas,data):
    textShift = 5
    statusTextHeight = 45
    blackPieceCount = pieceCount(data, "black")
    whitePieceCount = pieceCount(data, "white")
    canvas.create_text(data.leftX+textShift,data.topY+2*statusTextHeight,
    anchor = "nw",text="Piece count: "+str(whitePieceCount),font = "Ariel 18")
    canvas.create_text(data.leftX+textShift,
    data.innerBottomY+2*statusTextHeight,
    anchor = "nw",text="Piece count: "+str(blackPieceCount),font = "Ariel 18")
def drawTurnCount(canvas,data):
    textShift = 5
    statusTextHeight = 45
    canvas.create_text(data.innerRightX+textShift,data.topY+statusTextHeight,
    anchor = "ne",text="Turn "+str(data.turnCount),font = "Ariel 18")

def initMenuButtons(data):
    #Variables for positioning the buttons
    data.leftX=data.width//2-data.boardWidth//2-data.buttonOffset
    data.leftX -= data.buttonWidth
    data.rightX=data.width//2+data.boardWidth//2+data.buttonOffset
    data.rightX += data.buttonWidth
    data.innerLeftX = data.width//2-data.boardWidth//2-data.buttonOffset
    data.innerRightX =  data.width//2+data.boardWidth//2+data.buttonOffset 
    data.topY = data.height//2-data.buttonOffset-data.buttonHeight
    data.innerTopY = data.height//2-data.buttonOffset
    data.bottomY = data.height//2+data.buttonOffset+data.buttonHeight
    data.innerBottomY = data.height//2+data.buttonOffset
def drawPanels(canvas,data, enableButtons = False):
    tan30 = math.tan(math.pi/6)
    button1 = canvas.create_polygon((data.innerLeftX, data.innerTopY),
        (data.leftX,data.innerTopY),(data.leftX,data.topY),
        (data.innerLeftX+data.buttonHeight*tan30,data.topY),
        fill = "gray")
    button2 = canvas.create_polygon((data.innerLeftX, data.innerBottomY), 
        (data.leftX,data.innerBottomY),(data.leftX,data.bottomY),
        (data.innerLeftX+data.buttonHeight*tan30,data.bottomY),
        fill = "gray")
    button3 = canvas.create_polygon((data.innerRightX, data.innerTopY), 
        (data.rightX,data.innerTopY),(data.rightX,data.topY),
        (data.innerRightX-data.buttonHeight*tan30,data.topY),
        fill = "gray")
    button4 = canvas.create_polygon((data.innerRightX, data.innerBottomY), 
        (data.rightX,data.innerBottomY),(data.rightX,data.bottomY),
        (data.innerRightX-data.buttonHeight*tan30,data.bottomY),
        fill = "gray")
    pass

def drawBoard(canvas, data, cx=None,cy =None):
    if(cx == None):
        cx = data.width//2
    if(cy == None):
        cy = data.height//2
    r = data.boardWidth//2
    cos60 = math.cos(math.pi/3)
    sin60 = math.sin(math.pi/3)  
    #Draw hexagonal board 
    canvas.create_polygon(cx-r,cy,cx-r*cos60,cy-r*sin60,cx+r*cos60,cy-r*sin60,
        cx+r,cy,cx+r*cos60,cy+r*sin60,cx-r*cos60,cy+r*sin60,fill = "sienna")
    for i in range(data.hexesAcross):
        spotY = (cy-r*sin60) + i*data.hexSize*sin60 + data.hexSize*sin60/2
        rowLength = getRowLength(i,data)
        startX = cx-rowLength*data.hexSize//2 + data.hexSize//2
        for j in range(rowLength):
            spotX = startX + j*data.hexSize
            canvas.create_oval(spotX-data.spotRadius,spotY-data.spotRadius,
                spotX+data.spotRadius,spotY+data.spotRadius, fill = "tan")
            #Add this location to boardScreenPos
            if(data.boardScreenPos[i][j] == None):
                data.boardScreenPos[i][j] = (spotX,spotY)
def drawPieces(canvas,data):
    for row in range(data.hexesAcross):
        rowLength = getRowLength(row,data)
        for col in range(rowLength):
            (pieceX,pieceY) = data.boardScreenPos[row][col]
            #Highlight selected pieces:
            currHex = data.board3AxisCoords[row][col]
            for selected in data.selectedPieces:
                if(selected == currHex):
                    canvas.create_oval(pieceX-data.selectionRadius,
                    pieceY-data.selectionRadius, pieceX+data.selectionRadius,
                    pieceY+data.selectionRadius, fill = "chartreuse")
            #Draw pieces
            if(data.board[row][col] == "white"):
                canvas.create_oval(pieceX-data.pieceRadius,
                pieceY-data.pieceRadius,pieceX+data.pieceRadius,
                pieceY+data.pieceRadius, fill = "white")
            elif(data.board[row][col] == "black"):
                canvas.create_oval(pieceX-data.pieceRadius,
                pieceY-data.pieceRadius,pieceX+data.pieceRadius,
                pieceY+data.pieceRadius, fill = "black")
            #canvas.create_text(pieceX,pieceY,
            #text = str(data.board3AxisCoords[i][j]),fill= "green")
####
#Human Controls
####
def hexDiff(hex1,hex2): #returns the direction and distance between hexes
    (x1,y1,z1) = hex1
    (x2,y2,z2) = hex2
    dist = max(abs(x2-x1),abs(y2-y1),abs(z2-z1))
    direction = ((x2-x1)//dist,(y2-y1)//dist,(z2-z1)//dist)
    return (direction,dist)
def humanControl(rowClicked,colClicked,data):
    #This function allows human mouse input to select pieces
    if(len(data.selectedPieces) == 0):
        if(data.board[rowClicked][colClicked] == data.turn):
            data.selectedPieces={data.board3AxisCoords[rowClicked][colClicked]}
    elif(len(data.selectedPieces) == 1):
        #This function handles the second click
        humanControlSecondClick(rowClicked,colClicked,data)
    else:
        #If we have a chain selected (third click)
        humanControlThirdClick(rowClicked,colClicked,data)
    print("SelectedPieces: ",data.selectedPieces)
def humanControlSecondClick(rowClicked,colClicked,data):
    currHex = list(data.selectedPieces)[0]
    newHex = data.board3AxisCoords[rowClicked][colClicked]
    data.lastHex = newHex
    
    #Case 1, click to a blank square
    if(data.board[rowClicked][colClicked] == None):
        (direction,dist) = hexDiff(currHex,newHex)
        if(dist == 1): #click was adjacent
            makeHumanMove(data,direction)
    #Case 2, click on another piece (form chain)
    elif(data.board[rowClicked][colClicked] == data.turn):
        if(newHex == currHex): #double clicks deselect
            data.selectedPieces = {} 
        else: #Find the correct chain
            chains = []
            (row,col) = data.convertCoords[currHex]
            possibleChainsForPiece(data.board,
                data.turn,data,row,col,chains)
            shortestChain = getShortestChain(chains,newHex)
            if(shortestChain != None):
                data.selectedPieces = shortestChain
def humanControlThirdClick(rowClicked,colClicked,data):
    newHex = data.board3AxisCoords[rowClicked][colClicked]
    if(newHex == data.lastHex):
        data.selectedPieces = {}
    else:
        (direction,dist) = hexDiff(data.lastHex,newHex)
        makeHumanMove(data,direction)
def makeHumanMove(data,direction):
    newBoard = possibleMoveForChainInDirection(data.board,data.turn,data,
    data.selectedPieces,direction) 
    if(newBoard != None):
        data.board = newBoard
        data.turn = getOpposingColor(data.turn)
        if(checkLoss(data,data.turn) == True):
            data.gameOver = True
        #Advance the tutorial
        if(data.gameMode == "how_to_play" and data.howToStep == 3):
            data.howToStep += 1
    data.selectedPieces = {}
    data.turnCount += 1

def getShortestChain(possibleChains,newHex):
    #Gets the shortest chain that contains both the selected hex
    bestLength = None
    bestChain = None
    for possibleChain in possibleChains:
        #See if it contains the selected hex
        pieceFound = False
        for piece in possibleChain:
            if(piece == newHex):
                pieceFound = True
        chainLength = len(possibleChain)
        if(pieceFound==True and (bestLength==None or chainLength<bestLength)):
            bestLength = chainLength
            bestChain = possibleChain
    return bestChain


def checkLoss(data,color):
    return (pieceCount(data,color) <= 8)
def pieceCount(data,color):
    pieceCount = 0
    for row in range(len(data.board)):
        for col in range(len(data.board[row])):
            if(data.board[row][col] == color):
                pieceCount +=1
    return pieceCount
####
#AI
####

##Citation: Minimax algorithm written myself with reference from these articles:
#https://en.wikipedia.org/wiki/Minimax
#https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning
def minimax(data,depth):
    #This function returns the board chosen
    #as a result of the minimax algorithm with alpha-beta prunning
    currColor = data.turn
    possibleBoards = possibleMoves(data.board,currColor,data)
    nextColor = getOpposingColor(currColor)
    bestBoards = []
    bestScore = None
    alpha = None
    beta = None
    alpha_beta = [None,None]
    print(depth*"   " +currColor +" moves to check: ", len(possibleBoards))  
    for possibleBoard in possibleBoards:
         boardScore = alphaBetaRecursive(data,possibleBoard,nextColor,depth-1,
            alpha,beta)
         if(data.turn == "black"):
            if(bestScore == None or boardScore > bestScore):
                bestScore = boardScore
                bestBoards = [possibleBoard]
            elif(boardScore == bestScore):
                bestBoards.append(possibleBoard)

         elif(data.turn == "white"):
            if(bestScore == None or boardScore < bestScore):
                bestScore = boardScore
                bestBoards = [possibleBoard]
            elif(boardScore == bestScore):
                bestBoards.append(possibleBoard)
    select = random.randint(0,len(bestBoards)-1)
    return bestBoards[select]
def alphaBetaRecursive(data,board,currColor,depth,alpha,beta):
    if(depth == 0):
        #print("board evaluated depth = 0")
        return boardEvaluator(board,data)
    possibleBoards = possibleMoves(board,currColor,data)
    #print(depth*"   " +currColor +" moves to check: ",
    #len(possibleBoards), " depth: ",depth)   
    if(currColor == "black"): #maximizer
        for possibleBoard in possibleBoards:
            nextColor = getOpposingColor(currColor)
            boardScore = alphaBetaRecursive(data,possibleBoard,nextColor,
                    depth-1,alpha,beta)
            if(alpha == None):
                alpha = boardScore
            else:
                alpha = max(alpha,boardScore)
            if(alpha != None and beta != None and beta <= alpha):
                print("prunned!")
                break
        return alpha
    else: #minimizer
        for possibleBoard in possibleBoards:
            nextColor = getOpposingColor(currColor)
            boardScore = alphaBetaRecursive(data,possibleBoard,nextColor,
                    depth-1,alpha,beta)
            if(beta == None):
                beta = boardScore
            else:
                beta = min(beta,boardScore)
            if(alpha != None and beta != None and beta <= alpha):
                print("prunned!")
                break
        return beta

def minimaxRecursive(data, board, currColor, depth):
    #print("minimaxRecusive depth = ", depth)
    possibleBoards = possibleMoves(board,currColor,data)
    #print(depth*"   " +currColor +" moves to check: ", len(possibleBoards))   
    if(depth <= 1): #Base Case
        return minimaxBaseCase(data, board, currColor, 
        depth, possibleBoards)
    else: #recursive case
        bestScore = None
        bestBoard = None
        nextColor = getOpposingColor(currColor)
        for possibleBoard in possibleBoards:
            boardScore = minimaxRecursive(data,possibleBoard,
            nextColor,depth-1,alpha_beta)
            if(currColor == "black"):
                if(bestScore == None or boardScore > bestScore):
                    bestScore = boardScore
                    bestBoard = possibleBoard
            elif(currColor == "white"):
                if(bestScore == None or boardScore < bestScore):
                    bestScore = boardScore
                    bestBoard = possibleBoard
        return bestScore
def minimaxBaseCase(data, board, currColor, depth, possibleBoards):
    #Once the algorithm reaches depth 1,
    #use the boardEvaluator to score the possibleBoards.
    bestBoard = None
    bestScore = None
    for possibleBoard in possibleBoards:
        boardScore = boardEvaluator(possibleBoard,data)
        if(currColor == "black"):
            if(bestScore == None or boardScore > bestScore):
                bestScore = boardScore
                bestBoard = possibleBoard
            if(alpha_beta[0] == None or bestScore > alpha_beta[0]):
                alpha_beta[0] = bestScore
        elif(currColor == "white"):
            if(bestScore == None or boardScore < bestScore):
                bestScore = boardScore
                bestBoard = possibleBoard
            if(alpha_beta[1] == None or bestScore < alpha_beta[1]):
                alpha_beta[1] = bestScore 
            if(canAlphaBetaPrun(alpha_beta,bestScore,currColor)):
                break
    return bestScore

def evaluateBoardScore(boardScore, bestScore):
    pass
def possibleChains(board,currColor,data):
    #Returns a list of sets of tuples, where each set is a chain of pieces
    chains = []
    for row in range(len(board)):
        for col in range(len(board[row])):
            if(board[row][col] == currColor):
                possibleChainsForPiece(board,currColor,data,row,col,chains)
    return chains
def possibleChainsForPiece(board,currColor,data,row,col,chains):
    pieceCoord = data.board3AxisCoords[row][col]
    chains.append(set([pieceCoord]))
    dirs = [(-1,+1, 0),(0,+1,-1),
        (-1, 0,+1),        (+1,0,-1),
            ( 0,-1,+1),(+1,-1, 0)]
    for direction in dirs:
        chainCoords = []
        (dx,dy,dz) = direction
        (x,y,z) = pieceCoord
        chainCoords.append(pieceCoord)
        while(getColorAtCoords(board,chainCoords[-1],data) == currColor):
            if(noRepeats(set(chainCoords),chains) == True):
                chains.append(set(chainCoords))
            (x,y,z) = chainCoords[-1]
            chainCoords.append((x+dx,y+dy,z+dz))
def noRepeats(currChain, chains):
    #Removes copies of the same chain
    for chain in chains:
        if(currChain == chain):
            return False
    return True
def possibleMoves(board,currColor,data):
    #Scans a board and returns a list of all possible moves.
    #The new moves are returned as new board states.
    possibleBoards = []
    dirs = [(-1,+1, 0),(0,+1,-1),
        (-1, 0,+1),        (+1,0,-1),
            ( 0,-1,+1),(+1,-1, 0)]
    chainsList = possibleChains(board,currColor,data)
    for chain in chainsList:
        for direction in dirs:
            #print("Checking Chain: ", chain, " in Direction: ", direction)
            newBoard = possibleMoveForChainInDirection(board,currColor,
                data,chain,direction)
            if(newBoard != None):
                possibleBoards.append(newBoard)
    return possibleBoards
def testIsInline():
    print("Testing isInline...", end = "")
    assert(isInline([(0,-1,1),(1,-2,1),(2,-3,1)],(-1,+1, 0)))
    assert(isInline([(1,-2,1),(0,-1,1),(2,-3,1)],(-1,+1, 0)))
    assert(isInline([(1,-2,1),(0,-1,1),(2,-3,1)],(+1,-1, 0)))
    print("Passed")
def isInline(chain,direction):
    for i in range(len(chain)-1):
        (x1,y1,z1) = chain[i]
        (x2,y2,z2) = chain[i+1]
        maxFactor = max(abs(x1-x2),abs(y1-y2),abs(z1-z2))
        chainDiff = ((x1-x2)//maxFactor,(y1-y2)//maxFactor,(z1-z2)//maxFactor)
        chainDiffRev=((x2-x1)//maxFactor,(y2-y1)//maxFactor,(z2-z1)//maxFactor)
        if(chainDiff != direction and chainDiffRev != direction): 
            return False
    return True
def possibleMoveForChainInDirection(board,currColor,data,chain,direction):
    #Checks if it is possible for a given chain to move in a given direction
    newChain = list(copy.deepcopy(chain))
    (dx,dy,dz) = direction
    broadsideMovePossible = True
    for i in range(len(newChain)):
        (x,y,z) = newChain[i]
        newPiece = (x+dx,y+dy,z+dz) 
        newChain[i] = newPiece
        if(getColorAtCoords(board,newPiece,data) != None):
            broadsideMovePossible = False
    if(broadsideMovePossible):
        #print("Make Broadside Move")
        return makeMove(board,currColor,data,chain,newChain)
    #Now check for a possible inline move or inline push
    if(isInline(newChain,direction) == False):
        return None
    inlineMovePossible = True
    pushMovePossible = True
    opposingChainStart = None
    newBoard = copy.deepcopy(board)
    for oldPiece in chain:
        setColorAtCoords(None,newBoard,oldPiece,data)
    for newPiece in newChain:
        checkSpot = getColorAtCoords(newBoard,newPiece,data)
        #print("checkspot: ",checkSpot)
        if(checkSpot != None):
            inlineMovePossible = False
            if(checkSpot == currColor or checkSpot == False):
                pushMovePossible = False
            else: #Opposite color
                opposingChainStart = newPiece
    if(inlineMovePossible):
        #print("Make Inline Move")
        return makeMove(board,currColor,data,chain,newChain)
    elif(pushMovePossible):
        #print("Make Inline Push Move")
        return makePushMove(board,currColor,data,chain,newChain,
        direction,opposingChainStart)
    
def makeMove(board,currColor,data,chain,newChain):
    #All pieces can be moved to an empty square, then the move is valid
    #Now make the new board
    newBoard = copy.deepcopy(board)
    for oldPiece in chain:
        setColorAtCoords(None,newBoard,oldPiece,data)
    for newPiece in newChain:
        setColorAtCoords(currColor,newBoard,newPiece,data)
    return newBoard
def makePushMove(board,currColor,data,chain,newChain,direction,
opposingChainStart):
    #Get the length of the current chain:
    #print("New chain: ", newChain)
    currChainLength = len(newChain)
    #Now, figure out the length of the opposing chain.
    opposingColor = getOpposingColor(currColor)
    currPiece = opposingChainStart
    opposingChainLength = 0
    opposingChain = []
    while(getColorAtCoords(board,currPiece,data) == opposingColor):
        opposingChain.append(currPiece)
        (x,y,z) = currPiece
        (dx,dy,dz) = direction
        currPiece = (x+dx,y+dy,z+dz)
        opposingChainLength += 1
    #print("currChainLength: ", currChainLength)
    #print("opposingChainLength: ", opposingChainLength)
    if(currChainLength > opposingChainLength):
        #first move the opposing chain:
        newOpposingChain = copy.deepcopy(opposingChain)
        for i in range(len(opposingChain)):
            (x,y,z) = newOpposingChain[i]
            newPiece = (x+dx,y+dy,z+dz) 
            newOpposingChain[i] = newPiece
            if(getColorAtCoords(board,newPiece,data) == currColor):
                return None
        newBoard = makeMove(board,opposingColor,data,
        opposingChain,newOpposingChain)
        return makeMove(newBoard,currColor,data,chain,newChain)
def getOpposingColor(currColor):
    if(currColor == "white"):
        return "black"
    else:
        return "white"

def getAdjacents(board,color,row,col,data):
    dirs = [(-1,+1, 0),(0,+1,-1),
            (-1, 0,+1),        (+1,0,-1),
                ( 0,-1,+1),(+1,-1, 0)]
    adjacents = []
    for direction in dirs:
        currCoord = data.board3AxisCoords[row][col]
        (x,y,z) = currCoord
        (dx,dy,dz) = direction
        newCoord = (x+dx,y+dy,z+dz)
        if(getColorAtCoords(board,newCoord,data) == color):
            adjacents.append(newCoord)
    return adjacents
def boardEvaluator(board, data):
    #Uses heuristics to score a current board based on who is winning.
    #High positive numbers indicate a black is winning, 
    #high negatives indicate white is winning.
    boardScore = 0
    boardScore += 20*evaluatePieceDifference(board, data)
    boardScore += evaluateControlOfCenter(board, data)
    return boardScore

def evaluatePieceDifference(board, data):
    #This checks which side has more pieces alive
    blackPieceCount = 0
    whitePieceCount = 0
    for row in range(len(board)):
        for col in range(len(board[row])):
            if(board[row][col] == "black"):
                blackPieceCount +=1
            elif(board[row][col] == "white"):
                whitePieceCount +=1
    return (blackPieceCount-whitePieceCount)
def evaluateControlOfCenter(board, data):
    #This checks which side has more control of the center
    centerControl = 0
    centerRow = data.hexesAcross//2
    centerCol = data.hexesAcross//2
    centerHex = (4,-4,0)
    for row in range(len(board)):
        for col in range(len(board[row])):
            currHex = data.board3AxisCoords[row][col]
            if(board[row][col] == "black"):
                centerControl += 4-hexDist(centerHex, currHex)
            elif(board[row][col] == "white"):
                centerControl -= 4-hexDist(centerHex, currHex)
    #print("Center control: ",centerControl)
    return centerControl
def hexDist(hex1,hex2):
    (x1,y1,z1) = hex1
    (x2,y2,z2) = hex2
    return max(abs(x1-x2),abs(y1-y2),abs(z1-z2))
def evaluateCompactness(board):
    #total distance between pieces - lower is better
    whitePieceDist = 0 
    blackPieceDist = 0

    pass
####################################
# use the run function as-is
####################################
##Citation: Tkinter MVC taken from 15-112 website:
##http://www.cs.cmu.edu/~112/notes/notes-animations.html
def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='light gray', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)
    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 500 # milliseconds
    initMenu(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(900, 600)