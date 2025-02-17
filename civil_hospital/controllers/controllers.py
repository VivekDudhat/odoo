from odoo import http
from odoo.http import request
import json
import re

class PatientAPI(http.Controller):

    @http.route('/api/patients', type='json', auth='user', methods=['POST'], csrf=False)
    
    def patients(self, gender=None, patient_email=None, age=None, state=None, patient_name=None, **kwargs):
        domain = [("state","=","active")]
        # Email regex pattern for validation
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        # Validate gender
        if gender:
            gender = gender.lower()
            if isinstance(gender, int):
                return {"status": "error", "message": "Gender cannot be a number"}
            if gender not in ["male", "female"]:
                return {"status": "error", "message": "Gender can be either male or female"}
            domain.append(('gender', '=', gender))

        # Validate email
        if patient_email:
            patient_email = patient_email.lower()
            if not re.match(email_regex, patient_email):
                return {"status": "error", "message": "Invalid email format"}
            domain.append(('email_id', '=', patient_email))

        # Validate age
        if age is not None:
            if age == "":
                return {"status": "error", "message": "Age cannot be an empty string"}
            try:
                age = int(age)
                if age < 0:
                    return {"status": "error", "message": "Age cannot be negative"}
                domain.append(('age', '=', age))
            except ValueError:
                return {"status": "error", "message": "Age must be a valid number"}

        # Validate patient name
        if patient_name:
            patient_name = patient_name.lower()
            domain.append(('patient_name', '=', patient_name))

        # If no valid parameters were provided
        if not domain:
            return {"status": "error", "message": "At least one valid parameter is required"}

        # Search for patients
        patients = request.env['hospital.patient'].sudo().search(domain)

        #  if  patient matches the input but is inactive
        inactive_patients = patients.filtered(lambda p: p.state == 'inactive')
        if inactive_patients:
            return {"status": "error", "message": "Not an active patient"}

        # only active patients
        active_patients = patients.filtered(lambda p: p.state != 'inactive')

     
        result = []
        for patient in active_patients:
            result.append({
                'id': patient.id,
                'patient_name': patient.patient_name,
                'gender': patient.gender,
                'contact': patient.contact,
                'age': patient.age,
                'patient_email': patient.email_id,
                'state': patient.state
            })

        # If  matching resullts, return else return an error
        if result:
            return {
                "status": "success",
                "patient_details": result
            }
        else:
            return {"status": "error", "message": "No matching data found"}