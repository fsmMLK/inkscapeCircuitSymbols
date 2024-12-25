#!/usr/bin/python

import inkscapeMadeEasy.inkscapeMadeEasy_Base as inkBase
import inkscapeMadeEasy.inkscapeMadeEasy_Draw as inkDraw


class diode(inkBase.inkscapeMadeEasy):
    def add(self, vector, delta):
        # nector does not need to be numpy array. delta will be converted to numpy array. Numpy can then deal with np.array + list
        return vector + np.array(delta)

    # ---------------------------------------------
    def drawDiode(self, parent, position=[0, 0], value='D', label='diode', angleDeg=0, flagVolt=True, voltName='v', flagCurr=True, currName='i',
                  invertArrows=False, flagType='regular', mirror=False, convention='passive', wireExtraSize=0):
        """ draws a diode

        parent: parent object
        position: position [x,y]
        value: string with diode label

        label: label of the object (it can be repeated)
        angleDeg: rotation angle in degrees counter-clockwise (default 0)
        flagVolt: indicates whether the voltage arrow must be drawn (default: true)
        voltName: voltage drop name (default: v)
        flagCurr: indicates whether the current arrow must be drawn (default: true)
        currName: current drop name (default: i)]
        flagType: type of element: available types:  'regular', 'LED', 'photoDiode', 'zener', 'schottky','tunnel','varicap' (default: regular)
        mirror: mirror diode (default: False)
        convention: Voltage/currente convention. 'active' or 'passive'
        wireExtraSize: additional length added to the terminals. If negative, the length will be reduced. default: 0)
        """

        group = self.createGroup(parent, label)
        elem = self.createGroup(group)

        if mirror:
            if flagType == 'varicap':
                inkDraw.line.relCoords(elem, [[-(16 + wireExtraSize), 0]], self.add(position, [-9, 0]))
            else:
                inkDraw.line.relCoords(elem, [[-(19 + wireExtraSize), 0]], self.add(position, [-6, 0]))

            inkDraw.line.relCoords(elem, [[12, 6], [0, -12], [-12, 6]], self.add(position, [-6, 0]))
            inkDraw.line.relCoords(elem, [[19 + wireExtraSize, 0]], self.add(position, [6, 0]))

            if flagType in ['regular', 'LED', 'photoDiode']:
                inkDraw.line.relCoords(elem, [[0, 12]], self.add(position, [-6, -6]))

            if flagType == 'zener':
                inkDraw.line.relCoords(elem, [[-2, -2], [0, -10], [-2, -2]], self.add(position, [-6 + 2, 5 + 2]))

            if flagType == 'schottky':
                inkDraw.line.relCoords(elem, [[0, 2], [3, 0], [0, -12], [3, 0], [0, 2]], self.add(position, [-6 - 3, 6 - 2]))

            if flagType == 'tunnel':
                inkDraw.line.relCoords(elem, [[-3, 0], [0, -12], [3, 0]], self.add(position, [-6 + 3, 6]))

            if flagType == 'varicap':
                inkDraw.line.relCoords(elem, [[0, 12]], self.add(position, [-6, -6]))
                inkDraw.line.relCoords(elem, [[0, 12]], self.add(position, [-9, -6]))

        else:
            if flagType == 'varicap':
                inkDraw.line.relCoords(elem, [[16 + wireExtraSize, 0]], self.add(position, [6 + 3, 0]))
            else:
                inkDraw.line.relCoords(elem, [[19 + wireExtraSize, 0]], self.add(position, [6, 0]))

            inkDraw.line.relCoords(elem, [[-(19 + wireExtraSize), 0]], self.add(position, [-6, 0]))
            inkDraw.line.relCoords(elem, [[-12, 6], [0, -12], [12, 6]], self.add(position, [6, 0]))

            if flagType in ['regular', 'LED', 'photoDiode']:
                inkDraw.line.relCoords(elem, [[0, 12]], self.add(position, [6, -6]))

            if flagType == 'zener':
                inkDraw.line.relCoords(elem, [[-2, -2], [0, -10], [-2, -2]], self.add(position, [6 + 2, 5 + 2]))

            if flagType == 'schottky':
                inkDraw.line.relCoords(elem, [[0, 2], [3, 0], [0, -12], [3, 0], [0, 2]], self.add(position, [6 - 3, 6 - 2]))

            if flagType == 'tunnel':
                inkDraw.line.relCoords(elem, [[3, 0], [0, -12], [-3, 0]], self.add(position, [6 - 3, 6]))

            if flagType == 'varicap':
                inkDraw.line.relCoords(elem, [[0, 12]], self.add(position, [6, -6]))
                inkDraw.line.relCoords(elem, [[0, 12]], self.add(position, [9, -6]))

        if value.strip() != "":

            if flagType == 'LED':
                pos_text = self.add(position, [0, -13 - self.textOffset])
            if flagType == 'photoDiode':
                pos_text = self.add(position, [0, -13 - self.textOffset])
            if flagType in ['regular', 'zener', 'schottky', 'tunnel', 'varicap']:
                pos_text = self.add(position, [0, -6 - self.textOffset])

            if inkDraw.useLatex:
                value = '$' + value + '$'

            inkDraw.text.latex(self, group, value, pos_text, fontSize=self.fontSize, refPoint='bc', preambleFile=self.preambleFile)

        if angleDeg != 0:
            self.rotateElement(group, position, angleDeg)

        if flagVolt:
            if convention == 'passive':
                self.drawVoltArrow(group, self.add(position, [0, 7]), name=voltName, color=self.voltageColor, angleDeg=angleDeg,
                                   invertArrows=not (invertArrows != mirror))
            if convention == 'active':
                self.drawVoltArrow(group, self.add(position, [0, 7]), name=voltName, color=self.voltageColor, angleDeg=angleDeg,
                                   invertArrows=(invertArrows != mirror))

        if flagCurr:
            self.drawCurrArrow(group, self.add(position, [20 + wireExtraSize, -5]), name=currName, color=self.currentColor, angleDeg=angleDeg,
                               invertArrows=(invertArrows != mirror))

        if flagType == 'LED':
            arrow = self.createGroup(elem)
            inkDraw.line.relCoords(arrow, [[7, 0]], position)
            inkDraw.line.relCoords(arrow, [[1.5, -1.5], [-1.5, -1.5]], self.add(position, [5.5, 1.5]))
            self.rotateElement(arrow, position, 60)
            self.moveElement(arrow, [-3, -8])
            self.copyElement(arrow, elem, distance=[5, 2])

        if flagType == 'photoDiode':
            arrow = self.createGroup(elem)
            inkDraw.line.relCoords(arrow, [[7, 0]], position)
            inkDraw.line.relCoords(arrow, [[1.5, -1.5], [-1.5, -1.5]], self.add(position, [5.5, 1.5]))
            self.rotateElement(arrow, position, -120)
            self.moveElement(arrow, [0, -14])
            self.copyElement(arrow, elem, distance=[5, 2])

        return group
