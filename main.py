from setting import Settings
import numpy as np

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

def calculateH(image, b, j):
    Hj = 0.0
    Hb = 0.0
    shape = image.shape
    for i in range(shape[0]):
        for j in range(shape[1]):
            Hb += -b*image[i,j]
            if i-1>=0:
                Hj += -j*image[i,j]*image[i-1,j]
            if i+1<shape[0]:
                Hj += -j*image[i,j]*image[i+1,j]
            if j-1>=0:
                Hj += -j*image[i,j]*image[i,j-1]
            if j+1<shape[1]:
                Hj += -j*image[i,j]*image[i,j+1]
    H = Hb + Hj/2
    return H

def calculateDeltaH():
    pass

def main():
    settings = Settings(settingPath)
    fieldSize = settings.getValue('size')
    field = createField(fieldSize,settings.getValue('init'))
    Hami = settings.getValue('hamiltonian')
    initH = calculateH(field,Hami[1],Hami[0])
    

if __name__ == '__main__':
    main()