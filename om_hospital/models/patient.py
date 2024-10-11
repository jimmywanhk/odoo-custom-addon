from odoo import api, fields, models


class HospitalPatient(models.Model):
    # 6 fields are automatically created
    # create_date, create_uid, display_name
    # id, write_date, write_uid
    _name = 'hospital.patient'
    _inherit = ['mail.thread']
    _description = 'Patient Master'

    name = fields.Char(string="Name", required=True, tracking=True)
    date_of_birth = fields.Date(string="DOB", tracking=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string="Gender", tracking=True)