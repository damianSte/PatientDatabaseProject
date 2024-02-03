import sqlite3
from collections import Counter

import matplotlib.pyplot as mtp

def calculate_yearly_regist_stats(data):
    """
    Function calculates yearly registration statistic based on patientDatabase
            Arguments:
                - data (file) -- patient database file
    Returns yearly registration counter
    """
    yearly_stats = Counter(patient["add_data"].split("-")[0] for patient in data)
    return yearly_stats


def plot_yearly_registration_stats(stats):
    """
    Function plots yearly registration statistic based on stats from calculate yearly registration
            Arguments:
                - stats (dict) -- dictionary of patient stats
    Returns yearly registration plot
    """
    years = list(stats.keys())
    counts = list(stats.values())
    mtp.bar(years, counts)
    mtp.xlabel("Year")
    mtp.ylabel("Number of Registrations")
    mtp.title("Yearly Patient Registrations")
    mtp.show()

def calculate_disease_frequency(data):
    """
    Function calculates frequency of appearance of patients diseases
            Arguments:
                - data (file) -- patient database file
    Returns patient disease counter
    """
    diseases = [patient["disease"] for patient in data]
    disease_counts = Counter(diseases)
    return disease_counts

def plot_disease_frequency(stats):
    """
    function plots frequency of appearance of patients disease from calculate_disease_frequency
            Arguments:
                - stats (dict)-- dictionary of patient  stats
    Returns plot with patients diseases
    """
    diseases = list(stats.keys())
    counts = list(stats.values())
    mtp.bar(diseases, counts)
    mtp.xlabel("Disease")
    mtp.ylabel("Number of Cases")
    mtp.title("Frequency of Diseases")
    mtp.xticks(rotation=45, ha="right")
    mtp.show()


def calculate_gender_distribution(data):
    """
    Function calculates gender distribution of patients based on database
            Arguments:
                - data (file) -- patent Database file
    Returns distribution of counter
    """
    genders = [patient["sex"] for patient in data]
    gender_counts = Counter(genders)
    return gender_counts

def plot_gender_distribution(stats):
    """
    Function plots gender distribution of patients based on calculate_gender_distribution
            Arguments:
                - stats (dict) -- dictionary of patient stats
    Returns plot with patients gender distribution
    """
    genders = list(stats.keys())
    counts = list(stats.values())
    mtp.pie(counts, labels=genders, autopct='%1.1f%%', startangle=140)
    mtp.axis('equal')
    mtp.title("Gender Distribution of Patients")
    mtp.show()


def fetch_all_patients(db_file):
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM patientProfiles")
    patients = cursor.fetchall()
    connection.close()
    return patients
