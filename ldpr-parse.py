import requests
from bs4 import BeautifulSoup
import lxml
from re import findall
from json import loads
import csv


HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36', 'accept': '*/*'}
URL = 'https://primorye.ldpr.ru/event/'
PAGE_URL = 'https://primorye.ldpr.ru/api/pb/articles?site_key=primorye&aggregate=full&limit=12&page='
FILE_NAME = 'ldpr events.csv'


def get_html(url):
    r = requests.get(url, headers=HEADERS)
    return r.text


def get_event_data(event):
    '''
    Функция принимает json-элемент и извлекает из него заголовок и дату.
    Запрашивается страница из которой извлекаются титульное фото и контент.
    Вся информация возвращается в виде словаря и выводится на экран.
    '''
    url = URL + str(event['id'])
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    title = event['title']
    date = ''.join(findall(r'\d\d\d\d-\d\d-\d\d', event['created_at']))
    photo = soup.find('div', class_='flex d-flex lg12').find('img').get('src')
    content_soup = soup.find('div', class_='flex subheading font-weight-light pa-3 event-content').find_all('p')
    content_list = []
    for el in content_soup:
        content_list.append(el.string)
    content = '\n'.join(content_list)
    event_data = {
        'title': title,
        'date': date,
        'photo': photo,
        'content': content,
    }
    print(event_data)
    return event_data


def get_valid_events():
    '''
    Проверяет статьи по указанной в условии дате, если дата не совпадает: прекращает выполнение цикла.
    Для каждого валидного индекса запускает функцию по извлечению информации.
    Словари, которые возвращает get_event_data(), записываются в csv-файл.
    '''
    try:

        with open(FILE_NAME, 'w', newline='') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow(['Заголовок', 'Дата', 'Фото', 'Контент'])

            page = 1
            while True:
                json_page = get_html(PAGE_URL + str(page))
                page += 1
                text = loads(json_page)
                for el in range(len(text['info'])):
                    if str(text['info'][el]['created_at']).startswith('2021-06'):
                        result = get_event_data(text['info'][el])
                        writer.writerow([result['title'], result['date'], result['photo'], result['content']])
                    else:
                        return
    except:
        return


if __name__ == '__main__':
    get_valid_events()