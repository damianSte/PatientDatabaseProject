import sqlite3
import unittest
from aifc import Error
from datetime import datetime

from PatientProfile import PatientProfile


class PatientDatabase:

    def __init__(self, db_file):
        self.db_file = db_file

    def create_connection(self):
        """
        Creates database connection to SQLite database
        Returns connection to SQLite database
        """
        connection = None

        try:
            connection = sqlite3.connect(self.db_file)
            return connection
        except Error as error:
            error = "Not able to connect"
            print(error)

    def create_table(self):
        """
        Creates table for PatientProfile objects using sqlite database
        Returns table for PatientProfile objects
        """

        connection = self.create_connection()

        if connection is not None:
            try:
                cursor = connection.cursor()
                cursor.execute('''CREATE TABLE IF NOT EXISTS patientProfiles (
                 full_name text not null,
                 pesel text not null PRIMARY KEY,
                 age integer,
                 sex text,
                 disease text,
                 medication text,
                 doctors_id varchar(20) not null,
                 add_data text)''')
                connection.commit()
                print("Table created")
            except Error as error:
                error = "Table was not created"
                print(error)
            finally:
                connection.close()

    def insert_data_database(self, patient):

        """
        Inserts data to table for PatientProfile objects
            Arguments:
                 - patient {string} - object of PatientProfile class
        Returns table with inserted object's values
        """
        connection = sqlite3.connect(self.db_file)

        if connection is not None:
            try:
                cursor = connection.cursor()
                add_data = datetime.now().strftime("%Y-%m-%d")
                cursor.execute('''INSERT INTO patientProfiles (full_name, pesel, age, sex, disease, medication, doctors_id, add_data)
                                VALUES (?,?,?,?,?,?,?,?)''',
                               (patient.full_name, patient.pesel, patient.age, patient.sex, patient.disease,
                                patient.medication, patient.doctors_id, add_data))
                connection.commit()
                print("Patient successfully added")

            except Error as error:
                error = "Not able to add patient"
                print(error)
            finally:
                pass

    def get_patient_by_pesel(self, pesel):
        """
        Retrieves patient data by PESEL from the database
        Param:
             - pesel (string) - PESEL value to search for
        Returns:
            - patient_data  - Patient data if existed, None otherwise
        """
        connection = self.create_connection()

        if connection is not None:
            try:
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM patientProfiles WHERE pesel=?", (pesel,))
                patient_data = cursor.fetchone()

                if patient_data:
                    columns = [desc[0] for desc in cursor.description]
                    return dict(zip(columns, patient_data))
                else:
                    return None
            except Error as error:
                print("Failed to fetch data by PESEL:", error)
            finally:
                connection.close()

    def get_all_data(self):

        """
        Retrieves all data from the table for PatientProfile objects

        Returns all data from the table for PatientProfile
        """
        connection = sqlite3.connect(self.db_file)

        if connection is not None:
            try:
                cursor = connection.cursor()
                cursor.execute("Select * from patientProfiles")
                rec = cursor.fetchall()

                columns = [desc[0] for desc in cursor.description]
                all_data = [dict(zip(columns, rec)) for rec in rec]
                return all_data
            except Error as error:
                print("Fetal to fetch data")
            finally:
                connection.close()


# class TestPatientDatabase(unittest.TestCase):
#
#     def setUp(self):
#         self.db = PatientDatabase("test_patient_database")
#         self.db.create_table()
#         self.patient = PatientProfile("Jan Kowalski", "12345678900", "25", "Male", "Sick", "Drug", "D1234")
#
#     def test_insert_patient_data(self):
#         # pesel is unique that is why we cannot run test twice when insert_data... is not commented out
#         #self.db.insert_data_database(self.patient)
#         result = self.db.get_all_data()
#         self.assertEqual(len(result), 1)
#         self.assertEqual(result[0]['full_name'], "Jan Kowalski")
#         self.assertEqual(result[0]['pesel'], "12345678900")
#
#     def test_get_patient_by_pesel(self):
#         result_pesel = self.db.get_patient_by_pesel('12345678900')
#         self.assertEqual(result_pesel['full_name'], 'Jan Kowalski')
#
#     def test_get_all_data(self):
#
#         result = self.db.get_all_data()
#         self.assertEqual(len(result),1)
#         self.assertEqual(result[0]['full_name'], "Jan Kowalski")
#
#
# if __name__ == '__main__':
#     unittest.main()

