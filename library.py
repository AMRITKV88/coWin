
import requests, sys, os, time, json
from hashlib import sha256
from datetime import datetime
import pandas as pd
from tabulate import tabulate

NAME_OF_PEOPLE_TO_VACCINATE = []
ACTUAL_TABLE_INDEX_OF_PEOPLE_TO_VACCINATE = -100
REG_USER_DETAILS = []
VACCINE_CENTERS_BY_PINCODE = -1
VACCINE_CENTERS_BY_STATE_DIST = []
VACCINE_CENTER_DETAILS = []
REG_USER_AGE_LIST = []
STRUCTURED_VACCINE_CENTER_DETAILS = []
ACTUAL_SELECTED_SLOT_INDEX = -100
REG_USER_COMPLETE_DATA = []
VACCINE_CENTER_COMPLETE_DATA = []
ACTUAL_SELECTED_VACCINE_CENTER_INDEX = -100

URL_GEN_OTP = 'https://cdn-api.co-vin.in/api/v2/auth/generateMobileOTP'
URL_VAL_OTP = 'https://cdn-api.co-vin.in/api/v2/auth/validateMobileOtp'
URL_FETCH_USER_DETAILS = "https://cdn-api.co-vin.in/api/v2/appointment/beneficiaries"
URL_VACCINE_CENTER_BY_PINCODE = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/calendarByPin?pincode={0}&date={1}"

##############################################################################################################################

# Print the data in a good tabular format
def show_details_in_tabular_format(consolidated_details):

    header = []
    row = []
    rows = []
    a = list(consolidated_details[0].keys())
    header = (['Index'] + a)
    i = 1
    for r in consolidated_details:
        row.append(i)
        for col in header[1:]:
            row.append(r[col])
        rows.append(row[:])
        i += 1
        row.clear()
    print(tabulate(rows, header, tablefmt='grid'))

##############################################################################################################################

# Display the vaccine center details (except the slot column) in tabular format
def show_vaccine_center_in_tabular_format(structured_vaccine_center_details):

    header = []
    row = []
    rows = []
    a = list(structured_vaccine_center_details[0].keys())
    header = (['Index'] + a)
    i = 1
    for r in structured_vaccine_center_details:
        row.append(i)
        for col in header[1:-2]:
            row.append(r[col])
        rows.append(row[:])
        i += 1
        row.clear()
    print("\n\n")
    print(tabulate(rows, header, tablefmt='grid'))

##############################################################################################################################

# Display the list of available slots for selected vaccine center
def show_vaccine_slots_in_tabular_format(vaccine_slots):

    header = []
    a = list(vaccine_slots.keys())
    header = (['Index'] + a)
    row= []
    rows = []
    i = 0
    for x in range(len(vaccine_slots["Slots"])):
        row.append(i+1)
        row.append(vaccine_slots["Slots"][x])
        rows.append(row[:])
        i += 1
        row.clear()
    print("\n\n--> Available vaccine slots for chosen vaccination center....!\n\n")
    print(tabulate(rows, header, tablefmt='grid'))

##############################################################################################################################

# Shows the vaccine details for all the centers
def fetch_vaccine_center_details(list_of_vaccine_centers):
    
    global REG_USER_AGE_LIST
    global ACTUAL_TABLE_INDEX_OF_PEOPLE_TO_VACCINATE
    actual_session_as_per_user_age = []

    for center in list_of_vaccine_centers["centers"]:

        for ii in range(len(center["sessions"])):

            if center["sessions"][ii]["min_age_limit"] == 45 & REG_USER_AGE_LIST[ACTUAL_TABLE_INDEX_OF_PEOPLE_TO_VACCINATE] >= 45:
                vacc_center_details = {
                    "Name" : center["name"],
                    "Vacc_Age" : center["sessions"][ii]["min_age_limit"],
                    "Vaccine" : center["sessions"][ii]["vaccine"],
                    "Fee" : center["fee_type"],
                    "Date" : center["sessions"][ii]["date"],
                    "Avl. Dose 1" : center["sessions"][ii]["available_capacity_dose1"],
                    "Avl. Dose 2" : center["sessions"][ii]["available_capacity_dose2"],
                    "Session_Id" : center["sessions"][ii]["session_id"],
                    "Slots" : center["sessions"][ii]["slots"]
                }
                actual_session_as_per_user_age.append(vacc_center_details)
            
            elif (center["sessions"][ii]["min_age_limit"] == 18) & (REG_USER_AGE_LIST[ACTUAL_TABLE_INDEX_OF_PEOPLE_TO_VACCINATE] <= 44):
                vacc_center_details = {
                    "Name" : center["name"],
                    "Vacc_Age" : center["sessions"][ii]["min_age_limit"],
                    "Vaccine" : center["sessions"][ii]["vaccine"],
                    "Fee" : center["fee_type"],
                    "Date" : center["sessions"][ii]["date"],
                    "Avl. Dose 1" : center["sessions"][ii]["available_capacity_dose1"],
                    "Avl. Dose 2" : center["sessions"][ii]["available_capacity_dose2"],
                    "Session_Id" : center["sessions"][ii]["session_id"],
                    "Slots" : center["sessions"][ii]["slots"]
                }
                actual_session_as_per_user_age.append(vacc_center_details)
            else:
                continue
            
    return actual_session_as_per_user_age

