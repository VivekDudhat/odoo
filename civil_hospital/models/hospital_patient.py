from odoo import models,api,fields
import re
from datetime import date
from odoo.exceptions import ValidationError





class Patient(models.Model):
    _name = 'hospital.patient'
    _description = 'Patient'
    _rec_name = "patient_name"
    _inherit = ['mail.thread','mail.activity.mixin']

    patient_name = fields.Char(string='Patient Name',required=True)
    gender = fields.Selection([('male', 'Male'),('female','Female')])
    contact = fields.Char(string='Contact Number',required=True)
    date_of_birth = fields.Date(string='Date Of Birth')
    age = fields.Integer(string="Age", compute='_compute_age', store=True)
    email_id = fields.Char(string="Email", required=True)
    appointment_ids = fields.One2many('hospital.appointment', 'patient_id', string='Appointments')
    user_id = fields.Many2one('res.users', string="User", readonly=True)
    state  = fields.Selection([('active', 'Active'),('inactive','Inactive')], 
    default = "active",
    string="State"
    )
    cancel_uid = fields.Many2one(
        'res.users',
        string='Cancel'
        )
    cancelation_date   = fields.Datetime(string="Cancelation Date")
    patient_image = fields.Image('Image', max_width=1024, max_height=1024)
    # html = fields.Html()

    @api.constrains('email_id')
    #Method for validating the Patient Email ID
    def _check_email_format(self):
        for patient in self:
            if patient.email_id:
                # Regex for email id validation in the format
                email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
                if not re.match(email_regex, patient.email_id):
                    raise ValidationError("The email address is not in a valid format.")

    @api.depends('date_of_birth')
    #compute method to calculate the patient Age
    def _compute_age(self):
        for record in self:
            if record.date_of_birth:
                today = date.today()
                dob = record.date_of_birth
                
                record.age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            else:
                record.age = 0


    @api.constrains('contact')
    #Method for validating the Patient Contact
    def _check_contact_format(self):
        for patient in self:
            if patient.contact:
                # Regex for phone number validation in the format
                phone_regex = r'^\+?\d{1,4}\s?\d{10}$'
                if not re.match(phone_regex, patient.contact):
                    raise ValidationError("The contact number is not in a valid format. It should be in the format +<country_code> <phone_number> (e.g., +91 8780085668).")

    @api.model
    def create(self, values):
       if 'email_id' in values:
        # Search for an existing user with the same email
          user = self.env['res.users'].search([('login', '=', values['email_id'])], limit=1)
        
          # If no user is found, create a new user
          if not user:
            user_values = {
                'name': values.get('patient_name'),
                'login': values.get('email_id'),
                'email': values.get('email_id'),
                'password': 'admin',
                'groups_id': [(6, 0, [self.env.ref('civil_hospital.group_demo_user_new').id])],  # Assign user to a specific group
            }
            user = self.env['res.users'].create(user_values)
        
            # Associate the created or found user to the patient record
            values['user_id'] = user.id
    
            # Call the parent create method to create the patient record
            patient = super(Patient, self).create(values)
    
            return patient



    _sql_constraints = [
        # Ensure that email is unique
        ('unique_email', 'UNIQUE(email_id)', 'The email address must be unique for each patient.'),
    ]


    def action_active(self):
        self.state = "active"
    def action_inactive(self):
        self.state = "inactive"
    def action_server(self):
        for record in self:
            if record.state == "active":
                record.action_inactive




   


