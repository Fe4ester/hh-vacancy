import requests
import bs4
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pprint import pprint


def remove_duplicates(dicts):
    seen = set()
    unique_dicts = []

    for d in dicts:
        dict_tuple = tuple(sorted(d.items()))
        if dict_tuple not in seen:
            seen.add(dict_tuple)
            unique_dicts.append(d)

    return unique_dicts


path = Service(ChromeDriverManager().install())

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')

browser = webdriver.Chrome(service=path, options=options)
browser.get('https://spb.hh.ru/search/vacancy?text=python&area=1&area=2')

html = browser.page_source

total_vacancy = []

soup = bs4.BeautifulSoup(html, features='lxml')
main_tag = soup.find('main', class_='vacancy-serp-content')
main_tags = main_tag.find_all('div')

for div in main_tags:
    salary_tag = div.find('span',
                          class_='fake-magritte-primary-text--Hdw8FvkOzzOcoR4xXWni compensation-text--kTJ0_rp54B2vNeZ3CTt2 separate-line-on-xs--mtby5gO4J0ixtqzW38wh')

    description_tag = div.find('span', class_='vacancy-name--c1Lay3KouCl7XasYakLk serp-item__title-link')
    link_tag = div.find('a', class_='bloko-link')

    if salary_tag:
        hard_text = salary_tag.text
        salary_text = hard_text.replace('\u202f', ' ').replace('\xa0', ' ')
    else:
        salary_text = None

    if description_tag:
        description_text = description_tag.text
    else:
        description_text = None

    if link_tag:
        link_text = link_tag.get('href')
    else:
        link_text = None

    if description_text is not None:
        total_vacancy.append({
            'description': description_text,
            'salary': salary_text,
            'link': link_text
        })

browser.quit()

total_vacancy = remove_duplicates(total_vacancy)


