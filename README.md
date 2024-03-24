# Odoo 14 Custom Module

## Overview

This project contains modules for Employee Import and Invoice API.

## Employee Import Module

The Employee Import module allows users to import employee data into the system using a queue job mechanism. Upon successful import, an email confirmation is sent.

## Invoice API Module

The Invoice API module provides functionalities for managing invoices, including creating invoices, updating existing invoices, registering payments, and retrieving invoice and payment information.

## Installation

- Clone the repository
- Install dependencies
- Configure settings

## Usage

- Import employees by accessing the Employee Import module interface
- Utilize the Invoice API endpoints for managing invoices and payments

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT). You are free to use, modify, and distribute this software.


## Configuration Sample

Below is a sample configuration file (`odoo.conf`) for configuring the Odoo server:

```ini
[options]
; This is the password that allows database operations:
admin_passwd = admin_password
db_host = localhost
db_port = 5432
db_user = odoo14
db_password = odoo14
addons_path = /opt/odoo/odoo14/addons,/opt/odoo/odoo14/custom_addons
xmlrpc_port = 8014
# logfile = /var/log/odoo/odoo-dev.log
log_level = debug
workers = 2
longpolling_port = 8072
server_wide_modules = web,queue_job
```