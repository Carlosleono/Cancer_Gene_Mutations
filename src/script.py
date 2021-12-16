import pandas as pd
import requests
import re
import nltk
import warnings
import csv

import sys

sys.path.append('/mnt/c/Users/cleon/Documents/CAL_CAL/ironhack/Final_project/Redefining_Cancer_treatment/src')
# import datafunctions as dataf

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

from nltk.corpus import stopwords


def getgenedata2(Gene, Chromosome, Tumour_type, Role, i):
    try:
        driver.implicitly_wait(5)
        # wait2.until(EC.element_to_be_clickable((By.ID, 'DataTables_Table_1_next')))
        driver.find_element_by_id("DataTables_Table_1_next").click()

    except Exception as e:
        return print(f'Error in clicking next at page {i}: {e}')

    for g in range(1, 26):

        try:
            Gene.append(driver.find_element_by_css_selector(
                f'#DataTables_Table_0 > tbody > tr:nth-child({g}) > td.sorting_1 > a').text)
        except:
            return print(f'Error at collecting Gene at page {i}, position {g}')
        try:
            Chromosome.append((driver.find_element_by_css_selector(
                f'#DataTables_Table_0 > tbody > tr:nth-child({g}) > td:nth-child(4)').text).split(':')[0])
        except:
            return print(f'Error at collecting Chromosome at page {i}, position {g}')
        try:
            Tumour_type.append((driver.find_element_by_css_selector(
                f'#DataTables_Table_0 > tbody > tr:nth-child({g}) > td:nth-child(10)').text).split(';')[0])
        except:
            return print(f'Error at Tumour_type at page {i}, position {g}')
        try:
            Role.append((driver.find_element_by_css_selector(
                f'#DataTables_Table_0 > tbody > tr:nth-child({g}) > td:nth-child(15)').text).split(';')[0])
        except:
            return print(f'Error at Role at page {i}, position {g}')

    return print(f'Data collected from page {i}')


def getgenedata(Gene, Chromosome, Tumour_type, Role):
    driver = webdriver.Chrome('./chromedriver.exe')

    # set the url
    url2 = "https://cancer.sanger.ac.uk/census"
    driver.get(url2)
    driver.implicitly_wait(3)

    for g in range(1, 26):
        Gene.append(driver.find_element_by_css_selector(
            f'#DataTables_Table_0 > tbody > tr:nth-child({g}) > td.sorting_1 > a').text)
        Chromosome.append((driver.find_element_by_css_selector(
            f'#DataTables_Table_0 > tbody > tr:nth-child({g}) > td:nth-child(4)').text).split(':')[0])
        Tumour_type.append((driver.find_element_by_css_selector(
            f'#DataTables_Table_0 > tbody > tr:nth-child({g}) > td:nth-child(10)').text).split(';')[0])
        Role.append((driver.find_element_by_css_selector(
            f'#DataTables_Table_0 > tbody > tr:nth-child({g}) > td:nth-child(15)').text).split(';')[0])

    return print('Data collected from page 1')


warnings.filterwarnings("ignore");
nltk.download('stopwords');

Gene = []
Chromosome = []
Tumour_type = []
Role = []

getgenedata(Gene, Chromosome, Tumour_type, Role)


def getgenedata2(Gene, Chromosome, Tumour_type, Role, i):
    driver = webdriver.Chrome('./chromedriver.exe')
    # set the url
    # wait2 = WebDriverWait(driver, 10)
    url2 = "https://cancer.sanger.ac.uk/census"
    driver.get(url2)
    driver.implicitly_wait(3)

    try:
        for pag in range(1, i):
            driver.implicitly_wait(5)

            driver.find_elements("#DataTables_Table_1_next").click()

    except Exception as e:
        return print(f'Error in clicking next at page {i}: {e}')

    for g in range(1, 26):

        try:
            Gene.append(driver.find_element_by_css_selector(
                f'#DataTables_Table_0 > tbody > tr:nth-child({g}) > td.sorting_1 > a').text)
        except:
            return print(f'Error at collecting Gene at page {i}, position {g}')
        try:
            Chromosome.append((driver.find_element_by_css_selector(
                f'#DataTables_Table_0 > tbody > tr:nth-child({g}) > td:nth-child(4)').text).split(':')[0])
        except:
            return print(f'Error at collecting Chromosome at page {i}, position {g}')
        try:
            Tumour_type.append((driver.find_element_by_css_selector(
                f'#DataTables_Table_0 > tbody > tr:nth-child({g}) > td:nth-child(10)').text).split(';')[0])
        except:
            return print(f'Error at Tumour_type at page {i}, position {g}')
        try:
            Role.append((driver.find_element_by_css_selector(
                f'#DataTables_Table_0 > tbody > tr:nth-child({g}) > td:nth-child(15)').text).split(';')[0])
        except:
            return print(f'Error at Role at page {i}, position {g}')

    return print(f'Data collected from page {i}')


driver = webdriver.Chrome('./chromedriver.exe')
# set the url
wait2 = WebDriverWait(driver, 10)
url2 = "https://cancer.sanger.ac.uk/census"
driver.get(url2)
driver.implicitly_wait(3)

cuenta = 2
for i in range(2, 31):
    getgenedata2(Gene, Chromosome, Tumour_type, Role, cuenta)
    cuenta += 1

sanger = pd.DataFrame(list(zip(Gene, Chromosome, Tumour_type, Role)), columns=['Gene', 'Chromosome', 'Tumour_type', 'Role'])
sanger.to_csv('../data/putalocura.csv')
