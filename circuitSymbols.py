#!/usr/bin/python

import math
import os

import inkscapeMadeEasy_Base as inkBase
import inkscapeMadeEasy_Draw as inkDraw
from drawAmpOp import ampOp
from drawArrows import arrow
from drawDiodes import diode
from drawRLC import RLC
from drawSignals import signal
from drawSources import source
from drawSwitches import switch
from drawTransistors import transistor

# some symbol definition

OhmChar = u'\u2126'.encode('utf-8')


# package needed:  steinmetz

def latexUnitMultiple(valueString):
    if valueString[-1] == 'M':
        return valueString.replace('M', r'\si\mega')

    if valueString[-1] == 'k':
        return valueString.replace('k', r'\si\kilo')

    if valueString[-1] == 'm':
        return valueString.replace('m', r'\si\milli')

    if valueString[-1] == 'u':
        return valueString.replace('u', r'\micro')

    if valueString[-1] == 'n':
        return valueString.replace('n', r'\si\nano')

    if valueString[-1] == 'p':
        return valueString.replace('p', r'\si\pico')

    return valueString


# ---------------------------------------------
class CircuitSymbols(RLC, source, transistor, signal, arrow, ampOp, diode, switch):
    def __init__(self):
        inkBase.inkscapeMadeEasy.__init__(self)

        self.OptionParser.add_option("--tab", action="store", type="string", dest="tab", default="object")

        self.OptionParser.add_option("--bipoleRLC", action="store", type="string", dest="bipoleRLC", default='resistor')
        self.OptionParser.add_option("--bipoleRLCVal", action="store", type="string", dest="bipoleRLCVal", default='Z')
        self.OptionParser.add_option("--bipoleRLCUnit", action="store", type="inkbool", dest="bipoleRLCUnit", default=False)
        self.OptionParser.add_option("--bipoleRLCRot", action="store", type="string", dest="bipoleRLCRot", default='0')
        self.OptionParser.add_option("--bipoleRLCconvention", action="store", type="string", dest="bipoleRLCconvention", default='passive')
        self.OptionParser.add_option("--bipoleRLCVolt", action="store", type="inkbool", dest="bipoleRLCVolt", default=True)
        self.OptionParser.add_option("--bipoleRLCCurr", action="store", type="inkbool", dest="bipoleRLCCurr", default=True)
        self.OptionParser.add_option("--bipoleRLCVoltName", action="store", type="string", dest="bipoleRLCVoltName", default='v')
        self.OptionParser.add_option("--bipoleRLCCurrName", action="store", type="string", dest="bipoleRLCCurrName", default='i')
        self.OptionParser.add_option("--bipoleRLCVoltCurrInvert", action="store", type="inkbool", dest="bipoleRLCVoltCurrInvert", default=True)

        self.OptionParser.add_option("--source", action="store", type="string", dest="source", default='voltIndep')
        self.OptionParser.add_option("--sourceVal", action="store", type="string", dest="sourceVal", default='E')
        self.OptionParser.add_option("--sourceUnit", action="store", type="inkbool", dest="sourceUnit", default=False)
        self.OptionParser.add_option("--sourceRot", action="store", type="string", dest="sourceRot", default='0')
        self.OptionParser.add_option("--sourceConvention", action="store", type="string", dest="sourceConvention", default='active')
        self.OptionParser.add_option("--sourceVolt", action="store", type="inkbool", dest="sourceVolt", default=True)
        self.OptionParser.add_option("--sourceCurr", action="store", type="inkbool", dest="sourceCurr", default=True)
        self.OptionParser.add_option("--sourceVoltName", action="store", type="string", dest="sourceVoltName", default='v')
        self.OptionParser.add_option("--sourceCurrName", action="store", type="string", dest="sourceCurrName", default='i')
        self.OptionParser.add_option("--sourceVoltCurrInvert", action="store", type="inkbool", dest="sourceVoltCurrInvert", default=True)
        self.OptionParser.add_option("--sourceMirror", action="store", type="inkbool", dest="sourceMirror", default=False)

        self.OptionParser.add_option("--sourceControlled", action="store", type="string", dest="sourceControlled", default='volt')
        self.OptionParser.add_option("--sourceControlledType", action="store", type="string", dest="sourceControlledType", default='curr')
        self.OptionParser.add_option("--sourceControlledGain", action="store", type="string", dest="sourceControlledGain", default='k')
        self.OptionParser.add_option("--sourceControlledControlName", action="store", type="string", dest="sourceControlledControlName", default='v_c')
        self.OptionParser.add_option("--sourceControlledRot", action="store", type="string", dest="sourceControlledRot", default='0')
        self.OptionParser.add_option("--sourceControlledConvention", action="store", type="string", dest="sourceControlledConvention", default='active')
        self.OptionParser.add_option("--sourceControlledVolt", action="store", type="inkbool", dest="sourceControlledVolt", default=True)
        self.OptionParser.add_option("--sourceControlledCurr", action="store", type="inkbool", dest="sourceControlledCurr", default=True)
        self.OptionParser.add_option("--sourceControlledVoltName", action="store", type="string", dest="sourceControlledVoltName", default='v')
        self.OptionParser.add_option("--sourceControlledCurrName", action="store", type="string", dest="sourceControlledCurrName", default='i')
        self.OptionParser.add_option("--sourceControlledVoltCurrInvert", action="store", type="inkbool", dest="sourceControlledVoltCurrInvert", default=True)
        self.OptionParser.add_option("--sourceControlledMirror", action="store", type="inkbool", dest="sourceControlledMirror", default=False)
        self.OptionParser.add_option("--sourceControlledDrawArrow", action="store", type="inkbool", dest="sourceControlledDrawArrow", default=False)

        self.OptionParser.add_option("--switchPoles", action="store", type="int", dest="switchPoles", default=1)
        self.OptionParser.add_option("--switchThrows", action="store", type="int", dest="switchThrows", default=1)
        self.OptionParser.add_option("--switchPushButton", action="store", type="inkbool", dest="switchPushButton", default=False)
        self.OptionParser.add_option("--switchVal", action="store", type="string", dest="switchVal", default='')
        self.OptionParser.add_option("--switchFlagOpen", action="store", type="inkbool", dest="switchFlagOpen", default=True)
        self.OptionParser.add_option("--switchConnection", action="store", type="int", dest="switchConnection", default=1)
        self.OptionParser.add_option("--switchCommuteArrow", action="store", type="inkbool", dest="switchCommuteArrow", default=True)
        self.OptionParser.add_option("--switchCommuteArrowOrientation", action="store", type="string", dest="switchCommuteArrowOrientation", default='acw')
        self.OptionParser.add_option("--switchCommuteText", action="store", type="string", dest="switchCommuteText", default='')
        self.OptionParser.add_option("--switchRot", action="store", type="string", dest="switchRot", default=0)
        self.OptionParser.add_option("--switchConvention", action="store", type="string", dest="switchConvention", default='passive')
        self.OptionParser.add_option("--switchVolt", action="store", type="inkbool", dest="switchVolt", default=True)
        self.OptionParser.add_option("--switchCurr", action="store", type="inkbool", dest="switchCurr", default=True)
        self.OptionParser.add_option("--switchVoltName", action="store", type="string", dest="switchVoltName", default='v')
        self.OptionParser.add_option("--switchCurrName", action="store", type="string", dest="switchCurrName", default='i')
        self.OptionParser.add_option("--switchVoltCurrInvert", action="store", type="inkbool", dest="switchVoltCurrInvert", default=True)

        self.OptionParser.add_option("--BJT", action="store", type="string", dest="BJT", default='none')
        self.OptionParser.add_option("--BJT_Photo", action="store", type="inkbool", dest="BJT_Photo", default=True)
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

        self.OptionParser.add_option("--FET_Type", action="store", type="string", dest="FET_Type", default='none')
        self.OptionParser.add_option("--FET_Gate", action="store", type="string", dest="FET_Gate", default='none')
        self.OptionParser.add_option("--FET_BodyDiode", action="store", type="inkbool", dest="FET_BodyDiode", default=False)
        self.OptionParser.add_option("--FET_4Terminals", action="store", type="inkbool", dest="FET_4Terminals", default=False)
        self.OptionParser.add_option("--FET_MoveGate", action="store", type="inkbool", dest="FET_MoveGate", default=False)
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

        self.OptionParser.add_option("--diode", action="store", type="string", dest="diode", default='none')
        self.OptionParser.add_option("--diodeVal", action="store", type="string", dest="diodeVal", default=None)
        self.OptionParser.add_option("--diodeRot", action="store", type="string", dest="diodeRot", default='0')
        self.OptionParser.add_option("--diodeVolt", action="store", type="inkbool", dest="diodeVolt", default=True)
        self.OptionParser.add_option("--diodeCurr", action="store", type="inkbool", dest="diodeCurr", default=True)
        self.OptionParser.add_option("--diodeConvention", action="store", type="string", dest="diodeConvention", default='passive')

        self.OptionParser.add_option("--diodeVoltName", action="store", type="string", dest="diodeVoltName", default='v')
        self.OptionParser.add_option("--diodeCurrName", action="store", type="string", dest="diodeCurrName", default='i')
        self.OptionParser.add_option("--diodeVoltCurrInvert", action="store", type="inkbool", dest="diodeVoltCurrInvert", default=True)
        self.OptionParser.add_option("--diodeMirror", action="store", type="inkbool", dest="diodeMirror", default=False)

        self.OptionParser.add_option("--nodal", action="store", type="string", dest="nodal", default='none')
        self.OptionParser.add_option("--nodalVal", action="store", type="string", dest="nodalVal", default='E')
        self.OptionParser.add_option("--nodalRot", action="store", type="float", dest="nodalRot", default=0)
        self.OptionParser.add_option("--nodalDrawLine", action="store", type="inkbool", dest="nodalDrawLine", default=False)

        self.OptionParser.add_option("--opamp", action="store", type="string", dest="opamp", default='none')
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

        self.OptionParser.add_option("--arrow", action="store", type="string", dest="arrow", default='none')
        self.OptionParser.add_option("--arrowVal", action="store", type="string", dest="arrowVal", default='')
        self.OptionParser.add_option("--arrowUnit", action="store", type="inkbool", dest="arrowUnit", default=False)
        self.OptionParser.add_option("--arrowRot", action="store", type="string", dest="arrowRot", default='0')
        self.OptionParser.add_option("--arrowInvert", action="store", type="inkbool", dest="arrowInvert", default=True)
        self.OptionParser.add_option("--arrowVSize", action="store", type="int", dest="arrowVSize", default=20)
        self.OptionParser.add_option("--arrowISize", action="store", type="int", dest="arrowISize", default=10)
        self.OptionParser.add_option("--arrowCurvaturDirection", action="store", type="inkbool", dest="arrowCurvaturDirection", default=True)

        self.OptionParser.add_option("--currColor", action="store", type="string", dest="currColor", default='#FF0000')
        self.OptionParser.add_option("--colorPickerCurrent", action="store", type="string", dest="colorPickerCurrent", default='0')

        self.OptionParser.add_option("--voltColor", action="store", type="string", dest="voltColor", default='#217B21')
        self.OptionParser.add_option("--colorPickerVolt", action="store", type="string", dest="colorPickerVolt", default='0')

    def effect(self):

        so = self.options
        so.tab = so.tab.replace('"', '')  # removes de exceeding double quotes from the string

        # latex related preamble
        self.preambleFile = os.getcwd() + '/textextLib/CircuitSymbolsLatexPreamble.tex'

        # root_layer = self.current_layer
        root_layer = self.document.getroot()
        # root_layer = self.getcurrentLayer()

        # text size and font style
        self.fontSize = 5
        self.fontSizeSmall = 4

        self.textOffset = self.fontSize / 1.5  # offset between symbol and text
        self.textOffsetSmall = self.fontSizeSmall / 2  # offset between symbol and text
        self.textStyle = inkDraw.textStyle.setSimpleBlack(self.fontSize, justification='center')
        self.textStyleSmall = inkDraw.textStyle.setSimpleBlack(self.fontSizeSmall, justification='center')

        # sets the position to the viewport center, round to next 10.
        position = [self.view_center[0], self.view_center[1]]
        position[0] = int(math.ceil(position[0] / 10.0)) * 10
        position[1] = int(math.ceil(position[1] / 10.0)) * 10

        [self.voltageColor, alpha] = inkDraw.color.parseColorPicker(so.voltColor, so.colorPickerVolt)
        [self.currentColor, alpha] = inkDraw.color.parseColorPicker(so.currColor, so.colorPickerCurrent)

        so.bipoleRLCRot = float(so.bipoleRLCRot)
        so.sourceRot = float(so.sourceRot)
        so.sourceControlledRot = float(so.sourceControlledRot)
        so.switchRot = float(so.switchRot)
        so.arrowRot = float(so.arrowRot)
        so.diodeRot = float(so.diodeRot)
        so.BJT_Rot = float(so.BJT_Rot)
        so.FET_Rot = float(so.FET_Rot)

        # x=inkDraw.textStyle.setSimpleBlack(fontSize=10, justification='center')
        # ang=30.0
        # inkDraw.text.write(self, 'abc', position, root_layer,
        #                    textStyle=x, fontSize=None, justification=None, angleDeg=ang)

        # inkDraw.text.latex(self, root_layer, 'def', position, fontSize=10, refPoint='cc', angleDeg=ang)
        # ---------------------------
        # RLC
        # ---------------------------
        if so.tab == 'RLC':

            if so.bipoleRLCUnit and inkDraw.useLatex:
                so.bipoleRLCVal = latexUnitMultiple(so.bipoleRLCVal)

            if so.bipoleRLC == "genericBipole":
                if so.bipoleRLCUnit:
                    if inkDraw.useLatex:
                        so.bipoleRLCVal += r'\si\ohm'
                    else:
                        so.bipoleRLCVal += OhmChar
                self.drawBipoleGeneral(root_layer, position, value=so.bipoleRLCVal, angleDeg=so.bipoleRLCRot,
                                       flagVolt=so.bipoleRLCVolt, voltName=so.bipoleRLCVoltName,
                                       flagCurr=so.bipoleRLCCurr, currName=so.bipoleRLCCurrName,
                                       invertArrows=so.bipoleRLCVoltCurrInvert, convention=so.bipoleRLCconvention)

            if so.bipoleRLC == "resistor":
                if so.bipoleRLCUnit:
                    if inkDraw.useLatex:
                        so.bipoleRLCVal += r'\si\ohm'
                    else:
                        so.bipoleRLCVal += OhmChar
                self.drawResistor(root_layer, position, value=so.bipoleRLCVal, angleDeg=so.bipoleRLCRot,
                                  flagVolt=so.bipoleRLCVolt, voltName=so.bipoleRLCVoltName, flagCurr=so.bipoleRLCCurr,
                                  currName=so.bipoleRLCCurrName, invertArrows=so.bipoleRLCVoltCurrInvert,
                                  convention=so.bipoleRLCconvention)

            if so.bipoleRLC == "capacitor":
                if so.bipoleRLCUnit:
                    if inkDraw.useLatex:
                        so.bipoleRLCVal += r'\si\farad'
                    else:
                        so.bipoleRLCVal += 'F'
                self.drawCapacitor(root_layer, position, value=so.bipoleRLCVal, flagPol=False, angleDeg=so.bipoleRLCRot,
                                   flagVolt=so.bipoleRLCVolt, voltName=so.bipoleRLCVoltName, flagCurr=so.bipoleRLCCurr,
                                   currName=so.bipoleRLCCurrName, invertArrows=so.bipoleRLCVoltCurrInvert,
                                   convention=so.bipoleRLCconvention)

            if so.bipoleRLC == "capacitorPol":
                if so.bipoleRLCUnit:
                    if inkDraw.useLatex:
                        so.bipoleRLCVal += r'\si\farad'
                    else:
                        so.bipoleRLCVal += 'F'
                self.drawCapacitor(root_layer, position, value=so.bipoleRLCVal, flagPol=True, angleDeg=so.bipoleRLCRot,
                                   flagVolt=so.bipoleRLCVolt, voltName=so.bipoleRLCVoltName, flagCurr=so.bipoleRLCCurr,
                                   currName=so.bipoleRLCCurrName, invertArrows=so.bipoleRLCVoltCurrInvert,
                                   convention=so.bipoleRLCconvention)

            if so.bipoleRLC == "inductor":
                if so.bipoleRLCUnit:
                    if inkDraw.useLatex:
                        so.bipoleRLCVal += r'\si\henry'
                    else:
                        so.bipoleRLCVal += 'H'
                self.drawInductor(root_layer, position, value=so.bipoleRLCVal, angleDeg=so.bipoleRLCRot,
                                  flagVolt=so.bipoleRLCVolt, voltName=so.bipoleRLCVoltName, flagCurr=so.bipoleRLCCurr,
                                  currName=so.bipoleRLCCurrName, invertArrows=so.bipoleRLCVoltCurrInvert,
                                  convention=so.bipoleRLCconvention)

            if so.bipoleRLC == "pot2T":
                if so.bipoleRLCUnit:
                    if inkDraw.useLatex:
                        so.bipoleRLCVal += r'\si\ohm'
                    else:
                        so.bipoleRLCVal += OhmChar
                self.drawPotentiometer(root_layer, position, value=so.bipoleRLCVal, angleDeg=so.bipoleRLCRot,
                                       flagVolt=so.bipoleRLCVolt, voltName=so.bipoleRLCVoltName,
                                       flagCurr=so.bipoleRLCCurr, currName=so.bipoleRLCCurrName,
                                       invertArrows=so.bipoleRLCVoltCurrInvert, is3T=False,
                                       convention=so.bipoleRLCconvention)

            if so.bipoleRLC == "pot3T":
                if so.bipoleRLCUnit:
                    if inkDraw.useLatex:
                        so.bipoleRLCVal += r'\si\ohm'
                    else:
                        so.bipoleRLCVal += OhmChar
                self.drawPotentiometer(root_layer, position, value=so.bipoleRLCVal, angleDeg=so.bipoleRLCRot,
                                       flagVolt=so.bipoleRLCVolt, voltName=so.bipoleRLCVoltName,
                                       flagCurr=so.bipoleRLCCurr, currName=so.bipoleRLCCurrName,
                                       invertArrows=so.bipoleRLCVoltCurrInvert, is3T=True,
                                       convention=so.bipoleRLCconvention)

        # ---------------------------
        # independendent sources
        # ---------------------------
        if so.tab == 'Indep. Source':

            if so.sourceUnit and inkDraw.useLatex:
                so.sourceVal = latexUnitMultiple(so.sourceVal)

            if so.source == "voltIndepDC":
                if so.sourceUnit:
                    if inkDraw.useLatex:
                        so.sourceVal += r'\si\volt'
                    else:
                        so.sourceVal += 'V'
                self.drawSourceVDC(root_layer, position, value=so.sourceVal, angleDeg=so.sourceRot,
                                   flagVolt=so.sourceVolt, flagCurr=so.sourceCurr, currName=so.sourceCurrName,
                                   invertArrows=so.sourceVoltCurrInvert, mirror=so.sourceMirror,
                                   convention=so.sourceConvention)

            if so.source == "voltIndepDCbattery":
                if so.sourceUnit:
                    if inkDraw.useLatex:
                        so.sourceVal += r'\si\volt'
                    else:
                        so.sourceVal += 'V'
                self.drawSourceVDCbattery(root_layer, position, value=so.sourceVal, angleDeg=so.sourceRot,
                                          flagVolt=so.sourceVolt, flagCurr=so.sourceCurr, currName=so.sourceCurrName,
                                          invertArrows=so.sourceVoltCurrInvert, mirror=so.sourceMirror,
                                          convention=so.sourceConvention)

            if so.source == "voltIndep":
                if so.sourceUnit:
                    if inkDraw.useLatex:
                        so.sourceVal += r'\si\volt'
                    else:
                        so.sourceVal += 'V'
                self.drawSourceV(root_layer, position, value=so.sourceVal, angleDeg=so.sourceRot,
                                 flagVolt=so.sourceVolt, flagCurr=so.sourceCurr, currName=so.sourceCurrName,
                                 invertArrows=so.sourceVoltCurrInvert, mirror=so.sourceMirror,
                                 convention=so.sourceConvention)

            if so.source == "voltIndepSinusoidal":
                if so.sourceUnit:
                    if inkDraw.useLatex:
                        so.sourceVal += r'\si\volt'
                    else:
                        so.sourceVal += 'V'
                self.drawSourceVSinusoidal(root_layer, position, value=so.sourceVal, angleDeg=so.sourceRot,
                                           flagVolt=so.sourceVolt, flagCurr=so.sourceCurr, currName=so.sourceCurrName,
                                           invertArrows=so.sourceVoltCurrInvert, mirror=so.sourceMirror,
                                           convention=so.sourceConvention)

            if so.source == "currIndep":
                if so.sourceUnit:
                    if inkDraw.useLatex:
                        so.sourceVal += r'\si\ampere'
                    else:
                        so.sourceVal += 'A'
                self.drawSourceI(root_layer, position, value=so.sourceVal, angleDeg=so.sourceRot,
                                 flagVolt=so.sourceVolt, flagCurr=so.sourceCurr, voltName=so.sourceVoltName,
                                 invertArrows=so.sourceVoltCurrInvert, mirror=so.sourceMirror,
                                 convention=so.sourceConvention)

        # --------------------------
        # controlled sources
        # ---------------------------
        if so.tab == 'Dep. Source':

            if so.sourceControlled == "volt":
                self.drawControledSourceV(root_layer, position, controlType=so.sourceControlledType,
                                          gain=so.sourceControlledGain, controlName=so.sourceControlledControlName,
                                          angleDeg=so.sourceControlledRot, flagVolt=so.sourceControlledVolt,
                                          flagCurr=so.sourceControlledCurr, currName=so.sourceControlledCurrName,
                                          invertArrows=so.sourceControlledVoltCurrInvert,
                                          mirror=so.sourceControlledMirror, convention=so.sourceControlledConvention,
                                          drawControl=so.sourceControlledDrawArrow)

            if so.sourceControlled == "curr":
                self.drawControledSourceI(root_layer, position, controlType=so.sourceControlledType,
                                          gain=so.sourceControlledGain, controlName=so.sourceControlledControlName,
                                          angleDeg=so.sourceControlledRot, flagVolt=so.sourceControlledVolt,
                                          flagCurr=so.sourceControlledCurr, voltName=so.sourceControlledVoltName,
                                          invertArrows=so.sourceControlledVoltCurrInvert,
                                          mirror=so.sourceControlledMirror, convention=so.sourceControlledConvention,
                                          drawControl=so.sourceControlledDrawArrow)

        # ---------------------------
        # Single Throw switches
        # ---------------------------
        if so.tab == 'Switches':
            if so.switchThrows == 1:
                self.drawNPST(root_layer, position, value=so.switchVal, angleDeg=so.switchRot,
                              isPushButton=so.switchPushButton, nPoles=so.switchPoles, flagOpen=so.switchFlagOpen,
                              drawCommuteArrow=so.switchCommuteArrow, commuteText=so.switchCommuteText,
                              flagVolt=so.switchVolt, voltName=so.switchVoltName, flagCurr=so.switchCurr,
                              currName=so.switchCurrName, invertArrows=so.switchVoltCurrInvert,
                              convention=so.switchConvention)
            else:
                self.drawNPNT(root_layer, position, value=so.switchVal, angleDeg=so.switchRot, nPoles=so.switchPoles,
                              nThrows=so.switchThrows, connection=so.switchConnection,
                              drawCommuteArrow=so.switchCommuteArrow,
                              commuteOrientation=so.switchCommuteArrowOrientation, commuteText=so.switchCommuteText,
                              flagVolt=so.switchVolt, voltName=so.switchVoltName, flagCurr=so.switchCurr,
                              currName=so.switchCurrName, invertArrows=so.switchVoltCurrInvert,
                              convention=so.switchConvention)

        # ---------------------------
        # diodes
        # ---------------------------
        if so.tab == 'Diodes':
            if so.diode in ['regular', 'LED', 'photoDiode', 'zener', 'schottky', 'tunnel', 'varicap']:
                self.drawDiode(root_layer, position, value=so.diodeVal, angleDeg=so.diodeRot, flagVolt=so.diodeVolt,
                               voltName=so.diodeVoltName, flagCurr=so.diodeCurr, currName=so.diodeCurrName,
                               invertArrows=not so.diodeVoltCurrInvert, flagType=so.diode, mirror=so.diodeMirror,
                               convention=so.diodeConvention)

        # ---------------------------
        # Transistors
        # ---------------------------
        if so.tab == 'Transistor_BJT':

            if so.BJT == 'BJT_PNP':
                typeBJT = 'PNP'
            else:
                typeBJT = 'NPN'

            self.drawTransistorBJT(root_layer, position, angleDeg=so.BJT_Rot, mirrorEC=so.BJT_MirrorEC,
                                   drawBCEtags=so.BJT_EBCtags, drawEnvelope=so.BJT_Envelope, transistorType=typeBJT,
                                   flagPhototransistor=so.BJT_Photo, drawVCE=so.BJT_DrawVCEarrow,
                                   drawVCB=so.BJT_DrawVCBarrow, drawVBE=so.BJT_DrawVBEarrow,
                                   drawICarrow=so.BJT_DrawICarrow, drawIBarrow=so.BJT_DrawIBarrow,
                                   drawIEarrow=so.BJT_DrawIEarrow, VCEname=so.BJT_VCEname, VCBname=so.BJT_VCBname,
                                   VBEname=so.BJT_VBEname, ICname=so.BJT_ICname, IBname=so.BJT_IBname,
                                   IEname=so.BJT_IEname)

        if so.tab == 'Transistor_FET':
            if 'MOSFET' in so.FET_Type:
                self.drawTransistorMOSFET(root_layer, position, angleDeg=so.FET_Rot, mirrorSD=so.FET_MirrorEC,
                                          drawSGDtags=so.FET_SGDtags, drawEnvelope=so.FET_Envelope,
                                          modeType=so.FET_Type, gateType=so.FET_Gate, is4terminal=so.FET_4Terminals,
                                          bodyDiode=so.FET_BodyDiode,drawVGS=so.FET_DrawVGSarrow, drawVDS=so.FET_DrawVDSarrow,
                                          drawVDG=so.FET_DrawVDGarrow, drawIDarrow=so.FET_DrawIDarrow,
                                          drawISarrow=so.FET_DrawISarrow, drawIGarrow=so.FET_DrawIGarrow,
                                          VGSname=so.FET_VGSname, VDSname=so.FET_VDSname, VDGname=so.FET_VDGname,
                                          IDname=so.FET_IDname, ISname=so.FET_ISname, IGname=so.FET_IGname)

            if 'JFET' in so.FET_Type:
                self.drawTransistorJFET(root_layer, position, angleDeg=so.FET_Rot, mirrorSD=so.FET_MirrorEC,
                                        drawSGDtags=so.FET_SGDtags, drawEnvelope=so.FET_Envelope, gateType=so.FET_Gate,
                                        moveGate=so.FET_MoveGate, drawVGS=so.FET_DrawVGSarrow,
                                        drawVDS=so.FET_DrawVDSarrow, drawVDG=so.FET_DrawVDGarrow,
                                        drawIDarrow=so.FET_DrawIDarrow, drawISarrow=so.FET_DrawISarrow,
                                        drawIGarrow=so.FET_DrawIGarrow, VGSname=so.FET_VGSname, VDSname=so.FET_VDSname,
                                        VDGname=so.FET_VDGname, IDname=so.FET_IDname, ISname=so.FET_ISname,
                                        IGname=so.FET_IGname)

        # --------------------------
        # operational amplifiers
        # ---------------------------
        if so.tab == 'Opamp':
            if so.opamp == "general":
                self.drawOpAmpGeneral(root_layer, position, mirrorInput=so.opampMirrorInput, drawVin=so.opampDrawVin,
                                      drawIin=so.opampDrawIin, drawVd=so.opampDrawVd, drawVout=so.opampDrawVout,
                                      drawIout=so.opampDrawIout, inputVPosName=so.opampInputVPosName,
                                      inputVNegName=so.opampInputVNegName, inputIPosName=so.opampInputIPosName,
                                      inputINegName=so.opampInputINegName, VoutName=so.opampVoutName,
                                      IoutName=so.opampIoutName, VdiffName=so.opampInputDiffName,
                                      flagDrawSupply=so.opampFlagSupply, FlagSupplyValues=so.opampFlagSupplyValues,
                                      flagSupplySymm=so.opampSupplySymm, supplyPositiveVal=so.opampSupplyPositiveVal,
                                      supplyNegativeVal=so.opampSupplyNegativeVal)

        # --------------------------
        # Nodes
        # ---------------------------
        if so.tab == 'Signals':

            if so.nodal == "GND":
                self.drawGND(root_layer, position, angleDeg=so.nodalRot)
                return

            if so.nodal == "common":
                self.drawCommon(root_layer, position, angleDeg=so.nodalRot)
                return

            if so.nodal == "custom":
                text = so.nodalVal

            if so.nodal == "digital":
                self.drawDigital(root_layer, position, angleDeg=so.nodalRot, nodalVal=so.nodalVal)
                return

            if so.nodal == "+vcc":
                text = '+V_{cc}'

            if so.nodal == "-vcc":
                text = '-V_{cc}'

            if so.nodal == "+5V":
                text = r'+5\volt'

            if so.nodal == "-5V":
                text = r'-5\volt'

            if so.nodal == "+15V":
                text = r'+15\volt'

            if so.nodal == "-15V":
                text = r'-15\volt'

            if so.nodal == "v_in":
                text = r'v_{in}'

            if so.nodal == "v_out":
                text = r'v_{out}'

            self.drawSignal(root_layer, position, angleDeg=so.nodalRot, nodalVal=text, drawLine=so.nodalDrawLine)
            return

        # --------------------------
        # Arrows
        # ---------------------------
        if so.tab == 'Arrow':

            if so.arrow == "voltage":
                if so.arrowUnit:
                    if inkDraw.useLatex:
                        so.arrowVal += r'\si\volt'
                    else:
                        so.arrowVal += 'V'
                self.drawVoltArrowSimple(root_layer, position, name=so.arrowVal, color=self.voltageColor,
                                         angleDeg=so.arrowRot, invertArrows=so.arrowInvert, size=so.arrowVSize,
                                         invertCurvatureDirection=so.arrowCurvaturDirection)

            if so.arrow == "current":
                if so.arrowUnit:
                    if inkDraw.useLatex:
                        so.arrowVal += r'\si\ampere'
                    else:
                        so.arrowVal += 'A'
                self.drawCurrArrowSimple(root_layer, position, name=so.arrowVal, color=self.voltageColor,
                                         angleDeg=so.arrowRot, invertArrows=so.arrowInvert, size=so.arrowISize,
                                         invertTextSide=so.arrowCurvaturDirection)


if __name__ == '__main__':
    circuit = CircuitSymbols()
    circuit.affect()
