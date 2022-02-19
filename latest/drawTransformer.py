#!/usr/bin/python

import numpy as np

import inkscapeMadeEasy.inkscapeMadeEasy_Base as inkBase
import inkscapeMadeEasy.inkscapeMadeEasy_Draw as inkDraw


# reference: https://www.electronics-tutorials.ws/resources/transformer-symbols.html

class transformer(inkBase.inkscapeMadeEasy):
    def add(self, vector, delta):
        # vector does not need to be numpy array. delta will be converted to numpy array. Numpy can then deal with np.array + list
        return vector + np.array(delta)

    # ---------------------------------------------
    def drawTransfWinding(self, parent, position=[0, 0], label='transfWinding', size=50, flagTapped=False, wireExtraSize=0,
                          forceEven=True, turnRadius=3.5,polarityIndication=0,flagAddSideTerminals=False):
        """ draws one winding of the transformer

        parent: parent object
        position: position [x,y]. the center of the winding will be places at this position
        label: label of the object (it can be repeated)
        size: size of the coil (default 50)
        flagTapped: add central tap
        wireExtraSize: extra terminal wire length
        forceEven: force even number of coil turns
        turnRadius: radius of each turn
        polarityIndication: 0: no indication  1: indication in one size  -1: indication in the other side
        flagAddSideTerminals (bool): used to create side terminas for transformers
        """

        elem = self.createGroup(parent, label)

        Nturns = int(size / (2 * turnRadius))
        # makes sure Nturns is even
        if forceEven and Nturns % 2 == 1:
            Nturns -= 1

        # terminals
        length = size / 2 + wireExtraSize - (turnRadius * 2) * (Nturns / 2)

        if flagAddSideTerminals:
            inkDraw.line.relCoords(elem, [[-length, 0], [0, -20]], self.add(position, [-(turnRadius * 2) * (Nturns / 2), 0]))
            inkDraw.line.relCoords(elem, [[length, 0], [0, -20]], self.add(position, [(turnRadius * 2) * (Nturns / 2), 0]))
        else:
            inkDraw.line.relCoords(elem, [[-length, 0]], self.add(position, [-(turnRadius * 2) * (Nturns / 2), 0]))
            inkDraw.line.relCoords(elem, [[length, 0]], self.add(position, [(turnRadius * 2) * (Nturns / 2), 0]))

        # wire loops
        center = -(Nturns / 2) * (turnRadius * 2) + turnRadius
        for i in range(Nturns):
            inkDraw.ellipseArc.centerAngStartAngEnd(elem, self.add(position, [center, 0]), turnRadius, turnRadius + 2, 0.0, 180.0, [0, 0],
                                                    largeArc=False)
            center += 2 * turnRadius

        # tapped
        if flagTapped:
            myLine = inkDraw.lineStyle.set(lineWidth=1.0, lineColor=inkDraw.color.defined('black'), fillColor=inkDraw.color.defined('black'))
            inkDraw.line.relCoords(elem, [[0, -20]], position,lineStyle=myLine)

        # phase indication
        if polarityIndication!=0:
            inkDraw.circle.centerRadius(elem, self.add(position, [-polarityIndication*(size / 2 - 5), -5]), 0.6)

        return elem  # ---------------------------------------------

    def inductor(self, parent, position=[0, 0], angleDeg=0, coreType='air', flagTapped=False, flagVolt=True, voltName='v', flagCurr=True,
                 currName='i', invertArrows=False, convention='passive', wireExtraSize=0):
        """ draws an inductor

        parent: parent object
        position: position [x,y]
        angleDeg: rotation angle in degrees counter-clockwise (default 0)
        coreType='air', 'iron', 'ferrite'
        flagTapped: add taps to the windings
        flagVolt: indicates whether the voltage arrow must be drawn (default: true)
        voltName: voltage drop name (default: v)
        flagCurr: indicates whether the current arrow must be drawn (default: true)
        currName: current drop name (default: i)
        invertArrows: invert V/I arrow directions (default: False)
        convention: passive/active sign convention. available types: 'passive' (default) , 'active'
        wireExtraSize: additional length added to the terminals. If negative, the length will be reduced. default: 0)
        """

        group = self.createGroup(parent)
        elem = self.createGroup(group)

        sizeCoil = 50
        turnRadius = 3

        #draw winding
        self.drawTransfWinding(elem, position=position, size=sizeCoil - 10, flagTapped=False, wireExtraSize=wireExtraSize + 5,
                               forceEven=True, turnRadius=turnRadius, polarityIndication=0, flagAddSideTerminals=False)

        # manual tap
        if flagTapped:
            inkDraw.line.relCoords(elem, [[0, -10]], position)

        if flagVolt:
            if coreType.lower() == 'air':
                posY = 8
            else:
                posY = 15

            if convention == 'passive':
                self.drawVoltArrowSimple(group, self.add(position, [0,posY]), name=voltName, color=self.voltageColor, angleDeg=angleDeg,
                                         invertArrows=not invertArrows, size=sizeCoil - 20, invertCurvatureDirection=False, extraAngleText=0.0)
            if convention == 'active':
                self.drawVoltArrowSimple(group, self.add(position, [0, posY]), name=voltName, color=self.voltageColor, angleDeg=angleDeg,
                                         invertArrows= invertArrows, size=sizeCoil - 20, invertCurvatureDirection=False, extraAngleText=0.0)

        if flagCurr:
            posText  = -( sizeCoil / 2 -10)
            self.drawCurrArrowSimple(group, self.add(position, [posText - wireExtraSize,-5]), name=currName, color=self.currentColor,
                                         angleDeg=angleDeg, invertArrows=invertArrows,invertTextSide=False, size=10)

        # core
        if coreType.lower() == 'iron':
            inkDraw.line.relCoords(elem, [[40, 0]], self.add(position, [-20,8.5]))
            inkDraw.line.relCoords(elem, [[40, 0]], self.add(position, [-20,11.5]))

        if coreType.lower() == 'ferrite':
            myDash = inkDraw.lineStyle.createDashedLinePattern(dashLength=3.0, gapLength=3.0)
            myDashedStyle = inkDraw.lineStyle.set(lineWidth=0.8, strokeDashArray=myDash)
            inkDraw.line.relCoords(elem, [[40, 0]], self.add(position, [-20,8.5]), lineStyle=myDashedStyle)
            inkDraw.line.relCoords(elem, [[40, 0]], self.add(position, [-20,11.5]), lineStyle=myDashedStyle)

        if angleDeg != 0:
            self.rotateElement(group, position, angleDeg)

        return group

    # ---------------------------------------------
    def drawTransformer(self, parent, position=[0, 0], angleDeg=0, transformerLabel='',
                        coreType='air', stepType='one2one', flagPolaritySymbol=False, nCoils=[1, 1], invertPolarity=[False, False],
                        flagTapped=[False, False], flagVolt=[True, True], voltName=['v', 'v'], flagCurr=[True, True], currName=['i', 'i'],
                        invertArrows=[False, False], convention=['passive', 'passive'], wireExtraSize=0):
        """ draws a transformer

        parent: parent object
        position: position [x,y]
        label: label of the object (it can be repeated)
        angleDeg: rotation angle in degrees counter-clockwise (default 0)
        coreType='air', 'iron', 'ferrite'
        stepType='up', 'down', 'one2one'
        flagPolaritySymbol: if True, add the dots to indicate the phase of the primary and secondary
        nCoils: (list) integer number of coils of the primary and secondary
        invertPolarity: (list) inverts phase symbol of the primary and secondary
        flagTapped: (list) add taps to the windings
        flagVolt: (list) indicates whether the voltage arrow must be drawn (default: true)
        voltName: (list) voltage drop name (default: v)
        flagCurr: (list) indicates whether the current arrow must be drawn (default: true)
        currName: (list) current drop name (default: i)
        invertArrows: (list) invert V/I arrow directions (default: False)
        convention: (list) passive/active sign convention. available types: 'passive' (default) , 'active'
        wireExtraSize: additional length added to the terminals. If negative, the length will be reduced. default: 0)
        """

        group = self.createGroup(parent)
        elem = self.createGroup(group)

        # ----------------------
        # primary
        # ----------------------
        extraSize = 0
        if nCoils[0] == 1:
            sizeCoil = 50
            posCoil = [position]
            turnRadius = 3.5

        if nCoils[0] == 2:
            sizeCoil = 25
            posCoil = [self.add(position, [0, -17.5]), self.add(position, [0, 17.5])]
            turnRadius = 3.0

        # step up/down only if primary/secondary have 1 coil each
        if nCoils[0] == 1 and nCoils[1] == 1:
            if stepType == 'up':
                extraSize = 5
                sizeCoil -= 10

        for pos in posCoil:

            # polarity indication
            polarity=0
            if flagPolaritySymbol and invertPolarity[0]:
                polarity=1
            if flagPolaritySymbol and not invertPolarity[0]:
                polarity=-1

            #draw winding
            wind = self.drawTransfWinding(elem, position=self.add(pos, [-10, 0]), size=sizeCoil, flagTapped=flagTapped[0],
                                   wireExtraSize=wireExtraSize + extraSize, forceEven=True, turnRadius=turnRadius, polarityIndication= polarity,
                                   flagAddSideTerminals=True)

            self.rotateElement(wind, self.add(pos, [-10, 0]), 90)

            if flagVolt[0]:
                distX=-30
                if convention[0] == 'passive':
                    self.drawVoltArrowSimple(group, self.add(pos, [distX, 0]), name=voltName[0], color=self.voltageColor, angleDeg=angleDeg + 90,
                                             invertArrows=invertArrows[0], size=sizeCoil - 10, invertCurvatureDirection=True, extraAngleText=0.0)
                if convention[0] == 'active':
                    self.drawVoltArrowSimple(group, self.add(pos, [distX, 0]), name=voltName[0], color=self.voltageColor, angleDeg=angleDeg + 90,
                                             invertArrows=not invertArrows[0], size=sizeCoil - 10, invertCurvatureDirection=True, extraAngleText=0.0)

            if flagCurr[0]:
                posText  = -( sizeCoil / 2 -5)
                invertTextSide=True
                arrowDir  = invertArrows[0]
                if flagPolaritySymbol and invertPolarity[0]:
                    posText  = -( sizeCoil / 2 -5)
                    invertTextSide=True
                    arrowDir = invertArrows[0]
                if flagPolaritySymbol and not invertPolarity[0]:
                    posText  = ( sizeCoil / 2 -5)
                    invertTextSide=False
                    arrowDir  = not invertArrows[0]

                self.drawCurrArrowSimple(group, self.add(pos, [-20, posText - wireExtraSize]), name=currName[0], color=self.currentColor,
                                             angleDeg=angleDeg, invertArrows=arrowDir,invertTextSide=invertTextSide, size=10)

        # ----------------------
        # secondary
        # ----------------------
        extraSize = 0
        if nCoils[1] == 1:
            sizeCoil = 50
            posCoil = [position]
            turnRadius = 3.5
            offsetCurrText = 0

        if nCoils[1] == 2:
            sizeCoil = 25
            posCoil = [self.add(position, [0, -17.5]), self.add(position, [0, 17.5])]
            turnRadius = 3.0
            offsetCurrText = -3

        # step up/down only if primary/secondary have 1 coil each
        if nCoils[0] == 1 and nCoils[1] == 1:
            if stepType == 'down':
                extraSize = 5
                sizeCoil -= 10

        for pos in posCoil:

            # polarity indication
            polarity=0
            if flagPolaritySymbol and invertPolarity[1]:
                polarity=-1
            if flagPolaritySymbol and not invertPolarity[1]:
                polarity=1

            wind = self.drawTransfWinding(elem, position=self.add(pos, [10, 0]), size=sizeCoil, flagTapped=flagTapped[1],
                                   wireExtraSize=wireExtraSize + extraSize, forceEven=True, turnRadius=turnRadius, polarityIndication=polarity,
                                   flagAddSideTerminals=True)

            self.rotateElement(wind, self.add(pos, [10, 0]), -90)

            if flagVolt[1]:
                if convention[1] == 'passive':
                    self.drawVoltArrowSimple(group, self.add(pos, [30, 0]), name=voltName[1], color=self.voltageColor, angleDeg=angleDeg + 90,
                                             invertArrows=not invertArrows[1], size=sizeCoil - 10, invertCurvatureDirection=False, extraAngleText=0.0)
                if convention[1] == 'active':
                    self.drawVoltArrowSimple(group, self.add(pos, [30, 0]), name=voltName[1], color=self.voltageColor, angleDeg=angleDeg + 90,
                                             invertArrows= invertArrows[1], size=sizeCoil - 10, invertCurvatureDirection=False, extraAngleText=0.0)

            if flagCurr[1]:
                posText  = -( sizeCoil / 2 -5)
                invertTextSide=True
                arrowDir  = invertArrows[1]
                if flagPolaritySymbol and invertPolarity[0]:
                    posText  = -( sizeCoil / 2 -5)
                    invertTextSide=True
                    arrowDir = invertArrows[1]
                if flagPolaritySymbol and not invertPolarity[1]:
                    posText  = ( sizeCoil / 2 -5)
                    invertTextSide=False
                    arrowDir  = not invertArrows[1]

                self.drawCurrArrowSimple(group, self.add(pos, [20, posText - wireExtraSize]), name=currName[1], color=self.currentColor,
                                             angleDeg=angleDeg, invertArrows=arrowDir,invertTextSide=invertTextSide, size=10)

        # core
        if coreType.lower() == 'iron':
            inkDraw.line.relCoords(elem, [[0, 50]], self.add(position, [1.5, -25]))
            inkDraw.line.relCoords(elem, [[0, 50]], self.add(position, [-1.5, -25]))

        if coreType.lower() == 'ferrite':
            myDash = inkDraw.lineStyle.createDashedLinePattern(dashLength=3.0, gapLength=3.0)
            myDashedStyle = inkDraw.lineStyle.set(lineWidth=0.8, strokeDashArray=myDash)
            inkDraw.line.relCoords(elem, [[0, 50]], self.add(position, [1.5, -25]), lineStyle=myDashedStyle)
            inkDraw.line.relCoords(elem, [[0, 50]], self.add(position, [-1.5, -25]), lineStyle=myDashedStyle)

        if angleDeg != 0:
            self.rotateElement(group, position, angleDeg)

        return group
