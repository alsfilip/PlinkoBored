"""
August 18th, 2015 - Alex Filipowicz

This is meant to be a Plinko version used to test the effects of uncertain environments on boredom. This version will be a cup version in which participants are attempting to catch a ball using a cup that they can move from side to side, and whose width is static. The goal will be to expose participants to two environments, one highly uncertain and one less uncertain, and measure their boredom before and after each environment.

"""

from psychopy import core,event,visual,gui
import pyglet, copy
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
#infoBox = gui.Dlg(title = "Participant Information")
#infoBox.addField('Participant Number: ')
#infoBox.addField('Age: ')
#infoBox.addField('Sex: ')
#infoBox.addField('Condition (1 or 2): ')
#infoBox.show()
#
#if gui.OK:
#    pData = infoBox.data
#    participant = str(pData[0])
#    age = str(pData[1])
#    sex = str(pData[2])
#    condition = str(pData[3])
#elif gui.CANCEL:
#    core.quit()

#For testing
participant = "test"
age = "12"
sex = "m"
condition = "1"

# Get directory for future data collection usage
path = os.getcwd()

# Set up data file
startTime = time.localtime()
datafile = file(path+"//data//" + participant +"_plinkoBored_cupData"+str(startTime.tm_mon)+str(startTime.tm_mday)+ "_" + str(startTime.tm_hour) + str(startTime.tm_min) + str(startTime.tm_sec)+".csv", "wb")

# Data file header
cupHeader = ["Participant", "Age", "Sex", "Condition", "Block", "Trial", "Distribution Number", "Ball Position", "CompMean", "OptimalPos", "CupMean","CupLeft","CupRight", "BallCaught", "TotalScore", "CupRT"]
datafile.write(",".join(cupHeader)+"\n")

########################
# Quick set parameters #
########################

# Ball speed - up here to modify more easily
moveTime =  [0.015]

# Distributions to be estimated - range goes from 0 to 39 (Slot 1 to Slot 40)
highUncert = [28, 29, 27, 31, 27, 26, 33, 29, 26, 31, 33, 34, 30, 33, 8, 5, 6, 4, 8, 3, 3, 7, 1, 6, 8, 11, 20, 20, 19, 19, 20, 18, 18, 21, 22, 20, 20, 20, 19, 21, 8, 12, 8, 11, 8, 10, 9, 11, 6, 11, 17, 18, 15, 18, 14, 16, 17, 18, 15, 17, 31, 32, 34, 30, 29, 37, 33, 33, 34, 34, 16, 16, 21, 16, 18, 17, 20, 18, 17, 20, 30, 29, 31, 31, 30, 32, 35, 32, 34, 35, 28, 12, 11, 14, 14, 9, 11, 12, 11, 12, 13, 13, 12, 28, 32, 29, 28, 29, 25, 22, 27, 30, 25, 25, 26, 16, 18, 19, 19, 21, 33, 33, 33, 32, 32, 33, 31, 33, 35, 35, 3, 4, 10, 5, 4, 8, 2, 5, 1, 6, 12, 27, 30, 23, 27, 27, 23, 28, 26, 26, 25, 10, 15, 14, 15, 16, 14, 16, 16, 18, 14, 17, 31, 30, 30, 34, 33, 32, 32, 30, 30, 30, 31, 5, 2, 6, 4, 4, 4, 6, 4, 4, 7, 34, 34, 32, 35, 33, 31, 36, 30, 33, 37, 10, 12, 8, 7, 9, 7, 9]

huCompMean = [30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 20, 20, 20, 20, 20, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 14, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 31, 31, 31, 31, 31, 31, 31, 31, 31, 31, 31, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 9, 9, 9, 9, 9, 9, 9] #Mean of the current gaussian generating the ball drops

