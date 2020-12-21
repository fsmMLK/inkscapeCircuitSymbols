#!/usr/bin/python

import inkscapeMadeEasy.inkscapeMadeEasy_Base as inkBase
import inkscapeMadeEasy.inkscapeMadeEasy_Draw as inkDraw


class source(inkBase.inkscapeMadeEasy):
    def add(self, vector, delta):
        # nector does not need to be numpy array. delta will be converted to numpy array. Numpy can then deal with np.array + list
        return vector + np.array(delta)

    def drawSigns(self, group, positionPos=None, positionNeg=None):
        # draw + and - signs
        # positive Sign
        lineStyleSign = inkDraw.lineStyle.setSimpleBlack(lineWidth=0.6)
        if positionPos is not None:
            inkDraw.line.relCoords(group, [[2, 0]], self.add(positionPos, [-1, 0]), lineStyle=lineStyleSign)
            inkDraw.line.relCoords(group, [[0, 2]], self.add(positionPos, [0, -1]), lineStyle=lineStyleSign)
        # negative Sign
        if positionNeg is not None:
            inkDraw.line.relCoords(group, [[0, 2]], self.add(positionNeg, [0, -1]), lineStyle=lineStyleSign)

    # ---------------------------------------------
    def drawSourceV(self, parent, position=[0, 0], value='v(t)', label='Source', angleDeg=0, flagVolt=True, flagCurr=True, currName='i',
                    invertArrows=False, mirror=False, convention='active', wireExtraSize=0):
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
        convention: passive/active sign convention. available types: 'passive', 'active' (default)
        wireExtraSize: additional length added to the terminals. If negative, the length will be reduced. default: 0)
        """

        group = self.createGroup(parent, label)
        elem = self.createGroup(group, label)

        inkDraw.line.relCoords(elem, [[-(18 + wireExtraSize), 0]], self.add(position, [-7, 0]))
        inkDraw.line.relCoords(elem, [[18 + wireExtraSize, 0]], self.add(position, [7, 0]))
        inkDraw.circle.centerRadius(elem, [0, 0], 7.0, offset=position, label='circle')

        # signs
        if mirror:
            self.drawSigns(elem, positionPos=self.add(position, [-4, 0]), positionNeg=self.add(position, [4, 0]))
        else:
            self.drawSigns(elem, positionPos=self.add(position, [4, 0]), positionNeg=self.add(position, [-4, 0]))

        pos_text = self.add(position, [0, -8 - self.textOffset])
        if inkDraw.useLatex:
            value = '$' + value + '$'

        inkDraw.text.latex(self, group, value, pos_text, fontSize=self.fontSize, refPoint='bc', preambleFile=self.preambleFile)

        if angleDeg != 0:
            self.rotateElement(group, position, angleDeg)

        inv_volt = (invertArrows == mirror)

        if flagVolt:
            if invertArrows:
                if inkDraw.useLatex:
                    if value[1] == '-':
                        value = value[0] + value[2:]
                    else:
                        value = value[0] + '-' + value[1:]
                else:
                    if value[0] == '-':
                        value = value[1:]
                    else:
                        value = '-' + value
            self.drawVoltArrow(group, self.add(position, [0, 8]), name=value, color=self.voltageColor, angleDeg=angleDeg, invertArrows=inv_volt)

        if flagCurr:
            if convention == 'active':
                self.drawCurrArrow(group, self.add(position, [20 + wireExtraSize, -5]), name=currName, color=self.currentColor, angleDeg=angleDeg,
                                   invertArrows=inv_volt)
            if convention == 'passive':
                self.drawCurrArrow(group, self.add(position, [20 + wireExtraSize, -5]), name=currName, color=self.currentColor, angleDeg=angleDeg,
                                   invertArrows=not inv_volt)

        return group

    # ---------------------------------------------
    def drawSourceVSinusoidal(self, parent, position=[0, 0], value='v(t)', label='Source', angleDeg=0, flagVolt=True, flagCurr=True, currName='i',
                              invertArrows=False, mirror=False, convention='active', wireExtraSize=0):
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
        convention: passive/active sign convention. available types: 'passive', 'active' (default)
        wireExtraSize: additional length added to the terminals. If negative, the length will be reduced. default: 0)
        """

        group = self.createGroup(parent, label)
        elem = self.createGroup(group, label)

        inkDraw.line.relCoords(elem, [[-(18 + wireExtraSize), 0]], self.add(position, [-7, 0]))
        inkDraw.line.relCoords(elem, [[18 + wireExtraSize, 0]], self.add(position, [7, 0]))
        inkDraw.circle.centerRadius(elem, [0, 0], 7.0, offset=position, label='circle')

        # signs
        sine = self.createGroup(elem)
        lineStyleSign = inkDraw.lineStyle.setSimpleBlack(lineWidth=0.6)

        inkDraw.arc.startEndRadius(sine, self.add(position, [-5, 0]), position, 2.6, [0, 0], lineStyle=lineStyleSign, flagRightOf=True,
                                   largeArc=False)
        inkDraw.arc.startEndRadius(sine, self.add(position, [5, 0]), position, 2.6, [0, 0], lineStyle=lineStyleSign, flagRightOf=True, largeArc=False)
        self.rotateElement(sine, position, -angleDeg)

        if mirror:
            self.drawSigns(elem, positionPos=self.add(position, [-10, -4]), positionNeg=self.add(position, [10, -4]))
        else:
            self.drawSigns(elem, positionPos=self.add(position, [10, -4]), positionNeg=self.add(position, [-10, -4]))

        pos_text = self.add(position, [0, -8 - self.textOffset])
        if inkDraw.useLatex:
            value = '$' + value + '$'

        inkDraw.text.latex(self, group, value, pos_text, fontSize=self.fontSize, refPoint='bc', preambleFile=self.preambleFile)

        if angleDeg != 0:
            self.rotateElement(group, position, angleDeg)

        inv_volt = (invertArrows == mirror)

        if flagVolt:
            if invertArrows:
                if inkDraw.useLatex:
                    if value[1] == '-':
                        value = value[0] + value[2:]
                    else:
                        value = value[0] + '-' + value[1:]
                else:
                    if value[0] == '-':
                        value = value[1:]
                    else:
                        value = '-' + value
            self.drawVoltArrow(group, self.add(position, [0, 8]), name=value, color=self.voltageColor, angleDeg=angleDeg, invertArrows=inv_volt)

        if flagCurr:
            if convention == 'active':
                self.drawCurrArrow(group, self.add(position, [20 + wireExtraSize, -5]), name=currName, color=self.currentColor, angleDeg=angleDeg,
                                   invertArrows=inv_volt)
            if convention == 'passive':
                self.drawCurrArrow(group, self.add(position, [20 + wireExtraSize, -5]), name=currName, color=self.currentColor, angleDeg=angleDeg,
                                   invertArrows=not inv_volt)

        return group

    # ---------------------------------------------
    def drawSourceVDC(self, parent, position=[0, 0], value='V', label='Source', angleDeg=0, flagVolt=True, flagCurr=True, currName='i',
                      invertArrows=False, mirror=False, convention='active', wireExtraSize=0):
        """ draws a DC voltage source

        parent: parent object
        position: position [x,y]
        value: string with value.
        label: label of the object (it can be repeated)
        angleDeg: rotation angle in degrees counter-clockwise (default 0)
        flagVolt: indicates whether the voltage arrow must be drawn (default: true)
        flagCurr: indicates whether the current arrow must be drawn (default: true)
        currName: current drop name (default: i)
        mirror: mirror source drawing (default: False)
        convention: passive/active sign convention. available types: 'passive', 'active' (default)
        wireExtraSize: additional length added to the terminals. If negative, the length will be reduced. default: 0)
        """

        group = self.createGroup(parent, label)
        elem = self.createGroup(group, label)

        inkDraw.line.relCoords(elem, [[-(24 + wireExtraSize), 0]], self.add(position, [-1, 0]))
        inkDraw.line.relCoords(elem, [[23 + wireExtraSize, 0]], self.add(position, [2, 0]))

        # draw source
        if mirror:
            self.drawSigns(elem, positionPos=self.add(position, [-4, -4]), positionNeg=self.add(position, [5, -4]))
            inkDraw.line.relCoords(elem, [[0, -6]], self.add(position, [2, 3]))
            inkDraw.line.relCoords(elem, [[0, -14]], self.add(position, [-1, 7]))
        else:
            self.drawSigns(elem, positionPos=self.add(position, [5, -4]), positionNeg=self.add(position, [-4, -4]))
            inkDraw.line.relCoords(elem, [[0, -6]], self.add(position, [-1, 3]))
            inkDraw.line.relCoords(elem, [[0, -14]], self.add(position, [2, 7]))

        pos_text = self.add(position, [0, -8 - self.textOffset])
        if inkDraw.useLatex:
            value = '$' + value + '$'

        inkDraw.text.latex(self, group, value, pos_text, fontSize=self.fontSize, refPoint='bc', preambleFile=self.preambleFile)

        if angleDeg != 0:
            self.rotateElement(group, position, angleDeg)

        inv_volt = (invertArrows == mirror)

        if flagVolt:
            if invertArrows:
                if inkDraw.useLatex:
                    if value[1] == '-':
                        value = value[0] + value[2:]
                    else:
                        value = value[0] + '-' + value[1:]
                else:
                    if value[0] == '-':
                        value = value[1:]
                    else:
                        value = '-' + value
            self.drawVoltArrow(group, self.add(position, [0, 8]), name=value, color=self.voltageColor, angleDeg=angleDeg, invertArrows=inv_volt)

        if flagCurr:
            if convention == 'active':
                self.drawCurrArrow(group, self.add(position, [20 + wireExtraSize, -5]), name=currName, color=self.currentColor, angleDeg=angleDeg,
                                   invertArrows=inv_volt)
            if convention == 'passive':
                self.drawCurrArrow(group, self.add(position, [20 + wireExtraSize, -5]), name=currName, color=self.currentColor, angleDeg=angleDeg,
                                   invertArrows=not inv_volt)

        return group

        # ---------------------------------------------

    def drawSourceVDCbattery(self, parent, position=[0, 0], value='V', label='Source', angleDeg=0, flagVolt=True, flagCurr=True, currName='i',
                             invertArrows=False, mirror=False, convention='active', wireExtraSize=0):
        """ draws a DC battery  source

        parent: parent object
        position: position [x,y]
        value: string with value.
        label: label of the object (it can be repeated)
        angleDeg: rotation angle in degrees counter-clockwise (default 0)
        flagVolt: indicates whether the voltage arrow must be drawn (default: true)
        flagCurr: indicates whether the current arrow must be drawn (default: true)
        currName: current drop name (default: i)
        mirror: mirror source drawing (default: False)
        convention: passive/active sign convention. available types: 'passive', 'active' (default)
        wireExtraSize: additional length added to the terminals. If negative, the length will be reduced. default: 0)
        """

        group = self.createGroup(parent, label)
        elem = self.createGroup(group, label)

        inkDraw.line.relCoords(elem, [[-(18 + wireExtraSize), 0]], self.add(position, [-7, 0]))
        inkDraw.line.relCoords(elem, [[17 + wireExtraSize, 0]], self.add(position, [8, 0]))

        # draw source
        if mirror:
            self.drawSigns(elem, positionPos=self.add(position, [-10, -4]), positionNeg=self.add(position, [11, -4]))
            inkDraw.line.relCoords(elem, [[0, -6]], self.add(position, [-4, 3]))
            inkDraw.line.relCoords(elem, [[0, -14]], self.add(position, [-7, 7]))
            inkDraw.line.relCoords(elem, [[0, -6]], self.add(position, [2, 3]))
            inkDraw.line.relCoords(elem, [[0, -14]], self.add(position, [-1, 7]))
            inkDraw.line.relCoords(elem, [[0, -6]], self.add(position, [8, 3]))
            inkDraw.line.relCoords(elem, [[0, -14]], self.add(position, [5, 7]))
        else:
            self.drawSigns(elem, positionPos=self.add(position, [11, -4]), positionNeg=self.add(position, [-10, -4]))
            inkDraw.line.relCoords(elem, [[0, -14]], self.add(position, [-4, 7]))
            inkDraw.line.relCoords(elem, [[0, -6]], self.add(position, [-7, 3]))
            inkDraw.line.relCoords(elem, [[0, -14]], self.add(position, [2, 7]))
            inkDraw.line.relCoords(elem, [[0, -6]], self.add(position, [-1, 3]))
            inkDraw.line.relCoords(elem, [[0, -14]], self.add(position, [8, 7]))
            inkDraw.line.relCoords(elem, [[0, -6]], self.add(position, [5, 3]))

        pos_text = self.add(position, [0, -8 - self.textOffset])
        if inkDraw.useLatex:
            value = '$' + value + '$'

        inkDraw.text.latex(self, group, value, pos_text, fontSize=self.fontSize, refPoint='bc', preambleFile=self.preambleFile)

        if angleDeg != 0:
            self.rotateElement(group, position, angleDeg)

        inv_volt = (invertArrows == mirror)

        if flagVolt:
            if invertArrows:
                if inkDraw.useLatex:
                    if value[1] == '-':
                        value = value[0] + value[2:]
                    else:
                        value = value[0] + '-' + value[1:]
                else:
                    if value[0] == '-':
                        value = value[1:]
                    else:
                        value = '-' + value
            self.drawVoltArrow(group, self.add(position, [0, 8]), name=value, color=self.voltageColor, angleDeg=angleDeg, invertArrows=inv_volt)

        if flagCurr:
            if convention == 'active':
                self.drawCurrArrow(group, self.add(position, [20 + wireExtraSize, -5]), name=currName, color=self.currentColor, angleDeg=angleDeg,
                                   invertArrows=inv_volt)
            if convention == 'passive':
                self.drawCurrArrow(group, self.add(position, [20 + wireExtraSize, -5]), name=currName, color=self.currentColor, angleDeg=angleDeg,
                                   invertArrows=not inv_volt)

        return group

    # ---------------------------------------------
    def drawSourceI(self, parent, position=[0, 0], value='i(t)', label='Source', angleDeg=0, flagVolt=True, flagCurr=True, voltName='v',
                    invertArrows=False, mirror=False, convention='active', wireExtraSize=0):
        """ draws a independend general current source

        parent: parent object
        position: position [x,y]
        value: string with value.
        label: label of the object (it can be repeated)
        angleDeg: rotation angle in degrees counter-clockwise (default 0)
        flagVolt: indicates whether the voltage arrow must be drawn (default: true)
        voltName: voltage drop name (default: v)
        flagCurr: indicates whether the current arrow must be drawn (default: true)
        mirror: mirror source drawing (default: False)
        convention: passive/active sign convention. available types: 'passive', 'active' (default)
        wireExtraSize: additional length added to the terminals. If negative, the length will be reduced. default: 0)
        """

        group = self.createGroup(parent, label)
        elem = self.createGroup(group, label)

        inkDraw.line.relCoords(elem, [[-(18 + wireExtraSize), 0]], self.add(position, [-7, 0]))
        inkDraw.line.relCoords(elem, [[18 + wireExtraSize, 0]], self.add(position, [7, 0]))
        inkDraw.circle.centerRadius(elem, [0, 0], 7.0, offset=position, label='circle')

        # arrow
        lineStyleSign = inkDraw.lineStyle.set(lineWidth=0.7, lineColor=inkDraw.color.defined('black'), fillColor=inkDraw.color.defined('black'))
        if mirror:
            inkDraw.line.relCoords(elem, [[-5, 0], [0, 1.2], [-3, -1.2], [3, -1.2], [0, 1.2]], self.add(position, [4, 0]), lineStyle=lineStyleSign)
        else:
            inkDraw.line.relCoords(elem, [[5, 0], [0, 1.2], [3, -1.2], [-3, -1.2], [0, 1.2]], self.add(position, [-4, 0]), lineStyle=lineStyleSign)

        pos_text = self.add(position, [0, -8 - self.textOffset])
        if inkDraw.useLatex:
            value = '$' + value + '$'

        inkDraw.text.latex(self, group, value, pos_text, fontSize=self.fontSize, refPoint='bc', preambleFile=self.preambleFile)

        if angleDeg != 0:
            self.rotateElement(group, position, angleDeg)

        inv_curr = (invertArrows == mirror)

        if flagVolt:
            if convention == 'active':
                self.drawVoltArrow(group, self.add(position, [0, 8]), name=voltName, color=self.voltageColor, angleDeg=angleDeg,
                                   invertArrows=inv_curr)
            if convention == 'passive':
                self.drawVoltArrow(group, self.add(position, [0, 8]), name=voltName, color=self.voltageColor, angleDeg=angleDeg,
                                   invertArrows=not inv_curr)

        if flagCurr:
            if invertArrows:
                if inkDraw.useLatex:
                    if value[1] == '-':
                        value = value[0] + value[2:]
                    else:
                        value = value[0] + '-' + value[1:]
                else:
                    if value[0] == '-':
                        value = value[1:]
                    else:
                        value = '-' + value

            self.drawCurrArrow(group, self.add(position, [20 + wireExtraSize, -5]), name=value, color=self.currentColor, angleDeg=angleDeg,
                               invertArrows=inv_curr)

        return group

    # ---------------------------------------------
    def drawControledSourceV(self, parent, position=[0, 0], controlType='volt', gain='k', controlName='v_c', label='Source', angleDeg=0,
                             flagVolt=True, flagCurr=True, currName='i', invertArrows=False, mirror=False, convention='active', drawControl=False,
                             wireExtraSize=0):
        """ draws a controlled general voltage source

        parent: parent object
        position: position [x,y]
        controlType: 'volt' or 'curr'
        gain: controlled source gain value
        controlName: name of the controlling signal
        label: label of the object (it can be repeated)
        angleDeg: rotation angle in degrees counter-clockwise (default 0)
        flagVolt: indicates whether the voltage arrow must be drawn (default: true)
        currName: current name (default: i)
        flagCurr: indicates whether the current arrow must be drawn (default: true)
        mirror: mirror source drawing (default: False)
        convention: passive/active sign convention. available types: 'passive', 'active' (default)
        wireExtraSize: additional length added to the terminals. If negative, the length will be reduced. default: 0)
        drawControl: draws control annotation arrow (default:false)
        """

        group = self.createGroup(parent, label)
        elem = self.createGroup(group, label)

        inkDraw.line.relCoords(elem, [[-(17 + wireExtraSize), 0]], self.add(position, [-8, 0]))
        inkDraw.line.relCoords(elem, [[17 + wireExtraSize, 0]], self.add(position, [8, 0]))
        inkDraw.line.relCoords(elem, [[8, 8], [8, -8], [-8, -8], [-8, 8]], self.add(position, [-8, 0]))

        # signs
        if mirror:
            self.drawSigns(elem, positionPos=self.add(position, [-4, 0]), positionNeg=self.add(position, [4, 0]))
        else:
            self.drawSigns(elem, positionPos=self.add(position, [4, 0]), positionNeg=self.add(position, [-4, 0]))

        # text
        pos_text = self.add(position, [0, -8 - self.textOffset])
        value = gain + '.' + controlName

        if inkDraw.useLatex:
            value = '$' + value + '$'

        inkDraw.text.latex(self, group, value, pos_text, fontSize=self.fontSize, refPoint='bc', preambleFile=self.preambleFile)

        if angleDeg != 0:
            self.rotateElement(group, position, angleDeg)

        # arrows
        inv_volt = (invertArrows == mirror)

        if flagVolt:
            if invertArrows:
                if inkDraw.useLatex:
                    if value[1] == '-':
                        value = value[0] + value[2:]
                    else:
                        value = value[0] + '-' + value[1:]
                else:
                    if value[0] == '-':
                        value = value[1:]
                    else:
                        value = '-' + value
            self.drawVoltArrow(group, self.add(position, [0, 8]), name=value, color=self.voltageColor, angleDeg=angleDeg, invertArrows=inv_volt)

        if flagCurr:
            if convention == 'active':
                self.drawCurrArrow(group, self.add(position, [20 + wireExtraSize, -5]), name=currName, color=self.currentColor, angleDeg=angleDeg,
                                   invertArrows=inv_volt)
            if convention == 'passive':
                self.drawCurrArrow(group, self.add(position, [20 + wireExtraSize, -5]), name=currName, color=self.currentColor, angleDeg=angleDeg,
                                   invertArrows=not inv_volt)

        # control signal
        if drawControl:
            for theta in range(0, 360, 90):
                pos1 = self.add(position, [-20, 25 + theta / 4])
                pos2 = self.add(position, [0, 25 + theta / 4])
                if controlType == 'volt':
                    temp1 = self.drawVoltArrow(parent, pos1, name=controlName, color=self.voltageColor, angleDeg=theta, invertArrows=False)
                    temp2 = self.drawVoltArrow(parent, pos2, name=controlName, color=self.voltageColor, angleDeg=theta, invertArrows=True)
                if controlType == 'curr':
                    temp1 = self.drawCurrArrow(parent, pos1, name=controlName, color=self.currentColor, angleDeg=theta, invertArrows=False)
                    temp2 = self.drawCurrArrow(parent, pos2, name=controlName, color=self.currentColor, angleDeg=theta, invertArrows=True)

                self.rotateElement(temp1, pos1, theta)
                self.rotateElement(temp2, pos2, theta)

        return group

    # ---------------------------------------------
    def drawControledSourceI(self, parent, position=[0, 0], controlType='volt', gain='k', controlName='v_c', label='Source', angleDeg=0,
                             flagVolt=True, flagCurr=True, voltName='v', invertArrows=False, mirror=False, convention='active', drawControl=False,
                             wireExtraSize=0):
        """ draws a controlled general current source

        parent: parent object
        position: position [x,y]
        controlType: 'volt' or 'curr'
        gain: controlled source gain value
        controlName: name of the controlling signal
        label: label of the object (it can be repeated)
        angleDeg: rotation angle in degrees counter-clockwise (default 0)
        flagVolt: indicates whether the voltage arrow must be drawn (default: true)
        voltName: voltage name (default: v)
        flagCurr: indicates whether the current arrow must be drawn (default: true)
        mirror: mirror source drawing (default: False)
        convention: passive/active sign convention. available types: 'passive', 'active' (default)
        wireExtraSize: additional length added to the terminals. If negative, the length will be reduced. default: 0)
        drawControl: draws control annotation arrow (default:false)
        """

        group = self.createGroup(parent, label)
        elem = self.createGroup(group, label)

        inkDraw.line.relCoords(elem, [[-(17 + wireExtraSize), 0]], self.add(position, [-8, 0]))
        inkDraw.line.relCoords(elem, [[17 + wireExtraSize, 0]], self.add(position, [8, 0]))
        inkDraw.line.relCoords(elem, [[8, 8], [8, -8], [-8, -8], [-8, 8]], self.add(position, [-8, 0]))

        # arrow
        lineStyleSign = inkDraw.lineStyle.set(lineWidth=0.7, lineColor=inkDraw.color.defined('black'), fillColor=inkDraw.color.defined('black'))
        if mirror:
            inkDraw.line.relCoords(elem, [[-5, 0], [0, 1.2], [-3, -1.2], [3, -1.2], [0, 1.2]], self.add(position, [4, 0]), lineStyle=lineStyleSign)
        else:
            inkDraw.line.relCoords(elem, [[5, 0], [0, 1.2], [3, -1.2], [-3, -1.2], [0, 1.2]], self.add(position, [-4, 0]), lineStyle=lineStyleSign)

        # text
        pos_text = self.add(position, [0, -8 - self.textOffset])
        value = gain + '.' + controlName

        if inkDraw.useLatex:
            value = '$' + value + '$'

        inkDraw.text.latex(self, group, value, pos_text, fontSize=self.fontSize, refPoint='bc', preambleFile=self.preambleFile)

        if angleDeg != 0:
            self.rotateElement(group, position, angleDeg)

        # arrows
        inv_curr = (invertArrows == mirror)

        if flagVolt:
            if convention == 'active':
                self.drawVoltArrow(group, self.add(position, [0, 8]), name=voltName, color=self.voltageColor, angleDeg=angleDeg,
                                   invertArrows=inv_curr)
            if convention == 'passive':
                self.drawVoltArrow(group, self.add(position, [0, 8]), name=voltName, color=self.voltageColor, angleDeg=angleDeg,
                                   invertArrows=not inv_curr)

        if flagCurr:
            if invertArrows:
                if inkDraw.useLatex:
                    if value[1] == '-':
                        value = value[0] + value[2:]
                    else:
                        value = value[0] + '-' + value[1:]
                else:
                    if value[0] == '-':
                        value = value[1:]
                    else:
                        value = '-' + value

            self.drawCurrArrow(group, self.add(position, [20 + wireExtraSize, -5]), name=value, color=self.currentColor, angleDeg=angleDeg,
                               invertArrows=inv_curr)

        # control signal
        if drawControl:
            for theta in range(0, 360, 90):
                pos1 = self.add(position, [-20, 25 + theta / 4])
                pos2 = self.add(position, [0, 25 + theta / 4])
                if controlType == 'volt':
                    temp1 = self.drawVoltArrow(parent, pos1, name=controlName, color=self.voltageColor, angleDeg=theta, invertArrows=False)
                    temp2 = self.drawVoltArrow(parent, pos2, name=controlName, color=self.voltageColor, angleDeg=theta, invertArrows=True)
                if controlType == 'curr':
                    temp1 = self.drawCurrArrow(parent, pos1, name=controlName, color=self.currentColor, angleDeg=theta, invertArrows=False)
                    temp2 = self.drawCurrArrow(parent, pos2, name=controlName, color=self.currentColor, angleDeg=theta, invertArrows=True)

                self.rotateElement(temp1, pos1, theta)
                self.rotateElement(temp2, pos2, theta)

        return group
