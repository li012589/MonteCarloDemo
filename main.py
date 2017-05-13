import numpy as np
import math
import random
from random import randint
import matplotlib.pyplot as plt
from general import createField,calculateH,calculateM
from Metropolis import Metropolis

generalSettingPath = './general_settings.txt'
MetroSettingPath = './Metropolis_settings.txt'
WofflSettingPath = './Woffl_settings.txt'

def main():
    m = Metropolis(MetroSettingPath)
    f = createField(m.fieldSize,m.fieldInitMethod)
#    plt.matshow(f)
    m.init(f)
    initH = calculateH(m.field,m.Hami[0],m.Hami[1])
    initM = calculateM(m.field)
    m.run(m.maxIter)
    #plt.plot(m.HHistory(initH))
    plt.plot(m.MHistory(initM))
    plt.show()


if __name__ == '__main__':
    main()