#!/usr/bin/python

import math

import inkscapeMadeEasy_Base as inkBase
import inkscapeMadeEasy_Draw as inkDraw


class transistor(inkBase.inkscapeMadeEasy):

    # ---------------------------------------------
    # bipolar junction transistors (NPN and PNP)
    def drawTransistorBJT(self, parent, position=[0, 0], angleDeg=0, label='BJT', mirrorEC=False, drawBCEtags=False, drawEnvelope=False, transistorType='NPN', flagPhototransistor=False, drawVCE=False,
                          drawVCB=False, drawVBE=False, drawICarrow=False, drawIBarrow=False, drawIEarrow=False, VCEname='V_{ce}', VCBname='V_{cb}', VBEname='V_{be}', ICname='i_c', IBname='i_b',
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
        flagPhototransistor: creates a phototransistor (default: False)
        drawVCE,drawVCB,drawVBE: draw voltage drop annotations (default: False)
        drawICarrow,drawIBarrow,drawIEarrow: draw current annotations (default: False)
        VCEname,VCBname,VBEname: voltage drop annotation text
        ICname,IBname,IEname: current annotation text
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
            inkDraw.line.relCoords(elem, [[28, 0]], [position[0] - 10, position[1]])  # base
        else:  # light arrows
            arrow = self.createGroup(elem)
            inkDraw.line.relCoords(arrow, [[7, 0]], position)
            inkDraw.line.relCoords(arrow, [[1.5, -1.5], [-1.5, -1.5]], [position[0] + 5.5, position[1] + 1.5])
            self.rotateElement(arrow, position, -30)
            self.moveElement(arrow, [4, -7])
            arrow = self.createGroup(elem)
            inkDraw.line.relCoords(arrow, [[7, 0]], position)
            inkDraw.line.relCoords(arrow, [[1.5, -1.5], [-1.5, -1.5]], [position[0] + 5.5, position[1] + 1.5])
            self.rotateElement(arrow, position, -30)
            self.moveElement(arrow, [4, 0])

        inkDraw.line.relCoords(elem, [[0, 12]], [position[0] + 17.5, position[1] - 6], lineStyle=inkDraw.lineStyle.setSimpleBlack(lineWidth=2))  # vertical junction line

        # build emitter arrow marker
        L_arrow = 2.5
        markerBJT = inkDraw.marker.createMarker(self, 'BJTArrow', 'M 0,0 l -%f,%f l 0,-%f z' % (L_arrow * 1.2, L_arrow / 2.0, L_arrow), RenameMode=1, strokeColor=colorBlack, fillColor=colorBlack,
                                                lineWidth=0.6)
        lineStyleArrow = inkDraw.lineStyle.set(lineWidth=1, lineColor=colorBlack, markerEnd=markerBJT)

        # draw emitter and collector terminals
        if isNPN:
            inkDraw.line.relCoords(elem, [[7, -Yfactor * 5], [0, -Yfactor * 17]], [position[0] + 18, position[1] - Yfactor * 3])  # collector
            inkDraw.line.relCoords(elem, [[7, Yfactor * 5]], [position[0] + 18, position[1] + Yfactor * 3], lineStyle=lineStyleArrow)  # emitter arrow
            inkDraw.line.relCoords(elem, [[0, Yfactor * 17]], [position[0] + 25, position[1] + Yfactor * 8])  # emitter
        else:
            inkDraw.line.relCoords(elem, [[7, -Yfactor * 5], [0, -Yfactor * 17]], [position[0] + 18, position[1] - Yfactor * 3])  # collector
            inkDraw.line.relCoords(elem, [[-7, -Yfactor * 5]], [position[0] + 25, position[1] + Yfactor * 8], lineStyle=lineStyleArrow)  # emitter arrow
            inkDraw.line.relCoords(elem, [[0, Yfactor * 17]], [position[0] + 25, position[1] + Yfactor * 8])  # emitter

        if drawEnvelope:
            inkDraw.circle.centerRadius(elem, centerPoint=[position[0] + 22, position[1]], radius=10, offset=[0, 0], label='circle')

        if drawBCEtags:
            pos_Ctag = [position[0] + 22.5, position[1] - Yfactor * 12.5]
            pos_Etag = [position[0] + 22.5, position[1] + Yfactor * 12.5]
            if not flagPhototransistor:
                tB = inkDraw.text.latex(self, group, 'B', position=[position[0] + 10, position[1] - 3], fontSize=self.fontSizeSmall / 1.5, refPoint='cc', preambleFile=self.preambleFile,
                                        angleDeg=-angleDeg)
            tC = inkDraw.text.latex(self, group, 'C', position=pos_Ctag, fontSize=self.fontSizeSmall / 1.5, refPoint='cc', preambleFile=self.preambleFile, angleDeg=-angleDeg)
            tE = inkDraw.text.latex(self, group, 'E', position=pos_Etag, fontSize=self.fontSizeSmall / 1.5, refPoint='cc', preambleFile=self.preambleFile, angleDeg=-angleDeg)

        if angleDeg != 0:
            self.rotateElement(group, position, angleDeg)

        # draw voltage drops
        if drawVCE:
            pos = [position[0] + 25 + 10, position[1]]
            self.drawVoltArrowSimple(group, pos, name=VCEname, color=self.voltageColor, angleDeg=90, invertArrows=mirrorEC, size=20.0, invertCurvatureDirection=False, extraAngleText=angleDeg)

        if drawVCB:
            pos = [position[0] + 12, position[1] - Yfactor * 12]
            ang = Yfactor * 45
            self.drawVoltArrowSimple(group, pos, name=VCBname, color=self.voltageColor, angleDeg=ang, invertArrows=False, size=20.0, invertCurvatureDirection=not mirrorEC, extraAngleText=angleDeg)

        if drawVBE:
            pos = [position[0] + 12, position[1] + Yfactor * 12]
            ang = -Yfactor * 45
            self.drawVoltArrowSimple(group, pos, name=VBEname, color=self.voltageColor, angleDeg=ang, invertArrows=True, size=20.0, invertCurvatureDirection=mirrorEC, extraAngleText=angleDeg)

        # draw terminal currents
        if drawICarrow:
            self.drawCurrArrowSimple(group, [position[0] + 30, position[1] - Yfactor * 17.5], name=ICname, color=self.currentColor, angleDeg=90, invertArrows=mirrorEC ^ isNPN, size=7.5,
                                     invertTextSide=True, extraAngleText=angleDeg)

        if drawIBarrow:
            self.drawCurrArrowSimple(group, [position[0] + 7.5 - 10, position[1] - 5], name=IBname, color=self.currentColor, angleDeg=0, invertArrows=not isNPN, size=7.5, invertTextSide=False,
                                     extraAngleText=angleDeg)

        if drawIEarrow:
            self.drawCurrArrowSimple(group, [position[0] + 30, position[1] + Yfactor * 17.5], name=IEname, color=self.currentColor, angleDeg=90, invertArrows=mirrorEC ^ isNPN, size=7.5,
                                     invertTextSide=True, extraAngleText=angleDeg)
        return group

    # ---------------------------------------------
    # metal-oxide-semiconductor field-effect transistor (N and P channel)
    def drawTransistorMOSFET(self, parent, position=[0, 0], angleDeg=0, label='MOSFET', mirrorSD=False, drawSGDtags=False, drawEnvelope=False, modeType='MOSFET-E', gateType='P_gate', is4terminal=True,
                             bodyDiode=False, drawVGS=False, drawVDS=False, drawVDG=False, drawIDarrow=False, drawISarrow=False, drawIGarrow=False, VGSname='V_{GS}', VDSname='V_{SD}',
                             VDGname='V_{GD}', IDname='i_d', ISname='i_s', IGname='i_g'):

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
        is3terminal: 3 (True, Default) or 4 (False) terminals transistor
        bodyDiode: draws body diode (MOSFET-E only)
        drawVGS,drawVDS,drawVDG: draw voltage drop annotations (default: False)
        drawIDarrow,drawISarrow,drawIGarrow: draw current annotations (default: False)
        VGSname,VDSname,VDGname: voltage drop annotation text
        IDname,ISname,IGname: current annotation text
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

        L_arrow = 2.0
        markerMOS = inkDraw.marker.createMarker(self, 'MOSArrow', 'M -0.3,0 l -%f,%f l 0,-%f z' % (L_arrow * 1.2, L_arrow / 2.0, L_arrow), RenameMode=1, strokeColor=colorBlack, fillColor=colorBlack,
                                                lineWidth=0.6)
        lineStyleArrow = inkDraw.lineStyle.set(lineWidth=0.7, lineColor=colorBlack, markerEnd=markerMOS)
        lineStyleFine = inkDraw.lineStyle.set(lineWidth=0.7, lineColor=colorBlack)

        inkDraw.line.relCoords(elem, [[0, 11], [-28,0]], [position[0] + 17, position[1] - 6])  # gate

        inkDraw.line.relCoords(elem, [[0, -19.6]], [position[0] + 24, position[1] - 5.4])  # drain line
        inkDraw.line.relCoords(elem, [[5, 0]], [position[0] + 19, position[1] - 5.25], lineStyle=lineStyleFine)  # drain line

        inkDraw.line.relCoords(elem, [[0, 19.6]], [position[0] + 24, position[1] + 5.4])  # source line
        inkDraw.line.relCoords(elem, [[5, 0]], [position[0] + 19, position[1] + 5.25], lineStyle=lineStyleFine)  # source line

        if is4terminal:
            inkDraw.line.relCoords(elem, [[20, 0]], [position[0] + 24, position[1]])  # source line
        else:
            inkDraw.line.relCoords(elem, [[0, -5.25]], [position[0] + 24, position[1] + 5.25], lineStyle=lineStyleFine)  # source line
            inkDraw.circle.centerRadius(elem, [position[0] + 24, position[1] + 5.25], radius=0.4, offset=[0, 0], label='circle')  # source dot

        if isNgate:
            inkDraw.line.relCoords(elem, [[-5, 0]], [position[0] + 24, position[1] + 0], lineStyle=lineStyleArrow)  # horizontal arrow line
        else:
            inkDraw.line.relCoords(elem, [[5, 0]], [position[0] + 19, position[1] + 0], lineStyle=lineStyleArrow)  # horizontal arrow line

        if bodyDiode and isEmode and not is4terminal:
            inkDraw.circle.centerRadius(elem, [position[0] + 24, position[1] - 5.25], radius=0.4, offset=[0, 0], label='circle')  # diode cathode dot
            inkDraw.line.relCoords(elem, [[4, 0], [0, 3.75]], [position[0] + 24, position[1] - 5.25], lineStyle=lineStyleFine)  # diode cathode
            inkDraw.line.relCoords(elem, [[4, 0], [0, -3.75]], [position[0] + 24, position[1] + 5.25], lineStyle=lineStyleFine)  # diode anode

            if isNgate:
                inkDraw.line.relCoords(elem, [[3, 0]], [position[0] + 26.5, position[1] - 1.5], lineStyle=lineStyleFine)  # diode cathode side line
                inkDraw.line.relCoords(elem, [[3, 0], [-1.5, -3], [-1.5, 3]], [position[0] + 26.5, position[1] + 1.5], lineStyle=lineStyleFine)  # diode
            else:
                inkDraw.line.relCoords(elem, [[3, 0]], [position[0] + 26.5, position[1] + 1.5], lineStyle=lineStyleFine)  # diode cathode side line
                inkDraw.line.relCoords(elem, [[3, 0], [-1.5, 3], [-1.5, -3]], [position[0] + 26.5, position[1] - 1.5], lineStyle=lineStyleFine)  # diode

        if mirrorSD:
            self.scaleElement(elem, scaleX=1.0, scaleY=-1.0, center=position)
            Yfactor = -1
        else:
            Yfactor = 1

        if isEmode:
            # enhancement-mode line
            inkDraw.line.relCoords(elem, [[0, 3.5]], [position[0] + 19, position[1] - 7], lineStyle=lineStyleFine)  # vertical gate line
            inkDraw.line.relCoords(elem, [[0, 3.5]], [position[0] + 19, position[1] - 1.75], lineStyle=lineStyleFine)  # vertical gate line
            inkDraw.line.relCoords(elem, [[0, 3.5]], [position[0] + 19, position[1] + 3.5], lineStyle=lineStyleFine)  # vertical gate line
        else:
            inkDraw.line.relCoords(elem, [[0, 14]], [position[0] + 19, position[1] - 7], lineStyle=lineStyleFine)  # vertical gate line

        if drawEnvelope:
            if bodyDiode and isEmode:
                inkDraw.circle.centerRadius(elem, centerPoint=[position[0] + 22, position[1]], radius=10, offset=[0, 0], label='circle')
            else:
                inkDraw.circle.centerRadius(elem, centerPoint=[position[0] + 20, position[1]], radius=10, offset=[0, 0], label='circle')

        if drawSGDtags:
            if bodyDiode and isEmode:
                pos_Gtag = [position[0] + 9, position[1] + Yfactor * 2]
                pos_Dtag = [position[0] + 26.5, position[1] - Yfactor * 12.5]
                pos_Stag = [position[0] + 26.5, position[1] + Yfactor * 12.5]
                pos_Btag = [position[0] + 35, position[1] - Yfactor * 3]
            else:
                pos_Gtag = [position[0] + 7, position[1] + Yfactor * 2]
                pos_Dtag = [position[0] + 26.5, position[1] - Yfactor * 11.5]
                pos_Stag = [position[0] + 26.5, position[1] + Yfactor * 11.5]
                pos_Btag = [position[0] + 33, position[1] - Yfactor * 3]

            tB = inkDraw.text.latex(self, group, 'G', position=pos_Gtag, fontSize=self.fontSizeSmall / 1.5, refPoint='cc', preambleFile=self.preambleFile, angleDeg=-angleDeg)
            tC = inkDraw.text.latex(self, group, 'D', position=pos_Dtag, fontSize=self.fontSizeSmall / 1.5, refPoint='cc', preambleFile=self.preambleFile, angleDeg=-angleDeg)
            tE = inkDraw.text.latex(self, group, 'S', position=pos_Stag, fontSize=self.fontSizeSmall / 1.5, refPoint='cc', preambleFile=self.preambleFile, angleDeg=-angleDeg)
            if is4terminal:
                tB = inkDraw.text.latex(self, group, 'B', position=pos_Btag, fontSize=self.fontSizeSmall / 1.5, refPoint='cc', preambleFile=self.preambleFile, angleDeg=-angleDeg)

        if angleDeg != 0:
            self.rotateElement(group, position, angleDeg)

        # draw voltage drops
        if drawVDS:
            pos = [position[0] + 25 + 10, position[1]]
            self.drawVoltArrowSimple(group, pos, name=VDSname, color=self.voltageColor, angleDeg=90, invertArrows=mirrorSD, size=20.0, invertCurvatureDirection=False, extraAngleText=angleDeg)

        if drawVGS:
            pos = [position[0] + 15, position[1] + Yfactor * 14]
            ang = -Yfactor * 19
            self.drawVoltArrowSimple(group, pos, name=VGSname, color=self.voltageColor, angleDeg=ang, invertArrows=True, size=10.0, invertCurvatureDirection=mirrorSD, extraAngleText=angleDeg)

        if drawVDG:
            pos = [position[0] + 10, position[1] - Yfactor * 8]
            ang = Yfactor * 45
            self.drawVoltArrowSimple(group, pos, name=VDGname, color=self.voltageColor, angleDeg=ang, invertArrows=False, size=20.0, invertCurvatureDirection=not mirrorSD, extraAngleText=angleDeg)

        # draw terminal currents
        if drawISarrow:
            pos = [position[0] + 29, position[1] + Yfactor * 17.5]
            self.drawCurrArrowSimple(group, pos, name=ISname, color=self.currentColor, angleDeg=90, invertArrows=not mirrorSD, size=7.5, invertTextSide=True, extraAngleText=angleDeg)

        if drawIGarrow:
            pos = [position[0] - 5, position[1] + Yfactor * 10]
            self.drawCurrArrowSimple(group, pos, name=IGname, color=self.currentColor, angleDeg=0, invertArrows=False, size=7.5, invertTextSide=not mirrorSD, extraAngleText=angleDeg)

        if drawIDarrow:
            pos = [position[0] + 29, position[1] - Yfactor * 17.5]
            self.drawCurrArrowSimple(group, pos, name=IDname, color=self.currentColor, angleDeg=90, invertArrows=not mirrorSD, size=7.5, invertTextSide=True, extraAngleText=angleDeg)

        return group

    # ---------------------------------------------
    # junction gate field-effect transistor (N and P channel)
    def drawTransistorJFET(self, parent, position=[0, 0], angleDeg=0, label='JFET', mirrorSD=False, drawSGDtags=False, drawEnvelope=False, gateType='P_gate', moveGate=False, drawVGS=False,
                           drawVDS=False, drawVDG=False, drawIDarrow=False, drawISarrow=False, drawIGarrow=False, VGSname='V_{GS}', VDSname='V_{SD}', VDGname='V_{GD}', IDname='i_d', ISname='i_s',
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
        markerMOS = inkDraw.marker.createMarker(self, 'MOSArrow', 'M -0.3,0 l -%f,%f l 0,-%f z' % (L_arrow * 1.2, L_arrow / 2.0, L_arrow), RenameMode=1, strokeColor=colorBlack, fillColor=colorBlack,
                                                lineWidth=0.6)
        lineStyleArrow = inkDraw.lineStyle.set(lineWidth=1.0, lineColor=colorBlack, markerEnd=markerMOS)

        inkDraw.line.relCoords(elem, [[6, 0], [0, 20]], [position[0] + 17, position[1] + 5.0])  # source line
        inkDraw.line.relCoords(elem, [[6, 0], [0, -20]], [position[0] + 17, position[1] - 5.0])  # drain line

        inkDraw.line.relCoords(elem, [[0, 14]], [position[0] + 17, position[1] - 7], lineStyle=inkDraw.lineStyle.setSimpleBlack(lineWidth=2))  # vertical junction line

        if moveGate:
            posG_Y = Yfactor * 5
        else:
            posG_Y = 0

        theta = math.asin(posG_Y / R_circle)
        P1 = [10 + R_circle * (1 - math.cos(theta)), posG_Y]
        P2 = [10 + R_circle - 3, posG_Y]

        inkDraw.line.absCoords(elem, [[-12, posG_Y], P1], position)  # gate terminal

        if isNgate:
            inkDraw.line.absCoords(elem, [P1, P2], position, lineStyle=lineStyleArrow)  # gate arrow  -->
        else:
            inkDraw.line.absCoords(elem, [P2, P1], position, lineStyle=lineStyleArrow)  # gate arrow   <--

        if drawEnvelope:
            inkDraw.circle.centerRadius(elem, centerPoint=[position[0] + 19, position[1]], radius=10, offset=[0, 0], label='circle')

        if drawSGDtags:
            pos_Gtag = [position[0] + 6, position[1] - Yfactor * 3 + posG_Y]
            pos_Dtag = [position[0] + 25.5, position[1] - Yfactor * 11.5]
            pos_Stag = [position[0] + 25.5, position[1] + Yfactor * 11.5]

            tB = inkDraw.text.latex(self, group, 'G', position=pos_Gtag, fontSize=self.fontSizeSmall / 1.5, refPoint='cc', preambleFile=self.preambleFile, angleDeg=-angleDeg)
            tC = inkDraw.text.latex(self, group, 'D', position=pos_Dtag, fontSize=self.fontSizeSmall / 1.5, refPoint='cc', preambleFile=self.preambleFile, angleDeg=-angleDeg)
            tE = inkDraw.text.latex(self, group, 'S', position=pos_Stag, fontSize=self.fontSizeSmall / 1.5, refPoint='cc', preambleFile=self.preambleFile, angleDeg=-angleDeg)

        if angleDeg != 0:
            self.rotateElement(group, position, angleDeg)

        # draw voltage drops
        if drawVDS:
            pos = [position[0] + 25 + 9, position[1]]
            self.drawVoltArrowSimple(group, pos, name=VDSname, color=self.voltageColor, angleDeg=90, invertArrows=mirrorSD, size=20.0, invertCurvatureDirection=False, extraAngleText=angleDeg)

        if drawVGS:
            if moveGate:
                pos = [position[0] + 15, position[1] + Yfactor * 13]
                ang = -Yfactor * 19
                L = 10
            else:
                pos = [position[0] + 12, position[1] + Yfactor * 11]
                ang = -Yfactor * 30
                L = 15
            self.drawVoltArrowSimple(group, pos, name=VGSname, color=self.voltageColor, angleDeg=ang, invertArrows=True, size=L, invertCurvatureDirection=mirrorSD, extraAngleText=angleDeg)

        if drawVDG:
            if moveGate:
                pos = [position[0] + 12, position[1] - Yfactor * 9]
                ang = Yfactor * 45
                L = 20
            else:
                pos = [position[0] + 12, position[1] - Yfactor * 11]
                ang = Yfactor * 30
                L = 15
            self.drawVoltArrowSimple(group, pos, name=VDGname, color=self.voltageColor, angleDeg=ang, invertArrows=False, size=L, invertCurvatureDirection=not mirrorSD, extraAngleText=angleDeg)

        # draw terminal currents
        if drawISarrow:
            pos = [position[0] + 28, position[1] + Yfactor * 17.5]
            self.drawCurrArrowSimple(group, pos, name=ISname, color=self.currentColor, angleDeg=90, invertArrows=mirrorSD ^ isNgate, size=7.5, invertTextSide=True, extraAngleText=angleDeg)

        if drawIGarrow:
            pos = [position[0] - 5, position[1] + posG_Y + Yfactor * 5]
            self.drawCurrArrowSimple(group, pos, name=IGname, color=self.currentColor, angleDeg=0, invertArrows=not isNgate, size=7.5, invertTextSide=not mirrorSD, extraAngleText=angleDeg)

        if drawIDarrow:
            pos = [position[0] + 28, position[1] - Yfactor * 17.5]
            self.drawCurrArrowSimple(group, pos, name=IDname, color=self.currentColor, angleDeg=90, invertArrows=mirrorSD ^ isNgate, size=7.5, invertTextSide=True, extraAngleText=angleDeg)

        return group
