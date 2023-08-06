#!/usr/bin/env python3
import pygame
import sys
from pygame.locals import *
import pygame.scrap as scrap

from pygameElements import Label, InputBox, Square, Ellipse, Image, Line, CheckBox, Button

class testPygameElements():
    def __init__(self, screenWidth=900, screenHeight=600, caption='PygameElement Elements Example', isFullscreen=False, desiredFrameRate=50.0):
        #settings:
        self.renderObjects=[]
        self.isFullscreen=isFullscreen
        self.screenWidth=screenWidth
        self.screenHeight=screenHeight
        self.caption=caption
        self.desiredFrameRate=desiredFrameRate
        self.event=(0,0)
        self.desiredIntervalInMilliseconds=int(round(1000.0/desiredFrameRate))
        if self.desiredIntervalInMilliseconds<1:
            self.desiredIntervalInMilliseconds=1
        
        self.screenColorBackground=pygame.Color('yellow') 
        # set up pygame
        pygame.init()
        
        # get display information from user machine
        pgdi=pygame.display.Info()

        
        # store desktop size
        self.desktopSize=(pgdi.current_w, pgdi.current_h)
        
        # create window
        self.setDisplay()
        
        # initialize scrap module to be able to use clipboard
        scrap.init()
        scrap.set_mode(SCRAP_CLIPBOARD)
            
        # create some test elements
        
        self.renderObjects.append(Label(self.windowSurface, 'screen1', 'lblName1', 'This will show the several elements', pygame.Color('black'), 500, 250))
        self.renderObjects.append(Label(self.windowSurface, 'screen1', 'lblName2', 'That can be used in Pygame', pygame.Color('black'), 500, 350))
        self.renderObjects.append(Label(self.windowSurface, 'screen1', 'lblName3', 'They will resize with screen resizes', pygame.Color('black'), 500, 450))
        self.renderObjects.append(Button(self.windowSurface, 'screen1', 'btnBack', 300,920,300,100, text='Click to go to End', fontSizePromille=50,onClick=self.handleClick))
        self.renderObjects.append(Button(self.windowSurface, 'screen1', 'btnContinue', 700,920,300,100, text='Click to Continue', fontSizePromille=50,onClick=self.handleClick))
        
        self.renderObjects.append(Label(self.windowSurface, 'screenShowLabel', 'lblName1', 'the Label element', pygame.Color('black'), 500, 50, isBold=True))
        self.renderObjects.append(Label(self.windowSurface, 'screenShowLabel', 'lblName2', 'can', pygame.Color('black'), 200, 100, fontSizePromille=20))
        self.renderObjects.append(Label(self.windowSurface, 'screenShowLabel', 'lblName3', 'have', pygame.Color('black'), 200, 120, fontSizePromille=40))
        self.renderObjects.append(Label(self.windowSurface, 'screenShowLabel', 'lblName4', 'any', pygame.Color('black'), 200, 150, fontSizePromille=80))
        self.renderObjects.append(Label(self.windowSurface, 'screenShowLabel', 'lblName5', 'size', pygame.Color('black'), 200, 235, fontSizePromille=160))
        self.renderObjects.append(Label(self.windowSurface, 'screenShowLabel', 'lblName6', 'or', pygame.Color('red'), 500, 120))
        self.renderObjects.append(Label(self.windowSurface, 'screenShowLabel', 'lblName7', 'color', pygame.Color('green'), 500, 200))
        self.renderObjects.append(Label(self.windowSurface, 'screenShowLabel', 'lblName8', 'or', pygame.Color('red'), 800, 120, alphaValue=120))
        self.renderObjects.append(Label(self.windowSurface, 'screenShowLabel', 'lblName9', 'alphaValue', pygame.Color('green'), 800, 200, alphaValue=40))
        self.renderObjects.append(Label(self.windowSurface, 'screenShowLabel', 'lblName10', 'can use any system font', pygame.Color('black'), 500, 340, fontSizePromille=60))
        self.renderObjects.append(Label(self.windowSurface, 'screenShowLabel', 'lblName11', 'like arial', pygame.Color('black'), 500, 420, fontName='arial', fontSizePromille=80))
        self.renderObjects.append(Label(self.windowSurface, 'screenShowLabel', 'lblName12', 'or couriernew', pygame.Color('black'), 500, 500, fontName='couriernew', fontSizePromille=80))
        self.renderObjects.append(Label(self.windowSurface, 'screenShowLabel', 'lblName13', 'most system fonts also have', pygame.Color('black'), 500, 580, fontSizePromille=60))
        self.renderObjects.append(Label(self.windowSurface, 'screenShowLabel', 'lblName14', 'bold text', pygame.Color('black'), 500, 660, isBold=True, fontSizePromille=80))
        self.renderObjects.append(Label(self.windowSurface, 'screenShowLabel', 'lblName15', 'italic text', pygame.Color('black'), 500, 740, isItalic=True, fontSizePromille=80))
        self.renderObjects.append(Label(self.windowSurface, 'screenShowLabel', 'lblName16', 'bold and italic text', pygame.Color('black'), 500, 820, isBold=True, isItalic=True, fontSizePromille=80))
        self.renderObjects.append(Button(self.windowSurface, 'screenShowLabel', 'btnBack', 300,920,300,100, text='Click to go Back', fontSizePromille=50,onClick=self.handleClick))
        self.renderObjects.append(Button(self.windowSurface, 'screenShowLabel', 'btnContinue', 700,920,300,100, text='Click to Continue', fontSizePromille=50,onClick=self.handleClick))
        
        self.renderObjects.append(Label(self.windowSurface, 'screenShowLabel2', 'lblName1', 'the Label element', pygame.Color('black'), 500, 50, isBold=True))
        self.renderObjects.append(Label(self.windowSurface, 'screenShowLabel2', 'lblName2', 'can use fonts from file', pygame.Color('black'), 500, 140, fontSizePromille=60))
        self.renderObjects.append(Label(self.windowSurface, 'screenShowLabel2', 'lblName3', 'if they are .ttf or .otf', pygame.Color('black'), 500, 220, fontSizePromille=60))
        self.renderObjects.append(Label(self.windowSurface, 'screenShowLabel2', 'lblName4', 'like Ballpointprint.ttf', pygame.Color('black'), 500, 300, sysFont=False, fontName='Ballpointprint.ttf', fontSizePromille=80))
        self.renderObjects.append(Label(self.windowSurface, 'screenShowLabel2', 'lblName5', 'but they dont have a bold nor italic', pygame.Color('black'), 500, 380, sysFont=False,fontName='Ballpointprint.ttf', fontSizePromille=60))
        self.renderObjects.append(Button(self.windowSurface, 'screenShowLabel2', 'btnBack', 300,920,300,100, text='Click to go Back', fontSizePromille=50,onClick=self.handleClick))
        self.renderObjects.append(Button(self.windowSurface, 'screenShowLabel2', 'btnContinue', 700,920,300,100, text='Click to Continue', fontSizePromille=50,onClick=self.handleClick))
        
        self.renderObjects.append(Label(self.windowSurface, 'screenShowLine', 'lblName1', 'the Line element', pygame.Color('black'), 500, 50, isBold=True))
        self.renderObjects.append(Label(self.windowSurface, 'screenShowLine', 'lblName2', 'has a start and end position', pygame.Color('black'), 500, 140, fontSizePromille=60))
        self.renderObjects.append(Line(self.windowSurface, 'screenShowLine', 'line1', pygame.Color('black'), (200, 185), (800,185)))
        self.renderObjects.append(Label(self.windowSurface, 'screenShowLine', 'lblName2', 'any color', pygame.Color('black'), 500, 220, fontSizePromille=60))
        self.renderObjects.append(Line(self.windowSurface, 'screenShowLine', 'line2', pygame.Color('blue'), (200, 265), (800,265)))
        self.renderObjects.append(Line(self.windowSurface, 'screenShowLine', 'line3', pygame.Color('green'), (200, 280), (800,280)))
        self.renderObjects.append(Line(self.windowSurface, 'screenShowLine', 'line4', pygame.Color('red'), (200, 295), (800,295)))
        self.renderObjects.append(Label(self.windowSurface, 'screenShowLine', 'lblName2', 'any width', pygame.Color('black'), 500, 340, fontSizePromille=60))
        self.renderObjects.append(Line(self.windowSurface, 'screenShowLine', 'line5', pygame.Color('black'), (200, 375), (200,410),widthLine=1))
        self.renderObjects.append(Line(self.windowSurface, 'screenShowLine', 'line6', pygame.Color('black'), (300, 375), (300,410),widthLine=2))
        self.renderObjects.append(Line(self.windowSurface, 'screenShowLine', 'line7', pygame.Color('black'), (400, 375), (400,410),widthLine=4))
        self.renderObjects.append(Line(self.windowSurface, 'screenShowLine', 'line8', pygame.Color('black'), (500, 375), (500,410),widthLine=8))
        self.renderObjects.append(Line(self.windowSurface, 'screenShowLine', 'line9', pygame.Color('black'), (600, 375), (600,410),widthLine=16))
        self.renderObjects.append(Line(self.windowSurface, 'screenShowLine', 'line10', pygame.Color('black'), (700, 375), (700,410),widthLine=32))
        self.renderObjects.append(Label(self.windowSurface, 'screenShowLine', 'lblName2', 'any alphaValue', pygame.Color('black'), 500, 450, fontSizePromille=60))
        self.renderObjects.append(Line(self.windowSurface, 'screenShowLine', 'line11', pygame.Color('black'), (200, 500), (800,500), alphaValue=255))
        self.renderObjects.append(Line(self.windowSurface, 'screenShowLine', 'line12', pygame.Color('black'), (200, 520), (800,520), alphaValue=200))
        self.renderObjects.append(Line(self.windowSurface, 'screenShowLine', 'line13', pygame.Color('black'), (200, 540), (800,540), alphaValue=150))
        self.renderObjects.append(Line(self.windowSurface, 'screenShowLine', 'line14', pygame.Color('black'), (200, 560), (800,560), alphaValue=100))
        self.renderObjects.append(Line(self.windowSurface, 'screenShowLine', 'line15', pygame.Color('black'), (200, 580), (800,580), alphaValue=50))
        self.renderObjects.append(Button(self.windowSurface, 'screenShowLine', 'btnBack', 300,920,300,100, text='Click to go Back', fontSizePromille=50,onClick=self.handleClick))
        self.renderObjects.append(Button(self.windowSurface, 'screenShowLine', 'btnContinue', 700,920,300,100, text='Click to Continue', fontSizePromille=50,onClick=self.handleClick))
        
        self.renderObjects.append(Label(self.windowSurface, 'screenShowSquare', 'lblName1', 'the Square element', pygame.Color('black'), 500, 50, isBold=True))
        self.renderObjects.append(Label(self.windowSurface, 'screenShowSquare', 'lblName2', 'Any Size or Color or AlphaValue', pygame.Color('black'), 500, 140, fontSizePromille=60))
        self.renderObjects.append(Square(self.windowSurface, 'screenShowSquare', 'sq1',pygame.Color('black'), 200, 250, 100,40))
        self.renderObjects.append(Square(self.windowSurface, 'screenShowSquare', 'sq2',pygame.Color('red'), 350, 250, 40,100))
        self.renderObjects.append(Square(self.windowSurface, 'screenShowSquare', 'sq3',pygame.Color('blue'), 600, 250, 40,40))
        self.renderObjects.append(Square(self.windowSurface, 'screenShowSquare', 'sq4',pygame.Color('white'), 800, 250, 80,50))
        self.renderObjects.append(Square(self.windowSurface, 'screenShowSquare', 'sq5',pygame.Color('black'), 200, 300, 100,40, alphaValue=200))
        self.renderObjects.append(Square(self.windowSurface, 'screenShowSquare', 'sq6',pygame.Color('black'), 450, 300, 40,100, alphaValue=150))
        self.renderObjects.append(Square(self.windowSurface, 'screenShowSquare', 'sq7',pygame.Color('black'), 600, 300, 40,40, alphaValue=100))
        self.renderObjects.append(Square(self.windowSurface, 'screenShowSquare', 'sq8',pygame.Color('black'), 800, 300, 80,50, alphaValue=50))
        self.renderObjects.append(Label(self.windowSurface, 'screenShowSquare', 'lblName3', 'WidthBorder 0 means filled in', pygame.Color('black'), 500, 380, fontSizePromille=60))
        self.renderObjects.append(Label(self.windowSurface, 'screenShowSquare', 'lblName4', 'Any other WidthBorder will leave middle open', pygame.Color('black'), 500, 450, fontSizePromille=60))
        self.renderObjects.append(Square(self.windowSurface, 'screenShowSquare', 'sq9',pygame.Color('black'), 200, 550, 100,100, widthBorder=5))
        self.renderObjects.append(Square(self.windowSurface, 'screenShowSquare', 'sq10',pygame.Color('black'), 400, 550, 100,100, widthBorder=10))
        self.renderObjects.append(Square(self.windowSurface, 'screenShowSquare', 'sq11',pygame.Color('black'), 600, 550, 100,100, widthBorder=20))
        self.renderObjects.append(Square(self.windowSurface, 'screenShowSquare', 'sq12',pygame.Color('black'), 800, 550, 100,100, widthBorder=40))
        self.renderObjects.append(Label(self.windowSurface, 'screenShowSquare', 'lblName3', 'You can also round up each corner', pygame.Color('black'), 500, 650, fontSizePromille=60))
        self.renderObjects.append(Label(self.windowSurface, 'screenShowSquare', 'lblName4', 'by a specific amount', pygame.Color('black'), 500, 700, fontSizePromille=60))
        self.renderObjects.append(Square(self.windowSurface, 'screenShowSquare', 'sq13',pygame.Color('black'), 200, 800, 100,100, widthBorder=10,borderTopLeft=20 ))
        self.renderObjects.append(Square(self.windowSurface, 'screenShowSquare', 'sq14',pygame.Color('black'), 400, 800, 100,100, widthBorder=20,borderTopLeft=60, borderTopRight=20))
        self.renderObjects.append(Square(self.windowSurface, 'screenShowSquare', 'sq15',pygame.Color('black'), 600, 800, 100,100, borderTopLeft=20, borderBottomLeft=20))
        self.renderObjects.append(Square(self.windowSurface, 'screenShowSquare', 'sq16',pygame.Color('black'), 800, 800, 100,100, borderTopLeft=60, borderBottomRight=60))
        self.renderObjects.append(Button(self.windowSurface, 'screenShowSquare', 'btnBack', 300,920,300,100, text='Click to go Back', fontSizePromille=50,onClick=self.handleClick))
        self.renderObjects.append(Button(self.windowSurface, 'screenShowSquare', 'btnContinue', 700,920,300,100, text='Click to Continue', fontSizePromille=50,onClick=self.handleClick))
      
        self.renderObjects.append(Label(self.windowSurface, 'screenShowEllipse', 'lblName1', 'the Ellipse element', pygame.Color('black'), 500, 50, isBold=True))
        self.renderObjects.append(Label(self.windowSurface, 'screenShowEllipse', 'lblName2', 'Any Size or Color or AlphaValue', pygame.Color('black'), 500, 180, fontSizePromille=60))
        self.renderObjects.append(Ellipse(self.windowSurface, 'screenShowEllipse', 'el1',pygame.Color('black'), 200,350,100,200))
        self.renderObjects.append(Ellipse(self.windowSurface, 'screenShowEllipse', 'el2',pygame.Color('blue'), 400,350,50,100))
        self.renderObjects.append(Ellipse(self.windowSurface, 'screenShowEllipse', 'el3',pygame.Color('red'), 600,350,100,120))
        self.renderObjects.append(Ellipse(self.windowSurface, 'screenShowEllipse', 'el4',pygame.Color('white'), 800,350,200,100))
        self.renderObjects.append(Ellipse(self.windowSurface, 'screenShowEllipse', 'el5',pygame.Color('blue'), 250,350,80,100, alphaValue=200))
        self.renderObjects.append(Ellipse(self.windowSurface, 'screenShowEllipse', 'el6',pygame.Color('black'), 450,350,60,70, alphaValue=150))
        self.renderObjects.append(Ellipse(self.windowSurface, 'screenShowEllipse', 'el7',pygame.Color('white'), 650,350,90,80, alphaValue=100))
        self.renderObjects.append(Ellipse(self.windowSurface, 'screenShowEllipse', 'el8',pygame.Color('red'), 850,350,70,100, alphaValue=50))
        self.renderObjects.append(Label(self.windowSurface, 'screenShowEllipse', 'lblName3', 'WidthBorder 0 means filled in', pygame.Color('black'), 500, 500, fontSizePromille=60))
        self.renderObjects.append(Label(self.windowSurface, 'screenShowEllipse', 'lblName4', 'Any other WidthBorder will leave middle open', pygame.Color('black'), 500, 560, fontSizePromille=60))
        self.renderObjects.append(Ellipse(self.windowSurface, 'screenShowEllipse', 'el9',pygame.Color('black'), 200,700,100,200, widthBorder=5))
        self.renderObjects.append(Ellipse(self.windowSurface, 'screenShowEllipse', 'el10',pygame.Color('blue'), 400,700,50,100, widthBorder=10))
        self.renderObjects.append(Ellipse(self.windowSurface, 'screenShowEllipse', 'el11',pygame.Color('red'), 600,700,100,120, widthBorder=20))
        self.renderObjects.append(Ellipse(self.windowSurface, 'screenShowEllipse', 'el12',pygame.Color('white'), 800,700,200,100, widthBorder=40))
        self.renderObjects.append(Button(self.windowSurface, 'screenShowEllipse', 'btnBack', 300,920,300,100, text='Click to go Back', fontSizePromille=50,onClick=self.handleClick))
        self.renderObjects.append(Button(self.windowSurface, 'screenShowEllipse', 'btnContinue', 700,920,300,100, text='Click to Continue', fontSizePromille=50,onClick=self.handleClick))
        
        self.renderObjects.append(Label(self.windowSurface, 'screenShowImage', 'lblName1', 'the Image element', pygame.Color('black'), 500, 50, isBold=True))
        self.renderObjects.append(Label(self.windowSurface, 'screenShowImage', 'lblName2', 'Any Size or AlphaValue', pygame.Color('black'), 500, 180, fontSizePromille=60))
        self.renderObjects.append(Image(self.windowSurface, 'screenShowImage', 'img1', 'someimage.png', 200, 250, 100,100))
        self.renderObjects.append(Image(self.windowSurface, 'screenShowImage', 'img2', 'someimage.png', 400, 250, 20,100))
        self.renderObjects.append(Image(self.windowSurface, 'screenShowImage', 'img3', 'someimage.png', 600, 250, 100,20))
        self.renderObjects.append(Image(self.windowSurface, 'screenShowImage', 'img4', 'someimage.png', 800, 250, 20,20))
        self.renderObjects.append(Image(self.windowSurface, 'screenShowImage', 'img5', 'someimage.png', 200, 350, 100,100, alphaValue=200))
        self.renderObjects.append(Image(self.windowSurface, 'screenShowImage', 'img6', 'someimage.png', 300, 350, 100,100, alphaValue=150))
        self.renderObjects.append(Image(self.windowSurface, 'screenShowImage', 'img7', 'someimage.png', 400, 350, 100,100, alphaValue=100))
        self.renderObjects.append(Image(self.windowSurface, 'screenShowImage', 'img8', 'someimage.png', 500, 350, 100,100, alphaValue=50))
        self.renderObjects.append(Image(self.windowSurface, 'screenShowImage', 'img9', 'someimage.png', 600, 350, 100,100, alphaValue=20))
        self.renderObjects.append(Image(self.windowSurface, 'screenShowImage', 'img10', 'someimage.png', 700, 350, 100,100, alphaValue=10))
        self.renderObjects.append(Image(self.windowSurface, 'screenShowImage', 'img11', 'someimage.png', 800, 350, 100,100, alphaValue=5))
        self.renderObjects.append(Label(self.windowSurface, 'screenShowImage', 'lblName3', 'You can elect to use the unstretched image', pygame.Color('black'), 500, 425, fontSizePromille=60))
        self.renderObjects.append(Image(self.windowSurface, 'screenShowImage', 'img12', 'someimage.png', 500, 570, 500,500, stretch=False))
        self.renderObjects.append(Label(self.windowSurface, 'screenShowImage', 'lblName4', 'when image is not found, it shows a placeholder', pygame.Color('black'), 500, 710, fontSizePromille=60))
        self.renderObjects.append(Image(self.windowSurface, 'screenShowImage', 'img13', 'doesnotexist.png', 500, 800, 100,100))
        self.renderObjects.append(Button(self.windowSurface, 'screenShowImage', 'btnBack', 300,920,300,100, text='Click to go Back', fontSizePromille=50,onClick=self.handleClick))
        self.renderObjects.append(Button(self.windowSurface, 'screenShowImage', 'btnContinue', 700,920,300,100, text='Click to Continue', fontSizePromille=50,onClick=self.handleClick))
