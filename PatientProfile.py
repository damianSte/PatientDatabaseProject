
"""
Class Creates PatientProfile object
"""

class PatientProfile:
    """
        This class crates PatientProfile objects, further to be placed in database
    """

    def __init__(self, full_name, pesel, age, sex, disease, medication, doctors_id):
        """
            Constructor method
        """
        self.full_name = full_name
        self.pesel = pesel
        self.age = age
        self.sex = sex
        self.disease = disease
        self.medication = medication
        self.doctors_id = doctors_id
