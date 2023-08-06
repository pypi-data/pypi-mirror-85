# Transfer Line Quadrupole Tuning

The goal of this example is to show how to set up a multi-objective optimization of lattice parameters using the example
of tuning quadrupole gradient strengths on a beamline. The particle distribution at the entrance is used as an input and
the strengths of 21 quadrupoles along the beamline are varied during the optimization in order to achieve the following
optimization targets:

* Small beam spot size at target position,
* Smaller than aperture beam spot size at beam dump location,
* Small beam loss along the beamline.

A detailed explanation of the setup can be found in the [walkthrough](./walkthrough.ipynb) and a complete example script
is available at [main.py](./main.py).
