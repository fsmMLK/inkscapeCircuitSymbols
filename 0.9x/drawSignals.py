#!/usr/bin/python

import os
import inkex
import inkscapeMadeEasy_Base as inkBase
import inkscapeMadeEasy_Draw as inkDraw
import math


class signal(inkBase.inkscapeMadeEasy):

  #---------------------------------------------
  def drawSignal(self,parent,position=[0, 0],label='GND',angleDeg=0,nodalVal='V_{cc}',drawLine=True):
    """ draws a Voltage node
    
    parent: parent object
    position: position [x,y]
    label: label of the object (it can be repeated)
    angleDeg: rotation angle in degrees counter-clockwise (default 0)
    nodalVal: name of the node (default: 'V_{cc}')
    drawLine: draws line for connection (default: True)
    """
    linestyleBlackFill=inkDraw.lineStyle.set(lineWidth=0.7,fillColor=inkDraw.color.defined('black'))
    group = self.createGroup(parent,label)
    elem = self.createGroup(group,label)
   
    inkDraw.circle.centerRadius(elem, position, 1.0, offset=[0,0],lineStyle=linestyleBlackFill)
    if drawLine: 
      inkDraw.line.relCoords(elem, [[0,10]],position)
      
    #text
    if abs(angleDeg)<=90:
      justif='bc'
      pos_text=[position[0],position[1]-self.textOffset]
    else:
      justif='tc'
      pos_text=[position[0],position[1]+self.textOffset]
        
    if not inkDraw.useLatex:
      value = nodalVal.replace('_','').replace('{','').replace('}','').replace(r'\volt','V')  # removes LaTeX stuff
    else:
      value = '$'+nodalVal+'$'
    temp=inkDraw.text.latex(self,group,value,pos_text,fontSize=self.fontSize,refPoint=justif,preambleFile=self.preambleFile)

    self.rotateElement(temp,position,-angleDeg)
    
    if angleDeg!=0:
      self.rotateElement(group,position,angleDeg)
      
    return group;

  #---------------------------------------------
  def drawDigital(self,parent,position=[0, 0],label='GPIO',angleDeg=0,nodalVal='GPIO'):
    """ draws a digital signal
    
    parent: parent object
    position: position [x,y]
    label: label of the object (it can be repeated)
    angleDeg: rotation angle in degrees counter-clockwise (default 0)
    nodalVal: name of the node (default: 'V_{cc}')
    """
    linestyleBlackFill=inkDraw.lineStyle.set(lineWidth=0.8)
    group = self.createGroup(parent,label)
    elem = self.createGroup(group,label)
   
    inkDraw.line.relCoords(elem, [[0,4],[25,0],[4,-4],[-4,-4],[-25,0],[0,4]],[position[0],position[1]],lineStyle=linestyleBlackFill)
      
    #text
    if not inkDraw.useLatex:
      value = nodalVal.replace('_','').replace('{','').replace('}','').replace(r'\volt','V')  # removes LaTeX stuff
    else:
      value = '$'+nodalVal+'$'
    temp=inkDraw.text.latex(self,group,value,[position[0]+2,position[1]],fontSize=self.fontSize,refPoint='cl',preambleFile=self.preambleFile)

    self.rotateElement(temp,position,-angleDeg)
    
    if angleDeg!=0:
      self.rotateElement(group,position,angleDeg)
      
    return group;
    
    
  #---------------------------------------------
  def drawGND(self,parent,position=[0, 0],label='GND',angleDeg=0):
    """ draws a GND
    
    parent: parent object
    position: position [x,y]
    label: label of the object (it can be repeated)
    angleDeg: rotation angle in degrees counter-clockwise (default 0)
    """

    group = self.createGroup(parent,label)
    elem = self.createGroup(group,label)
   
    inkDraw.line.relCoords(elem, [[0,10]],position)
    inkDraw.line.relCoords(elem, [[-14,0]],[position[0]+7,position[1]+10])
    inkDraw.line.relCoords(elem, [[-7,0]],[position[0]+3.5,position[1]+12])
    inkDraw.line.relCoords(elem, [[ -2,0]],[position[0]+1,position[1]+14])
           
    if angleDeg!=0:
      self.rotateElement(group,position,angleDeg)
      
    return group;
    
  #---------------------------------------------
  def drawCommon(self,parent,position=[0, 0],label='Common',angleDeg=0):
    """ draws a GND
    
    parent: parent object
    position: position [x,y]
    label: label of the object (it can be repeated)
    angleDeg: rotation angle in degrees counter-clockwise (default 0)
    """

    group = self.createGroup(parent,label)
    elem = self.createGroup(group,label)
   
    inkDraw.line.relCoords(elem, [[0,10]],position)
    inkDraw.line.relCoords(elem, [[-10,0],[5,5],[5,-5]],[position[0]+5,position[1]+10])
           
    if angleDeg!=0:
      self.rotateElement(group,position,angleDeg)
      
    return group;
