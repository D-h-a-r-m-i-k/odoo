from click import clear
from odoo import fields, models, api
import base64
import face_recognition
import numpy as np
import cv2


class Attendance(models.Model):
    _name = 'attendance.module'
    _description = 'make a attendance'
    _inherit = ['mail.thread']
    image = fields.Binary("Employee Image", attachment=True, required=True, store=True)
    name = fields.Char(string='Name')
    date_of_birth = fields.Date(string='DOB')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ], string='Gender')
    new_face_encoding = fields.Json(string="Face Encoding", compute="_compute_face_encoding", store=True)

    @api.depends('image')
    def action_recognize_employee(self):
        for record in self:
            binary_data = record.image
            if binary_data:
                decoded_data = base64.b64decode(binary_data)
                image_array = np.frombuffer(decoded_data, np.uint8)
                image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
                image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                face_encodings = face_recognition.face_encodings(image_rgb)
                employees = self.env['first.module'].search([])
                for employee in employees:
                    stored_encoding = employee.face_encoding

                    if face_encodings:
                        record.new_face_encoding = face_encodings[0].tolist()
                        if stored_encoding:
                            stored_encoding = np.array(stored_encoding)
                            match = face_recognition.compare_faces([stored_encoding], face_encodings[0])
                            if match[0]:
                                record.name = employee.name
                                record.date_of_birth = employee.date_of_birth
                                record.gender = employee.gender
                            else:
                                record.name = 'No match found 😒'
                                record.date_of_birth = None
                                record.gender = None
                        else:
                            clear()
                    else:
                        record.name = 'No face detected 😶‍🌫️'
                        record.date_of_birth = None
                        record.gender = None
            else:
                clear()

    @staticmethod
    def open_camera_popup(self):
        return {
            'type': 'ir.actions.client',
            'tag': 'open_camera_popup',
        }
    # def _match_face_encoding(self, face_encoding):
    #
    #     employees = self.env['first.module'].search([])  # Get all employees
    #     for employee in employees:
    #         stored_encoding = employee.face_encoding
    #         if stored_encoding:
    #             # Compare the encodings
    #             stored_encoding = np.array(stored_encoding)
    #             match = face_recognition.compare_faces([stored_encoding], face_encoding)
    #             if match[0]:
    #                 return employee
    #     return None
