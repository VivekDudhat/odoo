from odoo import models, api, fields
from datetime import  time,datetime, timedelta,date
from odoo.exceptions import ValidationError


class Appointment(models.Model):
    
    _name = 'hospital.appointment'
    _description = 'Appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin',]
    _rec_name = "patient_id"

    user_id = fields.Many2one('res.users', string="User")
    patient_id = fields.Many2one(
        "hospital.patient", 
        string='Patient Name', 
        required=True, 
        tracking=True
    )
    email_id = fields.Char(related='patient_id.email_id',readonly=True,store=True,tracking = True,string='Email')
    doctor_id = fields.Many2one(
        'hospital.physician', 
        string='Doctor', 
        required=True, 
        tracking=True
    )
    specialization = fields.Many2one('physician.speciality', related='doctor_id.specialization_id',readonly=True,store=True,tracking = True)
    consultant_charge = fields.Float(string='Consultant Fee', related='doctor_id.fees', readonly=True, store=True)
    appointment_date = fields.Date(
        string='Appointment Date', 
        required=True, 
        tracking=True
    )
    new_appointment = fields.Date(string="New Appointment")
    time_slot = fields.Selection(
        selection="get_time_slots", 
        string='Time Slot', 
        required=True, 
        tracking=True
    )
    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('confirmed', 'Confirmed'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled')
        ],
        default='draft',
        string='State',
        tracking=True
    )
    medicine_ids = fields.Many2many(
        'hospital.medicine', 
        'appointment_medicine_rel', 
        'appointment_id', 
        'medicine_id', 
        string="Medicines"
    )
    total_medicine_cost = fields.Float(
        string="Total Medicine Cost", 
        compute='_compute_medicine_total_cost', 
        store=True
    )
    begin_date = fields.Date(string="Start Date" )
    end_date = fields.Date(string="End Date")
    total_cost = fields.Float(string='Total Cost',compute = '_compute_field')
    physician_count = fields.Integer(compute='_compute_physician_count', string="Physician Count")
   
    #compute method compute total cost
    @api.depends('patient_id','state')
    def _compute_field(self):
        for record in self:

            if record.patient_id:
                appointments = self.search([('patient_id','=',record.patient_id.id),('state','=','completed')])
                record.total_cost = sum(appointment.consultant_charge for appointment in appointments)
            else:
                record.total_cost = 0.0

    @api.depends('medicine_ids')
    def _compute_medicine_total_cost(self):
        for record in self:
            record.total_medicine_cost = sum(medicine.medicine_cost for medicine in record.medicine_ids)
    
    
    #Methods for appointments
    @api.model
    def get_time_slots(self):
        slots = []
        start_time = datetime.strptime("08:00", "%H:%M")
        end_time = datetime.strptime("18:00", "%H:%M")
        slot_duration = 30  # Duration in minutes

        # Get doctor and date from context
        doctor_id = self.doctor_id
        appointment_date = self.appointment_date
        booked_slots = []
        if doctor_id and appointment_date:
            # Fetch booked slots for confirmed appointments
            appointments = self.search([
                ('doctor_id', '=', doctor_id.id),
                ('appointment_date', '=', appointment_date),
                ('state', '=', 'confirmed')  # Only consider confirmed appointments
            ])
            booked_slots = [appt.time_slot for appt in appointments]

        while start_time < end_time:
            slot_start = start_time
            slot_end = start_time + timedelta(minutes=slot_duration)
            slot = f"{slot_start.strftime('%H:%M')} - {slot_end.strftime('%H:%M')}"
            
            # Extract just the slot strings if booked_slots contains tuples
            booked_slot_strings = [bs[0] if isinstance(bs, tuple) else bs for bs in booked_slots]
            
            if slot.strip() not in [bs.strip() for bs in booked_slot_strings]:
                slots.append((slot, slot))
                start_time = slot_end
        return slots

    
    @api.model
    def send_appointment_reminders(self):
        # Get all appointments for the next day
        today = fields.Date.today()
        tomorrow = today + timedelta(days=1)
        appointments = self.search([('appointment_date', '=', tomorrow), ('state', '=', 'confirmed')])

        for appointment in appointments:
            # Send an email reminder to the patient
            mail_template = self.env.ref('civil_hospital.email_template_confirm')
            mail_template.send_mail(appointment.id, force_send=True)

    @api.onchange('doctor_id', 'appointment_date')
    def _onchange_doctor_date(self):
        #Set context dynamically when doctor or date changes.
        if self.doctor_id and self.appointment_date:
            self = self.with_context(
                doctor_id=self.doctor_id.id,
                appointment_date=self.appointment_date
          )

    @api.constrains('appointment_date', 'time_slot', 'doctor_id')
    def _check_slot_availability(self):
        #Ensure no overlapping appointments for the same doctor, date, and time slot.
        for record in self:
            overlapping_appointments = self.search([
                ('doctor_id', '=', record.doctor_id.id),
                ('appointment_date', '=', record.appointment_date),
                ('time_slot', '=', record.time_slot),
                ('id', '!=', record.id),
                ('state', '=', 'confirmed')  # Only consider confirmed appointments
            ])
            if overlapping_appointments:
                raise ValidationError(
                    f"The doctor is already booked for the selected time slot: {record.time_slot} ."
                )
 
    def _compute_physician_count(self):
        # Count the total number of physicians
        total_physicians = self.env['hospital.physician'].search_count([])
        for record in self:
            record.physician_count = total_physicians

    def action_view_physician(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Physician',
            'res_model': 'hospital.physician',
            'view_mode': 'tree',
            'view_id': self.env.ref('civil_hospital.view_hospital_physician_tree').id,
            'res_id': self.doctor_id.id,
            'target': 'current',
        }

    def action_open_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Download Appointmnet in Excel',
            'res_model': 'appointment.wizard',
            'view_mode': 'form',
            'target': 'new',
        }
    def send_mail(self,mail):
        mail_template = self.env.ref(mail)
        mail_template.send_mail(self.id, force_send=True)

    def action_confirm(self):
      
        self.state = 'confirmed'
        self.send_mail("civil_hospital.email_template_confirm")

    def action_completed(self):
    
        self.state = 'completed'
        self.send_mail("civil_hospital.email_template_completed")

    def action_cancel(self):
      
        self.state = 'cancelled'
        self.send_mail("civil_hospital.email_template_cancelled")

    def action_draft(self):
        
        self.state = 'draft'

    def name_get(self):
        result = []
        for record in self:
        # patient name might be missing
            patient_name = record.patient_id.patient_name if record.patient_id else 'No Patient'
        
        #  specialization might be missing through doctor
            specialization_name = record.doctor_id.specialization_id.name if record.doctor_id and record.doctor_id.specialization_id else 'No Specialization'
        
        # Combine patient name and doctor's specialization
            name = f"{patient_name} - {specialization_name}"
        result.append((record.id, name))
    
        return result

 
  
    def _get_report_values(self, docids, data=None):
        
        appointment = self.env['hospital.appointment'].browse(docids)
       
        appointments = self.env['hospital.appointment'].search([('patient_id', '=', appointment.patient_id.display_name)])

        import pdb;pdb.set_trace()

        return {
            'docs': appointments,  # Pass all appointments of the same patient to the template
        }
    def print_report(self):
        return self.env.ref('civil_hospital.action_report_hospital_appointment').report_action(self)


   
   
    


    