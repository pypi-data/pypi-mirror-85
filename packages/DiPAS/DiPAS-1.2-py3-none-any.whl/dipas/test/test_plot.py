from importlib import resources
import unittest
import warnings

import matplotlib.pyplot as plt

from dipas.build import from_file
from dipas.compute import InitialLatticeParameters, twiss
from dipas.elements import Kicker
from dipas.plot import plot_twiss
import dipas.test.sequences


def _load_sequence(sequence):
    with resources.path('dipas.test.sequences', f'{sequence}.seq') as path:
        return from_file(str(path)).makethin({Kicker: 2})


class TestPlotTwiss(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        warnings.simplefilter('ignore')

    def test_cryring(self):
        self._test(_load_sequence('cryring'))

    def test_hades(self):
        seq = _load_sequence('hades')
        beta0 = InitialLatticeParameters(
            beta_x=17.35, alpha_x=-1.65, beta_y=6.24, alpha_y=0.044, dx=1.139, dpx=0.184, dy=-0.0012, dpy=3.98e-5)
        self._test(seq, data=twiss(seq, initial=beta0)['lattice'])

    def test_sis18(self):
        self._test(_load_sequence('sis18'))

    def _test(self, sequence, *, data=None):
        fig, axes = plot_twiss(sequence, data=data)
        self.assertTrue(len(axes), 3)
        if __name__ == '__main__':
            plt.show()


if __name__ == '__main__':
    unittest.main()
