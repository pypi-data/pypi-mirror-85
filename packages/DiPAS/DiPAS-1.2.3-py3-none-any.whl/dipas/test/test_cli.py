from importlib import resources
import os
import unittest

import click
from click.testing import CliRunner

from dipas.cli import cli, plot, twiss, orm, madx_twiss, madx_orm
import dipas.test.sequences


class TestPlot(unittest.TestCase):
    def test(self):
        runner = CliRunner()
        with resources.path('dipas.test.sequences', 'sis18.seq') as f_path:
            with runner.isolated_filesystem():
                result = runner.invoke(cli, ['plot', str(f_path), '--save', 'fig.png', '--hide'])
                self.assertTrue(os.path.exists('fig.png'))
        self.assertFalse(result.exception)
        self.assertEqual(result.exit_code, 0)


class TestTwiss(unittest.TestCase):
    def test(self):
        runner = CliRunner()
        with resources.path('dipas.test.sequences', 'sis18.seq') as f_path:
            with runner.isolated_filesystem():
                result = runner.invoke(cli, ['twiss', str(f_path), '--outfile', 'twiss.csv'])
                self.assertTrue(os.path.exists('twiss.csv'))
        self.assertFalse(result.exception)
        self.assertEqual(result.exit_code, 0)


class TestORM(unittest.TestCase):
    def test(self):
        runner = CliRunner()
        with resources.path('dipas.test.sequences', 'sis18.seq') as f_path:
            with runner.isolated_filesystem():
                result = runner.invoke(cli, ['orm', str(f_path), 'orm.csv'])
                self.assertTrue(os.path.exists('orm.csv'))
        self.assertFalse(result.exception)
        self.assertEqual(result.exit_code, 0)


MADX = os.path.expanduser('~/bin/madx')


class TestMADXTwiss(unittest.TestCase):
    def test(self):
        runner = CliRunner()
        with resources.path('dipas.test.sequences', 'sis18.seq') as f_path:
            with runner.isolated_filesystem():
                result = runner.invoke(cli, ['madx', 'twiss', str(f_path), '--outfile', 'twiss.csv', '--madx', MADX])
                self.assertTrue(os.path.exists('twiss.csv'))
        self.assertFalse(result.exception)
        self.assertEqual(result.exit_code, 0)


class TestMADXORM(unittest.TestCase):
    def test(self):
        runner = CliRunner()
        with resources.path('dipas.test.sequences', 'sis18.seq') as f_path:
            with runner.isolated_filesystem():
                result = runner.invoke(cli, ['madx', 'orm', str(f_path), 'orm.csv', '--madx', MADX])
                self.assertTrue(os.path.exists('orm.csv'))
        self.assertFalse(result.exception)
        self.assertEqual(result.exit_code, 0)


if __name__ == '__main__':
    unittest.main()
