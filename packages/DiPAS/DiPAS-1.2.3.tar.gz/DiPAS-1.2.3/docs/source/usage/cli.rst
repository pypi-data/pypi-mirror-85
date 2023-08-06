Command line interface
----------------------

The DiPAS distribution contains a command line interface which can be used to invoke various functionalities:

* Compute Twiss/lattice parameters: ``dipas twiss path/to/script.madx``
* Compute Orbit Response Matrix (ORM): ``dipas orm path/to/script.madx``.
* Plot lattice: ``dipas plot path/to/script.madx``
* Dipas also supports invoking MADX to compute various quantities:
  * MADX: compute Twiss: ``dipas madx twiss path/to/script.madx``
  * MADX: compute ORM: ``dipas madx orm path/to/script.madx``

Each of the commands supports a variety of options for customization which can be displayed by using ``--help``
(e.g. ``dipas twiss --help``).

In addition to the above, DiPAS offers the following command utilities:

* Convert a lattice to HTML which can be viewed in the browser: ``madx-to-html path/to/script.madx outfile.html``
* Compute the complete set of beam parameters from user input: ``print-beam`` (e.g. ``print-beam --particle=proton --energy=1.4``)
