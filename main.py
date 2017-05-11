from setting import Settings
import numpy as np
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
    i = []
    j = []
    for _ in range(times):
        i.append(randint(0,size[0]-1))
        j.append(randint(0,size[1]-1))
    return i,j

def calculateH(image, B, J):
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

def calculateDeltaH(x,y,J,B,image):
    deltaHb = 0.0
    deltaHj = 0.0
    changes = []
    shape = image.shape
    for n in range(len(x)):
        changes.append((x[n],y[n]))
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
    print -deltaHj
    print deltaHb
    return -deltaHj + deltaHb

def main():
    settings = Settings(settingPath)
    fieldSize = settings.getValue('size')
    field = createField(fieldSize,settings.getValue('init'))
    print field
    Hami = settings.getValue('hamiltonian')
    initH = calculateH(field,Hami[1],Hami[0])
    print initH
    flipTimes = settings.getValue('flipTimes')
    #i,j = createChange(fieldSize,flipTimes)
    i = [0,0]
    j = [0,1]
    for n in range(len(i)):
        field[i[n],j[n]] = -field[i[n],j[n]]
    print field
    deltaH = calculateDeltaH(i,j,Hami[0],Hami[1],field)
    print deltaH
    print calculateH(field,Hami[1],Hami[0])
if __name__ == '__main__':
    main()