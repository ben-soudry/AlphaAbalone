import math
from tkinter import *
import copy

####################################
# customize these functions
####################################

def init(data):
    data.boardWidth = 550
    data.hexesPerSide = 5 #A standard abalone board has side length 5 hexes
    data.hexesAcross = 2*data.hexesPerSide-1
    data.hexSize = data.boardWidth//data.hexesAcross
    data.spotRadius = 23
    data.pieceRadius = 26
    data.textHeight = 30
    
    createBoardLists(data)
    setUpBoard(data)
    assign3AxisCoords(data)
    createPieceLists(data)
    
    print(getColorAtCoords(data.board,(3,-2,-1),data))

    print("Overall Board Score: ", boardEvaluator(data.board,data))
    pass
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
def createPieceLists(data):
    data.whitePieceList = []
    data.blackPieceList = []
    for row in range(len(data.board)):
        for col in range(len(data.board[row])):
            if(data.board[row][col] == "white"):
                data.whitePieceList.append(piece(row,col,"white",data))
            elif(data.board[row][col] == "black"):
                data.blackPieceList.append(piece(row,col,"black",data))
def getColorAtCoords(board,coords,data):
    for row in range(len(board)):
        for col in range(len(board[row])):
            if(data.board3AxisCoords[row][col] == coords):
                return board[row][col]
    return False
def setColorAtCoords(color,board,coords,data):
    print("Setting ", color, " at ", coords)
    for row in range(len(board)):
        for col in range(len(board[row])):
            if(data.board3AxisCoords[row][col] == coords):
                board[row][col] = color
class piece(object):
    def __init__(self,row,col,color,data):
        self.row = row
        self.col = col
        self.color = color
        self.coord = data.board3AxisCoords[row][col]
    def possibleChains(self):
        dirs = [(-1,+1, 0),(0,+1,-1),
            (-1, 0,+1),        (+1,0,-1),
                ( 0,-1,+1),(+1,-1, 0)]
        chains = []
        for direction in dirs:
            (dx,dy,dz) = direction
            (x,y,z) = self.coord
            chains.append(self.coords)
            
            newChains = possibleChainsRecursive(direction,newCoord)
            if(newChains != None):
                chains.extend(newChains)
    def possibleChainsRecursive(direction,coord):
        if(data.boardDict[newCoord] == self.color):
            (dx,dy,dz) = direction
            newCoord = (x+dx,y+dy,+z+dz)
            result = coord + possibleChainsRecursive(direction,newCoord)
        else:
            return None
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
    pass

def keyPressed(event, data):
    if(event.keysym == "c"):
        chains = possibleChains(data.board,"white",data)
        print(chains)
    elif(event.keysym == "m"):
        possibleBoards = possibleMoves(data.board,"black",data)
        bestScore = None
        bestBoard = None
        for possibleBoard in possibleBoards:
            #print("Possible Board: ", possibleBoard)
            boardScore = boardEvaluator(possibleBoard,data)
            if(bestScore == None or boardScore > bestScore):
                bestScore = boardScore
                bestBoard = possibleBoard
        data.board = bestBoard
    if(event.keysym == "n"):
        possibleBoards = possibleMoves(data.board,"white",data)
        bestScore = None
        bestBoard = None
        for possibleBoard in possibleBoards:
            boardScore = boardEvaluator(possibleBoard,data)
            if(bestScore == None or boardScore < bestScore):
                bestScore = boardScore
                bestBoard = possibleBoard
        data.board = bestBoard
    pass

def timerFired(data):
    pass

def redrawAll(canvas, data):
    drawText(canvas, data)
    drawBoard(canvas, data)
    drawPieces(canvas, data)
    pass
def drawText(canvas,data):
    canvas.create_text(data.width//2,data.textHeight,text = "AlphaAbalone")
def drawBoard(canvas, data):
    cx = data.width//2
    cy = data.height//2
    r = data.boardWidth//2
    cos60 = math.cos(math.pi/3)
    sin60 = math.sin(math.pi/3)  
    #Draw hexagonal board 
    canvas.create_polygon(cx-r,cy,cx-r*cos60,cy-r*sin60,cx+r*cos60,cy-r*sin60,cx+r,cy,
        cx+r*cos60,cy+r*sin60,cx-r*cos60,cy+r*sin60,fill = "sienna")
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
    for i in range(data.hexesAcross):
        rowLength = getRowLength(i,data)
        for j in range(rowLength):
            (pieceX,pieceY) = data.boardScreenPos[i][j]
            if(data.board[i][j] == "white"):
                canvas.create_oval(pieceX-data.pieceRadius,pieceY-data.pieceRadius,
                pieceX+data.pieceRadius,pieceY+data.pieceRadius, fill = "white")
            elif(data.board[i][j] == "black"):
                canvas.create_oval(pieceX-data.spotRadius,pieceY-data.spotRadius,
                pieceX+data.pieceRadius,pieceY+data.pieceRadius, fill = "black")
            canvas.create_text(pieceX,pieceY,text = str(data.board3AxisCoords[i][j]),fill= "green")
    pass
####
#Controls
####

####
#AI
####
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
            print("Checking Chain: ", chain, " in Direction: ", direction)
            newBoard = possibleMoveForChainInDirection(board,currColor,
                data,chain,direction)
            if(newBoard != None):
                print("This ran")
                possibleBoards.append(newBoard)

    return possibleBoards
def possibleMoveForChainInDirection(board,currColor,data,chain,direction):
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
        return makeMove(board,currColor,data,chain,newChain)
    #Now check for a possible inline move
    inlineMovePossible = True
    newBoard = copy.deepcopy(board)
    for oldPiece in chain:
        setColorAtCoords(None,newBoard,oldPiece,data)
    for newPiece in newChain:
        if(getColorAtCoords(newBoard,newPiece,data) != None):
            inlineMovePossible = False
    if(inlineMovePossible):
        return makeMove(board,currColor,data,chain,newChain)
def makeMove(board,currColor,data,chain,newChain):
    #All pieces can be moved to an empty square, then the move is valid
    #Now make the new board
    newBoard = copy.deepcopy(board)
    for oldPiece in chain:
        print("Deleted old piece")
        setColorAtCoords(None,newBoard,oldPiece,data)
    for newPiece in newChain:
        print("Created new Piece")
        setColorAtCoords(currColor,newBoard,newPiece,data)
    return newBoard
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
    #High positive numbers indicate a black is winning, high negatives indicate white is.
    boardScore = 0
    boardScore += 10*evaluatePieceDifference(board, data)
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
    print("Center control: ",centerControl)
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

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
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
    data.timerDelay = 100 # milliseconds
    init(data)
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