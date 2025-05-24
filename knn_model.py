import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder
import numpy as np

# Load and preprocess dataset
def train_model():
    df = pd.read_csv("C:/python_project/python_project/mental_health_dataset.csv")  # replace with your actual dataset filename

    # Encode categorical answers
    answer_map = {'yes': 2, 'sometimes': 1, 'no': 0}
    for col in df.columns[:-1]:  # assuming last column is 'disorder'
        df[col] = df[col].map(answer_map)

    label_encoder = LabelEncoder()
    df['disorder'] = label_encoder.fit_transform(df['disorder'])

    X = df.drop('disorder', axis=1)
    y = df['disorder']

    knn = KNeighborsClassifier(n_neighbors=3)
    knn.fit(X, y)

    return knn, label_encoder

# Predict disorder using trained model
def predict_disorder(user_answers):
    knn, label_encoder = train_model()

    # Convert answers to numbers
    answer_map = {'yes': 2, 'sometimes': 1, 'no': 0}
    input_vector = [answer_map[ans] for ans in user_answers]

    # Predict
    prediction = knn.predict([input_vector])
    disorder_name = label_encoder.inverse_transform(prediction)
    return disorder_name[0]
