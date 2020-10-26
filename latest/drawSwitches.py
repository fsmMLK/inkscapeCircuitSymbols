#!/usr/bin/python

import inkscapeMadeEasy.inkscapeMadeEasy_Base as inkBase
import inkscapeMadeEasy.inkscapeMadeEasy_Draw as inkDraw


class switch(inkBase.inkscapeMadeEasy):

    # ---------------------------------------------
    def drawNPST(self, parent, position=[0, 0], value='S', label='Switch', angleDeg=0, isPushButton=False, nPoles=1, flagOpen=True,
                 drawCommuteArrow=False, commuteText='', flagVolt=True, voltName='v', flagCurr=True, currName='i', invertArrows=False,
                 convention='passive'):
        """ draws a switch with two terminals only

        parent: parent object
        position: position [x,y]
        value: string with resistor value. (default 'S')
        label: label of the object (it can be repeated)
        angleDeg: rotation angle in degrees counter-clockwise (default 0)
        isPushButton: draws push-button (defalut: False)
        nPoles: numer of poles (default: 1)
        flagOpen: normaly open switch (default:True)
        drawCommuteArrow: draw comuting arrow (default: False)
        commuteText: string with comuting info
        flagVolt: indicates whether the voltage arrow must be drawn (default: true)
        voltName: voltage drop name (default: v)
        flagCurr: indicates whether the current arrow must be drawn (default: true)
        currName: current drop name (default: i)
        invertArrows: invert V/I arrow directions (default: False)
        convention: passive/active sign convention. available types: 'passive' (default) , 'active'
        """

        group = self.createGroup(parent, label)
        elem = self.createGroup(group, label)
        color = inkDraw.color.defined('red')
        colorBlack = inkDraw.color.defined('black')
        colorWhite = inkDraw.color.defined('white')
        lineStyleSign = inkDraw.lineStyle.set(lineWidth=0.7, lineColor=colorBlack, fillColor=colorWhite)
        [arrowStart, arrowEnd] = inkDraw.marker.createArrow1Marker(self, 'arrowSwitch', RenameMode=0, scale=0.25, strokeColor=color, fillColor=color)

        inkDraw.line.relCoords(elem, [[15, 0]], position)
        inkDraw.line.relCoords(elem, [[-15, 0]], [position[0] + 50, position[1]])

        if isPushButton:  # push-button
            if flagOpen:
                inkDraw.line.relCoords(elem, [[20, 0]], [position[0] + 15, position[1] - 5])
                inkDraw.line.relCoords(elem, [[0, -7]], [position[0] + 25, position[1] - 5])
            else:
                inkDraw.line.relCoords(elem, [[20, 0]], [position[0] + 15, position[1] + 2])
                inkDraw.line.relCoords(elem, [[0, -9]], [position[0] + 15, position[1] + 2])
        else:  # throw switch
            if flagOpen:
                inkDraw.line.relCoords(elem, [[20, -8]], [position[0] + 15, position[1]])
            else:
                inkDraw.line.relCoords(elem, [[20, -2]], [position[0] + 15, position[1]])

        inkDraw.circle.centerRadius(elem, [position[0] + 35, position[1]], 1.2, offset=[0, 0], lineStyle=lineStyleSign)
        inkDraw.circle.centerRadius(elem, [position[0] + 15, position[1]], 1.2, offset=[0, 0], lineStyle=lineStyleSign)

        if drawCommuteArrow:
            if commuteText:
                if isPushButton:  # push-button
                    pos_text = [position[0] + 12, position[1] - 10 - self.textOffset]
                else:  # throw switch
                    pos_text = [position[0] + 12, position[1] - 5 - self.textOffset]

                if inkDraw.useLatex:
                    commuteText = '$' + commuteText + '$'

                inkDraw.text.latex(self, group, commuteText, pos_text, textColor=color, fontSize=self.fontSize * 0.8, refPoint='tc',
                                   preambleFile=self.preambleFile)

            if isPushButton:  # push-button
                lineStyle = inkDraw.lineStyle.set(lineWidth=0.6, lineColor=color, markerEnd=arrowEnd, strokeDashArray='1,1.5')
                inkDraw.line.relCoords(group, [[0, 14]], [position[0] + 20, position[1] - 8], lineStyle=lineStyle)

            else:  # throw switch
                if flagOpen:
                    lineStyle = inkDraw.lineStyle.set(lineWidth=0.6, lineColor=color, markerEnd=arrowEnd, strokeDashArray='1,1.5')
                else:
                    lineStyle = inkDraw.lineStyle.set(lineWidth=0.6, lineColor=color, markerStart=arrowStart, strokeDashArray='1,1.5')
                inkDraw.arc.startEndRadius(group, [-4, -10], [3, 1], 10, [position[0] + 24, position[1]], lineStyle=lineStyle, flagRightOf=False)

        if isPushButton:  # push-button
            pos_text = [position[0] + 28, position[1] - 6 - self.textOffset]
        else:  # throw switch
            if drawCommuteArrow:
                pos_text = [position[0] + 28, position[1] - 8 - self.textOffset]
            else:
                if nPoles > 1:
                    pos_text = [position[0] + 28, position[1] - 6 - self.textOffset]
                else:
                    pos_text = [position[0] + 23, position[1] - 6 - self.textOffset]
        if value:
            if inkDraw.useLatex:
                value = '$' + value + '$'

            inkDraw.text.latex(self, group, value, pos_text, fontSize=self.fontSize, refPoint='bl', preambleFile=self.preambleFile)

        # multiple poles
        if nPoles > 1:
            spacingY = -25
            for i in range(nPoles - 1):
                self.copyElement(elem, group, distance=[0, spacingY * (i + 1)])
            lineStyle = inkDraw.lineStyle.set(lineWidth=0.6, lineColor=colorBlack, strokeDashArray='1.5,1.5')

            if isPushButton:  # push-button
                if flagOpen:
                    inkDraw.line.relCoords(elem, [[0, spacingY * (nPoles - 1)]], [position[0] + 25, position[1] - 7], lineStyle=lineStyle)
                else:
                    inkDraw.line.relCoords(elem, [[0, spacingY * (nPoles - 1)]], [position[0] + 25, position[1] + 2], lineStyle=lineStyle)
            else:  # throw switch
                if flagOpen:
                    inkDraw.line.relCoords(elem, [[0, spacingY * (nPoles - 1)]], [position[0] + 25, position[1] - 4], lineStyle=lineStyle)
                else:
                    inkDraw.line.relCoords(elem, [[0, spacingY * (nPoles - 1)]], [position[0] + 25, position[1] - 1], lineStyle=lineStyle)

        if angleDeg != 0:
            self.rotateElement(group, position, angleDeg)

        if flagVolt:
            if convention == 'passive':
                self.drawVoltArrow(group, [position[0] + 25, position[1] + 7], name=voltName, color=self.voltageColor, angleDeg=angleDeg,
                                   invertArrows=not invertArrows)
            if convention == 'active':
                self.drawVoltArrow(group, [position[0] + 25, position[1] + 7], name=voltName, color=self.voltageColor, angleDeg=angleDeg,
                                   invertArrows=invertArrows)

        if flagCurr:
            self.drawCurrArrow(group, [position[0] + 40, position[1] - 5], name=currName, color=self.currentColor, angleDeg=angleDeg,
                               invertArrows=invertArrows)

        return group

    # ---------------------------------------------
    def drawNPNT(self, parent, position=[0, 0], value='S', label='Switch', angleDeg=0, connection=1, nPoles=1, nThrows=1, drawCommuteArrow=False,
                 commuteOrientation='ccw', commuteText='', flagVolt=True, voltName='v', flagCurr=True, currName='i', invertArrows=False,
                 convention='passive'):
        """ draws a switch with two terminals only

        parent: parent object
        position: position [x,y]
        value: string with resistor value. (default 'S')
        label: label of the object (it can be repeated)
        angleDeg: rotation angle in degrees counter-clockwise (default 0)
        connection: switch connection position (default:1)  0: OPEN
        drawCommuteArrow: draw comuting arrow (default: False)
        commuteOrientation: orientation of the commutation arrow, 'cw', 'ccw' (default)
        commuteText: string with comuting info
        flagVolt: indicates whether the voltage arrow must be drawn (default: true)
        voltName: voltage drop name (default: v)
        flagCurr: indicates whether the current arrow must be drawn (default: true)
        currName: current drop name (default: i)
        invertArrows: invert V/I arrow directions (default: False)
        convention: passive/active sign convention. available types: 'passive' (default) , 'active'
        """

        group = self.createGroup(parent, label)
        elem = self.createGroup(group, label)
        color = inkDraw.color.defined('red')
        colorBlack = inkDraw.color.defined('black')
        colorWhite = inkDraw.color.defined('white')
        lineStyleSign = inkDraw.lineStyle.set(lineWidth=0.7, lineColor=colorBlack, fillColor=colorWhite)
        [arrowStart, arrowEnd] = inkDraw.marker.createArrow1Marker(self, 'arrowSwitch', RenameMode=0, scale=0.25, strokeColor=color, fillColor=color)

        # pole
        inkDraw.line.relCoords(elem, [[15, 0]], position)

        # throw
        if nThrows < 3:
            spacingThrowY = 20
        else:
            spacingThrowY = 10

        Y_positions = [(i - (nThrows - 1) / float(2)) * spacingThrowY for i in range(nThrows)]

        # connection position
        conn = min(connection, nThrows)
        if conn > 0:
            inkDraw.line.relCoords(elem, [[15, Y_positions[conn - 1]]], [position[0] + 15, position[1]])
        else:
            inkDraw.line.relCoords(elem, [[7.5, Y_positions[0]]], [position[0] + 15, position[1]])

        for i in range(nThrows):
            inkDraw.line.relCoords(elem, [[-10, 0], [-10, 0]], [position[0] + 50, position[1] + Y_positions[i]])
            inkDraw.circle.centerRadius(elem, [position[0] + 30, position[1] + Y_positions[i]], 1.2, offset=[0, 0], lineStyle=lineStyleSign)
            inkDraw.text.latex(self, elem, chr(ord('@') + i + 1), [position[0] + 30, position[1] + Y_positions[i] - self.fontSize * 0.4],
                               fontSize=self.fontSize * 0.5, refPoint='bc', preambleFile=self.preambleFile)

        inkDraw.circle.centerRadius(elem, [position[0] + 15, position[1]], 1.2, offset=[0, 0], lineStyle=lineStyleSign)

        # commute arrow
        if drawCommuteArrow:
            if commuteText:
                pos_text = [position[0] + 12, position[1] - 5 - self.textOffset]

                if inkDraw.useLatex:
                    commuteText = '$' + commuteText + '$'

                inkDraw.text.latex(self, group, commuteText, pos_text, textColor=color, fontSize=self.fontSize * 0.8, refPoint='tc',
                                   preambleFile=self.preambleFile)

            if commuteOrientation == 'cw':
                lineStyle = inkDraw.lineStyle.set(lineWidth=0.6, lineColor=color, markerEnd=arrowEnd, strokeDashArray='1,1.5')
            else:
                lineStyle = inkDraw.lineStyle.set(lineWidth=0.6, lineColor=color, markerStart=arrowStart, strokeDashArray='1,1.5')

            inkDraw.arc.startEndRadius(group, [-4, -9], [-4, 9], 10, [position[0] + 24, position[1]], lineStyle=lineStyle, flagRightOf=False)

        # label
        pos_text = [position[0] + 15, position[1] + Y_positions[0] - self.textOffset]

        if value:
            if inkDraw.useLatex:
                value = '$' + value + '$'

            inkDraw.text.latex(self, group, value, pos_text, fontSize=self.fontSize, refPoint='bl', preambleFile=self.preambleFile)

        # multiples poles

        if nPoles > 1:
            spacingY = -(25 + spacingThrowY * (nThrows - 1))
            for i in range(nPoles - 1):
                self.copyElement(elem, group, distance=[0, spacingY * (i + 1)])
            lineStyle = inkDraw.lineStyle.set(lineWidth=0.6, lineColor=colorBlack, strokeDashArray='1.5,1.5')

            inkDraw.line.relCoords(elem, [[0, spacingY * (nPoles - 1)]], [position[0] + 22.5, position[1] + Y_positions[conn - 1] / 2],
                                   lineStyle=lineStyle)

        if angleDeg != 0:
            self.rotateElement(group, position, angleDeg)

        if flagVolt:
            if convention == 'passive':
                self.drawVoltArrow(group, [position[0] + 25, position[1] + 6 + Y_positions[-1]], name=voltName, color=self.voltageColor,
                                   angleDeg=angleDeg, invertArrows=not invertArrows)
            if convention == 'active':
                self.drawVoltArrow(group, [position[0] + 25, position[1] + 6 + Y_positions[-1]], name=voltName, color=self.voltageColor,
                                   angleDeg=angleDeg, invertArrows=invertArrows)

        if flagCurr:
            self.drawCurrArrowSimple(group, [position[0] + 10, position[1] + 5], name=currName, color=self.currentColor, angleDeg=angleDeg + 180,
                                     invertArrows=invertArrows, size=10.0, invertTextSide=False, extraAngleText=0.0)
        return group
