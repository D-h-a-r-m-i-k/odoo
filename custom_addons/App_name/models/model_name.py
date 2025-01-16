from email.policy import default

import requests

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError,UserError
import base64
import face_recognition
import numpy as np
import cv2

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
    hobie= fields.Many2many('user.tag','user_tag_rel','user_id','tag_id','Hobbies')
    image = fields.Binary("Employee Image", attachment=True, required=True, store=True)
    face_encoding = fields.Json(string="Face Encoding",compute="_compute_face_encoding",store=True)
    cont_no=fields.Char(string='Cont.no')
    attendance_count=fields.Integer(string='Attendance_count',compute='get_count')
    salary=fields.Integer(string='Salary per month',help='Base Salary per Month', required=True)
    standard_working_hours=fields.Float(string='Standard Working Hours',help='Min Working Hours', required=True,default=8.00)
    bank_detail_ids=fields.One2many('bank.details','bank_detail_id',string='Bank')

    def get_count(self):
        cont = self.env['attendance.module'].search_count([('name','=',self.name)])
        self.attendance_count=cont

    @api.model_create_multi
    def name_get(self):
        result=[]
        for rec in self:
            name= rec.name+'-'+rec.cont_no
            result.append((rec.id,name))
        return result


    def lala(self):
        return {
            'name': _('Attendance'),
            'domain':[('name','=',self.name)],
            'view_type': 'form',
            'view_mode': 'list',
            'res_model': 'attendance.module',
            'view_id': False,
            'type': 'ir.actions.act_window',
        }


    @api.depends('image')
    def _compute_face_encoding(self):
        for record in self:
            binary_data = record.image
            if binary_data:
                decoded_data = base64.b64decode(binary_data)
                image_array = np.frombuffer(decoded_data, np.uint8)
                image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
                image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                face_encodings = face_recognition.face_encodings(image_rgb)

                if face_encodings:
                    record.face_encoding = face_encodings[0].tolist()
                else:
                    record.face_encoding = None
            else:
                record.face_encoding = None

class BankDetails(models.Model):
    _name = 'bank.details'
    _description = 'User Bank Details'

    bank_detail_id=fields.Many2one('first.module',string='Bank Details')
    Account_no=fields.Char(string='Account No.')
    ifsc_code=fields.Char(string='IFSC code')
    branch=fields.Char(string='Branch',compute='get_bank_details',default='')
    Bank_name=fields.Char(string='Bank Name',compute='get_bank_details',default='')



    @api.depends('ifsc_code')
    def get_bank_details(self):
        url = f"https://ifsc.razorpay.com/{self.ifsc_code}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if "BRANCH" in data and "BANK" in data:
                self.Bank_name=data['BANK']
                self.branch=data['BRANCH']
            else:
                raise UserError(_('Invalid IFSC code or information not available.'))

        except Exception as e:
            raise UserError(_(f"An error occurred: {e}"))