huOpCupPos = [27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 31, 31, 31, 31, 31, 31, 31, 31, 31, 31, 31, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 19, 19, 19, 19, 19, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 12, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 31, 31, 31, 31, 31, 31, 31, 31, 31, 31, 31, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 8, 8, 8, 8, 8, 8, 8] #Optimal cup mean given generated ball drops

huDN = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 11, 11, 11, 11, 11, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 14, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 20, 20, 20, 20, 20, 20, 20] #Which switch people are on in each block

lowUncert = [17, 17, 17, 16, 15, 17, 16, 19, 17, 18, 15, 16, 17, 16, 11, 16, 17, 15, 17, 14, 19, 20, 19, 17, 18, 19, 14, 21, 16, 22, 18, 13, 18, 18, 16, 15, 18, 16, 19, 16, 17, 17, 14, 21, 19, 20, 22, 17, 19, 14, 17, 18, 15, 18, 14, 16, 17, 18, 15, 17, 31, 32, 34, 30, 29, 37, 33, 33, 34, 34, 32, 36, 35, 34, 36, 33, 34, 32, 34, 33, 36, 33, 33, 34, 33, 30, 29, 34, 31, 36, 33, 34, 32, 34, 30, 35, 35, 32, 35, 33, 33, 35, 36, 32, 37, 32, 32, 30, 33, 35, 36, 37, 33, 35, 32, 32, 33, 32, 35, 36, 33, 33, 33, 32, 32, 33, 31, 33, 35, 35, 3, 4, 10, 5, 4, 8, 2, 5, 1, 6, 6, 4, 8, 7, 6, 5, 6, 7, 8, 6, 6, 6, 7, 7, 5, 4, 4, 4, 5, 3, 2, 3, 5, 4, 1, 8, 6, 2, 8, 4, 1, 4, 6, 5, 2, 6, 4, 4, 4, 6, 4, 4, 7, 34, 34, 32, 35, 33, 31, 36, 30, 33, 37, 34, 32, 34, 32, 38, 29, 34]

luCompMean = [17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33]

luOpCupPos = [17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33]

luDN = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]

# Order of distributions depending on condition (1 or 2 specified in GUI)
blockOrder = None
blockType = None
dNOrder = None
if condition == "1":
    blockOrder = [highUncert,lowUncert]
    dNOrder = [huDN,luDN]
    compMOrder = [huCompMean, luCompMean]
    opPosOrder = [huOpCupPos, luOpCupPos]
    blockType = ["HU","LU"]
elif condition == "2":
    blockOrder = [lowUncert, highUncert]
    dNOrder = [luDN,huDN]
    compMOrder = [luCompMean, huCompMean]
    opPosOrder = [luOpCupPos, huOpCupPos]
    blockType = ["LU","HU"]

############################
# Plinko environment setup #
############################

# Get screen dimensions
root = tk.Tk()
screenX = root.winfo_screenwidth()
screenY = root.winfo_screenheight()
screenSize = (screenX,screenY)

# Build default plinko table size according to window size
tableWidth = screenX*0.7
tableHeight = screenY*0.5

# Initialize window and mouse
win = visual.Window(size = screenSize, color = "grey", units = "pix", fullscr = True, screen = 0)
mouse = event.Mouse(win=win)

# Wrapper to help reset mouse position
carbon = pyglet.lib.load_library(framework='/System/Library/Frameworks/Carbon.framework')
def set_mouse_position(win,x,y):
    point = pyglet.window.carbon.CGPoint()
    point.x = ( ((x+1) / 2.0) * win.size[0] ) + win.pos[0]
    point.y = ( ((y-1) / -2.0) * win.size[1] ) + win.pos[1]
    carbon.CGWarpMouseCursorPosition(point)
    win.winHandle._mouse_x = point.x-win.pos[0]
    win.winHandle._mouse_y = point.y-win.pos[1]

#Plinko Table specifications
pegRowNum = 29
pegSep = tableWidth/pegRowNum
rowSep = tableHeight/pegRowNum
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

