from odoo import fields, models, api
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

    tag_ids= fields.Many2many('user.tag','user_tag_rel','user_id','tag_id')
    image = fields.Binary("Employee Image", attachment=True, required=True, store=True)
    face_encoding = fields.Json(string="Face Encoding",compute="_compute_face_encoding",store=True)

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
