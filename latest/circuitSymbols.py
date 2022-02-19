#!/usr/bin/python

import math
import os

import inkscapeMadeEasy.inkscapeMadeEasy_Base as inkBase
import inkscapeMadeEasy.inkscapeMadeEasy_Draw as inkDraw
from drawAmpOp import ampOp
from drawArrows import arrow
from drawDiodes import diode
from drawRLC import RLC
from drawSignals import signal
from drawSources import source
from drawSwitches import switch
from drawTransformer import transformer
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
class CircuitSymbols(RLC, source, transistor, transformer, signal, arrow, ampOp, diode, switch):
    def __init__(self):
        inkBase.inkscapeMadeEasy.__init__(self)

        self.arg_parser.add_argument("--tab", type=str, dest="tab", default="object")
        self.arg_parser.add_argument("--subTab_sigAnn", type=str, dest="subTab_sigAnn", default="object")
        self.arg_parser.add_argument("--subTab_sources", type=str, dest="subTab_sources", default="object")
        self.arg_parser.add_argument("--subTab_help", type=str, dest="subTab_help", default="object")
        self.arg_parser.add_argument("--subtab_transformerWindings", type=str, dest="subtab_transformerWindings", default="object")

        self.arg_parser.add_argument("--bipoleRLC", type=str, dest="bipoleRLC", default='resistor')
        self.arg_parser.add_argument("--bipoleRLCVal", type=str, dest="bipoleRLCVal", default='Z')
        self.arg_parser.add_argument("--bipoleRLCvariable", type=self.bool, dest="bipoleRLCvariable", default=False)
        self.arg_parser.add_argument("--bipoleRLCUnit", type=self.bool, dest="bipoleRLCUnit", default=False)
        self.arg_parser.add_argument("--bipoleRLCRot", type=str, dest="bipoleRLCRot", default='0')
        self.arg_parser.add_argument("--bipoleRLCconvention", type=str, dest="bipoleRLCconvention", default='passive')
        self.arg_parser.add_argument("--bipoleRLCstandard", type=str, dest="bipoleRLCstandard", default='IEC')
        self.arg_parser.add_argument("--bipoleRLCVolt", type=self.bool, dest="bipoleRLCVolt", default=True)
        self.arg_parser.add_argument("--bipoleRLCCurr", type=self.bool, dest="bipoleRLCCurr", default=True)
        self.arg_parser.add_argument("--bipoleRLCVoltName", type=str, dest="bipoleRLCVoltName", default='v')
        self.arg_parser.add_argument("--bipoleRLCCurrName", type=str, dest="bipoleRLCCurrName", default='i')
        self.arg_parser.add_argument("--bipoleRLCVoltCurrInvert", type=self.bool, dest="bipoleRLCVoltCurrInvert", default=True)
        self.arg_parser.add_argument("--bipoleRLCextraWireSize", type=float, dest="bipoleRLCextraWireSize", default=0.0)

        self.arg_parser.add_argument("--source", type=str, dest="source", default='voltIndep')
        self.arg_parser.add_argument("--sourceVal", type=str, dest="sourceVal", default='E')
        self.arg_parser.add_argument("--sourceVariable", type=self.bool, dest="sourceVariable", default=False)
        self.arg_parser.add_argument("--sourceUnit", type=self.bool, dest="sourceUnit", default=False)
        self.arg_parser.add_argument("--sourceStandard", type=str, dest="sourceStandard", default='IEC')
        self.arg_parser.add_argument("--sourceRot", type=str, dest="sourceRot", default='0')
        self.arg_parser.add_argument("--sourceConvention", type=str, dest="sourceConvention", default='active')
        self.arg_parser.add_argument("--sourceVolt", type=self.bool, dest="sourceVolt", default=True)
        self.arg_parser.add_argument("--sourceCurr", type=self.bool, dest="sourceCurr", default=True)
        self.arg_parser.add_argument("--sourceVoltName", type=str, dest="sourceVoltName", default='v')
        self.arg_parser.add_argument("--sourceCurrName", type=str, dest="sourceCurrName", default='i')
        self.arg_parser.add_argument("--sourceVoltCurrInvert", type=self.bool, dest="sourceVoltCurrInvert", default=True)
        self.arg_parser.add_argument("--sourceMirror", type=self.bool, dest="sourceMirror", default=False)
        self.arg_parser.add_argument("--sourceExtraWireSize", type=float, dest="sourceExtraWireSize", default=0.0)

        self.arg_parser.add_argument("--sourceControlled", type=str, dest="sourceControlled", default='volt')
        self.arg_parser.add_argument("--sourceControlledType", type=str, dest="sourceControlledType", default='curr')
        self.arg_parser.add_argument("--sourceControlledStandard", type=str, dest="sourceControlledStandard", default='IEC')
        self.arg_parser.add_argument("--sourceControlledGain", type=str, dest="sourceControlledGain", default='k')
        self.arg_parser.add_argument("--sourceControlledControlName", type=str, dest="sourceControlledControlName", default='v_c')
        self.arg_parser.add_argument("--sourceControlledRot", type=str, dest="sourceControlledRot", default='0')
        self.arg_parser.add_argument("--sourceControlledMirror", type=self.bool, dest="sourceControlledMirror", default=False)
        self.arg_parser.add_argument("--sourceControlledDrawArrow", type=self.bool, dest="sourceControlledDrawArrow", default=False)
        self.arg_parser.add_argument("--sourceControlledExtraWireSize", type=float, dest="sourceControlledExtraWireSize", default=0.0)

        self.arg_parser.add_argument("--switchPoles", type=int, dest="switchPoles", default=1)
        self.arg_parser.add_argument("--switchThrows", type=int, dest="switchThrows", default=1)
        self.arg_parser.add_argument("--switchPushButton", type=self.bool, dest="switchPushButton", default=False)
        self.arg_parser.add_argument("--switchVal", type=str, dest="switchVal", default='')
        self.arg_parser.add_argument("--switchConnection", type=str, dest="switchConnection", default=0)
        self.arg_parser.add_argument("--switchCommuteArrow", type=self.bool, dest="switchCommuteArrow", default=True)
        self.arg_parser.add_argument("--switchCommuteArrowOrientation", type=str, dest="switchCommuteArrowOrientation", default='ccw')
        self.arg_parser.add_argument("--switchCommuteText", type=str, dest="switchCommuteText", default='')
        self.arg_parser.add_argument("--switchRot", type=str, dest="switchRot", default=0)
        self.arg_parser.add_argument("--switchConvention", type=str, dest="switchConvention", default='passive')
        self.arg_parser.add_argument("--switchVolt", type=self.bool, dest="switchVolt", default=True)
        self.arg_parser.add_argument("--switchCurr", type=self.bool, dest="switchCurr", default=True)
        self.arg_parser.add_argument("--switchVoltName", type=str, dest="switchVoltName", default='v')
        self.arg_parser.add_argument("--switchCurrName", type=str, dest="switchCurrName", default='i')
        self.arg_parser.add_argument("--switchVoltCurrInvert", type=self.bool, dest="switchVoltCurrInvert", default=True)
        self.arg_parser.add_argument("--switchExtraWireSize", type=float, dest="switchExtraWireSize", default=0.0)

        self.arg_parser.add_argument("--transformerType", type=str, dest="transformerType", default='transformer')
        self.arg_parser.add_argument("--transformerRot", type=str, dest="transformerRot", default='0')
        self.arg_parser.add_argument("--transformerLabel", type=str, dest="transformerLabel", default='')
        self.arg_parser.add_argument("--transformerCore", type=str, dest="transformerCore", default='air')
        self.arg_parser.add_argument("--transformerStepType", type=str, dest="transformerStepType", default='one2one')
        self.arg_parser.add_argument("--transformerPolaritySymbol", type=self.bool, dest="transformerPolaritySymbol", default=True)
        self.arg_parser.add_argument("--transformerNcoils1", type=int, dest="transformerNcoils1", default=1)
        self.arg_parser.add_argument("--transformerTapped1", type=self.bool, dest="transformerTapped1", default=True)
        self.arg_parser.add_argument("--transformerInvPolarity1", type=self.bool, dest="transformerInvPolarity1", default=False)
        self.arg_parser.add_argument("--transformerConvention1", type=str, dest="transformerConvention1", default='passive')
        self.arg_parser.add_argument("--transformerVolt1", type=self.bool, dest="transformerVolt1", default=True)
        self.arg_parser.add_argument("--transformerCurr1", type=self.bool, dest="transformerCurr1", default=True)
        self.arg_parser.add_argument("--transformerVoltName1", type=str, dest="transformerVoltName1", default='v')
        self.arg_parser.add_argument("--transformerCurrName1", type=str, dest="transformerCurrName1", default='i')
        self.arg_parser.add_argument("--transformerVoltCurrInvert1", type=self.bool, dest="transformerVoltCurrInvert1", default=True)
        self.arg_parser.add_argument("--transformerNcoils2", type=int, dest="transformerNcoils2", default=1)
        self.arg_parser.add_argument("--transformerTapped2", type=self.bool, dest="transformerTapped2", default=True)
        self.arg_parser.add_argument("--transformerInvPolarity2", type=self.bool, dest="transformerInvPolarity2", default=False)
        self.arg_parser.add_argument("--transformerConvention2", type=str, dest="transformerConvention2", default='passive')
        self.arg_parser.add_argument("--transformerVolt2", type=self.bool, dest="transformerVolt2", default=True)
        self.arg_parser.add_argument("--transformerCurr2", type=self.bool, dest="transformerCurr2", default=True)
        self.arg_parser.add_argument("--transformerVoltName2", type=str, dest="transformerVoltName2", default='v')
        self.arg_parser.add_argument("--transformerCurrName2", type=str, dest="transformerCurrName2", default='i')
        self.arg_parser.add_argument("--transformerVoltCurrInvert2", type=self.bool, dest="transformerVoltCurrInvert2", default=True)
        self.arg_parser.add_argument("--transformerExtraWireSize", type=float, dest="transformerExtraWireSize", default=0.0)

        self.arg_parser.add_argument("--BJT", type=str, dest="BJT", default='none')
        self.arg_parser.add_argument("--BJT_IGBT", type=self.bool, dest="BJT_IGBT", default=False)
        self.arg_parser.add_argument("--BJT_Photo", type=self.bool, dest="BJT_Photo", default=True)
        self.arg_parser.add_argument("--BJT_Rot", type=str, dest="BJT_Rot", default='0')
        self.arg_parser.add_argument("--BJT_Envelope", type=self.bool, dest="BJT_Envelope", default=True)
        self.arg_parser.add_argument("--BJT_MirrorEC", type=self.bool, dest="BJT_MirrorEC", default=False)
        self.arg_parser.add_argument("--BJT_EBCtags", type=self.bool, dest="BJT_EBCtags", default=False)
        self.arg_parser.add_argument("--BJT_DrawVCEarrow", type=self.bool, dest="BJT_DrawVCEarrow", default=False)
        self.arg_parser.add_argument("--BJT_DrawVCBarrow", type=self.bool, dest="BJT_DrawVCBarrow", default=False)
        self.arg_parser.add_argument("--BJT_DrawVBEarrow", type=self.bool, dest="BJT_DrawVBEarrow", default=False)
        self.arg_parser.add_argument("--BJT_DrawICarrow", type=self.bool, dest="BJT_DrawICarrow", default=False)
        self.arg_parser.add_argument("--BJT_DrawIBarrow", type=self.bool, dest="BJT_DrawIBarrow", default=False)
        self.arg_parser.add_argument("--BJT_DrawIEarrow", type=self.bool, dest="BJT_DrawIEarrow", default=False)
        self.arg_parser.add_argument("--BJT_VCEname", type=str, dest="BJT_VCEname", default='v_{ce}')
        self.arg_parser.add_argument("--BJT_VCBname", type=str, dest="BJT_VCBname", default='v_{cb}')
        self.arg_parser.add_argument("--BJT_VBEname", type=str, dest="BJT_VBEname", default='v_{be}')
        self.arg_parser.add_argument("--BJT_ICname", type=str, dest="BJT_ICname", default='i_c')
        self.arg_parser.add_argument("--BJT_IBname", type=str, dest="BJT_IBname", default='i_b')
        self.arg_parser.add_argument("--BJT_IEname", type=str, dest="BJT_IEname", default='i_e')
        self.arg_parser.add_argument("--BJT_ExtraWireSize", type=float, dest="BJT_ExtraWireSize", default=0.0)

        self.arg_parser.add_argument("--FET_Type", type=str, dest="FET_Type", default='none')
        self.arg_parser.add_argument("--FET_Gate", type=str, dest="FET_Gate", default='none')
        self.arg_parser.add_argument("--FET_BodyDiode", type=self.bool, dest="FET_BodyDiode", default=False)
        self.arg_parser.add_argument("--FET_MOSsymbolType", type=str, dest="FET_MOSsymbolType", default='3T')
        self.arg_parser.add_argument("--FET_MoveGate", type=self.bool, dest="FET_MoveGate", default=False)
        self.arg_parser.add_argument("--FET_Rot", type=str, dest="FET_Rot", default='0')
        self.arg_parser.add_argument("--FET_Envelope", type=self.bool, dest="FET_Envelope", default=True)
        self.arg_parser.add_argument("--FET_MirrorEC", type=self.bool, dest="FET_MirrorEC", default=False)
        self.arg_parser.add_argument("--FET_SGDtags", type=self.bool, dest="FET_SGDtags", default=False)
        self.arg_parser.add_argument("--FET_DrawVGSarrow", type=self.bool, dest="FET_DrawVGSarrow", default=False)
        self.arg_parser.add_argument("--FET_DrawVDSarrow", type=self.bool, dest="FET_DrawVDSarrow", default=False)
        self.arg_parser.add_argument("--FET_DrawVDGarrow", type=self.bool, dest="FET_DrawVDGarrow", default=False)
        self.arg_parser.add_argument("--FET_DrawIDarrow", type=self.bool, dest="FET_DrawIDarrow", default=False)
        self.arg_parser.add_argument("--FET_DrawISarrow", type=self.bool, dest="FET_DrawISarrow", default=False)
        self.arg_parser.add_argument("--FET_DrawIGarrow", type=self.bool, dest="FET_DrawIGarrow", default=False)
        self.arg_parser.add_argument("--FET_VGSname", type=str, dest="FET_VGSname", default='v_{gs}')
        self.arg_parser.add_argument("--FET_VDSname", type=str, dest="FET_VDSname", default='v_{ds}')
        self.arg_parser.add_argument("--FET_VDGname", type=str, dest="FET_VDGname", default='v_{dg}')
        self.arg_parser.add_argument("--FET_IDname", type=str, dest="FET_IDname", default='i_d')
        self.arg_parser.add_argument("--FET_ISname", type=str, dest="FET_ISname", default='i_s')
        self.arg_parser.add_argument("--FET_IGname", type=str, dest="FET_IGname", default='i_g')
        self.arg_parser.add_argument("--FET_ExtraWireSize", type=float, dest="FET_ExtraWireSize", default=0.0)

        self.arg_parser.add_argument("--diode", type=str, dest="diode", default='none')
        self.arg_parser.add_argument("--diodeVal", type=str, dest="diodeVal", default=None)
        self.arg_parser.add_argument("--diodeRot", type=str, dest="diodeRot", default='0')
        self.arg_parser.add_argument("--diodeVolt", type=self.bool, dest="diodeVolt", default=True)
        self.arg_parser.add_argument("--diodeCurr", type=self.bool, dest="diodeCurr", default=True)
        self.arg_parser.add_argument("--diodeConvention", type=str, dest="diodeConvention", default='passive')

        self.arg_parser.add_argument("--diodeVoltName", type=str, dest="diodeVoltName", default='v')
        self.arg_parser.add_argument("--diodeCurrName", type=str, dest="diodeCurrName", default='i')
        self.arg_parser.add_argument("--diodeVoltCurrInvert", type=self.bool, dest="diodeVoltCurrInvert", default=True)
        self.arg_parser.add_argument("--diodeMirror", type=self.bool, dest="diodeMirror", default=False)
        self.arg_parser.add_argument("--diodeExtraWireSize", type=float, dest="diodeExtraWireSize", default=0.0)

        self.arg_parser.add_argument("--opamp", type=str, dest="opamp", default='none')
        self.arg_parser.add_argument("--opampMirrorInput", type=self.bool, dest="opampMirrorInput", default=False)
        self.arg_parser.add_argument("--opampDrawVin", type=self.bool, dest="opampDrawVin", default=False)
        self.arg_parser.add_argument("--opampDrawIin", type=self.bool, dest="opampDrawIin", default=False)
        self.arg_parser.add_argument("--opampDrawVd", type=self.bool, dest="opampDrawVd", default=False)
        self.arg_parser.add_argument("--opampDrawVout", type=self.bool, dest="opampDrawVout", default=False)
        self.arg_parser.add_argument("--opampDrawIout", type=self.bool, dest="opampDrawIout", default=False)
        self.arg_parser.add_argument("--opampFlagSupply", type=self.bool, dest="opampFlagSupply", default=False)
        self.arg_parser.add_argument("--opampFlagSupplyValues", type=self.bool, dest="opampFlagSupplyValues", default=False)
        self.arg_parser.add_argument("--opampSupplySymm", type=self.bool, dest="opampSupplySymm", default=True)
        self.arg_parser.add_argument("--opampSupplyPositiveVal", type=str, dest="opampSupplyPositiveVal", default='+V_{cc}')
        self.arg_parser.add_argument("--opampSupplyNegativeVal", type=str, dest="opampSupplyNegativeVal", default='-V_{cc}')
        self.arg_parser.add_argument("--opampInputV+Name", type=str, dest="opampInputVPosName", default='v^+')
        self.arg_parser.add_argument("--opampInputV-Name", type=str, dest="opampInputVNegName", default='v^-')
        self.arg_parser.add_argument("--opampInputI+Name", type=str, dest="opampInputIPosName", default='v^+')
        self.arg_parser.add_argument("--opampInputI-Name", type=str, dest="opampInputINegName", default='v^-')
        self.arg_parser.add_argument("--opampVoutName", type=str, dest="opampVoutName", default='v_{out}')
        self.arg_parser.add_argument("--opampIoutName", type=str, dest="opampIoutName", default='i_{out}')
        self.arg_parser.add_argument("--opampInputDiffName", type=str, dest="opampInputDiffName", default='v_d')

        self.arg_parser.add_argument("--nodal", type=str, dest="nodal", default='none')
        self.arg_parser.add_argument("--nodalVal", type=str, dest="nodalVal", default='E')
        self.arg_parser.add_argument("--nodalRot", type=float, dest="nodalRot", default=0)
        self.arg_parser.add_argument("--nodalDrawLine", type=self.bool, dest="nodalDrawLine", default=False)

        self.arg_parser.add_argument("--arrow", type=str, dest="arrow", default='none')
        self.arg_parser.add_argument("--arrowVal", type=str, dest="arrowVal", default='')
        self.arg_parser.add_argument("--arrowUnit", type=self.bool, dest="arrowUnit", default=False)
        self.arg_parser.add_argument("--arrowRot", type=str, dest="arrowRot", default='0')
        self.arg_parser.add_argument("--arrowInvert", type=self.bool, dest="arrowInvert", default=True)
        self.arg_parser.add_argument("--arrowVSize", type=int, dest="arrowVSize", default=20)
        self.arg_parser.add_argument("--arrowISize", type=int, dest="arrowISize", default=10)
        self.arg_parser.add_argument("--arrowCurvaturDirection", type=self.bool, dest="arrowCurvaturDirection", default=True)

        self.arg_parser.add_argument("--currColor", type=str, dest="currColor", default='#FF0000FF')
        self.arg_parser.add_argument("--colorPickerCurrent", type=str, dest="colorPickerCurrent", default='0')

        self.arg_parser.add_argument("--voltColor", type=str, dest="voltColor", default='#217B21FF')
        self.arg_parser.add_argument("--colorPickerVolt", type=str, dest="colorPickerVolt", default='0')

    def effect(self):

        so = self.options
        so.tab = so.tab.replace('"', '')  # removes de exceeding double quotes from the string

        # latex related preamble
        self.preambleFile = os.getcwd() + '/' + 'circuitSymbolsPreamble.tex'

        root_layer = self.document.getroot()

        # text size and font style
        self.fontSize = 5
        self.fontSizeSmall = 4

        self.textOffset = self.fontSize / 1.5  # offset between symbol and text
        self.textOffsetSmall = self.fontSizeSmall / 2  # offset between symbol and text
        self.textStyle = inkDraw.textStyle.setSimpleBlack(self.fontSize, justification='center')
        self.textStyleSmall = inkDraw.textStyle.setSimpleBlack(self.fontSizeSmall, justification='center')

        
        # sets the position to the viewport center, round to next 10.
        position = [self.svg.namedview.center[0], self.svg.namedview.center[1]]
        position[0] = int(math.ceil(position[0] / 10.0)) * 10
        position[1] = int(math.ceil(position[1] / 10.0)) * 10

        self.voltageColor = inkDraw.color.parseColorPicker(so.voltColor, so.colorPickerVolt)
        self.currentColor = inkDraw.color.parseColorPicker(so.currColor, so.colorPickerCurrent)

        so.bipoleRLCRot = float(so.bipoleRLCRot)
        so.sourceRot = float(so.sourceRot)
        so.sourceControlledRot = float(so.sourceControlledRot)
        so.switchRot = float(so.switchRot)
        so.transformerRot = float(so.transformerRot)
        so.arrowRot = float(so.arrowRot)
        so.diodeRot = float(so.diodeRot)
        so.BJT_Rot = float(so.BJT_Rot)
        so.FET_Rot = float(so.FET_Rot)
        so.switchConnection = int(so.switchConnection)

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
                self.drawResistor(root_layer, position, value=so.bipoleRLCVal, angleDeg=so.bipoleRLCRot, flagVolt=so.bipoleRLCVolt,
                                  voltName=so.bipoleRLCVoltName, flagCurr=so.bipoleRLCCurr, currName=so.bipoleRLCCurrName,
                                  invertArrows=so.bipoleRLCVoltCurrInvert, convention=so.bipoleRLCconvention, wireExtraSize=so.bipoleRLCextraWireSize,
                                  standard='IEC',flagVariable=so.bipoleRLCvariable)

            if so.bipoleRLC == "resistor":
                if so.bipoleRLCUnit:
                    if inkDraw.useLatex:
                        so.bipoleRLCVal += r'\si\ohm'
                    else:
                        so.bipoleRLCVal += OhmChar
                self.drawResistor(root_layer, position, value=so.bipoleRLCVal, angleDeg=so.bipoleRLCRot, flagVolt=so.bipoleRLCVolt,
                                  voltName=so.bipoleRLCVoltName, flagCurr=so.bipoleRLCCurr, currName=so.bipoleRLCCurrName,
                                  invertArrows=so.bipoleRLCVoltCurrInvert, convention=so.bipoleRLCconvention,wireExtraSize=so.bipoleRLCextraWireSize,
                                  standard=so.bipoleRLCstandard,flagVariable=so.bipoleRLCvariable)

            if so.bipoleRLC == "capacitor":
                if so.bipoleRLCUnit:
                    if inkDraw.useLatex:
                        so.bipoleRLCVal += r'\si\farad'
                    else:
                        so.bipoleRLCVal += 'F'
                self.drawCapacitor(root_layer, position, value=so.bipoleRLCVal, flagPol=False, angleDeg=so.bipoleRLCRot, flagVolt=so.bipoleRLCVolt,
                                   voltName=so.bipoleRLCVoltName, flagCurr=so.bipoleRLCCurr, currName=so.bipoleRLCCurrName,
                                   invertArrows=so.bipoleRLCVoltCurrInvert, convention=so.bipoleRLCconvention,
                                   wireExtraSize=so.bipoleRLCextraWireSize, standard=so.bipoleRLCstandard,flagVariable=so.bipoleRLCvariable)

            if so.bipoleRLC == "capacitorPol":
                if so.bipoleRLCUnit:
                    if inkDraw.useLatex:
                        so.bipoleRLCVal += r'\si\farad'
                    else:
                        so.bipoleRLCVal += 'F'
                self.drawCapacitor(root_layer, position, value=so.bipoleRLCVal, flagPol=True, angleDeg=so.bipoleRLCRot, flagVolt=so.bipoleRLCVolt,
                                   voltName=so.bipoleRLCVoltName, flagCurr=so.bipoleRLCCurr, currName=so.bipoleRLCCurrName,
                                   invertArrows=so.bipoleRLCVoltCurrInvert, convention=so.bipoleRLCconvention,
                                   wireExtraSize=so.bipoleRLCextraWireSize, standard=so.bipoleRLCstandard,flagVariable=so.bipoleRLCvariable)

            if so.bipoleRLC == "inductor":
                if so.bipoleRLCUnit:
                    if inkDraw.useLatex:
                        so.bipoleRLCVal += r'\si\henry'
                    else:
                        so.bipoleRLCVal += 'H'
                self.drawInductor(root_layer, position, value=so.bipoleRLCVal, angleDeg=so.bipoleRLCRot, flagVolt=so.bipoleRLCVolt,
                                  voltName=so.bipoleRLCVoltName, flagCurr=so.bipoleRLCCurr, currName=so.bipoleRLCCurrName,
                                  invertArrows=so.bipoleRLCVoltCurrInvert, convention=so.bipoleRLCconvention,wireExtraSize=so.bipoleRLCextraWireSize,
                                  flagVariable=so.bipoleRLCvariable)

            if so.bipoleRLC == "pot2T":
                if so.bipoleRLCUnit:
                    if inkDraw.useLatex:
                        so.bipoleRLCVal += r'\si\ohm'
                    else:
                        so.bipoleRLCVal += OhmChar
                self.drawPotentiometer(root_layer, position, value=so.bipoleRLCVal, angleDeg=so.bipoleRLCRot, flagVolt=so.bipoleRLCVolt,
                                       voltName=so.bipoleRLCVoltName, flagCurr=so.bipoleRLCCurr, currName=so.bipoleRLCCurrName,
                                       invertArrows=so.bipoleRLCVoltCurrInvert, is3T=False, convention=so.bipoleRLCconvention,
                                       wireExtraSize=so.bipoleRLCextraWireSize, standard=so.bipoleRLCstandard)

            if so.bipoleRLC == "pot3T":
                if so.bipoleRLCUnit:
                    if inkDraw.useLatex:
                        so.bipoleRLCVal += r'\si\ohm'
                    else:
                        so.bipoleRLCVal += OhmChar
                self.drawPotentiometer(root_layer, position, value=so.bipoleRLCVal, angleDeg=so.bipoleRLCRot, flagVolt=so.bipoleRLCVolt,
                                       voltName=so.bipoleRLCVoltName, flagCurr=so.bipoleRLCCurr, currName=so.bipoleRLCCurrName,
                                       invertArrows=so.bipoleRLCVoltCurrInvert, is3T=True, convention=so.bipoleRLCconvention,
                                       wireExtraSize=so.bipoleRLCextraWireSize, standard=so.bipoleRLCstandard)

            if so.bipoleRLC == "fuse":
                self.drawFuse(root_layer, position, value=so.bipoleRLCVal, angleDeg=so.bipoleRLCRot, flagVolt=so.bipoleRLCVolt,
                                  voltName=so.bipoleRLCVoltName, flagCurr=so.bipoleRLCCurr, currName=so.bipoleRLCCurrName,
                                  invertArrows=so.bipoleRLCVoltCurrInvert, convention=so.bipoleRLCconvention, wireExtraSize=so.bipoleRLCextraWireSize,
                                  standard=so.bipoleRLCstandard)

        # ---------------------------
        # sources
        # ---------------------------
        if so.tab == 'Sources':
            # ---------------------------
            # independendent sources
            # ---------------------------
            if so.subTab_sources == 'Indep. Source':
                if so.sourceUnit and inkDraw.useLatex:
                    so.sourceVal = latexUnitMultiple(so.sourceVal)

                if so.source == "voltIndepDC":
                    if so.sourceUnit:
                        if inkDraw.useLatex:
                            so.sourceVal += r'\si\volt'
                        else:
                            so.sourceVal += 'V'
                    self.drawSourceVDC(root_layer, position, value=so.sourceVal, angleDeg=so.sourceRot, flagVolt=so.sourceVolt,
                                       flagCurr=so.sourceCurr, currName=so.sourceCurrName, invertArrows=so.sourceVoltCurrInvert,
                                       mirror=so.sourceMirror, convention=so.sourceConvention, wireExtraSize=so.sourceExtraWireSize,
                                       flagVariable=so.sourceVariable)

                if so.source == "voltIndepDCbattery":
                    if so.sourceUnit:
                        if inkDraw.useLatex:
                            so.sourceVal += r'\si\volt'
                        else:
                            so.sourceVal += 'V'
                    self.drawSourceVDCbattery(root_layer, position, value=so.sourceVal, angleDeg=so.sourceRot, flagVolt=so.sourceVolt,
                                              flagCurr=so.sourceCurr, currName=so.sourceCurrName, invertArrows=so.sourceVoltCurrInvert,
                                              mirror=so.sourceMirror, convention=so.sourceConvention, wireExtraSize=so.sourceExtraWireSize,
                                              flagVariable=so.sourceVariable)

                if so.source == "voltIndep":
                    if so.sourceUnit:
                        if inkDraw.useLatex:
                            so.sourceVal += r'\si\volt'
                        else:
                            so.sourceVal += 'V'
                    self.drawSourceV(root_layer, position, value=so.sourceVal, sourceType='general', angleDeg=so.sourceRot, flagVolt=so.sourceVolt,
                                     flagCurr=so.sourceCurr, currName=so.sourceCurrName, invertArrows=so.sourceVoltCurrInvert, mirror=so.sourceMirror,
                                     convention=so.sourceConvention, wireExtraSize=so.sourceExtraWireSize, standard=so.sourceStandard,
                                     flagVariable=so.sourceVariable)

                if so.source == "voltIndepSinusoidal":
                    if so.sourceUnit:
                        if inkDraw.useLatex:
                            so.sourceVal += r'\si\volt'
                        else:
                            so.sourceVal += 'V'
                    self.drawSourceV(root_layer, position, value=so.sourceVal, sourceType='sinusoidal', angleDeg=so.sourceRot, flagVolt=so.sourceVolt,
                                     flagCurr=so.sourceCurr, currName=so.sourceCurrName, invertArrows=so.sourceVoltCurrInvert, mirror=so.sourceMirror,
                                     convention=so.sourceConvention, wireExtraSize=so.sourceExtraWireSize, standard=so.sourceControlledStandard,
                                     flagVariable=so.sourceVariable)

                if so.source == "currIndep":
                    if so.sourceUnit:
                        if inkDraw.useLatex:
                            so.sourceVal += r'\si\ampere'  # weird effect of ampere symbol. It causes Latex text to be misplaced.
                        else:
                            so.sourceVal += 'A'
                    self.drawSourceI(root_layer, position, value=so.sourceVal, angleDeg=so.sourceRot, flagVolt=so.sourceVolt, flagCurr=so.sourceCurr,
                                     voltName=so.sourceVoltName, invertArrows=so.sourceVoltCurrInvert, mirror=so.sourceMirror,
                                     convention=so.sourceConvention, wireExtraSize=so.sourceExtraWireSize, standard=so.sourceStandard,
                                     flagVariable=so.sourceVariable)

                if so.source == "currIndepOld":
                    if so.sourceUnit:
                        if inkDraw.useLatex:
                            so.sourceVal += r'\si\ampere'  # weird effect of ampere symbol. It causes Latex text to be misplaced.
                        else:
                            so.sourceVal += 'A'
                    self.drawSourceI(root_layer, position, value=so.sourceVal, angleDeg=so.sourceRot, flagVolt=so.sourceVolt, flagCurr=so.sourceCurr,
                                     voltName=so.sourceVoltName, invertArrows=so.sourceVoltCurrInvert, mirror=so.sourceMirror,
                                     convention=so.sourceConvention, wireExtraSize=so.sourceExtraWireSize, standard='OLD',
                                     flagVariable=so.sourceVariable)



            # --------------------------
            # controlled sources
            # ---------------------------
            if so.subTab_sources == 'Dep. Source':

                if so.sourceControlled == "volt":
                    self.drawControledSourceV(root_layer, position, controlType=so.sourceControlledType, gain=so.sourceControlledGain,
                                              controlName=so.sourceControlledControlName, angleDeg=so.sourceControlledRot, flagVolt=so.sourceVolt,
                                              flagCurr=so.sourceCurr, currName=so.sourceCurrName, invertArrows=so.sourceVoltCurrInvert,
                                              mirror=so.sourceControlledMirror, convention=so.sourceConvention,
                                              drawControl=so.sourceControlledDrawArrow,wireExtraSize=so.sourceControlledExtraWireSize,standard=so.sourceControlledStandard)

                if so.sourceControlled == "curr":
                    self.drawControledSourceI(root_layer, position, controlType=so.sourceControlledType, gain=so.sourceControlledGain,
                                              controlName=so.sourceControlledControlName, angleDeg=so.sourceControlledRot, flagVolt=so.sourceVolt,
                                              flagCurr=so.sourceCurr, voltName=so.sourceVoltName, invertArrows=so.sourceVoltCurrInvert,
                                              mirror=so.sourceControlledMirror, convention=so.sourceConvention,
                                              drawControl=so.sourceControlledDrawArrow,wireExtraSize=so.sourceControlledExtraWireSize,standard=so.sourceControlledStandard)

        # ---------------------------
        # Single Throw switches
        # ---------------------------
        if so.tab == 'Switches':
            if so.switchPushButton or so.switchThrows==1:
                flagOpen = so.switchConnection == 0
                self.drawNPST(root_layer, position, value=so.switchVal, angleDeg=so.switchRot, isPushButton=so.switchPushButton,
                              nPoles=so.switchPoles, flagOpen=flagOpen, drawCommuteArrow=so.switchCommuteArrow, commuteText=so.switchCommuteText,
                              flagVolt=so.switchVolt, voltName=so.switchVoltName, flagCurr=so.switchCurr, currName=so.switchCurrName,
                              invertArrows=so.switchVoltCurrInvert, convention=so.switchConvention,wireExtraSize=so.switchExtraWireSize)
            else:
                self.drawNPNT(root_layer, position, value=so.switchVal, angleDeg=so.switchRot, nPoles=so.switchPoles, nThrows=so.switchThrows,
                              connection=so.switchConnection, drawCommuteArrow=so.switchCommuteArrow,
                              commuteOrientation=so.switchCommuteArrowOrientation, commuteText=so.switchCommuteText, flagVolt=so.switchVolt,
                              voltName=so.switchVoltName, flagCurr=so.switchCurr, currName=so.switchCurrName, invertArrows=so.switchVoltCurrInvert,
                              convention=so.switchConvention,wireExtraSize=so.switchExtraWireSize)

        # ---------------------------
        # Transformer
        # ---------------------------
        if so.tab == 'Transformers':
            if so.transformerType.lower() == 'transformer':
                self.drawTransformer(root_layer, position, angleDeg=so.transformerRot,
                                     coreType=so.transformerCore, stepType=so.transformerStepType, flagPolaritySymbol=so.transformerPolaritySymbol,
                                     nCoils=[so.transformerNcoils1, so.transformerNcoils2],
                                     invertPolarity=[so.transformerInvPolarity1, so.transformerInvPolarity2],
                                     flagTapped=[so.transformerTapped1, so.transformerTapped2], flagVolt=[so.transformerVolt1, so.transformerVolt2],
                                     voltName=[so.transformerVoltName1, so.transformerVoltName2], flagCurr=[so.transformerCurr1, so.transformerCurr2],
                                     currName=[so.transformerCurrName1, so.transformerCurrName2],
                                     invertArrows=[so.transformerVoltCurrInvert1, so.transformerVoltCurrInvert2],
                                     convention=[so.transformerConvention1, so.transformerConvention2], wireExtraSize=so.transformerExtraWireSize)
            if so.transformerType.lower() == 'inductor':
                self.inductor(root_layer, position, angleDeg=so.transformerRot, coreType=so.transformerCore, flagTapped=so.transformerTapped1,
                              flagVolt=so.transformerVolt1, voltName=so.transformerVoltName1, flagCurr=so.transformerCurr1,
                              currName=so.transformerCurrName1, invertArrows=so.transformerVoltCurrInvert1, convention=so.transformerConvention1,
                              wireExtraSize=so.transformerExtraWireSize)

        # ---------------------------
        # diodes
        # ---------------------------
        if so.tab == 'Diodes':
            if so.diode in ['regular', 'LED', 'photoDiode', 'zener', 'schottky', 'tunnel', 'varicap']:
                self.drawDiode(root_layer, position, value=so.diodeVal, angleDeg=so.diodeRot, flagVolt=so.diodeVolt, voltName=so.diodeVoltName,
                               flagCurr=so.diodeCurr, currName=so.diodeCurrName, invertArrows=not so.diodeVoltCurrInvert, flagType=so.diode,
                               mirror=so.diodeMirror, convention=so.diodeConvention,wireExtraSize=so.diodeExtraWireSize)
        # ---------------------------
        # Transistors
        # ---------------------------
        if so.tab == 'Transistor_BJT':
            if so.BJT == 'BJT_PNP':
                typeBJT = 'PNP'
            else:
                typeBJT = 'NPN'

            if not so.BJT_IGBT:
                self.drawTransistorBJT(root_layer, position, angleDeg=so.BJT_Rot, mirrorEC=so.BJT_MirrorEC, drawBCEtags=so.BJT_EBCtags,
                                       drawEnvelope=so.BJT_Envelope, transistorType=typeBJT, flagPhototransistor=so.BJT_Photo,
                                       drawVCE=so.BJT_DrawVCEarrow, drawVCB=so.BJT_DrawVCBarrow, drawVBE=so.BJT_DrawVBEarrow,
                                       drawICarrow=so.BJT_DrawICarrow, drawIBarrow=so.BJT_DrawIBarrow, drawIEarrow=so.BJT_DrawIEarrow,
                                       VCEname=so.BJT_VCEname, VCBname=so.BJT_VCBname, VBEname=so.BJT_VBEname, ICname=so.BJT_ICname, IBname=so.BJT_IBname,
                                       IEname=so.BJT_IEname,wireExtraSize=so.BJT_ExtraWireSize)
            else:
                self.drawTransistorIGBT(root_layer, position, angleDeg=so.BJT_Rot, mirrorEC=so.BJT_MirrorEC, drawGCEtags=so.BJT_EBCtags,
                                       drawEnvelope=so.BJT_Envelope, transistorType=typeBJT,
                                       drawVCE=so.BJT_DrawVCEarrow, drawVCG=so.BJT_DrawVCBarrow, drawVGE=so.BJT_DrawVBEarrow,
                                       drawICarrow=so.BJT_DrawICarrow, drawIGarrow=so.BJT_DrawIBarrow, drawIEarrow=so.BJT_DrawIEarrow,
                                       VCEname=so.BJT_VCEname, VCGname=so.BJT_VCBname, VGEname=so.BJT_VBEname, ICname=so.BJT_ICname, IGname=so.BJT_IBname,
                                       IEname=so.BJT_IEname,wireExtraSize=so.BJT_ExtraWireSize)


        if so.tab == 'Transistor_FET':
            if 'MOSFET' in so.FET_Type:
                self.drawTransistorMOSFET(root_layer, position, angleDeg=so.FET_Rot, mirrorSD=so.FET_MirrorEC, drawSGDtags=so.FET_SGDtags,
                                          drawEnvelope=so.FET_Envelope, modeType=so.FET_Type, gateType=so.FET_Gate, MOSsymbolType=so.FET_MOSsymbolType,
                                          bodyDiode=so.FET_BodyDiode, drawVGS=so.FET_DrawVGSarrow, drawVDS=so.FET_DrawVDSarrow,
                                          drawVDG=so.FET_DrawVDGarrow, drawIDarrow=so.FET_DrawIDarrow, drawISarrow=so.FET_DrawISarrow,
                                          drawIGarrow=so.FET_DrawIGarrow, VGSname=so.FET_VGSname, VDSname=so.FET_VDSname, VDGname=so.FET_VDGname,
                                          IDname=so.FET_IDname, ISname=so.FET_ISname, IGname=so.FET_IGname,wireExtraSize=so.FET_ExtraWireSize)

            if 'JFET' in so.FET_Type:
                self.drawTransistorJFET(root_layer, position, angleDeg=so.FET_Rot, mirrorSD=so.FET_MirrorEC, drawSGDtags=so.FET_SGDtags,
                                        drawEnvelope=so.FET_Envelope, gateType=so.FET_Gate, moveGate=so.FET_MoveGate, drawVGS=so.FET_DrawVGSarrow,
                                        drawVDS=so.FET_DrawVDSarrow, drawVDG=so.FET_DrawVDGarrow, drawIDarrow=so.FET_DrawIDarrow,
                                        drawISarrow=so.FET_DrawISarrow, drawIGarrow=so.FET_DrawIGarrow, VGSname=so.FET_VGSname,
                                        VDSname=so.FET_VDSname, VDGname=so.FET_VDGname, IDname=so.FET_IDname, ISname=so.FET_ISname,
                                        IGname=so.FET_IGname,wireExtraSize=so.FET_ExtraWireSize)

        # --------------------------
        # operational amplifiers
        # ---------------------------
        if so.tab == 'Opamp':
            if so.opamp == "general":
                self.drawOpAmpGeneral(root_layer, position, mirrorInput=so.opampMirrorInput, drawVin=so.opampDrawVin, drawIin=so.opampDrawIin,
                                      drawVd=so.opampDrawVd, drawVout=so.opampDrawVout, drawIout=so.opampDrawIout,
                                      inputVPosName=so.opampInputVPosName, inputVNegName=so.opampInputVNegName, inputIPosName=so.opampInputIPosName,
                                      inputINegName=so.opampInputINegName, VoutName=so.opampVoutName, IoutName=so.opampIoutName,
                                      VdiffName=so.opampInputDiffName, flagDrawSupply=so.opampFlagSupply, FlagSupplyValues=so.opampFlagSupplyValues,
                                      flagSupplySymm=so.opampSupplySymm, supplyPositiveVal=so.opampSupplyPositiveVal,
                                      supplyNegativeVal=so.opampSupplyNegativeVal)

        if so.tab == 'SignalsAnnotation':

            # --------------------------
            # Nodes
            # ---------------------------
            if so.subTab_sigAnn == 'Signals':

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
            if so.subTab_sigAnn == 'Arrow':

                if so.arrow == "voltage":
                    if so.arrowUnit:
                        if inkDraw.useLatex:
                            so.arrowVal += r'\si\volt'
                        else:
                            so.arrowVal += 'V'
                    self.drawVoltArrowSimple(root_layer, position, name=so.arrowVal, color=self.voltageColor, angleDeg=so.arrowRot,
                                             invertArrows=so.arrowInvert, size=so.arrowVSize, invertCurvatureDirection=so.arrowCurvaturDirection)

                if so.arrow == "current":
                    if so.arrowUnit:
                        if inkDraw.useLatex:
                            so.arrowVal += r'\si\ampere'
                        else:
                            so.arrowVal += 'A'
                    self.drawCurrArrowSimple(root_layer, position, name=so.arrowVal, color=self.voltageColor, angleDeg=so.arrowRot,
                                             invertArrows=so.arrowInvert, size=so.arrowISize, invertTextSide=so.arrowCurvaturDirection)


if __name__ == '__main__':
    circuit = CircuitSymbols()
    circuit.run()
