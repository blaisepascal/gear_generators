import argparse, dxfwrite
from geargenerator import GearGenerator
from dxfwrite import DXFEngine as dxf
from math import cos, sin, radians
from cmath import exp

def epicycloid_at(R,teeth,phi):
    k = 2*teeth
    r = R/k

    x = r*(k+1)*cos(phi) - r*cos((k+1)*phi)
    y = r*(k+1)*sin(phi) - r*sin((k+1)*phi)
    return x + y*1j

def hypocycloid_at(R, teeth, phi):
    k = 2*teeth
    r = R/k

    x = r*(k-1)*cos(phi) + r*cos((k-1)*phi)
    y = r*(k-1)*sin(phi) - r*sin((k-1)*phi)
    return x + y*1j
        
def rotated_by(phi):
    return exp(phi * 1j)

class CycloidGenerator(GearGenerator):
    'Generator for cycloid gears'

    def __init__(self, args):
        super(CycloidGenerator,self).__init__(args)
        
        self.r_cycloid = self.module/4 # I believe this is correct, it needs to be checked.
        self.r_outer = self.r_pitch + 2*self.r_cycloid
        self.r_root = self.r_pitch  - 2*self.r_cycloid

    def generate_text(self, drawing):
        textheight = self.module/2
        linespacing = self.module*1
    
        drawing.add(dxf.text("{} teeth".format(self.teeth),alignpoint=(0, linespacing/2),
                             height=textheight, halign=dxfwrite.CENTER, valign=dxfwrite.CENTER,
                             layer="geartext"))
        if self.metric:
            drawing.add(dxf.text("{}mm module".format(self.module), alignpoint=(0,-linespacing/2),
                                 height=textheight, halign=dxfwrite.CENTER, valign=dxfwrite.CENTER,
                                 layer="geartext"))
        else:
            drawing.add(dxf.text("{}/in Dp".format(self.diametricpitch), alignpoint=(0,-linespacing/2),
                                 height=textheight, halign=dxfwrite.CENTER, valign=dxfwrite.CENTER,
                                 layer="geartext"))
    
    def generate_tooth(self, tooth, drawing):

        # there are three segments to generate:
        # 1. hypocycloid from -phi_width/2 to -phi_width/4
        # 2. epicycloid from -phi_width/4 to phi_width/4
        # 3. hypocycloid from phi_width/4 to phi_width/2
        #
        # We will use 40 segments per tooth, each nominally phi_width/40 in side
        # this should be adjustable, depending on tooth count, but how, I don't know.

        # By default, epicycloid_at and hypocycloid_at touch the pitch circle at phi=0
        # we want them to touch at phi= +/- phi_width/4, so we need to keep that in mind.
        
        step = self.phi_width/40
        offset = - self.phi_width/4
        rotation = rotated_by(offset + tooth*self.phi_width)
        
        for i in range(-10,0):
            phi1 = i*step
            phi2 = (i+1)*step
            h1 = hypocycloid_at(self.r_pitch,self.teeth, phi1 ) * rotation
            h2 = hypocycloid_at(self.r_pitch,self.teeth, phi2 ) * rotation
            drawing.add(self.new_line(h1, h2))
        for i in range(0,20):
            phi1 = i*step
            phi2 = (i+1)*step
            e1 = epicycloid_at(self.r_pitch,self.teeth, phi1 ) * rotation
            e2 = epicycloid_at(self.r_pitch,self.teeth, phi2 ) * rotation
            drawing.add(self.new_line(e1, e2))
        for i in range(20,30):
            phi1 = i*step
            phi2 = (i+1)*step
            h1 = hypocycloid_at(self.r_pitch,self.teeth, phi1 ) * rotation
            h2 = hypocycloid_at(self.r_pitch,self.teeth, phi2 ) * rotation
            drawing.add(self.new_line(h1, h2))
        

        # offset = self.phi_width/4

        # hypo1 = [ hypocycloid_at(self.r_pitch, self.teeth, n*step-offset)
        #           for n in range(-20, -9)]
        # epi = [ epicycloid_at(self.r_pitch, self.teeth, n*step-offset)
        #         for n in range(-10, 11)]
        # hypo2 = [ p.conjugate() for p in hypo1 ]

        # for i in range(0,10):
        #     drawing.add(self.new_line(hypo1[i], hypo1[i+1], color= 3))
        # for i in range(0,20):
        #     drawing.add(self.new_line(epi[i], epi[i+1], color = 4))
        # for i in range(0,10):
        #     drawing.add(self.new_line(hypo2[i], hypo2[i+1], color = 5))
        
