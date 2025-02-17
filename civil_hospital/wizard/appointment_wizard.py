from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import xlsxwriter
import base64
from io import BytesIO
from datetime import datetime



class AppointmentWizard(models.TransientModel):
    _name = "appointment.wizard"
    _description = "Appointment Wizard"


    begin_date = fields.Date(string="Start Date", required=True)
    end_date = fields.Date(string="End Date", required=True)



    @api.constrains('begin_date','end_date')
    def _check_begin_date(self):
        for record in self:
            if record.end_date < record.begin_date:
                raise ValidationError("The End Date can not be earlier than Begin Date")

    
    def export_xslx(self):
        self.ensure_one()

        appointments = self.env['hospital.appointment'].search([('appointment_date' , '>=', self.begin_date),('appointment_date', '<=' , self.end_date)])
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet('Appointments')


        headers = [
            'Patient Name', 
            'Doctor', 
            'Specialization',
            'Appointment Date',
            'Time Slot',
            'State',
            'Consultant Fee',
            'Total Medicine Cost',
            'Total Cost'
        ]




        for col, header in enumerate(headers):
            worksheet.write(0, col, header)

        # Write data in rows
        for row, appointment in enumerate(appointments, start=1):
            worksheet.write(row, 0, appointment.patient_id.patient_name)
            worksheet.write(row, 1, appointment.doctor_id.physician_name)
            worksheet.write(row, 2, appointment.specialization.name)
            worksheet.write(row, 3, str(appointment.appointment_date))
            worksheet.write(row, 4, appointment.time_slot)
            worksheet.write(row, 5, appointment.state)
            worksheet.write(row, 6, appointment.consultant_charge)
            worksheet.write(row, 7, appointment.total_medicine_cost)
            worksheet.write(row, 8, appointment.total_cost)

        workbook.close()
        output.seek(0)
        excel_data = base64.b64encode(output.read())

        # Create attachment
        attachment = self.env['ir.attachment'].create({
            'name': f'appointments_report_{self.begin_date}_{self.end_date}.xlsx',
            'type': 'binary',
            'datas': excel_data,
            'store_fname': 'Appointments Report.xlsx',
            'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        })

        # Return download action
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{attachment.id}?download=true',
            'target': 'self',
        }
            
    def action_appointment(self):
        return self.export_xslx()