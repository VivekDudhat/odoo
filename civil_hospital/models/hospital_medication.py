from odoo import api,fields,models


class Medication(models.Model):
    _name = "hospital.medication"
    _description = "Medication"