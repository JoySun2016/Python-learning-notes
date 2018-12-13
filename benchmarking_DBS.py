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

from parse_DBS import parse_DBS

def main():
	#### read in the ISIN list ####
	with open('ISIN_LIST.csv', 'r') as f:
	  reader = csv.reader(f)
	  ISIN_list = list(reader)

	#### selenium driver setting ####
	chrome_options = Options()
	chrome_options.add_argument("--headless")       # define headless, Chrome will not be poped up then

	driver = webdriver.Chrome('V:/Joy/benchmarking/fund_benchmarking/Chrome_Driver/chromedriver.exe',chrome_options=chrome_options)

	#### run the parse_DBS function and produce the result ####
	for x in ISIN_list:
		current_isin = x[0]
		parse_DBS(current_isin, driver)
		

start_time = time.time()
main()
print("--- %s seconds ---" % (time.time() - start_time))




