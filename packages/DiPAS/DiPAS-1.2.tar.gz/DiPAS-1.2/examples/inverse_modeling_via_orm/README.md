# Inverse Modeling of Quadrupole Gradient Errors by Matching the Orbit Response Matrix

The goal of this example is to show how to setup inverse modeling (i.e. inference of model parameters) by comparison with reference measurements.
For the scope of this example the reference measurement is provided by a corresponding MADX simulation.
Each of the six quadrupole triplets is assigned a gradient error and the goal of the algorithm is to find these gradient errors.
This is achieved by matching the simulated Orbit Response Matrix as well as the tunes to the reference measurements
by varying the quadrupole gradient errors of the simulation model.

A detailed description of the setup and corresponding results can be found in the [walkthrough](./walkthrough.html).
