from odoo import models, api

class AccountMove(models.Model):
    _inherit = 'account.move'
    _description = 'Inherit Account Move'

    @api.model
    def create_and_post_invoice(self, invoice_vals):
        invoice = self.create(invoice_vals)
        invoice.action_post()
