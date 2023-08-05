# Odoo Build for Odoo

Odoo Build for Odoo is a hepler tool for Odoo project.

## Installation

### From PyPI

Install it in your project virtualenv:

    sudo apt-get install odoo-build

#### Requirements

An Odoo project with a python virtualenv.

## Configuration

### Project Settings

Create a file named obuild.yml in your project directory.

#### Options

* ``obuild``:
    * ``version``: Specify the version of odoo-build targeted by the configuration file.
* ``config``: Default Odoo config file to run it.
* ``database``: Database configuration.
    * ``host``: Database host.
    * ``port``: Database port.
    * ``user``: Database user.
    * ``password``: Database password.
* ``addons``: All project addons.
* ``addons``: Project addons to translate.

### Some examples

Run server and update _mymodule_ and _othermodule_ in _my_database_

    obuild odoo -u mymodule,othermodule -d my_database

See help for details.

## Credits

Bluestar Solutions Sàrl
Microcity - Rue Pierre-à-Mazel 39
CH-2000 Neuchâtel

## Copyright

Copyright (C) 2012-2020 Bluestar Solutions Sàrl (<http://www.blues2.ch>).

## License

[GNU AFFERO GENERAL PUBLIC LICENSE, version 3](http://www.gnu.org/licenses/agpl-3.0.html)
