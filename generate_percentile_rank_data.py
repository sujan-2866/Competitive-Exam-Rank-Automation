"""
Program acts on data already generated and updatees tables to set percentile and rank in a final created table.
Run after generate_test_data, no input except SQL Password
"""

import mysql.connector as msql
import math
import numpy as np
import random
import getpass
import csv

def compute_percentile_rank():
    password = getpass.getpass('Enter Password for MySQL: ')
    conect = msql.connect(user = 'root', host = 'localhost', passwd = password, database = 'JEE_Mains')
    cursor = conect.cursor()

    for i in range (1, 9):
        cursor.execute("DROP VIEW IF EXISTS Session%sP;" %(str(i)))
        cursor.execute('CREATE VIEW Session%sP AS (WITH t AS (SELECT COUNT(Reg_ID), Total, Math_Marks, Phy_Marks, Chem_Marks FROM Session%s GROUP BY Total, Math_Marks, Phy_Marks, Chem_Marks) SELECT Total, Math_Marks, Phy_Marks, Chem_Marks, ROUND( 100 * (1 - PERCENT_RANK() OVER (ORDER BY Total DESC)), 7)Total_Percentile,  ROUND( 100 * (1 - PERCENT_RANK() OVER (ORDER BY  Math_Marks DESC)),  7)Math_Percentile, ROUND( 100 * (1 - PERCENT_RANK() OVER (ORDER BY  Phy_Marks DESC)), 7)Phy_Percentile, ROUND(100 * (1 - PERCENT_RANK() OVER (ORDER BY Chem_Marks DESC)), 7) Chem_Percentile  FROM t)' %(str(i), str(i)));
        conect.commit()

        cursor.execute('CREATE VIEW Session%sJ AS (SELECT DISTINCT Session%s.Reg_ID, Session%s.Total, Session%sP.Total_Percentile FROM Session%s INNER JOIN Session%sP ON (Session%s.Total = Session%sP.Total) ORDER BY Session%sP.Total_Percentile ASC);' %(str(i), str(i), str(i), str(i), str(i), str(i), str(i), str(i), str(i)));
        conect.commit()
        cursor.execute('UPDATE Session%s T1 INNER JOIN Session%sJ T2 ON T1.Reg_ID = T2.Reg_ID SET T1.Total_Percentile = T2.Total_Percentile;' %(str(i), str(i)))
        conect.commit()
        cursor.execute('DROP VIEW Session%sJ;' %(str(i)))
        conect.commit()

        cursor.execute('CREATE VIEW Session%sJ AS (SELECT DISTINCT Session%s.Reg_ID, Session%s.Math_Marks, Session%sP.Math_Percentile FROM Session%s INNER JOIN Session%sP ON (Session%s.Math_Marks = Session%sP.Math_Marks) ORDER BY Session%sP.Math_Percentile ASC);' %(str(i), str(i), str(i), str(i), str(i), str(i), str(i), str(i), str(i)));
        conect.commit()
        cursor.execute('UPDATE Session%s T1 INNER JOIN Session%sJ T2 ON T1.Reg_ID = T2.Reg_ID SET T1.Math_Percentile = T2.Math_Percentile;' %(str(i), str(i)))
        conect.commit()
        cursor.execute('DROP VIEW Session%sJ;' %(str(i)))
        conect.commit()

        cursor.execute('CREATE VIEW Session%sJ AS (SELECT DISTINCT Session%s.Reg_ID, Session%s.Phy_Marks, Session%sP.Phy_Percentile FROM Session%s INNER JOIN Session%sP ON (Session%s.Phy_Marks = Session%sP.Phy_Marks) ORDER BY Session%sP.Phy_Percentile ASC);' %(str(i), str(i), str(i), str(i), str(i), str(i), str(i), str(i), str(i)));
        conect.commit()
        cursor.execute('UPDATE Session%s T1 INNER JOIN Session%sJ T2 ON T1.Reg_ID = T2.Reg_ID SET T1.Phy_Percentile = T2.Phy_Percentile;' %(str(i), str(i)))
        conect.commit()
        cursor.execute('DROP VIEW Session%sJ;' %(str(i)))
        conect.commit()

        cursor.execute('CREATE VIEW Session%sJ AS (SELECT DISTINCT Session%s.Reg_ID, Session%s.Chem_Marks, Session%sP.Chem_Percentile FROM Session%s INNER JOIN Session%sP ON (Session%s.Chem_Marks = Session%sP.Chem_Marks) ORDER BY Session%sP.Chem_Percentile ASC);' %(str(i), str(i), str(i), str(i), str(i), str(i), str(i), str(i), str(i)));
        conect.commit()
        cursor.execute('UPDATE Session%s T1 INNER JOIN Session%sJ T2 ON T1.Reg_ID = T2.Reg_ID SET T1.Chem_Percentile = T2.Chem_Percentile;' %(str(i), str(i)))
        conect.commit()
        cursor.execute('DROP VIEW Session%sJ;' %(str(i)))
        conect.commit()
    
        cursor.execute("DROP VIEW IF EXISTS Session%sP;" %(str(i)))

    cursor.execute('DROP TABLE IF EXISTS Student_FinalScores;')
    cursor.execute("CREATE TABLE Student_FinalScores (Reg_ID Char(11) NOT NULL PRIMARY KEY, Student_Name VARCHAR(40), Total1 INTEGER, Math1 INTEGER, Phy1 INTEGER, Chem1 INTEGER, Total2 INTEGER, Math2 INTEGER, Phy2 INTEGER, Chem2 INTEGER, TP1 FLOAT(10, 7), TP2 FLOAT(10, 7), MP1 FLOAT(10, 7), MP2 FLOAT(10, 7), PP1 FLOAT(10, 7), PP2 FLOAT(10, 7), CP1 FLOAT(10, 7), CP2 FLOAT(10, 7), Total_Percentile FLOAT(10, 7), Math_Percentile FLOAT(10, 7), Phy_Percentile FLOAT(10, 7), Chem_Percentile FLOAT(10, 7), Final_Rank INTEGER);")
    cursor.execute('SELECT Reg_ID, Attempt1, Attempt2, First_Name, Last_Name FROM Student_Master;')
    lis0 = cursor.fetchall()
    conect.commit()

    for i in range(len(lis0)):
        regid = lis0[i][0]
        attempt1 = lis0[i][1]
        attempt2 = lis0[i][2]
        S_name = str(lis0[i][3]) + ' ' + str(lis0[i][4])
        epsilon = 0.0000001
        tp1 = mp1 = cp1 = pp1 = tp2 = mp2 = pp2 = cp2 = 0.00
        t1 = m1 = p1 = c1 = t2 = m2 = c2 = p2 = 'NULL'
        if attempt1 != None:
            cursor.execute("SELECT * FROM Session%s WHERE Reg_ID = '%s';" %(str(attempt1), str(regid)))
            lis1 = cursor.fetchone()
            tp1 = lis1[8]
            mp1 = lis1[5]
            pp1 = lis1[6]
            cp1 = lis1[7]
            t1 = lis1[4]
            m1 = lis1[1]
            p1 = lis1[2]
            c1 = lis1[3]
        if attempt2 != None:
            cursor.execute("SELECT * FROM Session%s WHERE Reg_ID = '%s';" %(str(attempt2), str(regid)))
            lis2 = cursor.fetchone()
            tp2 = lis2[8]
            mp2 = lis2[5]
            pp2 = lis2[6]
            cp2 = lis2[7]
            t2 = lis2[4]
            m2 = lis2[1]
            p2 = lis2[2]
            c2 = lis2[3]

        tp = max(tp1, tp2)
        if abs(tp - tp2) > epsilon:
            mp, pp, cp, t = mp1, pp1, cp1, t1
        elif abs(tp - tp1) > epsilon:
            mp, pp, cp, t = mp2, pp2, cp2, t2
        else:
            mp = max(mp1, mp2)
            if abs(mp - mp2) > epsilon:
                pp, cp, t = pp1, cp1, t1
            elif abs(mp - mp1) > epsilon:
                pp, cp, t = pp2, cp2, t2
            else:
                pp = max(pp1, pp2)
                if abs(pp - pp2) > epsilon:
                    cp, t = cp1, t1
                elif abs(pp - pp1) > epsilon:
                    cp, t = cp2, t2
                else:
                    cp = max(cp1, cp2)
                    if abs(cp - cp2) > epsilon:
                        t = t1
                    elif abs(cp - cp1) > epsilon:
                        t = t2
                    else:
                        t = max(t1, t2)

        cursor.execute("INSERT INTO Student_FinalScores (Reg_ID, Student_Name, Total1, Math1, Phy1, Chem1, Total2, Math2, Phy2, Chem2, TP1, MP1, PP1, CP1, TP2, MP2, PP2, CP2, Total_Percentile, Math_Percentile, Phy_Percentile, Chem_Percentile) VALUES ('%s', '%s', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);" %(str(lis0[i][0]), S_name, str(t1), str(m1), str(p1), str(c1), str(t2), str(m2), str(p2), str(c2), str(tp1), str(mp1), str(pp1), str(cp1), str(tp2), str(mp2), str(pp2), str(cp2), str(tp), str(mp), str(pp), str(cp)))
        conect.commit()
    
    cursor.execute('DROP VIEW IF EXISTS TempRank;')
    cursor.execute('CREATE VIEW TempRank AS (SELECT Reg_ID, Total_Percentile, Math_Percentile, Phy_Percentile, Chem_Percentile,  ROW_NUMBER() OVER (ORDER BY Total_Percentile DESC, Math_Percentile DESC, Phy_Percentile DESC, Chem_Percentile DESC) AS Final_Rank FROM Student_FinalScores ORDER BY Final_Rank);')
    cursor.execute('UPDATE Student_FinalScores T1 INNER JOIN TempRank T2 ON T1.Reg_ID = T2.Reg_ID SET T1.Final_Rank = T2.Final_Rank;')
    cursor.execute('DROP VIEW IF EXISTS TempRank;')
    conect.commit()
    
    conect.close()

#__main__
compute_percentile_rank()
