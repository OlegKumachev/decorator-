import requests
from fake_headers import Headers
from bs4 import BeautifulSoup
import re
import json
from logger import logger_path, logger


def get_headers():
    return Headers(browser='Chrome', os='win').generate()


@logger
def get_tag():
    html_data = requests.get('https://spb.hh.ru/search/vacancy?text=python&area=1&area=2', headers=get_headers()).text
    soup = BeautifulSoup(html_data, 'lxml')
    tag_all_vac = soup.find_all(class_="vacancy-serp-item__layout")
    return tag_all_vac


@logger_path('log.txt')
def job_search(tag_all):
    vacancies_data = []
    for tag in tag_all:
        salary = tag.find('span', {'data-qa': "vacancy-serp__vacancy-compensation"})
        if salary == None:
            continue
        city = tag.find('div', {'data-qa': 'vacancy-serp__vacancy-address'}).text
        link = tag.find('a', class_='serp-item__title')['href']
        company = tag.find('a', class_="bloko-link bloko-link_kind-tertiary")
        vac_text = BeautifulSoup(requests.get(link, headers=get_headers()).text, 'lxml')
        text = vac_text.find('div', class_="g-user-content").text
        worlds = re.search(f"Django|Flask", text)
        if worlds != None:
            vacancies_data.append(
                {
                    'link': link,
                    'salary': salary.text.replace(u'\u202F', ' '),
                    'company': company.text.replace(u'\xa0', ' '),
                    'city': city
                }
            )

    return vacancies_data


if __name__ == '__main__':
    data_vac = job_search(get_tag())
    with open('data.json', 'w', encoding='utf-8') as data_file:
        json.dump(data_vac, data_file, ensure_ascii=False, indent=2)
