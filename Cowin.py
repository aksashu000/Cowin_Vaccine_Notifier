import requests, json, os
from types import SimpleNamespace as Namespace
from datetime import datetime, timedelta
from twilio.rest import Client

def sendSMS(message):    
    # the following line needs your Twilio Account SID and Auth Token
    client = Client(os.environ['TWILIO_ACCOUNT_SID'], os.environ['TWILIO_AUTH_TOKEN'])

    #SMS can contain only 1600 characters, so we will limit it to avoid exception
    if(len(message)>=1600):        
        message = message[0:1500] 

    # change the "from_" number to your Twilio number and the "to" number
    # to the phone number you signed up for Twilio with, or upgrade your
    # account to send SMS to any phone number
    client.messages.create(to="+917596911771", from_="+19514674784",body=message)            

def findVaccineSlotsAvailability(pinCodeList):    
    #Cowin URL
    url = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode='

    #We will check the slots for one month
    one_month_urls = list()
    for pin in pinCodeList:
        current = datetime.today().strftime('%d-%m-%Y')
        tempUrl = url + pin + "&date="
        for i in range(7,29,7):
            one_month_urls.append(tempUrl+current)
            next_week = datetime.today() + timedelta(days=i)
            current = next_week.strftime('%d-%m-%Y')

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}
    slotFound = False
    message = set()

    for url in one_month_urls:
        response = str(requests.get(url, headers=headers).json()).replace("\'", "\"")
        data = json.loads(response, object_hook = lambda d : Namespace(**d))
                
        for center in data.centers:
            for session in center.sessions:
                #Chech the slots for 18+ age
                if session.available_capacity > 0 and "45" in str(session.min_age_limit):                
                    message.add(str(center.pincode)+"_"+session.date+"_"+str(session.available_capacity))
                    slotFound = True                
        
    if slotFound:
        sendSMS(str(message))        
    else:        
        print("No slot found.")

#Call the function with the desired pin code list
pinCodeList=['560087', '560037', '560066', '411028', '800001', '800020', '800008', '800007', '249401', '249402', '249403']
findVaccineSlotsAvailability(pinCodeList)