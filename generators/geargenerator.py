import argparse, dxfwrite
from dxfwrite import DXFEngine as dxf
from math import pi, degrees
from cmath import phase

class GearGenerator(object):
    'Generator for a gear superclass'
    
    # Generator for a gear.
    #
    # all gears have a tooth count, diameter, module, and diametric pitch
    # we are assuming we are being passed an argparse object

    def __init__(self,args):
        self.teeth = args.teeth
        self.diameter = args.diameter
        self.module = args.module
        self.diametricpitch = args.diametricpitch

        # module and diametric pitch are metric/US ways of specifying the tooth size    
        if self.module == None:
            self.diametricpitch = args.diametricpitch
            self.module = 1/self.diametricpitch # module in inch
            self.metric = False
            self.unit="in"
        else:
            args.diametricpitch = 1/args.module # diametric pitch in 1/mm
            self.module = args.module
            self.diametricpitch = args.diametricpitch
            self.metric = True
            self.unit="in"

        # tooth count and diameter are two ways of specifying the gear size (given a module/Dp)
        if self.teeth == None:
            self.teeth = self.diameter * self.diametricpitch
        else:
            self.diameter = self.teeth * self.module
            
        assert float(self.teeth).is_integer(), "Teeth must be an integer, not {}".format(self.teeth)
        self.teeth = int(self.teeth)
        self.phi_width = 2*pi/self.teeth
        self.r_pitch = self.diameter / 2

    def verbose1(self):
        print "{} teeth".format(self.teeth)
        print "{}{} module".format(self.module, self.unit)
        print "{}/{} diametric pitch".format(self.diametricpitch, self.unit)
        print "{}{} diameter".format(self.diameter, self.unit)
        
    def verbose2(self):
        print "{:6.3f}{} root radius, {:4.2f} modules".format(self.r_root, self.unit,
                                                              (self.r_root - self.r_pitch)/self.module)
        print "{:6.3f}{} pitch radius".format(self.r_pitch, self.unit)
        print "{:6.3f}{} outer radius, {:4.2f} modules".format(self.r_outer, self.unit,
                                                               (self.r_outer-self.r_pitch)/self.module)
            
    @staticmethod
    def add_options(parser):
        modulegroup = parser.add_mutually_exclusive_group(required=True)
        modulegroup.add_argument("-m", "--module", type=float, help="Module of teeth (mm))")
        modulegroup.add_argument("-dp", "--diametricpitch", type=float,
                                 help="Diametric pitch of teeth (1/in)")
            
        sizegroup = parser.add_mutually_exclusive_group(required=True)
        sizegroup.add_argument("-t", "--teeth", type=int, help="Number of teeth on gear")
        sizegroup.add_argument("-d", "--diameter", type=float, help="Diameter of pitch circle")

        parser.add_argument("-v", "--verbose", action="store_true",
                           help="Print details of gear generated")

    # tools for creating DXF lines, arcs, circles, etc
    def new_line(self, s, e, layer='gearteeth', color = 0):
        return dxf.line(start=(s.real, s.imag),
                        end=(e.real, e.imag),
                        layer = layer, thickness=0.0, color = color)

    def new_circle(self, c, r, layer = 'gearcircles', color = 0):
        return dxf.circle(center=(c.real, c.imag), radius=r,
                          layer = layer, color = color, thickness=0)
        
    def new_arc(self, s, e, layer='gearteeth', r=None, color = 0):
        if r == None:
            r = abs(s)    
        sa = phase(s)
        ea = phase(e)
        return dxf.arc(radius = r,
                       startangle=degrees(sa),
                       endangle=degrees(ea),
                       layer = layer, thickness=0.0)

    def generate_teeth(self, drawing):
        for tooth in range(self.teeth):
            self.generate_tooth(tooth, drawing)
    
    def generate_tooth(self, tooth, drawing):
        pass
    
    def generate_circles(self, drawing):
        segs = []
        segs.append(self.new_circle(0,self.r_outer, color=2))
        segs.append(self.new_circle(0,self.r_pitch, color=1))
        segs.append(self.new_circle(0,self.r_root, color=4))
        for s in segs:
            drawing.add(s)

    def generate_centers(self, drawing):
        drawing.add(self.new_line(-self.r_pitch, self.r_pitch, layer="gearcenters", color= 5))
        drawing.add(self.new_line(-1j*self.r_pitch, 1j*self.r_pitch, layer="gearcenters", color= 5))
        
    def generate_text(self, drawing):
        pass    
