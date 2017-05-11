from setting import Settings
import numpy as np
import math
from random import randint

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

def calculateListofDelta(flipTimes, J, B):
    exponDeltaH = {}
    possibileDeltaH = (n for n in range(4*flipTimes))
    for delta in possibileDeltaH:
        exponDeltaH[delta] = math.exp(delta)
    return exponDeltaH

def main():
    settings = Settings(settingPath)
    fieldSize = settings.getValue('size')
    field = createField(fieldSize,settings.getValue('init'))
    #print field
    Hami = settings.getValue('hamiltonian')
    initH = calculateH(field,Hami[0],Hami[1])
    print initH
    flipTimes = settings.getValue('flipTimes')
    exponDeltaH = calculateListofDelta(flipTimes,Hami[0],Hami[1])
    print exponDeltaH
    changes = createChange(fieldSize,flipTimes)
    print changes
    #i = [0,0]
    #j = [0,1]
    for n in range(len(changes)):
        i = changes[n][0]
        j = changes[n][1]
        field[i,j] = -field[i,j]
    print field
    deltaH = calculateDeltaH(changes,Hami[0],Hami[1],field)
    print deltaH
    print calculateH(field,Hami[0],Hami[1])
    if deltaH in exponDeltaH:
        print exponDeltaH[deltaH]
if __name__ == '__main__':
    main()