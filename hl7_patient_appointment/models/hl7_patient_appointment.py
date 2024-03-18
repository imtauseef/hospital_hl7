import socket
from datetime import datetime
from odoo.exceptions import ValidationError
from odoo import models, fields, api, _
import hl7
from .hl7_codes_dictionary import APPOINTMENT_REASON_CODE, FILLER_STATUS_CODE, AIL_LOCATION_TYPE_CODE, \
    AIP_RESOURCE_STAFF_TYPE_CODE
import pytz


class Appointment(models.Model):
    _inherit = "hms.appointment"

    message_control_id = fields.Char(string='Message Control ID')
    appointment_reason = fields.Selection([
        ('CHECKUP', 'A routine check-up, such as an annual physical'),
        ('EMERGENCY', 'EMERGENCY room'),
        ('FOLLOWUP', 'A follow up visit from a previous appointment'),
        ('ROUTINE', 'Routine appointment - default if not valued'),
        ('WALKIN', 'A previously unscheduled walk-in visit'),
    ], string='Appointment Reason')
    filler_appointment_id = fields.Char(string='Filler appointment ID')
    occurrence_number = fields.Char(string='Occurrence Number')
    filler_contact_person = fields.Char(string='Filler Contact Person')
    appointment_mode = fields.Selection([
        ('1', 'In-Person Appointment'),
        ('2', 'Virtual Appointment'),
    ], string='Appointment Mode')

    filler_status_code = fields.Selection([
        ('Blocked', 'The indicated time slot(s) is(are) blocked'),
        ('Booked', 'The indicated appointment is booked'),
        ('Cancelled', 'The indicated appointment was stopped from occurring (canceled prior to starting)'),
        ('Completed', 'The indicated appointment has completed normally (was not discontinued, canceled, or deleted)'),
        ('Dc', "The indicated appointment was discontinued (DC'ed while in progress, discontinued parent appointment, or discontinued child appointment)"),
        ('Deleted', 'The indicated appointment was deleted from the filler application'),
        ('Noshow', 'The patient did not show up for the appointment'),
        ('Overbook', 'The appointment has been confirmed; however it is confirmed in an overbooked state'),
        ('Pending', 'Appointment has not yet been confirmed'),
        ('Started', 'The indicated appointment has begun and is currently in progress'),
        ('Waitlist', 'Appointment has been placed on a waiting list for a particular slot, or set of slots'),
    ], string='Filler Status Code')

    # added for RGS segment
    rgs_action_code = fields.Selection([('A', 'Add/Insert'), ('D', 'Delete'), ('U', 'Update')], string="Action Code")

    # added for AIS segment
    ais_action_code = fields.Selection([('A', 'Add/Insert'), ('D', 'Delete'), ('U', 'Update')], string="Action Code")
    aig_action_code = fields.Selection([('A', 'Add/Insert'), ('D', 'Delete'), ('U', 'Update')], string="Action Code")
    ail_action_code = fields.Selection([('A', 'Add/Insert'), ('D', 'Delete'), ('U', 'Update')], string="Action Code")
    aip_action_code = fields.Selection([('A', 'Add/Insert'), ('D', 'Delete'), ('U', 'Update')], string="Action Code")
    hospital_service_id = fields.Many2one('hospital.service', string="Speciality")
    ais_start_date_time = fields.Datetime(string='Start Date/Time')
    ais_universal_service_identifier_code = fields.Integer(string='Universal Service Identifier Code')
    ais_universal_service_identifier_name = fields.Integer(string='Universal Service Identifier Name')
    aig_start_date_time = fields.Datetime(string='Start Date/Time')
    ail_start_date_time = fields.Datetime(string='Start Date/Time')
    aip_start_date_time = fields.Datetime(string='Start Date/Time')
    aig_resource_id = fields.Integer(string='Resource ID')
    aig_resource_name = fields.Integer(string='Resource Name')
    aig_resource_type_id = fields.Integer(string='Resource Type ID')
    aig_resource_type_name = fields.Integer(string='Resource Type Name')
    ail_location_type = fields.Selection([
        ('C', 'Clinic'),
        ('D', 'Department'),
        ('H', 'Home'),
        ('N', 'Nursing Unit'),
        ('O', 'Provider’s Office'),
        ('P', 'Phone'),
        ('S', 'SNF'),
    ], string='Location Type-AIL')
    aip_resource_staff_type = fields.Selection([
        ('PHYSN', 'Physician'),
        ('NURSE', 'Nurse'),
        ('RADLOGST', 'Radiologist'),
        ('PHYSIOTHPST', 'Physiotherapist'),
        ('SOCWRKR', 'Social worker'),
        ('OCCRTHPST', 'Occupational therapist'),
        ('OTHERALLDHLTH', 'Other Allied health'),
    ], string='Resource/Staff Type')

    @api.model
    def generate_hl7_message(self, integration_record):
        local_tz = pytz.timezone('Asia/Dubai')
        local_time = datetime.now(local_tz)
        self.patient_id.patient_identifier_list

        hl7_message = (
            f"MSH|^~\&|SYSTEMCODE^SYSTEMCODE|SYSTEMCODE^SYSTEMCODE|Rhapsody^MALAFFI|ADHIE|{local_time.strftime('%Y%m%d%H%M%S')}+0400||SIU^S12|{integration_record.message_control_id}|P|2.3\n"
            f"SCH||{integration_record.filler_appointment_id}^^SYSTEMCODE|{integration_record.occurrence_number}||||{integration_record.appointment_reason}^{APPOINTMENT_REASON_CODE[integration_record.appointment_reason]}^MALAFFI||||^^^{integration_record.date}^{integration_record.date_to}|||||{integration_record.filler_contact_person}||||||{integration_record.appointment_mode}^MALAFFI|||{integration_record.filler_status_code}^MALAFFI||\n"
            # f"ODE||||1|||Booked^The indicated appointment is booked^MALAFFI||\n"
        )

        if integration_record.patient_id.death_indicator == 'Y':
            hl7_message += (
                f"PID|1||{integration_record.patient_id.code}^^^&SYSTEMCODE||{integration_record.patient_id.name}^^^^^^P||{integration_record.patient_id.birthday:%Y%m%d}|{integration_record.patient_id.gender_code}||||||{integration_record.patient_id.business_contact_no}^^CC||{integration_record.patient_id.marital_status_code}^{integration_record.patient_id.marital_status}^MALAFFI|{integration_record.patient_id.religion_hl7}||{integration_record.patient_id.emirates_id}|||||||||{integration_record.patient_id.nationality_code}^{integration_record.patient_id.nationality_id.name}^MALAFFI|{integration_record.patient_id.date_of_death:%Y%m%d}|{integration_record.patient_id.death_indicator}\n"
            )
        else:
            hl7_message += (
                f"PID|1||{integration_record.patient_id.code}^^^&SYSTEMCODE||{integration_record.patient_id.name}^^^^^^P||{integration_record.patient_id.birthday:%Y%m%d}|{integration_record.patient_id.gender_code}||||||{integration_record.patient_id.business_contact_no}^^CC||{integration_record.patient_id.marital_status_code}^{integration_record.patient_id.marital_status}^MALAFFI|{integration_record.patient_id.religion_hl7}||{integration_record.patient_id.emirates_id}|||||||||{integration_record.nationality_code}^{integration_record.nationality_id.name}^MALAFFI||{integration_record.patient_id.death_indicator}\n"
            )

        hl7_message += (
            # f"PV1|1|O|CARDIOLOGY^^^MF123&SYSTEMCODE-DOHID||||||GD11111^Test1^test4^^^^^^&SYSTEMCODE-DOHID|162||||P|||||101^^^&SYSTEMCODE|||||||||||||||||8||||||||20210114120000|20210114120000\n"
            f"RGS|1|{integration_record.rgs_action_code}|\n"
            f"AIS|1|{integration_record.ais_action_code}|{integration_record.ais_universal_service_identifier_code}^{integration_record.ais_universal_service_identifier_name}^SYSTEMCODE^{integration_record.hospital_service_id.code}^{integration_record.hospital_service_id.name}^MALAFFI|{integration_record.ais_start_date_time:%Y%m%d%H%M%S}||||||{integration_record.filler_status_code}^{FILLER_STATUS_CODE[integration_record.filler_status_code]}^MALAFFI||\n"
            f"AIG|1|{integration_record.aig_action_code}|{integration_record.aig_resource_id}^{integration_record.aig_resource_name}^SYSTEMCODE^^^^|{integration_record.resource_type_id}^{integration_record.resource_type_name}^SYSTEMCODE||||{integration_record.ais_start_date_time:%Y%m%d%H%M%S}||||||{integration_record.filler_status_code}^{FILLER_STATUS_CODE[integration_record.filler_status_code]}^MALAFFI\n"
            f"AIL|1|{integration_record.ail_action_code}|CARDIOLOGY^^^MF123&SYSTEMCODE-DOHID|{integration_record.ail_location_type}^{AIL_LOCATION_TYPE_CODE[integration_record.ail_location_type]}^MALAFFI||{integration_record.ail_start_date_time:%Y%m%d%H%M%S}||||||{integration_record.filler_status_code}^{FILLER_STATUS_CODE[integration_record.filler_status_code]}^MALAFFI\n"
            f"AIP|1|{integration_record.aip_action_code}|{integration_record.patient_id.id}^{integration_record.patient_id.name}^^^^^^&SYSTEMCODE-DOHID|{integration_record.aip_resource_staff_type}^{AIP_RESOURCE_STAFF_TYPE_CODE[integration_record.aip_resource_staff_type]}^MALAFFI||{integration_record.aip_start_date_time:%Y%m%d%H%M%S}||||||{integration_record.filler_status_code}^{FILLER_STATUS_CODE[integration_record.filler_status_code]}^MALAFFI\n"
        )
        return hl7_message

    @api.model
    def send_hl7_message(self, hl7_message, external_system_ip, external_system_port):
        try:
            # Establish connection to the external system
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((external_system_ip, external_system_port))

                # Send the HL7 message
                s.sendall(hl7_message.encode('utf-8'))

                print("HL7 Message Sent Successfully:", hl7_message)

                # If needed, receive and handle acknowledgment
                # acknowledgment = s.recv(1024)
                # handle_acknowledgment(acknowledgment)
        except Exception as e:
            print("Error Sending HL7 Message:", e)

    @api.model
    def generate_outgoing_hl7_message(self, integration_record_id):
        try:
            integration_record = self.browse(integration_record_id)
            hl7_message = self.generate_hl7_message(integration_record)
            print("Generated HL7 Message:", hl7_message)

            external_system_ip = '127.0.0.1'  # Replace with the actual IP address
            external_system_port = 1234  # Replace with the actual port number

            self.send_hl7_message(hl7_message, external_system_ip, external_system_port)

            # Display acknowledgment message
            acknowledgment_message = (
               f"HL7 Message for Patient Registration has been created Successfully and sent to the designated Server.")

            return self.display_acknowledgment_message(acknowledgment_message)

        except Exception as e:
            error_message = f"Error generating or sending HL7 Message: {e}"
            return self.display_acknowledgment_message(error_message)

    @api.model
    def display_acknowledgment_message(self, message):
        # Create an action to display a client message
        action = {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'HL7 Message Acknowledgment',
                'sticky': True,
                'message': message,
            },
        }
        return action

    def appointment_confirm(self):
        rec = super(Appointment, self).appointment_confirm()
        print(f"{self.date}    {self.date_to}--------------------------------------------------")
        # rec.generate_outgoing_hl7_message()

        return rec

