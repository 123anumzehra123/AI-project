import joblib
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder
import numpy as np

import joblib

def predict_disorder(user_answers):

    loaded_model = joblib.load('naive_bayes_model (1).joblib')
    label_encoder = joblib.load('label_encoder.joblib')

    answer_map = {'yes': 2, 'sometimes': 1, 'no': 0}
    input_vector = [answer_map[ans] for ans in user_answers]

    # Reshape input to match model's expected format
    loaded_prediction = loaded_model.predict([input_vector])

    disorder_name = label_encoder.inverse_transform(loaded_prediction)
    print(disorder_name)
    return disorder_name[0]
