'''
This program generates random marks for the students whose ID's and names were already created in generate_master_data program and stored in MySQL. It Stores them in SQL Database.
'''

import numpy as np
import random
import mysql.connector as msql
import getpass

def get_student_marks():
    password = getpass.getpass('Enter Password for MySQL: ')
    conect = msql.connect(host = 'localhost', user = 'root', passwd = password, database = 'JEE_Mains')
    cursor = conect.cursor()
    cursor.execute("SELECT Reg_ID FROM Student_Master;")
    lis = cursor.fetchall()
    
    for i in range(8):
        cursor.execute('DROP TABLE IF EXISTS Session%s' %(str(i + 1)))
        cursor.execute('CREATE TABLE Session%s (Reg_ID CHAR(11) NOT NULL PRIMARY KEY, Math_Marks Integer, Phy_Marks Integer, Chem_Marks Integer, Total Integer, Math_Percentile FLOAT(10, 7), Phy_Percentile FLOAT(10, 7), Chem_Percentile FLOAT(10, 7), Total_Percentile FLOAT(10, 7));' %(str(i + 1)))
    conect.commit()

    bands = []
    probs = []
    band1 = (-20, -10, 0.1)
    band2 = (-10, 0, 0.1)
    band3 = (0, 10, 0.2)
    band4 = (10, 20, 0.2)
    band5 = (20, 30, 0.1)
    band6 = (30, 40, 0.1)
    band7 = (40, 50, 0.1)
    band8 = (50, 60, 0.05)
    band9 = (60, 70, 0.02)
    band10 = (70, 77, 0.01)
    band11 = (77, 83, 0.01)
    band12 = (83, 88, 0.0055)
    band13 = (88, 92, 0.0025)
    band14 = (92, 95, 0.0013)
    band15 = (95, 97, 0.0005)
    band16 = (97, 99, 0.00018)
    band17 = (99, 100, 0.00002)
    
    for i in range(1, 18):
        a = 'band' + str(i)
        bands.append(a)
        a = eval(a)
        probs.append(a[2])

    for i in range (len(lis)):
        marks_band = eval(np.random.choice(bands, p = probs))
        math_marks = random.randint(marks_band[0], marks_band[1])
        phy_marks = random.randint(marks_band[0], marks_band[1])
        chem_marks = random.randint(marks_band[0], marks_band[1])
        attempts = np.random.choice([1,2,3], p = [0.25, 0.25, 0.5])

        if attempts == 1:
            num = random.choice([1,2,3,4])
            cursor.execute("INSERT INTO Session%s (Reg_ID, Math_Marks, Phy_Marks, Chem_Marks) VALUES ('%s', '%s', '%s', '%s')" %(str(num), str(lis[i][0]), str(math_marks), str(phy_marks), str(chem_marks)))
            conect.commit()
            cursor.execute('UPDATE Student_Master SET Attempt1 = %s WHERE Reg_ID = "%s";' %(str(num), str(lis[i][0])))
            conect.commit()

        elif attempts == 2:
            num = random.choice([5,6,7,8])
            cursor.execute("INSERT INTO Session%s (Reg_ID, Math_Marks, Phy_Marks, Chem_Marks) VALUES ('%s', '%s', '%s', '%s')" %(str(num), str(lis[i][0]), str(math_marks), str(phy_marks), str(chem_marks)))
            conect.commit()
            cursor.execute('UPDATE Student_Master SET Attempt2= %s WHERE Reg_ID = "%s";' %(str(num), str(lis[i][0])))
            conect.commit()

        elif attempts == 3:
            num = random.choice([1,2,3,4])
            cursor.execute("INSERT INTO Session%s (Reg_ID, Math_Marks, Phy_Marks, Chem_Marks) VALUES ('%s', '%s', '%s', '%s')" %(str(num), str(lis[i][0]), str(math_marks), str(phy_marks), str(chem_marks)))
            conect.commit()
            cursor.execute('UPDATE Student_Master SET Attempt1 = %s WHERE Reg_ID = "%s";' %(str(num), str(lis[i][0])))
            conect.commit()

            math_marks = random.randint(marks_band[0], marks_band[1])
            phy_marks = random.randint(marks_band[0], marks_band[1])
            chem_marks = random.randint(marks_band[0], marks_band[1])

            num = random.choice([5,6,7,8])
            cursor.execute("INSERT INTO Session%s (Reg_ID, Math_Marks, Phy_Marks, Chem_Marks) VALUES ('%s', '%s', '%s', '%s')" %(str(num), str(lis[i][0]), str(math_marks), str(phy_marks), str(chem_marks)))
            conect.commit()
            cursor.execute('UPDATE Student_Master SET Attempt2 = %s WHERE Reg_ID = "%s";' %(str(num), str(lis[i][0])))
            conect.commit()

    for i in range(1,9):
        cursor.execute('UPDATE Session%s SET Total = Math_Marks + Phy_Marks + Chem_Marks;' %(str(i)))
        conect.commit()
    
    conect.close()
#__main__
get_student_marks()
