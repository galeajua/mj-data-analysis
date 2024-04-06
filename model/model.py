import argparse
import pandas as pd
from pymongo import MongoClient
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler
import pickle

# Argument parsing
parser = argparse.ArgumentParser(description='Predict Basketball Game Outcomes')
parser.add_argument('-u', '--uri', required=True, help="MongoDB URI with username/password")
args = parser.parse_args()

# MongoDB setup
mongo_uri = args.uri
mongo_db = "mj_career_stats"
mongo_collection = "mj_career"

client = MongoClient(mongo_uri)
db = client[mongo_db]
collection = db[mongo_collection]

# Fetch data from MongoDB
documents = collection.find({}, {"_id": 0, "Date": 0, "Opponent": 0})  # Exclude non-numeric and non-predictive fields

# Create DataFrame
df = pd.DataFrame(list(documents))

# Feature engineering
# Convert "Result" to a binary outcome: 1 for win (W), 0 for loss (L)
df['Outcome'] = df['Result'].apply(lambda x: 1 if 'W' in x else 0)
df.drop(columns=['Result'], inplace=True)

# Convert all columns to numeric type
df = df.apply(pd.to_numeric, errors='coerce')

# Handle missing values if necessary
df.fillna(df.mean, inplace=True)  # Example strategy: fill missing values with 0

# Split data into features (X) and target variable (y)
X = df.drop(columns=['Outcome'])
y = df['Outcome']

print(f"Number of features: {X.shape[1]}")
print("Feature names:")
print(X.columns.tolist())

# Splitting the dataset into the Training set and Test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

# Feature Scaling
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Training the Random Forest Classifier
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Predicting the Test set results
y_pred = clf.predict(X_test)

# Evaluating the Model
print("Accuracy Score:", accuracy_score(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))

# Save the trained model to disk
with open('basketball_game_outcome_predictor.pkl', 'wb') as file:
    pickle.dump(clf, file)

# Optionally, to load the model back from disk:
with open('basketball_game_outcome_predictor.pkl', 'rb') as file:
    loaded_clf = pickle.load(file)
