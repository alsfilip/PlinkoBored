'''
August 19th, 2015

This is a program to generate distributions for the PlinkoBored experiment. The distributions generated here will be added to the plinkoBored.py program and used during the experiment.

'''

import random
import numpy as np

random.seed(256) # Makes it so that the same distribution will be generated each time you run this code

######################################
# Function to generate distributions #
######################################

#This function gets the optimal cup position for each distribution - used in the function that follows
def opPos(bD):
	bCList = []
	cupPos = np.array([0,1,2])
	for i in range(38):
		l = []
		for x in cupPos:
			l.append(bD.count(x))
		bCList.append(sum(l))
		cupPos = cupPos + 1
	return bCList.index(max(bCList))


# Takes 2 arguments: r -range (the trial range that a distribution is meant to change); numT - number of trials needing to be generated
def genDist(r,numT,sd):
	slotRange = range(40) #Number of slots that could serve as a mean
	dist = [] #Place holder list that will contain ball drops
	mList = []
	dNumList = []
	opPosList = []
	intList = []
	dNum = 0 #The distributions number in the list (e.g., the first, second, etc)
	borders = [sd*2,39-(sd*2)]
	lastMean = None
	while len(dist) < numT: #Keep generating until the desired number of trials has been generated
		currDist = []
		dNum += 1
		interval = random.choice(r) #Chooses a random interval
		intList.append(interval)
		mean = None
		while True:
			mean = random.choice(slotRange)
			#Designates the slots that are outside a 2 sd range of the previous mean
			buffZone = None
			if lastMean != None:
				msd = lastMean - (2*sd)
				psd = lastMean + (2*sd)
				if msd < 0:
					msd = 0
				if psd > 39:
					psd = 39
				bufferZone = range(0,msd)+range(psd,40)
			if lastMean == None:
				if mean in range(borders[0],borders[1]+1):
					break		
			elif mean in bufferZone:
				if mean in range(borders[0],borders[1]+1):
					break
		lastMean = mean
		for i in range(interval):
			if len(dist) >= numT:
				break
			drop = None
			while True:
				drop = int(np.round(random.gauss(mean,sd)))
				if drop in slotRange:
					break
			currDist.append(drop)
			dist.append(drop)
			mList.append(mean)
			dNumList.append(dNum)
		opPosList += [opPos(currDist)+1]*len(currDist)
	return [dist,mList,dNumList,opPosList], intList

##########################################
# Generate Low Uncertainty distributions #
##########################################

trialNum = 200
lutR = (50,70)
sd = 2
trialNumRange = range(lutR[0],lutR[1]+1)
luDist = genDist(trialNumRange,trialNum,sd)
# print luDist[0][0] #Ball drops generated
# print luDist[0][1] #Means of the generative distributions
# print luDist[0][2] #Distribution number
# print luDist[0][3] #Optimal cup mean
# print luDist[1]    #The intervals between each distributions

###########################################
# Generate High Uncertainty distributions #
###########################################

# First step - figure our what parts of the distributions you're going to keep the same
# For now lets work with keeping the 10 trials that precede a switch, and the 10 trials that follow a switch

tBs = 10 #Trials before a switch to be kept from the low uncertainty condition
tAs = 10 #Trials after a switch to be kept from the low uncertainty condition

# The easiest will probably be to generate a whole new set of distributions and replace some of the generated ones with ones that you want
hutR = (10,15)
huTNR = range(hutR[0],hutR[1]+1)
huDist = genDist(huTNR,trialNum,sd)

# Now we extract the portions of the low uncertainty distribution that we want to insert into the high uncertainty distribution
luBD = luDist[0][0]
huBD = huDist[0][0]

# Same thing but for the means
luMean = luDist[0][1]
huMean = huDist[0][1]

# Same for the optimal cup size
luOp = luDist[0][3]
huOp = huDist[0][3]

# Adjust the high uncertainty values
sPoints = []
lp = 0
for i in luDist[1]:
	sPoints.append(i+lp)
	lp += i
sRan = [[(sPoints[0]-tBs),(sPoints[0]+tAs)],[(sPoints[1]-tBs),(sPoints[1]+tAs)],[(sPoints[2]-tBs),(sPoints[2]+tAs)]]

Insert1_BD = luBD[sRan[0][0]:sRan[0][1]]
Insert2_BD = luBD[sRan[1][0]:sRan[1][1]]
Insert3_BD = luBD[sRan[2][0]:sRan[2][1]]

Insert1_Mean = luMean[sRan[0][0]:sRan[0][1]]
Insert2_Mean = luMean[sRan[1][0]:sRan[1][1]]
Insert3_Mean = luMean[sRan[2][0]:sRan[2][1]]

Insert1_Op = luOp[sRan[0][0]:sRan[0][1]]
Insert2_Op = luOp[sRan[1][0]:sRan[1][1]]
Insert3_Op = luOp[sRan[2][0]:sRan[2][1]]

# Insert switches, mean and optimal cup size info
huBD[sRan[0][0]:sRan[0][1]] = Insert1_BD
huBD[sRan[1][0]:sRan[1][1]] = Insert2_BD
huBD[sRan[2][0]:sRan[2][1]] = Insert3_BD

huMean[sRan[0][0]:sRan[0][1]] = Insert1_Mean
huMean[sRan[1][0]:sRan[1][1]] = Insert2_Mean
huMean[sRan[2][0]:sRan[2][1]] = Insert3_Mean

huOp[sRan[0][0]:sRan[0][1]] = Insert1_Op
huOp[sRan[1][0]:sRan[1][1]] = Insert2_Op
huOp[sRan[2][0]:sRan[2][1]] = Insert3_Op

# Make a distribution number list for high uncertainty that matches the actual switches
luDistNum = luDist[0][2]
huDistNum = []
lastIt = None
dn = 0
for i in huMean:
	if i != lastIt:
		lastIt = i
		dn +=1
	huDistNum.append(dn)

# Output ball drops
print "Ball Distributions"
print luBD
print huBD

# Output Means
print "Distribution Means"
print luMean
print huMean

# Output Optimal Cup Size
print "Optimal Cup Size"
print luOp
print huOp

# Print distribution numbers
print "Distribution Numbers"
print luDistNum
print huDistNum
