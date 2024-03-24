# Employee Import Module

This module provides functionality to import employee records from an Excel file. It includes a model to handle the import process and tests to ensure the reliability of the employee creation functionality.

## Features

- Import employee data from an Excel file.
- Validate the necessary fields are present in each row.
- Create employee records in the system based on the imported data.
- Send a notification upon completion of the import process.

## Installation

1. Place the module in your Odoo addons directory.
2. Update the module list in the Odoo backend.
3. Install the module by navigating to Apps and searching for Employee Import.

## Usage

After installation, you can access the functionality through the Employee Import menu item in the Odoo backend. Upload an Excel file with employee data and the system will process it accordingly.

## Testing

Tests are included to verify the correctness of the employee creation process. To run the tests, use the following command:

```sh
odoo-bin -c "config-file" -d "database-name" --test-enable --stop-after-init -i your_module_name --log-level=test
```

```sh
./odoo-bin -c odoo.conf -d odoo14db_clean_api --test-enable --stop-after-init -i employee_import --log-level=test
```
