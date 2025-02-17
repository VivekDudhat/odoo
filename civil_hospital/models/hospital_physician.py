from odoo import models, fields, api
import re
from odoo.exceptions import ValidationError

class HospitalPhysician(models.Model):
    _name = 'hospital.physician'
    _description = 'Hospital Physician'
    _rec_name = 'physician_name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    physician_name = fields.Char(string="Physician Name", required=True)
    contact_number = fields.Char(string='Contact Number')
    email = fields.Char(string="Email", required=True)
    specialization_id = fields.Many2one(
        string='Specialization',
        comodel_name='physician.speciality',
    )
    fees = fields.Float(
        string='Fees',
        compute='_compute_fees',
        store=True,  
    )
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')])
   

    user_id = fields.Many2one('res.users', string="User", readonly=True)

    @api.depends('specialization_id')
    def _compute_fees(self):
        for physician in self:
            physician.fees = physician.specialization_id.fees if physician.specialization_id else 0.0

    @api.constrains('email')
    def _check_email_format(self):
        for physician in self:
            if physician.email:
                email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
                if not re.match(email_regex, physician.email):
                    raise ValidationError("The email address is not in a valid format.")

    @api.constrains('contact_number')
    def _check_contact_number_format(self):
        for physician in self:
            if physician.contact_number:
                phone_regex = r'^\+?\d{1,4}\s?\d{10}$' 
                if not re.match(phone_regex, physician.contact_number):
                    raise ValidationError("The contact number must include a country code and be in a valid format (e.g., +123456789012).")

    
    
    @api.model
    def create(self, values):
        if 'email' in values:
            user = self.env['res.users'].search([('login', '=', values['email'])], limit=1)
            if not user:
                user_values = {
                    'name': values.get('physician_name'),
                    'login': values.get('email'),
                    'email': values.get('email'),
                    'password': 'admin',
                    'groups_id': [(6, 0, [self.env.ref('civil_hospital.group_admin_new').id])],  # Assign Admin rights
                }
                user = self.env['res.users'].create(user_values)
            
            values['user_id'] = user.id

        physician = super(HospitalPhysician, self).create(values)
        return physician

