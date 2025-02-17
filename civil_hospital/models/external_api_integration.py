from odoo import fields, api, models
import requests
from odoo.exceptions import UserError


class HospitalRemedy(models.Model):
    _name = 'hospital.remedy'
    _description = 'Hospital Remedy'

    name = fields.Char(string='Remedy', required=True)

class HospitalDoctor(models.Model):
    _name = 'hospital.doctor'
    _description = 'Hospital Doctor'

    name = fields.Char(string='Doctor', required=True)


class HospitalDisease(models.Model):
    _name = 'hospital.disease.api'
    _description = 'Hospital Disease Data'
    _rec_name = "disease_input"

    disease_input = fields.Char(string='Disease', required=True)
    remedies = fields.Many2many('hospital.remedy', string='Remedies')
    doctors = fields.Many2many('hospital.doctor', string='Consultant(s)')

    def fetch_disease_data(self):
        # Base URL of the external API
        base_url = "https://67a9c9566e9548e44fc4dfea.mockapi.io/api/hospital"
        endpoint = "disease" 
        url = f"{base_url}/{endpoint}"

        # request to the external API
        response = requests.get(url)
   
        if response:
     
            data = response.json()

        
            remedies_list = []
            doctors_list = []

            # Search for matching diseases in the API response
            for item in data:
                if item.get('dieseas', '').lower() == self.disease_input.lower():
                    # Create new remedy and doctor records in Odoo
                    remedy = self.env['hospital.remedy'].create({'name': item.get('Remedies', '')})
                    doctor = self.env['hospital.doctor'].create({'name': item.get('Doctor', '')})

                    remedies_list.append(remedy)
                    doctors_list.append(doctor)

            # If no matching disease was found
            if not remedies_list:
                raise UserError(f"No data found for the disease: {self.disease_input}")

            # Auto the doctor and remedi field matching deisease
            self.write({
                'remedies': [(6, 0, [remedy.id for remedy in remedies_list])],
                'doctors': [(6, 0, [doctor.id for doctor in doctors_list])],
            })
        else:
            # response was not successful
            raise UserError(f"Failed to fetch data from external API. Status code: {response.status_code}")
