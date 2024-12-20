import pandas as pd
import numpy as np
import random
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LogisticRegression

# Метрики и их веса
METRICS_WEIGHTS = {
    "business_process_importance": 0.15,
    "monitoring_score": 0.15,
    "technical_complexity": 0.13,
    "integration_level": 0.12,
    "team_experience": 0.10,
    "urgency": 0.10,
    "change_management_plan": 0.10,
    "regulatory_compliance": 0.05,
    "change_predictability": 0.05,
    "error_response": 0.05,
}

# Генерация данных для примера
def generate_data(num_samples=100):
    data = np.random.rand(num_samples, len(METRICS_WEIGHTS))  # Случайные значения метрик
    weights = np.array(list(METRICS_WEIGHTS.values()))
    risk_scores = np.dot(data, weights)  # Вычисление итогового риска
    risk_labels = np.digitize(risk_scores, bins=[0.33, 0.66])  # 0 - низкий, 1 - средний, 2 - высокий
    return data, risk_labels

# Подготовка данных
X, y = generate_data(num_samples=500)
feature_names = list(METRICS_WEIGHTS.keys())
df = pd.DataFrame(X, columns=feature_names)
df['risk_level'] = y

# Нормализация данных
scaler = MinMaxScaler()
X_normalized = scaler.fit_transform(df[feature_names])

# Разделение на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X_normalized, df['risk_level'], test_size=0.2, random_state=42)

# Обучение модели
model = LogisticRegression(multi_class='multinomial', max_iter=200)
model.fit(X_train, y_train)

# Оценка модели
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred, target_names=['Низкий риск', 'Средний риск', 'Высокий риск']))

# Предсказание уровня риска для нового релиза
def predict_risk(metrics_values):
    """Предсказывает уровень риска на основе значений метрик."""
    if len(metrics_values) != len(METRICS_WEIGHTS):
        raise ValueError("Количество значений метрик не совпадает с количеством метрик.")
    normalized_values = scaler.transform([metrics_values])
    prediction = model.predict(normalized_values)
    risk_levels = {0: "Низкий риск", 1: "Средний риск", 2: "Высокий риск"}
    return prediction[0]

# Пример использования
new_release_metrics = [0.8, 0.6, 0.7, 0.4, 0.9, 0.3, 0.8, 0.5, 0.6, 0.7]
predicted_risk = predict_risk(new_release_metrics)
print(f"Предсказанный уровень риска: {predicted_risk}")

