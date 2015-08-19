from psychopy import visual,event,core


scrnX = 1280
scrnY = 1024
#Background window
win = visual.Window(size=[scrnX,scrnY],allowGUI=False,fullscr=0, color="grey",units='pix')
mouse = event.Mouse()



distanceX = scrnX/3.2 #meant to be 400 pixels on a 1280x1024 screen but gets adjusted with the screen dimensions
distanceY = scrnY/5.12 #meant to be 200 pixels on 1280x1024 screen
itemSize = scrnX/5 #meant to be 256x256 pixels (original resolution) for each item picture on a 1280x1024 screen
textSize = scrnX/32 # meant to be a height of 40 on a screen that is 1280x1024

#Done Button
button=visual.Rect(win, fillColor='black', width=itemSize, height = itemSize/4,pos=(0,-distanceY*1.40))
buttontext = visual.TextStim(win,text = "Done",height=textSize,wrapWidth = (scrnX*0.8),pos=(0,-distanceY*1.40))

#Probe Instructions
probetext = visual.TextStim(win,text = "Rate each of the following as it relates to you right now.",height=textSize*0.75,wrapWidth = (scrnX*0.8),pos=(0,distanceY+distanceY/2))

#Keeping Track of Robes
probenum = 1

probepos = [distanceY,distanceY/2,-distanceY,-distanceY/2,0]

        
Scale1 = visual.RatingScale(win, scale="How bored are you?", marker = 'triangle', tickMarks = (0,100),
                                singleClick=False,precision= 1,textSize = 1.5, disappear = True,
                                low = 0, high = 100, showValue = False, 
                                showAccept = False, mouseOnly = True, stretch = 3, size = 0.5,
                                labels = ("not at all","very much"), pos = (0,probepos[0]))
                                
Scale2 = visual.RatingScale(win, scale="How frustrated are you?", marker = 'triangle', tickMarks = (0,100),
                                singleClick=False,precision= 1, textSize = 1.5,
                                low = 0, high = 100, showValue = False,
                                showAccept = False, mouseOnly = True,  stretch = 3, size = 0.5, 
                                labels = ("not at all","very much"), pos = (0,probepos[1]))

Scale3 = visual.RatingScale(win, scale="To what extent do you feel in control in the task?", marker = 'triangle', tickMarks = (0,100),
                                singleClick=False,precision= 1, textSize = 1.5,
                                low = 0, high = 100, showValue = False,
                                showAccept = False, mouseOnly = True,  stretch = 3, size = 0.5,
                                labels = ("not at all","very much"), pos = (0,probepos[2]))
                                
Scale4 = visual.RatingScale(win, scale="How much do you care about winning?", marker = 'triangle', tickMarks = (0,100),
                                singleClick=False,precision= 1, textSize = 1.5,
                                low = 0, high = 100, showValue = False,
                                showAccept = False, mouseOnly = True, stretch = 3, size = 0.5,
                                labels = ("not at all","very much"), pos = (0,probepos[3]))
                                
Scale5 = visual.RatingScale(win, scale="How challenging is this task?", marker = 'triangle', tickMarks = (0,100),
                                singleClick=False,precision= 1, textSize = 1.5,
                                low = 0, high = 100, showValue = False,
                                showAccept = False, mouseOnly = True,  stretch = 3, size = 0.5,
                                labels = ("not at all","very much"), pos = (0,probepos[4]))


while True:
    button.draw()
    buttontext.draw()  
    probetext.draw()             
    Scale1.draw()
    Scale2.draw()
    Scale3.draw()
    Scale4.draw()
    Scale5.draw()
    win.flip()
    keyPress = event.getKeys()

    if "q" in keyPress:
        quit()

    if mouse.isPressedIn(button) and Scale1.getRating() != None and Scale2.getRating() != None and Scale3.getRating() != None and Scale4.getRating() != None and Scale5.getRating() != None : break

SetScore1 = Scale1.getRating()
SetScore2 = Scale2.getRating()
SetScore3 = Scale3.getRating()
SetScore4 = Scale4.getRating()
SetScore5 = Scale5.getRating()

torecord = str(probenum) + "," + str(SetScore1) + "," + str(Scale1.getRT()) + "," + str(SetScore2)+ ","+ str(Scale2.getRT()) + "," + str(SetScore3) + "," + str(Scale3.getRT()) + "," + str(SetScore4) + "," + str(Scale4.getRT()) + "," + str(SetScore5) + "," + str(Scale5.getRT())

recordData(torecord)
probenum += 1
 
win.flip()
    