##############################################################################################################################

# Take user input for desired pincodes
def take_user_defined_pincode():

    user_defined_pincode = -1
    while(True):
        try:
            user_defined_pincode = int(input("\n\n--> Please enter the pincode (example: 111111): "))

            if (len(str(user_defined_pincode))>6) or (not user_defined_pincode) or (len(str(user_defined_pincode))<6) :
                print("\n\n--> Please input a valid PIN code number as per given format....!")
                continue
            else:
                return user_defined_pincode

        except ValueError or TypeError:
            print('\n\n--> Please input a valid PIN code number as per given format....!')
            continue

##############################################################################################################################

# Search vaccine center by pincode
def search_vaccine_center_by_pincode(updated_header):
    
    global VACCINE_CENTERS_BY_PINCODE
    global STRUCTURED_VACCINE_CENTER_DETAILS
    global VACCINE_CENTER_COMPLETE_DATA

    try:
        print("\n\n--> Searching For Vaccine Locations Based On Your Given Pincodes From Date : Today Till Next 4 Days....!")
        date_today = datetime.today().strftime('%d-%m-%Y')
        vaccine_details_by_pincode = []
        base_url = URL_VACCINE_CENTER_BY_PINCODE
        pincode = take_user_defined_pincode()

        # This section checks for available centers for all the pincodes
        # If the status code is not 200 for any of the pincodes, it restarts the loop again
        restart = False
        while restart==False:

            vaccine_details_by_pincode = requests.get(base_url.format(pincode, date_today), headers=updated_header)
        
            if vaccine_details_by_pincode.status_code == 200 :
                VACCINE_CENTERS_BY_PINCODE = vaccine_details_by_pincode.json()
                VACCINE_CENTER_COMPLETE_DATA = VACCINE_CENTERS_BY_PINCODE
                restart = True
            else:
                print("\n\n--> There might have some errors to fetch location details. Trying Again....!")
                restart = False

        # List the vaccine center details as per the user's age
        STRUCTURED_VACCINE_CENTER_DETAILS = fetch_vaccine_center_details(VACCINE_CENTERS_BY_PINCODE)
        show_vaccine_center_in_tabular_format(STRUCTURED_VACCINE_CENTER_DETAILS)
        return STRUCTURED_VACCINE_CENTER_DETAILS
    except Exception as e:
        print(str(e))
        sys.exit(1)

##############################################################################################################################

# Search vaccine center by state & dist
def search_vaccine_center_by_state_dist(updated_header):
    pass

##############################################################################################################################

