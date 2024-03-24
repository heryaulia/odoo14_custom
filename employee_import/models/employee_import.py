from odoo import models, fields, api
import base64
import xlrd
from odoo.exceptions import UserError

class EmployeeImport(models.Model):
    _name = 'employee.import'
    _description = 'Import Employees'

    file = fields.Binary('Excel File', required=True)
    file_name = fields.Char('File Name')
    import_status = fields.Text(string='Import Status', readonly=True)

    @api.model
    def create_employee_jobs(self, file_content, context):
        """
        Processes the employee data from the file and creates job entries for each.

        Args:
            file_content (list): A list of dictionaries where each dictionary represents an employee's data.
            context (EmployeeImport): The current instance of the EmployeeImport model.

        Sets the import status on the context based on whether all employee creations were successful.
        """
        all_successful = True
        for row_data in file_content:
            success = self.with_delay().create_employee_from_row(row_data)
            if not success:
                all_successful = False

        context.import_status = 'Completed successfully' if all_successful else 'Completed with errors'
        context.send_notification_email()

    def send_notification_email(self):
        """
        Sends a notification email upon the completion of the import process.
        This method looks for a specific email template and sends a notification using that template.
        """
        template = self.env.ref('employee_import.email_template_import_complete')
        if template:
            template.send_mail(self.id, force_send=True)

    @api.model
    def create_employee_from_row(self, row_data):
        """
        Creates an employee record from a row of data.

        Args:
            row_data (dict): A dictionary containing the employee's data.

        Returns:
            bool: True if the employee was successfully created, False otherwise.
        """
        employee_model = self.env['hr.employee']
        if not all(key in row_data for key in ['Name', 'Work Email', 'Job Title', 'Work Phone']):
            print("Invalid data provided. Missing one or more required fields.")
            return False

        try:
            employee_model.create({
                'name': row_data.get('Name'),
                'work_email': row_data.get('Work Email'),
                'job_title': row_data.get('Job Title'),
                'work_phone': row_data.get('Work Phone'),
            })
        except Exception as e:
            print(f"Failed to create employee: {str(e)}")
            return False
        return True


    def action_import(self):
        """
        The main action to initiate the import process. It reads the uploaded file,
        parses the Excel content, and triggers the employee creation jobs.

        Raises:
            UserError: If no file is uploaded.

        Returns:
            dict: A dictionary defining an Odoo client action to notify the user of the import status.
        """
        if not self.file:
            raise UserError("Please upload a file.")
        
        # parse Excel
        file_content = base64.b64decode(self.file)
        workbook = xlrd.open_workbook(file_contents=file_content)
        sheet = workbook.sheet_by_index(0)

        file_data = []
        for row in range(1, sheet.nrows):
            values = sheet.row_values(row)
            file_data.append({
                'Name': values[0],
                'Work Email': values[1],
                'Job Title': values[2],
                'Work Phone': values[3],
            })

        print(file_data, "################################################################")

        self.create_employee_jobs(file_data, self)
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Employee Import',
                'message': 'Employee import is being processed. You will be notified upon completion.',
                'sticky': False,
            },
        }
