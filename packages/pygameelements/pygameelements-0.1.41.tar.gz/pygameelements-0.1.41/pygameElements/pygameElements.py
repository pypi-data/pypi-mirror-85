#!/usr/bin/env python3
import os
import sys
import pygame

class Button():
    def __init__(self, blitToSurface=None, gameState='', name='', horizontalMiddlePromille=500, verticalMiddlePromille=500, horizontalSizePromille=500,  
verticalSizePromille=100, colorNormal=(190,190,190), colorHasFocus=(190,255,190),colorMouseOver=(190,190,255),colorMouseDown=(255,190,190), value=None, 
alphaValue=255, hasFocus=False, visible=True, onClick=None, text='button', enabled=True, sysFont=True, fontName='timesnewroman', fontSizePromille=80, antiAlias=True):
       
        
        self.type='button'
        self.blitToSurface=blitToSurface
        self.gameState=gameState
        self.name=name
        
        self.horizontalMiddlePromille=horizontalMiddlePromille
        self.verticalMiddlePromille=verticalMiddlePromille
        self.horizontalSizePromille=horizontalSizePromille
        self.verticalSizePromille=verticalSizePromille
        
        self.colorNormal=colorNormal
        self.colorHasFocus=colorHasFocus
        self.colorMouseOver=colorMouseOver
        self.colorMouseDown=colorMouseDown
        self.value=value
        self.text=text
        self.enabled=enabled
        self.sysFont=sysFont
        self.fontName=fontName
        self.fontSizePromille=fontSizePromille
        self.antiAlias=antiAlias
        
        self.alphaValue=alphaValue
        self.hasFocus=hasFocus
        self.visible=visible
        
        self.gotMouseOver=False
        self.gotMouseDown=False
        
        self.currentState='stateNormal'
        
        self.onClick=onClick
        
        widthBorder=0 # fill
        borderTopLeft=10
        borderTopRight=10
        borderBottomLeft=10
        borderBottomRight=10
        alphaValue=self.alphaValue

        self.buttonNormal=Square(self.blitToSurface, self.gameState, self.name, self.colorNormal, self.horizontalMiddlePromille, self.verticalMiddlePromille, self.horizontalSizePromille,  self.verticalSizePromille,  widthBorder, borderTopLeft,borderTopRight,borderBottomLeft, borderBottomRight,alphaValue, self.visible)
        self.buttonFocus=Square(self.blitToSurface, self.gameState, self.name, self.colorHasFocus, self.horizontalMiddlePromille, self.verticalMiddlePromille, self.horizontalSizePromille,  self.verticalSizePromille,  widthBorder, borderTopLeft,borderTopRight,borderBottomLeft, borderBottomRight, alphaValue, self.visible)
        self.buttonMouseOver=Square(self.blitToSurface, self.gameState, self.name, self.colorMouseOver, self.horizontalMiddlePromille, self.verticalMiddlePromille, self.horizontalSizePromille,  self.verticalSizePromille,  widthBorder, borderTopLeft,borderTopRight,borderBottomLeft, borderBottomRight, alphaValue, self.visible)
        self.buttonMouseDown=Square(self.blitToSurface, self.gameState, self.name, self.colorMouseDown, self.horizontalMiddlePromille, self.verticalMiddlePromille, self.horizontalSizePromille,  self.verticalSizePromille,  widthBorder, borderTopLeft,borderTopRight,borderBottomLeft, borderBottomRight, alphaValue, self.visible)

        self.labelColorNormal=(int(self.colorNormal[0]/2),int(self.colorNormal[1]/2),int(self.colorNormal[2]/2))
        self.labelColorFocus=(int(self.colorHasFocus[0]/4),155,int(self.colorHasFocus[2]/4))
        self.labelColorMouseOver=(int(self.colorMouseOver[0]/2),int(self.colorMouseOver[1]/2),155)
        self.labelColorMouseDown=(155,int(self.colorMouseDown[1]/2),int(self.colorMouseDown[2]/2))
        
        self.labelNormal=Label(self.blitToSurface, self.gameState, self.name, self.text, self.labelColorNormal, self.horizontalMiddlePromille, self.verticalMiddlePromille, self.sysFont, self.fontName, self.fontSizePromille, False, False, self.antiAlias, self.alphaValue, self.visible)
        self.labelFocus=Label(self.blitToSurface, self.gameState, self.name, self.text, self.labelColorFocus, self.horizontalMiddlePromille, self.verticalMiddlePromille, self.sysFont, self.fontName, self.fontSizePromille, True, False, self.antiAlias, self.alphaValue, self.visible)
        self.labelMouseOver=Label(self.blitToSurface, self.gameState, self.name, self.text, self.labelColorMouseOver, self.horizontalMiddlePromille, self.verticalMiddlePromille, self.sysFont, self.fontName, self.fontSizePromille, False, True, self.antiAlias, self.alphaValue, self.visible)
        self.labelMouseDown=Label(self.blitToSurface, self.gameState, self.name, self.text, self.labelColorMouseDown, self.horizontalMiddlePromille, self.verticalMiddlePromille, self.sysFont, self.fontName, self.fontSizePromille, False, True, self.antiAlias, self.alphaValue, self.visible)
        
        
        self.resize(blitToSurface)
        
        
    def checkMouseUp(self,position):
        if not self.visible:
            return False
        oldMouseOver=self.gotMouseOver
        oldMouseDown=self.gotMouseDown
        
        if position[0]<self.left or position[0]>self.right or position[1]<self.top or position[1]>self.bottom:
            self.gotMouseOver=False
            self.gotMouseDown=False
        else:
            self.gotMouseOver=True
            self.gotMouseDown=False
            self.hasFocus=True
            
            if not self.onClick==None:
                self.onClick(self.name, str(self.value), 'mouseclick')
            
        if oldMouseOver==self.gotMouseOver and oldMouseDown==self.gotMouseDown:
            return False
        else:
            return True     

    def checkMouseDown(self,position):
        if not self.visible:
            return False  
        
        oldMouseDown=self.gotMouseDown
        
        if position[0]<self.left or position[0]>self.right or position[1]<self.top or position[1]>self.bottom:
            self.gotMouseDown=False
        else:
            self.gotMouseDown=True
            
        if oldMouseDown==self.gotMouseDown:
            return False
        else:
            return True     

    def checkMouseOver(self,position):
        if not self.visible:
            return False
        
        oldMouseOver=self.gotMouseOver
        oldMouseDown=self.gotMouseDown
        
        if position[0]<self.left or position[0]>self.right or position[1]<self.top or position[1]>self.bottom:
            self.gotMouseOver=False
            self.gotMouseDown=False
        else:
            self.gotMouseOver=True
        
        if oldMouseOver==self.gotMouseOver and oldMouseDown==self.gotMouseDown:
            return False
        else:
            return True    
    
    def resize(self, newSurface):
        self.screenWidth=newSurface.get_size()[0]
        self.screenHeight=newSurface.get_size()[1]        
    
        self.buttonNormal.resize(newSurface)
        self.buttonFocus.resize(newSurface)
        self.buttonMouseOver.resize(newSurface)
        self.buttonMouseDown.resize(newSurface)
        
        self.labelNormal.resize(newSurface)
        self.labelFocus.resize(newSurface)
        self.labelMouseOver.resize(newSurface)
        self.labelMouseDown.resize(newSurface)
        
        self.width=int((self.screenWidth/1000.0)*self.horizontalSizePromille)
        self.height=int((self.screenHeight/1000.0)*self.verticalSizePromille)
        self.horizontalMiddle=int((self.screenWidth/1000.0)*self.horizontalMiddlePromille)
        self.verticalMiddle=int((self.screenHeight/1000.0)*self.verticalMiddlePromille)
        self.top=int(self.verticalMiddle-(self.height/2.0))
        self.bottom=int(self.verticalMiddle+(self.height/2.0))
        self.left=int(self.horizontalMiddle-(self.width/2.0))
        self.right=int(self.horizontalMiddle+(self.width/2.0))
        self.leftTop=(self.left,self.top)
        
    def updateOnScreen(self): 
        if self.visible:
            self.currentState='stateNormal'
            if self.hasFocus:
                self.currentState='stateFocus'
            if self.gotMouseOver:
                self.currentState='stateMouseOver'
                if self.gotMouseDown:
                    self.currentState='stateMouseDown'
        
            if self.currentState=='stateNormal':
                self.buttonNormal.updateOnScreen()
                self.labelNormal.updateOnScreen()
            elif self.currentState=='stateFocus':
                self.buttonFocus.updateOnScreen()
                self.labelFocus.updateOnScreen()
            elif self.currentState=='stateMouseOver':
                self.buttonMouseOver.updateOnScreen()
                self.labelMouseOver.updateOnScreen()
            elif self.currentState=='stateMouseDown':
                self.buttonMouseDown.updateOnScreen()
                self.labelMouseDown.updateOnScreen()
    
