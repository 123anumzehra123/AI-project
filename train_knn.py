import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib

# 1. Load dataset
df = pd.read_csv("mental_health_dataset.csv")

# 🔧 Drop any rows with missing values
df.dropna(inplace=True)

# ✅ Ensure labels are strings
df["label"] = df["label"].astype(str)

# 🧪 Debug: print label classes
print("Labels in dataset:", df["label"].unique())

# 2. Ensure all answers are integers
df.iloc[:, :-1] = df.iloc[:, :-1].astype(int)

# 3. Encode the labels
label_encoder = LabelEncoder()
df["label"] = label_encoder.fit_transform(df["label"])

# 4. Split the data
X = df.drop("label", axis=1)
y = df["label"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 5. Train the KNN model
knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(X_train, y_train)

# 6. Evaluate
y_pred = knn.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred, target_names=label_encoder.classes_))

# 7. Save model and label encoder
joblib.dump(knn, "knn_model.pkl")
joblib.dump(label_encoder, "label_encoder.pkl")
