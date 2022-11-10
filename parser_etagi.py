from bs4 import BeautifulSoup as BS
import requests as req
import datetime
import csv
import os

URL = 'https://tver.etagi.com/realty/'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.141 YaBrowser/22.3.3.852 Yowser/2.5 Safari/537.36', 'accept': '*/*'}
FILE = 'realty.csv'

def get_html(url, params=None):
    page = req.get(url, headers=HEADERS, params=params)
    return page


def get_pages_count(html):
    soup = BS(html, 'lxml')
    pagination = soup.find_all('button', class_='x0SgG Q7VHf') + soup.find_all('button', class_='x0SgG JThfy Q7VHf')
    if pagination:
        return int(pagination[-1].get_text())
    else:
        return 1
    #print(pagination)

def get_content(html):
    soup = BS(html, 'lxml')
    items = soup.find_all('div', class_='y8VEv templates-object-card etagiSlider__parent')
    print(items)
    #print(items)
    realty = []
    for item in items:
        realty.append({'adress': item.find('div', class_='EDAsp').get_text(strip=True).replace('\n   ', ','),
                       'price': item.find('span', class_='eypL8 uwvkD').get_text(strip=True).replace('руб.', ''),
                       'rooms': item.find('div', class_='templates-object-card__params').find_next('span').get_text(),
                        'square': item.find('div', class_='templates-object-card__params').find_next('span').find_next('span').get_text()

                       })
    return realty



def save_file(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Адрес', 'Цена', 'Объект', 'Площадь'])
        for item in items:
            writer.writerow([item['adress'], item['price'], item['rooms'], item['square']])


def parcing():
    URL = input('Введите ссылку: ').strip()
    page_html = get_html(URL)
    if page_html.status_code == 200:
        realty = []
        pages_count = get_pages_count(page_html.text)
        for page in range(1, pages_count+1):
            print(f'Парсинг страницы {page} из {pages_count}')
            page_html = get_html(URL,params={'page': page})
            realty.extend(get_content(page_html.text))
    #time_parce = datetime.timedelta(datetime.now().time(),start)
    save_file(realty, FILE)
    os.startfile(FILE)
    return f'Получено {len(realty)} объектов недвижимости'

print(parcing())