class CheckBox():
    #self.windowSurface, 'all', 'chkOne', pygame.Color('blue'), 900, 500, 950,550, alphaValue=255, widthMargin=5 , value=False))
    def __init__(self,blitToSurface=None, gameState='', name='', horizontalMiddlePromille=500, verticalMiddlePromille=500, horizontalSizePromille=500,  
verticalSizePromille=500, inColor=(190,190,190), outColor=(135,135,135), tickColor=(100,100,100),
alphaValue=255, widthMargin=5, widthBorder=5, value=True, hasFocus=False, visible=True, onClick=None):

        self.type='checkbox'
        self.blitToSurface=blitToSurface
        self.gameState=gameState
        self.name=name
        self.inColor=inColor
        self.outColor=outColor
        self.tickColor=tickColor
        
        self.horizontalMiddlePromille=horizontalMiddlePromille
        self.verticalMiddlePromille=verticalMiddlePromille
        self.horizontalSizePromille=horizontalSizePromille
        self.verticalSizePromille=verticalSizePromille
        
        self.alphaValue=alphaValue
        self.widthMargin=widthMargin
        self.widthBorder=widthBorder
        self.value=value
        self.hasFocus=hasFocus
        self.visible=visible
        
        self.gotMouseOver=False
        self.gotMouseDown=False
        
        self.currentState='stateNormal'
        
        self.onClick=onClick
        #Square (blitToSurface=None, gameState='', name='', color=(255,255,255,255), 
