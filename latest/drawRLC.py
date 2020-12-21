#!/usr/bin/python

import numpy as np

import inkscapeMadeEasy.inkscapeMadeEasy_Base as inkBase
import inkscapeMadeEasy.inkscapeMadeEasy_Draw as inkDraw


class RLC(inkBase.inkscapeMadeEasy):
    def add(self, vector, delta):
        # nector does not need to be numpy array. delta will be converted to numpy array. Numpy can then deal with np.array + list
        return vector + np.array(delta)

    # ---------------------------------------------
    def drawBipoleGeneral(self, parent, position=[0, 0], value='Z', label='Bipole', angleDeg=0, flagVolt=True, voltName='v', flagCurr=True,
                          currName='i', invertArrows=False, convention='passive', wireExtraSize=0):
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
        invertArrows: invert V/I arrow directions (default: False)
        convention: passive/active sign convention. available types: 'passive' (default) , 'active'
        wireExtraSize: additional length added to the terminals. If negative, the length will be reduced. default: 0)
        """

        group = self.createGroup(parent, label)
        elem = self.createGroup(group)

        inkDraw.line.relCoords(elem, [[-(15.5 + wireExtraSize), 0]], self.add(position, [-9.5, 0]))
        inkDraw.line.relCoords(elem, [[19, 0], [0, -6], [-19, 0], [0, 6]], self.add(position, [-9.5, 3]))
        inkDraw.line.relCoords(elem, [[15.5 + wireExtraSize, 0]], self.add(position, [9.5, 0]))

        pos_text = self.add(position, [0, -3 - self.textOffset])
        if inkDraw.useLatex:
            value = '$' + value + '$'

        inkDraw.text.latex(self, group, value, pos_text, fontSize=self.fontSize, refPoint='bc', preambleFile=self.preambleFile)

        if angleDeg != 0:
            self.rotateElement(group, position, angleDeg)

        if flagVolt:
            if convention == 'passive':
                self.drawVoltArrow(group, self.add(position, [0, 5]), name=voltName, color=self.voltageColor, angleDeg=angleDeg,
                                   invertArrows=not invertArrows)
            if convention == 'active':
                self.drawVoltArrow(group, self.add(position, [0, 5]), name=voltName, color=self.voltageColor, angleDeg=angleDeg,
                                   invertArrows=invertArrows)

        if flagCurr:
            self.drawCurrArrow(group, self.add(position, [20 + wireExtraSize, -5]), name=currName, color=self.currentColor, angleDeg=angleDeg,
                               invertArrows=invertArrows)

        return group

    # ---------------------------------------------
    def drawResistor(self, parent, position=[0, 0], value='R', label='Resistor', angleDeg=0, flagVolt=True, voltName='v', flagCurr=True, currName='i',
                     invertArrows=False, convention='passive', wireExtraSize=0):
        """ draws a resistor

        parent: parent object
        position: position [x,y]
        value: string with resistor value. (Default 'R')

        label: label of the object (it can be repeated)
        angleDeg: rotation angle in degrees counter-clockwise (default 0)
        flagVolt: indicates whether the voltage arrow must be drawn (default: true)
        voltName: voltage drop name (default: v)
        flagCurr: indicates whether the current arrow must be drawn (default: true)
        currName: current drop name (default: i)
        invertArrows: invert V/I arrow directions (default: False)
        convention: passive/active sign convention. available types: 'passive' (default) , 'active'
        wireExtraLength: additional lenght added to the terminals. If negative, the length will be reduced. default: 0)
        """

        group = self.createGroup(parent, label)
        elem = self.createGroup(group)

        inkDraw.line.relCoords(elem,
                               [[15.5 + wireExtraSize, 0], [2, 3], [3, -6], [3, 6], [3, -6], [3, 6], [3, -6], [2, 3], [15.5 + wireExtraSize, 0]],
                               self.add(position, [-25 - wireExtraSize, 0]))

        pos_text = self.add(position, [0, -3 - self.textOffset])
        if inkDraw.useLatex:
            value = '$' + value + '$'

        inkDraw.text.latex(self, group, value, pos_text, fontSize=self.fontSize, refPoint='bc', preambleFile=self.preambleFile)

        if angleDeg != 0:
            self.rotateElement(group, position, angleDeg)

        if flagVolt:
            if convention == 'passive':
                self.drawVoltArrow(group, self.add(position, [0, 5]), name=voltName, color=self.voltageColor, angleDeg=angleDeg,
                                   invertArrows=not invertArrows)
            if convention == 'active':
                self.drawVoltArrow(group, self.add(position, [0, 5]), name=voltName, color=self.voltageColor, angleDeg=angleDeg,
                                   invertArrows=invertArrows)

        if flagCurr:
            self.drawCurrArrow(group, self.add(position, [20 + wireExtraSize, -5]), name=currName, color=self.currentColor, angleDeg=angleDeg,
                               invertArrows=invertArrows)

        return group

    # ---------------------------------------------
    def drawPotentiometer(self, parent, position=[0, 0], value='R', label='Potentiometer', angleDeg=0, flagVolt=True, voltName='v', flagCurr=True,
                          currName='i', invertArrows=False, is3T=False, convention='passive', wireExtraSize=0):
        """ draws a potentiometer

        parent: parent object
        position: position [x,y]
        value: string with resistor value. (default 'R')

        label: label of the object (it can be repeated)
        angleDeg: rotation angle in degrees counter-clockwise (default 0)
        flagVolt: indicates whether the voltage arrow must be drawn (default: true)
        voltName: voltage drop name (default: v)
        flagCurr: indicates whether the current arrow must be drawn (default: true)
        currName: current drop name (default: i)
        invertArrows: invert V/I arrow directions (default: False)
        is3T: indicates the drawPotentiometer has 3 terminals (default:false)
        convention: passive/active sign convention. available types: 'passive' (default) , 'active'
        wireExtraSize: additional length added to the terminals. If negative, the length will be reduced. default: 0)
        """

        group = self.createGroup(parent, label)
        elem = self.createGroup(group)

        # build arrow marker
        colorBlack = inkDraw.color.defined('black')
        L_arrow = 2.5
        markerPath = 'M 0,0 l -%f,%f l 0,-%f z' % (L_arrow * 1.2, L_arrow / 2.0, L_arrow)
        renameMode = 0  # 0: do not modify  1: overwrite  2:rename
        markerArrow = inkDraw.marker.createMarker(self, 'BJTArrow', markerPath, RenameMode=0, strokeColor=colorBlack, fillColor=colorBlack,
                                                  lineWidth=0.6, markerTransform='translate (1,0)')
        lineStyleArrow = inkDraw.lineStyle.set(lineWidth=1, lineColor=colorBlack, markerEnd=markerArrow)

        inkDraw.line.relCoords(elem,
                               [[15.5 + wireExtraSize, 0], [2, 3], [3, -6], [3, 6], [3, -6], [3, 6], [3, -6], [2, 3], [15.5 + wireExtraSize, 0]],
                               self.add(position, [-25 - wireExtraSize, 0]))

        # 2-terminal Potentiometer
        if is3T:
            inkDraw.line.relCoords(elem, [[0, -10]], self.add(position, [0, 15]), lineStyle=lineStyleArrow)
            pos_text = self.add(position, [0, -3 - self.textOffset])
        else:
            inkDraw.line.relCoords(elem, [[20, -12]], self.add(position, [-10, 6]), lineStyle=lineStyleArrow)
            pos_text = self.add(position, [0, -6 - self.textOffset])

        if inkDraw.useLatex:
            value = '$' + value + '$'

        inkDraw.text.latex(self, group, value, pos_text, fontSize=self.fontSize, refPoint='bc', preambleFile=self.preambleFile)

        if angleDeg != 0:
            self.rotateElement(group, position, angleDeg)

        if flagVolt:
            if is3T:
                pos = self.add(position, [0, -13])
                invertCurvature = True
            else:
                pos = self.add(position, [0, 8])
                invertCurvature = False

            if convention == 'passive':
                self.drawVoltArrowSimple(group, pos, name=voltName, color=self.voltageColor, angleDeg=0, invertArrows=invertArrows,
                                         invertCurvatureDirection=invertCurvature)

            if convention == 'active':
                self.drawVoltArrowSimple(group, pos, name=voltName, color=self.voltageColor, angleDeg=0, invertArrows=not invertArrows,
                                         invertCurvatureDirection=invertCurvature)

        if flagCurr:
            if is3T:
                pos = self.add(position, [20 + wireExtraSize, -5])
            else:
                pos = self.add(position, [-(20 + wireExtraSize), -5])
            self.drawCurrArrow(group, pos, name=currName, color=self.currentColor, angleDeg=angleDeg, invertArrows=invertArrows)

        return group

    # ---------------------------------------------
    def drawCapacitor(self, parent, position=[0, 0], value='C', label='Capacitor', flagPol=False, angleDeg=0, flagVolt=True, voltName='v',
                      flagCurr=True, currName='i', invertArrows=False, convention='passive', wireExtraSize=0):
        """ draws a capacitor

        parent: parent object
        position: position [x,y]
        value: string with value. (default 'C')
        label: label of the object (it can be repeated)
        flagPol: draw sign for polarized capacitor
        angleDeg: rotation angle in degrees counter-clockwise (default 0)
        flagVolt: indicates whether the voltage arrow must be drawn (default: true)
        voltName: voltage drop name (default: v)
        flagCurr: indicates whether the current arrow must be drawn (default: true)
        currName: current drop name (default: i)
        invertArrows: invert V/I arrow directions (default: False)
        convention: passive/active sign convention. available types: 'passive' (default) , 'active'
        wireExtraSize: additional length added to the terminals. If negative, the length will be reduced. default: 0)
        """

        group = self.createGroup(parent, label)
        elem = self.createGroup(group)

        inkDraw.line.relCoords(elem, [[-(23 + wireExtraSize), 0]], self.add(position, [-2, 0]))
        inkDraw.line.relCoords(elem, [[23 + wireExtraSize, 0]], self.add(position, [2, 0]))
        inkDraw.line.relCoords(elem, [[0, -14]], self.add(position, [-2, 7]))
        inkDraw.line.relCoords(elem, [[0, -14]], self.add(position, [2, 7]))

        pos_text = self.add(position, [0, -8 - self.textOffset])
        if inkDraw.useLatex:
            value = '$' + value + '$'

        inkDraw.text.latex(self, group, value, pos_text, fontSize=self.fontSize, refPoint='bc', preambleFile=self.preambleFile)

        if flagPol:
            lineStyleSign = inkDraw.lineStyle.setSimpleBlack(lineWidth=0.6)
            inkDraw.line.relCoords(elem, [[-2, 0]], self.add(position, [6, -5]), lineStyle=lineStyleSign)
            inkDraw.line.relCoords(elem, [[0, 2]], self.add(position, [5, -6]), lineStyle=lineStyleSign)

        if angleDeg != 0:
            self.rotateElement(group, position, angleDeg)

        if flagVolt:
            if convention == 'passive':
                self.drawVoltArrow(group, self.add(position, [0, 9]), name=voltName, color=self.voltageColor, angleDeg=angleDeg,
                                   invertArrows=not invertArrows)
            if convention == 'active':
                self.drawVoltArrow(group, self.add(position, [0, 9]), name=voltName, color=self.voltageColor, angleDeg=angleDeg,
                                   invertArrows=invertArrows)

        if flagCurr:
            self.drawCurrArrow(group, self.add(position, [20 + wireExtraSize, -5]), name=currName, color=self.currentColor, angleDeg=angleDeg,
                               invertArrows=invertArrows)

        return group

    # ---------------------------------------------
    def drawInductor(self, parent, position=[0, 0], value='L', label='Inductro', angleDeg=0, flagVolt=True, voltName='v', flagCurr=True, currName='i',
                     invertArrows=False, convention='passive', wireExtraSize=0):
        """ draws an inductor

        parent: parent object
        position: position [x,y]
        value: string with value. (Default 'L')

        label: label of the object (it can be repeated)
        angleDeg: rotation angle in degrees counter-clockwise (default 0)
        flagVolt: indicates whether the voltage arrow must be drawn (default: true)
        voltName: voltage drop name (default: v)
        flagCurr: indicates whether the current arrow must be drawn (default: true)
        currName: current drop name (default: i)
        invertArrows: invert V/I arrow directions (default: False)
        convention: passive/active sign convention. available types: 'passive' (default) , 'active'
        wireExtraSize: additional length added to the terminals. If negative, the length will be reduced. default: 0)
        """

        group = self.createGroup(parent, label)
        elem = self.createGroup(group)

        inkDraw.line.relCoords(elem, [[-(13 + wireExtraSize), 0]], self.add(position, [-12, 0]))
        inkDraw.line.relCoords(elem, [[13 + wireExtraSize, 0]], self.add(position, [12, 0]))

        inkDraw.arc.centerAngStartAngEnd(elem, self.add(position, [-9, 0]), 3.0, 0.0, 180.0, [0, 0], largeArc=False)
        inkDraw.arc.centerAngStartAngEnd(elem, self.add(position, [-3, 0]), 3.0, 0.0, 180.0, [0, 0], largeArc=False)
        inkDraw.arc.centerAngStartAngEnd(elem, self.add(position, [3, 0]), 3.0, 0.0, 180.0, [0, 0], largeArc=False)
        inkDraw.arc.centerAngStartAngEnd(elem, self.add(position, [9, 0]), 3.0, 0.0, 180.0, [0, 0], largeArc=False)

        pos_text = self.add(position, [0, -self.textOffset])
        if inkDraw.useLatex:
            value = '$' + value + '$'

        inkDraw.text.latex(self, group, value, pos_text, fontSize=self.fontSize, refPoint='bc', preambleFile=self.preambleFile)

        if angleDeg != 0:
            self.rotateElement(group, position, angleDeg)

        if flagVolt:
            if convention == 'passive':
                self.drawVoltArrow(group, self.add(position, [0, 5]), name=voltName, color=self.voltageColor, angleDeg=angleDeg,
                                   invertArrows=not invertArrows)
            if convention == 'active':
                self.drawVoltArrow(group, self.add(position, [0, 5]), name=voltName, color=self.voltageColor, angleDeg=angleDeg,
                                   invertArrows=invertArrows)

        if flagCurr:
            self.drawCurrArrow(group, self.add(position, [20 + wireExtraSize, -5]), name=currName, color=self.currentColor, angleDeg=angleDeg,
                               invertArrows=invertArrows)

        return group
