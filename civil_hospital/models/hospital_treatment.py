from odoo import api,fields,models



class Hospital_Treatment(models.Model):
    _name  = "hospital.treatment"
    _description = "Hospital treatment"
    _rec_name = "patient_id"



    patient_id = fields.Many2one(
        'hospital.patient',
        string='Patient Name',
        )

  

    medicines = fields.Many2many(
        'hospital.medicine',
        'treatment_medicine_rel', 
        'treatment_id',  
        'medicine_id',  
        string='Medicines'
    )

    # Total cost of the treatment computed from the selected medicines
    total_cost = fields.Float(
        string="Total Cost",
        compute='_compute_total_cost',
        store=True
    )

    @api.depends('medicines.medicine_cost',)
    def _compute_total_cost(self):
        for record in self:
            total = 0
            for medicine in record.medicines:
                total += medicine.medicine_cost  # Add medicine cost
            record.total_cost = total