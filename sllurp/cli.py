"""Command-line wrapper for sllurp commands.
"""

from __future__ import print_function, unicode_literals
from collections import namedtuple
import logging
import click
from . import __version__
from . import log as loggie
from .verb import reset as _reset
from .verb import inventory as _inventory
from .verb import log as _log
from .llrp_proto import Modulation_Name2Type

# Disable Click unicode warning since we use unicode string exclusively
click.disable_unicode_literals_warning = True

logger = logging.getLogger(__name__)
mods = sorted(Modulation_Name2Type.keys())


@click.group()
@click.option('-d', '--debug', is_flag=True, default=False)
@click.option('-l', '--logfile', type=click.Path())
def cli(debug, logfile):
    loggie.init_logging(debug, logfile)


@cli.command()
@click.argument('host', type=str, nargs=-1)
@click.option('-p', '--port', type=int, default=5084)
@click.option('-t', '--time', type=float, default=5,
              help='seconds to inventory (default 5)')
@click.option('-n', '--report-every-n-tags', type=int,
              help='issue a TagReport every N tags')
@click.option('-a', '--antennas', type=str, default='1',
              help='comma-separated list of antennas to use (0=all;'
                   ' default 1)')
@click.option('-X', '--tx-power', type=int, default=0,
              help='transmit power (default 0=max power)')
@click.option('-M', '--modulation', type=click.Choice(mods),
              help='Reader-to-Tag Modulation')
@click.option('-T', '--tari', type=int, default=0,
              help='Tari value (default 0=auto)')
@click.option('-s', '--session', type=int, default=2,
              help='Gen2 session (default 2)')
@click.option('-m', '--mode-identifier', type=int, help='ModeIdentifier value')
@click.option('-P', '--tag-population', type=int, default=4,
              help="Tag Population value (default 4)")
@click.option('-r', '--reconnect', is_flag=True, default=False,
              help='reconnect on connection failure or loss')
def inventory(host, port, time, report_every_n_tags, antennas, tx_power,
              modulation, tari, session, mode_identifier,
              tag_population, reconnect):
    # XXX band-aid hack to provide many args to _inventory.main
    Args = namedtuple('Args', ['host', 'port', 'time', 'every_n', 'antennas',
                               'tx_power', 'modulation', 'tari', 'session',
                               'population', 'mode_identifier',
                               'reconnect'])
    args = Args(host=host, port=port, time=time, every_n=report_every_n_tags,
                antennas=antennas, tx_power=tx_power, modulation=modulation,
                tari=tari, session=session, population=tag_population,
                mode_identifier=mode_identifier,
                reconnect=reconnect)
    logger.debug('inventory args: %s', args)
    _inventory.main(args)


@click.argument('host', type=str, nargs=-1)
@click.option('-o', '--outfile', type=click.File('w'), default='-')
@click.option('-a', '--antennas', type=str, default='0',
              help='comma-separated list of antennas to use (default 0=all)')
@click.option('-g', '--stagger', type=int,
              help='delay (ms) between connecting to readers')
@click.option('-e', '--epc', type=str, help='log only a specific EPC')
@cli.command()
def log(host, outfile, antennas, stagger, epc):
    _log.main(host, outfile, antennas, stagger, epc)


@cli.command()
def version():
    print(__version__)


@cli.command()
@click.argument('host', type=str, nargs=-1)
@click.option('-p', '--port', type=int, default=5084)
def reset(host, port):
    _reset.main(host, port)
