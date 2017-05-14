from setting import Settings
import numpy as np
import math
import random
from random import randint
import matplotlib.pyplot as plt
from exponDeltaH import exponDeltaH
from general import createField,calculateH,calculateM

class MetaMothod:
    def __init__(self,settingPath):
        self.settings = Settings(settingPath)
        self.fieldSize = self.settings.getValue('size')
        self.t = self.settings.getValue('temperture')
        self.Hami = self.settings.getValue('hamiltonian')
        self.maxIter = self.settings.getValue('maxIter')
        self.exponDeltaHList = exponDeltaH({})
        self.fieldInitMethod = self.settings.getValue('init')
        random.seed(self.settings.getValue('randomSeed'))
        self.applyFunc = {}
        self.changeHistory = []
        self.deltaHHistory = []
        self.deltaMHistory = []
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
    pass