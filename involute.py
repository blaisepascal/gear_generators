#!/usr/bin/python
#
# Involute gear generator
#
#
# Copyright 2014 Buddha Buck <blaisepascal@gmail.com>
#

import argparse, sys, dxfwrite
from dxfwrite import DXFEngine as dxf
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

# Parser configuration
parser = argparse.ArgumentParser(description="Generate involute gears",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument("-p", "--pressureangle", type=float, default=20, help="Pressure Angle of gear")

modulegroup = parser.add_mutually_exclusive_group(required=True)
modulegroup.add_argument("-m", "--module", type=float, help="Module of teeth (mm))")
modulegroup.add_argument("-dp", "--diametricpitch", type=float, help="Diametric pitch of teeth (1/in)")

sizegroup = parser.add_mutually_exclusive_group(required=True)
sizegroup.add_argument("-t", "--teeth", type=int, help="Number of teeth on gear")
sizegroup.add_argument("-d", "--diameter", type=float, help="Diameter of pitch circle")

parser.add_argument("-a", "--addendum", type=float, default=1.0, help="Addendum (in units of module)")
parser.add_argument("-dd", "--dedendum", type=float, default=1.25, help="Dedendum (in units of module)")

# Parse arguments 
args = parser.parse_args()

# Metric gears are specified by module, in mm
# Non-metric gears are specified by diametric pitch, in 1/in
# Other than metric/imperial, the two values are inverses of each other.
#
# By converting them to one measurement system, it makes the maths simpler
# and I can simply specify the unit system in the output.

metric = True
if args.module == None:
    args.module = 1/args.diametricpitch # module in inch
    metric = False
else:
    args.diametricpitch = 1/args.module # diametric pitch in 1/mm
    
if args.teeth == None:
    args.teeth = args.diameter * args.diametricpitch
else:
    args.diameter = args.teeth * args.module

assert float(args.teeth).is_integer(), "Teeth must be an integer, not {}".format(args.teeth)
args.teeth = int(args.teeth)    
    
unit = "mm" if metric else "in"
    
print "{} teeth".format(args.teeth)
print "{} pressure angle".format(args.pressureangle)
print "{}{} module".format(args.module, unit)
print "{}/{} diametric pitch".format(args.diametricpitch, unit)
print "{}{} diameter".format(args.diameter, unit)

r_pitch = args.diameter / 2
r_outer = r_pitch + args.module*args.addendum
r_root = r_pitch - args.module*args.dedendum
r_base = r_pitch * cos(radians(args.pressureangle))

# Don't want root greater than base, so make sure it's at least module/10 below
r_root = min(r_root, r_base - args.module/10)

print "{:6.3f}{} root radius, {:4.2f} modules".format(r_root, unit, (r_root - r_pitch)/args.module)
print "{:6.3f}{} base radius, {:4.2f} modules".format(r_base, unit, (r_base-r_pitch)/args.module)
print "{:6.3f}{} pitch radius".format(r_pitch, unit)
print "{:6.3f}{} outer radius, {:4.2f} modules".format(r_outer, unit, (r_outer-r_pitch)/args.module)

# Angular width of tooth shape is phi_width = 2 pi / number of teeth

phi_width = 2*pi / args.teeth

involute = Involute(r_base)

# center of tooth is at phi = 0,
# involute faces cross pitch-line at +/- phi_width/4, so involute start needs to take care of that.
# involute stops at outer circle

phi_at_pitch = involute.phi_at_r(r_pitch)
phi_at_outer = involute.phi_at_r(r_outer)
t_at_base = 0
t_at_outer = involute.t_at_r(r_outer)

phi_root_start     = phi_width/2
phi_involute_start = phi_width/4 + phi_at_pitch    
phi_involute_stop  = phi_involute_start - phi_at_outer

# Let's draw this sucker
filename = "involute_gear_{}{}_{}pa_{}.dxf".format(args.module if metric else args.diametricpitch,
                                           "mm" if metric else "",
                                          args.pressureangle,
                                          args.teeth)

drawing = dxf.drawing(filename)
segs = []

# circles
segs.append(dxf.circle(radius=r_outer, thickness=0, color=2, layer='gearcircles'))
segs.append(dxf.circle(radius=r_pitch, thickness=0, color=1, layer='gearcircles'))
segs.append(dxf.circle(radius=r_base , thickness=0, color=3, layer='gearcircles'))
segs.append(dxf.circle(radius=r_root , thickness=0, color=4, layer='gearcircles'))

# centers
segs.append(dxf.line(start=(0,-r_pitch), end=(0,r_pitch), thickness=0, color=5, layer='gearcenters'))
segs.append(dxf.line(start=(-r_pitch,0), end=(r_pitch,0), thickness=0, color=5, layer='gearcenters'))

# text
textheight = args.module/2
linespacing = args.module*1

segs.append(dxf.text("{} teeth".format(args.teeth),alignpoint=(0, linespacing),
                     height=textheight, halign=dxfwrite.CENTER, valign=dxfwrite.CENTER,
                     layer="geartext"))
segs.append(dxf.text("{} pressure angle".format(args.pressureangle),alignpoint=(0,0),
                     height=textheight, halign=dxfwrite.CENTER, valign=dxfwrite.CENTER,
                     layer="geartext"))
if metric:
    segs.append(dxf.text("{}mm module".format(args.module), alignpoint=(0,-linespacing),
                         height=textheight, halign=dxfwrite.CENTER, valign=dxfwrite.CENTER,
                         layer="geartext"))
else:
    segs.append(dxf.text("{}/in Dp".format(args.diametricalpitch), alignpoint=(0,-linespacing),
                         height=textheight, halign=dxfwrite.CENTER, valign=dxfwrite.CENTER,
                         layer="geartext"))

p1 = rect(r_root, phi_root_start)
p2 = rect(r_root, phi_involute_start)
p3 = rect(r_base, phi_involute_start)
p4 = rect(r_outer, phi_involute_stop)

# calculate involute points, 10 segments
t_per_segment = t_at_outer/10
offset = exp(phi_involute_start*1j)
involute_segments = [ involute.at(i*t_per_segment).conjugate()*offset for i in range(11)]
control_points = [p1,p2,p3,p4]
control_points = control_points + [ p.conjugate() for p in control_points[::-1]]

for i in range(args.teeth):
    rotate = exp(i*phi_width*1j)
    inv = [ p * rotate for p in involute_segments]
    inv2 = [ p.conjugate() * rotate for p in involute_segments]
    p = [ pt * rotate for pt in control_points]
    
    segs.append( dxf.arc(radius=abs(p[0]),
                         startangle=degrees(phase(p[1])),
                         endangle=degrees(phase(p[0])),
                         layer = "gearteeth", thickness=0.0))
    
    # 2. a radial line from the root circle to the base circle along phi_involute_start
    
    
    segs.append(dxf.line(start=(p[1].real, p[1].imag),
                         end=(p[2].real, p[2].imag),
                         layer = "gearteeth", thickness=0.0))
    
    # 3. An involute from the base circle to the outer circle, starting at phi_involute_start
    
    for i in range(10):
        segs.append(dxf.line(start = (inv[i].real, inv[i].imag),
                             end   = (inv[i+1].real, inv[i+1].imag),
                             layer="gearteeth", thickness=0.0))
        
    # 4. An arc along the outer circle from phi_involute_stop to -phi_involute_stop
    segs.append(dxf.arc(radius=abs(p[3]),
                        startangle=degrees(phase(p[4])),
                        endangle=degrees(phase(p[3])),
                        layer = "gearteeth", thickness=0.0))
    
    # 5. An involute, mirroring 3
    for i in range(10):
        segs.append(dxf.line(start = (inv2[i].real, inv2[i].imag),
                             end   = (inv2[i+1].real, inv2[i+1].imag),
                             layer="gearteeth", thickness=0.0))    
        
        
    # 6. A radial line, mirroring 2
    
    segs.append(dxf.line(start = (p[5].real, p[5].imag),
                         end   = (p[6].real, p[6].imag),
                         layer = "gearteeth", thickness=0.0))
    
    # 7. An arc mirroring 1
            
    segs.append(dxf.arc(radius=abs(p[6]),
                        startangle=degrees(phase(p[7])),
                        endangle=degrees(phase(p[6])),
                        layer = "gearteeth", thickness=0.0))
    

for l in segs:
    drawing.add(l)

drawing.save()







        
