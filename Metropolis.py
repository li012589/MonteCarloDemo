from setting import Settings
import numpy as np
import math
import random
from random import randint
import matplotlib.pyplot as plt
from exponDeltaH import exponDeltaH
from general import createField,calculateH,calculateM

class Metropolis:
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
        self.field = field
        self.startField = field
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
    def calculateDeltaM(self):
        self.deltaM = 0.0
        for n in range(len(self.changes)):
            i = self.changes[n][0]
            j = self.changes[n][1]
            self.deltaM += -2*self.field[i,j]
        return self.deltaM
    def runOnce(self):
        self.createChange()
        #print self.field
        #print changes
        self.changeField()
        #print field
        self.calculateDeltaH()
        self.calculateDeltaM()
        #print self.field
        #print deltaH
        if self.deltaH <= 0:
            self.field = self.newfield
            self.changeHistory.append(self.changes)
            #print 'Accepted!'
            self.deltaHHistory.append(self.deltaH)
            self.deltaMHistory.append(self.deltaM)
            print self.deltaH
        else:
            if random.random() <= self.exponDeltaHList.calculate(self.deltaH,self.t):
                #print 'Accepted with high H!'
                self.field = self.newfield
                self.changeHistory.append(self.changes)
                self.deltaHHistory.append(self.deltaH)
                self.deltaMHistory.append(self.deltaM)
                print self.deltaH
            else:
                print 'Rejected'
                self.changeHistory.append([])
                self.deltaHHistory.append(0)
                self.deltaMHistory.append(0)
        return self.field
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
    # Test if works
    m = Metropolis('./Metropolis_settings.txt')
    f = createField(m.fieldSize,m.fieldInitMethod)
    m.init(f)
#    m.showField()
    print calculateH(m.field,m.Hami[0],m.Hami[1])
    M = [calculateM(m.field)]
    H = [calculateH(m.field,m.Hami[0],m.Hami[1])]
    Hh = H
    Mh = M
    for _ in range(10):
        m.runOnce()
        H.append(calculateH(m.field,m.Hami[0],m.Hami[1]))
        M.append(calculateM(m.field))
        Hh.append(Hh[0]+sum(m.deltaHHistory))
        Mh.append(Mh[0]+sum(m.deltaMHistory))
    #print calculateH(m.field,m.Hami[0],m.Hami[1])
    #print H
    print calculateH(m.field,m.Hami[0],m.Hami[1])
    print Hh
    #print M
    #print Mh
    print m.HHistory(H[0])
    print m.deltaHHistory
    print H == m.HHistory(H[0])
    print M == m.MHistory(M[0])
    #m.showField()