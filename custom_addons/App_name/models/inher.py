from odoo import fields,api,models

class Inh(models.Model):
    _inherit = 'sale.order'

    test=fields.Char('Test')
    img_data=fields.Many2one('img.module','img_data') 