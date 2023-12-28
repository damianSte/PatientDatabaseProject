from datetime import datetime
import sqlite3
import tkinter as tk
from aifc import Error
from tkinter import messagebox, ttk, font


class CreatePatientApp:
    def __init__(self, master, db):
        """
        Function Create Patient App view window (displays after running)
                Arguments:
                    - master -- Tkinter window instance
                    - db -- sqlite3 (database) instance

        Returns view window with filedes to assign values to table (db)
        """
        self.master = master
        self.master.title("Patients")
        self.master.geometry("600x550")
        self.master.configure(bg="Skyblue")
        self.master.resizable(False, False)
        self.db = db

        # Title
        title_font = font.Font(family="Helvetica", size=16, weight="bold")
        title_label = tk.Label(master, text="Patient Database", font=title_font, background="Skyblue", foreground="White")
        title_label.grid(row=0, column=0, columnspan=3, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)

        labels = ["Doctors ID:", "Full name:", "Pesel:", "Age:", "Sex:", "Disease:", "Medication:"]

        # Loops to adjust labels in window/root
        # Columns
        for i in range(3):
            self.master.columnconfigure(i, weight=1)
        # Rows
        for i in range(len(labels)+1):
            self.master.rowconfigure(i, weight=1)
        # Putting labels into rows
        for i, label_text in enumerate(labels):
            tk.Label(master, text=label_text, background="Skyblue").grid(row=i+1, column=0, padx=10, pady=2, sticky=tk.E)

        # Entry boxes
        entry_width = 40
        self.entry_doctors_id = tk.Entry(master, width=entry_width)
        self.entry_full_name = tk.Entry(master, width=entry_width)
        self.entry_pesel = tk.Entry(master, width=entry_width)
        self.entry_age = tk.Entry(master, width=entry_width)
        self.entry_disease = tk.Entry(master, width=entry_width)
        self.entry_medication = tk.Entry(master, width=entry_width)

        # Combobox - sex optional
        self.sex_options = ["Male", "Female", "Other"]
        self.sex_st = tk.StringVar()
        self.sex_combobox = ttk.Combobox(master, textvariable=self.sex_st, values=self.sex_options, state="readonly",
                                         width=38)

        # Place Entry boxes
        # self.entry_full_name.grid(row=0, column=1, padx=10, pady=5)
        # self.entry_pesel.grid(row=1, column=1, padx=10, pady=5)
        # self.entry_age.grid(row=2, column=1, padx=10, pady=5)
        # self.entry_sex.grid(row=3, column=1, padx=10, pady=5)
        # self.entry_disease.grid(row=4, column=1, padx=10, pady=5)
        # self.entry_prescription.grid(row=5, column=1, padx=10, pady=5)

        # Placing Entry boxes and combobox(sex) in rows
        for i, entry_widget in enumerate(
                [self.entry_doctors_id, self.entry_full_name, self.entry_pesel, self.entry_age, self.sex_combobox,
                 self.entry_disease, self.entry_medication]):
            entry_widget.grid(row=i+1, column=1, padx=10, pady=2)

        # Creating button to insert values to database
        tk.Button(master, text="Insert Data", command=self.insert_data).grid(row=(len(labels) + 1), column=1, padx=5,
                                                                             pady=10)

    def insert_data(self):
        """
        Inserts the data into the database, function inherits function insert_data_database from class PatientDatabase
                and values specified in Entry
        """
        # Assigning values using .get() from window's entries
        full_name = self.entry_full_name.get()
        pesel = self.entry_pesel.get()
        age = self.entry_age.get()
        sex = self.sex_st.get()
        disease = self.entry_disease.get()
        medication = self.entry_medication.get()
        doctors_id = self.entry_doctors_id.get()

        # Checking if all necessary fields are filed
        if not all((full_name, pesel, age, sex)):
            messagebox.showinfo("Error", "Full Name, PESEL, Age and Sex must be field")
            return

        # Checking PESEL as it is primary key (most important value)
        if len(pesel) != 11:
            messagebox.showerror("Error", "Invalid Pesel")

        # If everything checks inserting values using insert_data_database function class PatientDatabase
        else:
            patient = PatientProfile(full_name, pesel, age, sex, disease, medication, doctors_id)
            self.db.insert_data_database(patient)


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

