import bs4
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pprint import pprint
import time
import re


def remove_duplicates(dicts):
    seen = set()
    unique_dicts = []

    for d in dicts:
        dict_tuple = tuple(sorted(d.items()))
        if dict_tuple not in seen:
            seen.add(dict_tuple)
            unique_dicts.append(d)

    return unique_dicts


def fetch_vacancy_text(browser, link):
    browser.get(link)
    html = browser.page_source
    soup = bs4.BeautifulSoup(html, features='lxml')
    text_tag = soup.find('div', class_='g-user-content')

    if text_tag:
        return ' '.join(span.text for span in text_tag.find_all('span'))
    return ''


def contains_frameworks(text):
    pattern = r'django|flask|джанго|фласк'

    match = re.search(pattern, text, re.IGNORECASE)

    return bool(match)


def get_links(url, browser):
    browser.get(url)

    html = browser.page_source

    soup = bs4.BeautifulSoup(html, features='lxml')
    main_tag = soup.find('main', class_='vacancy-serp-content')
    main_tags = main_tag.find_all('div')
    total_vacancy = []

    for div in main_tags:

        name_tag = div.find('span', class_='vacancy-name--c1Lay3KouCl7XasYakLk serp-item__title-link')

        salary_tag = div.select_one(
            'span.fake-magritte-primary-text--Hdw8FvkOzzOcoR4xXWni.compensation-text--kTJ0_rp54B2vNeZ3CTt2')

        link_tag = div.find('a', class_='bloko-link')

        company_tag = div.find('span', class_='company-info-text--vgvZouLtf8jwBmaD1xgp')

        city_tag = div.select_one(
            'span.fake-magritte-primary-text--Hdw8FvkOzzOcoR4xXWni:not(.compensation-text--kTJ0_rp54B2vNeZ3CTt2)')

        if name_tag:
            name_text = name_tag.text
        else:
            name_text = None

        if salary_tag:
            salary_hard_text = salary_tag.text
            salary_text = salary_hard_text.replace('\u202f', ' ').replace('\xa0', ' ')
        else:
            salary_text = None

        if link_tag:
            link_text = link_tag.get('href')
        else:
            link_text = None

        if company_tag:
            company_hard_name = company_tag.text
            company_name = company_hard_name.replace('\u202f', ' ').replace('\xa0', ' ')
        else:
            company_name = None

        if city_tag:
            city_name = city_tag.text
        else:
            city_name = None

        if name_text is not None:
            total_vacancy.append({
                'link': link_text,
                'salary': salary_text,
                'company_name': company_name,
                'city_name': city_name
            })

    total_vacancy = remove_duplicates(total_vacancy)

    return total_vacancy


def get_vacancies(total_vacancy, browser, count=52):
    vacancies = []

    for item in range(count):
        link = total_vacancy[item]['link']
        text = ''
        browser.get(link)
        html = browser.page_source
        soup = bs4.BeautifulSoup(html, features='lxml')
        text_tag = soup.find('div', class_='g-user-content')
        if text_tag is not None:
            text_tags = text_tag.find_all('span')

            for j in text_tags:
                text += j.text

            if contains_frameworks(text):
                vacancies.append(total_vacancy[item])

        print('finish')

    return vacancies


start_time = time.time()

path = Service(ChromeDriverManager().install())

url = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')

browser = webdriver.Chrome(service=path, options=options)

total_vacancy = get_links(url, browser)

pprint(total_vacancy)
print(len(total_vacancy))

# vacancies = get_vacancies(total_vacancy, browser)
#
# pprint(vacancies)

browser.quit()

print("--- %s seconds ---" % (time.time() - start_time))
