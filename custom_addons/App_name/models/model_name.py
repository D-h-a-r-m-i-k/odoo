from odoo import fields, models

class First(models.Model):
    _name = 'first.module'
    _description='Hello World,That is My First Module'

    name=fields.Char(string='Name',required=True)
    DoB=fields.Date(string="Date Of Birth",required=True)
    gender=fields.Selection([('male','Male'),('female','Female')],string='Gender',required=True)
    age=fields.Integer('Age',required=True)