#horizontalMiddlePromille=500, verticalMiddlePromille=500, horizontalSizePromille=100,  verticalSizePromille=400, 
#widthBorder=0, borderTopLeft=1,borderTopRight=1,borderBottomLeft=1, borderBottomRight=1, 
#alphaValue=255, visible=True):
        
        
        
        self.resize(blitToSurface)
        
    def checkMouseUp(self,position):
        if not self.visible:
            return False
        oldMouseOver=self.gotMouseOver
        oldMouseDown=self.gotMouseDown
        
        if position[0]<self.left or position[0]>self.right or position[1]<self.top or position[1]>self.bottom:
            self.gotMouseOver=False
            self.gotMouseDown=False
            self.hasFocus=False
        else:
            self.gotMouseOver=True
            self.gotMouseDown=False
            self.hasFocus=True
            self.value=not self.value
            try:
                self.onClick(self.name, str(self.value), 'mouseclick')
            except:
                pass
            
        if oldMouseOver==self.gotMouseOver and oldMouseDown==self.gotMouseDown:
            return False
        else:
            return True     

    def checkMouseDown(self,position):
        if not self.visible:
            return False  
        
        oldMouseDown=self.gotMouseDown
        
        if position[0]<self.left or position[0]>self.right or position[1]<self.top or position[1]>self.bottom:
            self.gotMouseDown=False
        else:
            self.gotMouseDown=True
            
        if oldMouseDown==self.gotMouseDown:
            return False
        else:
            return True     

    def checkMouseOver(self,position):
        if not self.visible:
            return False
        
        oldMouseOver=self.gotMouseOver
        oldMouseDown=self.gotMouseDown
        
        if position[0]<self.left or position[0]>self.right or position[1]<self.top or position[1]>self.bottom:
            self.gotMouseOver=False
            self.gotMouseDown=False
        else:
            self.gotMouseOver=True
        
        if oldMouseOver==self.gotMouseOver and oldMouseDown==self.gotMouseDown:
            return False
        else:
            return True    
        
    def resize(self, newSurface):
        self.screenWidth=newSurface.get_size()[0]
        self.screenHeight=newSurface.get_size()[1]        
    
        widthBorder=0 # fill
        borderTopLeft=10
        borderTopRight=10
        borderBottomLeft=10
        borderBottomRight=10
        alphaValue=self.alphaValue        
        focusColor=(self.outColor[0],200,self.outColor[2])
        mouseOverColor=(self.outColor[0],self.outColor[2],255)
        mouseDownColor=(255,self.outColor[0],self.outColor[2])
        

        self.outsideNormal=Square(self.blitToSurface, self.gameState, self.name, self.outColor, self.horizontalMiddlePromille, self.verticalMiddlePromille, self.horizontalSizePromille,  self.verticalSizePromille,  widthBorder, borderTopLeft,borderTopRight,borderBottomLeft, borderBottomRight,alphaValue, self.visible)
        self.outsideFocus=Square(self.blitToSurface, self.gameState, self.name, focusColor, self.horizontalMiddlePromille, self.verticalMiddlePromille, self.horizontalSizePromille,  self.verticalSizePromille,  widthBorder, borderTopLeft,borderTopRight,borderBottomLeft, borderBottomRight, alphaValue, self.visible)
        self.outsideMouseOver=Square(self.blitToSurface, self.gameState, self.name, mouseOverColor, self.horizontalMiddlePromille, self.verticalMiddlePromille, self.horizontalSizePromille,  self.verticalSizePromille,  widthBorder, borderTopLeft,borderTopRight,borderBottomLeft, borderBottomRight, alphaValue, self.visible)
        self.outsideMouseDown=Square(self.blitToSurface, self.gameState, self.name, mouseDownColor, self.horizontalMiddlePromille, self.verticalMiddlePromille, self.horizontalSizePromille,  self.verticalSizePromille,  widthBorder, borderTopLeft,borderTopRight,borderBottomLeft, borderBottomRight, alphaValue, self.visible)

        horizontalSizePromille=int(self.horizontalSizePromille-self.widthMargin)
        verticalSizePromille=int(self.verticalSizePromille-self.widthMargin)

        widthBorder=0
        borderTopLeft=10
        borderTopRight=10
        borderBottomLeft=10
        borderBottomRight=10
        alphaValue=self.alphaValue
        focusColor=(self.inColor[0],200,self.inColor[2])
        mouseOverColor=(self.inColor[0],self.inColor[2],255)
        mouseDownColor=(255,self.inColor[0],self.inColor[2])

        self.insideNormal=Square(self.blitToSurface, self.gameState, self.name, self.inColor, self.horizontalMiddlePromille, self.verticalMiddlePromille, horizontalSizePromille, verticalSizePromille,  widthBorder, borderTopLeft,borderTopRight,borderBottomLeft, borderBottomRight,alphaValue, self.visible)
        self.insideFocus=Square(self.blitToSurface, self.gameState, self.name, focusColor, self.horizontalMiddlePromille, self.verticalMiddlePromille, horizontalSizePromille, verticalSizePromille,  widthBorder, borderTopLeft,borderTopRight,borderBottomLeft, borderBottomRight, alphaValue, self.visible)
        self.insideMouseOver=Square(self.blitToSurface, self.gameState, self.name, mouseOverColor, self.horizontalMiddlePromille, self.verticalMiddlePromille, horizontalSizePromille,  verticalSizePromille,  widthBorder, borderTopLeft,borderTopRight,borderBottomLeft, borderBottomRight, alphaValue, self.visible)
        self.insideMouseDown=Square(self.blitToSurface, self.gameState, self.name, mouseDownColor, self.horizontalMiddlePromille, self.verticalMiddlePromille, horizontalSizePromille,  verticalSizePromille,  widthBorder, borderTopLeft,borderTopRight,borderBottomLeft, borderBottomRight, alphaValue, self.visible)
        
        horizontalSizePromille=int(self.horizontalSizePromille-self.widthMargin*2.0)
        verticalSizePromille=int(self.verticalSizePromille-self.widthMargin*2.0)

        widthBorder=0 # fill
        borderTopLeft=5
        borderTopRight=5
        borderBottomLeft=5
        borderBottomRight=5
        
        focusColor=(self.tickColor[0],120,self.tickColor[2])
        mouseOverColor=(self.tickColor[0],self.tickColor[2],255)
        mouseDownColor=(255,self.tickColor[0],self.tickColor[2])
        
        self.tickedNormal=Square(self.blitToSurface, self.gameState, self.name, self.tickColor, self.horizontalMiddlePromille, self.verticalMiddlePromille, horizontalSizePromille,  verticalSizePromille,  widthBorder, borderTopLeft,borderTopRight,borderBottomLeft, borderBottomRight, self.alphaValue, self.visible)
        self.tickedFocus=Square(self.blitToSurface, self.gameState, self.name, focusColor, self.horizontalMiddlePromille, self.verticalMiddlePromille, horizontalSizePromille,  verticalSizePromille,  widthBorder, borderTopLeft,borderTopRight,borderBottomLeft, borderBottomRight,  self.alphaValue, self.visible)
        self.tickedMouseOver=Square(self.blitToSurface, self.gameState, self.name, mouseOverColor, self.horizontalMiddlePromille, self.verticalMiddlePromille, horizontalSizePromille,  verticalSizePromille,  widthBorder, borderTopLeft,borderTopRight,borderBottomLeft, borderBottomRight,  self.alphaValue, self.visible)
        self.tickedMouseDown=Square(self.blitToSurface, self.gameState, self.name, mouseDownColor, self.horizontalMiddlePromille, self.verticalMiddlePromille, horizontalSizePromille,  verticalSizePromille,  widthBorder, borderTopLeft,borderTopRight,borderBottomLeft, borderBottomRight,  self.alphaValue, self.visible)
        
        self.checkboxWidth=int((self.screenWidth/1000.0)*self.horizontalSizePromille)
        self.checkboxHeight=int((self.screenHeight/1000.0)*self.verticalSizePromille)
        self.horizontalMiddle=int((self.screenWidth/1000.0)*self.horizontalMiddlePromille)
        self.verticalMiddle=int((self.screenHeight/1000.0)*self.verticalMiddlePromille)
        self.top=int(self.verticalMiddle-(self.checkboxHeight/2.0))
        self.bottom=int(self.verticalMiddle+(self.checkboxHeight/2.0))
        self.left=int(self.horizontalMiddle-(self.checkboxWidth/2.0))
        self.right=int(self.horizontalMiddle+(self.checkboxWidth/2.0))
        
        
        
    def updateOnScreen(self):   
        if self.visible:
            self.currentState='stateNormal'
            if self.hasFocus:
                self.currentState='stateFocus'
            if self.gotMouseOver:
                self.currentState='stateMouseOver'
                if self.gotMouseDown:
                    self.currentState='stateMouseDown'
        
            if self.currentState=='stateNormal':
                self.outsideNormal.updateOnScreen()
                self.insideNormal.updateOnScreen()
            elif self.currentState=='stateFocus':
                self.outsideFocus.updateOnScreen()
                self.insideFocus.updateOnScreen()
            elif self.currentState=='stateMouseOver':
                self.outsideMouseOver.updateOnScreen()
                self.insideMouseOver.updateOnScreen()
            elif self.currentState=='stateMouseDown':
                self.outsideMouseDown.updateOnScreen()
                self.insideMouseDown.updateOnScreen()
        
            if self.value:
                if self.currentState=='stateNormal':
                    self.tickedNormal.updateOnScreen()
                elif self.currentState=='stateFocus':
                    self.tickedFocus.updateOnScreen()
                elif self.currentState=='stateMouseOver':
                    self.tickedMouseOver.updateOnScreen()
                elif self.currentState=='stateMouseDown':
                    self.tickedMouseDown.updateOnScreen()
                
            
