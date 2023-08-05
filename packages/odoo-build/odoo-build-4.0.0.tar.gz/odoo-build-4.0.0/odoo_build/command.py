# Part of odoo-build.
# See LICENSE file for full copyright and licensing details.

import subprocess

from .console import out


class Command():
    def __init__(self, *args):
        self.args = args or []

    def call(self, **kwargs):
        out("Command: {}".format(' '.join(self.args)), 'important')
        try:
            process = subprocess.Popen(self.args, **kwargs)
            process.communicate()
        except KeyboardInterrupt:
            try:
                process.terminate()
                process.wait()
            except OSError:
                pass
            out("Odoo stopped by keyboard interrupt!", 'warning')

    @staticmethod
    def run(cmd):
        Command(cmd).call(shell=True)
