from odoo import http
from odoo.http import request
from datetime import datetime

class PatientAPI(http.Controller):
    
    @http.route('/api/delete', type='json', auth='public', methods=['POST'], csrf=False)
    def cancel_patient(self, patient_id):
        # Check if the patient exists
        patient = request.env['hospital.patient'].sudo().browse(patient_id)
        if not patient.exists():
            return {'error': 'Patient not found'}

        # Check the patient is active before changing
        if patient.state != 'active':
            return {'error': 'Patient is not in an active state'}

        # Update the patient state to 'inactive' and set cancellation details
        patient.state = 'inactive'
        patient.cancel_uid = request.env.user.id  # Set the cancel user ID (currently logged-in user)
        patient.cancelation_date = datetime.now()  # Set the current datetime as cancellation date

        # Return the change details details
        return {
            'patient_id': patient.id,
            'state': patient.state,
            'cancel_uid': patient.cancel_uid.id,
            'cancelation_date': patient.cancelation_date
        }