class InputBox():
    def __init__(self,blitToSurface=None, gameState='', name='', text='', colorText=(255,255,255),
horizontalMiddlePromille=500, verticalMiddlePromille=500, sysFont=True, fontName='timesnewroman', 
fontSizePromille=100, isBold=False, isItalic=True, antiAlias=True, alphaValue=255, visible=True, 
hasFocus=False, onClick=None, maxSize=15):

        self.blitToSurface=blitToSurface
        self.hasFocus=hasFocus
        self.labelNormal=Label(blitToSurface, gameState, name, text, colorText, horizontalMiddlePromille, verticalMiddlePromille, sysFont, fontName, fontSizePromille, False, False, antiAlias, alphaValue, visible)
        self.labelFocus=Label(blitToSurface, gameState, name, text, (0,155,0), horizontalMiddlePromille, verticalMiddlePromille, sysFont, fontName, fontSizePromille, True, isItalic, antiAlias, alphaValue, visible)
        self.labelMouseOver=Label(blitToSurface, gameState, name, text, (0,50,155), horizontalMiddlePromille, verticalMiddlePromille, sysFont, fontName, fontSizePromille, isBold, True, antiAlias, alphaValue, visible)
        self.labelMouseDown=Label(blitToSurface, gameState, name, text, (255,0,0), horizontalMiddlePromille, verticalMiddlePromille, sysFont, fontName, fontSizePromille, isBold, True, antiAlias, alphaValue, visible)
        self.gotMouseOver=False
        self.gotMouseDown=False
        self.type='inputbox'
        self.visible=visible
        
        self.currentState='stateNormal'
            
        self.name=name
        self.gameState=gameState
        self.text=text
        self.maxSize=maxSize
        
        self.onClick=onClick
        
        self.resize(blitToSurface)
        
    def setText(self,text):
        if len(text)>self.maxSize:
            self.text=text[:self.maxSize]
        else:
            self.text=text
        self.labelNormal.renderText(self.text)
        self.labelFocus.renderText(self.text)
        self.labelMouseOver.renderText(self.text)
        self.labelMouseDown.renderText(self.text)
        
    def setVisible(self,newVisible):
        self.visible=newVisible
        self.labelNormal.visible=newVisible
        self.labelFocus.visible=newVisible
        self.labelMouseOver.visible=newVisible
        self.labelMouseDown.visible=newVisible
        
    def checkMouseUp(self,position):
        if not self.visible:
            return False
        oldMouseOver=self.gotMouseOver
        oldMouseDown=self.gotMouseDown
        
        if position[0]<self.left or position[0]>self.right or position[1]<self.top or position[1]>self.bottom:
            self.gotMouseOver=False
            self.gotMouseDown=False
            self.hasFocus=False
        else:
            self.gotMouseOver=True
            self.gotMouseDown=False
            self.hasFocus=True
            try:
                self.onClick(self.name, self.text, 'mouseclick')
            except:
                pass
            
        if oldMouseOver==self.gotMouseOver and oldMouseDown==self.gotMouseDown:
            return False
        else:
            return True                
        
    def checkMouseDown(self,position):
        if not self.visible:
            return False
        
        oldMouseDown=self.gotMouseDown
        
        if position[0]<self.left or position[0]>self.right or position[1]<self.top or position[1]>self.bottom:
            self.gotMouseDown=False
        else:
            self.gotMouseDown=True
            
        if oldMouseDown==self.gotMouseDown:
            return False
        else:
            return True        
        
    def checkMouseOver(self,position):
        if not self.visible:
            return False
        
        oldMouseOver=self.gotMouseOver
        oldMouseDown=self.gotMouseDown
        
        if position[0]<self.left or position[0]>self.right or position[1]<self.top or position[1]>self.bottom:
            self.gotMouseOver=False
            self.gotMouseDown=False
        else:
            self.gotMouseOver=True
        
        if oldMouseOver==self.gotMouseOver and oldMouseDown==self.gotMouseDown:
            return False
        else:
            return True        
        
        
    def resize(self, newSurface):
        
        self.labelNormal.blitToSurface=newSurface
        self.labelNormal.createFont()
        self.labelNormal.renderText(self.text)
	    
        self.labelFocus.blitToSurface=newSurface
        self.labelFocus.createFont()
        self.labelFocus.renderText(self.text)
	    
        self.labelMouseOver.blitToSurface=newSurface
        self.labelMouseOver.createFont()
        self.labelMouseOver.renderText(self.text)
	    
        self.labelMouseDown.blitToSurface=newSurface
        self.labelMouseDown.createFont()
        self.labelMouseDown.renderText(self.text)
        
        self.screenWidth=newSurface.get_size()[0]
        self.screenHeight=newSurface.get_size()[1]        
        self.textWidth=self.labelNormal.textRender.get_rect()[2]
        self.textHeight=self.labelNormal.textRender.get_rect()[3]
        self.horizontalMiddle=int((self.screenWidth/1000.0)*self.labelNormal.horizontalMiddlePromille)
        self.verticalMiddle=int((self.screenHeight/1000.0)*self.labelNormal.verticalMiddlePromille)
        self.top=int(self.verticalMiddle-(self.textHeight/2.0))
        self.bottom=int(self.verticalMiddle+(self.textHeight/2.0))
        self.left=int(self.horizontalMiddle-(self.textWidth/2.0))
        self.right=int(self.horizontalMiddle+(self.textWidth/2.0))
       

    def updateOnScreen(self):

        self.currentState='stateNormal'
        if self.hasFocus:
            self.currentState='stateFocus'
        if self.gotMouseOver:
            self.currentState='stateMouseOver'
            if self.gotMouseDown:
                self.currentState='stateMouseDown'
    
        if self.currentState=='stateNormal':
            if self.labelNormal.visible:
                self.labelNormal.blitToSurface.blit(self.labelNormal.textRender, self.labelNormal.leftTop)	     
        elif self.currentState=='stateFocus':
            if self.labelFocus.visible:
                self.labelFocus.blitToSurface.blit(self.labelFocus.textRender, self.labelFocus.leftTop)	     
        elif self.currentState=='stateMouseOver':
            if self.labelMouseOver.visible:
                self.labelMouseOver.blitToSurface.blit(self.labelMouseOver.textRender, self.labelMouseOver.leftTop)	     
        elif self.currentState=='stateMouseDown':
            if self.labelMouseDown.visible:
                self.labelMouseDown.blitToSurface.blit(self.labelMouseDown.textRender, self.labelMouseDown.leftTop)	     

