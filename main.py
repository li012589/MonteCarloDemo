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
    m.run(m.maxIter)
    #plt.plot(m.HHistory(initH))
    plt.figure()
    Mm = m.MHistory(initMm)
    plt.plot(Mm)
    plt.ylabel('M')
    plt.xlabel('iterations')
    plt.title(r'Metropolis $\beta=$1/'+str(m.t))
    print "the mean M is " + str(sum(Mm)/len(Mm))
    plt.figure()
    plt.plot(m.HHistory(initHm))
    plt.ylabel('H')
    plt.xlabel('iterations')
    plt.title(r'Metropolis $\beta=$1/'+str(m.t))

    print "using Woffl method"
    w = Woffl(WofflSettingPath)
    fw = createField(w.fieldSize,w.fieldInitMethod)
    #plt.matshow(fw)
    w.init(fw)
    initHw = calculateH(w.field,w.Hami[0],w.Hami[1])
    initMw = calculateM(w.field)
    w.run(w.maxIter)
    plt.figure()
    plt.plot(w.HHistory(initHw))
    plt.ylabel('H')
    plt.xlabel('iterations')
    plt.title(r'Woffl $\beta=$1/'+str(w.t))

    plt.figure()
    Mw = w.MHistory(initMw)
    plt.plot(Mw)
    print "the mean M is " + str(sum(Mw)/len(Mw))
    plt.ylabel('M')
    plt.xlabel('iterations')
    plt.title(r'Woffl $\beta=$1/'+str(w.t))
    #plt.matshow(w.field)
    plt.show()


if __name__ == '__main__':
    main()