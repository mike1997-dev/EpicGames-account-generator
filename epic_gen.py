# Title: BattleNet generator
#
# Description: Goes to battle net website an makes accounts
#
# Author: Mr_bond#2732

from unicodedata import name
from playwright.sync_api import sync_playwright
import time
from webbrowser import get
from playwright.sync_api import Page, expect
import time
import string
import json
import requests
import sys
import os
from time import sleep
from datetime import datetime
import random
from termcolor import *
import json
from bs4 import BeautifulSoup
import re
import string



def create_account():
    
    token = sys.argv[1]
    custom_username = sys.argv[2]
    country = sys.argv[3]

    def random_char(char_num):
        return "".join(random.choice(string.ascii_letters) for _ in range(char_num))

    def random_num(charnum1):
        return "".join(random.choice(string.digits) for _ in range(charnum1))

    first_name = ["Nathania","Narin","Nan","Nahshon","Nafeesah","Nadira","Nadina","Mystie","Myrtle","Mylinh","Musa","Morganne","Montia","Moncia","Demaris","Delynn","Delmer","Deisi","Deanndra","Deacon","Daylan","Azariah","Aynsley","Avia","Avanti","Aurielle"]

    last_name = ["MENDEZ","BUSH","VAUGHN","PARKS","DAWSON","SANTIAGO","NORRIS","LOVE","STEELE","CURRY","POWERS","SCHULTZ","BARKER","GUZMAN","PAGE","MUNOZ","BALL","GIBBS","TYLER","GROSS","FITZGERALD","STOKES","DOYLE","SHERMAN","SAUNDERS","WISE","COLON","GILL","ALVARADO","GREER","PADILLA", "SIMON","WATERS","NUNEZ","BOONE","CORTEZ",]
    random1 = ["01", "02", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
    random1 = random.choice(random1)
    random2 = random.randint(10, 29)
    random3 = random.randint(1970, 2002)
    first_name1 = random.choice(first_name).lower()
    last_name1 = random.choice(last_name).lower()
    password = random_char(7) + random_num(6)
    
    
    playwright = sync_playwright().start()
    browser = playwright.firefox.launch(headless=False)
    context = browser.new_context(
        viewport={"width": 500, "height": 400},
        device_scale_factor=2,
    )
    page = context.new_page()

    page.set_default_timeout(9000000)

    time.sleep(1)
    # start of account creation
    page.goto("https://www.epicgames.com/id/register/epic")
    time.sleep(1)

    page.locator('//*[@id="month"]').dblclick()
    time.sleep(1)
    page.locator('//*[@id="day"]').dblclick()
    time.sleep(2)
    page.locator('//*[@id="year"]').type(str(random3),delay=100)
    time.sleep(2)
    page.locator('//*[@id="continue"]').click()
    time.sleep(1)
    page.locator('//*[@id="country"]').fill(country)
    
    #Making API request for email and prints out email and id number
    response = requests.get(
        "http://api.kopeechka.store/mailbox-get-email?site=https://www.epicgames.com/id/register/epic&mail_type=OUTLOOK&token="+ str(token) +"&soft=$SOFT_ID&type=JSON&api=2.0")
    data = json.loads(response.text)
    email = data['mail']  # Email
    code = data['id']  # ID number

    page.locator('//*[@id="name"]').type(first_name1,delay=100)
    time.sleep(1)
    page.locator('//*[@id="lastName"]').type(last_name1)
    time.sleep(2)
    custom_username1 = custom_username + random_num(5)
    page.locator('//*[@id="displayName"]').type(custom_username1,delay=100)
    time.sleep(1)
    time.sleep(1)
    page.locator('//*[@id="email"]').type(email)
    time.sleep(1)
    time.sleep(2)
    page.locator('//*[@id="password"]').type(password,delay=100)
    time.sleep(1)
    time.sleep(1)
    page.locator('//*[@id="tos"]').click()
    time.sleep(1)
    page.click('//*[@id="btn-submit"]')
    time.sleep(5)

    while True:
        response1 = requests.get(
            f"http://api.kopeechka.store/mailbox-get-message?full=$FULL&id={str(code)}&token=8ec3318fdfa3d6f2a3d185a3c516ff0d&type=JSON&api=2.0")

        data1 = json.loads(response1.text)
        
        if data1['status'] == 'OK':
            global code1
            soup = BeautifulSoup(data1['fullmessage'], 'html.parser')

            verification_code_msg_tbl = soup.find(text=re.compile('Email Verification Code:')).parent.parent.parent.parent

            verification_code = verification_code_msg_tbl.find_all('tr')[1].find('td').text.strip().rstrip()
            code1 = str(verification_code)

            break
        elif data1['status'] == 'WAIT_LINK':
            time.sleep(5)

    page.locator('//*[@id="modal-content"]/div[2]/div/div[1]/div/form/div[1]/div/div[1]/div/input').type(code1)
    time.sleep(1)
    page.locator('//*[@id="continue"]').click()
    time.sleep(2)    
    time.sleep(1)

    time.sleep(2)

    data_list = [email, password, custom_username1]
    with open("EpicAccounts.txt", "a") as f:
        json.dump(data_list, f, indent=4)
        f.write("\n")
        f.close
    time.sleep(2)
    browser.close()

create_account()

# Took out threading, you can add yourself. So just called function above like that.