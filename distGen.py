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
	print bCList
	return bCList.index(max(bCList))


# Takes 2 arguments: r -range (the trial range that a distribution is meant to change); numT - number of trials needing to be generated
def genDist(r,numT,sd):
	slotRange = range(40) #Number of slots that could serve as a mean
	dist = [] #Place holder list that will contain ball drops
	mList = []
	dNumList = []
	opPosList = []
	dNum = 0 #The distributions number in the list (e.g., the first, second, etc)
	borders = [sd*2,39-(sd*2)]
	lastMean = None
	while len(dist) < numT: #Keep generating until the desired number of trials has been generated
		currDist = []
		dNum += 1
		interval = random.choice(r) #Chooses a random interval
		mean = None
		while True:
			mean = random.choice(slotRange)
			print mean, lastMean
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
	return [dist,mList,dNumList,opPosList]

##########################################
# Generate Low Uncertainty distributions #
##########################################

trialNum = 100
trialNumRange = range(30,50)
luDist = genDist(trialNumRange,trialNum,2)
print luDist[0]
print luDist[1]
print luDist[2]
print luDist[3]
print len(luDist[0]),len(luDist[1]),len(luDist[2]),len(luDist[3])

###########################################
# Generate High Uncertainty distributions #
###########################################