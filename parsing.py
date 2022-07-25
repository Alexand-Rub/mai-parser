import datetime
import requests
from bs4 import BeautifulSoup as Bs
from progress.bar import Bar


def normalization_date(date_text: str):
    try:
        normalized_date = datetime.datetime.strptime(date_text, '%Y.%m.%d').date()
        return normalized_date
    except ValueError:
        print("Некорректная дата! Введите дату ещё раз: ")


def get_page(page_utl: str):
    request = requests.get(page_utl)
    page = Bs(request.content, 'html.parser')
    return page


def get_microwave_journal(link: str):
    months_dict = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,
                   'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12}
    class_dick = {'Дата': '.date', 'Заголовок': '.headline > a', 'Описание': '.abstract > p'}

    page_num, article_num = 1, 1
    articles_info = list()
    tag_count = dict()
    end_date = normalization_date(input('\nДо какой даты скачивать статьи? (гггг.мм.дд) '))
    flag_date, last_date = datetime.date, datetime.date.today()
    total_day = 0
    bar = Bar('Загрузка', suffix='%(percent)d%%', max=(datetime.date.today()-end_date).days)
    while True:
        page = get_page(page_utl=link[:-1] + str(page_num))
        articles_list = page.select('.article-summary__details')
        if len(articles_list) > 0:
            for article in articles_list:
                info_dict = dict()
                for class_key in class_dick.keys():
                    try:
                        select = article.select_one(class_dick[class_key])
                        info = select.text
                        match class_key:
                            case 'Дата':
                                month, day, year = info.split()
                                info = '{year}.{month}.{day}'.format(
                                    year=year, month=months_dict[month], day=day[:-1]
                                )
                                flag_date = datetime.datetime.strptime(info, '%Y.%m.%d').date()

                                if flag_date < end_date:
                                    if total_day < (datetime.date.today() - end_date).days:
                                        bar.next((datetime.date.today() - end_date).days - total_day)
                                    bar.finish()
                                    source_info = {
                                        'articles': articles_info,
                                        'tags': tag_count
                                    }
                                    return source_info
                            case 'Заголовок':
                                tags = [tag.text for tag in get_page(select['href']).select('.tags > a')]
                                for tag in tags:
                                    if tag in tag_count.keys():
                                        tag_count[tag] += 1
                                    else:
                                        tag_count[tag] = 1
                                info_dict['теги'] = ', '.join(tags)

                        info_dict[class_key] = info
                    except AttributeError:
                        info_dict[class_key] = 'Нет данных'
                articles_info.append(info_dict)
                bar.next((last_date-flag_date).days)
                last_date = flag_date
                article_num += 1
        else:
            if total_day < (datetime.date.today()-end_date).days:
                bar.next((datetime.date.today()-end_date).days - total_day)
            bar.finish()
            source_info = {
                'articles': articles_info,
                'tags': tag_count
            }
            return source_info
        page_num += 1





