#!/usr/bin/python

import os
import inkex
import inkscapeMadeEasy_Base as inkBase
import inkscapeMadeEasy_Draw as inkDraw
import math

#some symbol definition

OhmChar=u'\u2126'.encode('utf-8')

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
    
  if valueString[-1]=='n':
    return valueString.replace('n',r'\si\nano')
  
  if valueString[-1]=='p':
    return valueString.replace('p',r'\si\pico')
  
  return valueString

#---------------------------------------------
class CircuitSymbols(inkBase.inkscapeMadeEasy):
  def __init__(self):
    inkBase.inkscapeMadeEasy.__init__(self)
    
    self.OptionParser.add_option("--tab",action="store", type="string",dest="tab", default="object") 
    
    self.OptionParser.add_option("--bipoleRLC",action="store", type="string",dest="bipoleRLC", default='resistor')
    self.OptionParser.add_option("--bipoleRLCVal", action="store", type="string", dest="bipoleRLCVal", default='Z') 
    self.OptionParser.add_option("--bipoleRLCUnit",action="store", type="inkbool",dest="bipoleRLCUnit", default=False)
    self.OptionParser.add_option("--bipoleRLCRot", action="store", type="string", dest="bipoleRLCRot", default='0') 
    self.OptionParser.add_option("--bipoleRLCVolt", action="store", type="inkbool", dest="bipoleRLCVolt", default=True) 
    self.OptionParser.add_option("--bipoleRLCCurr", action="store", type="inkbool", dest="bipoleRLCCurr", default=True)
    self.OptionParser.add_option("--bipoleRLCVoltName", action="store", type="string", dest="bipoleRLCVoltName", default='v') 
    self.OptionParser.add_option("--bipoleRLCCurrName", action="store", type="string", dest="bipoleRLCCurrName", default='i') 
    self.OptionParser.add_option("--bipoleRLCVoltCurrInvert", action="store", type="inkbool", dest="bipoleRLCVoltCurrInvert", default=True)
    
    self.OptionParser.add_option("--source",action="store", type="string",dest="source", default='voltIndep')
    self.OptionParser.add_option("--sourceVal", action="store", type="string", dest="sourceVal", default='E') 
    self.OptionParser.add_option("--sourceUnit",action="store", type="inkbool",dest="sourceUnit", default=False)
    self.OptionParser.add_option("--sourceRot", action="store", type="string", dest="sourceRot", default='0') 
    self.OptionParser.add_option("--sourceVolt", action="store", type="inkbool", dest="sourceVolt", default=True) 
    self.OptionParser.add_option("--sourceCurr", action="store", type="inkbool", dest="sourceCurr", default=True)
    self.OptionParser.add_option("--sourceVoltName", action="store", type="string", dest="sourceVoltName", default='v') 
    self.OptionParser.add_option("--sourceCurrName", action="store", type="string", dest="sourceCurrName", default='i') 
    self.OptionParser.add_option("--sourceVoltCurrInvert", action="store", type="inkbool", dest="sourceVoltCurrInvert", default=True)
    self.OptionParser.add_option("--sourceMirror", action="store", type="inkbool", dest="sourceMirror", default=False)
        
    self.OptionParser.add_option("--sourceControlled",action="store", type="string",dest="sourceControlled", default='volt')
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
    
    self.OptionParser.add_option("--switch",action="store", type="string",dest="switch", default='switch2T')
    self.OptionParser.add_option("--switchVal", action="store", type="string", dest="switchVal", default='') 
    self.OptionParser.add_option("--switchFlagOpen", action="store", type="inkbool", dest="switchFlagOpen", default=True) 
    self.OptionParser.add_option("--switchOpenClose", action="store", type="inkbool", dest="switchOpenClose", default=True) 
    self.OptionParser.add_option("--switchOpenCloseText",action="store", type="string",dest="switchOpenCloseText", default='')
    self.OptionParser.add_option("--switchRot", action="store", type="string", dest="switchRot", default=0) 

    self.OptionParser.add_option("--BJT",action="store", type="string",dest="BJT", default='none')
    self.OptionParser.add_option("--BJT_Rot", action="store", type="string", dest="BJT_Rot", default='0') 
    self.OptionParser.add_option("--BJT_Envelope", action="store", type="inkbool", dest="BJT_Envelope", default=True) 
    self.OptionParser.add_option("--BJT_MirrorEC", action="store", type="inkbool", dest="BJT_MirrorEC", default=False) 
    self.OptionParser.add_option("--BJT_EBCtags", action="store", type="inkbool", dest="BJT_EBCtags", default=False) 
    self.OptionParser.add_option("--BJT_DrawVCEarrow", action="store", type="inkbool", dest="BJT_DrawVCEarrow", default=False)
    self.OptionParser.add_option("--BJT_DrawVCBarrow", action="store", type="inkbool", dest="BJT_DrawVCBarrow", default=False)
    self.OptionParser.add_option("--BJT_DrawVBEarrow", action="store", type="inkbool", dest="BJT_DrawVBEarrow", default=False)
    self.OptionParser.add_option("--BJT_DrawICarrow", action="store", type="inkbool", dest="BJT_DrawICarrow", default=False)
    self.OptionParser.add_option("--BJT_DrawIBarrow", action="store", type="inkbool", dest="BJT_DrawIBarrow", default=False)
    self.OptionParser.add_option("--BJT_DrawIEarrow", action="store", type="inkbool", dest="BJT_DrawIEarrow", default=False)

    self.OptionParser.add_option("--BJT_VCEname", action="store", type="string", dest="BJT_VCEname", default='v_{ce}')
    self.OptionParser.add_option("--BJT_VCBname", action="store", type="string", dest="BJT_VCBname", default='v_{cb}')
    self.OptionParser.add_option("--BJT_VBEname", action="store", type="string", dest="BJT_VBEname", default='v_{be}')
    self.OptionParser.add_option("--BJT_ICname", action="store", type="string", dest="BJT_ICname", default='i_c')
    self.OptionParser.add_option("--BJT_IBname", action="store", type="string", dest="BJT_IBname", default='i_b')
    self.OptionParser.add_option("--BJT_IEname", action="store", type="string", dest="BJT_IEname", default='i_e')

    self.OptionParser.add_option("--FET_Type",action="store", type="string",dest="FET_Type", default='none')
    self.OptionParser.add_option("--FET_Gate",action="store", type="string",dest="FET_Gate", default='none')
    self.OptionParser.add_option("--FET_BodyDiode",action="store", type="inkbool",dest="FET_BodyDiode", default=False)    
    self.OptionParser.add_option("--FET_MoveGate",action="store", type="inkbool",dest="FET_MoveGate", default=False)    
    self.OptionParser.add_option("--FET_Rot", action="store", type="string", dest="FET_Rot", default='0') 
    self.OptionParser.add_option("--FET_Envelope", action="store", type="inkbool", dest="FET_Envelope", default=True) 
    self.OptionParser.add_option("--FET_MirrorEC", action="store", type="inkbool", dest="FET_MirrorEC", default=False) 
    self.OptionParser.add_option("--FET_SGDtags", action="store", type="inkbool", dest="FET_SGDtags", default=False) 
    self.OptionParser.add_option("--FET_DrawVGSarrow", action="store", type="inkbool", dest="FET_DrawVGSarrow", default=False)
    self.OptionParser.add_option("--FET_DrawVDSarrow", action="store", type="inkbool", dest="FET_DrawVDSarrow", default=False)
    self.OptionParser.add_option("--FET_DrawVDGarrow", action="store", type="inkbool", dest="FET_DrawVDGarrow", default=False)
    self.OptionParser.add_option("--FET_DrawIDarrow", action="store", type="inkbool", dest="FET_DrawIDarrow", default=False)
    self.OptionParser.add_option("--FET_DrawISarrow", action="store", type="inkbool", dest="FET_DrawISarrow", default=False)
    self.OptionParser.add_option("--FET_DrawIGarrow", action="store", type="inkbool", dest="FET_DrawIGarrow", default=False)

    self.OptionParser.add_option("--FET_VGSname", action="store", type="string", dest="FET_VGSname", default='v_{gs}')
    self.OptionParser.add_option("--FET_VDSname", action="store", type="string", dest="FET_VDSname", default='v_{ds}')
    self.OptionParser.add_option("--FET_VDGname", action="store", type="string", dest="FET_VDGname", default='v_{dg}')
    self.OptionParser.add_option("--FET_IDname", action="store", type="string", dest="FET_IDname", default='i_d')
    self.OptionParser.add_option("--FET_ISname", action="store", type="string", dest="FET_ISname", default='i_s')
    self.OptionParser.add_option("--FET_IGname", action="store", type="string", dest="FET_IGname", default='i_g')

    self.OptionParser.add_option("--diode",action="store", type="string",dest="diode", default='none')
    self.OptionParser.add_option("--diodeVal", action="store", type="string", dest="diodeVal", default=None) 
    self.OptionParser.add_option("--diodeRot", action="store", type="string", dest="diodeRot", default='0')     
    self.OptionParser.add_option("--diodeVolt", action="store", type="inkbool", dest="diodeVolt", default=True) 
    self.OptionParser.add_option("--diodeCurr", action="store", type="inkbool", dest="diodeCurr", default=True)
    self.OptionParser.add_option("--diodeVoltName", action="store", type="string", dest="diodeVoltName", default='v') 
    self.OptionParser.add_option("--diodeCurrName", action="store", type="string", dest="diodeCurrName", default='i') 
    self.OptionParser.add_option("--diodeVoltCurrInvert", action="store", type="inkbool", dest="diodeVoltCurrInvert", default=True)
    self.OptionParser.add_option("--diodeMirror", action="store", type="inkbool", dest="diodeMirror", default=False)
       
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
    #root_layer = self.getcurrentLayer()
    
    # text size and font style
    self.fontSize=5
    self.fontSizeSmall=4

      
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
    so.diodeRot=float(so.diodeRot)
    so.BJT_Rot=float(so.BJT_Rot)
    so.FET_Rot=float(so.FET_Rot)
    
    #x=inkDraw.textStyle.setSimpleBlack(fontSize=10, justification='center')
    #ang=30.0
    #inkDraw.text.write(self, 'abc', position, root_layer, textStyle=x, fontSize=None, justification=None, angleDeg=ang)
    
    #inkDraw.text.latex(self, root_layer, 'def', position, fontSize=10, refPoint='cc', angleDeg=ang)
    #---------------------------
    # RLC
    #---------------------------
    if so.tab=='RLC':
      
      
      if so.bipoleRLCUnit and inkDraw.useLatex:
          so.bipoleRLCVal=latexUnitMultiple(so.bipoleRLCVal)
        
      if so.bipoleRLC=="genericBipole":
        if so.bipoleRLCUnit:
          if inkDraw.useLatex:
            so.bipoleRLCVal+=r'\si\ohm'
          else:
            so.bipoleRLCVal+= OhmChar
        self.drawBipoleGeneral(root_layer,position,value=so.bipoleRLCVal,angleDeg=so.bipoleRLCRot,
                              flagVolt=so.bipoleRLCVolt,voltName=so.bipoleRLCVoltName,flagCurr=so.bipoleRLCCurr,
                              currName=so.bipoleRLCCurrName,invertArrows=so.bipoleRLCVoltCurrInvert)
        
      if so.bipoleRLC=="resistor":
        if so.bipoleRLCUnit:
          if inkDraw.useLatex:
            so.bipoleRLCVal+=r'\si\ohm'
          else:
            so.bipoleRLCVal+= OhmChar
        self.drawResistor(root_layer,position,value=so.bipoleRLCVal,angleDeg=so.bipoleRLCRot,
                          flagVolt=so.bipoleRLCVolt,voltName=so.bipoleRLCVoltName,flagCurr=so.bipoleRLCCurr,
                          currName=so.bipoleRLCCurrName,invertArrows=so.bipoleRLCVoltCurrInvert)
        
      if so.bipoleRLC=="capacitor":
        if so.bipoleRLCUnit:
          if inkDraw.useLatex:
            so.bipoleRLCVal+=r'\si\farad'
          else:
            so.bipoleRLCVal+='F'
        self.drawCapacitor(root_layer,position,value=so.bipoleRLCVal,flagPol=False,angleDeg=so.bipoleRLCRot,
                          flagVolt=so.bipoleRLCVolt,voltName=so.bipoleRLCVoltName,flagCurr=so.bipoleRLCCurr,
                          currName=so.bipoleRLCCurrName,invertArrows=so.bipoleRLCVoltCurrInvert)
        
      if so.bipoleRLC=="capacitorPol":
        if so.bipoleRLCUnit:
          if inkDraw.useLatex:
            so.bipoleRLCVal+=r'\si\farad'
          else:
            so.bipoleRLCVal+='F'
        self.drawCapacitor(root_layer,position,value=so.bipoleRLCVal,flagPol=True,angleDeg=so.bipoleRLCRot,
                          flagVolt=so.bipoleRLCVolt,voltName=so.bipoleRLCVoltName,flagCurr=so.bipoleRLCCurr,
                          currName=so.bipoleRLCCurrName,invertArrows=so.bipoleRLCVoltCurrInvert)

      if so.bipoleRLC=="inductor":
        if so.bipoleRLCUnit:
          if inkDraw.useLatex:
            so.bipoleRLCVal+=r'\si\henry'
          else:
            so.bipoleRLCVal+='H'
        self.drawInductor(root_layer,position,value=so.bipoleRLCVal,angleDeg=so.bipoleRLCRot,
                          flagVolt=so.bipoleRLCVolt,voltName=so.bipoleRLCVoltName,flagCurr=so.bipoleRLCCurr,
                          currName=so.bipoleRLCCurrName,invertArrows=so.bipoleRLCVoltCurrInvert)
                                    
      if so.bipoleRLC=="pot2T":
        if so.bipoleRLCUnit:
          if inkDraw.useLatex:
            so.bipoleRLCVal+=r'\si\ohm'
          else:
            so.bipoleRLCVal+= OhmChar
        self.drawPotentiometer(root_layer,position,value=so.bipoleRLCVal,angleDeg=so.bipoleRLCRot,
                               flagVolt=so.bipoleRLCVolt,voltName=so.bipoleRLCVoltName,flagCurr=so.bipoleRLCCurr,
                               currName=so.bipoleRLCCurrName,invertArrows=so.bipoleRLCVoltCurrInvert,is3T=False)
       
      if so.bipoleRLC=="pot3T":
        if so.bipoleRLCUnit:
          if inkDraw.useLatex:
            so.bipoleRLCVal+=r'\si\ohm'
          else:
            so.bipoleRLCVal+= OhmChar
        self.drawPotentiometer(root_layer,position,value=so.bipoleRLCVal,angleDeg=so.bipoleRLCRot,
                               flagVolt=so.bipoleRLCVolt,voltName=so.bipoleRLCVoltName,flagCurr=so.bipoleRLCCurr,
                               currName=so.bipoleRLCCurrName,invertArrows=so.bipoleRLCVoltCurrInvert,is3T=True)
        
    #---------------------------
    # independendent sources
    #---------------------------
    if so.tab=='Indep. Source':
      
      if so.sourceUnit and inkDraw.useLatex:
          so.sourceVal=latexUnitMultiple(so.sourceVal)
                
      if so.source=="voltIndepDC":
        if so.sourceUnit:
          if inkDraw.useLatex:
            so.sourceVal+=r'\si\volt'
          else:
            so.sourceVal+='V'
        self.drawSourceVDC(root_layer,position,value=so.sourceVal,angleDeg=so.sourceRot,
                          flagVolt=so.sourceVolt,flagCurr=so.sourceCurr,
                          currName=so.sourceCurrName,invertArrows=so.sourceVoltCurrInvert,mirror=so.sourceMirror)
                                        
      if so.source=="voltIndepDCbattery":
        if so.sourceUnit:
          if inkDraw.useLatex:
            so.sourceVal+=r'\si\volt'
          else:
            so.sourceVal+='V'
        self.drawSourceVDCbattery(root_layer,position,value=so.sourceVal,angleDeg=so.sourceRot,
                                flagVolt=so.sourceVolt,flagCurr=so.sourceCurr,
                                currName=so.sourceCurrName,invertArrows=so.sourceVoltCurrInvert,mirror=so.sourceMirror)

      if so.source=="voltIndep":
        if so.sourceUnit:
          if inkDraw.useLatex:
            so.sourceVal+=r'\si\volt'
          else:
            so.sourceVal+='V'
        self.drawSourceV(root_layer,position,value=so.sourceVal,angleDeg=so.sourceRot,
                        flagVolt=so.sourceVolt,flagCurr=so.sourceCurr,
                        currName=so.sourceCurrName,invertArrows=so.sourceVoltCurrInvert,mirror=so.sourceMirror)
                                    
      if so.source=="voltIndepSinusoidal":
        if so.sourceUnit:
          if inkDraw.useLatex:
            so.sourceVal+=r'\si\volt'
          else:
            so.sourceVal+='V'
        self.drawSourceVSinusoidal(root_layer,position,value=so.sourceVal,angleDeg=so.sourceRot,
                                    flagVolt=so.sourceVolt,flagCurr=so.sourceCurr,
                                    currName=so.sourceCurrName,invertArrows=so.sourceVoltCurrInvert,mirror=so.sourceMirror)
                                    
      if so.source=="currIndep":
        if so.sourceUnit:
          if inkDraw.useLatex:
            so.sourceVal+=r'\si\ampere'
          else:
            so.sourceVal+='A'
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
    # diodes
    #---------------------------
    if so.tab=='Diodes':
      if so.diode in ['regular','LED','photoDiode','zener','schottky','tunnel','varicap']:
        self.drawDiode(root_layer,position,value=so.diodeVal,angleDeg=so.diodeRot,
                      flagVolt=so.diodeVolt,voltName=so.diodeVoltName,flagCurr=so.diodeCurr,
                      currName=so.diodeCurrName,invertArrows=not so.diodeVoltCurrInvert,flagType=so.diode,mirror=so.diodeMirror)  
      
    #---------------------------
    # Transistors
    #---------------------------
    if so.tab=='Transistor_BJT':
      
      if so.BJT =='BJT_PNP':
        type='PNP'
      else:
        type='NPN'
        
      self.drawTransistorBJT(root_layer,position,angleDeg=so.BJT_Rot,mirrorEC=so.BJT_MirrorEC,
                              drawBCEtags=so.BJT_EBCtags,drawEnvelope=so.BJT_Envelope,transistorType=type,
                              drawVCE=so.BJT_DrawVCEarrow,drawVCB=so.BJT_DrawVCBarrow,drawVBE=so.BJT_DrawVBEarrow,
                              drawICarrow=so.BJT_DrawICarrow,drawIBarrow=so.BJT_DrawIBarrow,drawIEarrow=so.BJT_DrawIEarrow,
                              VCEname=so.BJT_VCEname,VCBname=so.BJT_VCBname,VBEname=so.BJT_VBEname,
                              ICname=so.BJT_ICname,IBname=so.BJT_IBname,IEname=so.BJT_IEname)


    if so.tab=='Transistor_FET':
      if 'MOSFET' in so.FET_Type:
        self.drawTransistorMOSFET(root_layer,position,angleDeg=so.FET_Rot,mirrorSD=so.FET_MirrorEC,
                                  drawSGDtags=so.FET_SGDtags,drawEnvelope=so.FET_Envelope,modeType=so.FET_Type,gateType=so.FET_Gate,bodyDiode=so.FET_BodyDiode,
                                  drawVGS=so.FET_DrawVGSarrow,drawVDS=so.FET_DrawVDSarrow,drawVDG=so.FET_DrawVDGarrow,
                                  drawIDarrow=so.FET_DrawIDarrow,drawISarrow=so.FET_DrawISarrow,drawIGarrow=so.FET_DrawIGarrow,
                                  VGSname=so.FET_VGSname,VDSname=so.FET_VDSname,VDGname=so.FET_VDGname,
                                  IDname=so.FET_IDname,ISname=so.FET_ISname,IGname=so.FET_IGname)
        
      if 'JFET' in so.FET_Type:
        self.drawTransistorJFET(root_layer,position,angleDeg=so.FET_Rot,mirrorSD=so.FET_MirrorEC,
                                  drawSGDtags=so.FET_SGDtags,drawEnvelope=so.FET_Envelope,gateType=so.FET_Gate,moveGate=so.FET_MoveGate,
                                  drawVGS=so.FET_DrawVGSarrow,drawVDS=so.FET_DrawVDSarrow,drawVDG=so.FET_DrawVDGarrow,
                                  drawIDarrow=so.FET_DrawIDarrow,drawISarrow=so.FET_DrawISarrow,drawIGarrow=so.FET_DrawIGarrow,
                                  VGSname=so.FET_VGSname,VDSname=so.FET_VDSname,VDGname=so.FET_VDGname,
                                  IDname=so.FET_IDname,ISname=so.FET_ISname,IGname=so.FET_IGname)
      
    # --------------------------
    # operational amplifiers
    #---------------------------
    if so.tab=='Opamp':
      if so.opamp=="general":
        opamp_elem=self.drawOpAmpGeneral(root_layer,position,mirrorInput=so.opampMirrorInput,
                                        drawVin=so.opampDrawVin,drawIin=so.opampDrawIin,
                                        drawVd=so.opampDrawVd,drawVout=so.opampDrawVout,drawIout=so.opampDrawIout,
                                        inputVPosName=so.opampInputVPosName,inputVNegName=so.opampInputVNegName,
                                        inputIPosName=so.opampInputIPosName,inputINegName=so.opampInputINegName,
                                        VoutName=so.opampVoutName,IoutName=so.opampIoutName,
                                        VdiffName=so.opampInputDiffName,
                                        flagDrawSupply=so.opampFlagSupply,FlagSupplyValues=so.opampFlagSupplyValues,
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
    if inkDraw.useLatex:
      value='$'+value + '$'
      
    inkDraw.text.latex(self,group,value,pos_text,fontSize=self.fontSize,refPoint='bc',preambleFile=self.preambleFile)
      
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
      
    group = self.createGroup(parent,label)
    elem = self.createGroup(group)
    
    inkDraw.line.relCoords(elem, [[15.5,0],[2,3],[3,-6],[3,6],[3,-6],[3,6],[3,-6],[2,3],[15.5,0]],position)
      
    pos_text=[position[0]+25,position[1]-3-self.textOffset]
    if inkDraw.useLatex:
      value='$'+value +'$'
      
    inkDraw.text.latex(self,group,value,pos_text,fontSize=self.fontSize,refPoint='bc',preambleFile=self.preambleFile)

    if angleDeg!=0:
      self.rotateElement(group,position,angleDeg)
    
    if flagVolt:
      self.drawVoltArrow(group,[position[0]+25 ,position[1]+5],name=voltName,color=self.voltageColor,angleDeg=angleDeg,invertArrows=not invertArrows)
      
    if flagCurr:
      self.drawCurrArrow(group,[position[0]+40 ,position[1]-5],name=currName,color=self.currentColor,angleDeg=angleDeg,invertArrows=invertArrows)
      
    return group;
    
  #---------------------------------------------
  def drawPotentiometer(self,parent,position=[0, 0],value='R',label='Potentiometer',angleDeg=0,
                        flagVolt=True,voltName='v',flagCurr=True,currName='i',invertArrows=False,is3T=False):
    """ draws a potentiometer
    
    parent: parent object
    position: position [x,y]
    value: string with resistor value.
    
    label: label of the object (it can be repeated)
    angleDeg: rotation angle in degrees counter-clockwise (default 0)
    flagVolt: indicates whether the voltage arrow must be drawn (default: true)
    voltName: voltage drop name (default: v)
    flagCurr: indicates whether the current arrow must be drawn (default: true)
    currName: current drop name (default: i)
    is3T: indicates the drawPotentiometer has 3 terminals (default:false)
    """
      
    group = self.createGroup(parent,label)
    elem = self.createGroup(group)
    
    # build arrow marker
    colorBlack=inkDraw.color.defined('black')
    L_arrow=2.5
    markerPath = 'M 0,0 l -%f,%f l 0,-%f z'% (L_arrow*1.2, L_arrow/2.0,L_arrow)
    markerArrow=inkDraw.marker.createMarker(self, 'BJTArrow', markerPath, RenameMode=1, strokeColor=colorBlack, fillColor=colorBlack,lineWidth=0.6,markerTransform='translate (1,0)')
    lineStyleArrow = inkDraw.lineStyle.set(lineWidth=1, lineColor=colorBlack, markerEnd=markerArrow)
    
    
    inkDraw.line.relCoords(elem, [[15.5,0],[2,3],[3,-6],[3,6],[3,-6],[3,6],[3,-6],[2,3],[15.5,0]],position)
    
    # 2-terminal Potentiometer
    if is3T:
      inkDraw.line.relCoords(elem, [[0,-10]],[position[0]+25,position[1]+15],lineStyle=lineStyleArrow)
      pos_text=[position[0]+25,position[1]-3-self.textOffset]
    else:
      inkDraw.line.relCoords(elem, [[20,-12]],[position[0]+15,position[1]+6],lineStyle=lineStyleArrow)
      pos_text=[position[0]+25,position[1]-6-self.textOffset]
    

    if inkDraw.useLatex:
      value='$'+value +'$'
      
    inkDraw.text.latex(self,group,value,pos_text,fontSize=self.fontSize,refPoint='bc',preambleFile=self.preambleFile)

    if angleDeg!=0:
      self.rotateElement(group,position,angleDeg)
    
    if flagVolt:
      if is3T:
        pos=[position[0]+25 ,position[1]+5]
      else:
        pos=[position[0]+25 ,position[1]+8]
      self.drawVoltArrow(group,pos,name=voltName,color=self.voltageColor,angleDeg=angleDeg,invertArrows=not invertArrows)
      
    if flagCurr:
      if is3T:
        pos=[position[0]+40 ,position[1]-5]
      else:
        pos=[position[0]+42 ,position[1]-5]
      self.drawCurrArrow(group,pos,name=currName,color=self.currentColor,angleDeg=angleDeg,invertArrows=invertArrows)
      
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
    if inkDraw.useLatex:
      value='$'+value +'$'
      
    inkDraw.text.latex(self,group,value,pos_text,fontSize=self.fontSize,refPoint='bc',preambleFile=self.preambleFile)
      
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
      
    group = self.createGroup(parent,label)
    elem = self.createGroup(group,label)
    
    inkDraw.line.relCoords(elem, [[13,0]],position)
    inkDraw.line.relCoords(elem, [[-13,0]],[position[0]+50,position[1]])
    
    inkDraw.arc.centerAngStartAngEnd(elem,[position[0]+16,position[1]], 3.0,0.0,180.0,[0,0],flagOpen=True,largeArc=False)   
    inkDraw.arc.centerAngStartAngEnd(elem,[position[0]+22,position[1]], 3.0,0.0,180.0,[0,0],flagOpen=True,largeArc=False)  
    inkDraw.arc.centerAngStartAngEnd(elem,[position[0]+28,position[1]], 3.0,0.0,180.0,[0,0],flagOpen=True,largeArc=False)  
    inkDraw.arc.centerAngStartAngEnd(elem,[position[0]+34,position[1]], 3.0,0.0,180.0,[0,0],flagOpen=True,largeArc=False)  
    
    pos_text=[position[0]+25,position[1]-self.textOffset]
    if inkDraw.useLatex:
      value='$'+value +'$'
      
    inkDraw.text.latex(self,group,value,pos_text,fontSize=self.fontSize,refPoint='bc',preambleFile=self.preambleFile)

    if angleDeg!=0:
      self.rotateElement(group,position,angleDeg)
    
    if flagVolt:
      self.drawVoltArrow(group,[position[0]+25 ,position[1]+5],name=voltName,color=self.voltageColor,angleDeg=angleDeg,invertArrows=not invertArrows)
      
    if flagCurr:
      self.drawCurrArrow(group,[position[0]+40 ,position[1]-5],name=currName,color=self.currentColor,angleDeg=angleDeg,invertArrows=invertArrows)
      
    return group;

  #---------------------------------------------
  def drawDiode(self,parent,position=[0, 0],value='D',label='diode',angleDeg=0,
                flagVolt=True,voltName='v',flagCurr=True,currName='i',invertArrows=False,flagType='regular',mirror=False):
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
    flagType: tipe of element: available types:  'regular', 'LED', 'photoDiode', 'zener', 'schottky','tunnel','varicap' (default: regular)
    mirror: mirror diode (default: False)
    """
      
    group = self.createGroup(parent,label)
    elem = self.createGroup(group)

    if mirror:
      if flagType == 'varicap':
        inkDraw.line.relCoords(elem, [[16,0]],position)
      else:
        inkDraw.line.relCoords(elem, [[19,0]],position)
        
      inkDraw.line.relCoords(elem, [[12,6],[0,-12],[-12,6]],[position[0]+19,position[1]])
      inkDraw.line.relCoords(elem, [[19,0]],[position[0]+31,position[1]])
      
      
      if flagType in ['regular','LED','photoDiode']:
        inkDraw.line.relCoords(elem, [[0,12]],[position[0]+19,position[1]-6])
      
      if flagType == 'zener':
        inkDraw.line.relCoords(elem, [[-2,-2],[0,-10],[-2,-2]],[position[0]+19+2,position[1]+5+2])
        
      if flagType == 'schottky':
        inkDraw.line.relCoords(elem, [[0,2],[3,0],[0,-12],[3,0],[0,2]],[position[0]+19-3,position[1]+6-2])
        
      if flagType == 'tunnel':
        if mirror:
          inkDraw.line.relCoords(elem, [[-3,0],[0,-12],[3,0]],[position[0]+19+3,position[1]+6])
        else:
          inkDraw.line.relCoords(elem, [[3,0],[0,-12],[-3,0]],[position[0]+19-3,position[1]+6])
      
      if flagType == 'varicap':
        inkDraw.line.relCoords(elem, [[0,12]],[position[0]+19,position[1]-6])
        if mirror:
          inkDraw.line.relCoords(elem, [[0,12]],[position[0]+16,position[1]-6])
        else:
          inkDraw.line.relCoords(elem, [[0,12]],[position[0]+22,position[1]-6])
        
    else:
      inkDraw.line.relCoords(elem, [[19,0]],position)
      inkDraw.line.relCoords(elem, [[-12,6],[0,-12],[12,6]],[position[0]+31,position[1]])
      if flagType == 'varicap':
        inkDraw.line.relCoords(elem, [[16,0]],[position[0]+31+3,position[1]])
      else:
        inkDraw.line.relCoords(elem, [[19,0]],[position[0]+31,position[1]])
      
      
      if flagType in ['regular','LED','photoDiode']:
        inkDraw.line.relCoords(elem, [[0,12]],[position[0]+31,position[1]-6])
      
      if flagType == 'zener':
        inkDraw.line.relCoords(elem, [[-2,-2],[0,-10],[-2,-2]],[position[0]+31+2,position[1]+5+2])
        
      if flagType == 'schottky':
        inkDraw.line.relCoords(elem, [[0,2],[3,0],[0,-12],[3,0],[0,2]],[position[0]+31-3,position[1]+6-2])
        
      if flagType == 'tunnel':
        inkDraw.line.relCoords(elem, [[3,0],[0,-12],[-3,0]],[position[0]+31-3,position[1]+6])
      
      if flagType == 'varicap':
        inkDraw.line.relCoords(elem, [[0,12]],[position[0]+31,position[1]-6])
        inkDraw.line.relCoords(elem, [[0,12]],[position[0]+34,position[1]-6])
         
    if value!=None:
      
      if flagType=='LED':
        pos_text=[position[0]+25,position[1]-13-self.textOffset]
      if flagType=='photoDiode':
        pos_text=[position[0]+25,position[1]-13-self.textOffset]
      if flagType in ['regular','zener','schottky','tunnel','varicap']:
        pos_text=[position[0]+25,position[1]-6-self.textOffset]
      
      if inkDraw.useLatex:
        value='$'+value +'$'

      inkDraw.text.latex(self,group,value,pos_text,fontSize=self.fontSize,refPoint='bc',preambleFile=self.preambleFile)

    if angleDeg!=0:
      self.rotateElement(group,position,angleDeg)
    
    if flagVolt:
      self.drawVoltArrow(group,[position[0]+25 ,position[1]+7],name=voltName,color=self.voltageColor,angleDeg=angleDeg,invertArrows= not (invertArrows != mirror ))
      
    if flagCurr:
      self.drawCurrArrow(group,[position[0]+40 ,position[1]-5],name=currName,color=self.currentColor,angleDeg=angleDeg,invertArrows=(invertArrows != mirror ))
    
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
    if inkDraw.useLatex:
      value='$'+value +'$'
      
    inkDraw.text.latex(self,group,value,pos_text,fontSize=self.fontSize,refPoint='bc',preambleFile=self.preambleFile)
           
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
    if inkDraw.useLatex:
      value='$'+value +'$'
      
    inkDraw.text.latex(self,group,value,pos_text,fontSize=self.fontSize,refPoint='bc',preambleFile=self.preambleFile)
           
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
    if inkDraw.useLatex:
      value='$'+value +'$'
      
    inkDraw.text.latex(self,group,value,pos_text,fontSize=self.fontSize,refPoint='bc',preambleFile=self.preambleFile)
    
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
    if inkDraw.useLatex:
      value='$'+value +'$'
      
    inkDraw.text.latex(self,group,value,pos_text,fontSize=self.fontSize,refPoint='bc',preambleFile=self.preambleFile)
   
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
    if inkDraw.useLatex:
      value='$'+value +'$'
      
    inkDraw.text.latex(self,group,value,pos_text,fontSize=self.fontSize,refPoint='bc',preambleFile=self.preambleFile)
           
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
    value=gain + '.' + controlName
    
    if inkDraw.useLatex:
      value='$'+value +'$'
      
    inkDraw.text.latex(self,group,value,pos_text,fontSize=self.fontSize,refPoint='bc',preambleFile=self.preambleFile)
           
           
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
    value=gain + '.' + controlName
    
    if inkDraw.useLatex:
      value='$'+value +'$'
      
    inkDraw.text.latex(self,group,value,pos_text,fontSize=self.fontSize,refPoint='bc',preambleFile=self.preambleFile)
    
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
                       drawVin=False,
                       drawIin=False,
                       drawVd=False,
                       drawVout=False,
                       drawIout=False,
                       inputVPosName='v^+',
                       inputVNegName='v^-',
                       inputIPosName='i^+',
                       inputINegName='i^-',
                       VoutName='v_o',
                       IoutName='i_o',
                       VdiffName='v_d',
                       flagDrawSupply=False,
                       FlagSupplyValues=False,
                       flagSupplySymm=True,
                       supplyPositiveVal='V_{cc}',
                       supplyNegativeVal='-V_{cc}'):
    """ draws a general ampOp
    
    parent: parent object
    position: position [x,y]
    label: label of the object (it can be repeated)
    mirrorInput: invert + and - inputs (default: positive above, negative below)
    drawVin: write v+ and v- besides the inputs (default: False)
    drawVd: write vd besides the input terminals
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
      if FlagSupplyValues:
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
      if drawVin:
        textVTop=inputVNegName
        textVBot=inputVPosName
      if drawIin:
        textITop=inputINegName
        textIBot=inputIPosName
    else:
      inkDraw.line.relCoords(elem, [[-3,0]],[position[0]+6,position[1]+10],lineStyle=lineStyleSign)
      inkDraw.line.relCoords(elem, [[-3,0]],[position[0]+6,position[1]-10],lineStyle=lineStyleSign)
      inkDraw.line.relCoords(elem, [[0,3]],[position[0]+4.5,position[1]-11.5],lineStyle=lineStyleSign)
      if drawVin:
        textVTop=inputVPosName
        textVBot=inputVNegName
      if drawIin:
        textITop=inputIPosName
        textIBot=inputINegName
          
    #write v+ v-
    if drawVin:
      posTop=[position[0]-1 ,position[1]-10-self.textOffsetSmall]
      posBot=[position[0]-1 ,position[1]+10-self.textOffsetSmall]
      
      if inkDraw.useLatex:
        textVTop='$'+textVTop+'$'
        textVBot='$'+textVBot+'$'
        
      temp1=inkDraw.text.latex(self,group,textVTop,posTop,textColor=self.voltageColor,fontSize=self.fontSizeSmall,refPoint='br',preambleFile=self.preambleFile)
      temp2=inkDraw.text.latex(self,group,textVBot,posBot,textColor=self.voltageColor,fontSize=self.fontSizeSmall,refPoint='br',preambleFile=self.preambleFile)
        
    #write i+ i-
    if drawIin:
      posTop=[position[0]-7.5 ,position[1]-10+3]
      posBot=[position[0]-7.5 ,position[1]+10+3]
        
      temp1=self.drawCurrArrow(group,posTop,name=textITop,color=self.currentColor,angleDeg=180,invertArrows=False)
      self.rotateElement(temp1,posTop,180)
      temp1=self.drawCurrArrow(group,posBot,name=textIBot,color=self.currentColor,angleDeg=180,invertArrows=False)
      self.rotateElement(temp1,posBot,180)
      
    #write v_out
    if drawVout:
      postext=[position[0]+35,position[1]-self.textOffsetSmall]
      
      if inkDraw.useLatex:
        VoutName='$'+VoutName+'$'
        
      temp1=inkDraw.text.latex(self,group,VoutName,postext,textColor=self.voltageColor,fontSize=self.fontSize,refPoint='bl',preambleFile=self.preambleFile)

    #write i_out
    if drawIout:
      pos=[position[0]+42,position[1]+3]
        
      temp1=self.drawCurrArrow(group,pos,name=IoutName,color=self.currentColor,angleDeg=180,invertArrows=False)
      self.rotateElement(temp1,pos,180)
      
    if drawVd:
      pos1=[position[0]+6 ,position[1]]
      temp1=self.drawVoltArrow(group,pos1,name=VdiffName,color=self.voltageColor,angleDeg=90,invertArrows=not mirrorInput,size=15)
      self.rotateElement(temp1,pos1,90)
      
    return group;
  
  #---------------------------------------------
  #bipolar junction transistors (NPN and PNP)
  def drawTransistorBJT(self,parent,position=[0, 0],angleDeg=0,label='BJT',mirrorEC=False,
                       drawBCEtags=False,
                       drawEnvelope=False,
                       transistorType='NPN',
                       drawVCE=False,
                       drawVCB=False,
                       drawVBE=False,
                       drawICarrow=False,
                       drawIBarrow=False,
                       drawIEarrow=False,
                       VCEname='V_{ce}',
                       VCBname='V_{cb}',
                       VBEname='V_{be}',
                       ICname='i_c',
                       IBname='i_b',
                       IEname='i_e'):
    
    """ draws BJT transisitor
    
    parent: parent object
    label: label of the object (it can be repeated)
    position: position [x,y]
    angleDeg: orientation (default: 0.0)
    mirrorED: invert E and C terminals (default: False (C above, E below)
    drawBCEtags: indentify BCE terminals (default: False)
    drawEnvelope: draw circular envelope (default:False)
    transistorType: type of Bipolar junction transistor values: 'NPN' (Default)  'PNP'
    drawVCE,drawVCB,drawVBE: draw voltage drop annotations (default: False)
    drawICarrow,drawIBarrow,drawIEarrow: draw current annotations (default: False)
    VCEname,VCBname,VBEname: voltage drop annotation text
    ICname,IBname,IEname: current annotation text
    """
    
    if transistorType == 'NPN':
      isNPN=True
    else:
      isNPN=False
    
    group = self.createGroup(parent,label)
    elem = self.createGroup(group,label)
    colorBlack=inkDraw.color.defined('black')
   
    inkDraw.line.relCoords(elem, [[28,0]],[position[0]-10,position[1]])   #base
    inkDraw.line.relCoords(elem, [[0,12]],[position[0]+17.5,position[1]-6],lineStyle=inkDraw.lineStyle.setSimpleBlack(lineWidth=2)) # vertical junction line
    
    # build emitter arrow marker
    L_arrow=2.5
    markerBJT=inkDraw.marker.createMarker(self, 'BJTArrow', 'M 0,0 l -%f,%f l 0,-%f z'% (L_arrow*1.2, L_arrow/2.0,L_arrow), RenameMode=1,
                                          strokeColor=colorBlack, fillColor=colorBlack,lineWidth=0.6)
    lineStyleArrow = inkDraw.lineStyle.set(lineWidth=1, lineColor=colorBlack, markerEnd=markerBJT)
    
    #draw emitter and collector terminals
    if mirrorEC:
      if isNPN:
        inkDraw.line.relCoords(elem, [[7,5],[0,17]],[position[0]+18,position[1]+3]) # emitter
        inkDraw.line.relCoords(elem, [[7,-5]],[position[0]+18,position[1]-3],lineStyle=lineStyleArrow) # emitter arrow
        inkDraw.line.relCoords(elem, [[0,-17]],[position[0]+25,position[1]-8]) # collector
      else:
        inkDraw.line.relCoords(elem, [[7,5],[0,17]],[position[0]+18,position[1]+3]) # emitter
        inkDraw.line.relCoords(elem, [[-7,5]],[position[0]+25,position[1]-8],lineStyle=lineStyleArrow) # emitter arrow
        inkDraw.line.relCoords(elem, [[0,-17]],[position[0]+25,position[1]-8]) # collector
      pos_Etag=[position[0]+22.5,position[1]-12.5]
      pos_Ctag=[position[0]+22.5,position[1]+12.5]
    else:
      if isNPN:
        inkDraw.line.relCoords(elem, [[7,-5],[0,-17]],[position[0]+18,position[1]-3]) # collector
        inkDraw.line.relCoords(elem, [[7,5]],[position[0]+18,position[1]+3],lineStyle=lineStyleArrow) # emitter arrow
        inkDraw.line.relCoords(elem, [[0,17]],[position[0]+25,position[1]+8]) # emitter
      else:
        inkDraw.line.relCoords(elem, [[7,-5],[0,-17]],[position[0]+18,position[1]-3]) # collector
        inkDraw.line.relCoords(elem, [[-7,-5]],[position[0]+25,position[1]+8],lineStyle=lineStyleArrow) # emitter arrow
        inkDraw.line.relCoords(elem, [[0,17]],[position[0]+25,position[1]+8]) # emitter
      pos_Ctag=[position[0]+22.5,position[1]-12.5]
      pos_Etag=[position[0]+22.5,position[1]+12.5]
    
    if drawEnvelope:
      inkDraw.circle.centerRadius(elem, centerPoint=[position[0]+22,position[1]], radius=10, offset=[0, 0], label='circle')
      
    if drawBCEtags:
      tB=inkDraw.text.latex(self,group,'B',position=[position[0]+10,position[1]-3],fontSize=self.fontSizeSmall/1.5,refPoint='cc',preambleFile=self.preambleFile,angleDeg=-angleDeg)
      tC=inkDraw.text.latex(self,group,'C',position=pos_Ctag,fontSize=self.fontSizeSmall/1.5,refPoint='cc',preambleFile=self.preambleFile,angleDeg=-angleDeg)
      tE=inkDraw.text.latex(self,group,'E',position=pos_Etag,fontSize=self.fontSizeSmall/1.5,refPoint='cc',preambleFile=self.preambleFile,angleDeg=-angleDeg)
        
      
    if angleDeg!=0:
      self.rotateElement(group,position,angleDeg)
      
    #draw voltage drops
    if drawVCE:
      pos=[position[0]+25+10 ,position[1]]
      self.drawVoltArrowSimple(group,pos,name=VCEname,color=self.voltageColor,angleDeg=90,invertArrows=mirrorEC,size=20.0,invertCurvatureDirection=False,extraAngleText=angleDeg)
    
    if drawVCB:
      if mirrorEC:
        pos = [position[0]+12,position[1]+12]
        ang = -45
      else:
        pos = [position[0]+12,position[1]-12]
        ang = 45
        
      self.drawVoltArrowSimple(group,pos,name=VCBname,color=self.voltageColor,angleDeg=ang,invertArrows=False,size=20.0,invertCurvatureDirection=not mirrorEC,extraAngleText=angleDeg)
 
    if drawVBE:
      if mirrorEC:
        pos = [position[0]+12,position[1]-12]
        ang = 45
      else:
        pos = [position[0]+12,position[1]+12]
        ang = -45

      self.drawVoltArrowSimple(group,pos,name=VBEname,color=self.voltageColor,angleDeg= ang,invertArrows=True,size=20.0,invertCurvatureDirection= mirrorEC,extraAngleText=angleDeg)


    # draw terminal currents
    if drawICarrow:
      if mirrorEC:
        self.drawCurrArrowSimple(group,[position[0]+30 ,position[1]+17.5],name=ICname,color=self.currentColor,
                                angleDeg=90,invertArrows=not isNPN,size=7.5,invertTextSide=True,extraAngleText=angleDeg)
      else:
        self.drawCurrArrowSimple(group,[position[0]+30 ,position[1]-17.5],name=ICname,color=self.currentColor,
                                angleDeg=90,invertArrows=isNPN,size=7.5,invertTextSide=True,extraAngleText=angleDeg)
      
    if drawIBarrow:
      self.drawCurrArrowSimple(group,[position[0]+7.5-10 ,position[1]-5],name=IBname,color=self.currentColor,
                               angleDeg=0,invertArrows=not isNPN,size=7.5,invertTextSide=False,extraAngleText=angleDeg) 
      
    if drawIEarrow:
      if mirrorEC:
        self.drawCurrArrowSimple(group,[position[0]+30 ,position[1]-17.5],name=IEname,color=self.currentColor,
                                 angleDeg=90,invertArrows=not isNPN,size=7.5,invertTextSide=True,extraAngleText=angleDeg) 
      else:
        self.drawCurrArrowSimple(group,[position[0]+30 ,position[1]+17.5],name=IEname,color=self.currentColor,
                                angleDeg=90,invertArrows=isNPN,size=7.5,invertTextSide=True,extraAngleText=angleDeg)
    return group;
  
  #---------------------------------------------
  #metal-oxide-semiconductor field-effect transistor (N and P channel)
  def drawTransistorMOSFET(self,parent,position=[0, 0],angleDeg=0,label='MOSFET',mirrorSD=False,
                          drawSGDtags=False,
                          drawEnvelope=False,
                          modeType='MOSFET-E',
                          gateType='P_gate',
                          bodyDiode=False,
                          drawVGS=False,
                          drawVDS=False,
                          drawVDG=False,
                          drawIDarrow=False,
                          drawISarrow=False,
                          drawIGarrow=False,
                          VGSname='V_{GS}',
                          VDSname='V_{SD}',
                          VDGname='V_{GD}',
                          IDname='i_d',
                          ISname='i_s',
                          IGname='i_g'):
         
    """ draws a general Field Effect transistor
    
    parent: parent object
    label: label of the object (it can be repeated)
    position: position [x,y]
    angleDeg: orientation (default: 0.0)
    mirrorSD: invert S and D terminals (default: False (D above, S below)
    drawSGDtags: indentify SGD terminals (default: False)
    drawEnvelope: draw circular envelope (default:False)
    modeType: type of field effect transistor: 'MOSFET-E' (Default)  'MOSFET_P'
    gateType: type of gate: 'P_gate',  'N_gate'
    bodyDiode: draws body diode (MOSFET-E only)
    drawVGS,drawVDS,drawVDG: draw voltage drop annotations (default: False)
    drawIDarrow,drawISarrow,drawIGarrow: draw current annotations (default: False)
    VGSname,VDSname,VDGname: voltage drop annotation text
    IDname,ISname,IGname: current annotation text
    """
    
    if gateType == 'P_gate':
      isNgate=False
    else:
      isNgate=True
    
    if modeType == 'MOSFET-E':
      isEmode=True
    else:
      isEmode=False

    group = self.createGroup(parent,label)
    elem = self.createGroup(group,label)
    colorBlack=inkDraw.color.defined('black')

    L_arrow=2.0
    markerMOS=inkDraw.marker.createMarker(self, 'MOSArrow', 'M -0.3,0 l -%f,%f l 0,-%f z'% (L_arrow*1.2, L_arrow/2.0,L_arrow), RenameMode=1,
                                          strokeColor=colorBlack, fillColor=colorBlack, lineWidth=0.6)
    lineStyleArrow = inkDraw.lineStyle.set(lineWidth=0.7, lineColor=colorBlack, markerEnd=markerMOS)
    lineStyleFine = inkDraw.lineStyle.set(lineWidth=0.7, lineColor=colorBlack)

    if mirrorSD:
      inkDraw.line.relCoords(elem, [[0,-12],[-28,0]],[position[0]+17,position[1]+6])   #gate
      
      if bodyDiode and isEmode:
        inkDraw.line.relCoords(elem, [[0,18.75]],[position[0]+24,position[1]+5.25]) # drain line
      else:
        inkDraw.line.relCoords(elem, [[0,18.6]],[position[0]+24,position[1]+5.4]) # drain line
      inkDraw.line.relCoords(elem, [[5,0],[0,5.25]],[position[0]+19,position[1]+5.25],lineStyle=lineStyleFine) # drain line
      
      inkDraw.line.relCoords(elem, [[0,-20.75]],[position[0]+24,position[1]-5.25]) # source line
      inkDraw.line.relCoords(elem, [[5,0],[0,5.25]],[position[0]+19,position[1]-5.25],lineStyle=lineStyleFine) # source line
      
      inkDraw.circle.centerRadius(elem, [position[0]+24,position[1]-5.25], radius=0.4, offset=[0, 0], label='circle') # source dot
      if isNgate:
        inkDraw.line.relCoords(elem, [[-5,0]],[position[0]+24,position[1]+0],lineStyle=lineStyleArrow) # horizontal arrow line 
      else:
        inkDraw.line.relCoords(elem, [[5,0]],[position[0]+19,position[1]+0],lineStyle=lineStyleArrow) # horizontal arrow line 

      if bodyDiode and isEmode:
        inkDraw.circle.centerRadius(elem, [position[0]+24,position[1]+5.25], radius=0.4, offset=[0, 0], label='circle') # diode cathode dot
        inkDraw.line.relCoords(elem, [[4,0],[0,-3.75]],[position[0]+24,position[1]+5.25],lineStyle=lineStyleFine) # diode cathode
        inkDraw.line.relCoords(elem, [[4,0],[0, 3.75]],[position[0]+24,position[1]-5.25],lineStyle=lineStyleFine) # diode anode
        
        if isNgate:
          inkDraw.line.relCoords(elem, [[3,0]],[position[0]+26.5,position[1]+1.5],lineStyle=lineStyleFine) # diode cathode side line
          inkDraw.line.relCoords(elem, [[3,0],[-1.5, 3],[-1.5,-3]],[position[0]+26.5,position[1]-1.5],lineStyle=lineStyleFine) # diode
        else:
          inkDraw.line.relCoords(elem, [[3,0]],[position[0]+26.5,position[1]-1.5],lineStyle=lineStyleFine) # diode cathode side line
          inkDraw.line.relCoords(elem, [[3,0],[-1.5,-3],[-1.5, 3]],[position[0]+26.5,position[1]+1.5],lineStyle=lineStyleFine) # diode

        pos_Gtag=[position[0]+9,position[1]-3]
        pos_Dtag=[position[0]+26.5,position[1]+12.5]
        pos_Stag=[position[0]+26.5,position[1]-12.5]
      else:
        pos_Gtag=[position[0]+7,position[1]-3]
        pos_Dtag=[position[0]+26.5,position[1]+11.5]
        pos_Stag=[position[0]+26.5,position[1]-11.5]
        
    else:
      inkDraw.line.relCoords(elem, [[0,12],[-28,0]],[position[0]+17,position[1]-6])   #gate

      if bodyDiode and isEmode:
        inkDraw.line.relCoords(elem, [[0,-18.75]],[position[0]+24,position[1]-5.25]) # drain line
      else:
        inkDraw.line.relCoords(elem, [[0,-18.6]],[position[0]+24,position[1]-5.4]) # drain line

      inkDraw.line.relCoords(elem, [[5,0],[0,-5.25]],[position[0]+19,position[1]-5.25],lineStyle=lineStyleFine) # drain line
      
      inkDraw.line.relCoords(elem, [[0,20.75]],[position[0]+24,position[1]+5.25]) # source line
      inkDraw.line.relCoords(elem, [[5,0],[0,-5.25]],[position[0]+19,position[1]+5.25],lineStyle=lineStyleFine) # source line

      inkDraw.circle.centerRadius(elem, [position[0]+24,position[1]+5.25], radius=0.4, offset=[0, 0], label='circle') # source dot
      if isNgate:
        inkDraw.line.relCoords(elem, [[-5,0]],[position[0]+24,position[1]+0],lineStyle=lineStyleArrow) # horizontal arrow line 
      else:
        inkDraw.line.relCoords(elem, [[5,0]],[position[0]+19,position[1]+0],lineStyle=lineStyleArrow) # horizontal arrow line 

      if bodyDiode and isEmode:
        inkDraw.circle.centerRadius(elem, [position[0]+24,position[1]-5.25], radius=0.4, offset=[0, 0], label='circle') # diode cathode dot
        inkDraw.line.relCoords(elem, [[4,0],[0, 3.75]],[position[0]+24,position[1]-5.25],lineStyle=lineStyleFine) # diode cathode
        inkDraw.line.relCoords(elem, [[4,0],[0,-3.75]],[position[0]+24,position[1]+5.25],lineStyle=lineStyleFine) # diode anode
        
        if isNgate:
            inkDraw.line.relCoords(elem, [[3,0]],[position[0]+26.5,position[1]-1.5],lineStyle=lineStyleFine) # diode cathode side line
            inkDraw.line.relCoords(elem, [[3,0],[-1.5,-3],[-1.5,3]],[position[0]+26.5,position[1]+1.5],lineStyle=lineStyleFine) # diode
        else:
            inkDraw.line.relCoords(elem, [[3,0]],[position[0]+26.5,position[1]+1.5],lineStyle=lineStyleFine) # diode cathode side line
            inkDraw.line.relCoords(elem, [[3,0],[-1.5,3],[-1.5,-3]],[position[0]+26.5,position[1]-1.5],lineStyle=lineStyleFine) # diode

        pos_Gtag=[position[0]+9,position[1]+3]
        pos_Dtag=[position[0]+26.5,position[1]-12.5]
        pos_Stag=[position[0]+26.5,position[1]+12.5]
      else:
        pos_Gtag=[position[0]+7,position[1]+3]
        pos_Dtag=[position[0]+26.5,position[1]-11.5]
        pos_Stag=[position[0]+26.5,position[1]+11.5]
            
    if isEmode:
      # enhancement-mode line
      inkDraw.line.relCoords(elem, [[0,3.5]],[position[0]+19,position[1]-7],lineStyle=lineStyleFine) #vertical gate line
      inkDraw.line.relCoords(elem, [[0,3.5]],[position[0]+19,position[1]-1.75],lineStyle=lineStyleFine) #vertical gate line
      inkDraw.line.relCoords(elem, [[0,3.5]],[position[0]+19,position[1]+3.5],lineStyle=lineStyleFine) #vertical gate line
    else:
      inkDraw.line.relCoords(elem, [[0,14]],[position[0]+19,position[1]-7],lineStyle=lineStyleFine) #vertical gate line
      
    if drawEnvelope:
      if bodyDiode and isEmode:
        inkDraw.circle.centerRadius(elem, centerPoint=[position[0]+22,position[1]], radius=10, offset=[0, 0], label='circle')
      else:
        inkDraw.circle.centerRadius(elem, centerPoint=[position[0]+20,position[1]], radius=10, offset=[0, 0], label='circle')

    if drawSGDtags:
      tB=inkDraw.text.latex(self,group,'G',position=pos_Gtag,fontSize=self.fontSizeSmall/1.5,refPoint='cc',preambleFile=self.preambleFile,angleDeg=-angleDeg)
      tC=inkDraw.text.latex(self,group,'D',position=pos_Dtag,fontSize=self.fontSizeSmall/1.5,refPoint='cc',preambleFile=self.preambleFile,angleDeg=-angleDeg)
      tE=inkDraw.text.latex(self,group,'S',position=pos_Stag,fontSize=self.fontSizeSmall/1.5,refPoint='cc',preambleFile=self.preambleFile,angleDeg=-angleDeg)
            
    if angleDeg!=0:
      self.rotateElement(group,position,angleDeg)
      
    #draw voltage drops
    if drawVDS:
      pos=[position[0]+25+10 ,position[1]]
      self.drawVoltArrowSimple(group,pos,name=VDSname,color=self.voltageColor,angleDeg=90,
                               invertArrows=mirrorSD ,size=20.0,invertCurvatureDirection=False,extraAngleText=angleDeg)
    
    if drawVGS:
      if mirrorSD:
        pos = [position[0]+15,position[1]-14]
        ang = +19
      else:
        pos = [position[0]+15,position[1]+14]
        ang = -19
      self.drawVoltArrowSimple(group,pos,name=VGSname,color=self.voltageColor,angleDeg=ang,
                               invertArrows=True, size=10.0,  invertCurvatureDirection=mirrorSD, extraAngleText=angleDeg)

    if drawVDG:
      if mirrorSD:
        pos = [position[0]+10,position[1]+8]
        ang = -45
      else:
        pos = [position[0]+10,position[1]-8]
        ang = 45
      self.drawVoltArrowSimple(group,pos,name=VDGname,color=self.voltageColor,angleDeg= ang,
                                invertArrows= False,size=20.0,invertCurvatureDirection=not mirrorSD,extraAngleText=angleDeg)
          
    # draw terminal currents
    if drawISarrow:
      if mirrorSD:
        pos = [position[0]+29 ,position[1]-17.5]
      else:
        pos = [position[0]+29 ,position[1]+17.5]

      self.drawCurrArrowSimple(group,pos,name=ISname,color=self.currentColor,
                              angleDeg=90,invertArrows=not mirrorSD,size=7.5,invertTextSide=True,extraAngleText=angleDeg)
     
    if drawIGarrow:
      if mirrorSD:
        pos = [position[0]-5 ,position[1]-11]
      else:
        pos = [position[0]-5 ,position[1]+11]

      self.drawCurrArrowSimple(group,pos,name=IGname,color=self.currentColor,
                               angleDeg=0,invertArrows=False,size=7.5,invertTextSide=not mirrorSD,extraAngleText=angleDeg) 

    if drawIDarrow:
      if mirrorSD:
        pos = [position[0]+29 ,position[1]+17.5]
      else:
        pos = [position[0]+29 ,position[1]-17.5]
      self.drawCurrArrowSimple(group,pos,name=IDname,color=self.currentColor,
                                 angleDeg=90,invertArrows=not mirrorSD,size=7.5,invertTextSide=True,extraAngleText=angleDeg) 

    return group;
  
  #---------------------------------------------
  #junction gate field-effect transistor (N and P channel)
  def drawTransistorJFET(self,parent,position=[0, 0],angleDeg=0,label='JFET',mirrorSD=False,
                        drawSGDtags=False,
                        drawEnvelope=False,
                        gateType='P_gate',
                        moveGate=False,
                        drawVGS=False,
                        drawVDS=False,
                        drawVDG=False,
                        drawIDarrow=False,
                        drawISarrow=False,
                        drawIGarrow=False,
                        VGSname='V_{GS}',
                        VDSname='V_{SD}',
                        VDGname='V_{GD}',
                        IDname='i_d',
                        ISname='i_s',
                        IGname='i_g'):
         
    """ draws a junction gate field-effect transistor JFET
    
    parent: parent object
    label: label of the object (it can be repeated)
    position: position [x,y]
    angleDeg: orientation (default: 0.0)
    mirrorSD: invert S and D terminals (default: False (D above, S below)
    drawSGDtags: indentify SGD terminals (default: False)
    drawEnvelope: draw circular envelope (default:False)
    transistorType: type of field effect transistor: 'MOSFET-E' (Default)  'MOSFET_P'
    gateType: type of gate: 'P_gate',  'N_gate'
    moveGate: move gate terminar towards the source
    drawVGS,drawVDS,drawVDG: draw voltage drop annotations (default: False)
    drawIDarrow,drawISarrow,drawIGarrow: draw current annotations (default: False)
    VGSname,VDSname,VDGname: voltage drop annotation text
    IDname,ISname,IGname: current annotation text
    """
    
    if gateType == 'P_gate':
      isNgate=False
    else:
      isNgate=True

    group = self.createGroup(parent,label)
    elem = self.createGroup(group,label)
    colorBlack=inkDraw.color.defined('black')

    R_circle=10.0
    L_arrow=2.0
    markerMOS=inkDraw.marker.createMarker(self, 'MOSArrow', 'M -0.3,0 l -%f,%f l 0,-%f z'% (L_arrow*1.2, L_arrow/2.0,L_arrow), RenameMode=1,
                                          strokeColor=colorBlack, fillColor=colorBlack, lineWidth=0.6)
    lineStyleArrow = inkDraw.lineStyle.set(lineWidth=1.0, lineColor=colorBlack, markerEnd=markerMOS)

    inkDraw.line.relCoords(elem, [[6,0],[0,20]],[position[0]+17,position[1]+5.0]) # source line
    inkDraw.line.relCoords(elem, [[6,0],[0,-20]],[position[0]+17,position[1]-5.0]) # drain line
    
    inkDraw.line.relCoords(elem, [[0,14]],[position[0]+17,position[1]-7],lineStyle=inkDraw.lineStyle.setSimpleBlack(lineWidth=2)) # vertical junction line

    
    if moveGate:
      if mirrorSD:
        posG_Y=-5
      else:
        posG_Y=5
    else:
      posG_Y=0
    
    theta=math.asin(posG_Y/R_circle)
    P1=[10+R_circle*(1-math.cos(theta)),posG_Y]
    P2=[10+R_circle-3,posG_Y]
  
    inkDraw.line.absCoords(elem, [[-12,posG_Y],P1],position)                                    #gate terminal

    if isNgate:
      inkDraw.line.absCoords(elem, [P1,P2],position,lineStyle=lineStyleArrow)   #gate arrow  -->
    else:
      inkDraw.line.absCoords(elem, [P2,P1],position,lineStyle=lineStyleArrow)   #gate arrow   <--
      
    if drawEnvelope:
      inkDraw.circle.centerRadius(elem, centerPoint=[position[0]+19,position[1]], radius=10, offset=[0, 0], label='circle')

    if drawSGDtags:
      if mirrorSD:
        pos_Gtag=[position[0]+6,position[1]+3+posG_Y]
        pos_Dtag=[position[0]+25.5,position[1]+11.5]
        pos_Stag=[position[0]+25.5,position[1]-11.5]
        
      else:
        pos_Gtag=[position[0]+6,position[1]-3+posG_Y]
        pos_Dtag=[position[0]+25.5,position[1]-11.5]
        pos_Stag=[position[0]+25.5,position[1]+11.5]
        
      tB=inkDraw.text.latex(self,group,'G',position=pos_Gtag,fontSize=self.fontSizeSmall/1.5,refPoint='cc',preambleFile=self.preambleFile,angleDeg=-angleDeg)
      tC=inkDraw.text.latex(self,group,'D',position=pos_Dtag,fontSize=self.fontSizeSmall/1.5,refPoint='cc',preambleFile=self.preambleFile,angleDeg=-angleDeg)
      tE=inkDraw.text.latex(self,group,'S',position=pos_Stag,fontSize=self.fontSizeSmall/1.5,refPoint='cc',preambleFile=self.preambleFile,angleDeg=-angleDeg)
            
    if angleDeg!=0:
      self.rotateElement(group,position,angleDeg)
      
    #draw voltage drops
    if drawVDS:
      pos=[position[0]+25+9 ,position[1]]
      self.drawVoltArrowSimple(group,pos,name=VDSname,color=self.voltageColor,angleDeg=90,
                               invertArrows=mirrorSD ,size=20.0,invertCurvatureDirection=False,extraAngleText=angleDeg)
    
    if drawVGS:
      if mirrorSD:
        if moveGate:
          pos = [position[0]+15,position[1]-13]
          ang = 19
          L = 10
        else:
          pos = [position[0]+12,position[1]-11]
          ang = +30
          L = 15
      else:
        if moveGate:
          pos = [position[0]+15,position[1]+13]
          ang = -19
          L = 10
        else:
          pos = [position[0]+12,position[1]+11]
          ang = -30
          L = 15
      self.drawVoltArrowSimple(group,pos,name=VGSname,color=self.voltageColor,angleDeg=ang,
                               invertArrows=True, size=L,  invertCurvatureDirection=mirrorSD, extraAngleText=angleDeg)

    if drawVDG:
      if mirrorSD:
        if moveGate:
          pos = [position[0]+12,position[1]+9]
          ang = -45
          L = 20
        else:
          pos = [position[0]+12,position[1]+11]
          ang = -30
          L = 15
      else:
        if moveGate:
          pos = [position[0]+12,position[1]-9]
          ang = 45
          L = 20
        else:
          pos = [position[0]+12,position[1]-11]
          ang = 30
          L = 15
      self.drawVoltArrowSimple(group,pos,name=VDGname,color=self.voltageColor,angleDeg= ang,
                                invertArrows= False,size=L,invertCurvatureDirection=not mirrorSD,extraAngleText=angleDeg)
          
    # draw terminal currents
    if drawISarrow:
      if mirrorSD:
        pos = [position[0]+28 ,position[1]-17.5]
      else:
        pos = [position[0]+28 ,position[1]+17.5]

      self.drawCurrArrowSimple(group,pos,name=ISname,color=self.currentColor,
                              angleDeg=90,invertArrows=not mirrorSD,size=7.5,invertTextSide=True,extraAngleText=angleDeg)
     
    if drawIGarrow:
      if mirrorSD:
        pos = [position[0]-5 ,position[1]+posG_Y-5]
      else:
        pos = [position[0]-5 ,position[1]+posG_Y+5]

      self.drawCurrArrowSimple(group,pos,name=IGname,color=self.currentColor,
                               angleDeg=0,invertArrows=False,size=7.5,invertTextSide=not mirrorSD,extraAngleText=angleDeg) 

    if drawIDarrow:
      if mirrorSD:
        pos = [position[0]+28 ,position[1]+17.5]
      else:
        pos = [position[0]+28 ,position[1]-17.5]
      self.drawCurrArrowSimple(group,pos,name=IDname,color=self.currentColor,
                                 angleDeg=90,invertArrows=not mirrorSD,size=7.5,invertTextSide=True,extraAngleText=angleDeg) 

    return group;
    
    
  #---------------------------------------------
  def drawSwitch2T(self,parent,position=[0, 0],value='S',label='Switch',angleDeg=0,flagOpen=True,flagDrawArrow=False,OpenCloseText=''):
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
        
        if inkDraw.useLatex:
          OpenCloseText='$'+OpenCloseText +'$'
          
        inkDraw.text.latex(self,group,OpenCloseText,pos_text,fontSize=self.fontSize,refPoint='tc',preambleFile=self.preambleFile)

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
      if inkDraw.useLatex:
        value='$'+value +'$'
        
      inkDraw.text.latex(self,group,value,pos_text,fontSize=self.fontSize,refPoint='bc',preambleFile=self.preambleFile)
      
    if angleDeg!=0:
      self.rotateElement(group,position,angleDeg)
         
    return group;
    
  #---------------------------------------------
  
  def drawVoltArrowSimple(self,parent,position,label='arrowV',name='v',color=inkDraw.color.defined('black'),
                          angleDeg=0,invertArrows=False,size=20.0,invertCurvatureDirection=False,extraAngleText=0.0):
                                
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
    extraAngleText: extra angle (in degrees) added to the text. (default: 0.0)
    """
    
    if invertCurvatureDirection:
      arrow_elem=self.drawVoltArrow(parent,position,label,name,color,angleDeg+180, invertArrows,size,extraAngleText)
      self.rotateElement(arrow_elem,position,angleDeg+180)
    else:
      arrow_elem=self.drawVoltArrow(parent,position,label,name,color,angleDeg    ,not invertArrows,    size,extraAngleText)
      self.rotateElement(arrow_elem,position,angleDeg)

  #---------------------------------------------
  
  def drawVoltArrow(self,parent,position,label='name',name='v',color=inkDraw.color.defined('black'),angleDeg=0,invertArrows=False,size=20.0,extraAngleText=0.0):
    """ draws a voltage drop arrow
    
    parent: parent object
    position: position [x,y]
    label: label of the object (it can be repeated)
    name: string with namee. (default 'v')
    color: color of the arrow and text
    invertArrows: invert current direction
    size: size of the arrow
    extraAngleText: extra angle (in degrees) added to the text. (default: 0.0)
    """
    
    group = self.createGroup(parent,label)
    
    scale=size/20.0  # the default size was 20 height
    
    renameMode=0   #0: do not modify  1: overwrite  2:rename
    #make linestyle
    [arrowStartVolt,arrowEndVolt] = inkDraw.marker.createArrow1Marker(self,'arrowVoltage',RenameMode=renameMode,scale=0.25,strokeColor=color,fillColor=color)
    
    if invertArrows:
      lineStyle = inkDraw.lineStyle.set(lineColor=color,markerStart=arrowStartVolt);
    else:
      lineStyle = inkDraw.lineStyle.set(lineColor=color,markerEnd=arrowEndVolt);
    
    radius=30.0*scale
    h=10.0*scale
    halfTheta=math.asin(h/radius)
    inkDraw.arc.startEndRadius(group, [h,0], [-h,0], radius, position,lineStyle=lineStyle,flagRightOf=False)
      
    # get appropriate refPoint based on the angle
    theta=angleDeg+extraAngleText
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
                  if theta<=340:
                    justif='tr'
                  else:
                    justif='tc'
                  
    centerY=-radius*math.cos(halfTheta)
    posY=centerY+radius
    
    if not name == '':
      if inkDraw.useLatex:
        name='$'+name + '$'
        dist=4.0
      else:
        dist=3.0
      inkDraw.text.latex(self,group,name,[position[0],position[1]+posY+dist],fontSize=self.fontSize,
                         refPoint=justif,textColor=color,angleDeg=-theta,preambleFile=self.preambleFile)
          
    return group

  #---------------------------------------------
  
  def drawCurrArrowSimple(self,parent,position,label='arrowI',name='',color=inkDraw.color.defined('black'),
                          angleDeg=0,invertArrows=False,size=20.0,invertTextSide=False,extraAngleText=0.0):
                                
    """ draws a current arrow
    
    parent: parent object
    position: position [x,y]
    label: label of the object (it can be repeated)
    name: string with namee. (default none)
    color: color of the arrow and text
    angleDeg: rotation angle in degrees counter-clockwise (default 0)
    invertArrows: invert current direction
    size: size of the arrow
    invertTextSide: invert side of the text in relation to the arrow
    extraAngleText: extra angle (in degrees) added to the text. (default: 0.0)
    """
      
    #control signal
    if invertTextSide:
      temp1=self.drawCurrArrow(parent,position,label,name,color=self.currentColor,angleDeg=angleDeg+180,invertArrows=invertArrows,size=size,extraAngleText=extraAngleText)    
      self.rotateElement(temp1,position,angleDeg+180)
    else:
      temp1=self.drawCurrArrow(parent,position,label,name,color=self.currentColor,angleDeg=angleDeg,invertArrows=not invertArrows,size=size,extraAngleText=extraAngleText)    
      self.rotateElement(temp1,position,angleDeg)
      
      
  #---------------------------------------------
  def drawCurrArrow(self,parent,position,label='name',name='i',color=inkDraw.color.defined('black'),angleDeg=0,invertArrows=False,size=10.0,extraAngleText=0.0):
    """ draws a current arrow
    
    parent: parent object
    position: position [x,y]
    label: label of the object (it can be repeated)
    name: string with namee. (default 'v')
    color: color of the arrow and text
    angleDeg: rotation angle in degrees
    invertArrows: invert current direction
    size: size of the arrow
    extraAngleText: extra angle (in degrees) added to the text. (default: 0.0)
    """
    scale=size/10.0
    group = self.createGroup(parent,label)
    renameMode=0   #0: do not modify  1: overwrite  2:rename
        
    #make linestyle
    [arrowStartCurr,arrowEndCurr] = inkDraw.marker.createArrow1Marker(self,'arrowCurrent',RenameMode=renameMode,scale=0.25,strokeColor=color,fillColor=color)
    lineStyle = inkDraw.lineStyle.set(lineColor=color,markerEnd=arrowEndCurr);
    
    if invertArrows:
      inkDraw.line.relCoords(group, [[10*scale,0]], [position[0]-5*scale,position[1]], label='none', lineStyle=lineStyle)
    else:
      inkDraw.line.relCoords(group, [[-10*scale,0]], [position[0]+5*scale,position[1]], label='none', lineStyle=lineStyle)
    
    # get appropriate refPoint based on the angle
    theta=angleDeg+extraAngleText
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
    
    
    if inkDraw.useLatex:
      name='$'+name + '$'
        
    inkDraw.text.latex(self,group,name,[position[0],position[1]-self.textOffset*0.8],fontSize=self.fontSize,refPoint=justif,textColor=color,angleDeg=-theta,preambleFile=self.preambleFile)
    
    return group
if __name__ == '__main__':
  circuit = CircuitSymbols()
  circuit.affect()
    
