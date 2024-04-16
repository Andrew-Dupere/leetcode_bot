from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import dep.arcturis as arc
from openai import OpenAI
import os


client = OpenAI()

language = 'C++'

options = webdriver.FirefoxOptions()
driver = webdriver.Firefox(options=options)
url = "https://leetcode.com/accounts/login/"

solution = ''


def wait_and_find_element(driver, by, value):
    return WebDriverWait(driver, 10).until(EC.presence_of_element_located((by, value)))

def login(driver):
    driver.get(url)

    login_field = wait_and_find_element(driver, By.ID, "id_login")
    login_field.send_keys(arc.e)

    password_field = wait_and_find_element(driver, By.ID, "id_password")
    password_field.send_keys(arc.p)

    EC.element_to_be_clickable((By.XPATH, "//div[@class='btn-content-container__2HVS']/span[text()='Sign In']"))
    WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.ID, "initial-loading")))

    
    sign_in_button = wait_and_find_element(driver,By.XPATH, "//div[@class='btn-content-container__2HVS']/span[text()='Sign In']")

    driver.execute_script("arguments[0].scrollIntoView(true);", sign_in_button)

    time.sleep(2)
    sign_in_button.click()
    time.sleep(2)

def select_problem(driver):

    problems = wait_and_find_element(driver, By.XPATH,"//a[@href='/problemset/all/']")
    problems.click()

    pickone = wait_and_find_element(driver, By.XPATH,"//div[contains(@class, 'ml-auto')]")
    
    pickone.click()

def click_next_button(driver):
    
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
            break

def gpt_prompt(prompt):
    completion = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )
    return(completion.choices[0].message.content)

def input_solution():
    global solution

    pass

def click_submit(driver):    
    submit = wait_and_find_element(driver,By.CSS_SELECTOR, "button[data-e2e-locator='console-submit-button']")
    submit.click()
    time.sleep(1)




