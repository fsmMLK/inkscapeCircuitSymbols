#!/usr/bin/python

import inkscapeMadeEasy_Base as inkBase
import inkscapeMadeEasy_Draw as inkDraw


class diode(inkBase.inkscapeMadeEasy):

    # ---------------------------------------------
    def drawDiode(self, parent, position=[0, 0], value='D', label='diode', angleDeg=0, flagVolt=True, voltName='v',
                  flagCurr=True, currName='i', invertArrows=False, flagType='regular', mirror=False,
                  convention='passive'):
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
        flagType: type of element: available types:  'regular', 'LED', 'photoDiode', 'zener', 'schottky','tunnel','varicap' (default: regular)
        mirror: mirror diode (default: False)
        convention: Voltage/currente convention. 'active' or 'passive'
        """

        group = self.createGroup(parent, label)
        elem = self.createGroup(group)

        if mirror:
            if flagType == 'varicap':
                inkDraw.line.relCoords(elem, [[16, 0]], position)
            else:
                inkDraw.line.relCoords(elem, [[19, 0]], position)

            inkDraw.line.relCoords(elem, [[12, 6], [0, -12], [-12, 6]], [position[0] + 19, position[1]])
            inkDraw.line.relCoords(elem, [[19, 0]], [position[0] + 31, position[1]])

            if flagType in ['regular', 'LED', 'photoDiode']:
                inkDraw.line.relCoords(elem, [[0, 12]], [position[0] + 19, position[1] - 6])

            if flagType == 'zener':
                inkDraw.line.relCoords(elem, [[-2, -2], [0, -10], [-2, -2]],
                                       [position[0] + 19 + 2, position[1] + 5 + 2])

            if flagType == 'schottky':
                inkDraw.line.relCoords(elem, [[0, 2], [3, 0], [0, -12], [3, 0], [0, 2]],
                                       [position[0] + 19 - 3, position[1] + 6 - 2])

            if flagType == 'tunnel':
                if mirror:
                    inkDraw.line.relCoords(elem, [[-3, 0], [0, -12], [3, 0]], [position[0] + 19 + 3, position[1] + 6])
                else:
                    inkDraw.line.relCoords(elem, [[3, 0], [0, -12], [-3, 0]], [position[0] + 19 - 3, position[1] + 6])

            if flagType == 'varicap':
                inkDraw.line.relCoords(elem, [[0, 12]], [position[0] + 19, position[1] - 6])
                if mirror:
                    inkDraw.line.relCoords(elem, [[0, 12]], [position[0] + 16, position[1] - 6])
                else:
                    inkDraw.line.relCoords(elem, [[0, 12]], [position[0] + 22, position[1] - 6])

        else:
            inkDraw.line.relCoords(elem, [[19, 0]], position)
            inkDraw.line.relCoords(elem, [[-12, 6], [0, -12], [12, 6]], [position[0] + 31, position[1]])
            if flagType == 'varicap':
                inkDraw.line.relCoords(elem, [[16, 0]], [position[0] + 31 + 3, position[1]])
            else:
                inkDraw.line.relCoords(elem, [[19, 0]], [position[0] + 31, position[1]])

            if flagType in ['regular', 'LED', 'photoDiode']:
                inkDraw.line.relCoords(elem, [[0, 12]], [position[0] + 31, position[1] - 6])

            if flagType == 'zener':
                inkDraw.line.relCoords(elem, [[-2, -2], [0, -10], [-2, -2]],
                                       [position[0] + 31 + 2, position[1] + 5 + 2])

            if flagType == 'schottky':
                inkDraw.line.relCoords(elem, [[0, 2], [3, 0], [0, -12], [3, 0], [0, 2]],
                                       [position[0] + 31 - 3, position[1] + 6 - 2])

            if flagType == 'tunnel':
                inkDraw.line.relCoords(elem, [[3, 0], [0, -12], [-3, 0]], [position[0] + 31 - 3, position[1] + 6])

            if flagType == 'varicap':
                inkDraw.line.relCoords(elem, [[0, 12]], [position[0] + 31, position[1] - 6])
                inkDraw.line.relCoords(elem, [[0, 12]], [position[0] + 34, position[1] - 6])

        if value is not None:

            if flagType == 'LED':
                pos_text = [position[0] + 25, position[1] - 13 - self.textOffset]
            if flagType == 'photoDiode':
                pos_text = [position[0] + 25, position[1] - 13 - self.textOffset]
            if flagType in ['regular', 'zener', 'schottky', 'tunnel', 'varicap']:
                pos_text = [position[0] + 25, position[1] - 6 - self.textOffset]

            if inkDraw.useLatex:
                value = '$' + value + '$'

            inkDraw.text.latex(self, group, value, pos_text, fontSize=self.fontSize, refPoint='bc',
                               preambleFile=self.preambleFile)

        if angleDeg != 0:
            self.rotateElement(group, position, angleDeg)

        if flagVolt:
            if convention == 'passive':
                self.drawVoltArrow(group, [position[0] + 25, position[1] + 7], name=voltName, color=self.voltageColor,
                                   angleDeg=angleDeg, invertArrows=not (invertArrows != mirror))
            if convention == 'active':
                self.drawVoltArrow(group, [position[0] + 25, position[1] + 7], name=voltName, color=self.voltageColor,
                                   angleDeg=angleDeg, invertArrows= (invertArrows != mirror))



        if flagCurr:
            self.drawCurrArrow(group, [position[0] + 40, position[1] - 5], name=currName, color=self.currentColor,
                               angleDeg=angleDeg, invertArrows=(invertArrows != mirror))

        if flagType == 'LED':
            arrow = self.createGroup(elem)
            inkDraw.line.relCoords(arrow, [[7, 0]], position)
            inkDraw.line.relCoords(arrow, [[1.5, -1.5], [-1.5, -1.5]], [position[0] + 5.5, position[1] + 1.5])
            self.rotateElement(arrow, position, 60)
            self.moveElement(arrow, [22, -8])
            arrow = self.createGroup(elem)
            inkDraw.line.relCoords(arrow, [[7, 0]], position)
            inkDraw.line.relCoords(arrow, [[1.5, -1.5], [-1.5, -1.5]], [position[0] + 5.5, position[1] + 1.5])
            self.rotateElement(arrow, position, 60)
            self.moveElement(arrow, [27, -6])

        if flagType == 'photoDiode':
            arrow = self.createGroup(elem)
            inkDraw.line.relCoords(arrow, [[7, 0]], position)
            inkDraw.line.relCoords(arrow, [[1.5, -1.5], [-1.5, -1.5]], [position[0] + 5.5, position[1] + 1.5])
            self.rotateElement(arrow, position, -120)
            self.moveElement(arrow, [25, -14])
            arrow = self.createGroup(elem)
            inkDraw.line.relCoords(arrow, [[7, 0]], position)
            inkDraw.line.relCoords(arrow, [[1.5, -1.5], [-1.5, -1.5]], [position[0] + 5.5, position[1] + 1.5])
            self.rotateElement(arrow, position, -120)
            self.moveElement(arrow, [30, -12])

        return group
