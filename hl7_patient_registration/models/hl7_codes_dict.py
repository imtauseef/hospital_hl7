ADMIT_SOURCE_CODE = {'1': 'Physician referral', '2': 'Clinic referral', '3': 'HMO referral',
                     '4': 'Transfer from a hospital',
                     '5': 'Transfer from a skilled nursing facility', '6': 'Transfer from another health care facility',
                     '7': 'Emergency room',
                     '8': 'Court/law enforcement', '9': 'Information not available', 'P': 'Patient/Self/Walk-in'}

PATIENT_CLASS_CODE = {'E': 'Emergency', 'I': 'Inpatient', 'O': 'Outpatient', 'UC': 'Urgent Care', 'T': 'Telemedicine',
                      'HC': 'Home Care',
                      'P': 'Preadmit', 'R': 'Recurring patient', 'B': 'Obstetrics', 'C': 'Commercial account',
                      'N': 'Not applicable',
                      'DC': 'Day Case'}

RELIGION_CODE = {
    'MU': 'Muslim', 'CHR': 'Christianity ', 'AOG': 'Christian: Assembly of God', 'BAP': 'Christian: Baptist',
    'BUD': 'Buddhist', 'CAT': 'Christian: Roman Catholic', 'COC': 'Christian: Church of Christ',
    'COG': 'Christian: Church of God', 'GRE': 'Christian: Greek Orthodox', 'HIN': 'Hindu', 'JH': 'Jewish',
    'JWN': "Christian: Jehovah's Witness", 'LUT': 'Christian: Lutheran', 'MET': 'Christian: Methodist',
    'MOM': 'Christian: Latter-day Saints', 'NAZ': 'Christian: Church of the Nazarene', 'OTH': 'Other',
    'PEN': 'Christian: Pentecostal', 'PRE': 'Christian: Presbyterian', 'SEV': 'Christian: Seventh Day Adventist',
    'VAR': 'Unknown', 'EPI': 'Christian: Episcopalian'
}
SMOKING_STATUS_CODE = {
    '8517006': 'Ex_smoker',
    '77176002': 'Smoker',
    '43381005': 'Passive_smoker',
    '8392000': 'Non_smoker',

}

SMOKING_DEVICE_CODE = {
    '722497008': 'Cigar',
    '722496004': 'Cigarette',
    '722495000': 'Hookah_pipe',
    '722498003': 'Electronic_cigarette',
    '35001000087102': 'Smoking_Pipe',
}
# SMOKING_FREQUENCY_CODE = {
#
#     '{InhaledTobaccoUsePacks}/d': 'Cigarette',
#     'mg/d': 'Nicotine',
# }

ALCOHOL_DRINKING_STATUS_CODE = {
    '82581004': 'Ex-drinker',
    '160577002': 'Heavy drinker - 7-9u/day',
    '160575005': 'Light drinker - 1-2u/day',
    '160576006': 'Moderate drinker - 3-6u/day',
    '105542008': 'Non - drinker',
    '28127009': 'Social drinker',
    '266917007': 'Trivial drinker - <1u/day',
    '160578007': 'Very heavy drinker - greater than 9 units/day',

}

SUBSTANCE_ABUSE_STATUS_CODE = {

    '428406005': 'Benzodiazepine misuse',
    '428493006': 'Crack cocaine misuse',
    '428495004': 'Solvent misuse',
    '428623008': 'Barbiturate misuse',
    '428659002': 'Amphetamine misuse',
    '428819003': 'Opiate misuse',
    '428823006': 'Cannabis misuse',
    '429179002': 'Antidepressant misuse',
    '429512006': 'Methadone misuse',
    '429782000': 'Cocaine misuse',
    '228368007': 'Has never misused drugs',
}

EDUCATION_LEVEL_CODE = {
    "LA35-1": "No schooling",
    "LA36-9": "8th grade/less",
    "LA37-7": "9-11 grades",
    "LA38-5": "High School",
    "LA39-3": "Technical or Trade School",
    "LA40-1": "Some College",
    "LA12459-6": "Associate degree (e.g., AA, AS)",
    "LA12460-4": "Bachelors Degree",
    "LA12461-2": "Master's degree (e.g., MA, MS, MEng, MEd, MSW, MBA)",
    "LA30185-5": "Doctoral degree (e.g., PhD, EdD)",
    "LA30186-3": "Professional degree (e.g., MD, DDS, DVM, LLB, JD)",
    "LA4489-6": "Unknown",

}

EMPLOYMENT_STATUS_CODE = {

    "440584001": "Permanently unable to perform work activities due to medical condition",
    "440337002": "Temporarily unable to perform work activities due to medical condition",
    "307112004": "On secondment from work",
    "224462003": "Suspended from work",
    "224461005": "On unpaid leave",
    "224460006": "On compassionate leave",
    "224459001": "On sick leave from work",
    "224458009": "On paternity leave",
    "224457004": "On maternity leave",
    "224456008": "On leave from work",
    "224372004": "Does voluntary work",
    "224363007": "Employed",
    "160906004": "Self Employed",
    "160895006": "Stopped work",
    "105493001": "Retired",
    "73438004": "Unemployed",
}

HUNT_HESS_CODE = {
    'G1': 'Grade 1',
    'G2': 'Grade 2',
    'G3': 'Grade 3',
    'G4': 'Grade 4',
    'G5': 'Grade 5',
}

CONDITION_PRESENCE = {
    'yes': 'Yes',
    'no': 'No',
}
