import pandas as pd
import random

# Количество записей
num_records = 1000

criticality_levels = ["Низкая", "Средняя", "Высокая"]
# Качество данных от 60 до 100
# Сложность изменений от 1 до 10
# История ошибок (0-6)
# Объем данных (5-200 ГБ)
# Количество связанных процессов (1-20)

# Генерация синтетических данных
data = {
    "Витрина": [f"DWH_Vitrina_{i+1}" for i in range(num_records)],
    "Критичность": [random.choice(criticality_levels) for _ in range(num_records)],
    "Объём данных (ГБ)": [random.randint(5, 201) for _ in range(num_records)],
    "Кол-во связей": [random.randint(1, 21) for _ in range(num_records)], 
    "Качество данных": [random.randint(60, 101) for _ in range(num_records)],
    "Сложность изменений": [random.randint(1, 11) for _ in range(num_records)],
    "Ошибки в истории": [random.randint(0, 7) for _ in range(num_records)],
}

df = pd.DataFrame(data)

def calculate_risk(row):
    if row["Критичность"] == "Высокая" and row["Ошибки в истории"] > 4:
        return "Высокий"
    elif row["Критичность"] == "Средняя" and row["Ошибки в истории"] > 2:
        return "Средний"
    else:
        return "Низкий"

df["Уровень риска"] = df.apply(calculate_risk, axis=1)

df.to_csv("synthetic_data.csv", index=False, encoding="utf-8-sig")

df
