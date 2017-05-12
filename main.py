import numpy as np
import math
import random
from random import randint
import matplotlib.pyplot as plt
from general import createField,calculateH
from Metropolis import Metropolis

Metro_settingPath = './Metropolis_settings.txt'

def main():
    m = Metropolis(Metro_settingPath)
    f = createField(m.fieldSize,m.fieldInitMethod)
    m.init(f)
    print calculateH(m.field,m.Hami[0],m.Hami[1])
    m.run(10)
    print calculateH(m.field,m.Hami[0],m.Hami[1])


if __name__ == '__main__':
    main()