class Image():
    def __init__(self, blitToSurface=None, gameState='', name='', fileName='', 
horizontalMiddlePromille=500, verticalMiddlePromille=500, horizontalSizePromille=500,  verticalSizePromille=500, 
rotation=0, stretch=True, alphaValue=255, visible=True):

        self.type='image'
        self.blitToSurface=blitToSurface
        self.gameState=gameState
        self.name=name
        self.fileName=fileName
        self.horizontalMiddlePromille=horizontalMiddlePromille
        self.verticalMiddlePromille=verticalMiddlePromille
        self.horizontalSizePromille=horizontalSizePromille
        self.verticalSizePromille=verticalSizePromille
        self.rotation=rotation
        self.stretch=stretch
        self.alphaValue=alphaValue        
        self.visible=visible
        
        self.loadFileName(self.fileName)
        
    def loadFileName(self,fileName):
        self.fileName=fileName
        self.imageRaw=None
        if os.path.isfile(fileName): # load from same place as executable
            self.imageRaw=pygame.image.load(fileName)
        else:
            if os.path.isdir('images') and os.path.isfile(os.path.join('images' , fileName)):
                self.imageRaw=pygame.image.load(os.path.join('images' , fileName))
            else:
                parts=os.path.abspath(__file__+"/../..") # take the path this very py file is in now (os dependant!), and drop the last 2 items (the pygameElements name and folder it is in)
                parts=os.path.join(parts , 'pygameElementsTest') # then, at that place, add the pygameElementsTest folder 
                folder=os.path.join(parts , 'images') # inside that: there should be a images folder
                fileLocation=os.path.join(folder , fileName) # adding the filename required, should be the fileLocation
                if os.path.isdir(folder) and os.path.isfile(fileLocation): # so if that folder exist: and the file exist as well
                    self.imageRaw = pygame.image.load(fileLocation) # use it
                else:   # ok give up, just take timesnewroman   
                    print(f"warning: Could not load image {fileName}")
                    # lets make a cross ourselves
                    self.screenWidth=self.blitToSurface.get_size()[0]
                    self.screenHeight=self.blitToSurface.get_size()[1]
                    
                    self.horizontalMiddle=int((self.screenWidth/1000.0)*self.horizontalMiddlePromille)
                    self.verticalMiddle=int((self.screenHeight/1000.0)*self.verticalMiddlePromille)
                    
                    self.width=int((self.screenWidth/1000.0)*self.horizontalSizePromille)
                    self.height=int((self.screenHeight/1000.0)*self.verticalSizePromille)

                    self.imageRaw=pygame.Surface((self.width, self.height),pygame.SRCALPHA)
                    self.imageRaw.set_alpha(128)          
                    self.imageRaw.fill(pygame.Color('grey'))
                    pygame.draw.line(self.imageRaw,pygame.Color('red'), (0,0),(self.width, self.height), 3)
                    pygame.draw.line(self.imageRaw,pygame.Color('red'), (self.width,0),(0, self.height), 3)
                    self.imageRawRect=self.imageRaw.get_rect()

        self.renderImage()
        
    def renderImage(self):
        self.imageRawRect=self.imageRaw.get_rect()
        self.screenWidth=self.blitToSurface.get_size()[0]
        self.screenHeight=self.blitToSurface.get_size()[1]
        
        self.horizontalMiddle=int((self.screenWidth/1000.0)*self.horizontalMiddlePromille)
        self.verticalMiddle=int((self.screenHeight/1000.0)*self.verticalMiddlePromille)
        
        self.width=int((self.screenWidth/1000.0)*self.horizontalSizePromille)
        self.height=int((self.screenHeight/1000.0)*self.verticalSizePromille)
        if self.stretch:
            self.top=self.verticalMiddle-self.height/2.0
            self.left=self.horizontalMiddle-self.width/2.0
        else:
            self.top=self.verticalMiddle-self.imageRawRect[2]/2.0
            self.left=self.horizontalMiddle-self.imageRawRect[3]/2.0
        
        self.leftTop=(self.left,self.top)
        if self.stretch:
            self.imageRender = pygame.Surface((self.imageRawRect[2], self.imageRawRect[3]),pygame.SRCALPHA)
            self.imageRender.set_alpha(self.alphaValue)          
            self.imageRender.blit(self.imageRaw, (0,0))
            self.imageRender=pygame.transform.scale(self.imageRender, (self.width, self.height))
        else: 
            self.imageRender = pygame.Surface((self.width, self.height),pygame.SRCALPHA)
            self.imageRender.set_alpha(self.alphaValue)          
            self.imageRender.blit(self.imageRaw, (0,0))
        
        if not self.rotation==0: # rotated image
            self.imageRender=pygame.transform.rotate(self.imageRender, self.rotation) 
            self.surfaceRect=self.imageRender.get_rect()
            self.extraWidthBecauseRotation=self.surfaceRect.w-self.width
            self.extraHeightBecauseRotation=self.surfaceRect.h-self.height
            self.leftAfterRotation=int(self.left-(self.extraWidthBecauseRotation/2.0))
            self.topAfterRotation=int(self.top-(self.extraHeightBecauseRotation/2.0))
            self.leftTopRotated=(self.leftAfterRotation,self.topAfterRotation)
        else:
            self.leftTopRotated=self.leftTop
        
    def resize(self, newSurface):
        self.blitToSurface=newSurface
        self.renderImage()
	    
    def updateOnScreen(self):
        if self.visible:
            self.blitToSurface.blit(self.imageRender, (self.leftTopRotated))
            

