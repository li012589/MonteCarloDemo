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
        self.flipTimes = self.settings.getValue('flipTimes')
        self.fieldInitMethod = self.settings.getValue('init')
        random.seed(self.settings.getValue('randomSeed'))
        self.applyFunc = {}
        self.changeHistory = []
        self.deltaHHistory = []
        self.deltaMHistory = []
    def init(self,field):
        self.field = np.copy(field)
        self.startField = np.copy(field)
        return field


if __name__ == '__main__':
    pass