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
        self.P_add = 1-math.exp(-2*self.Hami[0]/self.t)
        return self.field
    def createChange(self):
        self.tochanges = [(randint(0,self.fieldSize[0]-1),randint(0,self.fieldSize[1]-1))]
        self.boundary = set()
        self.nboundary = set()
        self.seed = self.field[self.tochanges[0][0],self.tochanges[0][1]]
        #print self.changes[0]
        self.totalChange = 1
        self.oldfield = np.copy(self.field)
        self.field[self.tochanges[0][0],self.tochanges[0][1]] = -self.seed
        self.changes = [(self.tochanges[0][0],self.tochanges[0][1])]
        while len(self.tochanges) >0:
            changes = self.tochanges.pop(0)
            i = changes[0]
            j = changes[1]
            if i+1 < self.fieldSize[0]:
                if self.field[(i+1,j)] == self.seed:
                    if random.random() <= self.P_add:
                        self.tochanges.append((i+1,j))
                        self.totalChange += 1
                        self.field[i+1,j] = -self.seed
                        self.changes.append((i+1,j))
                        #print i+1,j
                    else:
                        self.boundary.add((i+1,j))
                else:
                    self.nboundary.add((i+1,j))
            if i-1 >= 0:
                if self.field[(i-1,j)] == self.seed:
                    if random.random() <= self.P_add:
                        self.tochanges.append((i-1,j))
                        self.totalChange += 1
                        self.field[i-1,j] = -self.seed
                        self.changes.append((i-1,j))
                        #print i-1,j
                    else:
                        self.boundary.add((i-1,j))
                else:
                    self.nboundary.add((i-1,j))
            if j+1 < self.fieldSize[1]:
                if self.field[(i,j+1)] == self.seed:
                    if random.random() <= self.P_add:
                        self.tochanges.append((i,j+1))
                        self.totalChange += 1
                        self.field[i,j+1] = -self.seed
                        self.changes.append((i,j+1))
                        #print i,j+1
                    else:
                        self.boundary.add((i,j+1))
                else:
                    self.nboundary.add((i,j+1))
            if j-1 >= 0:
                if self.field[(i,j-1)] == self.seed:
                    if random.random() <= self.P_add:
                        self.tochanges.append((i,j-1))
                        self.totalChange += 1
                        self.field[i,j-1] = -self.seed
                        self.changes.append((i,j-1))
                        #print i,j-1
                    else:
                        self.boundary.add((i,j-1))
                else:
                    self.nboundary.add((i,j-1))
        return self.field
#    def changeField(self):
 #       pass
    def showField(self):
        plt.matshow(self.field)
        plt.show()
    def calculateDeltaH(self):
        B = self.Hami[1]
        J = self.Hami[0]
        deltaHb = 0.0
        deltaHj = 0.0
        sumBoundary = 0
        sumnBoundary = 0
        #print self.boundary
        #print self.nboundary
        #print self.totalChange
        for iterm in self.boundary:
            if self.field[iterm[0],iterm[1]] == self.seed:
                sumBoundary += 1
        for iterm in self.nboundary:
            if self.oldfield[iterm[0],iterm[1]] != self.seed:
                sumnBoundary += 1
        #print sumBoundary
        #print sumnBoundary
        deltaHb = 2*B*self.totalChange*self.seed
        deltaHj = 2*J*sumBoundary - 2*J*sumnBoundary
        #print deltaHb
        #print deltaHj
        self.deltaH = (deltaHj + deltaHb)
        return self.deltaH
    def calculateDeltaM(self):
        self.deltaM = -2*self.totalChange*self.seed
        return self.deltaM
    def runOnce(self):
        #print self.field
        self.createChange()
        self.calculateDeltaH()
        self.calculateDeltaM()
        #print self.field
        self.changeHistory.append(self.changes)
        self.deltaHHistory.append(self.deltaH)
        self.deltaMHistory.append(self.deltaM)
        return self.field
    def run(self,times):
        #self.M = [calculateM(self.field)]
        #self.H = [calculateH(self.field,self.Hami[0],self.Hami[1])]
        #initH = calculateH(self.field,self.Hami[0],self.Hami[1])
        #print "initH = "+ str(initH)
        for _ in range(times):
            self.runOnce()
            #self.M.append(calculateM(self.field))
            #self.H.append(calculateH(self.field,self.Hami[0],self.Hami[1]))
            #print "cal = "+ str(calculateH(self.field,self.Hami[0],self.Hami[1]))
            #print "delta = "+str((self.HHistory(initH))[-1])
            #print "delta2 = "+str(initH + np.sum(self.deltaH))
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
    #test if work
    w = Woffl('./Woffl_settings.txt')
    f = createField(w.fieldSize,w.fieldInitMethod)
    w.init(f)
    initH = calculateH(w.field,w.Hami[0],w.Hami[1])
    #print initH
    initM  =calculateM(w.field)
    w.run(1000)
    #w.runOnce()
    #print w.deltaHHistory
    #print w.HHistory(initH)
    #H = calculateH(w.field,w.Hami[0],w.Hami[1])
    #print H
    a = w.MHistory(initM)
    b =  w.M
    aa = w.HHistory(initH)
    bb = w.H
    #print aa
    #print bb
    print a ==b
    error = 0.0
    for n in range(len(aa)):
        error += aa[n] + bb[n]
    if error >= 1:
        print "false"
    else:
        print "true"