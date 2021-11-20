import click
from basestation_ctrl.basestation_ctrl import BasestationCtrl


@click.group()
def cli():
    pass


@click.command()
def sleep():
    macs = ["e0:81:5e:b8:20:fc"]
    lhctrl = BasestationCtrl()
    lhctrl.sleep(macs)


@click.command()
def wake():
    macs = ["e0:81:5e:b8:20:fc"]
    lhctrl = BasestationCtrl()
    lhctrl.wake(macs)


@click.command()
def scan():
    lhctrl = BasestationCtrl()
    lhctrl.scan()

cli.add_command(sleep)
cli.add_command(wake)
cli.add_command(scan)

if __name__ == '__main__':
    cli()
