#!/usr/bin/python

import math

import inkscapeMadeEasy.inkscapeMadeEasy_Base as inkBase
import inkscapeMadeEasy.inkscapeMadeEasy_Draw as inkDraw


class transistor(inkBase.inkscapeMadeEasy):
    def add(self, vector, delta):
        # nector does not need to be numpy array. delta will be converted to numpy array. Numpy can then deal with np.array + list
        return vector + np.array(delta)

    # ---------------------------------------------
    # bipolar junction transistors (NPN and PNP)
    def drawTransistorBJT(self, parent, position=[0, 0], angleDeg=0, label='BJT', mirrorEC=False, drawBCEtags=False, drawEnvelope=False,
                          transistorType='NPN', flagPhototransistor=False, drawVCE=False, drawVCB=False, drawVBE=False, drawICarrow=False,
                          drawIBarrow=False, drawIEarrow=False, VCEname='V_{ce}', VCBname='V_{cb}', VBEname='V_{be}', ICname='i_c', IBname='i_b',
                          IEname='i_e', wireExtraSize=0):

        """ draws BJT transisitor

        parent: parent object
        label: label of the object (it can be repeated)
        position: position [x,y]
        angleDeg: orientation (default: 0.0)
        mirrorED: invert E and C terminals (default: False (C above, E below)
        drawBCEtags: indentify BCE terminals (default: False)
        drawEnvelope: draw circular envelope (default:False)
        transistorType: type of Bipolar junction transistor values: 'NPN' (Default)  'PNP'
        flagPhototransistor: creates a phototransistor (default: False)
        drawVCE,drawVCB,drawVBE: draw voltage drop annotations (default: False)
        drawICarrow,drawIBarrow,drawIEarrow: draw current annotations (default: False)
        VCEname,VCBname,VBEname: voltage drop annotation text
        ICname,IBname,IEname: current annotation text
        wireExtraSize: additional length added to the terminals. If negative, the length will be reduced. default: 0)
        """

        if transistorType == 'NPN':
            isNPN = True
        else:
            isNPN = False

        if mirrorEC:
            Yfactor = -1
        else:
            Yfactor = 1

        group = self.createGroup(parent, label)
        elem = self.createGroup(group, label)
        colorBlack = inkDraw.color.defined('black')

        if not flagPhototransistor:
            inkDraw.line.relCoords(elem, [[28 + wireExtraSize, 0]], self.add(position, [- 10 - wireExtraSize, 0]))  # base
        else:  # light arrows
            arrow = self.createGroup(elem)
            inkDraw.line.relCoords(arrow, [[7, 0]], position)
            inkDraw.line.relCoords(arrow, [[1.5, -1.5], [-1.5, -1.5]], self.add(position, [5.5, 1.5]))
            self.rotateElement(arrow, position, -30)
            self.moveElement(arrow, [4, -7])
            self.copyElement(arrow, elem, distance=[0, 7])

        # vertical junction line
        style = inkDraw.lineStyle.setSimpleBlack(lineWidth=2)
        inkDraw.line.relCoords(elem, [[0, 12]], self.add(position, [17.5, -6]), lineStyle=style)  # vertical junction line

        # build emitter arrow marker
        L_arrow = 2.5
        markerBJT = inkDraw.marker.createMarker(self, 'BJTArrow', 'M 0,0 l -%f,%f l 0,-%f z' % (L_arrow * 1.2, L_arrow / 2.0, L_arrow), RenameMode=0,
                                                strokeColor=colorBlack, fillColor=colorBlack, lineWidth=0.6)
        lineStyleArrow = inkDraw.lineStyle.set(lineWidth=1, lineColor=colorBlack, markerEnd=markerBJT)

        # draw emitter and collector terminals
        # collector
        inkDraw.line.relCoords(elem, [[7, -Yfactor * 5], [0, -Yfactor * (17 + wireExtraSize)]], self.add(position, [18, - Yfactor * 3]))
        if isNPN:
            inkDraw.line.relCoords(elem, [[7, Yfactor * 5]], self.add(position, [18, Yfactor * 3]), lineStyle=lineStyleArrow)  # emitter arrow
            inkDraw.line.relCoords(elem, [[0, Yfactor * (17 + wireExtraSize)]], self.add(position, [25, Yfactor * 8]))  # emitter
        else:
            inkDraw.line.relCoords(elem, [[-7, -Yfactor * 5]], self.add(position, [25, Yfactor * 8]), lineStyle=lineStyleArrow)  # emitter arrow
            inkDraw.line.relCoords(elem, [[0, Yfactor * (17 + wireExtraSize)]], self.add(position, [25, Yfactor * 8]))  # emitter

        if drawEnvelope:
            inkDraw.circle.centerRadius(elem, centerPoint=self.add(position, [22, 0]), radius=10, offset=[0, 0], label='circle')

        if drawBCEtags:
            pos_Ctag = self.add(position, [22.5, -Yfactor * 12.5])
            pos_Etag = self.add(position, [22.5, Yfactor * 12.5])
            if not flagPhototransistor:
                tB = inkDraw.text.latex(self, group, 'B', position=self.add(position, [10, -3]), fontSize=self.fontSizeSmall / 1.5, refPoint='cc',
                                        preambleFile=self.preambleFile, angleDeg=-angleDeg)
            tC = inkDraw.text.latex(self, group, 'C', position=pos_Ctag, fontSize=self.fontSizeSmall / 1.5, refPoint='cc',
                                    preambleFile=self.preambleFile, angleDeg=-angleDeg)
            tE = inkDraw.text.latex(self, group, 'E', position=pos_Etag, fontSize=self.fontSizeSmall / 1.5, refPoint='cc',
                                    preambleFile=self.preambleFile, angleDeg=-angleDeg)

        if angleDeg != 0:
            self.rotateElement(group, position, angleDeg)

        # draw voltage drops
        if drawVCE:
            pos = self.add(position, [25 + 10, 0])
            self.drawVoltArrowSimple(group, pos, name=VCEname, color=self.voltageColor, angleDeg=90, invertArrows=mirrorEC, size=20.0,
                                     invertCurvatureDirection=False, extraAngleText=angleDeg)

        if drawVCB:
            pos = self.add(position, [12, - Yfactor * 12])
            ang = Yfactor * 45
            self.drawVoltArrowSimple(group, pos, name=VCBname, color=self.voltageColor, angleDeg=ang, invertArrows=False, size=20.0,
                                     invertCurvatureDirection=not mirrorEC, extraAngleText=angleDeg)

        if drawVBE:
            pos = self.add(position, [12, Yfactor * 12])
            ang = -Yfactor * 45
            self.drawVoltArrowSimple(group, pos, name=VBEname, color=self.voltageColor, angleDeg=ang, invertArrows=True, size=20.0,
                                     invertCurvatureDirection=mirrorEC, extraAngleText=angleDeg)

        # draw terminal currents
        if drawICarrow:
            self.drawCurrArrowSimple(group, self.add(position, [30, - Yfactor * (20 + wireExtraSize)]), name=ICname, color=self.currentColor,
                                     angleDeg=90, invertArrows=mirrorEC ^ isNPN, size=7.5, invertTextSide=True, extraAngleText=angleDeg)

        if drawIBarrow:
            self.drawCurrArrowSimple(group, self.add(position, [7.5 - 10, - 5]), name=IBname, color=self.currentColor, angleDeg=0,
                                     invertArrows=not isNPN, size=7.5, invertTextSide=False, extraAngleText=angleDeg)

        if drawIEarrow:
            self.drawCurrArrowSimple(group, self.add(position, [30, Yfactor * (20 + wireExtraSize)]), name=IEname, color=self.currentColor,
                                     angleDeg=90, invertArrows=mirrorEC ^ isNPN, size=7.5, invertTextSide=True, extraAngleText=angleDeg)
        return group

    # ---------------------------------------------
    # Insulated Gate Bipolar Transistor (NPN and PNP)
    def drawTransistorIGBT(self, parent, position=[0, 0], angleDeg=0, label='IGBT', mirrorEC=False, drawGCEtags=False, drawEnvelope=False,
                          transistorType='NPN', drawVCE=False, drawVCG=False, drawVGE=False, drawICarrow=False,
                          drawIGarrow=False, drawIEarrow=False, VCEname='V_{ce}', VCGname='V_{cb}', VGEname='V_{be}', ICname='i_c', IGname='i_b',
                          IEname='i_e', wireExtraSize=0):

        """ draws BJT transisitor

        parent: parent object
        label: label of the object (it can be repeated)
        position: position [x,y]
        angleDeg: orientation (default: 0.0)
        mirrorED: invert E and C terminals (default: False (C above, E below)
        drawGCEtags: indentify BCE terminals (default: False)
        drawEnvelope: draw circular envelope (default:False)
        transistorType: type of Bipolar junction transistor values: 'NPN' (Default)  'PNP'
        drawVCE,drawVCG,drawVGE: draw voltage drop annotations (default: False)
        drawICarrow,drawIGarrow,drawIEarrow: draw current annotations (default: False)
        VCEname,VCGname,VGEname: voltage drop annotation text
        ICname,IGname,IEname: current annotation text
        wireExtraSize: additional length added to the terminals. If negative, the length will be reduced. default: 0)
        """

        if transistorType == 'NPN':
            isNPN = True
        else:
            isNPN = False

        if mirrorEC:
            Yfactor = -1
        else:
            Yfactor = 1

        group = self.createGroup(parent, label)
        elem = self.createGroup(group, label)
        colorBlack = inkDraw.color.defined('black')

        inkDraw.line.relCoords(elem, [[26 + wireExtraSize, 0]], self.add(position, [- 10 - wireExtraSize, 0]))  # base

        # vertical junction line
        inkDraw.line.relCoords(elem, [[0, 12]], self.add(position, [18, -6]))  # vertical junction line
        inkDraw.line.relCoords(elem, [[0, 10]], self.add(position, [16, -5]))  # vertical junction line

        # build emitter arrow marker
        L_arrow = 2.5
        markerBJT = inkDraw.marker.createMarker(self, 'BJTArrow', 'M 0,0 l -%f,%f l 0,-%f z' % (L_arrow * 1.2, L_arrow / 2.0, L_arrow), RenameMode=0,
                                                strokeColor=colorBlack, fillColor=colorBlack, lineWidth=0.6)
        lineStyleArrow = inkDraw.lineStyle.set(lineWidth=1, lineColor=colorBlack, markerEnd=markerBJT)

        # draw emitter and collector terminals
        # collector
        inkDraw.line.relCoords(elem, [[7, -Yfactor * 5], [0, -Yfactor * (17 + wireExtraSize)]], self.add(position, [18, - Yfactor * 3]))
        if isNPN:
            inkDraw.line.relCoords(elem, [[7, Yfactor * 5]], self.add(position, [18, Yfactor * 3]), lineStyle=lineStyleArrow)  # emitter arrow
            inkDraw.line.relCoords(elem, [[0, Yfactor * (17 + wireExtraSize)]], self.add(position, [25, Yfactor * 8]))  # emitter
        else:
            inkDraw.line.relCoords(elem, [[-7, -Yfactor * 5]], self.add(position, [25, Yfactor * 8]), lineStyle=lineStyleArrow)  # emitter arrow
            inkDraw.line.relCoords(elem, [[0, Yfactor * (17 + wireExtraSize)]], self.add(position, [25, Yfactor * 8]))  # emitter

        if drawEnvelope:
            inkDraw.circle.centerRadius(elem, centerPoint=self.add(position, [22, 0]), radius=10, offset=[0, 0], label='circle')

        if drawGCEtags:
            pos_Ctag = self.add(position, [22.5, -Yfactor * 12.5])
            pos_Etag = self.add(position, [22.5, Yfactor * 12.5])

            tB = inkDraw.text.latex(self, group, 'G', position=self.add(position, [10, -3]), fontSize=self.fontSizeSmall / 1.5, refPoint='cc',
                                        preambleFile=self.preambleFile, angleDeg=-angleDeg)
            tC = inkDraw.text.latex(self, group, 'C', position=pos_Ctag, fontSize=self.fontSizeSmall / 1.5, refPoint='cc',
                                    preambleFile=self.preambleFile, angleDeg=-angleDeg)
            tE = inkDraw.text.latex(self, group, 'E', position=pos_Etag, fontSize=self.fontSizeSmall / 1.5, refPoint='cc',
                                    preambleFile=self.preambleFile, angleDeg=-angleDeg)

        if angleDeg != 0:
            self.rotateElement(group, position, angleDeg)

        # draw voltage drops
        if drawVCE:
            pos = self.add(position, [25 + 10, 0])
            self.drawVoltArrowSimple(group, pos, name=VCEname, color=self.voltageColor, angleDeg=90, invertArrows=mirrorEC, size=20.0,
                                     invertCurvatureDirection=False, extraAngleText=angleDeg)

        if drawVCG:
            pos = self.add(position, [12, - Yfactor * 12])
            ang = Yfactor * 45
            self.drawVoltArrowSimple(group, pos, name=VCGname, color=self.voltageColor, angleDeg=ang, invertArrows=False, size=20.0,
                                     invertCurvatureDirection=not mirrorEC, extraAngleText=angleDeg)

        if drawVGE:
            pos = self.add(position, [12, Yfactor * 12])
            ang = -Yfactor * 45
            self.drawVoltArrowSimple(group, pos, name=VGEname, color=self.voltageColor, angleDeg=ang, invertArrows=True, size=20.0,
                                     invertCurvatureDirection=mirrorEC, extraAngleText=angleDeg)

        # draw terminal currents
        if drawICarrow:
            self.drawCurrArrowSimple(group, self.add(position, [30, - Yfactor * (20 + wireExtraSize)]), name=ICname, color=self.currentColor,
                                     angleDeg=90, invertArrows=mirrorEC ^ isNPN, size=7.5, invertTextSide=True, extraAngleText=angleDeg)

        if drawIGarrow:
            self.drawCurrArrowSimple(group, self.add(position, [7.5 - 10, - 5]), name=IGname, color=self.currentColor, angleDeg=0,
                                     invertArrows=not isNPN, size=7.5, invertTextSide=False, extraAngleText=angleDeg)

        if drawIEarrow:
            self.drawCurrArrowSimple(group, self.add(position, [30, Yfactor * (20 + wireExtraSize)]), name=IEname, color=self.currentColor,
                                     angleDeg=90, invertArrows=mirrorEC ^ isNPN, size=7.5, invertTextSide=True, extraAngleText=angleDeg)
        return group

    # ---------------------------------------------
    # metal-oxide-semiconductor field-effect transistor (N and P channel)
    def drawTransistorMOSFET(self, parent, position=[0, 0], angleDeg=0, label='MOSFET', mirrorSD=False, drawSGDtags=False, drawEnvelope=False,
                             modeType='MOSFET-E', gateType='P_gate', MOSsymbolType=True, bodyDiode=False, drawVGS=False, drawVDS=False, drawVDG=False,
                             drawIDarrow=False, drawISarrow=False, drawIGarrow=False, VGSname='V_{GS}', VDSname='V_{SD}', VDGname='V_{GD}',
                             IDname='i_d', ISname='i_s', IGname='i_g', wireExtraSize=0):

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
        MOSsymbolType: symbol type: '3T', '4T', '3TnB', 'shorthand'
        bodyDiode: draws body diode (MOSFET-E only)
        drawVGS,drawVDS,drawVDG: draw voltage drop annotations (default: False)
        drawIDarrow,drawISarrow,drawIGarrow: draw current annotations (default: False)
        VGSname,VDSname,VDGname: voltage drop annotation text
        IDname,ISname,IGname: current annotation text
        wireExtraSize: additional length added to the terminals. If negative, the length will be reduced. default: 0)
        """

        if gateType == 'P_gate':
            isNgate = False
        else:
            isNgate = True

        if modeType == 'MOSFET-E':
            isEmode = True
        else:
            isEmode = False

        group = self.createGroup(parent, label)
        elem = self.createGroup(group, label)
        colorBlack = inkDraw.color.defined('black')
        colorWhite = inkDraw.color.defined('white')

        L_arrow = 2.0
        if drawEnvelope:
            lineWidth = 0.7
        else:
            lineWidth = 1.0

        markerMOSa = inkDraw.marker.createMarker(self, 'MOSArrowA', 'M -0.1,0 l -%f,%f l 0,-%f z' % (L_arrow * 1.2, L_arrow / 2.0, L_arrow),
                                                RenameMode=0, strokeColor=colorBlack, fillColor=colorBlack, lineWidth=0.6)
        lineStyleArrow = inkDraw.lineStyle.set(lineWidth=1.0, lineColor=colorBlack, markerEnd=markerMOSa)
        markerMOS = inkDraw.marker.createMarker(self, 'MOSArrowB', 'M -0.3,0 l -%f,%f l 0,-%f z' % (L_arrow * 1.2, L_arrow / 2.0, L_arrow),
                                                RenameMode=0, strokeColor=colorBlack, fillColor=colorBlack, lineWidth=0.6)
        lineStyleArrowFine = inkDraw.lineStyle.set(lineWidth=lineWidth, lineColor=colorBlack, markerEnd=markerMOS)
        lineStyleFine = inkDraw.lineStyle.set(lineWidth=lineWidth, lineColor=colorBlack)
        lineStyleBold = inkDraw.lineStyle.set(lineWidth=2, lineColor=colorBlack)
        lineStyleBoldFine = inkDraw.lineStyle.set(lineWidth=1.5, lineColor=colorBlack)
        #--- GATE
        if MOSsymbolType == 'shorthand':
            if not isEmode:
                inkDraw.line.relCoords(elem, [[0, 12]], self.add(position, [16, -6]), lineStyle=lineStyleFine)  # gate
                if isNgate:
                    inkDraw.line.relCoords(elem, [ [-(26.75 + wireExtraSize), 0]], self.add(position, [15.75, 0]))  # gate
                else:
                    inkDraw.line.relCoords(elem, [ [-(24.75 + wireExtraSize), 0]], self.add(position, [13.75, 0]))  # gate
                    inkDraw.circle.centerRadius(elem, self.add(position, [15, 0]), radius=1.0, offset=[0,0], label='circle',lineStyle=lineStyleFine) # gate negate input
            else:
                inkDraw.line.relCoords(elem, [[0, 12]], self.add(position, [17, -6]), lineStyle=lineStyleFine)  # gate
                if isNgate:
                    inkDraw.line.relCoords(elem, [ [-(27.75 + wireExtraSize), 0]], self.add(position, [16.75, 0]))  # gate
                else:
                    inkDraw.line.relCoords(elem, [ [-(25.75 + wireExtraSize), 0]], self.add(position, [14.75, 0]))  # gate
                    inkDraw.circle.centerRadius(elem, self.add(position, [16, 0]), radius=1.0, offset=[0,0], label='circle',lineStyle=lineStyleFine) # gate negate input

        if MOSsymbolType == '3TnB':
            inkDraw.line.relCoords(elem, [[0, 12]], self.add(position, [17, -6]), lineStyle=lineStyleFine)  # gate
            inkDraw.line.relCoords(elem, [ [-(27.75 + wireExtraSize), 0]], self.add(position, [16.75, 0]))  # gate

        if MOSsymbolType == '4T' or MOSsymbolType == '3T':
            inkDraw.line.relCoords(elem, [[0, 11]], self.add(position, [17, -6]), lineStyle=lineStyleFine)  # gate
            inkDraw.line.relCoords(elem, [ [-(27.75 + wireExtraSize), 0]], self.add(position, [16.75, 5]))  # gate

        #--- DRAIN
        inkDraw.line.relCoords(elem, [[0, -(19.6 + wireExtraSize)]], self.add(position, [24, -5.4]))  # drain line
        inkDraw.line.relCoords(elem, [[5, 0]], self.add(position, [19, -5.25]), lineStyle=lineStyleFine)  # drain line

        #--- SOURCE
        inkDraw.line.relCoords(elem, [[0, 19.6 + wireExtraSize]], self.add(position, [24, 5.4]))  # source line
        if MOSsymbolType == '3TnB':
            if not isNgate:
                inkDraw.line.relCoords(elem, [[-5, 0]], self.add(position, [24, 5.25]), lineStyle=lineStyleArrowFine)  # source current arrow
            else:
                inkDraw.line.relCoords(elem, [[5, 0]], self.add(position, [19, 5.25]), lineStyle=lineStyleArrowFine)  # source current arrow
        else:
            inkDraw.line.relCoords(elem, [[5, 0]], self.add(position, [19, 5.25]), lineStyle=lineStyleFine)  # source line

        #--- BULK
        if MOSsymbolType == '4T':
            inkDraw.line.relCoords(elem, [[25 + wireExtraSize, 0]], self.add(position, [24, 0]))  # bulk line
        if MOSsymbolType == '3T':
            inkDraw.line.relCoords(elem, [[0, -5.25]], self.add(position, [24, 5.25]), lineStyle=lineStyleFine)  # source-bulk connection line
            inkDraw.circle.centerRadius(elem, self.add(position, [24, 5.25]), radius=0.4, offset=[0, 0], label='circle')  # source dot

        if MOSsymbolType == '4T':
            if isNgate:
                inkDraw.line.relCoords(elem, [[-4.75, 0]], self.add(position, [24, 0]), lineStyle=lineStyleArrow)  # PN bulk junction
            else:
                inkDraw.line.relCoords(elem, [[5, 0]], self.add(position, [19.25, 0]), lineStyle=lineStyleArrow)  # PN bulk junction

        if MOSsymbolType == '3T':
            if isNgate:
                inkDraw.line.relCoords(elem, [[-5, 0]], self.add(position, [24, 0]), lineStyle=lineStyleArrowFine)  # PN bulk junction
            else:
                inkDraw.line.relCoords(elem, [[5, 0]], self.add(position, [19, 0]), lineStyle=lineStyleArrowFine)  # PN bulk junction

        #--- BODY DIODE
        if bodyDiode and isEmode and MOSsymbolType == '3T':
            lineStyleDiode = inkDraw.lineStyle.set(lineWidth=0.7, lineColor=colorBlack)
            inkDraw.circle.centerRadius(elem, self.add(position, [24, -5.25]), radius=0.4, offset=[0, 0], label='circle')  # diode cathode dot
            inkDraw.line.relCoords(elem, [[4, 0], [0, 3.75]], self.add(position, [24, -5.25]), lineStyle=lineStyleDiode)  # diode cathode
            inkDraw.line.relCoords(elem, [[4, 0], [0, -3.75]], self.add(position, [24, 5.25]), lineStyle=lineStyleDiode)  # diode anode

            if isNgate:
                inkDraw.line.relCoords(elem, [[3, 0]], self.add(position, [26.5, -1.5]), lineStyle=lineStyleDiode)  # diode cathode side line
                inkDraw.line.relCoords(elem, [[3, 0], [-1.5, -3], [-1.5, 3]], self.add(position, [26.5, 1.5]), lineStyle=lineStyleDiode)  # diode
            else:
                inkDraw.line.relCoords(elem, [[3, 0]], self.add(position, [26.5, 1.5]), lineStyle=lineStyleDiode)  # diode cathode side line
                inkDraw.line.relCoords(elem, [[3, 0], [-1.5, 3], [-1.5, -3]], self.add(position, [26.5, -1.5]), lineStyle=lineStyleDiode)  # diode

        if mirrorSD:
            self.scaleElement(elem, scaleX=1.0, scaleY=-1.0, center=position)
            Yfactor = -1
        else:
            Yfactor = 1

        #--- VERTICAL CHANNEL LINE
        if MOSsymbolType == 'shorthand':
            if isEmode:
                inkDraw.line.relCoords(elem, [[0, 14]], self.add(position, [19, -7]), lineStyle=lineStyleFine)  # vertical channel line
            else:
                inkDraw.line.relCoords(elem, [[0, 14]], self.add(position, [18.65, -7]), lineStyle=lineStyleBold)  # vertical channel line
        else:
            if isEmode:
                # enhancement-mode line
                inkDraw.line.relCoords(elem, [[0, 3.5]], self.add(position, [19, -7]), lineStyle=lineStyleFine)  # vertical channel line
                inkDraw.line.relCoords(elem, [[0, 3.5]], self.add(position, [19, -1.75]), lineStyle=lineStyleFine)  # vertical channel line
                inkDraw.line.relCoords(elem, [[0, 3.5]], self.add(position, [19, 3.5]), lineStyle=lineStyleFine)  # vertical channel line
            else:
                inkDraw.line.relCoords(elem, [[0, 14]], self.add(position, [19, -7]), lineStyle=lineStyleFine)  # vertical channel line

        #--- ENVELOPE
        if drawEnvelope:
            if bodyDiode and isEmode and MOSsymbolType == '3T':
                inkDraw.circle.centerRadius(elem, centerPoint=self.add(position, [22, 0]), radius=10, offset=[0, 0], label='circle')
            else:
                inkDraw.circle.centerRadius(elem, centerPoint=self.add(position, [20, 0]), radius=10, offset=[0, 0], label='circle')

        #--- TAGS
        if drawSGDtags:
            if bodyDiode and isEmode and MOSsymbolType == '3T':
                pos_Gtag = self.add(position, [9, Yfactor * 2])
                pos_Dtag = self.add(position, [26.5, - Yfactor * 12.5])
                pos_Stag = self.add(position, [26.5, Yfactor * 12.5])
                pos_Btag = self.add(position, [35, - Yfactor * 3])
            else:
                pos_Gtag = self.add(position, [7, Yfactor * 2])
                pos_Dtag = self.add(position, [26.5, - Yfactor * 11.5])
                pos_Stag = self.add(position, [26.5, Yfactor * 11.5])
                pos_Btag = self.add(position, [33, - Yfactor * 3])

            tB = inkDraw.text.latex(self, group, 'G', position=pos_Gtag, fontSize=self.fontSizeSmall / 1.5, refPoint='cc',
                                    preambleFile=self.preambleFile, angleDeg=-angleDeg)
            tC = inkDraw.text.latex(self, group, 'D', position=pos_Dtag, fontSize=self.fontSizeSmall / 1.5, refPoint='cc',
                                    preambleFile=self.preambleFile, angleDeg=-angleDeg)
            tE = inkDraw.text.latex(self, group, 'S', position=pos_Stag, fontSize=self.fontSizeSmall / 1.5, refPoint='cc',
                                    preambleFile=self.preambleFile, angleDeg=-angleDeg)
            if MOSsymbolType == '4T':
                tB = inkDraw.text.latex(self, group, 'B', position=pos_Btag, fontSize=self.fontSizeSmall / 1.5, refPoint='cc',
                                        preambleFile=self.preambleFile, angleDeg=-angleDeg)

        if angleDeg != 0:
            self.rotateElement(group, position, angleDeg)

        # draw voltage drops
        if drawVDS:
            pos = self.add(position, [25 + 10, 0])
            self.drawVoltArrowSimple(group, pos, name=VDSname, color=self.voltageColor, angleDeg=90, invertArrows=mirrorSD, size=20.0,
                                     invertCurvatureDirection=False, extraAngleText=angleDeg)

        if drawVGS:
            pos = self.add(position, [15, Yfactor * 14])
            ang = -Yfactor * 19
            self.drawVoltArrowSimple(group, pos, name=VGSname, color=self.voltageColor, angleDeg=ang, invertArrows=True, size=10.0,
                                     invertCurvatureDirection=mirrorSD, extraAngleText=angleDeg)

        if drawVDG:
            pos = self.add(position, [10, -Yfactor * 8])
            ang = Yfactor * 45
            self.drawVoltArrowSimple(group, pos, name=VDGname, color=self.voltageColor, angleDeg=ang, invertArrows=False, size=20.0,
                                     invertCurvatureDirection=not mirrorSD, extraAngleText=angleDeg)

        # draw terminal currents
        if drawISarrow:
            pos = self.add(position, [29, Yfactor * 17.5])
            self.drawCurrArrowSimple(group, pos, name=ISname, color=self.currentColor, angleDeg=90, invertArrows=not mirrorSD, size=7.5,
                                     invertTextSide=True, extraAngleText=angleDeg)

        if drawIGarrow:
            pos = self.add(position, [-5, Yfactor * 10])
            self.drawCurrArrowSimple(group, pos, name=IGname, color=self.currentColor, angleDeg=0, invertArrows=False, size=7.5,
                                     invertTextSide=not mirrorSD, extraAngleText=angleDeg)

        if drawIDarrow:
            pos = self.add(position, [29, -Yfactor * 17.5])
            self.drawCurrArrowSimple(group, pos, name=IDname, color=self.currentColor, angleDeg=90, invertArrows=not mirrorSD, size=7.5,
                                     invertTextSide=True, extraAngleText=angleDeg)

        return group

    # ---------------------------------------------
    # junction gate field-effect transistor (N and P channel)
    def drawTransistorJFET(self, parent, position=[0, 0], angleDeg=0, label='JFET', mirrorSD=False, drawSGDtags=False, drawEnvelope=False,
                           gateType='P_gate', moveGate=False, drawVGS=False, drawVDS=False, drawVDG=False, drawIDarrow=False, drawISarrow=False,
                           drawIGarrow=False, VGSname='V_{GS}', VDSname='V_{SD}', VDGname='V_{GD}', IDname='i_d', ISname='i_s', IGname='i_g',
                           wireExtraSize=0):

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
        wireExtraSize: additional length added to the terminals. If negative, the length will be reduced. default: 0)
        """

        if gateType == 'P_gate':
            isNgate = False
        else:
            isNgate = True

        if mirrorSD:
            Yfactor = -1
        else:
            Yfactor = 1

        group = self.createGroup(parent, label)
        elem = self.createGroup(group, label)
        colorBlack = inkDraw.color.defined('black')

        R_circle = 10.0
        L_arrow = 2.0
        markerMOS = inkDraw.marker.createMarker(self, 'MOSArrow', 'M -0.3,0 l -%f,%f l 0,-%f z' % (L_arrow * 1.2, L_arrow / 2.0, L_arrow),
                                                RenameMode=0, strokeColor=colorBlack, fillColor=colorBlack, lineWidth=0.6)
        lineStyleArrow = inkDraw.lineStyle.set(lineWidth=1.0, lineColor=colorBlack, markerEnd=markerMOS)

        inkDraw.line.relCoords(elem, [[6, 0], [0, 20 + wireExtraSize]], self.add(position, [17, 5]))  # source line
        inkDraw.line.relCoords(elem, [[6, 0], [0, -(20 + wireExtraSize)]], self.add(position, [17, -5]))  # drain line

        # vertical junction line
        inkDraw.line.relCoords(elem, [[0, 14]], self.add(position, [17, -7]), lineStyle=inkDraw.lineStyle.setSimpleBlack(lineWidth=2))

        if moveGate:
            posG_Y = Yfactor * 5
        else:
            posG_Y = 0

        theta = math.asin(posG_Y / R_circle)
        P1 = [10 + R_circle * (1 - math.cos(theta)), posG_Y]
        P2 = [10 + R_circle - 3, posG_Y]

        inkDraw.line.absCoords(elem, [[-(12 + wireExtraSize), posG_Y], P1], position)  # gate terminal

        if isNgate:
            inkDraw.line.absCoords(elem, [P1, P2], position, lineStyle=lineStyleArrow)  # gate arrow  -->
        else:
            inkDraw.line.absCoords(elem, [P2, P1], position, lineStyle=lineStyleArrow)  # gate arrow   <--

        if drawEnvelope:
            inkDraw.circle.centerRadius(elem, centerPoint=self.add(position, [19, 0]), radius=10, offset=[0, 0], label='circle')

        if drawSGDtags:
            pos_Gtag = self.add(position, [6, - Yfactor * 3 + posG_Y])
            pos_Dtag = self.add(position, [25.5, - Yfactor * 11.5])
            pos_Stag = self.add(position, [25.5, Yfactor * 11.5])

            tB = inkDraw.text.latex(self, group, 'G', position=pos_Gtag, fontSize=self.fontSizeSmall / 1.5, refPoint='cc',
                                    preambleFile=self.preambleFile, angleDeg=-angleDeg)
            tC = inkDraw.text.latex(self, group, 'D', position=pos_Dtag, fontSize=self.fontSizeSmall / 1.5, refPoint='cc',
                                    preambleFile=self.preambleFile, angleDeg=-angleDeg)
            tE = inkDraw.text.latex(self, group, 'S', position=pos_Stag, fontSize=self.fontSizeSmall / 1.5, refPoint='cc',
                                    preambleFile=self.preambleFile, angleDeg=-angleDeg)

        if angleDeg != 0:
            self.rotateElement(group, position, angleDeg)

        # draw voltage drops
        if drawVDS:
            pos = self.add(position, [25 + 9, 0])
            self.drawVoltArrowSimple(group, pos, name=VDSname, color=self.voltageColor, angleDeg=90, invertArrows=mirrorSD, size=20.0,
                                     invertCurvatureDirection=False, extraAngleText=angleDeg)

        if drawVGS:
            if moveGate:
                pos = self.add(position, [15, Yfactor * 13])
                ang = -Yfactor * 19
                L = 10
            else:
                pos = self.add(position, [12, Yfactor * 11])
                ang = -Yfactor * 30
                L = 15
            self.drawVoltArrowSimple(group, pos, name=VGSname, color=self.voltageColor, angleDeg=ang, invertArrows=True, size=L,
                                     invertCurvatureDirection=mirrorSD, extraAngleText=angleDeg)

        if drawVDG:
            if moveGate:
                pos = self.add(position, [12, - Yfactor * 9])
                ang = Yfactor * 45
                L = 20
            else:
                pos = self.add(position, [12, - Yfactor * 11])
                ang = Yfactor * 30
                L = 15
            self.drawVoltArrowSimple(group, pos, name=VDGname, color=self.voltageColor, angleDeg=ang, invertArrows=False, size=L,
                                     invertCurvatureDirection=not mirrorSD, extraAngleText=angleDeg)

        # draw terminal currents
        if drawISarrow:
            pos = self.add(position, [28, Yfactor * 17.5])
            self.drawCurrArrowSimple(group, pos, name=ISname, color=self.currentColor, angleDeg=90, invertArrows=mirrorSD ^ isNgate, size=7.5,
                                     invertTextSide=True, extraAngleText=angleDeg)

        if drawIGarrow:
            pos = self.add(position, [-5, posG_Y + Yfactor * 5])
            self.drawCurrArrowSimple(group, pos, name=IGname, color=self.currentColor, angleDeg=0, invertArrows=not isNgate, size=7.5,
                                     invertTextSide=not mirrorSD, extraAngleText=angleDeg)

        if drawIDarrow:
            pos = self.add(position, [28, - Yfactor * 17.5])
            self.drawCurrArrowSimple(group, pos, name=IDname, color=self.currentColor, angleDeg=90, invertArrows=mirrorSD ^ isNgate, size=7.5,
                                     invertTextSide=True, extraAngleText=angleDeg)

        return group
