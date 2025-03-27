from odoo import api,models,fields
import base64
import face_recognition
import cv2
import numpy as np

class AttendanceEmployee(models.Model):
    _inherit = 'event.event'

    player_type=fields.Selection([
        ('solo', 'Solo'),
        ('deo', 'Deo'),
        ('squad','Squad')
    ], string='Player Type', required=True)



