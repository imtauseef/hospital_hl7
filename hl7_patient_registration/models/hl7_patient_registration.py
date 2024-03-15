import socket
from datetime import datetime
from odoo.exceptions import ValidationError
from odoo import models, fields, api, _
import hl7
import pytz
from .hl7_codes_dict import ADMIT_SOURCE_CODE, PATIENT_CLASS_CODE, RELIGION_CODE, HUNT_HESS_CODE, SMOKING_STATUS_CODE, \
    SMOKING_DEVICE_CODE, ALCOHOL_DRINKING_STATUS_CODE, SUBSTANCE_ABUSE_STATUS_CODE, EDUCATION_LEVEL_CODE, \
    EMPLOYMENT_STATUS_CODE, CONDITION_PRESENCE


class FamilyHistory(models.Model):
    _name = 'family.history'
    _description = 'For Family History'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Family History', required=True)

    description = fields.Text(string='Description')

    code = fields.Char(string='Code', required=True)



class AcsFamilyMember(models.Model):
    _inherit = 'acs.family.member'
    
    family_history_id = fields.Many2one('family.history', string='Family History', required=True)

    family_member_gender = fields.Selection([
        ('M', 'Male'),
        ('F', 'Female'),
    ], string='Family member Gender', required=True)

    condition_presence = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No'),
    ], string='Condition Presence', required=True)

    relation_id = fields.Many2one('next.kin.relation', string='Relation', domain="[('family_terms', '=', True)]")


    @api.onchange('relation_id')
    def on_related_field_change(self):
        if self.relation_id:
            self.family_member_gender = self.relation_id.gender
        else:
            self.family_member_gender = False
        return


class NextKinRelation(models.Model):
    _name = 'next.kin.relation'
    _description = 'Next of Kin Relation'
    _inherit = ['mail.thread', 'mail.activity.mixin']


    name = fields.Char(string='Name of Kin', required=True)

    code = fields.Char(string='Code', required=True)

    family_terms = fields.Boolean(string="Family Terms")

    gender = fields.Selection([('M', 'Male'), ('F', 'Female')], string='Gender')

    inverse_relation_id = fields.Many2one("acs.family.member", string="Inverse Relation")




class HospitalService(models.Model):
    _name = 'hospital.service'
    _description = 'For Hospital Service'
    _inherit = ['mail.thread', 'mail.activity.mixin']


    name = fields.Char(string='Hospital Service', required=True)

    description = fields.Text(string='Description')

    code = fields.Char(string='Code', required=True)