#self, blitToSurface=None, gameState='', name='', horizontalMiddlePromille=500, verticalMiddlePromille=500, horizontalSizePromille=500,  
#verticalSizePromille=100, colorNormal=(190,190,190), colorHasFocus=(190,255,190),colorMouseOver=(190,190,255),colorMouseDown=(255,190,190), value=None, 
#alphaValue=255, hasFocus=False, visible=True, onClick=None, text='button', enabled=True, sysFont=True, fontName='timesnewroman', fontSizePromille=80, antiAlias=True):
        self.renderObjects.append(Label(self.windowSurface, 'screenShowButton', 'lblName1', 'the Button element', pygame.Color('black'), 500, 50, isBold=True))
        self.renderObjects.append(Button(self.windowSurface, 'screenShowButton', 'btnTest', 500, 150, 100,50, fontSizePromille=30, onClick=self.handleClick))
        self.renderObjects.append(Label(self.windowSurface, 'screenShowButton', 'lblName1', 'the Button element combines a Square and Label', pygame.Color('black'), 500, 200, isBold=True,fontSizePromille=60))
        self.renderObjects.append(Label(self.windowSurface, 'screenShowButton', 'lblName2', 'Any Size or Color or AlphaValue', pygame.Color('black'), 500, 250, fontSizePromille=60))
        self.renderObjects.append(Label(self.windowSurface, 'screenShowButton', 'lblName3', 'if it has tab focus, it is greenish and bold', pygame.Color('black'), 500, 300, isBold=True,fontSizePromille=60))
        self.renderObjects.append(Label(self.windowSurface, 'screenShowButton', 'lblName4', 'if the mouse is over it, it is blueish and italic', pygame.Color('black'), 500, 350, isBold=True,fontSizePromille=60))
        self.renderObjects.append(Label(self.windowSurface, 'screenShowButton', 'lblName5', 'if the mousebutton is down (but not up yet),', pygame.Color('black'), 500, 400, isBold=True,fontSizePromille=60))
        self.renderObjects.append(Label(self.windowSurface, 'screenShowButton', 'lblName6', 'it is redish and bold and italic', pygame.Color('black'), 500, 450, isBold=True,fontSizePromille=60))
        self.renderObjects.append(Label(self.windowSurface, 'screenShowButton', 'lblName7', '(note: the bold and italic only works on system fonts)', pygame.Color('black'), 500, 550, isItalic=True,fontSizePromille=50))
        self.renderObjects.append(Label(self.windowSurface, 'screenShowButton', 'lblName8', 'press enter (when it has tab focus) or click on it', pygame.Color('black'), 500, 650, isBold=True,fontSizePromille=60))
        self.renderObjects.append(Label(self.windowSurface, 'screenShowButton', 'lblName9', 'to run a user defined function, if any', pygame.Color('black'), 500, 700, isBold=True,fontSizePromille=60))
        self.renderObjects.append(Button(self.windowSurface, 'screenShowButton', 'btnTest', 200, 800, 100,50, colorNormal=pygame.Color('pink'), colorHasFocus=(255,255,203),colorMouseOver=(255,192,255),colorMouseDown=pygame.Color('pink'),onClick=self.handleClick, fontSizePromille=20, text='Rounded'))
        # do some trickery to get the square to be rounded how we want it:
        # select latest addition, then
        self.renderObjects[len(self.renderObjects)-1].buttonNormal=Square(self.windowSurface, 'screenShowButton', 'btnTest', pygame.Color('grey'), 200, 800,100,50, 0, 10,20,30, 40,255, True)
        self.renderObjects[len(self.renderObjects)-1].buttonFocus=Square(self.windowSurface, 'screenShowButton', 'btnTest', pygame.Color('lightgrey'), 200, 800,100,50, 0,  10,20,30, 40,255, True)
        self.renderObjects[len(self.renderObjects)-1].buttonMouseOver=Square(self.windowSurface, 'screenShowButton', 'btnTest', pygame.Color('darkgrey'), 200, 800,100,50, 0,  10,20,30, 40,255, True)
        self.renderObjects[len(self.renderObjects)-1].buttonMouseDown=Square(self.windowSurface, 'screenShowButton', 'btnTest', pygame.Color('red'), 200,800,100,50,  0,  10,20,30, 40,255, True)
        # continue with normal stuff
        self.renderObjects.append(Button(self.windowSurface, 'screenShowButton', 'btnTest', 400, 800, 130,60, fontSizePromille=50, onClick=self.handleClick, fontName='couriernew'))
        self.renderObjects.append(Button(self.windowSurface, 'screenShowButton', 'btnTest', 600, 800, 140,55, fontSizePromille=38, onClick=self.handleClick, text='Ballpointprint.ttf', sysFont=False, fontName='Ballpointprint.ttf'))
        self.renderObjects.append(Button(self.windowSurface, 'screenShowButton', 'btnTest', 800, 800, 150,75, fontSizePromille=24, onClick=self.handleClick, text='Press Me!', alphaValue=50))
        self.renderObjects.append(Button(self.windowSurface, 'screenShowButton', 'btnBack', 300,920,300,100, text='Click to go Back', fontSizePromille=50,onClick=self.handleClick))
        self.renderObjects.append(Button(self.windowSurface, 'screenShowButton', 'btnContinue', 700,920,300,100, text='Click to Continue', fontSizePromille=50,onClick=self.handleClick))
        
        self.renderObjects.append(Label(self.windowSurface, 'screenShowCheckBox', 'lblName2', 'the CheckBox element', pygame.Color('black'), 500, 50, isBold=True))
        self.renderObjects.append(CheckBox(self.windowSurface, 'screenShowCheckBox', 'checkOne', 400, 150, 50,50, alphaValue=255, widthMargin=10 , onClick=self.handleClick))
        self.renderObjects.append(CheckBox(self.windowSurface, 'screenShowCheckBox', 'checkTwo', 400, 250, 50,50, alphaValue=255, widthMargin=10 , onClick=self.handleClick, value=False))
        self.renderObjects.append(CheckBox(self.windowSurface, 'screenShowCheckBox', 'checkThree', 400, 350, 50,50, alphaValue=255, widthMargin=10 , onClick=self.handleClick))
        self.renderObjects.append(Label(self.windowSurface, 'screenShowCheckBox', 'labelOne', 'Value=ww', pygame.Color('black'), 550, 150, fontSizePromille=50))
        self.renderObjects.append(Label(self.windowSurface, 'screenShowCheckBox', 'labelTwo', 'Value=False', pygame.Color('black'), 550, 250, fontSizePromille=50))
        self.renderObjects.append(Label(self.windowSurface, 'screenShowCheckBox', 'labelThree', 'Value=True', pygame.Color('black'), 550, 350, fontSizePromille=50))
        self.renderObjects.append(Label(self.windowSurface, 'screenShowCheckBox', 'lblName2', 'you can tab and shift-tab over them', pygame.Color('black'), 550, 500, fontSizePromille=50))
        self.renderObjects.append(Label(self.windowSurface, 'screenShowCheckBox', 'lblName2', 'press SPACEBAR when it has tabfocus, or click', pygame.Color('black'), 550, 550, fontSizePromille=50))
        self.renderObjects.append(Label(self.windowSurface, 'screenShowCheckBox', 'lblName2', 'to toggle value and run a user defined function, if any', pygame.Color('black'), 550, 600, fontSizePromille=50))
        self.renderObjects.append(Label(self.windowSurface, 'screenShowCheckBox', 'lblName2', 'you can tweak size, color, borderWidth, alphaValue', pygame.Color('black'), 550, 650, fontSizePromille=50))
        
        self.renderObjects.append(Button(self.windowSurface, 'screenShowCheckBox', 'btnBack', 300,920,300,100, text='Click to go Back', fontSizePromille=50,onClick=self.handleClick))
        self.renderObjects.append(Button(self.windowSurface, 'screenShowCheckBox', 'btnContinue', 700,920,300,100, text='Click to Continue', fontSizePromille=50,onClick=self.handleClick))
        
        self.renderObjects.append(Label(self.windowSurface, 'screenShowInputBox', 'lblName3', 'the InputBox element', pygame.Color('black'), 500, 50, isBold=True))
        self.renderObjects.append(InputBox(self.windowSurface, 'screenShowInputBox', 'ipbName1', 'Type Here', pygame.Color('brown'), 500, 175, False, 'Ballpointprint.ttf', onClick=self.handleClick))        
        self.renderObjects.append(InputBox(self.windowSurface, 'screenShowInputBox', 'ipbName2', 'Or Here', pygame.Color('brown'), 500, 300, onClick=self.handleClick))  
        self.renderObjects.append(Label(self.windowSurface, 'screenShowInputBox', 'lblName2', 'Any Size or Color or AlphaValue', pygame.Color('black'), 500, 400, fontSizePromille=60))
        self.renderObjects.append(Label(self.windowSurface, 'screenShowInputBox', 'lblName2', 'You can type in the InputBox if it has tab focus', pygame.Color('black'), 500, 450, fontSizePromille=60))
        self.renderObjects.append(Label(self.windowSurface, 'screenShowInputBox', 'lblName2', 'Use tab and shift tab or click to give it tab focus', pygame.Color('black'), 500, 500, fontSizePromille=60))
        self.renderObjects.append(Label(self.windowSurface, 'screenShowInputBox', 'lblName2', 'you can use backspace', pygame.Color('black'), 500, 550, fontSizePromille=60))
        self.renderObjects.append(Label(self.windowSurface, 'screenShowInputBox', 'lblName2', 'and type wëìçrd letters (if the font has it, most sys fonts do)', pygame.Color('black'), 500, 600, fontSizePromille=60))
        self.renderObjects.append(Label(self.windowSurface, 'screenShowInputBox', 'lblName2', 'it has a maximum size you can set', pygame.Color('black'), 500, 650, fontSizePromille=60))
        
        self.renderObjects.append(Label(self.windowSurface, 'screenShowInputBox', 'lblName2', 'it can also copy text to clipboard with ctrl-c', pygame.Color('black'), 500, 750, fontSizePromille=60))
        self.renderObjects.append(Label(self.windowSurface, 'screenShowInputBox', 'lblName2', 'it can receive text from clipboard with ctrl-v', pygame.Color('black'), 500, 800, fontSizePromille=60))
        
        
        self.renderObjects.append(Button(self.windowSurface, 'screenShowInputBox', 'btnBack', 300,920,300,100, text='Click to go Back', fontSizePromille=50,onClick=self.handleClick))
        self.renderObjects.append(Button(self.windowSurface, 'screenShowInputBox', 'btnContinue', 700,920,300,100, text='Click to go to begin', fontSizePromille=50,onClick=self.handleClick))
        
        # toggle flag to signal a screen update is needed
        self.needScreenUpdate=True
        self.gameState='screen1'
        self.counter=0
        
        # start main loop
        self.MainLoop()
        
    def handleClick(self,fromName='', fromText='', origin='unknown'):
        if fromName=='checkOne':
            value=False
            for item in self.renderObjects:
                if item.name=='checkOne':
                    value=item.value
                    break  
            for item in self.renderObjects:
                if item.name=='labelOne':
                    item.text=f'Value={value}'
                    item.resize(self.windowSurface)# trigger re-render
                    break
        elif fromName=='checkTwo':
            value=False
            for item in self.renderObjects:
                if item.name=='checkTwo':
                    value=item.value
                    break
            for item in self.renderObjects:
                if item.name=='labelTwo':
                    item.text=f'Value={value}'
                    item.resize(self.windowSurface)# trigger re-render
                    break
        elif fromName=='checkThree':
            value=False
            for item in self.renderObjects:
                if item.name=='checkThree':
                    value=item.value
                    break
            for item in self.renderObjects:
                if item.name=='labelThree':
                    item.text=f'Value={value}'
                    item.resize(self.windowSurface)# trigger re-render
                    break
                    
                    
        if self.gameState=='screen1' and fromName=='btnContinue':
            self.gameState='screenShowLabel'
            self.needScreenUpdate=True
        elif self.gameState=='screen1' and fromName=='btnBack':
            self.gameState='screenShowInputBox'
            self.setFocus('ipbName1')
            self.needScreenUpdate=True
            
        elif self.gameState=='screenShowLabel' and fromName=='btnContinue':
            self.gameState='screenShowLabel2'
            self.needScreenUpdate=True            
        elif self.gameState=='screenShowLabel' and fromName=='btnBack':
            self.gameState='screen1'
            self.needScreenUpdate=True
            
        elif self.gameState=='screenShowLabel2' and fromName=='btnBack':
            self.gameState='screenShowLabel'
            self.needScreenUpdate=True
        elif self.gameState=='screenShowLabel2' and fromName=='btnContinue':
            self.gameState='screenShowLine'
            self.needScreenUpdate=True
            
        elif self.gameState=='screenShowLine' and fromName=='btnBack':
            self.gameState='screenShowLabel2'
            self.needScreenUpdate=True
        elif self.gameState=='screenShowLine' and fromName=='btnContinue':
            self.gameState='screenShowSquare'
            self.needScreenUpdate=True
        
        elif self.gameState=='screenShowSquare' and fromName=='btnBack':
            self.gameState='screenShowLine'
            self.needScreenUpdate=True
        elif self.gameState=='screenShowSquare' and fromName=='btnContinue':
            self.gameState='screenShowEllipse'
            self.needScreenUpdate=True
            
        elif self.gameState=='screenShowEllipse' and fromName=='btnBack':
            self.gameState='screenShowSquare'
            self.needScreenUpdate=True
        elif self.gameState=='screenShowEllipse' and fromName=='btnContinue':
            self.gameState='screenShowImage'
            self.needScreenUpdate=True
            
        elif self.gameState=='screenShowImage' and fromName=='btnBack':
            self.gameState='screenShowEllipse'
            self.needScreenUpdate=True
        elif self.gameState=='screenShowImage' and fromName=='btnContinue':
            self.gameState='screenShowButton'
            self.needScreenUpdate=True
        
        elif self.gameState=='screenShowButton' and fromName=='btnBack':
            self.gameState='screenShowImage'
            self.needScreenUpdate=True
        elif self.gameState=='screenShowButton' and fromName=='btnContinue':
            self.gameState='screenShowCheckBox'
            self.needScreenUpdate=True
            
        elif self.gameState=='screenShowCheckBox' and fromName=='btnBack':
            self.gameState='screenShowButton'
            self.needScreenUpdate=True
        elif self.gameState=='screenShowCheckBox' and fromName=='btnContinue':
            self.gameState='screenShowInputBox'
            self.setFocus('ipbName1')
            self.needScreenUpdate=True
        
        elif self.gameState=='screenShowInputBox' and fromName=='btnBack':
            self.gameState='screenShowCheckBox'
            self.needScreenUpdate=True
        elif self.gameState=='screenShowInputBox' and fromName=='btnContinue':
            self.gameState='screen1'
            self.needScreenUpdate=True

        self.cleanState() # remove any mouseovers in other states for when we come back to them
        self.checkMouseOver(self.event)
    
    def setFocus(self,name):
        for item in self.renderObjects:
            if item.name==name and item.gameState==self.gameState and item.visible:
                item.hasFocus=True
                break
            
    def cleanState(self):
        for item in self.renderObjects:
            if not self.gameState == item.gameState and (item.type=='inputbox' or item.type=='checkbox' or item.type=='button'):
                item.gotMouseOver=False
                item.gotMouseDown=False
                item.hasFocus=False
        
    def quitElegantly(self):
        # you could do things like saves here
        pygame.quit()
        sys.exit()
        
    def updateScreen(self):
        # draw the screenColorBackground onto the surface
        self.windowSurface.fill(self.screenColorBackground)
        
        for item in self.renderObjects:
            if item.gameState==self.gameState and item.visible:
                item.updateOnScreen()
        
        # draw the window onto the screen
        pygame.display.update()
        
        # reset flag
        self.needScreenUpdate=False
        
    def setDisplay(self):
    
        if self.isFullscreen:
            self.windowSurface = pygame.display.set_mode(self.desktopSize, pygame.FULLSCREEN ,0)
        else:
            self.windowSurface = pygame.display.set_mode((self.screenWidth, self.screenHeight), pygame.RESIZABLE ,0)
        pygame.display.set_caption(self.caption)
        
