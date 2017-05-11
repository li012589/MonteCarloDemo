from setting import Settings
import numpy as np
import math
import random
from random import randint
import matplotlib.pyplot as plt

settingPath = './settings.txt'

def createField(size, method):
    if method != -1:
        tmp = np.empty(tuple(size))
        tmp[:] = method
        return tmp
    else:
        tmp = np.random.random(tuple(size))
        tmp[tmp<0.5] = -1
        tmp[tmp>=0.5] = 1
        return tmp

def createChange(size,times):
    changes = []
    for _ in range(times):
        i=randint(0,size[0]-1)
        j=randint(0,size[1]-1)
        if (i,j) in changes:
            changes.remove((i,j))
        else:
            changes.append((i,j))
    return changes

def calculateH(image, J, B):
    Hj = 0.0
    Hb = 0.0
    shape = image.shape
    for i in range(shape[0]):
        for j in range(shape[1]):
            Hb += -B*image[i,j]
            if i-1>=0:
                Hj += -J*image[i,j]*image[i-1,j]
            if i+1<shape[0]:
                Hj += -J*image[i,j]*image[i+1,j]
            if j-1>=0:
                Hj += -J*image[i,j]*image[i,j-1]
            if j+1<shape[1]:
                Hj += -J*image[i,j]*image[i,j+1]
    H = Hb + Hj/2
    return H

def calculateDeltaH(changes,J,B,image):
    deltaHb = 0.0
    deltaHj = 0.0
    shape = image.shape
    for n in range(len(changes)):
        i = changes[n][0]
        j = changes[n][1]
        deltaHb += -2*image[i,j]*B
        if i-1>=0 :
            if not (i-1,j) in changes:
                deltaHj += -J*-image[i,j]*image[i-1,j]+J*image[i,j]*image[i-1,j]
            else:
                deltaHj += -J*-image[i,j]*-image[i-1,j]+J*image[i,j]*image[i-1,j]
        if i+1<shape[0]:
            if not (i+1,j) in changes:
                deltaHj += -J*-image[i,j]*image[i+1,j]+J*image[i,j]*image[i+1,j]
            else:
                deltaHj += -J*-image[i,j]*-image[i+1,j]+J*image[i,j]*image[i+1,j]
        if j-1>=0:
            if not (i,j-1) in changes:
                deltaHj += -J*-image[i,j]*image[i,j-1]+J*image[i,j]*image[i,j-1]
            else:
                deltaHj += -J*-image[i,j]*-image[i,j-1]+J*image[i,j]*image[i,j-1]
        if j+1<shape[1]:
            if not (i,j+1) in changes:
                deltaHj += -J*-image[i,j]*image[i,j+1]+J*image[i,j]*image[i,j+1]
            else:
                deltaHj += -J*-image[i,j]*-image[i,j+1]+J*image[i,j]*image[i,j+1]
    return -deltaHj + deltaHb

def calculateListofDelta(flipTimes, J, B, T):
    exponDeltaH = {}
    possibileDeltaH = []
    maxJ = 2*4*flipTimes
    maxB = 2*flipTimes
    for j in range(maxJ+1):
        for b in range(maxB+1):
            possibileDeltaH.append(j*J+b*B)
    for delta in possibileDeltaH:
        exponDeltaH[delta] = math.exp(-delta/T)
    return exponDeltaH

def changeField(changes,image):
    for n in range(len(changes)):
        i = changes[n][0]
        j = changes[n][1]
        image[i,j] = -image[i,j]
    return image

class exponDeltaH:
    def __init__(self,d):
        self.dic = d
    def calculate(self,delta,T):
        if delta in self.dic:
            return self.dic[delta]
        else:
            self.dic[delta]  = math.exp(-delta/T)
            return self.dic[delta]

def Metropolis(iteration,field,fieldSize,flipTimes,Hami,t):
    exponDeltaHList = exponDeltaH({})
    for n in range(iteration):
        changes = createChange(fieldSize,flipTimes)
        #print changes
        newField = changeField(changes,field)
        #print field
        deltaH = calculateDeltaH(changes,Hami[0],Hami[1],field)
        #print deltaH
        if deltaH <= 0:
            field = newField
            print 'Accepted!'
        else:
            if random.random() <= exponDeltaHList.calculate(deltaH,t):
                print 'Accepted with high H!'
                field = newField
            else:
                print 'Rejected'
                pass
    return field

def main():
    settings = Settings(settingPath)
    fieldSize = settings.getValue('size')
    field = createField(fieldSize,settings.getValue('init'))
    t = settings.getValue('temperture')
    plt.matshow(field)
    #print field
    Hami = settings.getValue('hamiltonian')
    initH = calculateH(field,Hami[0],Hami[1])
    #print initH
    flipTimes = settings.getValue('flipTimes')
    random.seed(settings.getValue('randomSeed'))
    maxTter = settings.getValue('maxIter')

    field = Metropolis(maxTter,field,fieldSize,flipTimes,Hami,t)

    plt.matshow(field)
    plt.show()
    #print calculateH(field,Hami[0],Hami[1])


if __name__ == '__main__':
    main()