class Ellipse():
    def __init__(self, blitToSurface=None, gameState='', name='', color=(255,255,255), 
horizontalMiddlePromille=500, verticalMiddlePromille=500, horizontalSizePromille=500,  verticalSizePromille=500, 
widthBorder=0, alphaValue=255, visible=True):

        self.type='elipse'
        self.blitToSurface=blitToSurface
        self.gameState=gameState
        self.name=name
        self.color=color
        self.horizontalMiddlePromille=horizontalMiddlePromille
        self.verticalMiddlePromille=verticalMiddlePromille
        self.horizontalSizePromille=horizontalSizePromille
        self.verticalSizePromille=verticalSizePromille
        
        self.widthBorder=widthBorder
        self.alphaValue=alphaValue        
        self.visible=visible
        
        self.renderEllipse()
        
    def renderEllipse(self):
        self.screenWidth=self.blitToSurface.get_size()[0]
        self.screenHeight=self.blitToSurface.get_size()[1]
        
        self.horizontalMiddle=int((self.screenWidth/1000.0)*self.horizontalMiddlePromille)
        self.verticalMiddle=int((self.screenHeight/1000.0)*self.verticalMiddlePromille)
        
        self.width=(self.screenWidth/1000.0)*self.horizontalSizePromille
        self.height=(self.screenHeight/1000.0)*self.verticalSizePromille
        
        self.top=self.verticalMiddle-self.height/2.0
        self.left=self.horizontalMiddle-self.width/2.0
        
        self.elipseRender = pygame.Surface((self.width, self.height),pygame.SRCALPHA)
        self.elipseRender.set_alpha(self.alphaValue)    
        #self.elipseRender.set_alpha(255)    
        widthBorder=int((self.screenHeight/1000.0)*self.widthBorder)
        #pygame.draw.arc(self.elipseRender, self.color, (0,0,self.width, self.height), self.beginArc, self.endArc, width=widthBorder)
        pygame.draw.ellipse(self.elipseRender, self.color, (0,0,self.width, self.height),width=widthBorder)
        #pygame.draw.rect(self.elipseRender,self.color,(0, 0, self.width, self.height), widthBorder,widthBorderBottomRight, widthBorderTopLeft, widthBorderTopRight, widthBorderBottomLeft )
            
        self.leftTop=(self.left, self.top)
        
    def resize(self, newSurface):
        self.blitToSurface=newSurface
        self.renderEllipse()
	    
    def updateOnScreen(self):
        if self.visible:
            self.blitToSurface.blit(self.elipseRender, self.leftTop)
        
