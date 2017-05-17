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
    x = []
    c = []
    T = [float(t)/100 for t in range(214,240)]
    for t in T:
        c.append(0)
        x.append(0)
    N = 10*10
    for _ in range(10):
        for n in range(len(T)):
            t = T[n]
            m = Metropolis(MetroSettingPath)
            f = createField(m.fieldSize,m.fieldInitMethod)
            m.init_t(f,t)
            #print m.t
            initH = calculateH(m.field,m.Hami[0],m.Hami[1])
            initM = calculateM(m.field)
            m.run(m.maxIter)
            M = m.MHistory(initM)
            H = m.HHistory(initH)
            M2 = [m**2 for m in M]
            H2 = [h**2 for h in H]
            Mmean = sum(M)/len(M)
            Hmean = sum(H)/len(H)
            M2mean = sum(M2)/len(M2)
            H2mean = sum(H2)/len(H2)
            c[n] += ((H2mean - Hmean**2)*1/(t**2*N))
            x[n] += ((1/(t*N))*(M2mean - Mmean**2))
    #print c
    #print x
    c = [i/10 for i in c]
    x = [i/10 for i in x]
    plt.figure()
    plt.plot(T,c)
    plt.ylabel('c')
    plt.xlabel('t')
    plt.figure()
    plt.plot(T,x)
    plt.ylabel('x')
    plt.xlabel('t')
    plt.show()
if __name__ == '__main__':
    main()