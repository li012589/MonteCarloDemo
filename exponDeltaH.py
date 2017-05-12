import math

class exponDeltaH:
    def __init__(self,d):
        self.dic = d
    def calculate(self,delta,T):
        if delta in self.dic:
            return self.dic[delta]
        else:
            self.dic[delta]  = math.exp(-delta/T)
            return self.dic[delta]