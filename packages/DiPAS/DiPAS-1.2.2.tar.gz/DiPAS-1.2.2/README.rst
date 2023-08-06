.. image:: https://gitlab.com/Dominik1123/dipas/badges/develop/pipeline.svg
   :target: https://gitlab.com/Dominik1123/dipas/-/commits/master

.. image:: https://gitlab.com/Dominik1123/dipas/badges/develop/coverage.svg
   :target: https://gitlab.com/Dominik1123/dipas/-/commits/master

.. image:: https://img.shields.io/pypi/v/dipas.svg
   :target: https://pypi.org/project/DiPAS/


DiPAS
=====

DiPAS is a program for differentiable simulations of particle accelerators. It acts as a framework and thus
supports a wide range of use cases such as particle tracking or optics calculations such as closed
orbit search or computation of Twiss parameters.

The involved computations are backed by the `PyTorch <https://pytorch.org/>`__ package which also provides the relevant
functionality for differentiation of user-defined quantities as well as a variety of gradient-based optimizers that integrate
with the thus derived quantities.

The DiPAS package can parse MADX lattice definitions and hence allows for zero-overhead importing of existing lattices.
In addition it supports custom lattice definitions from provided element classes.


Relevant links
--------------

* `Documentation <https://dipas.readthedocs.io/>`__
* `Examples <https://gitlab.com/Dominik1123/dipas/blob/master/examples>`__
* `PyPI Project <https://pypi.org/project/dipas/>`__


Example usage
-------------

Minimizing loss along beamline by tuning quadrupoles:

.. code:: python

   import numpy
   from dipas.build import from_file
   from dipas.elements import Quadrupole
   import torch

   lattice = from_file('example.madx')

   for quad in lattice[Quadrupole]:
       quad.k1 = torch.nn.Parameter(quad.k1)

   optimizer = torch.optim.Adam(lattice.parameters(), lr=1e-3)

   particles = torch.from_numpy(numpy.load('particles.npy'))

   while True:
       tracked, loss_val = lattice.linear(particles, recloss='sum')
       lost = 1 - tracked.shape[1] / particles.shape[1]
       if lost < 0.01:  # Fraction of particles lost less than 1%.
           break
       optimizer.zero_grad()
       loss_val.backward()
       optimizer.step()
