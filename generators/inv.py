from math import *
from cmath import phase, rect, exp

class Involute:
    'Basic maths about involutes of a circle (of radius base_radius)'

    def __init__(self, radius):
        self.base_radius = radius

    # Involutes are parameterized by an angle parameter t. To get the
    # point on the involute (of the unit circle) corresponding to t,
    # follow a radius of the unit circle at angle t, then follow a tangent
    # at that point for distance t.

    def at(self, t):
        return rect(self.r(t), self.phi(t))
    
    def r(self,t):
        return self.base_radius*sqrt(1+t*t)

    def phi(self,t):
        return t - atan(t)

    # r and phi are increasing functions of t, and sometimes the inverses are helpful
    def t_at_r(self,r):
        norm_r = r/self.base_radius
        return sqrt(norm_r*norm_r-1)

    # It's also useful to find the phi when the involute is of a particular r
    def phi_at_r(self,r):
        return self.phi(self.t_at_r(r))

