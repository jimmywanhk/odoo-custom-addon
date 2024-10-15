from odoo import api, fields, models


class HospitalAppointment(models.Model):
    # 6 fields are automatically created
    # create_date, create_uid, display_name
    # id, write_date, write_uid
    _name = 'hospital.appointment'
    _inherit = ['mail.thread']
    _description = 'Hospital Appointment'
    _rec_names_search = ['reference', 'patient_id']
    _rec_name = 'patient_id'

    reference = fields.Char(string="Reference", default="New")
    patient_id = fields.Many2one('hospital.patient', string="Patient")
    date_appointment = fields.Date(string="Date")
    note = fields.Text(string="Note")
    state = fields.Selection([('draft', 'Draft'), ('confirmed', 'Confirmed'), ('ongoing', 'Ongoing'), ('done', 'Done'), ('cancel', 'Cancelled')], default="draft")
    # hospital.appointment.line is the model name below
    appoint_line_ids = fields.One2many('hospital.appointment.line', 'appointment_id', string="Lines")

    # _compute_total_qty is the function name
    # we can add "store=True" attribute to store the field in the database
    # there are 2 types of compute field, store or non-store
    total_qty = fields.Float(compute='_compute_total_qty', string="Total Quantity", store=True)

    # we can add "store=True" attribute to store the field in the database
    # there are 2 types of related field, store or non-store
    date_of_birth = fields.Date(related='patient_id.date_of_birth', store=True)

    @api.model_create_multi
    def create(self, vals_list):
        print("odoo mates", vals_list)
        for vals in vals_list:
            if not vals.get('reference') or vals['reference'] == 'New':
                vals['reference'] = self.env['ir.sequence'].next_by_code('hospital.appointment')
        return super().create(vals_list)

    # when you create a stored compute field, you need to specify
    # the dependency when the field recompute
    @api.depends('appoint_line_ids', 'appoint_line_ids.qty')
    def _compute_total_qty(self):
        for rec in self:
            rec.total_qty = sum(rec.appoint_line_ids.mapped('qty'))
            #total_qty = 0
            #print(rec.appoint_line_ids)
            #for line in rec.appoint_line_ids:
            #    total_qty += line.qty
            #rec.total_qty = total_qty

    def _compute_display_name(self):
        for rec in self:
            print("value is", f"[{rec.reference}] {rec.patient_id.name}")
            rec.display_name = f"[{rec.reference}] {rec.patient_id.name}"

    def action_confirm(self):
        for rec in self:
            print("button is clicked", self, rec)
            print("reference...", self.reference)
            print("note...", self.note)
            rec.state = 'confirmed'

    def action_ongoing(self):
        for rec in self:
            rec.state = 'ongoing'

    def action_done(self):
        for rec in self:
            rec.state = 'done'

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'

# you can add multiple models in the same file or separate file
class HospitalAppointmentLine(models.Model):
    _name = 'hospital.appointment.line'
    _description = 'Hospital Appointment Line'

    appointment_id = fields.Many2one('hospital.appointment', string="Appointment")
    product_id = fields.Many2one('product.product', string="Product", required=True)
    qty = fields.Float(string="Quantity")