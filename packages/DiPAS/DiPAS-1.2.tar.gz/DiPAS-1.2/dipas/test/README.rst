Tests
=====

This folder contains unittests as well as benchmarks against the MADX program.
They can be run via ``python -m unittest discover``. The benchmarks contained in
``test_compute.py`` take about half an hour to complete.

.. note::

   The benchmarks in ``test_compute.py`` are set up to be run against the "intel"
   compiled version of MADX
   (e.g. `madx-linux64-intel <https://madx.web.cern.ch/madx/releases/last-rel/madx-linux64-intel>`_)
   and to be run also on Intel CPUs.
   If run against the "gnu" compiled version or on non-Intel CPUs, some tests might raise a
   ``UserWarning`` coming from MADX. Specifically the test
   ``TestSecondOrderClosedOrbitToyLatticeWithInactiveDipolesAndFieldErrorsNonZeroKickers.test_twiss_init_beta_alpha_mu``
   is known to fail under these conditions.
   This is because Intel CPUs use 80-bit floating point numbers when served with corresponding
   opcodes from the Intel compiler. The GNU compiled version uses the standard 64-bit floating point
   numbers. This is sometimes not sufficient to reach the required tolerance for the closed orbit search.
   A rather strict tolerance of ``1e-16`` has been chosen for the computation of sectormaps, since any deviation
   of the closed orbit, between the two programs DiPAS and MADX, at the beginning of the lattice will be amplified 
   during traversal of the lattice and consequentially leads to a noticeable deviation of sectormaps towards
   the end of the lattice. The strict tolerance of ``1e-16`` ensures that this deviation and hence its effect on
   sectormaps is negligible for all test lattices.


Customization
-------------

The ``DIPAS_TEST_COMPUTE_WDIR`` environment variable can be set to use a custom working directory
to contain the MADX reference data for each test case rather than to fallback on creating
temporary directories for that purpose.