#        updateScreen(fontName, message, windowSurface)

    def toggleFullScreen(self):
        self.isFullscreen=not self.isFullscreen
        self.setDisplay()
        
    def getPromille(self, position):
        #converts positon on screen to a promillage
        if self.isFullscreen:
            return ( int((1.0/(self.desktopSize[0]/position[0]))*1000.0), int((1.0/(self.desktopSize[1]/position[1])*1000.0)))
        else:
            return ( int((1.0/(self.screenWidth/position[0]))*1000.0), int((1.0/(self.screenHeight/position[1])*1000.0)))
        
    def handleResize(self, event):
        if self.screenWidth==event.w and self.screenHeight==event.h:
            pass # nothing changed
        else:
            if not self.isFullscreen: 
                self.screenWidth=event.w
                self.screenHeight=event.h
                self.setDisplay()	
        
        for item in self.renderObjects:
            item.resize(self.windowSurface)
            
    def checkMouseDown(self,event):
        for item in self.renderObjects:
            if item.gameState==self.gameState and item.visible and (item.type=='inputbox' or item.type=='checkbox' or item.type=='button'):
                if item.checkMouseDown(event.pos):
                    self.needScreenUpdate=True                    
    
    def checkMouseOver(self,event):
        for item in self.renderObjects:
            if item.gameState==self.gameState and item.visible and (item.type=='inputbox' or item.type=='checkbox' or item.type=='button'):
                if item.checkMouseOver(event.pos):
                    self.needScreenUpdate=True                    
                
    def checkMouseUp(self,event):
        for item in self.renderObjects:
            if item.type=='inputbox' or item.type=='checkbox' or item.type=='button':
                item.hasFocus=False
        for item in self.renderObjects:
            if item.gameState==self.gameState and item.visible and (item.type=='inputbox' or item.type=='checkbox' or item.type=='button'):
                #print(f"item.gameState={item.gameState} self.gameState={self.gameState}")
                if item.checkMouseUp(event.pos):
                    self.needScreenUpdate=True
                    break
        
    def MainLoop(self):
        currentTime=pygame.time.get_ticks()
        # run the game loop
        while True:
            
            # check to see if we need a screen update. If so, update the screen. 
            if self.needScreenUpdate:
                self.updateScreen()
            
            # check for quit events
            for event in pygame.event.get():
                if event.type == QUIT: # like control-break in the console, or the cross in the top right corner of the window
                    self.quitElegantly()
                elif event.type== KEYDOWN:
                    mods=pygame.key.get_mods()
                    if event.key== K_ESCAPE: # also quit on escape
                        self.quitElegantly()
                    elif (mods & KMOD_LALT or mods & KMOD_RALT) and event.key==K_F4:  #also quit on alt-f4
                        self.quitElegantly()
                    
                    elif (mods & KMOD_LCTRL or mods & KMOD_RCTRL) and event.key== K_f: # f pressed: toggle fullscreen
                        self.toggleFullScreen()
                        self.needScreenUpdate=True # toggle flag to signal a screen update is needed
                    
                    elif event.key== K_TAB:
                        self.needScreenUpdate=True
                        
                        # get list of tabable objects, as well as the current position of the focus
                        tabFocusAbleObjects=[]
                        counter=0
                        currentTabAt=-1
                        #for item in self.renderObjects:
                            #if item.type=='inputbox' or item.type=='checkbox' or item.type=='button':
                                #item.hasFocus=False

                        for item in self.renderObjects:
                            if item.type=='inputbox' or item.type=='checkbox' or item.type=='button':
                                if item.gameState==self.gameState and item.visible:
                                    tabFocusAbleObjects.append(item)
                                    if item.hasFocus:
                                        currentTabAt=counter
                                    counter=counter+1
                                item.hasFocus=False
                                

                        if mods & KMOD_SHIFT: # shift tab
                            if len(tabFocusAbleObjects): # only act if we have tabable objects
                                if currentTabAt==-1:# if there is no current tab position: focus the last 
                                    tabFocusAbleObjects[len(tabFocusAbleObjects)-1].hasFocus=True
                                    
                                else:
                                    if currentTabAt==0:# prevent going to far down
                                        currentTabAt=len(tabFocusAbleObjects)
                                    tabFocusAbleObjects[currentTabAt-1].hasFocus=True # set focus to one less

                        else: # tab
                            if len(tabFocusAbleObjects):# only act if we have tabable objects
                                if currentTabAt==-1:# if there is no current tab position: focus the first
                                    tabFocusAbleObjects[0].hasFocus=True
                                else:
                                    if currentTabAt==len(tabFocusAbleObjects)-1:# prevent going to far up
                                        currentTabAt=-1
                                    tabFocusAbleObjects[currentTabAt+1].hasFocus=True # set focus to one more
                    
                    elif event.key== K_RETURN:
                        for item in self.renderObjects:
                            if item.gameState==self.gameState and item.type=='inputbox' and item.hasFocus and item.visible:
                                item.onClick(item.name, item.text, 'enterkey')
                                self.needScreenUpdate=True
                            if item.gameState==self.gameState and item.type=='button' and item.hasFocus and item.visible:
                                item.onClick(item.name, item.value, 'enterkey')
                                self.needScreenUpdate=True
                    elif (mods & KMOD_LCTRL or mods & KMOD_RCTRL) and event.key== K_v:      
                        for item in self.renderObjects:
                            if item.gameState==self.gameState and item.type=='inputbox' and item.hasFocus and item.visible:
                                item.setText(pygame.scrap.get('text/plain;charset=utf-8').decode())
                                self.needScreenUpdate=True
                    elif (mods & KMOD_LCTRL or mods & KMOD_RCTRL) and event.key== K_c:      
                        for item in self.renderObjects:
                            if item.gameState==self.gameState and item.type=='inputbox' and item.hasFocus and item.visible:
                                scrap.put('text/plain;charset=utf-8', item.text.encode())
                                
                                print (f"copied {item.text} to clipboard")
                    
                    else:
                        for item in self.renderObjects:
                            if item.gameState==self.gameState and item.type=='inputbox' and item.hasFocus and item.visible:
                                if event.key==K_BACKSPACE:
                                    item.setText(item.text[:-1])
                                else:
                                    item.setText(item.text+event.unicode)
                                self.needScreenUpdate=True
                            if item.gameState==self.gameState and item.type=='checkbox' and item.hasFocus and item.visible:
                                if event.key==K_SPACE:
                                    item.value= not item.value
                                    if not item.onClick==None:
                                        item.onClick(item.name, item.value, 'spacebar')
                                    self.needScreenUpdate=True
                
                #detect game events:
                elif event.type == pygame.MOUSEBUTTONUP: # react to the moment the mouse button is going up again
                    if event.button==1: # left click, put new text location to click position
                        self.checkMouseUp(event)
                elif event.type == pygame.MOUSEMOTION: #
                    self.event=event
                    self.checkMouseOver(event)
                elif event.type== pygame.MOUSEBUTTONDOWN:
                    if event.button==1:
                        self.checkMouseDown(event)
                    
                elif event.type== VIDEORESIZE: # window resize detected
                    self.handleResize(event)
                    self.needScreenUpdate=True # toggle flag to signal a screen update is needed
            
            #check to see if we need sleep to free up processor
            oldTime=currentTime
            currentTime=pygame.time.get_ticks()
            overtime=(currentTime-oldTime)-self.desiredIntervalInMilliseconds
            if overtime<0:
                pygame.time.wait(abs(overtime))
                
if __name__=='__main__':
    testPygameElements()
    