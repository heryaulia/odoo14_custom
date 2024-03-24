from odoo import exceptions, http, fields
from odoo.http import request
import json


class InvoiceAPI(http.Controller):


    @http.route('/api/invoices', auth='public', type='http', methods=['POST'], csrf=False)
    def create_invoices(self, **kwargs):
        try:
            invoice_data_list = json.loads(request.httprequest.data.decode('utf-8')).get('invoices')
        except json.JSONDecodeError:
            return json.dumps({'success': False, 'error': 'Invalid JSON'})

        if not invoice_data_list:
            return json.dumps({'success': False, 'error': 'No invoice data provided'})

        user_id = request.session.uid
        required_fields = ['partner_id', 'invoice_line_ids']
        line_required_fields = ['product_id', 'quantity', 'price_unit']

        for invoice_data in invoice_data_list:
            missing_fields = [field for field in required_fields if field not in invoice_data]
            if missing_fields:
                return json.dumps({'success': False, 'error': f'Missing required invoice fields: {missing_fields}'})

            for line in invoice_data.get('invoice_line_ids', []):
                missing_line_fields = [field for field in line_required_fields if field not in line]
                if missing_line_fields:
                    return json.dumps({'success': False, 'error': f'Missing required invoice line fields: {missing_line_fields}'})

            invoice_vals = {
                'move_type': 'out_invoice',
                'partner_id': invoice_data['partner_id'],
                'invoice_line_ids': [
                    (0, 0, {
                        'product_id': line['product_id'],
                        'quantity': line['quantity'],
                        'price_unit': line['price_unit']
                    }) for line in invoice_data.get('invoice_line_ids', [])
                ],
            }
            request.env['account.move'].with_user(user_id).sudo().with_delay().create_and_post_invoice(invoice_vals)

        return json.dumps({'success': True, 'message': 'Invoice creation tasks have been enqueued'})



    @http.route('/api/invoice/payment', auth='public', type='json', methods=['POST'])
    def register_payment(self, **kwargs):
        required_fields = ['invoice_id', 'amount', 'journal_id']
        for field in required_fields:
            if field not in kwargs:
                return {'error': f'Missing {field}'}
            
        if float(kwargs['amount']) < 1:
            return {'error': 'The amount must be at least 1'}

        invoice = request.env['account.move'].sudo().browse(int(kwargs['invoice_id']))
        if not invoice.exists():
            return {'error': 'Invoice not found'}
        
        if invoice.state != 'posted':
            return {'error': 'Invoice not posted yet'}
        
        if invoice.move_type != 'out_invoice':
            return {'error': 'This Move is not Invoice'}

        if invoice.payment_state == 'paid':
            return {'error': 'Invoice is already fully paid'}

        journal = request.env['account.journal'].sudo().browse(int(kwargs['journal_id']))
        if not journal.exists():
            return {'error': 'Journal not found'}

        if journal.type not in ['bank', 'cash']:
            return {'error': 'Invalid journal type. Journal must be of type bank or cash for registering a payment.'}

        payment_method = journal.inbound_payment_method_ids[0] if journal.inbound_payment_method_ids else False
        if not payment_method:
            return {'error': 'No inbound payment method found in the journal'}

        payment_vals = {
            'date': fields.Date.today(),
            'amount': float(kwargs['amount']),
            'payment_type': 'inbound',
            'partner_type': 'customer',
            'ref': invoice.payment_reference or '',
            'journal_id': journal.id,
            'currency_id': invoice.currency_id.id,
            'partner_id': invoice.partner_id.id,
            'payment_method_id': payment_method.id,
        }

        payment = request.env['account.payment'].sudo().create(payment_vals)
        payment.action_post()

        # reconcile payment with the invoice
        if invoice.state == 'posted' and invoice.payment_state != 'paid':
            payment_lines = payment.line_ids.filtered(lambda line: line.account_internal_type in ('receivable', 'payable') and not line.reconciled)
            invoice_lines = invoice.line_ids.filtered(lambda line: line.account_internal_type in ('receivable', 'payable') and not line.reconciled)
            (payment_lines | invoice_lines).sudo().reconcile()

        return {'success': True, 'message': 'Payment created and associated with invoice successfully', 'payment_id': payment.id}


    @http.route('/api/invoice', auth='public', type='http', methods=['GET'])
    def get_invoice_and_payments(self, **kwargs):
        invoice_id = kwargs.get('invoice_id')

        if not invoice_id:
            return json.dumps({'success': False, 'message': 'No invoice ID provided'})

        invoice = request.env['account.move'].browse(int(invoice_id)).sudo()

        if not invoice.exists():
            return json.dumps({'success': False, 'message': 'Invoice not found'})

        payments_info = invoice._get_reconciled_info_JSON_values()
        invoice_data = {
            'invoice_id': invoice.id,
            'invoice_ref': invoice.payment_reference,
            'partner_name': invoice.partner_id.name,
            'state': invoice.state,
            'amount_total': invoice.amount_total,
            'outstanding_balance': invoice.amount_residual,
            'payments': [{
                'payment_id': payment['payment_id'],
                'payment_ref': payment['name'],
                'payment_date': payment['date'].strftime("%Y-%m-%d") if payment['date'] else "",
                'payment_amount': payment['amount'],
                'currency': payment['currency'],
            } for payment in payments_info]
        }

        return json.dumps({'success': True, 'data': invoice_data})


    @http.route('/api/invoice', auth='public', type='http', methods=['PUT'], csrf=False)
    def update_invoices(self):
        try:
            data = json.loads(request.httprequest.data)
        except json.JSONDecodeError:
            return json.dumps({'success': False, 'message': 'Invalid JSON data'})
        print(data, "##########################################################")
        
        try:
            invoice_id = data.get('invoice_id')
            if not invoice_id:
                return json.dumps({'success': False, 'message': 'No invoice ID provided'})

            invoice = request.env['account.move'].browse(int(invoice_id)).sudo()
            if not invoice.exists():
                return json.dumps({'success': False, 'message': 'Invoice not found'})

            if invoice.payment_state == 'paid':
                return json.dumps({'success': False, 'message': 'Invoice Already Fully Paid'})
            elif invoice.state == 'posted':
                invoice.button_draft()
            elif invoice.state != 'draft':
                return json.dumps({'success': False, 'message': 'Only draft or posted invoices can be updated'})

            update_fields = {
                'invoice_date': data.get('invoice_date'),
                'partner_id': data.get('partner_id'),
            }
            update_fields = {key: value for key, value in update_fields.items() if value is not None}
            
            partner_id = data.get('partner_id')
            partner = request.env['res.partner'].browse(int(partner_id)).sudo()
            if not partner.exists():
                return json.dumps({'success': False, 'message': 'partner not found'})


            if update_fields:
                invoice.write(update_fields)

            if 'invoice_lines' in data:
                invoice.invoice_line_ids.unlink()
                invoice_lines = data.get('invoice_lines')
                new_invoice_lines = [(0, 0, {
                    'product_id': int(line.get('product_id')),
                    'quantity': float(line.get('quantity')),
                    'price_unit': float(line.get('price_unit')),
                }) for line in invoice_lines]
                invoice.write({'invoice_line_ids': new_invoice_lines})

            invoice.action_post()
            return json.dumps({'success': True, 'message': 'Invoice updated successfully'})

        except exceptions.UserError as e:
            return json.dumps({'success': False, 'message': str(e.name)})
        except exceptions.MissingError as e:
            return json.dumps({'success': False, 'message': str(e.name)})
        except Exception as e:
            return json.dumps({'success': False, 'message': str(e)})