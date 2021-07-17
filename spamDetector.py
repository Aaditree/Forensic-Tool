import streamlit as st
import pickle
import sklearn
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import smtplib
import time
import imaplib
import email
import traceback
import bs4
from bs4 import BeautifulSoup
import csv
from email import policy
from datetime import datetime
#from win32com.client import Dispatch
import requests
import json
import os
import pandas as pd

url = "https://www.fast2sms.com/dev/bulk"

headers = {
'authorization': "yAjeClukhD2MGx093RNobUwnLdrmp5ZJKsvB1QaPtfzVSIiO4qVBpJHqFYfSvOci4htoxar3wGP9KNXZ",
'Content-Type': "application/x-www-form-urlencoded",
'Cache-Control': "no-cache",
}


ORG_EMAIL = "@gmail.com" 
FROM_EMAIL = "clearedaccess" + ORG_EMAIL 
FROM_PWD = "clear.access123@@@" 
SMTP_SERVER = "imap.gmail.com" 
SMTP_PORT = 993

ll=[]
full=[]

def read_email_from_gmail():
        mail = imaplib.IMAP4_SSL(SMTP_SERVER)
        mail.login(FROM_EMAIL,FROM_PWD)
        
        mail.list()
        mail.select('inbox')

        n=0
        (retcode, messages) = mail.search(None, '(UNSEEN)')
        if retcode == 'OK':

          for num in messages[0].split() :
            print ('Processing ')
            n=n+1
            typ, data = mail.fetch(num,'(RFC822)')
            for response_part in data:
              if isinstance(response_part, tuple):
                original = email.message_from_bytes(response_part[1])

                raw_email = data[0][1]
                raw_email_string = raw_email.decode('utf-8')
                email_message = email.message_from_string(raw_email_string)
              
                for part in email_message.walk():
                        if (part.get_content_type() == "text/plain"): # ignore attachments/html
                              body = part.get_payload(decode=True)
                              full.append([original['From'],original['Subject'],body.decode('utf-8') ])
                              fin = body.decode('utf-8')
                              ll.append([fin])
                              print(fin)

			       
                              
                        else:
                              continue
                with open('forensic_files.csv','w') as files:
                  csvwriter = csv.writer(files)
                  csvwriter.writerow(['From','Subject','Body'])
                  csvwriter.writerows(full)

                typ, data = mail.store(num,'+FLAGS','\\Seen')
                for i in ll:
                  if(spam_not_spam(i)==1):
                    mail.store(num, '+X-GM-LABELS', '\Spam')				
                    my_data={'sender_id':'FSTSMS', 'message': 'SPAM ALERT:'+str(i),'language':'english','route':'p','numbers':'9158074343'}
                    response = requests.request("POST",url,data = my_data,headers = headers)
                    print(response.text)
                    

                
        return ll

def spam_not_spam(lst):
  row=[]
  vec=cv.transform(lst).toarray()
  result=model.predict(vec)
  if result[0]==0:
    return 0
  else:
    return 1
			


'''def speak(text):
	speak=Dispatch(("SAPI.SpVoice"))
	speak.Speak(text)'''


model = pickle.load(open('spam.pkl','rb'))
cv=pickle.load(open('vectorizer.pkl','rb'))


def main():
	st.title("Email Spam Classification")
	activites=["Automatic Forensic Classification","Manual Forensic Classification"]
	choices=st.sidebar.selectbox("Choose method",activites)
	if choices=="Automatic Forensic Classification":
		
		while(choices=="Automatic Forensic Classification"):
      
			now = datetime.now()
			nw=now.strftime("%d %m %Y %H %M %S")
			filename='forensic_file_'+str(nw)+'.csv'
			lst=read_email_from_gmail()
      
			row=[]
			for data in lst:
				print(data)
				vec=cv.transform(data).toarray()
				result=model.predict(vec)
				if result[0]==0:
					st.success("This is Not A Spam Email")
					row.append([data,'Not Spam'])
				else:
					st.error("This is A Spam Email")
					row.append([data,'Spam'])
					
			with open(filename,'w') as csvfile:
					csvwriter=csv.writer(csvfile)
					csvwriter.writerow(['text','spam/not spam'])
					csvwriter.writerows(row)			
			df= pd.read_csv(filename)
			if df.empty == True:
        				os.remove(filename)

	elif choices=="Manual Forensic Classification":
		now = datetime.now()
		nw=now.strftime("%d %m %Y %H %M %S")
		filename='forensic_file_'+str(nw)+'.csv'
		print("Checking..." + "\n")
		print("Click on Process to get results")
		lst=[]
		

		if st.button("PROCESS"):
			row=[]
			lst=read_email_from_gmail()
			for data in lst:
				print(data)
				vec=cv.transform(data).toarray()
				result=model.predict(vec)
				if result[0]==0:
					st.success("This is Not A Spam Email")
					row.append([data,'Not Spam'])
	
				else:
					st.error("This is A Spam Email")
					row.append([data,'Spam'])
					

			with open(filename,'w') as csvfile:
					csvwriter=csv.writer(csvfile)
					csvwriter.writerow(['text','spam/not spam'])
					csvwriter.writerows(row)
			df= pd.read_csv(filename)
			if df.empty == True:
					os.remove(filename)
			
			
		if st.button("STOP"):
				st.empty()	
	
	
main()
