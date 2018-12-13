# creator: Sun Jiashuo
# Version 1.1.0 
# Release Date: 11-Dec-2018

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time
import pandas as pd
import numpy as np
from bs4 import *
import sys
import csv
import os

#################################### web scrapper for DBS fund risk rating ##################################

def parse_DBS(current_isin,driver):

    driver.get("http://lt.morningstar.com/gvji07hh87/fundquickrank/default.aspx?LanguageId=en-GB")
    time.sleep(2)

    try:
        driver.implicitly_wait(2) # seconds
        search_bar = driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_aFundQuickrankControl_txtSearchKey"]')
        search_bar.clear()
        search_bar.send_keys(current_isin)
        search_btn = driver.find_element_by_id("ctl00_ContentPlaceHolder1_aFundQuickrankControl_btnSearch")
        search_btn.click()
        time.sleep(1)
    except Exception:
        print("Unexpected error:", sys.exc_info()[1])



    funds = pd.DataFrame(columns = ['ISIN','fund_name', 'risk_rating'])
    #picking the fund name and fund risk rating
    try:
        results = driver.find_elements_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_aFundQuickrankControl_gridResult"]/tbody/tr') #count the number of funds in the search result
        n = len(results) + 1
        for i in range(2, n, 1):
            fund_name = driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_aFundQuickrankControl_gridResult"]/tbody/tr[%i]/td[3]/a' %(i)).text
            #print(fund_name)
            risk_rating = driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_aFundQuickrankControl_gridResult"]/tbody/tr[%i]/td[4]' %(i)).text
            #print(risk_rating)
            funds = funds.append({'ISIN': current_isin, 'fund_name':fund_name, 'risk_rating': risk_rating},ignore_index=True)
        print('%s processed' %(current_isin))
    except Exception:
        # print("Unexpected error:", sys.exc_info()[1])
        print('%s not found in DBS fund rating list' %(current_isin))

    # if file does not exist write header 
    if not os.path.isfile('DBS_Fund_Benchmarking.csv'):
       funds.to_csv('DBS_Fund_Benchmarking.csv', header=['ISIN','fund_name', 'risk_rating'],sep=',', index=False)
    else: # else it exists so append without writing the header
       funds.to_csv('DBS_Fund_Benchmarking.csv', mode='a', header=False, sep=',', index=False)
