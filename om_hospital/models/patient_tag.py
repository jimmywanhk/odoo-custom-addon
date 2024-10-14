from odoo import api, fields, models


class PatientTag(models.Model):
    # 6 fields are automatically created
    # create_date, create_uid, display_name
    # id, write_date, write_uid
    _name = 'patient.tag'
    _description = 'Patient Tag'

    name = fields.Char(string="Name", required=True)
