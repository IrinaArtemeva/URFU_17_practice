import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
page_title="Здесь будет красивое название",
page_icon="🧊")

def load_dataframe(file):
    # Читаем файл в DataFrame
    df = pd.read_csv(file)
    return df
    # Создаем файловый загрузчик с меткой и разрешенными типами файлов
    uploaded_file = st.file_uploader("Выберите CSV файл для загрузки", type="csv")

def create_colored_container(color, header, content):
    st.markdown(
        f"""
        <div style="background-color: {color}; padding: 20px; border-radius: 10px; margin-bottom: 15px;">
            <h2 style="color: black;">{header}</h2>
            <p style="color: black;">{content}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# Изменение дизайна страницы
page_element="""
<style>
[data-testid="stAppViewContainer"]{
  background-image: url("https://abrakadabra.fun/uploads/posts/2022-02/1643785322_14-abrakadabra-fun-p-zelenii-fon-sberbanka-16.jpg");
  background-size: cover;
}
[data-testid="baseButton-secondary"]{
background-color: rgb(24 118 42 / 70%);
}
[data-testid="stBaseButton-secondary"]{
background-color: rgb(133 123 12 / 71%);
}
[data-testid="stFileUploaderDropzone"]{
background-color: rgb(255, 255, 255);
}
[data-baseweb="base-input"]{
background-color: rgb(255, 255, 255);
}
[role="tablist"]{
background-color: rgb(24 118 42 / 90%);
border-radius: 10px;
height=100
}
[data-testid="stHeader"]{
  background-color: rgba(0,0,0,0);
}
.st-b1{
  margin: auto;
}
[data-testid="block-container"]
 { background-color: rgba(255, 255, 255, 0.4)
}
.st-cc {
    margin: auto;
}

</style>
"""
st.markdown(page_element, unsafe_allow_html=True)
# Инициализация состояния для страницы
if 'page' not in st.session_state:
    st.session_state.page = 'Main'  # По умолчанию главная страница

# Функция для перехода на главную страницу
def go_to_main():
    st.session_state.page = 'Main'

# Функция для перехода на страницу контактов
def go_to_contact():
    st.session_state.page = 'Contact'

# Определяем содержимое каждой страницы
def main_page():
    # Заголовок страницы
    st.title('ЗАГОЛОВОК')


    create_colored_container("#edededb3", 'Часть 1. Оценка про результатам мониторинга с тестированием витрин данных.', "Пояснение: ввиду отсутствия информации и доступа к реально используемым инструментам, к которым мог бы создаваться мониторинг, нашей командой принято решение на этапе демонстрации дать возможность пользователю самому выбрать данные для мониторинга. Вы можете указать путь либо загрузить данные в формате csv.")
    create_colored_container("#1ea137", "Оригинальная база данных:", " ")


    # Создаем два столбца
    col1, col2 = st.columns(2)

    # Создаем первый контейнер
    with col1:
        url_input = st.text_input("Введите URL:", key="url_input_1")
    
        if url_input:
            try:
                webbrowser.open(url_input)
                st.success("Ссылка успешно открыта!")
            except ValueError:
                st.error("Неверная ссылка. Пожалуйста, введите корректный URL.")


    # Создаем второй контейнер
    with col2:
        uploaded_file = st.file_uploader("Выберите CSV файл для загрузки", key="uploaded_file_1", type="csv")

        if uploaded_file is not None:
            df = load_dataframe(uploaded_file)  # Предполагается, что эта функция определена где-то в коде

    create_colored_container("#1ea137", "Витрина для тестирования:", " ")

    # Создаем два столбца
    col3, col4 = st.columns(2)

    # Создаем первый контейнер
    with col3:
        url_input = st.text_input("Введите URL:", key="url_input_2")
    
        if url_input:
            try:
                webbrowser.open(url_input)
                st.success("Ссылка успешно открыта!")
            except ValueError:
                st.error("Неверная ссылка. Пожалуйста, введите корректный URL.")


    # Создаем второй контейнер
    with col4:
        uploaded_file = st.file_uploader("Выберите CSV файл для загрузки", key="uploaded_file_2", type="csv")

        if uploaded_file is not None:
            df = load_dataframe(uploaded_file) 
        


    create_colored_container("#edededb3", "Часть 2. Оценка уровня риска текущих процессов проекта.", "Пояснение: для выбора стратегии тестирования предлагаем вам сообщить нам анкетные данные о вашем проекте")  


# Создаем контейнер для таблицы
    container = st.container()

# Создаем DataFrame с собственными данными
    data = {
        'Метрики': ["Важность бизнес-процессов", 
        "Оценка мониторинга",
	"Техническая сложность",
	"Уровень интеграции с другими системами",
	"Опыт команды",
	"Срочность",
	"План управления изменениями",
	"Соответствие требованиям регуляторов",
	"Прогнозируемость изменений",
	"Реакция на ошибки"],
        'Веса метрик': ['15%', '15%', '13%', '12%', '10%', '10%', '10%', '5%', '5%', '5%']
    }


    df = pd.DataFrame(data)

# Отображаем таблицу без индексов
    st.dataframe(df, hide_index=True)
   
    col5, col6, col7, col8, col9 = st.columns(5)

    # Второй столбец содержит кнопку
    with col7: 
        st.button("ОЦЕНИТЬ", on_click=go_to_contact)

def contact_page():
    st.title('РЕЗУЛЬТАТЫ ОЦЕНКИ')
    with st.container():
        create_colored_container("#1ea137", "Предлагаемая стратегия тестирования:", " ")
        with st.container():
            create_colored_container("#ffffff", "", "(вывод из принта нашего классификатора)") 
    # Создаем два столбца
    col01, col02 = st.columns(2)

    # Создаем первый контейнер
    with col01:
        create_colored_container("#1ea137", "Информация о тестировании витрин:", " ")
        create_colored_container("#ffffff", "", "(вывод результата прогона проверок в красивом графике)") 
    with col02:
        create_colored_container("#1ea137", "Информация из анкеты бизнес-процессов:", " ")
        create_colored_container("#ffffff", "", "(список критериев и вывод введенных данных с предыдущей страницы)")     
    create_colored_container("#ffffff", "", "(Хед протестированной витрины, выбранной на предыдущей странице)")      

    st.button("Вернуться на главную страницу", on_click=go_to_main)

# Логика отображения в зависимости от состояния
if st.session_state.page == 'Main':
    main_page()
else:
    contact_page()
