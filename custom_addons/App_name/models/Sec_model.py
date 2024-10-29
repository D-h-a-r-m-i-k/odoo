from email.policy import default

from docutils.nodes import reference

from odoo import fields, models,api
from odoo.http import request


class Sec(models.Model):
    _name = 'sec.module'
    _description='Second Module'
    _inherit = ['mail.thread']
    _rec_names_search = ['reference','user_name']
    _rec_name = 'user_name'
    reference=fields.Char(string='',default='New')
    user_name=fields.Many2one('first.module',string='Name',required=True,tracking=True)
    date_of_birth=fields.Date(string='Appointment Date',required=True,tracking=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ], string='Gender', required=True)
    status = fields.Selection([('draft', 'Draft'), ('confirmed', 'Confirmed'), ('ongoing', 'Ongoing'), ('done', 'Done'), ('cancel', 'Cancel')],default='draft',tracking=True)
    note=fields.Char(string='NOTE',tracking=True)
    appointment_line_ides=fields.One2many('first.line','appointment_id',string='lines')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('reference') or vals['reference']=='New':
                vals['reference']=self.env['ir.sequence'].next_by_code('sec.module')
        return super().create(vals_list)

    def action_confirmed(self):
        for i in self:
            self.status='confirmed'

    def action_ongoing(self):
        for i in self:
            self.status='ongoing'

    def action_done(self):
        for i in self:
            self.status='done'

    def action_cancel(self):
        for i in self:
            self.status = 'cancel'

class FirstLine(models.Model):
    _name='first.line'
    _description='user line'

    appointment_id = fields.Many2one('sec.module', string='Appointment')
    product_id=fields.Many2one('product.product',string='product')
    quantity=fields.Float(string='Quantity')