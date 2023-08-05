#!/usr/bin/env python3
import os
import pygame
		
class simpleText():
    def __init__(self, blitToSurface=None, name='', text='', colorText=(255,255,255), horizontalMiddlePromille=500, verticalMiddlePromille=500, sysFont=True, fontName='timesnewroman', fontSizePromille=100, isBold=False, isItalic=True, antiAlias=True, alphaValue=255, visible=True):
        self.blitToSurface=blitToSurface
        self.name=name
        self.text=text
        self.colorText=colorText
        self.horizontalMiddlePromille=horizontalMiddlePromille
        self.verticalMiddlePromille=verticalMiddlePromille
        self.sysFont=sysFont
        self.fontName=fontName
        self.fontSizePromille=fontSizePromille
        self.isBold=isBold
        self.isItalic=isItalic
        self.antiAlias=antiAlias
        self.alphaValue=alphaValue
        self.visible=visible
        
        self.createFont()
        self.renderText(self.text)
		
    def createFont(self):
        self.screenWidth=self.blitToSurface.get_size()[0]
        self.screenHeight=self.blitToSurface.get_size()[1]
        self.fontSize=int((self.screenHeight/1000.0)*self.fontSizePromille)
        self.basicFont = None
        if self.sysFont: # using system font
            self.basicFont = pygame.font.SysFont(self.fontName, self.fontSize, self.isBold, self.isItalic) 
        else: # loading font from file
            if os.path.isfile(self.fontName): # try loading it from the same location as the program 
                self.basicFont = pygame.font.Font(self.fontName, self.fontSize) 
            else: # or, if that fails, perhaps its in the 'fonts' folder?
                if os.path.isdir('fonts'):
                    if os.path.isfile(os.path.join('fonts' , self.fontName)):
                        self.basicFont = pygame.font.Font(os.path.join('fonts' , self.fontName), self.fontSize) 
	
    def renderText(self, text):
        self.text=text
        
        self.textRender= self.basicFont.render(self.text, self.antiAlias, self.colorText)
        alphaImage = pygame.Surface(self.textRender.get_size(), pygame.SRCALPHA)
        alphaImage.fill((255, 255, 255, self.alphaValue))
        self.textRender.blit(alphaImage, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        self.textWidth=self.textRender.get_rect()[2]
        self.textHeight=self.textRender.get_rect()[3]
        
        self.horizontalMiddle=int((self.screenWidth/1000.0)*self.horizontalMiddlePromille)
        self.verticalMiddle=int((self.screenHeight/1000.0)*self.verticalMiddlePromille)
        
        self.leftTop=(int(self.horizontalMiddle-(self.textWidth/2.0)),int(self.verticalMiddle-(self.textHeight/2.0)))

    def resize(self, newSurface):
        self.blitToSurface=newSurface
        self.createFont()
        self.renderText(self.text)
	    
    def updateOnScreen(self):
        if self.visible:
            self.blitToSurface.blit(self.textRender, self.leftTop)
	