APPOINTMENT_REASON_CODE = {
    'CHECKUP': 'A routine check-up, such as an annual physical',
    'EMERGENCY': 'EMERGENCY room',
    'FOLLOWUP': 'A follow up visit from a previous appointment',
    'ROUTINE': 'Routine appointment - default if not valued',
    'WALKIN': 'A previously unscheduled walk-in visit',

}

APPOINTMENT_MODE_CODE = {
    '1': 'In-Person Appointment',
    '2': 'Virtual Appointment',
}
FILLER_STATUS_CODE = {
    'Blocked': 'The indicated time slot(s) is(are) blocked',
    'Booked': 'The indicated appointment is booked',
    'Cancelled': 'The indicated appointment was stopped from occurring (canceled prior to starting)',
    'Completed': 'The indicated appointment has completed normally (was not discontinued, canceled, or deleted)',
    'Dc': "The indicated appointment was discontinued (DC'ed while in progress, discontinued parent appointment, or discontinued child appointment)",
    'Deleted': 'The indicated appointment was deleted from the filler application',
    'Noshow': 'The patient did not show up for the appointment',
    'Overbook': 'The appointment has been confirmed; however it is confirmed in an overbooked state)',
    'Pending': 'Appointment has not yet been confirmed',
    'Started': 'The indicated appointment has begun and is currently in progress',
    'Waitlist': 'Appointment has been placed on a waiting list for a particular slot, or set of slots',
}
AIL_LOCATION_TYPE_CODE = {
    'C': 'Clinic',
    'D': 'Department',
    'H': 'Home',
    'N': 'Nursing Unit',
    'O': 'Provider’s Office',
    'P': 'Phone',
    'S': 'SNF',
}
AIP_RESOURCE_STAFF_TYPE_CODE = {
    'PHYSN': 'Physician',
    'NURSE': 'Nurse',
    'RADLOGST': 'Radiologist',
    'PHYSIOTHPST': 'Physiotherapist',
    'SOCWRKR': 'Social worker',
    'OCCRTHPST': 'Occupational therapist',
    'OTHERALLDHLTH': 'Other Allied health',
}
