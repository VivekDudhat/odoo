from odoo import fields, api, models

class Hospital_Medicine(models.Model):
    _name = "hospital.medicine"
    _description = "Medicine"
    _rec_name = "medicine_name"  

    medicine_name = fields.Char(string="Medicine Name")
    medicine_cost = fields.Float(string="Price")

    image = fields.Image('Image', max_width=1024, max_height=1024)

    total_cost = fields.Float(string="Total Cost", compute="_compute_total_cost", store=True)

    display_name = fields.Char(string="Display Name", compute="_compute_display_name", store=True)

  
   


    @api.depends('medicine_cost')
    def _compute_total_cost(self):
        for record in self:
            record.total_cost += record.medicine_cost
