from odoo import fields, models

class First(models.Model):
    _name = 'first.module'
    _description='Hello World,That is My First Module'
    _inherit = ['mail.thread']
    name=fields.Char(string='Name',required=True,tracking=True)
    date_of_birth=fields.Date(string='DOB',required=True,tracking=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ], string='Gender', required=True)
