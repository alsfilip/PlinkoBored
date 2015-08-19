import pygame, sys, os
import math
import numpy
from pygame.locals import *


#Setting Up Environment
initial = 5#int(raw_input("Boredom Score 1-10: ")) # this is where we feed in the initial score value 


width,height = 800,600
pygame.init()
screen_info = pygame.display.Info()
width = screen_info.current_w
height = screen_info.current_h
windowSurfaceObj = pygame.display.set_mode((width,height))
pygame.display.set_caption("Radial Scale")

timefont = pygame.font.SysFont("Arial", 30)

InstructionBored = "The area of the orange circle represents the extent to which you were bored at the beginning of the experiment. Click and drag the circle to indicate your new level of boredom by either contracting or expanding the circle."
instlist = [InstructionBored]

Done = timefont.render("Done", 1, (255,255,255))

drag = False
size = 0

initsize = 30 #Initial Radius
maxsize = 200 #Maximum Radius


def drawText(surface, text, color, rect, font, aa=False, bkg=None): # This function is used to create warped text
    rect = Rect(rect)
    y = rect.top
    lineSpacing = -2
 
    # get the height of the font
    fontHeight = font.size("Tg")[1]
 
    while text:
        i = 1
 
        # determine if the row of text will be outside our area
        if y + fontHeight > rect.bottom:
            break
 
        # determine maximum width of line
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1
 
        # if we've wrapped the text, then adjust the wrap to the last word      
        if i < len(text): 
            i = text.rfind(" ", 0, i) + 1
 
        # render the line and blit it to the surface
        if bkg:
            image = font.render(text[:i], 1, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(text[:i], aa, color)
 
        surface.blit(image, (rect.left, y))
        y += fontHeight + lineSpacing
 
        # remove the text we just blitted
        text = text[i:]
 
    return text

def getarea(r):
    area = r*r*math.pi
    return area

while True:
    windowSurfaceObj.fill((255,255,255))
    drawText(windowSurfaceObj,InstructionBored,(0,0,0),(width/10,height/20,width-width*2/10,height-height*2/10),font=timefont,aa=False,bkg=None)
    circcolor = (220,70,50)
    circsurf = pygame.Surface((width,height))
    circsurf.fill(circcolor)
    circsurf.set_colorkey(circcolor)

    if size < initsize:
        pygame.draw.circle(circsurf, (255,100,0,255),(width/2,height/2), initsize)
        pygame.draw.circle(circsurf, (220,50,50,255),(width/2,height/2), size)
    if size >= initsize:
        pygame.draw.circle(circsurf, (220,50,50,255),(width/2,height/2), size)
        pygame.draw.circle(circsurf, (255,100,0,255),(width/2,height/2), initsize)

    circsurf.set_alpha(150)
    windowSurfaceObj.blit(circsurf,(0,0))
    
    pygame.draw.rect(windowSurfaceObj,[0,0,0],(width/2-75,(height-height/5)+50,150,50),0) #Draw Done Button
    windowSurfaceObj.blit(Done, (width/2-40,(height-height/5)+55))
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN: # If keypress

            if event.key == K_ESCAPE: # is escape
                pygame.event.post(pygame.event.Event(QUIT)) # quit game.
               
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                drag = True
 
                smousex, smousey = event.pos
                
        elif event.type == MOUSEMOTION:
            mousex, mousey = event.pos
            
            if drag == True:
                hypvalue = math.sqrt(math.pow((width/2-mousex),2) + math.pow((height/2-mousey),2))
                size = int(hypvalue/2)
                if size > maxsize:
                    size = maxsize

        elif event.type == MOUSEBUTTONUP:
            drag = False

            mousex, mousey = event.pos
            if (width/2-75)< mousex < (width/2+75) and ((height-height/5)+50) < mousey < ((height-height/5)+100): #Is click in 'Done' button box

                newarea = getarea(size)
                initarea = getarea(initsize)
                score = initial*abs((initarea-newarea)/initarea-1) #Calculate score
                print "Score: " + str(score)
                pygame.quit()
                sys.exit()
    
    pygame.display.flip() # Refresh Display
