from odoo import fields,models,api
from datetime import date



# import cv2
# import face_recognition



class Img(models.Model):
    _name ='img.module'
    _description = 'that tack a pic and create a new record'

    name=fields.Char(string='name')
    date_of_birth=fields.Date(string='DOB')
    age=fields.Integer(string='Age',help='Write a age',compute='_onchange_date_of_birth')
    cont_no=fields.Char(string='Cont.No')

    @api.depends('date_of_birth')
    def _onchange_date_of_birth(self):
        for rec in self:
            if rec.date_of_birth:
                today = date.today()
                try:
                    # Calculate age based on current date
                    rec.age = today.year - rec.date_of_birth.year - ((today.month, today.day) < (rec.date_of_birth.month, rec.date_of_birth.day))
                except Exception as e:
                    rec.age = 0  # In case of an error, set age to 0
            else:
                rec.age = 0


    def name_get(self):
        result=[]
        for rec in self:
            data=rec.name+'['+str(rec.cont_no)+']'
            result.append((rec.id,data))
            print(data)
        return result