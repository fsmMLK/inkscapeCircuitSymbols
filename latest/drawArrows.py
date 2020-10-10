#!/usr/bin/python

import math

import inkscapeMadeEasy.inkscapeMadeEasy_Base as inkBase
import inkscapeMadeEasy.inkscapeMadeEasy_Draw as inkDraw


class arrow(inkBase.inkscapeMadeEasy):

    # ---------------------------------------------
    def drawVoltArrowSimple(self, parent, position, label='arrowV', name='v', color=inkDraw.color.defined('black'),
                            angleDeg=0, invertArrows=False, size=20.0, invertCurvatureDirection=False,
                            extraAngleText=0.0):

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
            arrow_elem = self.drawVoltArrow(parent, position, label, name, color, angleDeg + 180, invertArrows, size,
                                            extraAngleText)
            self.rotateElement(arrow_elem, position, angleDeg + 180)
        else:
            arrow_elem = self.drawVoltArrow(parent, position, label, name, color, angleDeg, not invertArrows, size,
                                            extraAngleText)
            self.rotateElement(arrow_elem, position, angleDeg)

    # ---------------------------------------------

    def drawVoltArrow(self, parent, position, label='name', name='v', color=inkDraw.color.defined('black'), angleDeg=0,
                      invertArrows=False, size=20.0, extraAngleText=0.0):
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

        group = self.createGroup(parent, label)

        scale = size / 20.0  # the default size was 20 height

        renameMode = 0  # 0: do not modify  1: overwrite  2:rename
        # make linestyle
        [arrowStartVolt, arrowEndVolt] = inkDraw.marker.createArrow1Marker(self, 'arrowVoltage', RenameMode=renameMode,
                                                                           scale=0.25, strokeColor=color,
                                                                           fillColor=color)

        if invertArrows:
            lineStyle = inkDraw.lineStyle.set(lineColor=color, markerStart=arrowStartVolt)
        else:
            lineStyle = inkDraw.lineStyle.set(lineColor=color, markerEnd=arrowEndVolt)

        radius = 30.0 * scale
        h = 10.0 * scale
        halfTheta = math.asin(h / radius)
        inkDraw.arc.startEndRadius(group, [h, 0], [-h, 0], radius, position, lineStyle=lineStyle, flagRightOf=False)

        # get appropriate refPoint based on the angle
        theta = angleDeg + extraAngleText
        while theta < 0:
            theta = theta + 360
        while theta > 360:
            theta = theta - 360

        if theta <= 20:
            justif = 'tc'
        else:
            if theta <= 60:
                justif = 'tl'
            else:
                if theta <= 100:
                    justif = 'cl'
                else:
                    if theta <= 150:
                        justif = 'bl'
                    else:
                        if theta <= 200:
                            justif = 'bc'
                        else:
                            if theta <= 250:
                                justif = 'br'
                            else:
                                if theta <= 290:
                                    justif = 'cr'
                                else:
                                    if theta <= 340:
                                        justif = 'tr'
                                    else:
                                        justif = 'tc'

        centerY = -radius * math.cos(halfTheta)
        posY = centerY + radius

        if not name == '':
            if inkDraw.useLatex:
                name = '$' + name + '$'
                dist = 4.0
            else:
                dist = 3.0
            inkDraw.text.latex(self, group, name, [position[0], position[1] + posY + dist], fontSize=self.fontSize,
                               refPoint=justif, textColor=color, angleDeg=-theta, preambleFile=self.preambleFile)

        return group

    # ---------------------------------------------

    def drawCurrArrowSimple(self, parent, position, label='arrowI', name='', color=inkDraw.color.defined('black'),
                            angleDeg=0, invertArrows=False, size=20.0, invertTextSide=False, extraAngleText=0.0):

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

        # control signal
        if invertTextSide:
            temp1 = self.drawCurrArrow(parent, position, label, name, color=self.currentColor, angleDeg=angleDeg + 180,
                                       invertArrows=invertArrows, size=size, extraAngleText=extraAngleText)
            self.rotateElement(temp1, position, angleDeg + 180)
        else:
            temp1 = self.drawCurrArrow(parent, position, label, name, color=self.currentColor, angleDeg=angleDeg,
                                       invertArrows=not invertArrows, size=size, extraAngleText=extraAngleText)
            self.rotateElement(temp1, position, angleDeg)

    # ---------------------------------------------
    def drawCurrArrow(self, parent, position, label='name', name='i', color=inkDraw.color.defined('black'), angleDeg=0,
                      invertArrows=False, size=10.0, extraAngleText=0.0):
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
        scale = size / 10.0
        group = self.createGroup(parent, label)
        renameMode = 0  # 0: do not modify  1: overwrite  2:rename

        # make linestyle
        [arrowStartCurr, arrowEndCurr] = inkDraw.marker.createArrow1Marker(self, 'arrowCurrent', RenameMode=renameMode,
                                                                           scale=0.25, strokeColor=color,
                                                                           fillColor=color)
        lineStyle = inkDraw.lineStyle.set(lineColor=color, markerEnd=arrowEndCurr)

        if invertArrows:
            inkDraw.line.relCoords(group, [[10 * scale, 0]], [position[0] - 5 * scale, position[1]], label='none',
                                   lineStyle=lineStyle)
        else:
            inkDraw.line.relCoords(group, [[-10 * scale, 0]], [position[0] + 5 * scale, position[1]], label='none',
                                   lineStyle=lineStyle)

        # get appropriate refPoint based on the angle
        theta = angleDeg + extraAngleText
        while theta < 0:
            theta = theta + 360
        while theta > 360:
            theta = theta - 360

        if theta <= 20:
            justif = 'bc'
        else:
            if theta <= 60:
                justif = 'br'
            else:
                if theta <= 100:
                    justif = 'cr'
                else:
                    if theta <= 150:
                        justif = 'tr'
                    else:
                        if theta <= 200:
                            justif = 'tc'
                        else:
                            if theta <= 250:
                                justif = 'tl'
                            else:
                                if theta <= 290:
                                    justif = 'cl'
                                else:
                                    justif = 'bl'

        if inkDraw.useLatex:
            name = '$' + name + '$'

        inkDraw.text.latex(self, group, name, [position[0], position[1] - self.textOffset * 0.8],
                           fontSize=self.fontSize, refPoint=justif, textColor=color, angleDeg=-theta,
                           preambleFile=self.preambleFile)

        return group
