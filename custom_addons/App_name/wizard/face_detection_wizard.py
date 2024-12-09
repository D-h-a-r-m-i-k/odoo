from odoo import api,fields,models

class FaceDetectionWizard(models.TransientModel):
    _name='face.detection.wizard'
    _description='that store the data temporary'

    name=fields.Char(string='name')

    @staticmethod
    def show():
        print('hello')
