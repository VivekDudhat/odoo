from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError
from odoo import fields


class PatientTest(TransactionCase):

    # import pdb;pdb.set_trace()


    def setUp(cls):
    
        
        # Create necessary records or mock data if required
        cls.group_demo_user_new = cls.env.ref('civil_hospital.group_demo_user_new')
        print("******")

    
    def test_email_format_validation(self):
        # Test invalid email format
        with self.assertRaises(ValidationError):
            self.env['hospital.patient'].create({
                'patient_name': 'Test Patient',
                'contact': '+91 8780085668',
                'email_id': 'invalid-email',  # Invalid email format
                'date_of_birth': '1990-01-01'
            })
        
        # Test valid email format
        patient = self.env['hospital.patient'].create({
            'patient_name': 'Test Patient',
            'contact': '+91 8780085668',
            'email_id': 'test@example.com',  # Valid email format
            'date_of_birth': '1990-01-01'
        })
     
        print("******")

  

    def test_age_computation(self):
        # Create a patient and check if the age is computed correctly
        patient = self.env['hospital.patient'].create({
            'patient_name': 'Test Patient',
            'contact': '+91 8780085668',
            'email_id': 'test@example.com',
            'date_of_birth': '1990-01-01'
        })
        today = fields.Date.today()
        expected_age = today.year - 1990 - ((today.month, today.day) < (1, 1))  # Expected age calculation
        self.assertEqual(patient.age, expected_age)
        print("******")

