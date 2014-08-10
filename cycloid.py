#!/usr/bin/python
#
# Cycloid gear generator
#
#
# Copyright 2014 Buddha Buck <blaisepascal@gmail.com>
#

import argparse, sys
from dxfwrite import DXFEngine as dxf
from math import *

from generators.cycloidgenerator import CycloidGenerator

# Parser configuration
parser = argparse.ArgumentParser(description="Generate cycloid gears",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

CycloidGenerator.add_options(parser)

# Parse arguments 
args = parser.parse_args()
generator = CycloidGenerator(args)

if (args.verbose):
    generator.verbose1()
    generator.verbose2()

# Let's draw this sucker
filename = "cycloid_gear_{}{}_{}.dxf".format(generator.module if generator.metric else generator.diametricpitch,
                                                     "mm" if generator.metric else "",
                                                     generator.teeth)

drawing = dxf.drawing(filename)

generator.generate_circles(drawing)
generator.generate_centers(drawing)
generator.generate_text(drawing)
generator.generate_teeth(drawing)

drawing.save()







        
