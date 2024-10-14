from odoo import api, fields, models
from odoo.addons.test_impex.models import field


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
    # odoo will create a new table for Many2many fields
    # you can specify the table name 'patient_tag_rel'
    # the column name 'patient_id' and 'tag_id'
    tag_ids = fields.Many2many('patient.tag', 'patient_tag_rel', 'patient_id', 'tag_id', string="Tags")