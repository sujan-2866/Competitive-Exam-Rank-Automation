"""
Program allows user to enter student Reg ID and see his scores or alternatively, store data of toppers in a CSV file for users to read using excel or other tools; no. of toppers is decided by user.
Run after generate_percentile_rank_data, needs SQL Password and other inputs from user.
"""

import mysql.connector as msql
import csv
import getpass

password = getpass.getpass('Enter Password for MySQL: ')
conect = msql.connect(user = 'root', host = 'localhost', passwd = password, database = 'JEE_Mains')
cursor = conect.cursor()

while True:
          print()
          n = input("Enter 1 to see the markscard of any student of your choice, by Registration ID. \nEnter 2 to obtain the marks and percentile of the toppers. \nEnter 3 to obtain all students any range of ranks, between lower and upper limit rank. \nEnter 4 to obtain all students in a particular range by total marks. \nEnter 0 to exit: ")
 
          if n == '0':
              print()
              print('Thank you!')
              print()
              conect.close()
              break
 
          elif n == '1':
              print()
              regid = input('Enter Registration ID of student: ')
              print()
              cursor.execute("SELECT * FROM Student_FinalScores WHERE Reg_ID = '%s'" %(regid))
              list3 = cursor.fetchall()
 
              if not list3:
                  print('InvalidRegIDError: Entered Registration ID of Nonexistant Student.')
                  continue
 
              else:
                  list3 = list3[0]
                  print('PRINTING MARKS CARD OF STUDENT', list3[1])
                  print('Registration ID: ', list3[0])
                  print()
                  print('ATTEMPT 1 MARKS:')
                  print('Maths: ', list3[3], '\nPhysics: ', list3[4], '\nChemistry: ', list3[5],     '\nTotal Score: ', list3[2])
                  print()
                  print('ATTEMPT 2 MARKS:')
                  print('Maths: ', list3[7], '\nPhysics: ', list3[8], '\nChemistry: ', list3[9],     '\nTotal Score: ', list3[6])
                  print()
                  print('SUBJECT-WISE PERCENTILES:')
                  print('Maths percentile: ', list3[19])
                  print('Physics percentile: ', list3[20])
                  print('Chemistry percentile: ', list3[21])
                  print()
                  print('ONERALL PERCENTILE: ', list3[18])
                  print('FINAL RANK: ', list3[22])
 
          elif n == '2':
             no = (input('Enter how many top rankers you want to obtain: '))
             print()
             cursor.execute('SELECT Reg_ID, Student_Name, Final_Rank, Total1, Total2, Total_Percentile, Math_Percentile, Phy_Percentile, Chem_Percentile FROM Student_FinalScores ORDER BY Final_Rank LIMIT %s;' %(no))
             list4 = cursor.fetchall()
             header = ('Registration ID', 'Student Name', 'Final Rank', 'Attempt 1 Total', 'Attempt 2 Total', 'Overall Percentile', 'Maths Percentile', 'Physics Percentile', 'Chemistry Percentile')
 
             with open ('Toppers.csv', 'w') as F:
                 writer = csv.writer(F)
                 writer.writerow(header)
                 for row in list4:
                     writer.writerow(row)
             print('Successfully created CSV File Toppers.csv of Toppers.')
          elif n == '3':
            print()
            Lr = int(input('Enter lower rank limit: '))
            Hr = int(input('Enter upper rank limit: '))
            print()
            cursor.execute('SELECT Reg_ID, Student_Name, Final_Rank, Total1, Total2, Total_Percentile, Math_Percentile, Phy_Percentile, Chem_Percentile FROM Student_FinalScores WHERE Final_Rank BETWEEN %s AND %s ORDER BY Final_Rank;' %(str(Lr), str(Hr)))
            list4 = cursor.fetchall()
            header = ('Registration ID', 'Student Name', 'Final Rank', 'Attempt 1 Total', 'Attempt 2 Total', 'Overall Percentile', 'Maths Percentile', 'Physics Percentile', 'Chemistry Percentile')
            with open ('Ranklist.csv', 'w') as F:
                 writer = csv.writer(F)
                 writer.writerow(header)
                 for row in list4:
                     writer.writerow(row)
            print('Successfully created CSV File Ranklist.csv of Rankers between', Lr, 'and', Hr, '.')
          elif n == '4':
              print()
              Lm = int(input('Enter least value of marks for filter: '))
              Hm = int(input('Enter highest value of marks for filter: '))
              print()
              cursor.execute('SELECT Reg_ID, Student_Name, Final_Rank, Total1, Total2, Total_Percentile, Math_Percentile, Phy_Percentile, Chem_Percentile FROM Student_FinalScores WHERE GREATEST(Total1, Total2) BETWEEN %s AND %s ORDER BY Final_Rank;' %(str(Lm), str(Hm)))
              list4 = cursor.fetchall()
              header = ('Registration ID', 'Student Name', 'Final Rank', 'Attempt 1 Total', 'Attempt 2 Total', 'Overall Percentile', 'Maths Percentile', 'Physics Percentile', 'Chemistry Percentile')
              with open ('Markbandlist.csv', 'w') as F:
                   writer = csv.writer(F)
                   writer.writerow(header)
                   for row in list4:
                       writer.writerow(row)
              print('Successfully created CSV File Markbandlist of Scorers between', Lm, 'and', Hm, '.')
          else:
              continue
