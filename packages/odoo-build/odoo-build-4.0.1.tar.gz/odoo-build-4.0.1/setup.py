# Part of openerp-autobuild.
# See LICENSE file for full copyright and licensing details.

from setuptools import find_packages, setup

from odoo_build import __version__

setup(
    name='odoo-build',
    version=__version__,
    author="Bluestar Solutions Sàrl",
    author_email="devs@bluestar.solutions",
    description="An utility to manage Odoo pip build",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",

    python_requires='>=3.6',
    install_requires=[
        'setuptools',
        'setuptools-odoo',
        'psycopg2-binary',
        'argcomplete',
        'colorama',
        'pyyaml'],
    packages=find_packages(),
    include_package_data=True,

    url='https://bitbucket.org/bluestarsolutions/odoo-build',

    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development :: Build Tools"
    ],

    scripts=['odoo_build/obuild'],
)