# List to keep track of slot positions for drawing
for slot in range(slotNum):
    slotPos.append((slotX,slotY))
    slotX += slotWidth

# This draws the slots
for pos in slotPos:
    slotSpread.append((pos[0]-spread,pos[0]+spread))
    #Draw slots to be buffered
    slotSquare = visual.Rect(win, width = slotWidth, height=slotHeight, pos = pos, lineColor = "white", lineWidth = 2, fillColor="grey")
    slotSquare.draw()

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

#Draw empty rectangle for point accumulation
prY = -(screenY*.25)
prH = screenY*.02
pRect = visual.Rect(win, width = tableWidth*.8, height = prH, pos = (0,prY),fillColor = "grey")
pRect.draw()

#Buffer plinko table and bet slots (quicker to load on each ball movement than generating pegs every time)
plinkoTable = visual.BufferImageStim(win) 
cupBuffer = None

# Cup specifications
cupWidth = slotWidth * 3
cupHeight = slotWidth * 1.5
cupY = slotY-(slotHeight/2)-(cupHeight/2)-(slotHeight*.25)
slotStart = 20 #Default starting slot

# Button specifications. Draws the button position and the text - used to move to the next trial
bH = .06
bHm = bH/2
bP = .35
buttonX = (-screenX*bHm,screenX*bHm)
buttonY = (-(screenY*bP)-(screenY*bHm),-(screenY*bP)+(screenY*bHm))
button = visual.Rect(win, height = screenY*bH, width = screenX*bH, pos = (0,-(screenY*bP)),fillColor = "blue")
buttonText = visual.TextStim(win,text = "Next", height = (screenY*bHm), pos = (0,-(screenY*bP)))

##################
# Point tracking #
##################

# Draws a bar that increases as participants get points
totalPoints = 0
maxScore = len(lowUncert)
barLength = float(totalPoints)/maxScore
pbW = tableWidth*.8*barLength
pbX = -(tableWidth*.8/2)+(pbW/2)
pBar = visual.Rect(win,width = pbW, height = prH, pos = (pbX,prY),fillColor = "red")
pText = visual.TextStim(win,text= "Poor",height = prH*1.5,pos = (0,(prY+(prH*2))),color="red")

# Function to refresh the bar relative to the number of points acheived (changes colour and text)
def drawPbar(tP,mS):
    global pBar
    global pText
    barLength = float(tP)/mS
    if barLength > 1:
        barLength = 1
    pbW = tableWidth*.8*barLength
    pbX = -(tableWidth*.8/2)+(pbW/2)
    bCol = "red"
    bText = str(tP)
    if barLength > .20 and barLength <= .4:
        bCol = "orange"
    elif barLength > .4 and barLength <= .6:
        bCol = "yellow"
    elif barLength > .6 and barLength <= .8:
        bCol = "lightblue"
    elif barLength > .75:
        bCol = "lightgreen"
    pBar.setPos((pbX,prY))
    pBar.setWidth(pbW)
    pBar.setFillColor(bCol)
    pText.setText(bText) 
    pText.setColor(bCol)
    pBar.draw()
    pText.draw()

##########################################
# Functions to get participant responses #
##########################################

#Returns slot in which the mouse is positioned
def getSlot(mouseX, mouseY, slotSpread):
    slotNum = None
    for spread in slotSpread:
        if mouseX > spread[0] and mouseX < spread[1]:
            slotNum = slotSpread.index(spread)
            break
        else:
            pass
    return slotNum

#Function to draw cup - just specify the X coordinate
def drawCup(posX, col = "lightblue"):
    if posX >= slotPos[38][0]:
        posX = slotPos[38][0]
    elif posX <= slotPos[1][0]:
        posX = slotPos[1][0]
    cupX = posX
    cup = visual.Rect(win, width= cupWidth, height = cupHeight, pos= (cupX,cupY),fillColor = col, lineWidth = 2)
    topRect = visual.Rect(win,width = cupWidth+(cupWidth*.5), height = (cupHeight * .1), pos = (cupX, cupY+((cupHeight/2))),lineColor = "grey",fillColor = "grey")
    cup.draw()
    topRect.draw()

