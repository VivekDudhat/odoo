from odoo import fields,api,models


class Physician_Speciality(models.Model):
    _name = "physician.speciality"
    _description = "Physician Speciality"
    
    name = fields.Char(string="Specialty Name", required=True)
    code = fields.Char(string="Specialty Code", required=True, unique=True)
    fees = fields.Float(string="Fees of Physician",required=True)
    specialization_id = fields.Many2one('specialization.model', string='Specialization')


    _sql_constraints = [
    ('unique_code', 'unique(code)', 'The code must be unique!')
]




