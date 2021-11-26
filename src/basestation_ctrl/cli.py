import click
from basestation_ctrl.basestation_ctrl import BasestationCtrl


def common_options(function):
    function = click.option('--interface', '-i', default=0,
                            help='Which Bluetooth interface to use.'
                            ' An integer <n> corresponds to the'
                            ' device "/dev/hci<n>" ', show_default=True)(function)
    function = click.option('--tries', '-n', default=3,
                            help='Number of tries when connecting fails.',
                            show_default=True)(function)
    function = click.option('--pause', '-p', default=5.,
                            help='Seconds between of connection re-tries.',
                            show_default=True)(function)
    return function


@click.group()
@common_options
def cli(interface, tries, pause):
    """basestation-ctrl - A python library and CLI to wake up / power down SteamVR (Lighthouse)
    Base Stations. It currently only works for base stations v2.

    Use `basestation-ctrl <command> --help` for more help."""
    pass


@click.command()
@common_options
@click.argument('MAC_ADDRESS', nargs=-1)
def sleep(mac_address, interface, tries, pause):
    """Sends basestation into sleep mode"""
    lhctrl = BasestationCtrl(interface)
    lhctrl.sleep(mac_address, tries, pause)


@click.command()
@common_options
@click.argument('MAC_ADDRESS', nargs=-1)
def wake(mac_address, interface, tries, pause):
    """Wakes up basestation from sleep mode"""
    lhctrl = BasestationCtrl(interface)
    lhctrl.wake(mac_address, tries, pause)


@click.command()
@common_options
@click.option('--timeout', default=10., help='Scan timeout in seconds.', show_default=True)
@click.option('--show_all', default=10.,
              help='Show complete scan results, not only the devices starting with "LHB-".',
              show_default=True)
def scan(interface, tries, pause, timeout, show_all):
    """Scans for basestations in the vicinity (requires root permissions)"""
    lhctrl = BasestationCtrl(interface)
    results = lhctrl.scan(timeout, show_all)
    print(' '.join(results.values()))


cli.add_command(sleep)
cli.add_command(wake)
cli.add_command(scan)

if __name__ == '__main__':
    cli()
