import requests
import pandas as pd
from pandas import json_normalize
import time
import datetime

def get_URI(query: str, page_num: str, date: str, API_KEY: str) -> str:
    """
    Возвращает URL для статей по запросу, номеру страницы и дате.
    """
    # Формируем URI с параметрами запроса
    URI = (
        f'https://api.nytimes.com/svc/search/v2/articlesearch.json?q={query}'
        f'&page={page_num}&begin_date={date}&end_date={date}'
        f'&api-key={API_KEY}'
    )
    return URI

# Создаем датафрейм для хранения всех записей
df = pd.DataFrame()

# Получаем текущую дату
current_date = datetime.datetime.now().strftime('%Y%m%d')

# Собираем данные со всех доступных страниц
page_num = 1

while page_num < 6:
    # Получаем URI с записями, относящимися к COVID на текущую дату
    URI = get_URI(
        query='COVID',
        page_num=str(page_num),
        date=current_date,
        API_KEY='cCUIGMNHzrJMUkZaKf4Y11r5tTBS0qpJ',
    )

    # Делаем запрос по URI
    response = requests.get(URI)

    # Преобразуем результат в формат JSON
    data = response.json()

    print(data)

    # Преобразуем данные в датафрейм
    df_request = json_normalize(data)

    # Прерываем цикл, если отсутствуют новые записи
    if df_request.empty:
        break

    # Добавляем записи в конец датафрейма
    df = pd.concat([df, df_request])

    # Пауза для соблюдения требований к количеству запросов
    time.sleep(6)

    # Переходим на следующую страницу
    page_num += 1

df.info()
print(df)
print('this')
