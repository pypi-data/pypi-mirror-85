"""Print the full list of beam properties based on user input (i.e. also compute the remaining properties)."""

import argparse
import inspect
import pprint
import sys

import pandas as pd

from dipas.build import Beam
from dipas.madx.builder import write_command


class Namespace(dict):
    def __setattr__(self, name, value):
        self[name] = value


parser = argparse.ArgumentParser()
spec = inspect.getfullargspec(Beam)
for parameter, default in zip(spec.args[1:], spec.defaults):
    parser.add_argument(f'--{parameter}', default=default, type=spec.annotations[parameter])
parser.add_argument('--as', default='madx', choices=('dict', 'series' , 'madx'))

display_styles = {'dict': dict, 'series': pd.Series}


def display_style_madx(attrs):
    cmd = write_command('beam', attrs)
    return cmd.replace(', ', f',\n{4*" "}') + ';'


display_styles['madx'] = display_style_madx


def main():
    args = parser.parse_args(namespace=Namespace())
    display_style = display_styles[args.pop('as')]
    beam = Beam(**args)
    beam = display_style(beam.to_dict())
    printer = {str: print}.get(type(beam), pprint.pprint)
    printer(beam)
    return 0


if __name__ == '__main__':
    sys.exit(main())
