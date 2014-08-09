gear_generators
===============

Programs to generate generate DXF files of gears

Ultimately, all programs will allow you to specify the
module/diametrical pitch and the number of teeth/gear diameter, as
well as other parameters specific to the gear.

Plans include tools to generate gears with involute and cycloid tooth
profiles.

The output DXF files have three layers:
* gearteeth -- the outline of the tooth itself (in white/black)
* gearcircles -- the circles that define the gear. This includes at
least the root, pitch, and outer circles.
* gearcenters -- Two crossed pitch circle diameters, to identify the
center
* geartext -- A layer of gear identification text, including tooth
  count/gear diameter, module/diametrical pitch, and other necessary 

involute
--------

Generates external involute spur gears
Output file name is of form "involute_gear_8_14.2_80.dxf" for an 80-tooth gear with
8/in diametrical pitch and a 14.2 degree pressure angle.


    usage: involute.py [-h] [-p PRESSUREANGLE] (-m MODULE | -dp DIAMETRICPITCH)
                       (-t TEETH | -d DIAMETER) [-a ADDENDUM] [-dd DEDENDUM]
    
    Generate involute gears
    
    optional arguments:
      -h, --help            show this help message and exit
      -p PRESSUREANGLE, --pressureangle PRESSUREANGLE
                            Pressure Angle of gear (default: 20)
      -m MODULE, --module MODULE
                            Module of teeth (mm)) (default: None)
      -dp DIAMETRICPITCH, --diametricpitch DIAMETRICPITCH
                            Diametric pitch of teeth (1/in) (default: None)
      -t TEETH, --teeth TEETH
                            Number of teeth on gear (default: None)
      -d DIAMETER, --diameter DIAMETER
                            Diameter of pitch circle (default: None)
      -a ADDENDUM, --addendum ADDENDUM
                            Addendum (in units of module) (default: 1.0)
      -dd DEDENDUM, --dedendum DEDENDUM
                            Dedendum (in units of module) (default: 1.25)

