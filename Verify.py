import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from collections import namedtuple
from threading import Thread
import pandas as pd
keys = namedtuple('Keys', ['id', 'Password'])
key_1 = keys('FTA11042', 'Kunjal@2019')
key_2 = keys('FTA10003', 'nir@123')
reg_array = []
verify = []
data = pd.DataFrame()


def convert_list_to_np_array_to_dataframe():
    file_name = '/Users/DataScienceTreasures/Desktop/verify.xlsx'
    if len(reg_array) != 0:
        data['reg_number'] = pd.DataFrame(reg_array)
        data['Status'] = pd.DataFrame(verify)
        data.to_excel(file_name)

def clean_array():
    reg_array.clear()
    verify.clear()


def FM(id, password):
    path = "/Users/DataScienceTreasures/Downloads/chromedriver"
    option = webdriver.ChromeOptions()
    first_driver = webdriver.Chrome(executable_path=path)
    first_driver.get("https://www.hsrp.in/dealer_ewallet-login.php")
    first_driver.maximize_window()

    def enter_id_password(idx, passwordx):
        enter_username = first_driver.find_element(By.XPATH, '//*[@id="email"]')
        enter_username.click()
        enter_username.send_keys(idx)
        enter_password = first_driver.find_element(By.XPATH, '//*[@id="password"]')
        enter_password.click()
        enter_password.send_keys(passwordx)
        first_driver.find_element(By.XPATH, '//*[@id="cbody"]/div/div/div[2]/div[2]/div[1]/form/div[5]/input').click()

    def close():
        first_driver.quit()

    def close_first_popup():
        click_cross = first_driver.find_element(By.XPATH, '//*[@id="myModalMsg"]/div/div/div[1]/button')
        time.sleep(1)
        click_cross.click()

    def click_form():
        first_driver.find_element(By.XPATH, '//*[@id="sidebar"]/ul/li[2]/a/b').click()
        time.sleep(1)
        if first_driver.find_element(By.XPATH, '/html/body/div[3]/div[1]/ul/li[2]/ul/li[4]/a').text == \
                'Maruti Vahan Verification':
            first_driver.find_element(By.XPATH, '/html/body/div[3]/div[1]/ul/li[2]/ul/li[4]/a').click()
        else:
            first_driver.find_element(By.XPATH, '//*[@id="sidebar"]/ul/li[2]/ul/li[3]/a').click()
        time.sleep(2)
        first_driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div/div[2]/div[3]/div/div[1]/div[2]/div/form/div['
                                            '2]/div/div/a').click()

    enter_id_password(id, password)
    find_cross = WebDriverWait(first_driver, 300).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="myModalMsg"]/div/div/div[1]/button'))
    )
    if find_cross:
        close_first_popup()
        click_form()
        time.sleep(2)
        count = 1
        try:
            while first_driver.find_element(By.CLASS_NAME, f'row_{count}'):
                path = f'//*[@id="dynamic-table"]/tbody/tr[{count}]/td[2]'
                reg_number = first_driver.find_element(By.XPATH, path).text
                try:
                    verify_button = first_driver.find_element(By.XPATH, f'//*[@id="{reg_number}"]')
                    verify_button.click()
                    reg_array.append(reg_number)
                    verify.append('Verified')
                    time.sleep(6)  # you can change it
                except:
                    reg_array.append(reg_number)
                    verify.append('Not Verified')
                    pass
                count += 1
        except:
            print('Done_1')


if __name__ == '__main__':
    reg_array.append(f'{key_1.id}')
    verify.append(f'{key_1.id}')
    Thread(target=FM(key_1.id, key_1.Password)).start()
    Thread(target=FM(key_2.id, key_2.Password)).start()
    reg_array.append(f'{key_2.id}')
    verify.append(f'{key_2.id}')
    convert_list_to_np_array_to_dataframe()
