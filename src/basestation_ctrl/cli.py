import click
from basestation_ctrl.basestation_ctrl import BasestationCtrl


@click.group()
def cli():
    pass


@click.command()
# @click.option('--interface', '-i', default=0, help='Which Bluetooth interface to use.')
# @click.option('--mac_addresses', '-a', help='MAC address of the basestation.'
#              ' Multiple addresses can be entered, separated by comma.')
@click.argument('MAC_ADDRESS', nargs=-1)
def sleep(mac_address):
    lhctrl = BasestationCtrl()
    lhctrl.sleep(mac_address)


@click.command()
@click.argument('MAC_ADDRESS', nargs=-1)
def wake(mac_address):
    lhctrl = BasestationCtrl()
    lhctrl.wake(mac_address)


@click.command()
def scan():
    lhctrl = BasestationCtrl()
    results = lhctrl.scan()
    print(results)


cli.add_command(sleep)
cli.add_command(wake)
cli.add_command(scan)

if __name__ == '__main__':
    cli()
