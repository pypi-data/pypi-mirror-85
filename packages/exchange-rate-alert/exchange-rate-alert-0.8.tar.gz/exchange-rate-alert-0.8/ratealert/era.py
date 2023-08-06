from ratealert import ConversionAlert
import click


@click.command()
@click.option('--source', prompt='Source Currency', help='Source Currency.')
@click.option('--target', prompt='Target Currency', help='Target Currency.')
@click.option('--alert-rate', prompt='Alert Rate', help='Rate at which to raise alert.')
@click.option('--poll-interval', prompt='Polling Interval', help='Time intervals to check transfer rates.')
def main(source, target, alert_rate, poll_interval):
    ConversionAlert(source, target, alert_rate, poll_interval)


if __name__ == "__main__":
    main()
