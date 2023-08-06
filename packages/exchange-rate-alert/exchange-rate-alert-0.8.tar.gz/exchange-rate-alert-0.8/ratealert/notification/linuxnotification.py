import subprocess
import click


class LinuxNotification:

    def _set_notification(self, message):
        """Set notification for unix system"""
        click.echo(message)
        subprocess.call(['notify-send',
                         'Rate Alert!',
                         message + " Get that Money!"])

    def set_notification(self, message):
        """Set notification code for unix system"""
        return self._set_notification(message)
