from odoo import http
from odoo.http import request
from odoo.exceptions import ValidationError

class PatientRegistrationController(http.Controller):
    @http.route('/patient/form', type='http', auth="public",website=True,csrf=False)
    def patient_form(self):
        return request.render('civil_hospital.patient_form')

    #Method for Form Submitation
    @http.route('/patient/form/submit', type='http', auth="public", website=True,csrf=False)
    def submit_patient_form(self, **post):
        # Create a new patient record
        patient_obj = request.env['hospital.patient'].sudo()

        patient_data = {
            'patient_name': post.get('patient_name'),
            'gender': post.get('gender'),
            'contact': post.get('contact'),
            'date_of_birth': post.get('date_of_birth'),
            'email_id': post.get('email_id'),
        }
        # Create the patient record in the database
        patient_obj.create(patient_data)
        # Redirect to success page
        return request.render('civil_hospital.patient_form_success')

    # Method for appointment Form
    @http.route('/patient_appointment/form', type='http', auth="public",website=True,csrf=False)
    def patient_appointment_form(self):
        return request.render('civil_hospital.patient_appointment_form')
          
    #method for Appointment Booking
    @http.route('/create_appointment', auth='public', website=True, csrf=False)
    def create_appointment(self, **kwargs):
        if request.httprequest.method == 'POST':
            # Retrieve the values from the form
            patient_id = kwargs.get('patient_id')
            doctor_id = kwargs.get('doctor_id')
            appointment_date = kwargs.get('appointment_date')
            time_slot = kwargs.get('time_slot')

            # Create the appointment
            try:
                # Create an appointment record
                appointment = request.env['hospital.appointment'].sudo().create({
                    'patient_id': patient_id,
                    'doctor_id': doctor_id,
                    'appointment_date': appointment_date,
                    'time_slot': time_slot,
                    'state': 'draft',  # Default state
                })
              
            except ValidationError as e:
                return request.render('your_module.error_page', {'error_message': str(e)})
        else:
            doctors = request.env['hospital.physician'].sudo().search([])
            # Retrieve available time slots based on the selected doctor
            time_slots = request.env['hospital.appointment'].sudo().get_time_slots()
            return request.render('civil_hospital.create_appointment_form', {'doctors': doctors, 'time_slots': time_slots})

    @http.route('/patient_appointment/form', type='http', auth="public", website=True)
    def patient_appointment_form(self):
        time_slots = request.env['hospital.appointment'].search([])
        patients = request.env['hospital.patient'].search([])
        doctors = request.env['hospital.physician'].search([])  
        return request.render('civil_hospital.patient_appointment_form', {
            'doctors': doctors,
            'patients' : patients,
            'time_slots' : time_slots
        })
    


  