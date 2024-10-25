from email.policy import default

from docutils.nodes import reference

from odoo import fields, models,api
from odoo.http import request


class First(models.Model):
    _name = 'sec.module'
    _description='Second Module'
    _inherit = ['mail.thread']
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

    @api.model_create_multi
    def create(self, vals_list):
        print('Dharmik',vals_list)
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