class Square():
    def __init__(self, blitToSurface=None, gameState='', name='', color=(255,255,255,255), 
horizontalMiddlePromille=500, verticalMiddlePromille=500, horizontalSizePromille=100,  verticalSizePromille=400, 
widthBorder=0, borderTopLeft=1,borderTopRight=1,borderBottomLeft=1, borderBottomRight=1, 
alphaValue=255, visible=True):

        self.type='square'
        self.blitToSurface=blitToSurface
        self.gameState=gameState
        self.name=name
        self.color=color
        self.horizontalMiddlePromille=horizontalMiddlePromille
        self.verticalMiddlePromille=verticalMiddlePromille
        self.horizontalSizePromille=horizontalSizePromille
        self.verticalSizePromille=verticalSizePromille
        self.alphaValue=alphaValue
        self.widthBorder=widthBorder
        self.visible=visible
        self.borderBottomLeft=borderBottomLeft
        self.borderBottomRight=borderBottomRight
        self.borderTopLeft=borderTopLeft
        self.borderTopRight=borderTopRight
        
        self.renderSquare()        
    
    def renderSquare(self):
        self.screenWidth=self.blitToSurface.get_size()[0]
        self.screenHeight=self.blitToSurface.get_size()[1]
        
        self.horizontalMiddle=int((self.screenWidth/1000.0)*self.horizontalMiddlePromille)
        self.verticalMiddle=int((self.screenHeight/1000.0)*self.verticalMiddlePromille)
        
        self.width=(self.screenWidth/1000.0)*self.horizontalSizePromille
        self.height=(self.screenHeight/1000.0)*self.verticalSizePromille
        
        self.top=self.verticalMiddle-self.height/2.0
        self.left=self.horizontalMiddle-self.width/2.0
        
        self.squareRender = pygame.Surface((self.width, self.height),pygame.SRCALPHA)
        self.squareRender.set_alpha(self.alphaValue)    
        widthBorder=int((self.screenHeight/1000.0)*self.widthBorder)
        widthBorderBottomLeft=int((self.screenHeight/1000.0)*self.borderBottomLeft)
        widthBorderBottomRight=int((self.screenHeight/1000.0)*self.borderBottomRight)
        widthBorderTopLeft=int((self.screenHeight/1000.0)*self.borderTopLeft)
        widthBorderTopRight=int((self.screenHeight/1000.0)*self.borderTopRight)
        
        pygame.draw.rect(self.squareRender,self.color,(0, 0, self.width, self.height), widthBorder,widthBorderBottomRight, widthBorderTopLeft, widthBorderTopRight, widthBorderBottomLeft )
            
        self.leftTop=(self.left, self.top)
        
    def resize(self, newSurface):
        self.blitToSurface=newSurface
        self.renderSquare()
	    
    def updateOnScreen(self):
        if self.visible:
            self.blitToSurface.blit(self.squareRender, self.leftTop)

