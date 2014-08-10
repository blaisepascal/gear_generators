gear_generators
===============

Programs to generate generate DXF files of gears

Ultimately, all programs will allow you to specify the
module/diametrical pitch and the number of teeth/gear diameter, as
well as other parameters specific to the gear.

Plans include tools to generate gears with involute and cycloid tooth
profiles.

The output DXF files have four layers:
* gearteeth -- the outline of the tooth itself (in white/black)
* gearcircles -- the circles that define the gear. This includes at
least the root, pitch, and outer circles.
* gearcenters -- Two crossed pitch circle diameters, to identify the
center
* geartext -- A layer of gear identification text, including tooth
  count/gear diameter, module/diametrical pitch, and other necessary 

involute
--------

Generates involute spur gears

Inputs are
* Module (mm) or diametrical pitch (1/in) (determines if metric or US units)
* Teeth count or diameter
* Pressure Angle
* Backlash allowance
* Addendum and Dedendum amounts (in terms of the module)
* Rotation of the gear form, to allow clean drawings of meshing teeth.

Output file name is of form "involute_gear_8_14.2_80.dxf" for an 80-tooth gear with
8/in diametrical pitch and a 14.2 degree pressure angle.

cycloid
-------

Generates cycloidal gears (as in a Root's Blower, not as in a clock)

* Module (mm) or diametrical pitch (1/in) (determines if metric or US units)
* Teeth count or diameter
* Rotation of the gear form, to allow clean drawings of meshing teeth.

Output file name is of form "cycloid_gear_8_80.dxf" for an 80-tooth gear with 8/in diametrical pitch

