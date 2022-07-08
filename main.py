import requests
from bs4 import BeautifulSoup as Bs
import datetime


def microwavejournal(older_date=datetime.date.today() - datetime.timedelta(30)):
    months = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,
              'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12}

    article_dict = dict()
    article_list = list()
    flag_date = datetime.date.today()

    page_num = 1
    while True:
        request = requests.get('https://www.microwavejournal.com/articles/topic/3372?page=' + str(page_num))
        page = Bs(request.content, 'html.parser')
        # Получаем список новостей на странице
        articles = page.select('.article-summary__details')
        # Проверка пуста ли страница
        if len(articles):
            # Проходим по статьям на странице
            for news in articles:
                class_list = {'Дата': '.date', 'Заголовок': '.headline > a', 'Описание': '.abstract > p'}
                for select_class in class_list.keys():
                    description = news.select_one(class_list[select_class])
                    if select_class == 'Дата':
                        month = months[description.text.split(' ')[0]]
                        day = description.text.split(' ')[1][:-1]
                        year = description.text.split(' ')[2]
                        flag_date = datetime.date(int(year), int(month), int(day))
                        if flag_date < older_date:
                            return article_list
                        article_dict[select_class] = f'{year}.{month}.{day}'
                    else:
                        try:
                            article_dict[select_class] = description.text
                        except AttributeError:
                            article_dict[select_class] = 'Нет данных'
                article_list.append(article_dict)
            page_num += 1


def normalization_date(date_text: str):
    try:
        normalized_date = datetime.datetime.strptime(date_text, '%Y.%m.%d').date()
        return normalized_date
    except ValueError:
        input("Некорректная дата! Введите дату ещё раз: ")


if __name__ == '__main__':
    print('До какой даты смотерть статьи?')
    end_date = normalization_date(date_text=input('Введите дату (гггг.мм.дд): '))
    print(microwavejournal(older_date=end_date))
