import os
from .whatsapp import WhatsApp
import time
import json
import random
import re
import sys
import urllib.parse
import bs4
import requests
import chromedriver_autoinstaller


import time
import datetime as dt
import json
import os
import requests
import shutil
import pickle
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from urllib.parse import urlencode
try:
    from bs4 import BeautifulSoup
except ModuleNotFoundError:
    print("Beautiful Soup Library is reqired to make this library work(For getting participants list for the specified group).\npip3 install beautifulsoup4")

chromedriver_autoinstaller.install()

def ayushbot(receiver):
    client_name = str(random.randint(1337, 9696913371337)).rjust(13, '0')
    url = 'https://www.pandorabots.com/mitsuku/'
    session = requests.Session()
    session.headers.update({
        'User-Agent': ' '.join(('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2)',
                                'AppleWebKit/537.36 (KHTML, like Gecko)',
                                'Chrome/72.0.3626.119 Safari/537.36')),
        'Referer': url
    })

    main_page = session.get(url).text
    main_soup = bs4.BeautifulSoup(main_page, 'lxml')
    botkey = re.search(r'PB_BOTKEY: "(.*)"', main_page).groups()[0]

    whatsapp = WhatsApp(100, session="mysession")
    whatsapp.send_message(receiver, "AyushBOT will serve you till Ayush comes online and answers your questions. As it is still very young AyushBOT can act very stupid sometimes. Please dont mind it. Start talking with AyushBOT below")
    newmessages=[]
    responses=[]
    while 1==1:
        messages = whatsapp.get_last_message_for(receiver)
        newmessages.append(messages)
        print(newmessages)
        if len(newmessages)>1:
            if len(newmessages)>10:
                newmessages=newmessages[:-5]

            if newmessages[-1][-1] != newmessages[-2][-1]:
                try:
                    query=str(messages[-1])
                    response_raw = session.post(
                    f'https://miapi.pandorabots.com/talk?'
                    f'botkey={botkey}&'
                    f'input={query}&'
                    f'client_name={client_name}&'
                    f'sessionid=null&'
                    f'channel=6').text
                    try:
                        response_json = json.loads(response_raw)
                    except json.JSONDecodeError:
                        # Sometimes Mitsuku sends stuff like pictures.
                        response_json = {'responses': ["<i can't understand it, bro>"]}
                    # If the query is too long, Mitsuku answers in several lines.  Here
                    # I'll just put it into paragraphs.
                    response = '\n\n'.join(response_json['responses'])
                    print(response)

                except:
                    client_name = str(random.randint(1337, 9696913371337)).rjust(13, '0')

                    query=str(messages[-1])
                    response_raw = session.post(
                    f'https://miapi.pandorabots.com/talk?'
                    f'botkey={botkey}&'
                    f'input={query}&'
                    f'client_name={client_name}&'
                    f'sessionid=null&'
                    f'channel=6').text
                    try:
                        response_json = json.loads(response_raw)
                    except json.JSONDecodeError:
                        # Sometimes Mitsuku sends stuff like pictures.
                        response_json = {'responses': ["<i can't understand it, bro>"]}
                    # If the query is too long, Mitsuku answers in several lines.  Here
                    # I'll just put it into paragraphs.
                    response = '\n\n'.join(response_json['responses'])
                    print(response)
                if '{"status": "error","message":"401 unauthorized"}' in response:
                    response=response.replace('{"status": "error","message":"401 unauthorized"}','')
                if 'Kuki' in response:
                    response=response.replace('Kuki','AyushBot')
                if bool(response)==False:
                    client_name = str(random.randint(1337, 9696913371337)).rjust(13, '0')

                    query=str(messages[-1])
                    response_raw = session.post(
                    f'https://miapi.pandorabots.com/talk?'
                    f'botkey={botkey}&'
                    f'input={query}&'
                    f'client_name={client_name}&'
                    f'sessionid=null&'
                    f'channel=6').text
                    try:
                        response_json = json.loads(response_raw)
                    except json.JSONDecodeError:
                        # Sometimes Mitsuku sends stuff like pictures.
                        response_json = {'responses': ["<i can't understand it, bro>"]}
                    # If the query is too long, Mitsuku answers in several lines.  Here
                    # I'll just put it into paragraphs.
                    response = '\n\n'.join(response_json['responses'])

                if '{"status": "error","message":"401 unauthorized"}' in response:
                    response=response.replace('{"status": "error","message":"401 unauthorized"}','')
                if 'Kuki' in response:
                    response=response.replace('Kuki','AyushBot')
                if 'Pandorabots' in response:
                    response=response.replace('Pandorabots','Ayush')    
                responses.append(response)

                if len(responses)>1:
                    if responses[-1]!=responses[-2]:
                        whatsapp.send_message(receiver, f'{responses[-1]}')
                elif len(responses)==1:
                    whatsapp.send_message(receiver, f'{responses[-1]}')
                        

                


