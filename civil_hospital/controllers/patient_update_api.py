from odoo import http
from odoo.http import request
import json
import re

class PatientController(http.Controller):

    @http.route('/api/update', type='json', auth='public', methods=['POST'], csrf=False)
    def update_patient(self, patient_id, **kwargs):
      
        # Fetch the patient record by ID
        patient = request.env['hospital.patient'].sudo().browse(patient_id)

        # Check if the patient exists
        if not patient.exists():
            return {
                'status': 'error',
                'message': 'Patient not found'
            }

     
        # Prepare the fields to update
        update_values = {key: value for key, value in kwargs.items() if value is not None}

        # Check if there are any fields to update
        if not update_values:
            return {
                'status': 'error',
                'message': 'No valid fields provided for update'
            }

        # Perform the update
        patient.sudo().write(update_values)

        # Return success response with updated patient details
        return {
            'status': 'success',
            'message': 'Patient updated successfully',
            'patient_id': patient.id,
            'patient_name': patient.patient_name,
            'updated_fields': update_values
        }