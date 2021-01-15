#!/usr/bin/env python
# coding: utf-8

# In[269]:


import requests
from lxml import etree
import json
from selenium import webdriver
import pandas as pd
import numpy as np
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from random import randrange

import time
from datetime import datetime
import os, sys
import warnings
warnings.filterwarnings("ignore", message="use options instead of chrome_options")


# In[270]:


# https://medium.com/analytics-vidhya/effortlessly-automate-your-python-scripts-cd295697dff6
# where to save the pdf file
_DATA_TABLEAU_PATH_ = "/Users/xingruchen/Dropbox/COV/Vaccine/US-COVID-19-Vaccine/data/tableau/pdf"
_LOG_PATH_ = "/Users/xingruchen/Dropbox/COV/Vaccine/US-COVID-19-Vaccine/data/tableau/"


# In[272]:


# This dashboard is no longer updated as of December 31, 2020. Thank you to those who supported the project. 
# Please see the CDC for the latest data.
def spider():
    # specify download directory
    options = webdriver.ChromeOptions()
    prefs = {"download.default_directory" : _DATA_TABLEAU_PATH_}
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(executable_path = r'/usr/local/bin/chromedriver', chrome_options = options)
    driver.implicitly_wait(30)
    driver.get('https://public.tableau.com/profile/benjamin.renton#!/vizhome/COVID-19VaccineAllocationDashboard/Dashboard1')

    # jump to the iframe
    iframe = driver.find_element_by_xpath("//iframe[@title='Data Visualization']")
    driver.switch_to.frame(iframe)
    def download(name):
        # click to select the download icon
        # '//a[@class="expandable-trigger-more"]'
        button = driver.find_element_by_xpath('//*[@class="tabToolbarButton tab-widget download"]')
        button.click()
        # choose to download pdf file
        button = driver.find_element_by_xpath('//*[@data-tb-test-id="DownloadPdf-Button"]')
        button.click()
        # open dropdown menu
        # /span[@class="f1r23t9y"][text()="Specific sheets from this dashboard"]
        select = driver.find_element_by_xpath('//*[@aria-label="This View, Include"]');
        select.click()
        # choose Specific sheets from this dashboard, Include
        select = driver.find_element_by_xpath('//span[@class="frvoegc"][text()="Specific sheets from this workbook"]');
        select.click()
        # choose Allocation Table
        select = driver.find_element_by_xpath('//*[@title=' + '"' + name + '"' + ']');
        select.click()
        # download pdf file
        button = driver.find_element_by_xpath('//*[@data-tb-test-id="PdfDialogCreatePdf-Button"]')
        button.click()
        time.sleep(30)
    ########################################
    download(name = 'Allocation Table')
    download(name = 'Summary')
    
    
    def download_completed():
        for i in os.listdir(_DATA_TABLEAU_PATH_):
            if ".crdownload" in i:
                time.sleep(1)
    download_completed()
    driver.switch_to.default_content();
    driver.quit();


# In[273]:


try:
    spider()
except Exception as ex:
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    logf = open(_LOG_PATH_ + "error.log", "a")
    logf.write("On {0}: {1}\n".format(str(dt_string), str(ex)))
    logf.close()

