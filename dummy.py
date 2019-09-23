#this is a dummy python script to check 
#the proper installtion of the virtual env
#and other required modules
#this project uses python version 3.7.3
#=========required modules==========
#pip install virtualenv
#pip install --upgrade google-api-python-client
#pip install --upgrade google-auth-oauthlib google-auth-httplib2
#pip install requests
#pip install textblob
#pip install paralleldots

#install the abouve modules inside the vitualenv

print("hello im in a virtual env")
import csv
import os
import paralleldots
import google.oauth2.credentials
from textblob import TextBlob
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
#if there is no error after executing this file,
#you are good to go