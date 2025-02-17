from odoo import http
from odoo.http import request
import requests

class ExternalAPI(http.Controller):

    @http.route('/api/external', type='json', auth='none', methods=['POST'], csrf=False)
    def external(self, disease_input, **kwargs):
        if not disease_input:
            return {"status": "error", "message": "Disease name is required"}

        # Base URL of the external API
        url = "https://67a9c9566e9548e44fc4dfea.mockapi.io/api/hospital/disease"

        # Request to the external API
        response = requests.get(url)

        if not response:
            return {"status": "error", "message": f"Failed to fetch data from external API. Status code: {response.status_code}"}

        data = response.json()

        matching_remedies = []
        matching_doctors = []

        # Find all matching disease
        for disease in data:
            if disease.get('dieseas', '').lower() == disease_input.lower():
                # remedies and doctors for each matching disease
                remedies = disease.get('Remedies', [])
                doctors = disease.get('Doctor', [])
                
                full_remedies = ''.join(remedies)
                full_doctors = ''.join(doctors)
           
                matching_remedies.append(full_remedies)
                matching_doctors.append(full_doctors)

        if matching_remedies or matching_doctors:
            return {
                "status": "success",
                "disease_name": disease_input,
                "remedies": matching_remedies,
                "doctors": matching_doctors
            }
        
        # If no matching disease found
        return {"status": "error", "message": f"No details found for the disease: {disease_input}"}
