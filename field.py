import numpy as np

class Field(np.ndarray):
    def __init__(self,size,method):
        print size
        print method
        if method != -1:
            self = np.empty(tuple(size))
            self[:] = method
            self = tmp
        else:
            self = np.random.random(tuple(size))
            self[tmp<0.5] = -1
            self[tmp>=0.5] = 1
            self = tmp
    def Hamiltonian(self,J,B):
        Hj = 0.0
        Hb = 0.0
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                Hb += -B*self[i,j]
                if i-1>=0:
                    Hj += -J*self[i,j]*self[i-1,j]
                if i+1<self.shape[0]:
                    Hj += -J*self[i,j]*self[i+1,j]
                if j-1>=0:
                    Hj += -J*self[i,j]*self[i,j-1]
                if j+1<self.shape[1]:
                    Hj += -J*self[i,j]*self[i,j+1]
        self.H = Hb + Hj/2
        return self.H

if __name__ == '__main__':
    f = Field([3,3],1)
    print f
    