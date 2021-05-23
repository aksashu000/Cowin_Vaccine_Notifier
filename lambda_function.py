import requests, json, os, traceback
from types import SimpleNamespace as Namespace
from datetime import datetime, timedelta
from twilio.rest import Client

def sendSMS(message):
    # The following line needs your Twilio Account SID and Auth Token
    # They have been declared as environment variables so that to avoid putting credentials in the code
    client = Client(os.environ['TWILIO_ACCOUNT_SID'], os.environ['TWILIO_AUTH_TOKEN'])

    #SMS can contain only 1600 characters, so we will limit it to avoid exception
    if(len(message)>=1600):        
        message = message[0:1500] 

    # "from_" number is your Twilio number and the "to" number is the phone number you signed up for Twilio with
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

    #Set the below header, otherwise, you may get 403 error
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}
    slotFound = False
    #Create empty set to store the message to be sent
    message = set()

    for url in one_month_urls:
        response = str(requests.get(url, headers=headers).json()).replace("\'", "\"")
        data = json.loads(response, object_hook = lambda d : Namespace(**d))
                
        for center in data.centers:
            for session in center.sessions:
                #Check the slots for 18+ age, dose1
                if session.available_capacity_dose1 > 0 and "18" in str(session.min_age_limit):                
                    message.add(str(center.pincode)+"_"+session.date+"_"+str(session.available_capacity_dose1))
                    slotFound = True                
        
    if slotFound:
        sendSMS(str(message))        
    else:        
        print("No slot found.")

# This method is automatically invoked by AWS when the code is deployed as Lambda function
def lambda_handler(event, context):
    try:    
        pinCodeList=['560087', '560037', '560066', '844114', '847422', '800001', '403505']
        #Call the function with the desired pin code list
        findVaccineSlotsAvailability(pinCodeList)
        return {
            'statusCode': 200,
            'body': json.dumps('Execution completed successfully!')
        }
    except Exception as e:
        #sendSMS("Exception occurred." + str(e))
        traceback.print_exc()

#lambda_handler("","")