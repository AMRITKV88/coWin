from tabulate import tabulate
import time

from datetime import datetime
data = [{'beneficiary_reference_id': '72775533509960', 'Name': 'Amrit Kumar Verma', 'Year of Birth': '1993', 'Last 4 Digits of Mob.No.': '4433', 'Photo Id Type': 'PAN Card', 'Photo Id Number': 'ATCPV8543J', 'Comorbidity Ind': 'N', 'Vaccination Status': 'Not Vaccinated', 'Vaccine': '', 'Dose - 1 Date': '', 'Dose - 2 Date': '', 'Appointments': []}, {'beneficiary_reference_id': '10453461400050', 'Name': 'Kuldeep Singh', 'Year of Birth': '1992', 'Last 4 Digits of Mob.No.': '4433', 'Photo Id Type': 'PAN Card', 'Photo Id Number': 'DNKPS0631F', 'Comorbidity Ind': 'N', 'Vaccination Status': 'Not Vaccinated', 'Vaccine': '', 'Dose - 1 Date': '', 'Dose - 2 Date': '', 'Appointments': []}]

# header = []
# a = list(data[0].keys())
# header = (['Index'] + a)

# row= []
# rows = []
# i = 0
# for r in data:
#     row.append(i)
#     for col in header[1:]:
#         row.append(r[col])
#     rows.append(row[:])
#     i += 1
#     row.clear()

# print("\n*************")

# print(tabulate(rows, header, tablefmt='grid'))


#############################################################################################################################

# TABLE_INDEX_OF_PEOPLE_TO_VACCINATE =[]
# NAME_OF_PEOPLE_TO_VACCINATE=[]

# while(True):
#     try:
#         TABLE_INDEX_OF_PEOPLE_TO_VACCINATE = [int(x) for x in input("\n\nEnter the comma seperated index values of the people from the table who wants to get vaccinated (example : 0,1,2) : ").split(',')]

#         if (len(TABLE_INDEX_OF_PEOPLE_TO_VACCINATE)>len(data)) or (not TABLE_INDEX_OF_PEOPLE_TO_VACCINATE) :
#             print("\n\n--> Please enter valid number of people from the table....!")
#             continue
#         else:
#             try:
#                 for people in TABLE_INDEX_OF_PEOPLE_TO_VACCINATE:
#                     NAME_OF_PEOPLE_TO_VACCINATE.append(data[people]['Name'])
#                 print("\nYour requested name(s) -->")
#                 for l in range(len(NAME_OF_PEOPLE_TO_VACCINATE)):
#                     print("\n\t\t\t\t"f"--------> {NAME_OF_PEOPLE_TO_VACCINATE[l]}""\n")
#                 break
#             except IndexError:
#                 print('\n\n--> Please enter a valid index number as per the given table....!')
#                 continue
#     except ValueError:
#         print('\n\n--> Please input a valid number as per given format....!')
#         continue

#############################################################################################################################

# import datetime
# a = datetime.datetime.today()
# b = a.date()
# c = b + datetime.timedelta(days=4)
# print(a)
# print(b)
# print(c)    

#############################################################################################################################

# pincodes = [111111,222222]
# ag = pincodes
# a = 3
# restart = False
# while restart==False:
#     for pincode in pincodes :
#         if a == 2:
#             print("a=2")
#             restart = True
#             # continue
#         else:
#             print("else")
#             restart = False

#############################################################################################################################

# def ag():
#     while(True):
#         try:
#             user_defined_pincode = int(input("\n\n--> Enter one or more comma separated pincodes (example: 711111): "))

#             if (len(str(user_defined_pincode))>6) or (not user_defined_pincode) or (len(str(user_defined_pincode))<6) :
#                 print("\n\n--> Please input a valid PIN code number as per given format....!")
#                 continue
#             else:
#                 return user_defined_pincode

#         except ValueError or TypeError:
#             print('\n\n--> Please input a valid PIN code number as per given format....!')
#             continue

# print(ag())

#############################################################################################################################

# date_today = datetime.today().strftime('%d-%m-%Y')
# # date_today = date_today.date()
# print(date_today)

#############################################################################################################################

vacc = [{'Name': 'Urban Primary Health Centre', 'Vacc_Age': 18, 'Vaccine': 'COVISHIELD', 'Date': '22-05-2021', 'Avl. Dose 1': 0, 'Avl. Dose 2': 0, 'Slots': ['09:00AM-10:00AM', '10:00AM-11:00AM', '11:00AM-12:00PM', '12:00PM-03:00PM']}, {'Name': 'STNM Hospital Sochakgang', 'Vacc_Age': 18, 'Vaccine': 'COVISHIELD', 'Date': '22-05-2021', 'Avl. Dose 1': 0, 'Avl. Dose 2': 0, 'Slots': ['09:00AM-10:00AM', '10:00AM-11:00AM', '11:00AM-12:00PM', '12:00PM-03:00PM']}]
ag = {"Slots" : vacc[0]["Slots"]}
print(ag)

header = []
a = list(ag.keys())
header = (['Index'] + a)

row= []
rows = []
i = 0

for x in range(len(ag["Slots"])):
    row.append(i+1)
    row.append(ag["Slots"][x])
    rows.append(row[:])
    i += 1
    row.clear()

print("\n*************")

print(tabulate(rows, header, tablefmt='grid'))