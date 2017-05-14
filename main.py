import numpy as np
import math
import random
from random import randint
import matplotlib.pyplot as plt
from general import createField,calculateH,calculateM
from Metropolis import Metropolis
from Woffl import Woffl

generalSettingPath = './general_settings.txt'
MetroSettingPath = './Metropolis_settings.txt'
WofflSettingPath = './Woffl_settings.txt'

def main():

    print "using Metropolis method"
    m = Metropolis(MetroSettingPath)
    fm = createField(m.fieldSize,m.fieldInitMethod)
#    plt.matshow(f)
    m.init(fm)
    initHm = calculateH(m.field,m.Hami[0],m.Hami[1])
    initMm = calculateM(m.field)
    #m.run(m.maxIter)
    #plt.plot(m.HHistory(initH))
    plt.figure()
    plt.plot(m.MHistory(initMm))
    plt.ylabel('M')
    plt.xlabel('iterations')
    plt.title('Metropolis')

    print "using Woffl method"
    w = Woffl(WofflSettingPath)
    fw = createField(w.fieldSize,w.fieldInitMethod)
    w.init(fw)
    initHw = calculateH(w.field,w.Hami[0],w.Hami[1])
    initMw = calculateM(w.field)
    w.run(w.maxIter)
    plt.figure()
    plt.plot(w.MHistory(initMm))
    plt.ylabel('M')
    plt.xlabel('iterations')
    plt.title('Woffl')
    plt.show()


if __name__ == '__main__':
    main()