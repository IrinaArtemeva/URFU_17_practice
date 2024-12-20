
import requests
import json
import pandas as pd
from pandas import json_normalize
from sqlalchemy import create_engine


def get_URI(query: str, page_num: str, date: str, API_KEY: str) -> str:
    """# возвращет URL к статьям для текущего запроса по номеру страницы и дате """

    # добавляем запрос к uri
    URI = f'https://api.nytimes.com/svc/search/v2/articlesearch.json?q={query}'

    # добавляем номер страницы и дату
    URI = URI + f'&page={page_num}&begin_date={date}&end_date={date}'

    # добавляем ключ API
    URI = URI + f'&api-key={API_KEY}'

    return URI


import time
import datetime

# создаем датафрейм для хранения всех записей
df = pd.DataFrame()

# получаем текущую дату
current_date = datetime.datetime.now().strftime('%Y%m%d')

# собираем данные со всех доступных страниц
page_num = 1

while page_num < 6:

    # получаем URI с записями, относящимся к замним олимпийским играм на текущую дату
    URI = get_URI(query='COVID', page_num=str(page_num), date=current_date, API_KEY='cCUIGMNHzrJMUkZaKf4Y11r5tTBS0qpJ')

    # делаем запрос по URI
    response = requests.get(URI)

    #print(response)


    # преобразуем результат в формат JSON
    data = response.json()

    print(data)

    # преобразуем данные в фрейм данных
    df_request = json_normalize(data)

    # прерываем цикл если отсутсвуют новые записи
    if df_request.empty:
        break

    # добавляем записи в конец дата фрейма
    df = pd.concat([df, df_request])

    # пауза для требования по количеству запросов
    time.sleep(6)

    # переходим на следующую страницу
    page_num += 1

df.info()

print(df)