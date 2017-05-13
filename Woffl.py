from setting import Settings
import numpy as np
import math
import random
from random import randint
import matplotlib.pyplot as plt
from exponDeltaH import exponDeltaH
from general import createField,calculateH,calculateM

class Woffl:
    def __init__(self,settingPath):
        self.settings = Settings(settingPath)
        self.fieldSize = self.settings.getValue('size')
        self.t = self.settings.getValue('temperture')
        self.Hami = self.settings.getValue('hamiltonian')
        self.maxIter = self.settings.getValue('maxIter')
        self.exponDeltaHList = exponDeltaH({})
        #self.flipTimes = self.settings.getValue('flipTimes')
        self.fieldInitMethod = self.settings.getValue('init')
        random.seed(self.settings.getValue('randomSeed'))
        self.applyFunc = {}
        self.changeHistory = []
        self.deltaHHistory = []
        self.deltaMHistory = []
    def init(self,field):
        self.field = np.copy(field)
        self.startField = np.copy(field)
        return self.field
    def createChange(self):
        pass
    def changeField(self):
        self.newfield = self.changeFieldMulti(self.field,self.changes)
        return self.newfield
    def changeFieldMulti(self,field,changes):
        newfield = np.copy(field)
        for n in range(len(changes)):
            i = changes[n][0]
            j = changes[n][1]
            newfield[i,j] = -newfield[i,j]
        return newfield
    def showField(self):
        plt.matshow(self.field)
        plt.show()
    def calculateDeltaH(self):
        B = self.Hami[1]
        J = self.Hami[0]
        deltaHb = 0.0
        deltaHj = 0.0
        shape = self.fieldSize
        pass
    def calculateDeltaM(self):
        self.deltaM = 0.0
        for n in range(len(self.changes)):
            i = self.changes[n][0]
            j = self.changes[n][1]
            self.deltaM += -2*self.field[i,j]
        return self.deltaM
    def runOnce(self):
        self.createChange()
        self.changeField()
        self.calculateDeltaH()
        self.calculateDeltaM()
        pass
    def run(self,times):
        for _ in range(times):
            self.runOnce()
     def fieldHistory(self,n):
        field = np.copy(self.startField)
        for i in n:
            self.changeFieldMulti(field,changeHistory[i])
        return field
    def HHistory(self,initH):
        HHistory = [initH]
        for n in range(1,len(self.deltaHHistory)+1):
            HHistory.append(HHistory[n-1]+self.deltaHHistory[n-1])
        return HHistory
    def MHistory(self,initM):
        MHistory = [initM]
        for n in range(1,len(self.deltaMHistory)+1):
            MHistory.append(MHistory[n-1]+self.deltaMHistory[n-1])
        return MHistory


if __name__ == '__main__':
    w = Woffl('./Woffl_settings.txt')
    f = createField(w.fieldSize,m.fieldInitMethod)