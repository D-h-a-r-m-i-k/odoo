
from odoo import fields, models, api, _
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