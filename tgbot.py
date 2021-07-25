#base_cowin_url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=142&date=21-07-2021"

import requests
from datetime import datetime
import time
import schedule

base_cowin_url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict"

now = datetime.now()
today_date = now.strftime("%d-%m-%Y")
api_url_telegram = "https://api.telegram.org/........=@__groupid__&text="
group_id = "Getvaccineasap"


def fetch_data_from_cowin(district_id):
    query_params = "?district_id={}&date={}".format(district_id, today_date)
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    final_url = base_cowin_url+query_params
    response = requests.get(final_url, headers=headers)
    extract_availability_data(response)
    print(response)

def extract_availability_data(response):
    response_json = response.json()
    # count=0
    for center in response_json["centers"]:
        for session in center["sessions"]:
            # if session["available_capacity_dose1"]>0:             
                # print(center["center_id"], center["name"],
                #  session["available_capacity_dose1"],             
                #  session["min_age_limit"])                        
                message= "Pincode: {} \nName: {}  \nDose-1:{}  \nDose-2:{}  \nDate: {}  \nVaccine: {}  \nFee Type: {}  \nMinimum Age: {} \n----".format(
                    center["pincode"], center["name"],
                    session["available_capacity_dose1"],
                    session["available_capacity_dose2"],
                    session["date"],
                    session["vaccine"],
                    center["fee_type"],
                    session["min_age_limit"]
                )     
                send_message_telegram(message)
def send_message_telegram(message):       
    final_telegram_url = api_url_telegram.replace("__groupid__", group_id)
    final_telegram_url=final_telegram_url + message     
    response = requests.get(final_telegram_url)
    print(response)   
                                                                                                      
if __name__=="__main__":
#    fetch_data_from_cowin(247)
    schedule.every(10).seconds.do(lambda: (fetch_data_from_cowin(247)))                     
    while True:
        schedule.run_pending()
        time.sleep(1)
