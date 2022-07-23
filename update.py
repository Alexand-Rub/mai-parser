import sqlite3 as sq
import datetime
import requests
from bs4 import BeautifulSoup as Bs


def date_maker(fix_date):
    month, day, year = fix_date.split()
    months_dict = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,
                   'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12}
    normal_date = '{year}.{month}.{day}'.format(
        year=year, month=months_dict[month], day=day[:-1]
    )
    return datetime.datetime.strptime(normal_date, '%Y.%m.%d').date()


def check_update():
    today = datetime.date.today()
    bd = sq.connect('articles.db')
    cur = bd.cursor()
    cur.execute("SELECT * FROM source;")
    sources = cur.fetchall()
    cur.execute("SELECT date FROM classes WHERE site_name = 'Microwave Journal'")
    date_class = cur.fetchone()[0]
    to_update = list()
    for source in sources:
        if source[3] is not None:
            check_date = datetime.datetime.strptime(source[3], '%Y.%m.%d').date()
            request = requests.get(source[2])
            page = Bs(request.content, 'html.parser')
            last_date = date_maker(fix_date=page.select_one(date_class).text)
            if check_date < last_date:
                to_update.append(source[1])
        else:
            to_update.append(source[1])
    return to_update


def add_articles(update_list: list):
    pass


if __name__ == '__main__':
    command = input('Команды:\n1. Проверить наличие оновлений\n\nВведите команду: ')
    match command:
        case '1':
            updates = check_update()
            print('Доступно обновлений: {updates}\n'.format(updates=len(updates)))
            command = input('Обновить данные? (1. Да, 2. Нет): ')
            match command:
                case '1': add_articles(updates)


