# Part of odoo-build.
# See LICENSE file for full copyright and licensing details.

from argparse import ArgumentParser, RawDescriptionHelpFormatter

import argcomplete

from . import __version__

COPYRIGHT = """
Copyright (C) 2012-2020 Bluestar Solutions Sàrl (<http://bluestar.solutions>).
Released under GNU AGPLv3."""


class OBArgumentParser():
    args = None

    def __init__(self):
        parser = ArgumentParser(
            formatter_class=RawDescriptionHelpFormatter,
            description="A developer tool for Odoo.",
            epilog=f'''\
goal help:
    %(prog)s <goal> -h
{COPYRIGHT}''')
        parser.add_argument(
            '--version', action='version',
            version=f'%(prog)s {__version__}\n{COPYRIGHT}')

        parser_shared = ArgumentParser(add_help=False)

        parser_odoo_shared = ArgumentParser(add_help=False)
        parser_odoo_shared.add_argument(
            "-t", "--test", dest="odoo_test", action="store_true",
            help="Run with test configuration.")

        subparsers = parser.add_subparsers(metavar="<goal>")

        parser_odoo = subparsers.add_parser(
            'odoo', help="Run Odoo server normally.",
            parents=[parser_shared, parser_odoo_shared])
        parser_odoo.add_argument(
            "-u", "--update", dest="odoo_update",
            nargs='?', metavar='all|<module1>[,<module2>…]',
            const='def', default=None,
            help="Modules to update. Don't specify any module to use "
            "the module list of the current project. --database is required.")
        parser_odoo.add_argument(
            '-i', "--init", dest="odoo_install",
            nargs='?', metavar='all|<module1>[,<module2>…]',
            const='def', default=None,
            help="Modules to install. Don't specify any module to use "
            "the module list of the current project. --database is required.")
        parser_odoo.set_defaults(func="odoo")

        parser_project_version = subparsers.add_parser(
            'project.version', help="Set the version of all project modules",
            parents=[parser_shared])
        parser_project_version.add_argument(
            '-n', '--new-version', metavar='<version>',
            dest="project_version_new_version", default=None,
            help="The modules new version")
        parser_project_version.set_defaults(func="project-version")

        parser_i18n_export = subparsers.add_parser(
            'project.i18n.export',
            help="Export i18n templates files for addons specified "
            "in project configuration file.",
            parents=[parser_shared, parser_odoo_shared])
        parser_i18n_export.add_argument(
            '-d', "--database", dest="database",
            metavar='<database>',
            help="Database name for i18n export."
            "Use autobuild_{PROJECT_NAME} if not specified.",
            default='obuild_i18n')
        parser_i18n_export.add_argument(
            '-D', "--drop-database", action="store_true",
            dest="drop_database",
            help="Drop used database before exiting.")
        parser_i18n_export.set_defaults(func="i18n-export")

        parser_project_dist = subparsers.add_parser(
            'project.dist', help="Generate the distribution artifacts",
            parents=[parser_shared])
        parser_project_dist.set_defaults(func="project-dist")

        argcomplete.autocomplete(parser)
        self.args, self.odoo_args = parser.parse_known_args()
