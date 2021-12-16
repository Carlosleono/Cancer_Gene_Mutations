import re
import nltk
from nltk.corpus import stopwords
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions

nltk.download('stopwords');

stop_words = set(stopwords.words('english'))

def remove_stopwords(total_text, index, dataframe):
    if type(total_text) is not int:
        string = ""
        # Replace every special char with space
        total_text = re.sub('[^a-zA-Z0-9\n]', ' ', total_text)
        # Replace multiple spaces with single space
        total_text = re.sub('\s+',' ', total_text)
        # Converting all the chars into lower-case
        total_text = total_text.lower()
        
        for word in total_text.split():
        # If the word is not a stop word then retain that word from the data
            if not word in stop_words:
                string += word + " "
        
        dataframe['TEXT'][index] = string

def typeeffect(df):
    """
    This functions creates a column that indicates the type of mutation based in tha variation description. It also creates a column indicating the effect of the mutation
    """
    df['Type'] = 'unknown'
    df['Effect'] = 'unknown'
    for i,r in df.iterrows():
        if re.match('.*Fusion.*',r['Variation']):
            df['Effect'][i] = 'fusion'
            df['Type'][i] = 'Deletion'
            
        elif re.match('.*\*.*',r['Variation']):
            df['Type'][i] = 'Substitution'
            df['Effect'][i] = 'nonsense'
            
        elif re.match('.*\?.*',r['Variation']):
            df['Type'][i] = 'Substitution'
            
        elif re.match('.*Truncating.*',r['Variation']):
            df['Effect'][i] = 'nonsense'
        
        elif re.match('.*missense.*',r['Variation']):
            df['Effect'][i] = 'missense'
            
        elif re.match('.*ins.*|.*Ins.*',r['Variation']):
            df['Type'][i] = 'Insertion'
            
        elif re.match('.*del.*|.*Del.*',r['Variation']):
            df['Type'][i] = 'Deletion'
        
        elif re.match('[A-Z]\d*[A-Z]',r['Variation']):
            df['Type'][i] = 'Substitution'
            df['Effect'][i] = 'missense'
    return df

stop_words = set(stopwords.words('english'))

# def nlp_preprocessing(total_text, index, column):
#     if type(total_text) is not int:
#         string = ""
#         # Replace every special char with space
#         total_text = re.sub('[^a-zA-Z0-9\n]', ' ', total_text)
#         # Replace multiple spaces with single space
#         total_text = re.sub('\s+',' ', total_text)
#         # Converting all the chars into lower-case
#         total_text = total_text.lower()
def getgenedata(Gene, Chromosome, Tumour_type, Role):
    driver = webdriver.Chrome('./chromedriver.exe')

    # set the url
    url2 = "https://cancer.sanger.ac.uk/census"
    driver.get(url2)
    driver.implicitly_wait(3)

    for g in range(1, 26):
        Gene.append(driver.find_element_by_css_selector(f'#DataTables_Table_0 > tbody > tr:nth-child({g}) > td.sorting_1 > a').text)
        Chromosome.append((driver.find_element_by_css_selector(f'#DataTables_Table_0 > tbody > tr:nth-child({g}) > td:nth-child(4)').text).split(':')[0])
        Tumour_type.append((driver.find_element_by_css_selector(f'#DataTables_Table_0 > tbody > tr:nth-child({g}) > td:nth-child(10)').text).split(';')[0])
        Role.append((driver.find_element_by_css_selector(f'#DataTables_Table_0 > tbody > tr:nth-child({g}) > td:nth-child(15)').text).split(';')[0])

    return print('Data collected from page 1')



def getgenedata2(Gene, Chromosome, Tumour_type, Role,i):
    driver = webdriver.Chrome('./chromedriver.exe')
    # set the url
    #wait2 = WebDriverWait(driver, 10)
    url2 = "https://cancer.sanger.ac.uk/census"
    driver.get(url2)
    driver.implicitly_wait(3)

    try:
        for pag in range(1, i):
            driver.implicitly_wait(5)

            driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/section[2]/div/div/div/div[5]/a[3]").click()

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

def prueba(Gene, Chromosome, Tumour_type, Role,i):
    driver = webdriver.Chrome('./chromedriver.exe')
    # set the url
    url2 = "https://cancer.sanger.ac.uk/census"
    driver.get(url2)
    driver.implicitly_wait(3)

    inputElement = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/section[2]/div/div/div/div[1]/label/select')
    inputElement.send_keys(100)
    inputElement.send_keys(Keys.ENTER)
    inputElement.send_keys(Keys.ESCAPE)
    driver.implicitly_wait(1000)


    for g in range(1, 101):

        try:
            Gene.append(driver.find_element_by_css_selector(
                f'#DataTables_Table_0 > tbody > tr:nth-child({g}) > td.sorting_1 > a').text)
        except:
            return print(f'Error at collecting Gene at page 1, position {g}')
        try:
            Chromosome.append((driver.find_element_by_css_selector(
                f'#DataTables_Table_0 > tbody > tr:nth-child({g}) > td:nth-child(4)').text).split(':')[0])
        except:
            return print(f'Error at collecting Chromosome at page 1, position {g}')
        try:
            Tumour_type.append((driver.find_element_by_css_selector(
                f'#DataTables_Table_0 > tbody > tr:nth-child({g}) > td:nth-child(10)').text).split(';')[0])
        except:
            return print(f'Error at Tumour_type at page 1, position {g}')
        try:
            Role.append((driver.find_element_by_css_selector(
                f'#DataTables_Table_0 > tbody > tr:nth-child({g}) > td:nth-child(15)').text).split(';')[0])
        except:
            return print(f'Error at Role at page 1, position {g}')

    print('Data collected from page 1')
    for a in range(1,6):
        driver.implicitly_wait(100)
        #driver.find_element_by_css_selector('#DataTables_Table_1_next').click()
        driver.find_elements_by_css_selector(f'#DataTables_Table_1_next').click()
        # DataTables_Table_1_next
        # DataTables_Table_0_next
        #inputElement2.send_keys('\n')
        #nextelement.send_keys(Keys.ENTER)
        driver.implicitly_wait(100)


        for g in range(1, 101):

            try:
                Gene.append(driver.find_element_by_css_selector(
                    f'#DataTables_Table_0 > tbody > tr:nth-child({g}) > td.sorting_1 > a').text)
            except:
                return print(f'Error at collecting Gene at page {a+1}, position {g}')
            try:
                Chromosome.append((driver.find_element_by_css_selector(
                    f'#DataTables_Table_0 > tbody > tr:nth-child({g}) > td:nth-child(4)').text).split(':')[0])
            except:
                return print(f'Error at collecting Chromosome at page {a+1}, position {g}')
            try:
                Tumour_type.append((driver.find_element_by_css_selector(
                    f'#DataTables_Table_0 > tbody > tr:nth-child({g}) > td:nth-child(10)').text).split(';')[0])
            except:
                return print(f'Error at Tumour_type at page {a+1}, position {g}')
            try:
                Role.append((driver.find_element_by_css_selector(
                    f'#DataTables_Table_0 > tbody > tr:nth-child({g}) > td:nth-child(15)').text).split(';')[0])
            except:
                return print(f'Error at Role at page {a+1}, position {g}')

        print(f'Data collected from page {a}')
    return print(f'Data collected from all pages')
