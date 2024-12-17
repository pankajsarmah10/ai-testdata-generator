#Calling ollama API to generate response
#endpoint: /api/generate
import time

import requests
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
def generate_test_data(prompt):
    response = requests.post("http://localhost:11434/api/generate",
                             json={"model": "llama3:latest", "prompt": prompt, "stream": False})
    result = response.json()
    return result["response"]

prompt = """Generate sample user registration data in json with the following dataset: Firstname: [value], Lastname: [value], Address: [value], City: [value],State: [value], Zipcode: [value], Phone: [value], SSN: [value], Username: [value], Password: [value].
Do not include any additional text or explanations."""

test_data = generate_test_data(prompt)

json_data = json.loads(test_data)
print(json_data)

driver = webdriver.Chrome()
driver.get("https://parabank.parasoft.com/parabank/register.htm")
time.sleep(5)

assert driver.title == "ParaBank | Register for Free Online Account Access", f"Registration page is not open"

for item in json_data:
    driver.get("https://parabank.parasoft.com/parabank/register.htm")
    driver.find_element(By.CSS_SELECTOR, '[id="customer.firstName"]').send_keys(item["Firstname"])
    driver.find_element(By.CSS_SELECTOR, '[id="customer.lastName"]').send_keys(item["Lastname"])
    driver.find_element(By.CSS_SELECTOR, '[id="customer.address.street"]').send_keys(item["Address"])
    driver.find_element(By.CSS_SELECTOR, '[id="customer.address.city"]').send_keys(item["City"])
    driver.find_element(By.CSS_SELECTOR, '[id="customer.address.state"]').send_keys(item["State"])
    driver.find_element(By.CSS_SELECTOR, '[id="customer.address.zipCode"]').send_keys(item["Zipcode"])
    driver.find_element(By.CSS_SELECTOR, '[id="customer.phoneNumber"]').send_keys(item["Phone"])
    driver.find_element(By.CSS_SELECTOR, '[id="customer.ssn"]').send_keys(item["SSN"])
    driver.find_element(By.CSS_SELECTOR, '[id="customer.username"]').send_keys(item["Username"])
    driver.find_element(By.CSS_SELECTOR, '[id="customer.password"]').send_keys(item["Password"])
    driver.find_element(By.CSS_SELECTOR, '[id="repeatedPassword"]').send_keys(item["Password"])
    driver.find_element(By.CSS_SELECTOR, 'input[value=Register]').click()
    time.sleep(5)
    assert driver.title == "ParaBank | Customer Created", f"Registration Failed"

    driver.find_element(By.CSS_SELECTOR, 'a[href*=logout]').click()
    time.sleep(5)
    assert driver.title == "ParaBank | Welcome | Online Banking", f"Logout failed"

    driver.find_element(By.CSS_SELECTOR, 'input[name=username]').send_keys(item["Username"])
    driver.find_element(By.CSS_SELECTOR, 'input[name=password]').send_keys(item["Password"])
    driver.find_element(By.CSS_SELECTOR, 'input[value="Log In"]').click()
    time.sleep(5)
    assert driver.title == "ParaBank | Accounts Overview", f"Login failed"

driver.quit()