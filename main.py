import requests
from bs4 import BeautifulSoup as Bs

page_num = 1
while page_num <= 2:
    request = requests.get('https://www.microwavejournal.com/articles/topic/3372?page=' + str(page_num))
    page = Bs(request.content, 'html.parser')
    articles = page.select('.article-summary__details')
    if len(articles):
        for news in articles:
            class_list = {'Дата': '.date',
                          'Заголовок': '.headline > a',
                          'Описание': '.abstract > p'}

            for select_class in class_list.keys():
                description = news.select_one(class_list[select_class])
                try:
                    print('{title}: {description}'.format(
                        title=select_class, description=description.text
                    ))
                except:
                    print('{title}: {description}'.format(
                        title=select_class, description='Нет данных'
                    ))
            print()
    page_num += 1



