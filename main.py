import numpy as np
import math
import random
from random import randint
import matplotlib.pyplot as plt
from general import createField,calculateH
from Metropolis import Metropolis

generalSettingPath = './general_settings.txt'
MetroSettingPath = './Metropolis_settings.txt'
WofflSettingPath = './Woffl_settings.txt'

def main():
    m = Metropolis(MetroSettingPath)
    f = createField(m.fieldSize,m.fieldInitMethod)
    plt.matshow(f)
    m.init(f)
    print calculateH(m.field,m.Hami[0],m.Hami[1])
    m.run(m.maxIter)
    print calculateH(m.field,m.Hami[0],m.Hami[1])
    plt.matshow(m.field)
    plt.show()

if __name__ == '__main__':
    main()