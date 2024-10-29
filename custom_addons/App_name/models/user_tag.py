from odoo import fields, models


class UserTag(models.Model):
    _name = 'user.tag'
    _description='usr tags'
    _order = 'sequence,id'
    name=fields.Char(string='Name',required=True)
    color = fields.Integer('Color Index', default=0)
    sequence = fields.Integer(default=0)
