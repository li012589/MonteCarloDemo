from setting import Settings
import numpy as np
import math
import random
from random import randint
import matplotlib.pyplot as plt
from exponDeltaH import exponDeltaH
from general import createField,calculateH

class Metropolis:
    def __init__(self,settingPath):
         self.settings = Settings(settingPath)
         self.fieldSize = self.settings.getValue('size')
         self.t = self.settings.getValue('temperture')
         self.Hami = self.settings.getValue('hamiltonian')
         self.maxTter = self.settings.getValue('maxIter')
         self.exponDeltaHList = exponDeltaH({})
         self.flipTimes = self.settings.getValue('flipTimes')
         self.fieldInitMethod = self.settings.getValue('init')
         random.seed(self.settings.getValue('randomSeed'))
    def init(self,field):
        self.field = field
        return field
    def createChange(self):
        self.changes = []
        for _ in range(self.flipTimes):
            i=randint(0,self.fieldSize[0]-1)
            j=randint(0,self.fieldSize[1]-1)
            if (i,j) in self.changes:
                self.changes.remove((i,j))
            else:
                self.changes.append((i,j))
        return self.changes
    def changeField(self):
        self.newfield = np.copy(self.field)
        for n in range(len(self.changes)):
            i = self.changes[n][0]
            j = self.changes[n][1]
            self.newfield[i,j] = -self.newfield[i,j]
        return self.newfield
    def showField(self):
        plt.matshow(self.field)
        plt.show()
    def calculateDeltaH(self):
        B = self.Hami[1]
        J = self.Hami[0]
        deltaHb = 0.0
        deltaHj = 0.0
        shape = self.fieldSize
        for n in range(len(self.changes)):
            i = self.changes[n][0]
            j = self.changes[n][1]
            deltaHb += -2*self.field[i,j]*B
            if i-1>=0 :
                if not (i-1,j) in self.changes:
                    deltaHj += -J*-self.field[i,j]*self.field[i-1,j]+J*self.field[i,j]*self.field[i-1,j]
                else:
                    deltaHj += -J*-self.field[i,j]*-self.field[i-1,j]+J*self.field[i,j]*self.field[i-1,j]
            if i+1<shape[0]:
                if not (i+1,j) in self.changes:
                    deltaHj += -J*-self.field[i,j]*self.field[i+1,j]+J*self.field[i,j]*self.field[i+1,j]
                else:
                    deltaHj += -J*-self.field[i,j]*-self.field[i+1,j]+J*self.field[i,j]*self.field[i+1,j]
            if j-1>=0:
                if not (i,j-1) in self.changes:
                    deltaHj += -J*-self.field[i,j]*self.field[i,j-1]+J*self.field[i,j]*self.field[i,j-1]
                else:
                    deltaHj += -J*-self.field[i,j]*-self.field[i,j-1]+J*self.field[i,j]*self.field[i,j-1]
            if j+1<shape[1]:
                if not (i,j+1) in self.changes:
                    deltaHj += -J*-self.field[i,j]*self.field[i,j+1]+J*self.field[i,j]*self.field[i,j+1]
                else:
                    deltaHj += -J*-self.field[i,j]*-self.field[i,j+1]+J*self.field[i,j]*self.field[i,j+1]
        self.deltaH = -(-deltaHj + deltaHb)
        return self.deltaH
    def run(self,times):
        for n in range(times):
            self.createChange()
            #print self.field
            #print changes
            self.changeField()
            #print field
            self.calculateDeltaH()
            #print self.field
            #print deltaH
            if self.deltaH <= 0:
                self.field = self.newfield
                print 'Accepted!'
                print self.deltaH
            else:
                if random.random() <= self.exponDeltaHList.calculate(self.deltaH,self.t):
                    print 'Accepted with high H!'
                    self.field = self.newfield
                    print self.deltaH
                else:
                    #print 'Rejected'
                    pass
        return self.field

if __name__ == '__main__':
    # Test if works
    m = Metropolis('./settings.txt')
    f = createField(m.fieldSize,m.fieldInitMethod)
    m.init(f)
    m.showField()
    print calculateH(m.field,m.Hami[0],m.Hami[1])
    m.run(10)
    print calculateH(m.field,m.Hami[0],m.Hami[1])
    m.showField()