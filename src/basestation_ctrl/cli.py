import click
from basestation_ctrl.basestation_ctrl import BasestationCtrl
import logging

logger = logging.getLogger("basestation-ctrl")


def loglevel_callback(ctx, param, value):
    logger.setLevel(value)
    logging.basicConfig(level=value)


def common_options(function):
    function = click.option('--interface', '-i', default=0,
                            help='Which Bluetooth interface to use.'
                            ' An integer <n> corresponds to the'
                            ' device "/dev/hci<n>" ', show_default=True)(function)
    function = click.option('--max_tries', '-n', default=10,
                            help='Number of tries before giving up to connect.',
                            show_default=True)(function)
    function = click.option('--pause', '-p', default=1.,
                            help='Seconds between of connection re-tries.',
                            show_default=True)(function)
    function = click.option('--loglevel', '-l', type=click.Choice(list(logging._nameToLevel.keys())),
                            default='ERROR', show_default=True,
                            callback=loglevel_callback)(function)
    return function


@click.group()
@common_options
def cli(interface, max_tries, pause, loglevel):
    """basestation-ctrl - A python library and CLI to wake up / power down SteamVR (Lighthouse)
    Base Stations. It currently only works for base stations v2.

    Use `basestation-ctrl <command> --help` for more help."""
    pass


@click.command()
@common_options
@click.argument('MAC_ADDRESS', nargs=-1)
def sleep(mac_address, interface, max_tries, pause, loglevel):
    """Sends basestation into sleep mode"""
    lhctrl = BasestationCtrl(interface)
    lhctrl.sleep(mac_address, max_tries, pause)


@click.command()
@common_options
@click.argument('MAC_ADDRESS', nargs=-1)
def wake(mac_address, interface, max_tries, pause, loglevel):
    """Wakes up basestation from sleep mode"""
    lhctrl = BasestationCtrl(interface)
    lhctrl.wake(mac_address, max_tries, pause)


@click.command()
@common_options
@click.option('--timeout', default=10., help='Scan timeout in seconds.', show_default=True)
@click.option('--show_all', default=10.,
              help='Show complete scan results, not only the devices starting with "LHB-".',
              show_default=True)
def scan(interface, max_tries, pause, loglevel, timeout, show_all):
    """Scans for basestations in the vicinity (requires root permissions)"""
    lhctrl = BasestationCtrl(interface)
    results = lhctrl.scan(timeout, show_all)
    print(' '.join(results.values()))


cli.add_command(sleep)
cli.add_command(wake)
cli.add_command(scan)

if __name__ == '__main__':
    cli()
