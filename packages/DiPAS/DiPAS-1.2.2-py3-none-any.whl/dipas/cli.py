from contextlib import nullcontext
import itertools as it
from pprint import pprint
import re

import click
from click_inspect import add_options_from
import matplotlib.pyplot as plt
import pandas as pd
import torch

from .build import from_file
from . import compute
from .elements import HKicker, VKicker, HMonitor, VMonitor
from .madx.utils import run_file, run_orm, run_script
from .plot import plot_twiss
from .utils import TemporaryFileName


@click.group()
def cli():
    pass


@cli.command()
@click.argument('file', type=click.Path(exists=True))
@click.option('--save', type=click.Path())
@click.option('--hide', is_flag=True, default=False)
@add_options_from(plot_twiss, exclude={'data'})
def plot(file, save, hide, **kwargs):
    """Plot the given lattice and Twiss parameters."""
    fig, __ = plot_twiss(from_file(file), **kwargs)
    if save:
        fig.savefig(save)
    if not hide:
        plt.show()


@cli.command()
@click.argument('file', type=click.Path(exists=True))
@click.option('--outfile', type=click.Path(), help='File path to save the Twiss table')
@click.option('-v', '--verbose', count=True)
@add_options_from(compute.twiss, exclude={'initial'}, custom={'order': {'type': int}})
def twiss(file, outfile, verbose, **kwargs):
    """Compute Twiss data, print global parameters (such as tunes) and optionally save lattice functions."""
    lattice = from_file(file)
    lattice.apply_unique_labels()
    twiss_data = compute.twiss(lattice, **kwargs)
    twiss_table = twiss_data.pop('lattice')
    if outfile is not None:
        twiss_table.applymap(lambda x: x.item()).to_csv(outfile)
    keys = {0: ('Q1', 'Q2')}.get(verbose, twiss_data.keys())
    pprint({k: twiss_data[k] for k in keys})


@cli.command()
@click.argument('file', type=click.Path(exists=True))
@click.argument('outfile', type=click.Path())
@add_options_from(compute.orm, exclude={'kickers', 'monitors'}, custom={'order': {'type': int}})
def orm(file, outfile, **kwargs):
    """Compute Orbit Response Matrix and save as CSV file."""
    lattice = from_file(file)
    kickers = lattice[HKicker] + lattice[VKicker]
    h_monitor = lattice[HMonitor]
    v_monitor = lattice[VMonitor]
    monitors = h_monitor + v_monitor
    orm_data_all = compute.orm(lattice, kickers=kickers, monitors=monitors, **kwargs)
    orm_data_x = orm_data_all.x[:len(h_monitor)]
    orm_data_y = orm_data_all.y[len(h_monitor):]
    orm_data = torch.cat((orm_data_x, orm_data_y), dim=0)
    pd.DataFrame(
        index=[e.label for e in monitors],
        columns=[e.label for e in kickers],
        data = orm_data.numpy()
    ).to_csv(outfile)


@cli.group()
def madx():
    """MADX subcommands (twiss and orm)."""
    pass


@madx.command('twiss')
@click.argument('file', type=click.Path(exists=True))
@click.option('--outfile', type=click.Path(), help='File path to save the Twiss table')
@add_options_from(run_script, include={'madx', 'wdir'})
def madx_twiss(file, outfile, **kwargs):
    """Use MADX to compute Twiss data, print global parameters (such as tunes) and optionally save lattice parameters."""
    if outfile is None:
        file_name_ctx = TemporaryFileName()
    else:
        file_name_ctx = nullcontext(outfile)
    with file_name_ctx as twiss_file_name:
        twiss_table, twiss_meta = run_file(file, twiss=dict(file=twiss_file_name, meta=True), **kwargs)[twiss_file_name]
    pprint(twiss_meta)
    if outfile:
        twiss_table.to_csv(outfile)


@madx.command('orm')
@click.argument('file', type=click.Path(exists=True))
@click.argument('outfile', type=click.Path())
@click.option('--kickers', multiple=True, help='Regex (/) or glob (*) patterns to identify kickers by their labels')
@click.option('--monitors', multiple=True, help='Regex (/) or glob (*) patterns to identify monitors by their labels')
@add_options_from(run_orm, include={'kicks', 'madx'})
def madx_orm(file, outfile, *, kickers, monitors, **kwargs):
    """Use MADX to compute Orbit Response Matrix (ORM)."""

    lattice = from_file(file)

    def _select_element_labels(patterns, types):
        if patterns:
            patterns = (re.compile(p.strip('/')) if p.startswith('/') else p for p in patterns)
            elements = _select_elements_from_patterns(patterns)
        else:
            elements = (e for tp in types for e in lattice[tp])
        return [e.label for e in elements]

    def _select_elements_from_patterns(patterns):
        elements = (lattice[pattern] for pattern in patterns)
        elements = (e if isinstance(e, list) else [e] for e in elements)
        return it.chain.from_iterable(elements)

    orm_data = run_orm(file,
                       kickers=_select_element_labels(kickers, (HKicker, VKicker)),
                       monitors=_select_element_labels(monitors, (HMonitor, VMonitor)),
                       **kwargs)
    orm_data.to_csv(outfile)


if __name__ == '__main__': # DEBUG
    madx_orm()
