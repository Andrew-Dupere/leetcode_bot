from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import dep.arcturis as arc
import gpt as kadabra

from openai import OpenAI

client = OpenAI()

language = 'C++'

options = webdriver.FirefoxOptions()
driver = webdriver.Firefox(options=options)
url = "https://leetcode.com/accounts/login/"



def wait_and_find_element(driver, by, value):
    return WebDriverWait(driver, 10).until(EC.presence_of_element_located((by, value)))

def login_and_select(driver):
    driver.get(url)

    login_field = wait_and_find_element(driver, By.ID, "id_login")
    login_field.send_keys(arc.e)

    password_field = wait_and_find_element(driver, By.ID, "id_password")
    password_field.send_keys(arc.p)

    EC.element_to_be_clickable((By.XPATH, "//div[@class='btn-content-container__2HVS']/span[text()='Sign In']"))
    WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.ID, "initial-loading")))

    # Find the "Sign In" button
    sign_in_button = wait_and_find_element(driver,By.XPATH, "//div[@class='btn-content-container__2HVS']/span[text()='Sign In']")

    driver.execute_script("arguments[0].scrollIntoView(true);", sign_in_button)

    time.sleep(2)
    sign_in_button.click()
    time.sleep(2)


    problems = wait_and_find_element(driver, By.XPATH,"//a[@href='/problemset/all/']")
    problems.click()

    pickone = wait_and_find_element(driver, By.XPATH,"//div[contains(@class, 'ml-auto')]")
    # Click the button  
    pickone.click()

def click_next_button(driver):
    #find all of the elements in the navbar with "cursor-pointer" and click the 3rd one (next problem)
    navbar = wait_and_find_element(driver, By.CLASS_NAME,"z-nav-1")
    buttons = navbar.find_elements(By.CLASS_NAME,"cursor-pointer")
    buttons[2].click()  

def handle_subscribe_popup(driver):
    while True:
        try:
            # Check for the subscribe popup
            subscribe_popup = WebDriverWait(driver, 4).until(                
                EC.visibility_of_element_located((By.XPATH, "//div[contains(text(), 'Subscribe to unlock.')]"))
            )

            click_next_button(driver)
                

        except:
            # If the subscribe popup is not found, break out of the loop
            break

def solution_ai(driver):
    #extract the text in the problem, send it into the gpt prompt, clear the field, input sol 

    description_element = wait_and_find_element(driver,By.CLASS_NAME,'elfjS')
    description_text = description_element.text

    code_block_element = wait_and_find_element(driver,By.CSS_SELECTOR,'.view-lines')
   
    code_block_text = code_block_element.text

    line_elements = code_block_element.find_elements(By.CLASS_NAME, 'view-line')

    sol = kadabra.main(f"I would like you to solve a problem in {language}, please only return code, do not inlcude any additional text and do not add comments within the code. Here is the description of the problem: {description_text} and use this format to provide the solution {code_block_text}")

    container = wait_and_find_element(driver, By.CLASS_NAME, "view-lines.monaco-mouse-cursor-text")
    #clear cells
    driver.execute_script("arguments[0].innerText = '';", container)
    time.sleep(1)
    block_of_text = sol
    #use javascript to import solutions
    driver.execute_script("arguments[0].innerText = arguments[1];", container, block_of_text)
    time.sleep(1)

def click_submit(driver):
    #click submit 
    submit = wait_and_find_element(driver,By.CSS_SELECTOR, "button[data-e2e-locator='console-submit-button']")
    submit.click()
    time.sleep(1)

login_and_select(driver)
for num in range(10):
    handle_subscribe_popup(driver)
    solution_ai(driver)
    click_submit(driver)
    click_next_button(driver)

