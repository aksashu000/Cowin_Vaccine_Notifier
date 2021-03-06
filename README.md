# Warning 
This is not a production system setup and is purely for learning purpose. 
We will be using Cowin public API and it is advisable not to overwhelm the Cowin's system with lot of API calls as your IP may get blocked.

# Cowin Vaccine Notifier
Python(3.7) script to automate the notification of Cowin vaccine slots availability. You can schedule this script in Windows Task Scheduler or Crontab in Linux/Ubuntu systems. I have added information on how to schedule this on Amazon Web Services. See the tutorial video link at the bottom of this page.

# Pre requisite
pip install twilio

Also, I have included "dependencies.zip" file which contains the necessary packages for running the script. If you are unable to install twilio using pip, you may try with these given dependencies packages. Just extract them in the same project folder.

# Important points about Twilio
Twilio API has been used to send SMS notification. There are some steps that you need to follow.
1. Sign up for a free account on Twilio: https://www.twilio.com/.
2. After logging in, add your phone number on which you want to receive SMS notifications.
3. You'll also have to create a US/Canada phone number (free). You will get some TRIAL BALANCE (around 15 USD).
4. On the Dashboard page, make a note of the "ACCOUNT SID" and "AUTH TOKEN". These values will be used in sendSMS() function.
5. Once your Twilio account set up is complete, you can create environment variables TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN and use them in the sendSMS() function.
6. Twilio's SMS API has limitation of 1600 characters.

# Youtube tutorial video
[![Cowin Vaccine Notifier](Title.png)](http://www.youtube.com/watch?v=HbQCwNHL3S4&t=15s)
