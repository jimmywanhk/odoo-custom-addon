from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


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

    # inherit unlink method
    # unlink method delete the record based on the given ID
    # you can add some logic here when deleting the record
    def unlink(self):
        print("super method is executed")
        #for order in self:
        #    if order.purchase_order:
        #        raise UserError(_('You cannot Delete this record'))
        for rec in self:
            domain = [('patient_id', '=', rec.id)]
            appointments = self.env['hospital.appointment'].search(domain)
            if appointments:
                # you can also use UserError
                raise ValidationError(_("You cannot delete the patient now.\nAppointment existing for this patient: %s" % rec.name))
        return super().unlink()