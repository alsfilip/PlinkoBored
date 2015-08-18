"""
August 18th, 2015 - Alex Filipowicz

This is meant to be a Plinko version used to test the effects of uncertain environments on boredom. This version will be a cup version in which participants are attempting to catch a ball using a cup that they can move from side to side, and whose width is static. The goal will be to expose participants to two environments, one highly uncertain and one less uncertain, and measure their boredom before and after each environment.

"""

from psychopy import core,event,visual,gui
import random
import os
import numpy as np
import time
import math
import Tkinter as tk

###############################################
# Participant information and data file setup #
###############################################

# Get participant data via GUI
infoBox = gui.Dlg(title = "Participant Information")
infoBox.addField('Participant Number: ')
infoBox.addField('Age: ')
infoBox.addField('Sex: ')
infoBox.addField('Condition (1 or 2): ')
infoBox.show()

if gui.OK:
    pData = infoBox.data
    participant = str(pData[0])
    age = str(pData[1])
    sex = str(pData[2]
    condition = str(pData[3])
elif gui.CANCEL:
    core.quit()

# Get directory for future data collection usage
path = os.getcwd()

# Set up data file
startTime = time.localtime()
datafile = file(path+"//data//" + participant +"_plinkoBored_cupData"+str(startTime.tm_mon)+str(startTime.tm_mday)+ "_" + str(startTime.tm_hour) + str(startTime.tm_min) + str(startTime.tm_sec)+".csv", "wb")

# Data file header
cupHeader = ["Participant", "Age", "Sex", "Condition", "Trial", "Distribution Number", "Ball Position", "CompMean", "OptimalPos", "CupMean","CupLeft","CupRight", "BallCaught", "TotalScore", "CupRT"]
datafile.write(",".join(cupHeader)+"\n")


############################
# Plinko environment setup #
############################

# Get screen dimensions
root = tk.Tk()
screenX = root.winfo_screenwidth()
screenY = root.winfo_screenheight()
screenSize = (screenX,screenY)

# Build default plinko table size according to window size
tableWidth = screenX*0.8
tableHeight = screenY*0.5

# Ball speed
moveTime =  [0.015]

# Initialize window and mouse
win = visual.Window(size = screenSize, color = "grey", units = "pix", fullscr = True, screen = 1)
mouse = event.Mouse(win=win)

# Distributions to be estimated
highUncert = [40,40,40,40,40]
lowUncert = [1,1,1,1,1]

# Order of distributions depending on condition (1 or 2 specified in GUI)
if condition == "1":
	blockOrder = [highUncert,lowUncert]
elif condition == "2":
	blockOrder = [lowUncert, highUncert]

#Plinko Table specifications
pegRowNum = 29
pegSep = (screenX*0.8)/pegRowNum
rowSep = (screenY*0.5)/pegRowNum
pegRadius = 2.5
topPegY = (screenY/2)/1.2
topPegX = 0

# Draw Plinko board with specified number of pegs
pegY = topPegY
count = 0
for row in range(pegRowNum):
    pegSpread = pegSep*row
    pegX = -(pegSpread/2)
    for peg in range(row+1):
        dowel = visual.Circle(win, radius = pegRadius, fillColor = "black", pos = (pegX,pegY), lineColor = "grey")
        dowel.draw()
        pegX += pegSep
    pegY -= rowSep

#Ball slot positions and specifications
slotNum = 40 #number of slots wanted
slotWidth = tableWidth/slotNum
spread = slotWidth/2
slotHeight = 20
slotY = topPegY - (rowSep*pegRowNum)-(slotHeight/2)+5
slotX = -(tableWidth/2)+(slotWidth/2)
slotPos = []
slotSpread = []
slotLimits = []

for slot in range(slotNum):

    slotPos.append((slotX,slotY))

    slotCoins.append([])

    slotX += slotWidth



for pos in slotPos:

    slotSpread.append((pos[0]-spread,pos[0]+spread))

    #Draw slots to be buffered

    slotSquare = visual.Rect(win, width = slotWidth, height=slotHeight, pos = pos, lineColor = "white", lineWidth = 2, fillColor="grey")

    bar = visual.Rect(win, height = 0, width = slotWidth, fillColor = "blue", pos = pos, opacity = 0.7) #Draws all bet rectangles and specifies their x - all that's needed now is to specify the y in order to reflect the person's bet

    barList.append(bar)

    slotSquare.draw()



#Initialize datafiles for cup and bars



barHeader = ["Participant", "Answer Type", "Condition","Trial", "Block Number","Distribution Number", "Ball Position", "Slot Number", "Participant Slot Estimate", "Slot Height","Comp Ball Drop", "Participant Mean", "Participant SD", "Bar RT"]



barDataFile = None

cupDataFile = None 

if int(answerType) == 2:

    barDataFile = file(path+"//data//barData//" + participant + "_plinkoRBD_barData" +str(startTime.tm_mon)+str(startTime.tm_mday)+ "_" + str(startTime.tm_hour) + str(startTime.tm_min) + str(startTime.tm_sec)+".csv", "wb")

    barDataFile.write(",".join(barHeader)+"\n")

if int(answerType) == 1:

    cupDataFile = file(path+"//data//cupData//" + participant+"_plinkoRBD_cupData"+str(startTime.tm_mon)+str(startTime.tm_mday)+ "_" + str(startTime.tm_hour) + str(startTime.tm_min) + str(startTime.tm_sec)+".csv", "wb")

    cupDataFile.write(",".join(cupHeader)+"\n")





#Bet slot specifications + bet area

maxBetCoins = 100

betSlotHeight = screenY/5

betSlotY = slotY - slotHeight - (betSlotHeight/2)

betArea = visual.Rect(win, height = betSlotHeight, width = tableWidth, pos = (0, betSlotY), fillColor = "grey", lineColor = "white", lineWidth = 2)

betArea.draw()

playerScore = 0 #running player score that is incremented in the betting function

tallyX = screenX/4

tallyY = topPegY-100

scoreX = 0

scoreY = -(screenY/2) + 100

totalScorePos = (tallyX,tallyY)

scorePos = (scoreX,scoreY)

tallyText = "Total score: "

runningTally = visual.TextStim(win, text = tallyText + str(playerScore), height = 20, pos = totalScorePos)

trialScoreDisplay = visual.TextStim(win, text = "+ ", height = 40, pos = scorePos) #Initialize points for every trial

trialPoints = None

totalCoins = 0 #Keeps count of the number of balls a person has left to place when asked about probability



#Coin y coordinates

betYstart = betSlotY - (betSlotHeight/2)

coinY= betYstart

coinHeight = betSlotHeight/float(maxBetCoins)

coinSpread = []

for coins in range(maxBetCoins):

    coinY += coinHeight

    coinSpread.append(coinY)



#Cuts top off of slots

slotTopY = slotY+ slotHeight/2

slotTop = visual.Rect(win, width = tableWidth, height =5, pos = (0,slotTopY), fillColor = "grey", lineColor = "grey", lineWidth = 2)

slotTop.draw()



#Ball specifications

ballRadius = pegRadius*2

ballStart = (0, (topPegY+ballRadius+pegRadius))

ball = visual.Circle(win, radius = ballRadius, fillColor = "red", pos = ballStart)





#Specify spaces between pegs in bottom row to know where ball can come from

bottomPegSep = []

pegY = topPegY - ((pegRowNum-1)*rowSep)

pegX = -(((pegRowNum)*pegSep)/2)- (pegSep)

for peg in range(pegRowNum+1):

    pegX += pegSep

    bottomPegSep.append((pegX,pegY))



#Returns an array of curve vertices that allows for us to add in different functions that would be called later

def getCurve(function):

    vertexWidth = int(slotWidth) + int(slotWidth)%2

    global vertexHeight

    vertexHeight = betSlotY-(betSlotHeight/2)+2

    global curveStartY

    curvePoints = []

    for i in range(vertexWidth+1):

        curveX = (-vertexWidth/2)+i

        if function == 'q':

            curvePoints.append((curveX,curveX**2+vertexHeight))

            if i == 0:

                curveStartY = (curveX**2+vertexHeight)

    return(curvePoints)



#Initialize cup parameters

curveShape = 'q'

curveStartY = 0

posMove = slotWidth

vertPos = 20

curve = visual.ShapeStim(win=win, lineColor='blue', fillColor='lightblue', lineWidth = 3, vertices = getCurve(curveShape), opacity = 0.8)

desiredStartY = slotY-20

absHeightOffset = desiredStartY-curveStartY

curveHeight = -vertexHeight+curveStartY

relCurveHeight = betSlotHeight/curveHeight #size of curve relative to betSlotHeight

startSizeOffset = absHeightOffset/curveHeight

curve.setSize((0,startSizeOffset),'+')

curve.setPos((0,vertexHeight*startSizeOffset),'-')

if int(slotNum)%2 == 0:curve.setPos((slotWidth/2,0),'+') # Move cup over when slotNum even



#Buffer plinko table and bet slots (quicker to load on each ball movement than generating pegs every time)

plinkoTable = visual.BufferImageStim(win) 

betSpace = None

curveBuffer = None



#Loads items that will be refreshed throughout task

betRect = visual.Rect(win, height = betSlotHeight, width = slotWidth, fillColor = "grey", pos = (0,0), lineWidth = 2, opacity = 0.5) #Rectangle that follows cursor in bet space



#Lists to keep track of participant bar accuracy (List of the probability of each slot on each trial)

computerBars = {}

participantBars = {}

for slot in range(1,41):

    computerBars[slot] = []

    participantBars[slot] = []



#Generates ball path on each trial based on end point

def ballPath(endPoint):

    bPath = []

    ballY = topPegY - ((pegRowNum-1)*rowSep)

    startY = topPegY + ballRadius + pegRadius

    startPoint = (topPegX, startY)

    ballX = 0

    #figure out which bottom peg gaps are nearest the selected slot

    for pos in bottomPegSep:

        x = pos[0]

        nextPos = bottomPegSep.index(pos)+1

        nextX = 0

        if endPoint == slotPos[0]:

            ballX = x

            break

        elif nextPos == len(bottomPegSep):

            nextX = bottomPegSep[-1][0]

            ballX = x

            break

        else:

            nextX = bottomPegSep[nextPos][0]

            if endPoint[0] >= x and endPoint[0] <= nextX:

                ballX = random.choice([x,nextX])

                break

    bPath.append((ballX,ballY))

    #Draw path to start

    rowNum = pegRowNum

    for peg in range(pegRowNum):

        leftBoundary = -((pegSep*rowNum)/2)

        rightBoundary = (pegSep*rowNum)/2

        shift = pegSep/2

        xMove = [-shift, shift]

        if (ballX + xMove[0]) < leftBoundary:

            ballX += shift

        elif (ballX + xMove[1]) > rightBoundary:

            ballX -= shift

        else:

            ballX += random.choice(xMove)

        ballY += (ballRadius+pegRadius)

        bPath.append((ballX,ballY))

        ballY += rowSep-(ballRadius+pegRadius)

        bPath.append((ballX,ballY))

        rowNum -= 1

    bPath.append(startPoint)

    bPath.reverse()

    return bPath



#Responsible for animating the ball going through the plinko table

def ballTrack(ballPath, endPos, cup = False, score = False):

    win.clearBuffer()

    clock = core.Clock()

    for pos in ballPath:

        if betSpace != None:

            betSpace.draw()

        else:

            plinkoTable.draw()

        if score == True:

            runningTally.setText(tallyText+str(playerScore))

            runningTally.draw()

        ball.setPos(pos)

        if cup == True:

            curve.draw()

        ball.draw()

        win.flip()

        core.wait(random.choice(moveTime))

    ball.setPos(endPos)

    if betSpace != None:

        betSpace.draw()

    else:

        plinkoTable.draw()

    ball.draw()

    if cup == True:

        curve.draw()

    win.flip()



#Draws only the bet area (without ball or rectangle) - used to buffer a screen shot of the table plus previous bets

def drawBetArea(betList):

    slotCount = 0

    for coinList in betList:

        if len(coinList) > 0:

            numCoins = len(coinList)

            betWidth = slotWidth

            betX = slotPos[slotCount][0]

            betHeight = coinHeight*numCoins

            betY = betYstart + (betHeight/2)

            bet = barList[slotCount]

            bet.setPos((betX,betY))

            bet.setHeight(betHeight)

            bet.draw()

        slotCount +=1



#Draws bet area with ball and rectangle that follows the mouse to show you which slot you're betting on

def drawBets(betList, rectX = None, bP = None, flipScreen = True):

    betYstart = betSlotY - (betSlotHeight/2)

    plinkoTable.draw()

    if bP == True:

        ball.draw()

    elif bP != None:

        ball.setPos(bP)

        ball.draw()

    if rectX != None:

        betRect.setPos((rectX, betSlotY))

        betRect.draw()

    drawBetArea(betList)

    if flipScreen == True:

        win.flip()



#Draws cup in bet rectangle

def drawCurve(curve, score, points=None, ballDraw = None):

    win.clearBuffer()

    txtNum = visual.TextStim(win,text=score, height = 20, pos = (curve._posRendered[0],slotY-betSlotHeight-40))

    runningTally.setText(tallyText+str(playerScore))

    if betSpace != None:

        betSpace.draw()

    else:

        plinkoTable.draw()

    curve.draw()

    runningTally.draw()

    txtNum.draw()

    if points != None:

        trialScoreDisplay.setText("+"+str(points))

        if points < 6:

            trialScoreDisplay.setColor("red")

        elif points > 5 and points < 11:

            trialScoreDisplay.setColor("orange")

        elif points > 10 and points < 16:

            trialScoreDisplay.setColor("yellow")

        elif points > 15 and points < 18:

            trialScoreDisplay.setColor("lightblue")

        elif points >17:

            trialScoreDisplay.setColor("lightgreen")

        trialScoreDisplay.draw()

    if ballDraw != None:

        ball.draw()

    win.flip()



#Returns slot in which the mouse is positioned

def getSlot(mouseX, mouseY, slotSpread):

    slotNum = None

    for spread in slotSpread:

        if mouseX > spread[0] and mouseX < spread[1] and mouseY < (betSlotY+(betSlotHeight/2)) and mouseY > (betSlotY-(betSlotHeight/2)):

            slotNum = slotSpread.index(spread)

            break

        else:

            pass

    return slotNum



def getCoinNum(mouseY):

    coinNum = None

    for spread in coinSpread:

        if mouseY < spread:

            if mouseY <= (betYstart+(coinHeight/2)):

                coinNum = -1

            else:

                coinNum = coinSpread.index(spread)

            break

        else:

            pass

    return coinNum



def getSubProbData():

    subSpread = []

    slotFrequency = []

    slotTracker = 1

    for prob in slotCoins:

        probNum = len(prob)

        subSpread.append(probNum)

    for slot in subSpread:

        for num in range(slot):

            slotFrequency.append(slotTracker)

        slotTracker += 1

    subMean = np.mean(slotFrequency)

    subSD = np.std(slotFrequency)

    return subMean, subSD, subSpread



#Returns the appropriate curve width multiplier

def getWidthInc():

    originalCurveWidth = abs(curve.vertices[0,0]*2) #Calculates width of curve as drawn

    widthInc = (slotWidth*2/originalCurveWidth)

    return widthInc



#Returns the appropriate curve height multiplier

def getHeightInc():

    numMovesPossible = 20 #Max number of user cup height adjustments allowed

    relCurveHeight = betSlotHeight/curveHeight #size of curve relative to betSlotHeight

    heightInc = relCurveHeight/numMovesPossible

    return heightInc



#Returns the appropriate post-curve resizing adjustment to keep curve on the same plane

def getPosOffset():

    tempResize = getHeightInc()

    curve.draw()

    startCurveY = curve._verticesRendered[0,1]

    curve.setSize((0,tempResize),'-')

    curve.draw()

    newCurveY = curve._verticesRendered[0,1]

    posOffset = newCurveY-startCurveY

    curve.setSize((0,tempResize),'+')

    return posOffset



#Returns whether the ball landed in the cup

def getCupTrialResult(leftSlot,rightSlot,ballSlot):

    global playerScore, trialPoints

    if leftSlot <= ballSlot and rightSlot >= ballSlot:

        playerScore += vertPos #implement player score if necessary

        trialPoints = vertPos

        return True

    else:

        return False



def getCupData(leftCupEnd, rightCupEnd):

    spreadTracker = []

    cupSpread = range(leftCupEnd,rightCupEnd+1)

    for num in range(slotNum):

        if num in cupSpread:

            spreadTracker.append(1)

        else:

            spreadTracker.append(0)

    cupWidth = rightCupEnd+1-leftCupEnd

    cupMean = (rightCupEnd - (cupWidth/2))+1 #+1 to account for computer starting from 0

    return cupMean, cupWidth, spreadTracker



#Records bar data

def recordBarData(trial, bN,dist, ballP, rt):

    subCoins = 0.0
    subCoinList = []

    subData = getSubProbData()

    slotYPass = (betSlotY+(betSlotHeight/2))+(betSlotY+(betSlotHeight/2))/2

    ballSlot = getSlot(ballP[0], slotYPass, slotSpread)

    bP = ballSlot + 1

    for coinList in slotCoins:

        subCoins += len(coinList)
        subCoinList.append(len(coinList))

    subProbList = []

    for coinList in slotCoins:

        subProb = len(coinList)/subCoins

        subProbList.append(subProb)
    for i in range(0,slotNum):
        subProb = subProbList[i]
        subSlotHeight = subCoinList[i]

        if (i+1) == bP:

            compTrialProb = 1

            computerBars[i+1].append(1)

        else: 

            compTrialProb = 0

            computerBars[i+1].append(0)

        rawData = [str(participant), str(answerType), str(condition),str(trial), str(bN),str(dist), str(bP), str(i+1), str(subProb), str(subSlotHeight),str(compTrialProb), str(subData[0]), str(subData[1]), str(rt)]

        barDataFile.write(",".join(rawData)+"\n")

        barDataFile.flush()



def recordCupData(trial, bN, dist, ballP, cupM, cupS, cupL, cupR, inCup, cupRT):

    slotYPass = (betSlotY+(betSlotHeight/2))+(betSlotY+(betSlotHeight/2))/2

    bfromM = ballP-cupM

    rawData = [str(participant), str(answerType), str(condition),str(trial), str(bN),str(dist), str(ballP), str(trialPoints), str(playerScore), str(cupM), str(cupS), str(cupL), str(cupR), str(bfromM), str(inCup), str(cupRT)]

    cupDataFile.write(",".join(rawData)+"\n")

    cupDataFile.flush()



#Gets participant probability bars

def getBet(ballPos, dist, bP, trial, bN):

    global betSpace, totalCoins

    event.clearEvents()

    win.clearBuffer()

    drawBets(slotCoins)

    betting = True

    rectX = None

    initBallPos = bP[0]

    barClock = core.Clock()

    totalUsed = 0

    while betting:

        for key in event.getKeys():

            if key in ['q']:

                core.quit()

            if key in ['space']:

                totalUsed = []

                for betList in slotCoins:

                    totalUsed.append(len(betList))

                if sum(totalUsed) > 0:

                    betting = False

                else:

                    pass

            if key in ['backspace']:

                for coinList in slotCoins:

                    del coinList[:]

                    totalCoins = 0

        mouseX, mouseY = mouse.getPos()

        slotSpot = getSlot(mouseX, mouseY, slotSpread)

        if slotSpot != None:

            rectX = slotPos[slotSpot][0]

        if trial == 1:

            drawBets(slotCoins, bP = initBallPos, rectX = rectX)

        else:

            drawBets(slotCoins, bP = True, rectX = rectX)

        left, middle, right = mouse.getPressed()

        if slotSpot != None:

            betSlot = slotCoins[slotSpot]

            coinNum = getCoinNum(mouseY)

            bet = coinNum + 1

            if right ==1:

                del betSlot[:]

            if left == 1:

                currBetInSlot = len(betSlot)

                del betSlot[:]

                coinCounter = 0

                for coin in range(bet):

                    betSlot.append(1)

                    coinCounter += 1

                totalCoins = 0

                for l in slotCoins:

                    coinsUsed = len(l)

                    totalCoins += coinsUsed

#        time.sleep(0.01)

    #Enter bar data collection here - 

    barRT = barClock.getTime()

    recordBarData(trial, bN, dist, ballPos, barRT)

    plinkoTable.draw()

    drawBets(slotCoins, bP=None, rectX = None, flipScreen =False)

    betSpace = visual.BufferImageStim(win)

    ballTrack(bP, ballPos)



#Cup Mouse Implementation

def getCupMouseBet(compPlay, ballPos, trial, distNum, ballPath,bN): 

    global playerScore, trialPoints #Keeps track of player score across trials if desired

    global vertPos	#Keeps track of how many depth moves available to calculate score

    global curveBuffer

    event.clearEvents()

    slotCheckFeather = slotWidth/10

    horizSizeInc = getWidthInc() #Scales the width multiplier

    vertSizeInc = getHeightInc() #Scales the height multiplier

    vertPosOffset = getPosOffset() #Determines post-curve resizing movement amount

    slotYPass = (betSlotY+(betSlotHeight/2))+(betSlotY+(betSlotHeight/2))/2

    leftEdge = -tableWidth/2

    rightEdge = tableWidth/2

    leftEnd = curve._posRendered[0]+(curve.size[0]*curve.vertices[0,0])

    leftEndInSlot = getSlot(leftEnd+(slotCheckFeather),slotYPass,slotSpread)

    rightEnd = curve._posRendered[0]+(curve.size[0]*curve.vertices[-1,0])

    rightEndInSlot = getSlot(rightEnd-(slotCheckFeather),slotYPass,slotSpread)

    cupClock = core.Clock()

    mousepress = 2

    while True:	#Allows user to manipulate the cup with the mouse

        time.sleep(0.01)

        mouseDX,mouseDY = mouse.getRel()

        mouse1,mouse2,mouse3 = mouse.getPressed()

        wheelDX,wheelDY = mouse.getWheelRel()

        if mouse1: #Hold down left mouse and move mouse to reposition cup

            time.sleep(0.01)

            curve.setFillColor('white')

            curve.setPos([mouseDX,0],'+')

            drawCurve(curve,vertPos, points = trialPoints, ballDraw = ballPos)

            curve.draw()

            curve._calcVerticesRendered

            leftEnd = curve._posRendered[0]+(curve.size[0]*curve.vertices[0,0])

            rightEnd = curve._posRendered[0]+(curve.size[0]*curve.vertices[-1,0])

            mousepress=2

        if wheelDY>0 and vertPos > 1: #Scroll mouse-wheel up to widen cup

            vertPos -= 1

            if rightEnd+1 > rightEdge:

                curve.setSize((horizSizeInc,0),'+')

                curve.setSize((0,vertSizeInc),'-')

                curve.setPos((posMove,0),'-')

                leftEnd -= 2

            elif leftEnd-1 < leftEdge:

                curve.setSize((horizSizeInc,0),'+')

                curve.setSize((0,vertSizeInc),'-')

                curve.setPos((posMove,0),'+')

                rightEnd += 2

            else:

                curve.setSize((horizSizeInc,0),'+')

                curve.setSize((0,vertSizeInc),'-')

            curve.setPos((0,vertPosOffset),'-')

            drawCurve(curve,vertPos, points = trialPoints, ballDraw = ballPos)

            leftEnd = curve._posRendered[0]+(curve.size[0]*curve.vertices[0,0])

            rightEnd = curve._posRendered[0]+(curve.size[0]*curve.vertices[-1,0])

        if wheelDY<0 and vertPos < 20: #Scroll mouse-wheel down to shrink cup

            curve.setSize((horizSizeInc,0),'-')

            curve.setSize((0,vertSizeInc),'+')

            vertPos += 1

            curve.setPos((0,vertPosOffset),'+')

            drawCurve(curve,vertPos, points = trialPoints, ballDraw = ballPos)

            curve.draw()

            curve._calcVerticesRendered

            leftEnd = curve._posRendered[0]+(curve.size[0]*curve.vertices[0,0])

            rightEnd = curve._posRendered[0]+(curve.size[0]*curve.vertices[-1,0])

        if keyboard[pyglet.window.key.SPACE]: #Press right mouse button to confirm prediction and proceed to trial

            break

        if keyboard[pyglet.window.key.Q] == True: # Press Q to quit

            core.quit()

            exit()

        if mouse1==False and mousepress: #Snaps cup into position after user lets go of the mouse button

            mousepress -=1

            curve.setFillColor('lightblue')

            leftEnd = curve._posRendered[0]+(curve.size[0]*curve.vertices[0,0])

            rightEnd = curve._posRendered[0]+(curve.size[0]*curve.vertices[-1,0])

            if leftEnd<leftEdge: 

                snapRel = leftEdge-leftEnd

                curve.setPos((snapRel,0),'+')

            elif rightEnd>rightEdge+(slotCheckFeather):

                snapRel = rightEnd-rightEdge

                curve.setPos((snapRel,0),'-')

            elif leftEnd>=leftEdge: #Aligns cup with slots where left closest to

                leftEndInSlot = getSlot(leftEnd+(slotCheckFeather),slotYPass,slotSpread)

                linesInSlotX = slotSpread[leftEndInSlot]

                middleXSlot = np.mean(linesInSlotX)

                leftLineInSlot = linesInSlotX[0]

                rightLineInSlot = linesInSlotX[1]

            if leftEnd<=middleXSlot:

                snapRel = leftEnd-leftLineInSlot

                curve.setPos((snapRel,0),'-')

            elif leftEnd>middleXSlot:

                snapRel = rightLineInSlot-leftEnd

                curve.setPos((snapRel,0),'+')

            drawCurve(curve,vertPos, points = trialPoints, ballDraw = ballPos)

    cupRT = cupClock.getTime()

    ballTrack(ballPath, ballPos,cup = True, score = True)

    ballSlot = getSlot(ballPos[0],slotYPass,slotSpread)

    leftEnd = curve._posRendered[0]+(curve.size[0]*curve.vertices[0,0])

    leftEndInSlot = getSlot(leftEnd+(slotCheckFeather),slotYPass,slotSpread)

    rightEnd = curve._posRendered[0]+(curve.size[0]*curve.vertices[-1,0])

    rightEndInSlot = getSlot(rightEnd-(slotCheckFeather),slotYPass,slotSpread)

    caughtBall = getCupTrialResult(leftEndInSlot,rightEndInSlot,ballSlot)

    plays = getCupData(leftEndInSlot,rightEndInSlot)

    if caughtBall == False:

        trialPoints = 0

    recordCupData(trial, bN,distNum, compPlay, plays[0], plays[1], (leftEndInSlot+1), (rightEndInSlot+1), caughtBall, cupRT)


#Get density of participant distribution and computer distribution to give accuracy score
def getDense(dat = None, pDist=True):
    dense=[]
    if pDist == True:
        for barList in slotCoins:
            dense.append(len(barList)/float(totalCoins))
    if pDist == False:
        for i in range(0,40):
            dense.append(dat.count(i)/float(len(dat)))
    return dense

#Accuracy function for map function
def accMap(d1,d2):
    ac=map(min,d1,d2)
    print round(sum(ac),4)*100
    return round(sum(ac),4)*100

#Computer % overlap between computer distribution density and participant bar density

def accuracyScore(ballList):
    slotDense=getDense()
    compDense=getDense(dat=ballList,pDist=False)
    return accMap(slotDense, compDense)



#Score display between distributions

def interScreen(tType, ac, end = False):

    win.clearBuffer()

    iTxt = None

#    if show == False:

#    	pass

    if end == True:

        if tType == 2:

            barDataFile.close()

        elif tType == 1:

            cupDataFile.close()

        if tType == 1:

            iTxt = "Cup Score: " + str(playerScore)+"\n\nThank you for your participation. Please see the RA for the questionnaire protion of the experiment."

        elif tType == 2:

            iTxt = "Bar Accuracy: " + str(ac)+"%\n\nThank you for your participation. Please see the RA for the questionnaire protion of the experiment."

    else:

        if tType == 1:

            iTxt = "Cup Score: " + str(playerScore)+"\n\nEnd of block 1. Press enter to continue to the next block."

        elif tType == 2:

            iTxt = "Bar Accuracy: " + str(ac)+"%\n\nEnd of block 1. Press enter to continue to the next block."

#	if show == True:	

	interText = visual.TextStim(win, text = iTxt, height = 30, wrapWidth = screenX*0.8)

	interText.draw()

	win.flip()

	key = event.waitKeys(keyList = ['q','return'])

	if key[0] == 'q':

		core.quit()



def hack():

    test = visual.TextStim(win, text = "", height = 30)

    test.draw()

    win.flip()

    core.wait(0.01)



def endScreen(tType, acc, sc):

	if tType == 2:

		barDataFile.close()

	elif tType == 1:

		cupDataFile.close()

	if tType == 1:

		iTxt = "Cup Score: " + str(sc)+"\n\nThank you for your participation. Please see the RA for the questionnaire protion of the experiment."

	elif tType == 2:

		iTxt = "Bar Accuracy: " + str(acc)+"%\n\nThank you for your participation. Please see the RA for the questionnaire protion of the experiment."

	txtDisplay = visual.TextStim(win, text = iTxt, height = 30, wrapWidth = screenX*0.8)

	txtDisplay.draw()

	win.flip()

	key = event.waitKeys(keyList = ['q','return'])

	if key[0] == 'q':

		core.quit()



trialNum = 0



s = False
finalScore = 0
blockNum = None
if condition == "1":
    blockNum = 1
elif condition == "2":
    blockNum = 2

for block in blockOrder:
    if answerType == "1":
        #Initialize cup parameters
        curveShape = 'q'
        curveStartY = 0
        posMove = slotWidth
        vertPos = 20
        curve = visual.ShapeStim(win=win, lineColor='blue', fillColor='lightblue', lineWidth = 3, vertices = getCurve(curveShape), opacity = 0.8)
        desiredStartY = slotY-20
        absHeightOffset = desiredStartY-curveStartY
        curveHeight = -vertexHeight+curveStartY
        relCurveHeight = betSlotHeight/curveHeight #size of curve relative to betSlotHeight
        startSizeOffset = absHeightOffset/curveHeight
        curve.setSize((0,startSizeOffset),'+')
        curve.setPos((0,vertexHeight*startSizeOffset),'-')
        if int(slotNum)%2 == 0:curve.setPos((slotWidth/2,0),'+') # Move cup over when slotNum even
    acc = []
    distNum = 1

    for dist in block:

        endPosition = None

        distTrial = 0

        for pos in dist:

            distTrial += 1

            trialNum +=1

            endPosition = slotPos[pos]

            bP = ballPath(endPosition)

            if int(answerType) == 1:

                getCupMouseBet(pos+1, endPosition, trialNum, distNum, bP,blockNum)

            elif int(answerType) == 2:

                getBet(endPosition, distNum, bP, trialNum,blockNum)

        if int(answerType) == 2:

            distAcc = accuracyScore(dist)
            print distAcc

            acc.append(distAcc)

        for slot in computerBars:

            computerBars[slot] = []

        distNum += 1

    core.wait(0.5)

    hack()

    accuracy = round(np.mean(acc),2)

    interScreen(int(answerType), accuracy, end = s)

    s = True

    for coinList in slotCoins:

    	del coinList[:]

        totalCoins = 0
    finalScore = playerScore
    playerScore = 0
    if condition == "1":
        blockNum += 1
    elif condition == "2":
        blockNum -=1

    ball.setPos(ballStart)

endScreen(int(answerType), round(np.mean(acc),2),finalScore)

#interScreen(int(answerType), accuracy, end = True)



