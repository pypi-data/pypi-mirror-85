from argparse import Namespace
from importlib import resources
from io import StringIO
import os.path
import tempfile
import unittest
from unittest.mock import patch
import warnings

import dipas.test.sequences
import dipas.tools.madx_to_html
import dipas.tools.print_beam


class TestMADXToHTML(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        warnings.simplefilter('ignore')

    def test(self):
        for sequence in ('cryring', 'hades', 'sis18'):
            with resources.path('dipas.test.sequences', f'{sequence}.seq') as path:
                with tempfile.TemporaryDirectory() as td:
                    with patch('dipas.tools.madx_to_html.parser',
                               Namespace(parse_args=lambda: Namespace(infile=path, outfile=os.path.join(td, 'test'),
                                                                      paramodi=None, drift_quads=False))):
                        self.assertEqual(dipas.tools.madx_to_html.main(), 0)


class TestPrintBeam(unittest.TestCase):
    def test(self):
        class DefaultNamespace(Namespace):
            def __getattr__(self, item):
                return None

        with patch('dipas.tools.print_beam.parser',
                   Namespace(parse_args=lambda **kwargs: dipas.tools.print_beam.Namespace({
                       'particle': 'proton', 'energy': 1.0, 'as': 'dict'}))):
            with patch('pprint.pprint') as pprint_mock:
                dipas.tools.print_beam.main()
                pprint_mock.assert_called_once()


if __name__ == '__main__':
    unittest.main()
