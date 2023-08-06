from ratealert import ConversionAlert
import click


@click.command()
@click.option('--source', prompt='Source Currency', help='Source Currency.')
@click.option('--target', prompt='Target Currency', help='Target Currency.')
@click.option('--alert-rate', prompt='Alert Rate', help='Rate at which to raise alert.')
def main(source, target, alert_rate):
    ConversionAlert(source, target, alert_rate)


if __name__ == "__main__":
    main()