class Line():
    def __init__(self,blitToSurface=None, gameState='', name='', color=(255,255,255), 
startPosPromille=(0,0), endPosPromille=(1000,1000), widthLine=5, alphaValue=255, visible=True):

        self.type='line'
        self.blitToSurface=blitToSurface
        self.gameState=gameState
        self.name=name
        self.color=color
        self.startPosPromille=startPosPromille
        self.endPosPromille=endPosPromille
        self.widthLine=widthLine
        self.alphaValue=alphaValue
        self.visible=visible
       
        self.renderLine()
        
    def renderLine(self):
        screenWidth=self.blitToSurface.get_size()[0]
        screenHeight=self.blitToSurface.get_size()[1]
        
        startPosLeft=int((screenWidth/1000.0)*self.startPosPromille[0])
        startPosTop=int((screenHeight/1000.0)*self.startPosPromille[1])
        endPosLeft=int((screenWidth/1000.0)*self.endPosPromille[0])
        endPosTop=int((screenHeight/1000.0)*self.endPosPromille[1])
        
        startPos=(startPosLeft,startPosTop)
        endPos=(endPosLeft,endPosTop)
        widthLine=int((screenWidth/1000.0)*self.widthLine)
        self.lineRender = pygame.Surface((screenWidth, screenHeight),pygame.SRCALPHA)
        self.lineRender.set_alpha(self.alphaValue)    
        pygame.draw.line(self.lineRender, self.color, startPos, endPos, widthLine)
        
        
    def resize(self, newSurface):
        self.blitToSurface=newSurface
        self.renderLine()
	    
    def updateOnScreen(self):
        if self.visible:
            self.blitToSurface.blit(self.lineRender, (0,0))
            
class Label():
    def __init__(self, blitToSurface=None, gameState='', name='', text='', colorText=(255,255,255),
horizontalMiddlePromille=500, verticalMiddlePromille=500, sysFont=True, fontName='timesnewroman',
fontSizePromille=100, isBold=False, isItalic=False, antiAlias=True, alphaValue=255, visible=True, rotation=0):
        self.type='label'
        self.blitToSurface=blitToSurface
        self.gameState=gameState
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
        self.rotation=rotation
        
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
                if os.path.isdir('fonts') and os.path.isfile(os.path.join('fonts' , self.fontName)):
                    self.basicFont = pygame.font.Font(os.path.join('fonts' , self.fontName), self.fontSize) 
                else: # well, perhaps its inside the test suite?
                    parts=os.path.abspath(__file__+"/../..") # take the path this very py file is in now (os dependant!), and drop the last 2 items (the pygameElements name and folder it is in)
                    parts=os.path.join(parts , 'pygameElementsTest') # then, at that place, add the pygameElementsTest folder 
                    folder=os.path.join(parts , 'fonts') # inside that: there should be a fonts folder
                    fileLocation=os.path.join(folder , self.fontName) # adding the fontName required, should be the fileLocation
                    if os.path.isdir(folder) and os.path.isfile(fileLocation): # so if that folder exist: and the file exist as well
                        self.basicFont = pygame.font.Font(fileLocation, self.fontSize) # use it
                    else:   # ok give up, just take timesnewroman   
                        print (f'warning: could not find {self.fontName}') 
                        self.basicFont = pygame.font.SysFont('timesnewroman', self.fontSize, self.isBold, self.isItalic) 
    
    def renderText(self, text):
        self.text=text
        
        self.textRender= self.basicFont.render(self.text, self.antiAlias, self.colorText)
        alphaImage = pygame.Surface(self.textRender.get_size(), pygame.SRCALPHA)
        alphaImage.fill((255, 255, 255, self.alphaValue))
        self.textRender.blit(alphaImage, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        self.left=self.textRender.get_rect()[0]
        self.height=self.textRender.get_rect()[1]
        self.width=self.textRender.get_rect()[2]
        self.height=self.textRender.get_rect()[3]
        self.horizontalMiddle=int((self.screenWidth/1000.0)*self.horizontalMiddlePromille)
        self.verticalMiddle=int((self.screenHeight/1000.0)*self.verticalMiddlePromille)
        self.top=self.verticalMiddle-self.height/2.0
        self.left=self.horizontalMiddle-self.width/2.0
        self.leftTop=(int(self.horizontalMiddle-(self.width/2.0)),int(self.verticalMiddle-(self.height/2.0)))
        if self.rotation==0:
            self.leftTopRotated=self.leftTop
        else:
            self.textRender=pygame.transform.rotate(self.textRender, self.rotation) 
            self.surfaceRect=self.textRender.get_rect()
            self.extraWidthBecauseRotation=self.surfaceRect.w-self.width
            self.extraHeightBecauseRotation=self.surfaceRect.h-self.height
            self.leftAfterRotation=int(self.left-(self.extraWidthBecauseRotation/2.0))
            self.topAfterRotation=int(self.top-(self.extraHeightBecauseRotation/2.0))
            self.leftTopRotated=(self.leftAfterRotation,self.topAfterRotation)
            
    def resize(self, newSurface):
        self.blitToSurface=newSurface
        self.createFont()
        self.renderText(self.text)
	    
    def updateOnScreen(self):
        if self.visible:
            self.blitToSurface.blit(self.textRender, self.leftTopRotated)
	
    