class HmsPatient(models.Model):
    _inherit = 'hms.patient'
    _description = 'HL7 Patient Registration'

    hospital_service_id = fields.Many2one('hospital.service', string='Hospital Service', required=True)

    date_and_time_now = fields.Datetime(string='Date & Time Now', default=fields.Datetime.now)

    arrival_date_time = fields.Datetime(string='Arrival Date/Time', )

    doctor_seen_date_time = fields.Datetime(string='Doctor Seen Date/Time', )

    send_app_code = fields.Char(string='Application Code', required=True)

    send_facility_code = fields.Char(string='Facility Code', required=True)

    gender_code = fields.Char(string='Code', compute='_compute_code', store=True)

    business_contact_no = fields.Char(string='Business Contact No', required=True)

    marital_status_code = fields.Char(string='Code', compute='_compute_marital_code', store=True)

    nationality_code = fields.Char(string='Code', related='nationality_id.code', store=True)

    doctor_id_code = fields.Char(string='Code', related='primary_physician_id.code', store=True)

    hunt_and_hess_scale =fields.Selection([
        ('G1', 'Grade 1'),
        ('G2', 'Grade 2'),
        ('G3', 'Grade 3'),
        ('G4', 'Grade 4'),
        ('G5', 'Grade 5'),
    ], string='Hunt and Hess scale', required=True)

    rankin_scale = fields.Selection([
        ('0', '0'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
    ], string='Rankin Scale', default='0', required=True)

    nih_stroke_scale = fields.Integer(string='NIH Stroke scale', required=True)

    # death_date = fields.Date(string='Patient Death Date', required=False)
    death_time = fields.Float(string='Patient Death Time (in hours)', required=False)


    death_indicator = fields.Selection([
        ('Y', 'Deceased'),
        ('N', 'Not Deceased'),
    ], string='Patient Death Indicator', default='N')

    smoking_status = fields.Selection([
        ('8517006', 'Ex-smoker'),
        ('77176002', 'Smoker'),
        ('43381005', 'Passive smoker'),
        ('8392000', 'Non-smoker'),
    ], string='Smoking Status')

    #   smoking_status_code dict created in hl7_code file  #
    smoking_device = fields.Selection([
        ('722497008', 'Cigar'),
        ('722496004', 'Cigarette'),
        ('722495000', 'Hookah Pipe'),
        ('722498003', 'Electronic Cigarette'),
        ('35001000087102', 'Smoking Pipe'),
    ], string='Smoking Device')

    # SMOKING_DEVICE_CODE dict created in hl7_code file
    p_smoking_frequency = fields.Char(string='Smoking Frequency', compute='_compute_p_smoking_frequency')

    start_smoking_age = fields.Integer('Start Smoking Age')

    stop_smoking_age = fields.Integer('Stop Smoking Age')

    alcohol_drinking_status = fields.Selection([
        ('82581004', 'Ex-drinker'),
        ('160577002', 'Heavy drinker - 7-9u/day'),
        ('160575005', 'Light drinker - 1-2u/day'),
        ('160576006', 'Moderate drinker - 3-6u/day'),
        ('105542008', 'Non - drinker'),
        ('28127009', 'Social drinker'),
        ('266917007', 'Trivial drinker - <1u/day'),
        ('160578007', 'Very heavy drinker - greater than 9 units/day'),
    ], string='Alcohol Drinking Status')

     # ALCOHOL_DRINKING_STATUS_CODE CREATED IN hl7_code file
    substance_abuse_status = fields.Selection([
        ('428406005', 'Benzodiazepine misuse'),
        ('428493006', 'Crack cocaine misuse'),
        ('428495004', 'Solvent misuse'),
        ('428623008', 'Barbiturate misuse'),
        ('428659002', 'Amphetamine misuse'),
        ('428819003', 'Opiate misuse'),
        ('428823006', 'Cannabis misuse'),
        ('429179002', 'Antidepressant misuse'),
        ('429512006', 'Methadone misuse'),
        ('429782000', 'Cocaine misuse'),
        ('228368007','Has never misused drugs'),
    ], string='Substance Abuse Status')

    # SUBSTANCE_ABUSE_STATUS_CODE DICT CREATED IN HL7CODE FILE
    education_level = fields.Selection([
        ("LA35-1", "No schooling"),
        ("LA36-9", "8th grade/less"),
        ("LA37-7", "9-11 grades"),
        ("LA38-5", "High school"),
        ("LA39-3", "Technical or Trade School"),
        ("LA40-1", "Some College"),
        ("LA12459-6", "Associate degree (e.g., AA, AS)"),
        ("LA12460-4", "Bachelor's degree (e.g., BA, AB, BS)"),
        ("LA12461-2", "Master's degree (e.g., MA, MS, MEng, MEd, MSW, MBA)"),
        ("LA30185-5", "Doctoral degree (e.g., PhD, EdD)"),
        ("LA30186-3","Professional degree (e.g., MD, DDS, DVM, LLB, JD)"),
        ("LA4489-6","Unknown")
    ], string='Education Level')

    # EDUCATION_LEVEL_CODE dict created in hl7_cdoe fiel
    patient_employment_status = fields.Selection([
        ("440584001", "Permanently unable to perform work activities due to Medical condition"),
        ("440337002", "Temporarily unable to perform work activities due to Medical condition"),
        ("307112004", "On Secondment from work"),
        ("224462003", "Suspended from work"),
        ("224461005", "On Unpaid leave"),
        ("224460006", "On Compassionate leave"),
        ("224459001", "On Sick leave from work"),
        ("224458009", "On Paternity leave"),
        ("224457004", "On Maternity leave"),
        ("224456008", "On Leave from work"),
        ("224372004", "Does Voluntary work"),
        ("224363007", "Employed"),
        ("160906004", "Self-employed"),
        ("160895006", "Stopped work"),
        ("105493001", "Retired"),
        ("73438004", "Unemployed")
    ], string='Employment Status')
   
    message_control_id = fields.Char(string='Message Control ID') 

    ADMIT_SOURCE_SELECTION = [('1', 'Physician referral'), ('2', 'Clinic referral'), ('3', 'HMO referral'), ('4', 'Transfer from a hospital'),
                                ('5', 'Transfer from a skilled nursing facility'), ('6', 'Transfer from another health care facility'),
                                ('7', 'Emergency room'), ('8', 'Court/law enforcement'), ('9', 'Information not available'),
                                ('P', 'Patient/Self/Walk-in')]


    admit_source = fields.Selection(ADMIT_SOURCE_SELECTION, string='Admit Source', required=True)

    PATIENT_CLASS_SELECTION = [('E', 'Emergency'), ('I', 'Inpatient'), ('O', 'Outpatient'), ('UC', 'Urgent Care'), ('T', 'Telemedicine'),
                                ('HC', 'Home Care'), ('P', 'Preadmit'), ('R', 'Recurring patient'), ('B', 'Obstetrics'), ('C', 'Commercial account'),
                                ('N', 'Not applicable'), ('DC', 'Day Case')]

    patient_class = fields.Selection(PATIENT_CLASS_SELECTION, string='Patient Class', required=True)
    
    second_mobile_no = fields.Char(string='Second Mobile No')

    employment_status = fields.Selection([
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('self_employed', 'Self Employed'),
        ('not_employed', 'Not Employed'),
        ('business_owner', 'Business Owner'),
    ], string='Employment Status', default='')

    patient_employer = fields.Char(string="Patient Employer")

    birth_place = fields.Char(string="Place of Birth")

    visa_or_file_no = fields.Char(string="Visa/File Number")

    father_guardian_name = fields.Char(string="Father/Guardian Name")

    # /////////////////////////////////////
    nk_state = fields.Boolean(string="Next of Kin ?")

    family_bool = fields.Boolean(string="Family Member ?")

    social_history_bool_state = fields.Boolean(string="Social History ?")

    nk_name = fields.Char(string='Next of Kin Name')

    nk_relation = fields.Many2one('next.kin.relation', string='Relation')

    nk_phone = fields.Char(string='Next of Kin Phone Number')

    RELIGION = [('MU', 'Muslim'), ('CHR', 'Christianity '), ('AOG', 'Christian: Assembly of God'),
            ('BAP', 'Christian: Baptist'), ('BUD', 'Buddhist'), ('CAT', 'Christian: Roman Catholic'),
            ('COC', 'Christian: Church of Christ'), ('COG', 'Christian: Church of God'),
            ('GRE', 'Christian: Greek Orthodox'), ('HIN', 'Hindu'), ('JH', 'Jewish'),
            ('JWN', "Christian: Jehovah's Witness"), ('LUT', 'Christian: Lutheran'), ('MET', 'Christian: Methodist'),
            ('MOM', 'Christian: Latter-day Saints'), ('NAZ', 'Christian: Church of the Nazarene'), ('OTH', 'Other'),
            ('PEN', 'Christian: Pentecostal'), ('PRE', 'Christian: Presbyterian'),
            ('SEV', 'Christian: Seventh Day Adventist'), ('VAR', 'Unknown'), ('EPI', 'Christian: Episcopalian')]
    
    religion_hl7 = fields.Selection(RELIGION, string='Religion', required=True)

    emirates_id = fields.Char(string="Emirates_id", required=True)

    consulting_doctor = fields.Char(string='Consulting Doctor', compute='_compute_consulting_doctor', store=True)

    @api.depends('smoking_device')
    def _compute_p_smoking_frequency(self):
        for record in self:
            if record.smoking_device == '722496004':
                record.p_smoking_frequency = 'InhaledTobaccoUsePacks'
            else:
                record.p_smoking_frequency = 'mg'


    @api.depends('primary_physician_id')
    def _compute_consulting_doctor(self):
        for record in self:
            if record.primary_physician_id:
                record.consulting_doctor = record.primary_physician_id.name
            else:
                record.consulting_doctor = False

    @api.constrains('date_of_death', 'death_time', 'death_indicator')
    def _check_death_datetime(self):
        for patient in self:
            if patient.death_indicator == 'Y':
                if not patient.date_of_death or not patient.death_time:
                    raise ValidationError("Patient Death Date and Time are required when the patient is deceased.")
                
                # death_datetime = fields.Datetime.from_string(patient.date_of_death + ' ' + str(int(patient.death_time)) + ':00:00')
                # if death_datetime.date() != patient.date_of_death or death_datetime.time().hour != int(patient.death_time):
                #     raise ValidationError("Invalid Patient Death Date and Time.")
                
    @api.depends('gender')
    def _compute_code(self):
        for patient in self:
            if patient.gender == 'male':
                patient.gender_code = 'M'
            elif patient.gender == 'female':
                patient.gender_code = 'F'
            else:
                patient.gender_code = 'O'

    @api.depends('marital_status')
    def _compute_marital_code(self):
        for patient in self:
            if patient.marital_status == 'single':
                patient.marital_status_code = 'S'
            else:
                patient.marital_status_code = 'M'





    @api.model
    def generate_hl7_message(self, integration_record):
        local_tz = pytz.timezone('Asia/Dubai')
        local_time = datetime.now(local_tz)

        hl7_message = (
            f"MSH|^~\&|SYSTEMCODE^SYSTEMCODE|SYSTEMCODE^SYSTEMCODE|Rhapsody^MALAFFI|ADHIE|{local_time.strftime('%Y%m%d%H%M%S')}+0400||ADT^A04|{integration_record.message_control_id}|P|2.5.1\n"
           
            f"EVN|A04|{local_time.strftime('%Y%m%d%H%M%S')}\n"
            
            # f"PID|1||{integration_record.code}^^^&SYSTEx MCODE||{integration_record.name}^^^^^^P||{integration_record.birthday:%Y%m%d}|{integration_record.gender_code}|||||{integration_record.mobile}^^CH|{integration_record.business_contact_no}^^CC||{integration_record.marital_status_code}^{integration_record.marital_status}^MALAFFI|{integration_record.religion_hl7}^{RELIGION_CODE[integration_record.religion_hl7]}^MALAFFI||{integration_record.emirates_id}|||||||||{integration_record.nationality_code}^{integration_record.nationality_id.name}^MALAFFI||{integration_record.death_indicator}\n"

        )

        if integration_record.death_indicator == 'Y':
            hl7_message += (
                f"PID|1||{integration_record.code}^^^&SYSTEx MCODE||{integration_record.name}^^^^^^P||{integration_record.birthday:%Y%m%d}|{integration_record.gender_code}|||||{integration_record.mobile}^^CH|{integration_record.business_contact_no}^^CC||{integration_record.marital_status_code}^{integration_record.marital_status}^MALAFFI|{integration_record.religion_hl7}^{RELIGION_CODE[integration_record.religion_hl7]}^MALAFFI||{integration_record.emirates_id}|||||||||{integration_record.nationality_code}^{integration_record.nationality_id.name}^MALAFFI|{integration_record.date_of_death:%Y%m%d}|{integration_record.death_indicator}\n"
            )
        else:
            hl7_message += (
                f"PID|1||{integration_record.code}^^^&SYSTEx MCODE||{integration_record.name}^^^^^^P||{integration_record.birthday:%Y%m%d}|{integration_record.gender_code}|||||{integration_record.mobile}^^CH|{integration_record.business_contact_no}^^CC||{integration_record.marital_status_code}^{integration_record.marital_status}^MALAFFI|{integration_record.religion_hl7}^{RELIGION_CODE[integration_record.religion_hl7]}^MALAFFI||{integration_record.emirates_id}|||||||||{integration_record.nationality_code}^{integration_record.nationality_id.name}^MALAFFI||{integration_record.death_indicator}\n"
            )

        if integration_record.nk_state:
            hl7_message += f"NK1|1|{integration_record.nk_name}|{integration_record.nk_relation.code}^{integration_record.nk_relation.name}^MALAFFI||{integration_record.nk_phone}^^CC|^^^|\n"

        hl7_message += (
            f"PV1|1|{integration_record.patient_class}|^^^MF3333&SYSTEMCODE-DOHID||||||{integration_record.doctor_id_code}^{integration_record.title.name}^{integration_record.primary_physician_id.name}^^^^^^&SYSTEMCODE-DOHID|{integration_record.hospital_service_id.code}||||{ADMIT_SOURCE_CODE[integration_record.admit_source]}|||||{integration_record.code}^^^&SYSTEMCODE|||||||||||||||||||||||||{local_time.strftime('%Y%m%d%H%M%S')}\n"
            
            f"ZPV1||||||||{integration_record.arrival_date_time}|{integration_record.doctor_seen_date_time}|{integration_record.hunt_and_hess_scale}^{HUNT_HESS_CODE[integration_record.hunt_and_hess_scale]}^MALAFFI|{integration_record.rankin_scale}|{integration_record.nih_stroke_scale}\n"
            
            f"PR1|1|CPT|49080^PUNCTURE PERITONEAL CAVITY^CPT|PERITONEOCENTESIS, ABDOMINAL PARACENTESIS, OR PERITONEAL LAVAGE (DIAGNOSTIC ORTHERAPEUTIC); INITIAL|20180725120000|||GD18123^testdoc1^testere1^mname1^^Dr^^^&SYSTEMCODE-DOHID|||GD18668^testdoc2^testere2^^^Dr^^^&SYSTEMCODE-DOHID|GD18668^testdoc3^testere3^^^^^^&SYSTEMCODE-DOHID||1|E11.65^Type 2 diabetesmellitus with hyperglycemia^ICD10\n"
            
            f"PR1|2|CPT|93320^ECHO DPPLER CMPL^CPT|HC ECHO DPPLER CMPL|20180501120000||||||GD21223^asdasd^asdasd^^^^^^&SYSTEMCODE-DOHID|GD21223^asdasd^asdasd^^^^^^&SYSTEMCODE-DOHID||2|D64.9^Anemia^ICD10\n"
            
            f"IN1|1|{integration_record.insurance_plan_id.id}|{integration_record.insurance_company_id.id}|{integration_record.insurance_company_id.name}|||||||||||||||||||||||||||||||||||||||||||||abc1234\n"
            
            # f"ZFH|161062006^Child abuse in family^MALAFFI|SIS^Sister^MALAFFI|F|Yes\n"
            #
            # f"ZSH|{integration_record.smoking_status}^{SMOKING_STATUS_CODE[integration_record.smoking_status]}^MALAFFI|{integration_record.smoking_device}^{SMOKING_DEVICE_CODE[integration_record.smoking_device]}|MALAFFI|{{{integration_record.p_smoking_frequency}}}/d^{integration_record.p_smoking_frequency} / day^MALAFFI|{integration_record.start_smoking_age}|{integration_record.stop_smoking_age}|{integration_record.alcohol_drinking_status}^{ALCOHOL_DRINKING_STATUS_CODE[integration_record.alcohol_drinking_status]}^MALAFFI|{integration_record.substance_abuse_status}^{SUBSTANCE_ABUSE_STATUS_CODE[integration_record.substance_abuse_status]}^MALAFFI|{integration_record.education_level}^{EDUCATION_LEVEL_CODE[integration_record.education_level]}^MALAFFI|{integration_record.patient_employment_status}^{EMPLOYMENT_STATUS_CODE[integration_record.patient_employment_status]}^MALAFFI\n"
        )

        # if integration_record.family_member_ids:
        #     for family_member in integration_record.family_member_ids:
        #         relation_id = family_member.relation_id
        #         hl7_message += f"ZFH|161062006^Child abuse in family^MALAFFI|{relation_id.name}^MALAFFI|F|Yes\n"
        #
        # hl7_message += f"ZSH|{integration_record.smoking_status}^{SMOKING_STATUS_CODE[integration_record.smoking_status]}^MALAFFI|{integration_record.smoking_device}^{SMOKING_DEVICE_CODE[integration_record.smoking_device]}|MALAFFI|{{{integration_record.p_smoking_frequency}}}/d^{integration_record.p_smoking_frequency} / day^MALAFFI|{integration_record.start_smoking_age}|{integration_record.stop_smoking_age}|{integration_record.alcohol_drinking_status}^{ALCOHOL_DRINKING_STATUS_CODE[integration_record.alcohol_drinking_status]}^MALAFFI|{integration_record.substance_abuse_status}^{SUBSTANCE_ABUSE_STATUS_CODE[integration_record.substance_abuse_status]}^MALAFFI|{integration_record.education_level}^{EDUCATION_LEVEL_CODE[integration_record.education_level]}^MALAFFI|{integration_record.patient_employment_status}^{EMPLOYMENT_STATUS_CODE[integration_record.patient_employment_status]}^MALAFFI\n"

        if integration_record.family_member_ids and integration_record.family_bool:
            for family_member in integration_record.family_member_ids:
                relation_id = family_member.relation_id
                family_history_id = family_member.family_history_id
                family_member_gender = family_member.family_member_gender
                condition_presence = family_member.condition_presence
                if family_member.relation_id.name in ['Brother', 'Father', 'Mother']:
                    hl7_message += f"ZFH|{family_history_id.code}^{family_history_id.name}^MALAFFI|{relation_id.name}^MALAFFI||{CONDITION_PRESENCE[condition_presence]}\n"
                else:
                    hl7_message += f"ZFH|{family_history_id.code}^{family_history_id.name}^MALAFFI|{relation_id.name}^MALAFFI|{family_member_gender}|{CONDITION_PRESENCE[condition_presence]}\n"

        if integration_record.social_history_bool_state:
            hl7_message += f"ZSH|{integration_record.smoking_status}^{SMOKING_STATUS_CODE[integration_record.smoking_status]}^MALAFFI|{integration_record.smoking_device}^{SMOKING_DEVICE_CODE[integration_record.smoking_device]}|MALAFFI|{{{integration_record.p_smoking_frequency}}}/d^{integration_record.p_smoking_frequency} / day^MALAFFI|{integration_record.start_smoking_age}|{integration_record.stop_smoking_age}|{integration_record.alcohol_drinking_status}^{ALCOHOL_DRINKING_STATUS_CODE[integration_record.alcohol_drinking_status]}^MALAFFI|{integration_record.substance_abuse_status}^{SUBSTANCE_ABUSE_STATUS_CODE[integration_record.substance_abuse_status]}^MALAFFI|{integration_record.education_level}^{EDUCATION_LEVEL_CODE[integration_record.education_level]}^MALAFFI|{integration_record.patient_employment_status}^{EMPLOYMENT_STATUS_CODE[integration_record.patient_employment_status]}^MALAFFI\n"
        print(hl7_message)
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
            acknowledgment_message = (f"HL7 Message for Patient Registration has been created Successfully and sent to the designated Server.")

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