# Method to generate OTP
def generate_OTP(mobile_No, base_header):

    valid_token = False

    while not valid_token:

        try:
            data = {"mobile": mobile_No,
                    "secret": "U2FsdGVkX1+z/4Nr9nta+2DrVJSv7KS6VoQUSQ1ZXYDx/CJUkWxFYG6P3iM/VW+6jLQ9RDQVzp/RcZ8kbT41xw=="
            }
            txnId = requests.post(url=URL_GEN_OTP, json=data, headers=base_header)
            if txnId.status_code == 200:

                print("\n"f"--> OTP sent to the given {mobile_No} mobile number....!")
                txnId = txnId.json()['txnId']

                OTP = input("\n"f"--> Please enter the OTP sent to your mobile number {mobile_No} : ")

                if OTP:

                    data = {"otp": sha256(str(OTP).encode('utf-8')).hexdigest(), "txnId": txnId}
                    print("\n"f"--> Validating the OTP....!")
                    token = requests.post(url= URL_VAL_OTP , json=data, headers=base_header)

                    if token.status_code == 200:
                        token = token.json()['token']
                        print("\n""--> OTP Validation successful....!")
                        valid_token = True
                        print(token)
                        return token

                    else:
                        print("\n""--> Invalid OTP --> OTP validation UN-Successfull....!")
                        time.sleep(4)
                        sys.sys.exit()

            else:
                print("\n"f"--> Unable to send OTP to the given {mobile_No} mobile number....!")
                sys.sys.exit()

        except Exception as e:
            print(str(e))

##############################################################################################################################

# Fetch user data after login
def fetch_user_data(updated_header):

    global REG_USER_DETAILS
    global NAME_OF_PEOPLE_TO_VACCINATE
    global ACTUAL_TABLE_INDEX_OF_PEOPLE_TO_VACCINATE
    global REG_USER_COMPLETE_DATA
    # Hitting the API to fetch registered user details
    registered_users = requests.get(URL_FETCH_USER_DETAILS, headers=updated_header)
    
    if registered_users.status_code == 200:
        print("AG")
        registered_users = registered_users.json()['beneficiaries']
        REG_USER_COMPLETE_DATA = registered_users

        if len(registered_users) == 0:
            print("\n--> There is no registered user for the given mobile number....\n")
            print("\n--> Either --> Visit 'https://selfregistration.cowin.gov.in' to register yourself....\n\nOr --> Begin with registered mobile number\n")
            sys.exit(1)

        else :
            consolidated_registered_users_details = []
            i = 0
            for registered_user in registered_users:
                reg_user_age = datetime.today().year - int(registered_user['birth_year'])
                REG_USER_AGE_LIST.append(reg_user_age)
                reg_user_details = {
                    "Ref_id": registered_user["beneficiary_reference_id"],
                    "Name": registered_user["name"],
                    "Vaccine Status": registered_user["vaccination_status"],
                    "Vaccine": registered_user["vaccine"],
                    "Dose-1 Dt.": registered_user["dose1_date"],
                    "Dose-2 Dt.": registered_user["dose2_date"],
                    "Appointments": registered_user["appointments"]            
                }
                i += 1
                consolidated_registered_users_details.append(reg_user_details)
            REG_USER_DETAILS = consolidated_registered_users_details
            print("\n--> Showing basic details of the registered users\n")
            show_details_in_tabular_format(REG_USER_DETAILS)
    
    else:
        print('\n\n--> Unable to fetch regsitered user details')
        print("\n\n", registered_users.status_code)
        print("\n\n", registered_users.text)
        sys.exit(1)

    while(True):
        try:
            table_index_of_people_to_vaccinate = int(input("\n\n--> Enter the index values of the people from the table who wants to get vaccinated (example : 1) : "))
            ACTUAL_TABLE_INDEX_OF_PEOPLE_TO_VACCINATE = table_index_of_people_to_vaccinate - 1
            if (ACTUAL_TABLE_INDEX_OF_PEOPLE_TO_VACCINATE>len(REG_USER_DETAILS)) :
                print("\n\n--> Please enter valid number of people from the table....!")
                continue
            else:
                try:
                    NAME_OF_PEOPLE_TO_VACCINATE.append(REG_USER_DETAILS[ACTUAL_TABLE_INDEX_OF_PEOPLE_TO_VACCINATE]["Name"])
                    print("\n--> Your requested name(s) -->")
                    print("\n\t\t\t\t"f"--------> {NAME_OF_PEOPLE_TO_VACCINATE}""\n")
                    break
                except IndexError:
                    print('\n\n--> Please enter a valid index number as per the given table....!')
                    continue
        except ValueError or TypeError:
            print('\n\n--> Please input a valid number as per given format....!')
            continue
    
##############################################################################################################################

