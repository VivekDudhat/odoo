from odoo import http
from odoo.http import request
import re

class PatientController(http.Controller):

    @http.route('/api/create', type='json', auth='user', methods=['POST'], csrf=False)
    def create_patient(self, patient_name, gender, contact, date_of_birth, email_id, **kwargs):
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        
        # Check if the required fields are provided
        if not patient_name or not gender or not contact or not date_of_birth or not email_id:
            return {
                'status': 'error',
                'message': 'Missing required fields'
            }

        # Check if a patient with the same name already exists
        existing_patient_by_name = request.env['hospital.patient'].sudo().search([('patient_name', '=', patient_name)],)
        if existing_patient_by_name:
            return {
                'status': 'error',
                'message': 'A patient with this name already exists'
            }

        # Check if a patient with the same email already exists
        existing_patient_by_email = request.env['hospital.patient'].sudo().search([('email_id', '=', email_id)])
        if existing_patient_by_email:
            return {
                'status': 'error',
                'message': 'A patient with this email already exists'
            }
        existing_patient_by_contact = request.env['hospital.patient'].sudo().search([('contact', '=',contact)],)
        if existing_patient_by_contact:
            return{
                "status" : "error" ,
                "mesasage":"A patient same contact already exists"
            }
        
        if not re.match(email_regex, email_id):
            return {"status": "error", "message": "Invalid email"}

        

        # values for creating the new patient record
        patient_values = {
            'patient_name': patient_name,
            'gender': gender,
            'contact': contact,
            'date_of_birth': date_of_birth,
            'email_id': email_id,
        }

        # Create the patient record
        patient = request.env['hospital.patient'].sudo().create(patient_values)

        # Check if the patient creation was successful
        if patient:
            return {
                'status': 'success',
                'message': 'Patient created successfully',
                'patient_id': patient.id,
                'patient_name': patient.patient_name,
                'gender': patient.gender,
                'contact': patient.contact,
                'date_of_birth': patient.date_of_birth,
                'email_id': patient.email_id
            }
        else:
            return {
                'status': 'error',
                'message': 'Failed to create patient record'
            }
