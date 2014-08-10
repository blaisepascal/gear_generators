import argparse, dxfwrite
from geargenerator import GearGenerator
from dxfwrite import DXFEngine as dxf
from math import cos, radians, sin
from inv import Involute
from cmath import rect, exp, phase

class InvoluteGenerator(GearGenerator):
    'Generator for external involute gears'
    def __init__(self,args):
        super(InvoluteGenerator,self).__init__(args);

        pressureangle = args.pressureangle
        addendum = args.addendum
        dedendum = args.dedendum

        r_base = self.r_pitch * cos(radians(pressureangle))

        if args.internal:
            r_addendum = self.r_pitch - addendum * self.module
            r_dedendum = self.r_pitch + dedendum * self.module
            backlash = - args.backlash * (25.4 if self.metric else 1) / 2
        else:
            r_addendum = self.r_pitch + addendum * self.module
            r_dedendum = self.r_pitch - dedendum * self.module
            backlash = args.backlash * (25.4 if self.metric else 1) / 2

        r_outer = max(r_addendum, r_dedendum)
        r_root = min(r_addendum, r_dedendum)    
        r_inner = max(r_root, r_base) # where the involute starts

        self.involute = Involute(r_base)

        self.r_outer = r_outer
        self.r_inner = r_inner
        self.r_base = r_base
        self.r_root = r_root
        self.backlash = backlash
        self.pressureangle = pressureangle

    def involute_points(self):
        # Involute tooth shape geometry.
        # tooth shape extends from -phi_width/2 to +phi_width/2 in angular measure
        # involute crosses pitch circle at -/+ phi_width/4, so involute needs to be offset
        #    to make this so

        backlash_offset = self.backlash * (1/sin(self.pressureangle)) / self.r_pitch
        
        
        involute_phi_at_pitch = self.involute.phi_at_r(self.r_pitch)        
        involute_phi_offset = -self.phi_width/4 - involute_phi_at_pitch + backlash_offset
        offset = exp(involute_phi_offset*1j)

        # calculate involute points, 10 segments
        t_at_outer = self.involute.t_at_r(self.r_outer)
        t_at_inner = self.involute.t_at_r(self.r_inner)
        t_per_segment = (t_at_outer-t_at_inner)/10
        involute_points = [ self.involute.at(t_at_inner+i*t_per_segment)*offset for i in range(11)]

        return involute_points

    def verbose1(self):
        super(InvoluteGenerator,self).verbose1()
        print "{} pressure angle".format(self.pressureangle)

    def verbose2(self):
        super(InvoluteGenerator,self).verbose2()
        print "{:6.3f}{} base radius, {:4.2f} modules".format(self.r_base, self.unit,
                                                              (self.r_base-self.r_pitch)/self.module)
        
    @staticmethod
    def add_options(parser):
        GearGenerator.add_options(parser)

        parser.add_argument("-p", "--pressureangle", type=float, default=20,
                            help="Pressure Angle of gear")
        parser.add_argument("-a", "--addendum", type=float, default=1.0,
                            help="Addendum (in units of module)")
        parser.add_argument("-dd", "--dedendum", type=float, default=1.25,
                            help="Dedendum (in units of module)")
        parser.add_argument("-i", "--internal", action="store_true",
                            help="internal gear")
        parser.add_argument("-b", "--backlash", type=float, default=0.008,
                            help="Backlash (in)")
        

    def generate_circles(self, drawing):
        super(InvoluteGenerator,self).generate_circles(drawing)
        drawing.add(self.new_circle(0,self.r_base, color=3))
        drawing.add(self.new_circle(0,self.r_inner, color=4))

        drawing.add(self.new_circle(rect(self.r_pitch, self.phi_width/4), self.backlash, color=1))

    def generate_text(self, drawing):
        textheight = self.module/2
        linespacing = self.module*1
    
        drawing.add(dxf.text("{} teeth".format(self.teeth),alignpoint=(0, linespacing),
                             height=textheight, halign=dxfwrite.CENTER, valign=dxfwrite.CENTER,
                             layer="geartext"))
        drawing.add(dxf.text("{} pressure angle".format(self.pressureangle),alignpoint=(0,0),
                             height=textheight, halign=dxfwrite.CENTER, valign=dxfwrite.CENTER,
                             layer="geartext"))
        if self.metric:
            drawing.add(dxf.text("{}mm module".format(self.module), alignpoint=(0,-linespacing),
                                 height=textheight, halign=dxfwrite.CENTER, valign=dxfwrite.CENTER,
                                 layer="geartext"))
        else:
            drawing.add(dxf.text("{}/in Dp".format(self.diametricpitch), alignpoint=(0,-linespacing),
                                 height=textheight, halign=dxfwrite.CENTER, valign=dxfwrite.CENTER,
                                 layer="geartext"))

    def generate_tooth(self, tooth, drawing):

        involute_segments = self.involute_points()
        involute_start = involute_segments[0]
        involute_end = involute_segments[-1]
        
        # general setup
        p1 = rect(self.r_root, -self.phi_width/2)       # point where root starts
        p2 = rect(self.r_root, phase(involute_start))   # point where flank starts
        p3 = involute_start   # point where involute starts
        p4 = involute_end
        
        half_control_points = [p1,p2,p3,p4]
        mirrored_control_points = [ p.conjugate() for p in half_control_points[::-1]]
        control_points = half_control_points + mirrored_control_points    
        
        # per tooth
        rotate = exp(tooth*self.phi_width*1j)
        inv = [ p * rotate for p in involute_segments]
        inv2 = [ p.conjugate() * rotate for p in involute_segments]
        p = [ pt * rotate for pt in control_points]

        drawing.add( self.new_arc(p[0], p[1]))
        drawing.add( self.new_line(p[1], p[2]))
        for i in range(10):
            drawing.add(self.new_line(inv[i], inv[i+1]))
        drawing.add(self.new_arc(p[3],p[4]))
        for i in range(10):
            drawing.add(self.new_line(inv2[i], inv2[i+1]))
        drawing.add(self.new_line(p[5],p[6]))
        drawing.add(self.new_arc(p[6],p[7]))
        