# Collect desired vaccination center details
def collect_vaccine_center_info(updated_header):
    
    global ACTUAL_SELECTED_SLOT_INDEX
    global ACTUAL_SELECTED_VACCINE_CENTER_INDEX

    vacc_loc_choice = int(input("\n\n--> Search Vaccine Centers by (--Pincode--) or (--State & Dist--) --> Enter 1 for Pincode, 2 for State & Dist (Default 2) : "))

    if vacc_loc_choice == 1 :
        structured_vacc_center = search_vaccine_center_by_pincode(updated_header)

    elif vacc_loc_choice == 2 :
        structured_vacc_center = search_vaccine_center_by_state_dist(updated_header)

    elif not vacc_loc_choice or  vacc_loc_choice not in [1,2]:
        print("\n\n--> Going with the default choice : State & Dist")
        structured_vacc_center = search_vaccine_center_by_state_dist(updated_header)

    if (not structured_vacc_center) :
                
        print("\n\n--> There is no vaccination center available as per given Pincode/State_Dist/Age....! Please Try Again....!")
        # Need to implement repeated search for pincode if no vacc center found

     

    # Ask user to choose one of the centers based upon availability
    while(True):
        try:   
            selected_vacc_center_index = int(input("\n\n--> Please select one vaccine center as per the table index (example : 1) : "))
            ACTUAL_SELECTED_VACCINE_CENTER_INDEX = selected_vacc_center_index - 1
            slot_selection = {"Slots" : structured_vacc_center[ACTUAL_SELECTED_VACCINE_CENTER_INDEX]["Slots"]}
            show_vaccine_slots_in_tabular_format(slot_selection)
            selected_vacc_slot_index = int(input("\n\n--> Please select one slot (example : 1) : "))
            ACTUAL_SELECTED_SLOT_INDEX = selected_vacc_slot_index-1
            print("\n\n--> "f"Your selected vaccine slot is : {slot_selection['Slots'][ACTUAL_SELECTED_SLOT_INDEX]}")
            break

        except ValueError or TypeError:
            print('\n\n--> Please input a valid number as per given format....!')
            continue

##############################################################################################################################

# Start booking as per the given user input
def book_vaccine_appointment(updated_header):

    global REG_USER_DETAILS
    global ACTUAL_TABLE_INDEX_OF_PEOPLE_TO_VACCINATE
    global VACCINE_CENTER_COMPLETE_DATA
    global ACTUAL_SELECTED_VACCINE_CENTER_INDEX
    global STRUCTURED_VACCINE_CENTER_DETAILS
    global ACTUAL_SELECTED_SLOT_INDEX

    print("\n\n"f"REG_USER_DETAILS : {REG_USER_DETAILS}")
    print("\n\n"f"ACTUAL_TABLE_INDEX_OF_PEOPLE_TO_VACCINATE : {ACTUAL_TABLE_INDEX_OF_PEOPLE_TO_VACCINATE}")
    print("\n\n"f"VACCINE_CENTER_COMPLETE_DATA : {VACCINE_CENTER_COMPLETE_DATA}")
    print("\n\n"f"ACTUAL_SELECTED_VACCINE_CENTER_INDEX : {ACTUAL_SELECTED_VACCINE_CENTER_INDEX}")
    print("\n\n"f"STRUCTURED_VACCINE_CENTER_DETAILS : {STRUCTURED_VACCINE_CENTER_DETAILS}")
    print("\n\n"f"ACTUAL_SELECTED_SLOT_INDEX : {ACTUAL_SELECTED_SLOT_INDEX}")


    # booking_req_data = {
    # 'beneficiaries': REG_USER_DETAILS[ACTUAL_TABLE_INDEX_OF_PEOPLE_TO_VACCINATE]['beneficiary_reference_id'],
    # 'dose': 2 if REG_USER_DETAILS[ACTUAL_TABLE_INDEX_OF_PEOPLE_TO_VACCINATE]['Vaccine Status'] == 'Partially Vaccinated' else 1,
    # 'center_id' : VACCINE_CENTER_COMPLETE_DATA[ACTUAL_SELECTED_VACCINE_CENTER_INDEX]['center_id'],
    # 'session_id': STRUCTURED_VACCINE_CENTER_DETAILS[ACTUAL_SELECTED_VACCINE_CENTER_INDEX]['Session_Id'],
    # 'slot'      : STRUCTURED_VACCINE_CENTER_DETAILS['Slots'][ACTUAL_SELECTED_SLOT_INDEX]
    # }

    


##############################################################################################################################