# Function that waits while participants are setting their cup - takes one argument to specify where the cup was placed at the end of the last trial - exits when "Next" button is pressed
def setCup(pp):
    global button
    global cupBuffer
    sN = pp
    rtClock = core.Clock()
    while True:
        key = event.getKeys(keyList = ['q','escape'])
        if len(key) > 0:
            core.quit()
        mX, mY = mouse.getPos()
        if mX > buttonX[0] and mX < buttonX[1] and mY > buttonY[0] and mY < buttonY[1]: #Checks to see if "Next" button was pressed
            set_mouse_position(win,0,0)
            break
        if mY < (slotY-(slotHeight/2)) and mY > -(screenY*.2):
            sN1 = getSlot(mX,mY,slotSpread)
            if sN1 !=None:
                sN = sN1
            if sN == 0:
                sN = 1
            elif sN == 40:
                sN = 39
        plinkoTable.draw()
        button.draw()
        buttonText.draw()
        ball.draw()
        drawCup(slotPos[sN][0])
        drawPbar(totalPoints,maxScore)
        win.flip()
    rt = rtClock.getTime()
    plinkoTable.draw()
    drawCup(slotPos[sN][0])
    drawPbar(totalPoints,maxScore)
    cupBuffer = visual.BufferImageStim(win)
    return sN,rt

#Check if ball fell in cup and display outcome
def rewardDisp(sn,bS):
    global totalPoints
    global cup
    sn1 = sn[0]
    cupSpread = [sn1-1,sn1,sn1+1]
    cupCol = None
    score = 0
    if bS in cupSpread:
        totalPoints += 1
        score = 1
        cupCol = "lightgreen"
    else:
        cupCol = "red"
    plinkoTable.draw()
    ball.draw()
    drawCup(slotPos[sn1][0],col = cupCol)
    drawPbar(totalPoints,maxScore)
    win.flip()
    core.wait(.25)
    return score
    
#########################
# Generating ball paths #
#########################

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

# Responsible for animating the ball going through the plinko table
def ballTrack(ballPath, endPos, cupPos):
    win.clearBuffer()
    clock = core.Clock()
    for pos in ballPath:
        cupBuffer.draw()
        ball.setPos(pos)
        ball.draw()
        win.flip()
        core.wait(random.choice(moveTime))
    ball.setPos(endPos)
    cupBuffer.draw()
    ball.draw()
    win.flip()

###############
# Record data #
###############

# Function to write data to a csv
def recordData(blk, trial,dn,bp,compM,oP,cM,scr,totscr,rt):
    cl,cr = cM-1,cM+1
    trialData = map(str,[participant,age,sex,condition,blk,trial,dn,bp,compM,oP,cM,cl,cr,scr,totscr,rt])
    datafile.write(",".join(trialData) + "\n")
    datafile.flush()

#################
# Trial handler #
#################

bN = 0 #block number to help with indexing
for x in blockOrder:
    trialNum = 1 #keeps track of the trials for each certainty condition
    for i in x:
        ind = trialNum - 1 #index for other lists were pulling from
        cupSlot = setCup(slotStart)
        endPosition = slotPos[i]
        bPa = ballPath(endPosition)
        ballTrack(bPa,endPosition,cupSlot)
        score = rewardDisp(cupSlot,i)
        recordData(blockType[bN],trialNum, dNOrder[bN][ind],i+1,compMOrder[bN][ind],opPosOrder[bN][ind],cupSlot[0],score,totalPoints, cupSlot[1])
        slotStart = cupSlot[0]
        trialNum += 1
    totalPoints = 0
    bN += 1
core.quit()


