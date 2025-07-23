'''
This Program generates candidates for JEE MAINS exam
Registration Prefix will be used for all Registration ID's, for example 2022
Number of students for which scores ranks computed is to be inputed
Names, emails and mobile numbers will be auto-generated so will Registration ID's
This needs the file names.yaml to be in same folder as this program.
'''

import random
import sys
import yaml
import pandas as pd
import numpy as np
import mysql.connector as msql
import getpass

# names YAML file containing FirstName, LastName combinations
# n number of records
# prefix used in registration number
def gen_student_data(names, n, prefix):
    with open(names, "r") as inp:
        name_dict = yaml.safe_load(inp)
    name_sets = name_dict.keys()

    name_set_lengths = {}
    total = 0

    for i in range(1, len(name_sets) + 1):
        k = "Set" + str(i)
        first_names_len = len(name_dict[k]['FirstName'])
        last_names_len = len(name_dict[k]['LastName'])
        v = first_names_len * last_names_len
        name_set_lengths[k] = v
        total += v

    sets = []
    probs = []

    for k, v in name_set_lengths.items():
        sets.append(k)
        probs.append(v / total)

    email_ids = set()
    mobile_list = set()

    password = getpass.getpass('Enter Password for MySQL: ')
    conect = msql.connect(host = 'localhost', user = 'root', passwd = password)
    cursor = conect.cursor()
    cursor.execute('DROP DATABASE IF EXISTS JEE_Mains')
    cursor.execute('CREATE DATABASE JEE_Mains;')
    cursor.execute('USE JEE_Mains;')
    cursor.execute('CREATE TABLE Student_Master (Reg_ID Char(11) NOT NULL PRIMARY KEY, First_Name Varchar(20) NOT NULL, Last_Name Varchar(20) NOT NULL, EmailID Varchar(50), MobileNo Char(10), Attempt1 Integer, Attempt2 Integer);')

    for i in range(n):
        key = prefix + str(i).zfill(7)
        name_set = np.random.choice(sets, p = probs)
        first_name = random.choice(name_dict[name_set]['FirstName'])
        last_name = random.choice(name_dict[name_set]['LastName'])
        email_id = get_email_id(first_name, last_name, email_ids)
        contact_no = get_mobile_no(mobile_list)
        cursor.execute("INSERT INTO Student_Master (Reg_ID, First_Name, Last_Name, EmailID, MobileNo) VALUES ('%s', '%s', '%s', '%s', '%s');" %(key, first_name, last_name, email_id, contact_no))
        conect.commit()

    cursor.execute('SELECT * FROM Student_Master')
    a = cursor.fetchall()
    conect.close()
        
def get_email_id(first_name, last_name, email_ids):
    email_id = first_name + '.' + last_name
    ctr = 1

    while (email_id  in email_ids):
        email_id = first_name + '.' + last_name + '_' + str(ctr)
        ctr += 1
    email_ids.add(email_id)
    email_id += '@nta.com'
    return email_id

def get_mobile_no(mobile_list):
    n = 9000000000 + random.randint(1, 999999999)
    while n in mobile_list:
        n = 9000000000 + random.randint(1, 999999999)
    mobile_list.add(n)
    return n


#__main__
names = "names.yaml"
n = int(input('Enter the number of students (< 10 million) to generate percentile and rank: '))
prefix = input('Enter year or any 4 character prefix of your choice: ')
gen_student_data(names, n, prefix)

