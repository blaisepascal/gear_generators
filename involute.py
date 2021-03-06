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

from generators.involutegenerator import InvoluteGenerator

# Parser configuration
parser = argparse.ArgumentParser(description="Generate involute gears",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

InvoluteGenerator.add_options(parser)

# Parse arguments 
args = parser.parse_args()
generator = InvoluteGenerator(args)

if (args.verbose):
    generator.verbose1()
    generator.verbose2()

# Let's draw this sucker
filename = "involute_gear_{}{}_{}pa_{}{}.dxf".format(generator.module if generator.metric else generator.diametricpitch,
                                                     "mm" if generator.metric else "",
                                                     generator.pressureangle,
                                                     generator.teeth,
                                                     "i" if args.internal else "")

drawing = dxf.drawing(filename)

generator.generate_circles(drawing)
generator.generate_centers(drawing)
generator.generate_text(drawing)
generator.generate_teeth(drawing)

drawing.save()







        
