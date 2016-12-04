#!/usr/bin/python

import os
import inkex
import inkscapeMadeEasy_Base as inkBase
import inkscapeMadeEasy_Draw as inkDraw
import math

#some symbol definition

Ohm=u'\u2126'

# package needed:  steinmetz

def latexUnitMultiple(valueString):
  if valueString[-1]=='M':
    return valueString.replace('M',r'\si\mega')
    
  if valueString[-1]=='k':
    return valueString.replace('k',r'\si\kilo')
    
  if valueString[-1]=='m':
    return valueString.replace('m',r'\si\milli')
    
  if valueString[-1]=='u':
    return valueString.replace('u',r'\micro')
    
  if valueString[-1]=='p':
    return valueString.replace('p',r'\si\pico')
  
  return valueString

#---------------------------------------------
class CircuitSymbols(inkBase.inkscapeMadeEasy):
  def __init__(self):
    inkex.Effect.__init__(self)
    
    self.OptionParser.add_option("--tab",action="store", type="string",dest="tab", default="object") 
    
    self.OptionParser.add_option("--bipoleRLC",action="store", type="string",dest="bipoleRLC", default='none')
    self.OptionParser.add_option("--bipoleRLCVal", action="store", type="string", dest="bipoleRLCVal", default='Z') 
    self.OptionParser.add_option("--bipoleRLCUnit",action="store", type="inkbool",dest="bipoleRLCUnit", default=False)
    self.OptionParser.add_option("--bipoleRLCRot", action="store", type="string", dest="bipoleRLCRot", default='0') 
    self.OptionParser.add_option("--bipoleRLCVolt", action="store", type="inkbool", dest="bipoleRLCVolt", default=True) 
    self.OptionParser.add_option("--bipoleRLCCurr", action="store", type="inkbool", dest="bipoleRLCCurr", default=True)
    self.OptionParser.add_option("--bipoleRLCVoltName", action="store", type="string", dest="bipoleRLCVoltName", default='v') 
    self.OptionParser.add_option("--bipoleRLCCurrName", action="store", type="string", dest="bipoleRLCCurrName", default='i') 
    self.OptionParser.add_option("--bipoleRLCVoltCurrInvert", action="store", type="inkbool", dest="bipoleRLCVoltCurrInvert", default=True)
    
    self.OptionParser.add_option("--source",action="store", type="string",dest="source", default='none')
    self.OptionParser.add_option("--sourceVal", action="store", type="string", dest="sourceVal", default='E') 
    self.OptionParser.add_option("--sourceUnit",action="store", type="inkbool",dest="sourceUnit", default=False)
    self.OptionParser.add_option("--sourceRot", action="store", type="string", dest="sourceRot", default='0') 
    self.OptionParser.add_option("--sourceVolt", action="store", type="inkbool", dest="sourceVolt", default=True) 
    self.OptionParser.add_option("--sourceCurr", action="store", type="inkbool", dest="sourceCurr", default=True)
    self.OptionParser.add_option("--sourceVoltName", action="store", type="string", dest="sourceVoltName", default='v') 
    self.OptionParser.add_option("--sourceCurrName", action="store", type="string", dest="sourceCurrName", default='i') 
    self.OptionParser.add_option("--sourceVoltCurrInvert", action="store", type="inkbool", dest="sourceVoltCurrInvert", default=True)
    self.OptionParser.add_option("--sourceMirror", action="store", type="inkbool", dest="sourceMirror", default=False)
        
    self.OptionParser.add_option("--sourceControlled",action="store", type="string",dest="sourceControlled", default='none')
    self.OptionParser.add_option("--sourceControlledType",action="store", type="string",dest="sourceControlledType", default='curr')
    self.OptionParser.add_option("--sourceControlledGain", action="store", type="string", dest="sourceControlledGain", default='k')
    self.OptionParser.add_option("--sourceControlledControlName", action="store", type="string", dest="sourceControlledControlName", default='v_c')
    self.OptionParser.add_option("--sourceControlledRot", action="store", type="string", dest="sourceControlledRot", default='0') 
    self.OptionParser.add_option("--sourceControlledVolt", action="store", type="inkbool", dest="sourceControlledVolt", default=True) 
    self.OptionParser.add_option("--sourceControlledCurr", action="store", type="inkbool", dest="sourceControlledCurr", default=True)
    self.OptionParser.add_option("--sourceControlledVoltName", action="store", type="string", dest="sourceControlledVoltName", default='v') 
    self.OptionParser.add_option("--sourceControlledCurrName", action="store", type="string", dest="sourceControlledCurrName", default='i') 
    self.OptionParser.add_option("--sourceControlledVoltCurrInvert", action="store", type="inkbool", dest="sourceControlledVoltCurrInvert", default=True)
    self.OptionParser.add_option("--sourceControlledMirror", action="store", type="inkbool", dest="sourceControlledMirror", default=False)
    
    self.OptionParser.add_option("--switch",action="store", type="string",dest="switch", default='none')
    self.OptionParser.add_option("--switchVal", action="store", type="string", dest="switchVal", default='') 
    self.OptionParser.add_option("--switchFlagOpen", action="store", type="inkbool", dest="switchFlagOpen", default=True) 
    self.OptionParser.add_option("--switchOpenClose", action="store", type="inkbool", dest="switchOpenClose", default=True) 
    self.OptionParser.add_option("--switchOpenCloseText",action="store", type="string",dest="switchOpenCloseText", default='t_0')
    self.OptionParser.add_option("--switchRot", action="store", type="string", dest="switchRot", default=0) 

    self.OptionParser.add_option("--electr",action="store", type="string",dest="electr", default='none')
    self.OptionParser.add_option("--electrVal", action="store", type="string", dest="electrVal", default=None) 
    self.OptionParser.add_option("--electrRot", action="store", type="string", dest="electrRot", default='0') 
    self.OptionParser.add_option("--electrVolt", action="store", type="inkbool", dest="electrVolt", default=True) 
    self.OptionParser.add_option("--electrCurr", action="store", type="inkbool", dest="electrCurr", default=True)
    self.OptionParser.add_option("--electrVoltName", action="store", type="string", dest="electrVoltName", default='v') 
    self.OptionParser.add_option("--electrCurrName", action="store", type="string", dest="electrCurrName", default='i') 
    self.OptionParser.add_option("--electrVoltCurrInvert", action="store", type="inkbool", dest="electrVoltCurrInvert", default=True)
    
    self.OptionParser.add_option("--nodal",action="store", type="string",dest="nodal", default='none')
    self.OptionParser.add_option("--nodalVal", action="store", type="string", dest="nodalVal", default='E') 
    self.OptionParser.add_option("--nodalRot", action="store", type="float", dest="nodalRot", default=0)
    self.OptionParser.add_option("--nodalDrawLine", action="store", type="inkbool", dest="nodalDrawLine", default=False)
        
    self.OptionParser.add_option("--opamp",action="store", type="string",dest="opamp", default='none')
    self.OptionParser.add_option("--opampMirrorInput", action="store", type="inkbool", dest="opampMirrorInput", default=False) 
    self.OptionParser.add_option("--opampDrawVin", action="store", type="inkbool", dest="opampDrawVin", default=False)
    self.OptionParser.add_option("--opampDrawIin", action="store", type="inkbool", dest="opampDrawIin", default=False)
    self.OptionParser.add_option("--opampDrawVd", action="store", type="inkbool", dest="opampDrawVd", default=False)
    self.OptionParser.add_option("--opampDrawVout", action="store", type="inkbool", dest="opampDrawVout", default=False)
    self.OptionParser.add_option("--opampDrawIout", action="store", type="inkbool", dest="opampDrawIout", default=False)
    
    self.OptionParser.add_option("--opampFlagSupply", action="store", type="inkbool", dest="opampFlagSupply", default=False)
    self.OptionParser.add_option("--opampFlagSupplyValues", action="store", type="inkbool", dest="opampFlagSupplyValues", default=False)
    self.OptionParser.add_option("--opampSupplySymm", action="store", type="inkbool", dest="opampSupplySymm", default=True)
    self.OptionParser.add_option("--opampSupplyPositiveVal", action="store", type="string", dest="opampSupplyPositiveVal", default='+V_{cc}')
    self.OptionParser.add_option("--opampSupplyNegativeVal", action="store", type="string", dest="opampSupplyNegativeVal", default='-V_{cc}')
    self.OptionParser.add_option("--opampInputV+Name", action="store", type="string", dest="opampInputVPosName", default='v^+')
    self.OptionParser.add_option("--opampInputV-Name", action="store", type="string", dest="opampInputVNegName", default='v^-')
    self.OptionParser.add_option("--opampInputI+Name", action="store", type="string", dest="opampInputIPosName", default='v^+')
    self.OptionParser.add_option("--opampInputI-Name", action="store", type="string", dest="opampInputINegName", default='v^-')
    self.OptionParser.add_option("--opampVoutName", action="store", type="string", dest="opampVoutName", default='v_{out}')
    self.OptionParser.add_option("--opampIoutName", action="store", type="string", dest="opampIoutName", default='i_{out}')
    
    self.OptionParser.add_option("--opampInputDiffName", action="store", type="string", dest="opampInputDiffName", default='v_d')
    
    self.OptionParser.add_option("--arrow",action="store", type="string",dest="arrow", default='none')
    self.OptionParser.add_option("--arrowVal", action="store", type="string", dest="arrowVal", default='')     
    self.OptionParser.add_option("--arrowRot", action="store", type="string", dest="arrowRot", default='0') 
    self.OptionParser.add_option("--arrowInvert", action="store", type="inkbool", dest="arrowInvert", default=True)
    self.OptionParser.add_option("--arrowVSize",action="store", type="int",dest="arrowVSize", default=20)
    self.OptionParser.add_option("--arrowISize",action="store", type="int",dest="arrowISize", default=10)
    self.OptionParser.add_option("--arrowCurvaturDirection",action="store", type="inkbool",dest="arrowCurvaturDirection", default=True)

    self.OptionParser.add_option("--currColor", action="store", type="string", dest="currColor", default='#FF0000')
    self.OptionParser.add_option("--colorPickerCurrent", action="store", type="string", dest="colorPickerCurrent", default='0') 
        
    self.OptionParser.add_option("--voltColor", action="store", type="string", dest="voltColor", default='#217B21') 
    self.OptionParser.add_option("--colorPickerVolt", action="store", type="string", dest="colorPickerVolt", default='0') 
    
  def effect(self):
    
    so = self.options
    so.tab = so.tab.replace('"','')   # removes de exceding double quotes from the string
    
    #latex related preamble
    self.preambleFile=os.getcwd() + '/textextLib/CircuitSymbolsLatexPreamble.tex'
    
    #root_layer = self.current_layer
    root_layer = self.document.getroot()
    
    # text size and font style
    self.useLatex=True
    if self.useLatex:
      self.fontSize=5
      self.fontSizeSmall=4
    else:
      self.fontSize=8
      self.fontSizeSmall=5
      
    self.textOffset = self.fontSize/1.5  # offset between symbol and text
    self.textOffsetSmall = self.fontSizeSmall/2  # offset between symbol and text
    self.textStyle = inkDraw.textStyle.setSimpleBlack(self.fontSize,justification='center')
    self.textStyleSmall = inkDraw.textStyle.setSimpleBlack(self.fontSizeSmall,justification='center')
    
    # sets the position to the viewport center, round to next 10.
    position=[self.view_center[0],self.view_center[1]]
    position[0]=int(math.ceil(position[0] / 10.0)) * 10
    position[1]=int(math.ceil(position[1] / 10.0)) * 10

    [self.voltageColor,alpha]=inkDraw.color.parseColorPicker(so.voltColor,so.colorPickerVolt)
    [self.currentColor,alpha]=inkDraw.color.parseColorPicker(so.currColor,so.colorPickerCurrent)
    
        
    so.bipoleRLCRot=float(so.bipoleRLCRot)
    so.sourceRot=float(so.sourceRot)
    so.sourceControlledRot=float(so.sourceControlledRot)
    so.switchRot=float(so.switchRot)
    so.arrowRot=float(so.arrowRot)
    so.electrRot=float(so.electrRot)
    
    #---------------------------
    # RLC
    #---------------------------
    if so.tab=='RLC':
      
      if so.bipoleRLCUnit:
          so.bipoleRLCVal=latexUnitMultiple(so.bipoleRLCVal)
        
      if so.bipoleRLC=="genericBipole":
        if so.bipoleRLCUnit:
          so.bipoleRLCVal+=r'\si\ohm'
        self.drawBipoleGeneral(root_layer,position,value=so.bipoleRLCVal,angleDeg=so.bipoleRLCRot,
                              flagVolt=so.bipoleRLCVolt,voltName=so.bipoleRLCVoltName,flagCurr=so.bipoleRLCCurr,
                              currName=so.bipoleRLCCurrName,invertArrows=so.bipoleRLCVoltCurrInvert)
        
      if so.bipoleRLC=="resistor":
        if so.bipoleRLCUnit:
          so.bipoleRLCVal+=r'\si\ohm'
        self.drawResistor(root_layer,position,value=so.bipoleRLCVal,angleDeg=so.bipoleRLCRot,
                          flagVolt=so.bipoleRLCVolt,voltName=so.bipoleRLCVoltName,flagCurr=so.bipoleRLCCurr,
                          currName=so.bipoleRLCCurrName,invertArrows=so.bipoleRLCVoltCurrInvert)
        
      if so.bipoleRLC=="capacitor":
        if so.bipoleRLCUnit:
          so.bipoleRLCVal+=r'\si\farad'
        self.drawCapacitor(root_layer,position,value=so.bipoleRLCVal,flagPol=False,angleDeg=so.bipoleRLCRot,
                          flagVolt=so.bipoleRLCVolt,voltName=so.bipoleRLCVoltName,flagCurr=so.bipoleRLCCurr,
                          currName=so.bipoleRLCCurrName,invertArrows=so.bipoleRLCVoltCurrInvert)
        
      if so.bipoleRLC=="capacitorPol":
        if so.bipoleRLCUnit:
          so.bipoleRLCVal+=r'\si\farad'
        self.drawCapacitor(root_layer,position,value=so.bipoleRLCVal,flagPol=True,angleDeg=so.bipoleRLCRot,
                          flagVolt=so.bipoleRLCVolt,voltName=so.bipoleRLCVoltName,flagCurr=so.bipoleRLCCurr,
                          currName=so.bipoleRLCCurrName,invertArrows=so.bipoleRLCVoltCurrInvert)

      if so.bipoleRLC=="inductor":
        if so.bipoleRLCUnit:
          so.bipoleRLCVal+=r'\si\henry'
        self.drawInductor(root_layer,position,value=so.bipoleRLCVal,angleDeg=so.bipoleRLCRot,
                          flagVolt=so.bipoleRLCVolt,voltName=so.bipoleRLCVoltName,flagCurr=so.bipoleRLCCurr,
                          currName=so.bipoleRLCCurrName,invertArrows=so.bipoleRLCVoltCurrInvert)
                            
    #---------------------------
    # independendent sources
    #---------------------------
    if so.tab=='Indep. Source':
      
      if so.sourceUnit:
          so.sourceVal=latexUnitMultiple(so.sourceVal)
                
      if so.source=="voltIndepDC":
        if so.sourceUnit:
          so.sourceVal+=r'\si\volt'
        self.drawSourceVDC(root_layer,position,value=so.sourceVal,angleDeg=so.sourceRot,
                          flagVolt=so.sourceVolt,flagCurr=so.sourceCurr,
                          currName=so.sourceCurrName,invertArrows=so.sourceVoltCurrInvert,mirror=so.sourceMirror)
                                        
      if so.source=="voltIndepDCbattery":
        if so.sourceUnit:
          so.sourceVal+=r'\si\volt'
        self.drawSourceVDCbattery(root_layer,position,value=so.sourceVal,angleDeg=so.sourceRot,
                                flagVolt=so.sourceVolt,flagCurr=so.sourceCurr,
                                currName=so.sourceCurrName,invertArrows=so.sourceVoltCurrInvert,mirror=so.sourceMirror)

      if so.source=="voltIndep":
        if so.sourceUnit:
          so.sourceVal+=r'\si\volt'
        self.drawSourceV(root_layer,position,value=so.sourceVal,angleDeg=so.sourceRot,
                        flagVolt=so.sourceVolt,flagCurr=so.sourceCurr,
                        currName=so.sourceCurrName,invertArrows=so.sourceVoltCurrInvert,mirror=so.sourceMirror)
                                    
      if so.source=="voltIndepSinusoidal":
        if so.sourceUnit:
          so.sourceVal+=r'\si\volt'
        self.drawSourceVSinusoidal(root_layer,position,value=so.sourceVal,angleDeg=so.sourceRot,
                                    flagVolt=so.sourceVolt,flagCurr=so.sourceCurr,
                                    currName=so.sourceCurrName,invertArrows=so.sourceVoltCurrInvert,mirror=so.sourceMirror)
                                    
      if so.source=="currIndep":
        if so.sourceUnit:
          so.sourceVal+=r'\si\ampere'
        self.drawSourceI(root_layer,position,value=so.sourceVal,angleDeg=so.sourceRot,
                          flagVolt=so.sourceVolt,flagCurr=so.sourceCurr,
                          voltName=so.sourceVoltName,invertArrows=so.sourceVoltCurrInvert,mirror=so.sourceMirror)
          
    # --------------------------
    # controlled sources
    #---------------------------
    if so.tab=='Dep. Source':
      
      if so.sourceControlled=="volt":
        self.drawControledSourceV(root_layer,position,controlType=so.sourceControlledType,gain=so.sourceControlledGain,
                                  controlName=so.sourceControlledControlName,angleDeg=so.sourceControlledRot,
                                  flagVolt=so.sourceControlledVolt,flagCurr=so.sourceControlledCurr,currName=so.sourceControlledCurrName,
                                  invertArrows=so.sourceControlledVoltCurrInvert,mirror=so.sourceControlledMirror)             

      if so.sourceControlled=="curr":
        self.drawControledSourceI(root_layer,position,controlType=so.sourceControlledType,gain=so.sourceControlledGain,
                                  controlName=so.sourceControlledControlName,angleDeg=so.sourceControlledRot,
                                  flagVolt=so.sourceControlledVolt,flagCurr=so.sourceControlledCurr,voltName=so.sourceControlledVoltName,
                                  invertArrows=so.sourceControlledVoltCurrInvert,mirror=so.sourceControlledMirror)             
                                                    
    #---------------------------
    # switches
    #---------------------------
    if so.tab=='Switches':
      if so.switch=="switch2T":
        self.drawSwitch2T(root_layer,position,value=so.switchVal,angleDeg=so.switchRot,
                          flagOpen=so.switchFlagOpen,flagDrawArrow=so.switchOpenClose,
                          OpenCloseText=so.switchOpenCloseText)
                                                  
    #---------------------------
    # electronics
    #---------------------------
    if so.tab=='Semiconductor':
      if so.electr=="diode" or so.electr=="LED" or so.electr=="photoDiode":
        self.drawDiode(root_layer,position,value=so.electrVal,angleDeg=so.electrRot,
                      flagVolt=so.electrVolt,voltName=so.electrVoltName,flagCurr=so.electrCurr,
                      currName=so.electrCurrName,invertArrows=not so.electrVoltCurrInvert,flagType=so.electr)  
      
    # --------------------------
    # operational amplifiers
    #---------------------------
    if so.tab=='Opamp':
      if so.opamp=="general":
        opamp_elem=self.drawOpAmpGeneral(root_layer,position,mirrorInput=so.opampMirrorInput,
                                        opampDrawVin=so.opampDrawVin,opampDrawIin=so.opampDrawIin,
                                        opampDrawVd=so.opampDrawVd,opampDrawVout=so.opampDrawVout,opampDrawIout=so.opampDrawIout,
                                        opampInputVPosName=so.opampInputVPosName,opampInputVNegName=so.opampInputVNegName,
                                        opampInputIPosName=so.opampInputIPosName,opampInputINegName=so.opampInputINegName,
                                        opampVoutName=so.opampVoutName,opampIoutName=so.opampIoutName,
                                        opampInputDiffName=so.opampInputDiffName,
                                        flagDrawSupply=so.opampFlagSupply,opampFlagSupplyValues=so.opampFlagSupplyValues,
                                        flagSupplySymm=so.opampSupplySymm,supplyPositiveVal=so.opampSupplyPositiveVal,
                                        supplyNegativeVal=so.opampSupplyNegativeVal)             
                                
    # --------------------------
    # Nodes
    #---------------------------
    if so.tab=='Signals':
      
      if so.nodal=="GND":
        self.drawGND(root_layer,position,angleDeg=so.nodalRot)
        return
      
      if so.nodal=="common":
        self.drawCommon(root_layer,position,angleDeg=so.nodalRot)
        return
      
      if so.nodal=="custom":
        text=so.nodalVal
        
      if so.nodal=="+vcc":
        text='+V_{cc}'
        
      if so.nodal=="-vcc":
        text='-V_{cc}'
        
      if so.nodal=="+5V":
        text=r'+5\volt'
        
      if so.nodal=="-5V":
        text=r'-5\volt'
        
      if so.nodal=="+15V":
        text=r'+15\volt'
        
      if so.nodal=="-15V":
        text=r'-15\volt'
                  
      if so.nodal=="v_in":
        text=r'v_{in}'
        
      if so.nodal=="v_out":
        text=r'v_{out}'
      
      self.drawV(root_layer,position,angleDeg=so.nodalRot,nodalVal=text,drawLine=so.nodalDrawLine)
      return
      
    # --------------------------
    # Arrows
    #---------------------------   
    if so.tab=='Arrow':           
 
      if so.arrow=="voltage":
          self.drawVoltArrowSimple(root_layer,position,name=so.arrowVal,color=self.voltageColor,
                                              angleDeg=so.arrowRot,invertArrows=so.arrowInvert,size=so.arrowVSize,
                                              invertCurvatureDirection=so.arrowCurvaturDirection)

      if so.arrow=="current":
          self.drawCurrArrowSimple(root_layer,position,name=so.arrowVal,color=self.voltageColor,
                                              angleDeg=so.arrowRot,invertArrows=so.arrowInvert,size=so.arrowISize,
                                              invertTextSide=so.arrowCurvaturDirection)
          
  #---------------------------------------------
  def drawBipoleGeneral(self,parent,position=[0, 0],value='Z',label='Bipole',angleDeg=0,
                        flagVolt=True,voltName='v',flagCurr=True,currName='i',invertArrows=False):
    """ draws a generic bipole with a rectangle
    
    parent: parent object
    position: position [x,y]
    value: string with resistor value. (default 'Z')
    
    label: label of the object (it can be repeated)
    angleDeg: rotation angle in degrees counter-clockwise (default 0)
    flagVolt: indicates whether the voltage arrow must be drawn (default: true)
    voltName: voltage drop name (default: v)
    flagCurr: indicates whether the current arrow must be drawn (default: true)
    currName: current drop name (default: i)
    """
      
    group = self.createGroup(parent,label)
    elem = self.createGroup(group)

    inkDraw.line.relCoords(elem, [[15.5,0]],position)
    inkDraw.line.relCoords(elem, [[19,0],[0,-6],[-19,0],[0,6]],[position[0]+15.5,position[1]+3])
    inkDraw.line.relCoords(elem, [[15.5,0]],[position[0]+34.5,position[1]])
      
    pos_text=[position[0]+25,position[1]-3-self.textOffset]
    if self.useLatex:
      inkDraw.text.latex(self,group,'$'+value+'$',pos_text,fontSize=self.fontSize,refPoint='bc',preambleFile=self.preambleFile)
    else:
      inkDraw.text.write(self,value,pos_text,group,self.textStyle)
      
    if angleDeg!=0:
      self.rotateElement(group,position,angleDeg)
    
    if flagVolt:
      self.drawVoltArrow(group,[position[0]+25 ,position[1]+5],name=voltName,color=self.voltageColor,angleDeg=angleDeg,invertArrows=not invertArrows)
      
    if flagCurr:
      self.drawCurrArrow(group,[position[0]+40 ,position[1]-5],name=currName,color=self.currentColor,angleDeg=angleDeg,invertArrows=invertArrows)
      
    return group;
      
  #---------------------------------------------
  def drawResistor(self,parent,position=[0, 0],value='R',label='Resistor',angleDeg=0,
                   flagVolt=True,voltName='v',flagCurr=True,currName='i',invertArrows=False):
    """ draws a resistor
    
    parent: parent object
    position: position [x,y]
    value: string with resistor value. If it ends with 'ohm', 'OHM' or 'Ohm', proper Ohm symbol will be added. (Default 'R')
    
    label: label of the object (it can be repeated)
    angleDeg: rotation angle in degrees counter-clockwise (default 0)
    flagVolt: indicates whether the voltage arrow must be drawn (default: true)
    voltName: voltage drop name (default: v)
    flagCurr: indicates whether the current arrow must be drawn (default: true)
    currName: current drop name (default: i)
    """
    
    if not self.useLatex:
      if value[-3:]=='ohm' or value[-3:]=='OHM' or value[-3:]=='Ohm':
        textValue= value[0:-3] + Ohm
      else:
        textValue= value
      
    group = self.createGroup(parent,label)
    elem = self.createGroup(group)
    
    inkDraw.line.relCoords(elem, [[15.5,0],[2,3],[3,-6],[3,6],[3,-6],[3,6],[3,-6],[2,3],[15.5,0]],position)
      
    pos_text=[position[0]+25,position[1]-3-self.textOffset]
    if self.useLatex:
      inkDraw.text.latex(self,group,'$'+value+'$',pos_text,fontSize=self.fontSize,refPoint='bc',preambleFile=self.preambleFile)
    else:
      inkDraw.text.write(self,textValue,pos_text,group,self.textStyle)

    if angleDeg!=0:
      self.rotateElement(group,position,angleDeg)
    
    if flagVolt:
      self.drawVoltArrow(group,[position[0]+25 ,position[1]+5],name=voltName,color=self.voltageColor,angleDeg=angleDeg,invertArrows=not invertArrows)
      
    if flagCurr:
      self.drawCurrArrow(group,[position[0]+40 ,position[1]-5],name=currName,color=self.currentColor,angleDeg=angleDeg,invertArrows=invertArrows)
      
    return group;
    
  #---------------------------------------------
  def drawCapacitor(self,parent,position=[0, 0],value='C',label='Capacitor',flagPol=False,angleDeg=0,
                    flagVolt=True,voltName='v',flagCurr=True,currName='i',invertArrows=False):
    """ draws a capacitor
    
    parent: parent object
    position: position [x,y]
    value: string with value.    
    label: label of the object (it can be repeated)
    flagPol: draw sign for polarized capacitor
    angleDeg: rotation angle in degrees counter-clockwise (default 0)
    flagVolt: indicates whether the voltage arrow must be drawn (default: true)
    voltName: voltage drop name (default: v)
    flagCurr: indicates whether the current arrow must be drawn (default: true)
    currName: current drop name (default: i)
    """

    group = self.createGroup(parent,label)
    elem = self.createGroup(group,label)
   
    inkDraw.line.relCoords(elem, [[23,0]],position)
    inkDraw.line.relCoords(elem, [[-23,0]],[position[0]+50,position[1]])
    inkDraw.line.relCoords(elem, [[0,-14]],[position[0]+23,position[1]+7])
    inkDraw.line.relCoords(elem, [[0,-14]],[position[0]+27,position[1]+7])
    
    pos_text=[position[0]+25,position[1]-8-self.textOffset]
    if self.useLatex:
      inkDraw.text.latex(self,group,'$'+value+'$',pos_text,fontSize=self.fontSize,refPoint='bc',preambleFile=self.preambleFile)
    else:
      inkDraw.text.write(self,value,pos_text,group,self.textStyle)
      
    if flagPol:
      inkDraw.text.write(self,'+',[position[0]+31,position[1]-3],group,self.textStyle,fontSize=5)

    if angleDeg!=0:
      self.rotateElement(group,position,angleDeg)
    
    if flagVolt:
      self.drawVoltArrow(group,[position[0]+25 ,position[1]+9],name=voltName,color=self.voltageColor,angleDeg=angleDeg,invertArrows=not invertArrows)
      
    if flagCurr:
      self.drawCurrArrow(group,[position[0]+40 ,position[1]-5],name=currName,color=self.currentColor,angleDeg=angleDeg,invertArrows=invertArrows)
      
    return group;
    
  #---------------------------------------------
  def drawInductor(self,parent,position=[0, 0],value='L',label='Inductro',angleDeg=0,
                   flagVolt=True,voltName='v',flagCurr=True,currName='i',invertArrows=False):
    """ draws an inductor
    
    parent: parent object
    position: position [x,y]
    value: string with resistor value. If it ends with 'ohm', 'OHM' or 'Ohm', proper Ohm symbol will be added. (Default 'R')
    
    label: label of the object (it can be repeated)
    angleDeg: rotation angle in degrees counter-clockwise (default 0)
    flagVolt: indicates whether the voltage arrow must be drawn (default: true)
    voltName: voltage drop name (default: v)
    flagCurr: indicates whether the current arrow must be drawn (default: true)
    currName: current drop name (default: i)
    """
    
    if not self.useLatex:
      if value[-3:]=='ohm' or value[-3:]=='OHM' or value[-3:]=='Ohm':
        textValue= value[0:-3] + Ohm
      else:
        textValue= value
      
    group = self.createGroup(parent,label)
    elem = self.createGroup(group,label)
    
    inkDraw.line.relCoords(elem, [[13,0]],position)
    inkDraw.line.relCoords(elem, [[-13,0]],[position[0]+50,position[1]])
    
    inkDraw.arc.centerAngStartAngEnd(elem,[position[0]+16,position[1]], 3.0,0.0,180.0,[0,0],flagOpen=True,largeArc=False)   
    inkDraw.arc.centerAngStartAngEnd(elem,[position[0]+22,position[1]], 3.0,0.0,180.0,[0,0],flagOpen=True,largeArc=False)  
    inkDraw.arc.centerAngStartAngEnd(elem,[position[0]+28,position[1]], 3.0,0.0,180.0,[0,0],flagOpen=True,largeArc=False)  
    inkDraw.arc.centerAngStartAngEnd(elem,[position[0]+34,position[1]], 3.0,0.0,180.0,[0,0],flagOpen=True,largeArc=False)  
    
    pos_text=[position[0]+25,position[1]-self.textOffset]
    if self.useLatex:
      inkDraw.text.latex(self,group,'$'+value+'$',pos_text,fontSize=self.fontSize,refPoint='bc',preambleFile=self.preambleFile)
    else:
      inkDraw.text.write(self,textValue,pos_text,group,self.textStyle)

    if angleDeg!=0:
      self.rotateElement(group,position,angleDeg)
    
    if flagVolt:
      self.drawVoltArrow(group,[position[0]+25 ,position[1]+5],name=voltName,color=self.voltageColor,angleDeg=angleDeg,invertArrows=not invertArrows)
      
    if flagCurr:
      self.drawCurrArrow(group,[position[0]+40 ,position[1]-5],name=currName,color=self.currentColor,angleDeg=angleDeg,invertArrows=invertArrows)
      
    return group;

  #---------------------------------------------
  def drawDiode(self,parent,position=[0, 0],value='D',label='diode',angleDeg=0,
                flagVolt=True,voltName='v',flagCurr=True,currName='i',invertArrows=False,flagType='diode'):
    """ draws a diode
    
    parent: parent object
    position: position [x,y]
    value: string with resistor value. (default 'D')
    
    label: label of the object (it can be repeated)
    angleDeg: rotation angle in degrees counter-clockwise (default 0)
    flagVolt: indicates whether the voltage arrow must be drawn (default: true)
    voltName: voltage drop name (default: v)
    flagCurr: indicates whether the current arrow must be drawn (default: true)
    currName: current drop name (default: i)]
    flagType: tipe of element: available types:  'diode', 'LED', 'photoDiode' (default: diode)
    """
      
    group = self.createGroup(parent,label)
    elem = self.createGroup(group)

    inkDraw.line.relCoords(elem, [[19,0]],position)
    inkDraw.line.relCoords(elem, [[-12,6],[0,-12],[12,6]],[position[0]+31,position[1]])
    inkDraw.line.relCoords(elem, [[19,0]],[position[0]+31,position[1]])
    inkDraw.line.relCoords(elem, [[0,12]],[position[0]+31,position[1]-6])
      
    if value!=None:
      
      if flagType=='LED':
        pos_text=[position[0]+25,position[1]-13-self.textOffset]
      if flagType=='photoDiode':
        pos_text=[position[0]+25,position[1]-13-self.textOffset]
      if flagType=='diode':
        pos_text=[position[0]+25,position[1]-6-self.textOffset]
      
      
      if self.useLatex:
        inkDraw.text.latex(self,group,'$'+value+'$',pos_text,fontSize=self.fontSize,refPoint='bc',preambleFile=self.preambleFile)
      else:
        inkDraw.text.write(self,value,pos_text,group,self.textStyle)
      
    if angleDeg!=0:
      self.rotateElement(group,position,angleDeg)
    
    if flagVolt:
      self.drawVoltArrow(group,[position[0]+25 ,position[1]+7],name=voltName,color=self.voltageColor,angleDeg=angleDeg,invertArrows=not invertArrows)
      
    if flagCurr:
      self.drawCurrArrow(group,[position[0]+40 ,position[1]-5],name=currName,color=self.currentColor,angleDeg=angleDeg,invertArrows=invertArrows)
    
    if flagType=='LED':
      arrow = self.createGroup(elem)
      inkDraw.line.relCoords(arrow, [[7,0]],position)
      inkDraw.line.relCoords(arrow, [[1.5,-1.5],[-1.5,-1.5]],[position[0]+5.5,position[1]+1.5])
      self.rotateElement(arrow,position,60)
      self.moveElement(arrow,[22,-8])
      arrow = self.createGroup(elem)
      inkDraw.line.relCoords(arrow, [[7,0]],position)
      inkDraw.line.relCoords(arrow, [[1.5,-1.5],[-1.5,-1.5]],[position[0]+5.5,position[1]+1.5])
      self.rotateElement(arrow,position,60)
      self.moveElement(arrow,[27,-6])
      
    if flagType=='photoDiode':
      arrow = self.createGroup(elem)
      inkDraw.line.relCoords(arrow, [[7,0]],position)
      inkDraw.line.relCoords(arrow, [[1.5,-1.5],[-1.5,-1.5]],[position[0]+5.5,position[1]+1.5])
      self.rotateElement(arrow,position,-120)
      self.moveElement(arrow,[25,-14])
      arrow = self.createGroup(elem)
      inkDraw.line.relCoords(arrow, [[7,0]],position)
      inkDraw.line.relCoords(arrow, [[1.5,-1.5],[-1.5,-1.5]],[position[0]+5.5,position[1]+1.5])
      self.rotateElement(arrow,position,-120)
      self.moveElement(arrow,[30,-12])
    return group;
  
  #---------------------------------------------
  def drawSourceV(self,parent,position=[0, 0],value='v(t)',label='Source',angleDeg=0,
                    flagVolt=True,flagCurr=True,currName='i',invertArrows=False,mirror=False):
    """ draws a independend general voltage source
    
    parent: parent object
    position: position [x,y]
    value: string with value.    
    label: label of the object (it can be repeated)
    angleDeg: rotation angle in degrees counter-clockwise (default 0)
    flagVolt: indicates whether the voltage arrow must be drawn (default: true)
    flagCurr: indicates whether the current arrow must be drawn (default: true)
    currName: current drop name (default: i)
    mirror: mirror source drawing (default: False)
    """

    group = self.createGroup(parent,label)
    elem = self.createGroup(group,label)
   
    inkDraw.line.relCoords(elem, [[18,0]],position)
    inkDraw.line.relCoords(elem, [[-18,0]],[position[0]+50,position[1]])
    inkDraw.circle.centerRadius(elem, [25,0],7.0,offset=position, label='circle')
    
    #signs
    lineStyleSign=inkDraw.lineStyle.setSimpleBlack(lineWidth=0.6)
    if mirror:
      inkDraw.line.relCoords(elem, [[-2,0]],[position[0]+22,position[1]],lineStyle=lineStyleSign)
      inkDraw.line.relCoords(elem, [[0,2]],[position[0]+21,position[1]-1],lineStyle=lineStyleSign)
      inkDraw.line.relCoords(elem, [[0,2]],[position[0]+29,position[1]-1],lineStyle=lineStyleSign)
    else:
      inkDraw.line.relCoords(elem, [[-2,0]],[position[0]+30,position[1]],lineStyle=lineStyleSign)
      inkDraw.line.relCoords(elem, [[0,2]],[position[0]+29,position[1]-1],lineStyle=lineStyleSign)
      inkDraw.line.relCoords(elem, [[0,2]],[position[0]+21,position[1]-1],lineStyle=lineStyleSign)
    
    
    pos_text=[position[0]+25,position[1]-8-self.textOffset]
    if self.useLatex:
      inkDraw.text.latex(self,group,'$'+value+'$',pos_text,fontSize=self.fontSize,refPoint='bc',preambleFile=self.preambleFile)
    else:
      inkDraw.text.write(self,value,pos_text,group,self.textStyle)
           
    if angleDeg!=0:
      self.rotateElement(group,position,angleDeg)
    
    if flagVolt:
      self.drawVoltArrow(group,[position[0]+25 ,position[1]+8],name=value,color=self.voltageColor,angleDeg=angleDeg,invertArrows=not mirror)
      
    if flagCurr:
      self.drawCurrArrow(group,[position[0]+40 ,position[1]-5],name=currName,color=self.currentColor,angleDeg=angleDeg,invertArrows=(invertArrows== mirror))
      
    return group;
    
  #---------------------------------------------
  def drawSourceVSinusoidal(self,parent,position=[0, 0],value='v(t)',label='Source',angleDeg=0,
                    flagVolt=True,flagCurr=True,currName='i',invertArrows=False,mirror=False):
    """ draws a independend sinusoidal voltage source
    
    parent: parent object
    position: position [x,y]
    value: string with value.    
    label: label of the object (it can be repeated)
    angleDeg: rotation angle in degrees counter-clockwise (default 0)
    flagVolt: indicates whether the voltage arrow must be drawn (default: true)
    flagCurr: indicates whether the current arrow must be drawn (default: true)
    currName: current drop name (default: i)
    mirror: mirror source drawing (default: False)
    """

    group = self.createGroup(parent,label)
    elem = self.createGroup(group,label)
   
    inkDraw.line.relCoords(elem, [[18,0]],position)
    inkDraw.line.relCoords(elem, [[-18,0]],[position[0]+50,position[1]])
    inkDraw.circle.centerRadius(elem, [25,0],7.0,offset=position, label='circle')
    
    #signs
    sine = self.createGroup(elem)
    lineStyleSign=inkDraw.lineStyle.setSimpleBlack(lineWidth=0.6)
    
    inkDraw.arc.startEndRadius(sine,[position[0]+20,position[1]], [position[0]+25,position[1]], 2.6, [0,0], lineStyle=lineStyleSign,flagRightOf=True,flagOpen=True,largeArc=False)
    inkDraw.arc.startEndRadius(sine,[position[0]+30,position[1]], [position[0]+25,position[1]], 2.6, [0,0], lineStyle=lineStyleSign,flagRightOf=True,flagOpen=True,largeArc=False)
    self.rotateElement(sine,[position[0]+25,position[1]],-angleDeg)
    
    if mirror:
      inkDraw.line.relCoords(elem, [[-2,0]],[position[0]+16,position[1]-4],lineStyle=lineStyleSign)
      inkDraw.line.relCoords(elem, [[0,2]],[position[0]+15,position[1]-5],lineStyle=lineStyleSign)
      inkDraw.line.relCoords(elem, [[0,2]],[position[0]+35,position[1]-5],lineStyle=lineStyleSign)
    else:
      inkDraw.line.relCoords(elem, [[-2,0]],[position[0]+36,position[1]-4],lineStyle=lineStyleSign)
      inkDraw.line.relCoords(elem, [[0,2]],[position[0]+35,position[1]-5],lineStyle=lineStyleSign)
      inkDraw.line.relCoords(elem, [[0,2]],[position[0]+15,position[1]-5],lineStyle=lineStyleSign)
      
    
    pos_text=[position[0]+25,position[1]-8-self.textOffset]
    if self.useLatex:
      inkDraw.text.latex(self,group,'$'+value+'$',pos_text,fontSize=self.fontSize,refPoint='bc',preambleFile=self.preambleFile)
    else:
      inkDraw.text.write(self,value,pos_text,group,self.textStyle)
           
    if angleDeg!=0:
      self.rotateElement(group,position,angleDeg)
    
    if flagVolt:
      self.drawVoltArrow(group,[position[0]+25 ,position[1]+8],name=value,color=self.voltageColor,angleDeg=angleDeg,invertArrows=not mirror)
      
    if flagCurr:
      self.drawCurrArrow(group,[position[0]+40 ,position[1]-5],name=currName,color=self.currentColor,angleDeg=angleDeg,invertArrows=(invertArrows== mirror))
      
    return group;

  #---------------------------------------------
  def drawSourceVDC(self,parent,position=[0, 0],value='V',label='Source',angleDeg=0,
                    flagVolt=True,flagCurr=True,currName='i',invertArrows=False,mirror=False):
    """ draws a DC voltage source
    
    parent: parent object
    position: position [x,y]
    value: string with value.    
    label: label of the object (it can be repeated)
    angleDeg: rotation angle in degrees counter-clockwise (default 0)
    flagVolt: indicates whether the voltage arrow must be drawn (default: true)
    flagCurr: indicates whether the current arrow must be drawn (default: true)
    currName: output current drop name (default: i)
    mirror: mirror source drawing (default: False)
    """

    group = self.createGroup(parent,label)
    elem = self.createGroup(group,label)
   
    inkDraw.line.relCoords(elem, [[24,0]],position)
    inkDraw.line.relCoords(elem, [[-23,0]],[position[0]+50,position[1]])
    
    #draw source
    lineStyleSign=inkDraw.lineStyle.setSimpleBlack(lineWidth=0.6)
    if mirror:
      inkDraw.line.relCoords(elem, [[-2,0]],[position[0]+21,position[1]-4],lineStyle=lineStyleSign)
      inkDraw.line.relCoords(elem, [[0,2]],[position[0]+20,position[1]-5],lineStyle=lineStyleSign)
      inkDraw.line.relCoords(elem, [[0,2]],[position[0]+30,position[1]-5],lineStyle=lineStyleSign)
      inkDraw.line.relCoords(elem, [[0,-6]],[position[0]+27,position[1]+3])
      inkDraw.line.relCoords(elem, [[0,-14]],[position[0]+24,position[1]+7])
    else:
      inkDraw.line.relCoords(elem, [[-2,0]],[position[0]+31,position[1]-4],lineStyle=lineStyleSign)
      inkDraw.line.relCoords(elem, [[0,2]],[position[0]+30,position[1]-5],lineStyle=lineStyleSign)
      inkDraw.line.relCoords(elem, [[0,2]],[position[0]+21,position[1]-5],lineStyle=lineStyleSign)
      inkDraw.line.relCoords(elem, [[0,-6]],[position[0]+24,position[1]+3])
      inkDraw.line.relCoords(elem, [[0,-14]],[position[0]+27,position[1]+7])
    
    pos_text=[position[0]+25,position[1]-8-self.textOffset]
    if self.useLatex:
      inkDraw.text.latex(self,group,'$'+value+'$',pos_text,fontSize=self.fontSize,refPoint='bc',preambleFile=self.preambleFile)
    else:
      inkDraw.text.write(self,value,pos_text,group,self.textStyle)
    

    
    if angleDeg!=0:
      self.rotateElement(group,position,angleDeg)
    
    if flagVolt:
      self.drawVoltArrow(group,[position[0]+25 ,position[1]+8],name=value,color=self.voltageColor,angleDeg=angleDeg,invertArrows=not mirror)
      
    if flagCurr:
      self.drawCurrArrow(group,[position[0]+40 ,position[1]-5],name=currName,color=self.currentColor,angleDeg=angleDeg,invertArrows=(invertArrows== mirror))
      
    return group;
    
    #---------------------------------------------
  def drawSourceVDCbattery(self,parent,position=[0, 0],value='V',label='Source',angleDeg=0,
                    flagVolt=True,flagCurr=True,currName='i',invertArrows=False,mirror=False):
    """ draws a DC battery  source
    
    parent: parent object
    position: position [x,y]
    value: string with value.    
    label: label of the object (it can be repeated)
    angleDeg: rotation angle in degrees counter-clockwise (default 0)
    flagVolt: indicates whether the voltage arrow must be drawn (default: true)
    flagCurr: indicates whether the current arrow must be drawn (default: true)
    currName: output current drop name (default: i)
    mirror: mirror source drawing (default: False)
    """

    group = self.createGroup(parent,label)
    elem = self.createGroup(group,label)
   
    inkDraw.line.relCoords(elem, [[18,0]],position)
    inkDraw.line.relCoords(elem, [[-17,0]],[position[0]+50,position[1]])
    
    #draw source
        
    lineStyleSign=inkDraw.lineStyle.setSimpleBlack(lineWidth=0.6)
    if mirror:
      inkDraw.line.relCoords(elem, [[-2,0]],[position[0]+16,position[1]-4],lineStyle=lineStyleSign)
      inkDraw.line.relCoords(elem, [[0,2]],[position[0]+15,position[1]-5],lineStyle=lineStyleSign)
      inkDraw.line.relCoords(elem, [[0,2]],[position[0]+36,position[1]-5],lineStyle=lineStyleSign)
      inkDraw.line.relCoords(elem, [[0,-6]],[position[0]+33,position[1]+3])
      inkDraw.line.relCoords(elem, [[0,-14]],[position[0]+30,position[1]+7])
      inkDraw.line.relCoords(elem, [[0,-6]],[position[0]+27,position[1]+3])
      inkDraw.line.relCoords(elem, [[0,-14]],[position[0]+24,position[1]+7])
      inkDraw.line.relCoords(elem, [[0,-6]],[position[0]+21,position[1]+3])
      inkDraw.line.relCoords(elem, [[0,-14]],[position[0]+18,position[1]+7])
    else:
      inkDraw.line.relCoords(elem, [[-2,0]],[position[0]+37,position[1]-4],lineStyle=lineStyleSign)
      inkDraw.line.relCoords(elem, [[0,2]],[position[0]+36,position[1]-5],lineStyle=lineStyleSign)
      inkDraw.line.relCoords(elem, [[0,2]],[position[0]+15,position[1]-5],lineStyle=lineStyleSign)
      inkDraw.line.relCoords(elem, [[0,-6]],[position[0]+18,position[1]+3])
      inkDraw.line.relCoords(elem, [[0,-14]],[position[0]+21,position[1]+7])
      inkDraw.line.relCoords(elem, [[0,-6]],[position[0]+24,position[1]+3])
      inkDraw.line.relCoords(elem, [[0,-14]],[position[0]+27,position[1]+7])
      inkDraw.line.relCoords(elem, [[0,-6]],[position[0]+30,position[1]+3])
      inkDraw.line.relCoords(elem, [[0,-14]],[position[0]+33,position[1]+7])
    
    pos_text=[position[0]+25,position[1]-8-self.textOffset]
    if self.useLatex:
      inkDraw.text.latex(self,group,'$'+value+'$',pos_text,fontSize=self.fontSize,refPoint='bc',preambleFile=self.preambleFile)
    else:
      inkDraw.text.write(self,value,pos_text,group,self.textStyle)
    

    
    if angleDeg!=0:
      self.rotateElement(group,position,angleDeg)
    
    if flagVolt:
      self.drawVoltArrow(group,[position[0]+25 ,position[1]+8],name=value,color=self.voltageColor,angleDeg=angleDeg,invertArrows=not mirror)
      
    if flagCurr:
      self.drawCurrArrow(group,[position[0]+40 ,position[1]-5],name=currName,color=self.currentColor,angleDeg=angleDeg,invertArrows=(invertArrows== mirror))
      
    return group;
       
  #---------------------------------------------
  def drawSourceI(self,parent,position=[0, 0],value='i(t)',label='Source',angleDeg=0,
                    flagVolt=True,flagCurr=True,voltName='v',invertArrows=False,mirror=False):
    """ draws a independend general current source
    
    parent: parent object
    position: position [x,y]
    value: string with value.    
    label: label of the object (it can be repeated)
    angleDeg: rotation angle in degrees counter-clockwise (default 0)
    flagVolt: indicates whether the voltage arrow must be drawn (default: true)
    voltName: output voltage drop name (default: v)
    flagCurr: indicates whether the current arrow must be drawn (default: true)
    mirror: mirror source drawing (default: False)
    """

    group = self.createGroup(parent,label)
    elem = self.createGroup(group,label)
   
    inkDraw.line.relCoords(elem, [[18,0]],position)
    inkDraw.line.relCoords(elem, [[-18,0]],[position[0]+50,position[1]])
    inkDraw.circle.centerRadius(elem, [25,0],7.0,offset=position, label='circle')
    
    #arrow
    lineStyleSign=inkDraw.lineStyle.set(lineWidth=0.7, lineColor=inkDraw.color.defined('black'), fillColor=inkDraw.color.defined('black'))                      
    if mirror:
      inkDraw.line.relCoords(elem, [[-5,0],[0,1.2],[-3,-1.2],[3,-1.2],[0,1.2]],[position[0]+29,position[1]],lineStyle=lineStyleSign)
    else:
      inkDraw.line.relCoords(elem, [[5,0],[0,1.2],[3,-1.2],[-3,-1.2],[0,1.2]],[position[0]+21,position[1]],lineStyle=lineStyleSign)
    
    pos_text=[position[0]+25,position[1]-8-self.textOffset]
    if self.useLatex:
      inkDraw.text.latex(self,group,'$'+value+'$',pos_text,fontSize=self.fontSize,refPoint='bc',preambleFile=self.preambleFile)
    else:
      inkDraw.text.write(self,value,pos_text,group,self.textStyle)
           
    if angleDeg!=0:
      self.rotateElement(group,position,angleDeg)
    
    if flagVolt:
      self.drawVoltArrow(group,[position[0]+25 ,position[1]+8],name=voltName,color=self.voltageColor,angleDeg=angleDeg,invertArrows=(invertArrows== mirror))
      
    if flagCurr:
      self.drawCurrArrow(group,[position[0]+40 ,position[1]-5],name=value,color=self.currentColor,angleDeg=angleDeg,invertArrows=not mirror)
      
    return group;
    
           
  #---------------------------------------------
  def drawControledSourceV(self,parent,position=[0, 0],controlType='volt',gain='k',controlName='v_c',label='Source',angleDeg=0,
                           flagVolt=True,flagCurr=True,currName='i',invertArrows=False,mirror=False):
    """ draws a controlled general voltage source
    
    parent: parent object
    position: position [x,y]
    controlType: 'volt' or 'curr'
    gain: controlled source gain value
    controlName: name of the controlling signal
    label: label of the object (it can be repeated)
    angleDeg: rotation angle in degrees counter-clockwise (default 0)
    flagVolt: indicates whether the voltage arrow must be drawn (default: true)
    currName: output current name (default: i)
    flagCurr: indicates whether the current arrow must be drawn (default: true)
    mirror: mirror source drawing (default: False)
    """

    group = self.createGroup(parent,label)
    elem = self.createGroup(group,label)
   
    inkDraw.line.relCoords(elem, [[17,0]],position)
    inkDraw.line.relCoords(elem, [[-17,0]],[position[0]+50,position[1]])
    inkDraw.line.relCoords(elem, [[8,8],[8,-8],[-8,-8],[-8,8]],[position[0]+17,position[1]])
    
    #signs
    lineStyleSign=inkDraw.lineStyle.setSimpleBlack(lineWidth=0.6)
    if mirror:
      inkDraw.line.relCoords(elem, [[-2,0]],[position[0]+22,position[1]],lineStyle=lineStyleSign)
      inkDraw.line.relCoords(elem, [[0,2]],[position[0]+21,position[1]-1],lineStyle=lineStyleSign)
      inkDraw.line.relCoords(elem, [[0,2]],[position[0]+29,position[1]-1],lineStyle=lineStyleSign)
    else:
      inkDraw.line.relCoords(elem, [[-2,0]],[position[0]+30,position[1]],lineStyle=lineStyleSign)
      inkDraw.line.relCoords(elem, [[0,2]],[position[0]+29,position[1]-1],lineStyle=lineStyleSign)
      inkDraw.line.relCoords(elem, [[0,2]],[position[0]+21,position[1]-1],lineStyle=lineStyleSign)
    
    #text
    pos_text=[position[0]+25,position[1]-8-self.textOffset]
    value=gain + ' . ' + controlName
    if self.useLatex:
      inkDraw.text.latex(self,group,'$'+value+'$',pos_text,fontSize=self.fontSize,refPoint='bc',preambleFile=self.preambleFile)
    else:
      inkDraw.text.write(self,value,pos_text,group,self.textStyle)
           
           
    if angleDeg!=0:
      self.rotateElement(group,position,angleDeg)
    
    #arrows
    if flagVolt:
      self.drawVoltArrow(group,[position[0]+25 ,position[1]+8],name=value,color=self.voltageColor,angleDeg=angleDeg,invertArrows=not mirror)
      
    if flagCurr:
      self.drawCurrArrow(group,[position[0]+40 ,position[1]-5],name=currName,color=self.currentColor,angleDeg=angleDeg,invertArrows=(invertArrows== mirror))
    
    #control signal
    for theta in range(0,360,90):
      pos1=[position[0]+5 ,position[1]+25+theta/4]
      pos2=[position[0]+25 ,position[1]+25+theta/4]
      if controlType=='volt':
        temp1=self.drawVoltArrow(parent,pos1,name=controlName,color=self.voltageColor,angleDeg=theta,invertArrows=False)
        temp2=self.drawVoltArrow(parent,pos2,name=controlName,color=self.voltageColor,angleDeg=theta,invertArrows=True)
      if controlType=='curr':
        temp1=self.drawCurrArrow(parent,pos1,name=controlName,color=self.currentColor,angleDeg=theta,invertArrows=False)
        temp2=self.drawCurrArrow(parent,pos2,name=controlName,color=self.currentColor,angleDeg=theta,invertArrows=True)
        
      self.rotateElement(temp1,pos1,theta)
      self.rotateElement(temp2,pos2,theta)
      
    return group;
               
  #---------------------------------------------
  def drawControledSourceI(self,parent,position=[0, 0],controlType='volt',gain='k',controlName='v_c',label='Source',angleDeg=0,
                           flagVolt=True,flagCurr=True,voltName='v',invertArrows=False,mirror=False):
    """ draws a controlled general current source
    
    parent: parent object
    position: position [x,y]
    controlType: 'volt' or 'curr'
    gain: controlled source gain value
    controlName: name of the controlling signal
    label: label of the object (it can be repeated)
    angleDeg: rotation angle in degrees counter-clockwise (default 0)
    flagVolt: indicates whether the voltage arrow must be drawn (default: true)
    voltName: output voltage name (default: v)
    flagCurr: indicates whether the current arrow must be drawn (default: true)
    mirror: mirror source drawing (default: False)
    """

    group = self.createGroup(parent,label)
    elem = self.createGroup(group,label)
   
    inkDraw.line.relCoords(elem, [[17,0]],position)
    inkDraw.line.relCoords(elem, [[-17,0]],[position[0]+50,position[1]])
    inkDraw.line.relCoords(elem, [[8,8],[8,-8],[-8,-8],[-8,8]],[position[0]+17,position[1]])

    #arrow
    lineStyleSign=inkDraw.lineStyle.set(lineWidth=0.7, lineColor=inkDraw.color.defined('black'), fillColor=inkDraw.color.defined('black'))                      
    if mirror:
      inkDraw.line.relCoords(elem, [[-5,0],[0,1.2],[-3,-1.2],[3,-1.2],[0,1.2]],[position[0]+29,position[1]],lineStyle=lineStyleSign)
    else:
      inkDraw.line.relCoords(elem, [[5,0],[0,1.2],[3,-1.2],[-3,-1.2],[0,1.2]],[position[0]+21,position[1]],lineStyle=lineStyleSign)
    
    #text
    pos_text=[position[0]+25,position[1]-8-self.textOffset]
    value=gain + ' . ' + controlName
    if self.useLatex:
      inkDraw.text.latex(self,group,'$'+value+'$',pos_text,fontSize=self.fontSize,refPoint='bc',preambleFile=self.preambleFile)
    else:
      inkDraw.text.write(self,value,pos_text,group,self.textStyle)
    
    if angleDeg!=0:
      self.rotateElement(group,position,angleDeg)
    
    #arrows
    if flagVolt:
      self.drawVoltArrow(group,[position[0]+25 ,position[1]+8],name=voltName,color=self.voltageColor,angleDeg=angleDeg,invertArrows=(invertArrows== mirror))
      
    if flagCurr:
      self.drawCurrArrow(group,[position[0]+40 ,position[1]-5],name=value,color=self.currentColor,angleDeg=angleDeg,invertArrows=not mirror)
    
    #control signal
    for theta in range(0,360,90):
      pos1=[position[0]+5 ,position[1]+25+theta/4]
      pos2=[position[0]+25 ,position[1]+25+theta/4]
      if controlType=='volt':
        temp1=self.drawVoltArrow(parent,pos1,name=controlName,color=self.voltageColor,angleDeg=theta,invertArrows=False)
        temp2=self.drawVoltArrow(parent,pos2,name=controlName,color=self.voltageColor,angleDeg=theta,invertArrows=True)
      if controlType=='curr':
        temp1=self.drawCurrArrow(parent,pos1,name=controlName,color=self.currentColor,angleDeg=theta,invertArrows=False)
        temp2=self.drawCurrArrow(parent,pos2,name=controlName,color=self.currentColor,angleDeg=theta,invertArrows=True)
        
      self.rotateElement(temp1,pos1,theta)
      self.rotateElement(temp2,pos2,theta)
      
    return group;

  #---------------------------------------------
  def drawV(self,parent,position=[0, 0],label='GND',angleDeg=0,nodalVal='V_{cc}',drawLine=True):
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
    if self.useLatex:
      if abs(angleDeg)<=90:
        justif='bc'
        pos_text=[position[0],position[1]-self.textOffset]
      else:
        justif='tc'
        pos_text=[position[0],position[1]+self.textOffset]
        
      temp=inkDraw.text.latex(self,group,'$'+nodalVal+'$',pos_text,fontSize=self.fontSize,refPoint=justif,preambleFile=self.preambleFile)
    else:
      temp=inkDraw.text.write(self,nodalVal,pos_text,group,self.textStyle)
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
    
  #---------------------------------------------
  def drawOpAmpGeneral(self,parent,position=[0, 0],label='OpAmp',mirrorInput=False,
                       opampDrawVin=False,
                       opampDrawIin=False,
                       opampDrawVd=False,
                       opampDrawVout=False,
                       opampDrawIout=False,
                       opampInputVPosName='v^+',
                       opampInputVNegName='v^-',
                       opampInputIPosName='i^+',
                       opampInputINegName='i^-',
                       opampVoutName='v_o',
                       opampIoutName='i_o',
                       opampInputDiffName='v_d',
                       flagDrawSupply=False,
                       opampFlagSupplyValues=False,
                       flagSupplySymm=True,
                       supplyPositiveVal='V_{cc}',
                       supplyNegativeVal='-V_{cc}'):
    """ draws a general ampOp
    
    parent: parent object
    position: position [x,y]
    label: label of the object (it can be repeated)
    mirrorInput: invert + and - inputs (default: positive above, negative below)
    opampDrawVin: write v+ and v- besides the inputs (default: False)
    opampDrawVd: write vd besides the input terminals
    flagDrawSupply: draw supply terminals
    """
    group = self.createGroup(parent,label)
    elem = self.createGroup(group,label)
   
    inkDraw.line.relCoords(elem, [[-35,20],[0,-40],[35,20]],[position[0]+35,position[1]])
    inkDraw.line.relCoords(elem, [[-7.5,0]],[position[0],position[1]+10])
    inkDraw.line.relCoords(elem, [[-7.5,0]],[position[0],position[1]-10])
    inkDraw.line.relCoords(elem, [[7.5,0]],[position[0]+35,position[1]])
   
    if flagDrawSupply:
      inkDraw.line.relCoords(elem, [[0,-5]],[position[0]+17.5,position[1]-10])
      inkDraw.line.relCoords(elem, [[0,5]],[position[0]+17.5,position[1]+10])
      if opampFlagSupplyValues:
        if flagSupplySymm:
          self.drawV(elem,[position[0]+17.5,position[1]-25],angleDeg=0,nodalVal='+' + supplyPositiveVal.replace('+',''))
          self.drawV(elem,[position[0]+17.5,position[1]+25],angleDeg=180,nodalVal='-' + supplyPositiveVal.replace('+',''))
        else:
          self.drawV(elem,[position[0]+17.5,position[1]-25],angleDeg=0,nodalVal='+' + supplyPositiveVal.replace('+',''))
          self.drawV(elem,[position[0]+17.5,position[1]+25],angleDeg=180,nodalVal=supplyNegativeVal)
      
    #input signs
    lineStyleSign=inkDraw.lineStyle.setSimpleBlack(lineWidth=0.7)
    if mirrorInput:
      inkDraw.line.relCoords(elem, [[-3,0]],[position[0]+6,position[1]+10],lineStyle=lineStyleSign)
      inkDraw.line.relCoords(elem, [[0,-3]],[position[0]+4.5,position[1]+11.5],lineStyle=lineStyleSign)
      
      inkDraw.line.relCoords(elem, [[-3,0]],[position[0]+6,position[1]-10],lineStyle=lineStyleSign)
      if opampDrawVin:
        textVTop=opampInputVNegName
        textVBot=opampInputVPosName
      if opampDrawIin:
        textITop=opampInputINegName
        textIBot=opampInputIPosName
    else:
      inkDraw.line.relCoords(elem, [[-3,0]],[position[0]+6,position[1]+10],lineStyle=lineStyleSign)
      inkDraw.line.relCoords(elem, [[-3,0]],[position[0]+6,position[1]-10],lineStyle=lineStyleSign)
      inkDraw.line.relCoords(elem, [[0,3]],[position[0]+4.5,position[1]-11.5],lineStyle=lineStyleSign)
      if opampDrawVin:
        textVTop=opampInputVPosName
        textVBot=opampInputVNegName
      if opampDrawIin:
        textITop=opampInputIPosName
        textIBot=opampInputINegName
          
    #write v+ v-
    if opampDrawVin:
      posTop=[position[0]-1 ,position[1]-10-self.textOffsetSmall]
      posBot=[position[0]-1 ,position[1]+10-self.textOffsetSmall]
      if self.useLatex:
        temp1=inkDraw.text.latex(self,group,'$'+textVTop+'$',posTop,textColor=self.voltageColor,fontSize=self.fontSizeSmall,refPoint='br',preambleFile=self.preambleFile)
        temp2=inkDraw.text.latex(self,group,'$'+textVBot+'$',posBot,textColor=self.voltageColor,fontSize=self.fontSizeSmall,refPoint='br',preambleFile=self.preambleFile)
      else:
        temp1=inkDraw.text.write(self,textTop,posTop,group,self.textStyleSmall)
        temp2=inkDraw.text.write(self,textBot,posBot,group,self.textStyleSmall)
        
    #write i+ i-
    if opampDrawIin:
      posTop=[position[0]-7.5 ,position[1]-10+3]
      posBot=[position[0]-7.5 ,position[1]+10+3]
      temp1=self.drawCurrArrow(group,posTop,name='$'+textITop+'$',color=self.currentColor,angleDeg=180,invertArrows=False)
      self.rotateElement(temp1,posTop,180)
      temp1=self.drawCurrArrow(group,posBot,name='$'+textIBot+'$',color=self.currentColor,angleDeg=180,invertArrows=False)
      self.rotateElement(temp1,posBot,180)
      
    #write v_out
    if opampDrawVout:
      postext=[position[0]+35,position[1]-self.textOffsetSmall]
      if self.useLatex:
        temp1=inkDraw.text.latex(self,group,'$'+opampVoutName+'$',postext,textColor=self.voltageColor,fontSize=self.fontSize,refPoint='bl',preambleFile=self.preambleFile)
      else:
        temp1=inkDraw.text.write(self,opampVoutName,postext,group,self.textStyleSmall)

    #write i_out
    if opampDrawIout:
      pos=[position[0]+42,position[1]+3]
      temp1=self.drawCurrArrow(group,pos,name='$'+opampIoutName+'$',color=self.currentColor,angleDeg=180,invertArrows=False)
      self.rotateElement(temp1,pos,180)
      
    if opampDrawVd:
      pos1=[position[0]+6 ,position[1]]
      temp1=self.drawVoltArrow(group,pos1,name=opampInputDiffName,color=self.voltageColor,angleDeg=90,invertArrows=not mirrorInput,size=15)
      self.rotateElement(temp1,pos1,90)
      
    return group;
  #---------------------------------------------
  def drawSwitch2T(self,parent,position=[0, 0],value='S',label='Switch',angleDeg=0,flagOpen=True,flagDrawArrow=False,OpenCloseText='t_0'):
    """ draws a switch with two terminals only
    
    parent: parent object
    position: position [x,y] 
    label: label of the object (it can be repeated)
    """

    group = self.createGroup(parent,label)
    elem = self.createGroup(group,label)
    color=inkDraw.color.defined('red')
    colorBlack=inkDraw.color.defined('black')
    lineStyleSign=inkDraw.lineStyle.set(lineWidth=0.7, lineColor=colorBlack, fillColor=colorBlack)                      
    
    if flagOpen:
      inkDraw.line.relCoords(elem, [[15.5,0],[20,-8]],position)
      inkDraw.line.relCoords(elem, [[-15.5,0]],[position[0]+50,position[1]])
    else:
      inkDraw.line.relCoords(elem, [[15.5,0],[20,0]],position)
      inkDraw.line.relCoords(elem, [[-15.5,0]],[position[0]+50,position[1]])
    inkDraw.circle.centerRadius(elem, [position[0]+35,position[1]], 1.0, offset=[0,0],lineStyle=lineStyleSign)
    inkDraw.circle.centerRadius(elem, [position[0]+15,position[1]], 1.0, offset=[0,0],lineStyle=lineStyleSign)
    
    [arrowStart,arrowEnd] = inkDraw.marker.createArrow1Marker(self,'arrowSwitch',RenameMode=0,scale=0.25,strokeColor=color,fillColor=color)
    
    if flagDrawArrow:
      if OpenCloseText:
        pos_text=[position[0]+25,position[1]+4+self.textOffset]
        if self.useLatex:
          inkDraw.text.latex(self,group,'$'+OpenCloseText+'$',pos_text,fontSize=self.fontSize,refPoint='tc',preambleFile=self.preambleFile)
        else:
          inkDraw.text.write(self,OpenCloseText,pos_text,group,self.textStyle)
      if flagOpen:
        lineStyle = inkDraw.lineStyle.set(lineColor=color,markerEnd=arrowEnd);
      else:
        lineStyle = inkDraw.lineStyle.set(lineColor=color,markerStart=arrowStart);
      
      inkDraw.arc.startEndRadius(group, [0,-5], [0,5], 12, [position[0]+24,position[1]],lineStyle=lineStyle,flagRightOf=False)
      
    if flagOpen:
      pos_text=[position[0]+25,position[1]-6-self.textOffset]
    else:
      pos_text=[position[0]+25,position[1]-6-self.textOffset]
    
    if value:
      if self.useLatex:
        inkDraw.text.latex(self,group,'$'+value+'$',pos_text,fontSize=self.fontSize,refPoint='bc',preambleFile=self.preambleFile)
      else:
        inkDraw.text.write(self,value,pos_text,group,self.textStyle)
      
    if angleDeg!=0:
      self.rotateElement(group,position,angleDeg)
         
    return group;
    
  #---------------------------------------------
  
  def drawVoltArrowSimple(self,parent,position,label='arrowV',name='',color=inkDraw.color.defined('black'),
                          angleDeg=0,invertArrows=False,size=20.0,invertCurvatureDirection=False):
                                
    """ draws a voltage drop arrow
    
    parent: parent object
    position: position [x,y]
    label: label of the object (it can be repeated)
    name: string with namee. (default 'v')
    color: color of the arrow and text
    angleDeg: rotation angle in degrees counter-clockwise (default 0)
    invertArrows: invert current direction
    size: size of the arrow
    invertCurvatureDirection: invert curvature direction of the arrow
    """
    
    if invertCurvatureDirection:
      arrow_elem=self.drawVoltArrow(parent,position,label,name,color,angleDeg+180, invertArrows,size)
      self.rotateElement(arrow_elem,position,angleDeg+180)
    else:
      arrow_elem=self.drawVoltArrow(parent,position,label,name,color,angleDeg    ,not invertArrows,    size)
      self.rotateElement(arrow_elem,position,angleDeg)

  #---------------------------------------------
  
  def drawVoltArrow(self,parent,position,label='name',name='v',color=inkDraw.color.defined('black'),angleDeg=0,invertArrows=False,size=20.0):
    """ draws a voltage drop arrow
    
    parent: parent object
    position: position [x,y]
    label: label of the object (it can be repeated)
    name: string with namee. (default 'v')
    color: color of the arrow and text
    invertArrows: invert current direction
    size: size of the arrow
    """
    
    group = self.createGroup(parent,label)
    
    scale=size/20.0  # the default size was 20 height
    
    #make linestyle
    [arrowStartVolt,arrowEndVolt] = inkDraw.marker.createArrow1Marker(self,'arrowVoltage',RenameMode=0,scale=0.25,strokeColor=color,fillColor=color)
    
    if invertArrows:
      lineStyle = inkDraw.lineStyle.set(lineColor=color,markerStart=arrowStartVolt);
    else:
      lineStyle = inkDraw.lineStyle.set(lineColor=color,markerEnd=arrowEndVolt);
    
    radius=30.0*scale
    h=10.0*scale
    halfTheta=math.asin(h/radius)
    inkDraw.arc.startEndRadius(group, [h,0], [-h,0], radius, position,lineStyle=lineStyle,flagRightOf=False)
      
    # get appropriate refPoint based on the angle
    theta=angleDeg
    while theta<0:
      theta=theta+360;
    while theta>360:
      theta=theta-360;
      
    if theta<=20:
      justif='tc'
    else:
      if theta<=60:
        justif='tl'
      else:
        if theta<=100:
          justif='cl'
        else:
          if theta<=150:
            justif='bl'
          else:
            if theta<=200:
              justif='bc'
            else:
              if theta<=250:
                justif='br'
              else:
                if theta<=290:
                  justif='cr'
                else:
                  justif='tr'
                  
    centerY=-radius*math.cos(halfTheta)
    posY=centerY+radius
    if not name == '':
      inkDraw.text.latex(self,group,'$'+name+'$',[position[0],position[1]+posY+4.0],fontSize=self.fontSize,refPoint=justif,textColor=color,angleDeg=-theta,preambleFile=self.preambleFile)
          
    return group

  #---------------------------------------------
  
  def drawCurrArrowSimple(self,parent,position,label='arrowI',name='',color=inkDraw.color.defined('black'),
                          angleDeg=0,invertArrows=False,size=20.0,invertTextSide=False):
                                
    """ draws a current arrow
    
    parent: parent object
    position: position [x,y]
    label: label of the object (it can be repeated)
    name: string with namee. (default none)
    color: color of the arrow and text
    angleDeg: rotation angle in degrees counter-clockwise (default 0)
    invertArrows: invert current direction
    size: size of the arrow
    invertCurvatureDirection: invert curvature direction of the arrow
    """
      
          #control signal
    if invertTextSide:
      temp1=self.drawCurrArrow(parent,position,label,name,color=self.currentColor,angleDeg=angleDeg+180,invertArrows=invertArrows,size=size)    
      self.rotateElement(temp1,position,angleDeg+180)
    else:
      temp1=self.drawCurrArrow(parent,position,label,name,color=self.currentColor,angleDeg=angleDeg,invertArrows=not invertArrows,size=size)    
      self.rotateElement(temp1,position,angleDeg)
      
      
  #---------------------------------------------
  def drawCurrArrow(self,parent,position,label='name',name='i',color=inkDraw.color.defined('black'),angleDeg=0,invertArrows=False,size=10.0):
    """ draws a current arrow
    
    parent: parent object
    position: position [x,y]
    label: label of the object (it can be repeated)
    name: string with namee. (default 'v')
    color: color of the arrow and text
    angleDeg: rotation angle in degrees
    invertArrows: invert current direction
    """
    scale=size/10.0
    group = self.createGroup(parent,label)
    
    #make linestyle
    [arrowStartCurr,arrowEndCurr] = inkDraw.marker.createArrow1Marker(self,'arrowCurrent',RenameMode=0,scale=0.25,strokeColor=color,fillColor=color)
    lineStyle = inkDraw.lineStyle.set(lineColor=color,markerEnd=arrowEndCurr);
    
    if invertArrows:
      inkDraw.line.relCoords(group, [[10*scale,0]], [position[0]-5*scale,position[1]], label='none', lineStyle=lineStyle)
    else:
      inkDraw.line.relCoords(group, [[-10*scale,0]], [position[0]+5*scale,position[1]], label='none', lineStyle=lineStyle)
    
    # get appropriate refPoint based on the angle
    theta=angleDeg
    while theta<0:
      theta=theta+360;
    while theta>360:
      theta=theta-360;
      
    if theta<=20:
      justif='bc'
    else:
      if theta<=60:
        justif='br'
      else:
        if theta<=100:
          justif='cr'
        else:
          if theta<=150:
            justif='tr'
          else:
            if theta<=200:
              justif='tc'
            else:
              if theta<=250:
                justif='tl'
              else:
                if theta<=290:
                  justif='cl'
                else:
                  justif='bl'
        
    inkDraw.text.latex(self,group,'$'+name+'$',[position[0],position[1]-self.textOffset*0.8],fontSize=self.fontSize,refPoint=justif,textColor=color,angleDeg=-theta,preambleFile=self.preambleFile)
    
    return group
if __name__ == '__main__':
  circuit = CircuitSymbols()
  circuit.affect()
    