# Part of odoo-build.
# See LICENSE file for full copyright and licensing details.

from colorama import Fore, Style

STYLES = {
    'info': Fore.WHITE + Style.BRIGHT,
    'success': Fore.GREEN + Style.BRIGHT,
    'warning': Fore.YELLOW + Style.BRIGHT,
    'error': Fore.RED + Style.BRIGHT,
    'important': Fore.CYAN + Style.BRIGHT}
HEAD = Fore.MAGENTA + Style.BRIGHT + '[obuild] ' + Style.RESET_ALL


def out(txt, style='none'):
    print((HEAD + STYLES.get(style, '') + txt + Style.RESET_ALL))
