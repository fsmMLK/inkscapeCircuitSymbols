#!/usr/bin/python

import inkscapeMadeEasy.inkscapeMadeEasy_Base as inkBase
import inkscapeMadeEasy.inkscapeMadeEasy_Draw as inkDraw


class ampOp(inkBase.inkscapeMadeEasy):

    # ---------------------------------------------
    def drawOpAmpGeneral(self, parent, position=[0, 0], label='OpAmp', mirrorInput=False, drawVin=False, drawIin=False, drawVd=False, drawVout=False,
                         drawIout=False, inputVPosName='v^+', inputVNegName='v^-', inputIPosName='i^+', inputINegName='i^-', VoutName='v_o',
                         IoutName='i_o', VdiffName='v_d', flagDrawSupply=False, FlagSupplyValues=False, flagSupplySymm=True,
                         supplyPositiveVal='V_{cc}', supplyNegativeVal='-V_{cc}'):
        """ draws a general ampOp

        parent: parent object
        position: position [x,y]
        label: label of the object (it can be repeated)
        mirrorInput: invert + and - inputs (default: positive above, negative below)
        drawVin: write v+ and v- besides the inputs (default: False)
        drawVd: write vd besides the input terminals
        flagDrawSupply: draw supply terminals
        """
        group = self.createGroup(parent, label)
        elem = self.createGroup(group, label)

        inkDraw.line.relCoords(elem, [[-35, 20], [0, -40], [35, 20]], [position[0] + 35, position[1]])
        inkDraw.line.relCoords(elem, [[-7.5, 0]], [position[0], position[1] + 10])
        inkDraw.line.relCoords(elem, [[-7.5, 0]], [position[0], position[1] - 10])
        inkDraw.line.relCoords(elem, [[7.5, 0]], [position[0] + 35, position[1]])

        if flagDrawSupply:
            inkDraw.line.relCoords(elem, [[0, -5]], [position[0] + 17.5, position[1] - 10])
            inkDraw.line.relCoords(elem, [[0, 5]], [position[0] + 17.5, position[1] + 10])
            if FlagSupplyValues:
                if flagSupplySymm:
                    self.drawSignal(elem, [position[0] + 17.5, position[1] - 25], angleDeg=0, nodalVal='+' + supplyPositiveVal.replace('+', ''))
                    self.drawSignal(elem, [position[0] + 17.5, position[1] + 25], angleDeg=180, nodalVal='-' + supplyPositiveVal.replace('+', ''))
                else:
                    self.drawSignal(elem, [position[0] + 17.5, position[1] - 25], angleDeg=0, nodalVal='+' + supplyPositiveVal.replace('+', ''))
                    self.drawSignal(elem, [position[0] + 17.5, position[1] + 25], angleDeg=180, nodalVal=supplyNegativeVal)

        # input signs
        lineStyleSign = inkDraw.lineStyle.setSimpleBlack(lineWidth=0.7)
        if mirrorInput:
            inkDraw.line.relCoords(elem, [[-3, 0]], [position[0] + 6, position[1] + 10], lineStyle=lineStyleSign)
            inkDraw.line.relCoords(elem, [[0, -3]], [position[0] + 4.5, position[1] + 11.5], lineStyle=lineStyleSign)

            inkDraw.line.relCoords(elem, [[-3, 0]], [position[0] + 6, position[1] - 10], lineStyle=lineStyleSign)
            if drawVin:
                textVTop = inputVNegName
                textVBot = inputVPosName
            if drawIin:
                textITop = inputINegName
                textIBot = inputIPosName
        else:
            inkDraw.line.relCoords(elem, [[-3, 0]], [position[0] + 6, position[1] + 10], lineStyle=lineStyleSign)
            inkDraw.line.relCoords(elem, [[-3, 0]], [position[0] + 6, position[1] - 10], lineStyle=lineStyleSign)
            inkDraw.line.relCoords(elem, [[0, 3]], [position[0] + 4.5, position[1] - 11.5], lineStyle=lineStyleSign)
            if drawVin:
                textVTop = inputVPosName
                textVBot = inputVNegName
            if drawIin:
                textITop = inputIPosName
                textIBot = inputINegName

        # write v+ v-
        if drawVin:
            posTop = [position[0] - 1, position[1] - 10 - self.textOffsetSmall]
            posBot = [position[0] - 1, position[1] + 10 - self.textOffsetSmall]

            if inkDraw.useLatex:
                textVTop = '$' + textVTop + '$'
                textVBot = '$' + textVBot + '$'

            temp1 = inkDraw.text.latex(self, group, textVTop, posTop, textColor=self.voltageColor, fontSize=self.fontSizeSmall, refPoint='br',
                                       preambleFile=self.preambleFile)
            temp2 = inkDraw.text.latex(self, group, textVBot, posBot, textColor=self.voltageColor, fontSize=self.fontSizeSmall, refPoint='br',
                                       preambleFile=self.preambleFile)

        # write i+ i-
        if drawIin:
            posTop = [position[0] - 7.5, position[1] - 10 + 3]
            posBot = [position[0] - 7.5, position[1] + 10 + 3]

            temp1 = self.drawCurrArrow(group, posTop, name=textITop, color=self.currentColor, angleDeg=180, invertArrows=False)
            self.rotateElement(temp1, posTop, 180)
            temp1 = self.drawCurrArrow(group, posBot, name=textIBot, color=self.currentColor, angleDeg=180, invertArrows=False)
            self.rotateElement(temp1, posBot, 180)

        # write v_out
        if drawVout:
            postext = [position[0] + 35, position[1] - self.textOffsetSmall]

            if inkDraw.useLatex:
                VoutName = '$' + VoutName + '$'

            temp1 = inkDraw.text.latex(self, group, VoutName, postext, textColor=self.voltageColor, fontSize=self.fontSize, refPoint='bl',
                                       preambleFile=self.preambleFile)

        # write i_out
        if drawIout:
            pos = [position[0] + 42, position[1] + 3]

            temp1 = self.drawCurrArrow(group, pos, name=IoutName, color=self.currentColor, angleDeg=180, invertArrows=False)
            self.rotateElement(temp1, pos, 180)

        if drawVd:
            pos1 = [position[0] + 6, position[1]]
            temp1 = self.drawVoltArrow(group, pos1, name=VdiffName, color=self.voltageColor, angleDeg=90, invertArrows=not mirrorInput, size=15)
            self.rotateElement(temp1, pos1, 90)

        return group
