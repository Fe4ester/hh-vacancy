import requests
import bs4
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait


def wait_element(browser, delay_seconds=1, by=By.CLASS_NAME, value=None):
    return WebDriverWait(browser, delay_seconds).until(
        expected_conditions.presence_of_element_located((by, value))
    )


path = Service(ChromeDriverManager().install())

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')

browser = webdriver.Chrome(service=path, options=options)
browser.get('https://spb.hh.ru/search/vacancy?text=python&area=1&area=2')

html = browser.page_source

salary = []
sorted_salary = []

soup = bs4.BeautifulSoup(html, features='lxml')
main_tag = soup.find('main', class_='vacancy-serp-content')
main_tags = main_tag.find_all('div')

for div in main_tags:
    next_tag = div.find('span',
                        class_='fake-magritte-primary-text--Hdw8FvkOzzOcoR4xXWni compensation-text--kTJ0_rp54B2vNeZ3CTt2 separate-line-on-xs--mtby5gO4J0ixtqzW38wh')

    if next_tag:
        hard_text = next_tag.text
        compensation_text = hard_text.replace('\u202f', ' ').replace('\xa0', ' ')
    else:
        compensation_text = None

    salary.append(compensation_text)

browser.quit()

for i in salary:
    if i is not None:
        if '$' in i:
            sorted_salary.append(i)
            print(i)

print(sorted_salary)
print(len(salary))
print(len(sorted_salary))
