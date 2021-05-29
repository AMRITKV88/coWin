import copy
import sys, time
from library import generate_OTP, fetch_user_data, collect_vaccine_center_info, book_vaccine_appointment



def start_with_cowin():
    global ACTUAL_SELECTED_SLOT_INDEX
    try:
        # Data collection starts here....
        mobile_No = None
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
        }
        # Take user's mobile number to generate OTP....
        mobile_No = input("\n--> Enter the registered mobile number : ")

        if mobile_No:
            response_token = generate_OTP(mobile_No, header)
        else:
            print("\n--> Mobile number can not be empty....!\n")
            time.sleep(4)
            sys.exit()

        updated_header = copy.deepcopy(header)
        updated_header["Authorization"] = f"Bearer {response_token}"

        # Fetch user data just for confirmation
        print("\n\n################## Fetching Registered User Data ##################")
        fetch_user_data(updated_header)
    
        # Start checking vaccine availability
        print("\n\n################## Start Checking Vaccine Availability ##################")
        collect_vaccine_center_info(updated_header)

        # Start booking vaccination center as per the user preferred choice
        print("\n\n################## Start Booking Vaccine Appointment ##################")
        book_vaccine_appointment(updated_header)


    except Exception as e:
        print(str(e))
        print("\n--> There might be some issues while running the script....!\n")


def main():

    print("\n--> Before starting to find the slot & booking procedure, please register yourself on this portal --> https://selfregistration.cowin.gov.in \n")
    print("--> Let's go for --> Finding slots for Covid Vaccine & booking the slots....!")

    start_with_cowin()


if __name__ == '__main__':
    main()