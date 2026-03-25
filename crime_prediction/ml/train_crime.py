import pandas as pd, numpy as np, joblib, os
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

np.random.seed(42)

# Create realistic crime data with patterns based on location, month, and year
crime_data = []
# All 33 Indian states and UTs
locations = list(range(1, 34))
crime_types = ['Theft', 'Assault', 'Cybercrime', 'Fraud', 'Vandalism']

# Location-specific crime patterns
location_crime_patterns = {
    1: ['Theft', 'Assault'],              # Andhra Pradesh
    2: ['Assault', 'Vandalism'],          # Arunachal Pradesh
    3: ['Assault', 'Theft'],              # Assam
    4: ['Fraud', 'Theft'],                # Bihar
    5: ['Assault', 'Vandalism'],          # Chhattisgarh
    6: ['Theft', 'Cybercrime'],           # Goa
    7: ['Fraud', 'Theft'],                # Gujarat
    8: ['Cybercrime', 'Fraud'],           # Haryana
    9: ['Theft', 'Assault'],              # Himachal Pradesh
    10: ['Assault', 'Vandalism'],         # Jharkhand
    11: ['Cybercrime', 'Fraud'],          # Karnataka
    12: ['Theft', 'Cybercrime'],          # Kerala
    13: ['Fraud', 'Theft'],               # Madhya Pradesh
    14: ['Cybercrime', 'Fraud'],          # Maharashtra
    15: ['Assault', 'Vandalism'],         # Manipur
    16: ['Theft', 'Assault'],             # Meghalaya
    17: ['Assault', 'Vandalism'],         # Mizoram
    18: ['Assault', 'Theft'],             # Nagaland
    19: ['Theft', 'Vandalism'],           # Odisha
    20: ['Fraud', 'Theft'],               # Punjab
    21: ['Theft', 'Assault'],             # Rajasthan
    22: ['Theft', 'Assault'],             # Sikkim
    23: ['Theft', 'Cybercrime'],          # Tamil Nadu
    24: ['Cybercrime', 'Fraud'],          # Telangana
    25: ['Assault', 'Theft'],             # Tripura
    26: ['Fraud', 'Cybercrime'],          # Uttar Pradesh
    27: ['Theft', 'Assault'],             # Uttarakhand
    28: ['Theft', 'Assault'],             # West Bengal
    29: ['Cybercrime', 'Fraud'],          # Chandigarh
    30: ['Cybercrime', 'Fraud'],          # Delhi
    31: ['Assault', 'Fraud'],             # Jammu & Kashmir
    32: ['Theft', 'Assault'],             # Ladakh
    33: ['Cybercrime', 'Theft'],          # Puducherry
}

# Generate diverse training data with patterns
for year in range(2018, 2025):
    for month in range(1, 13):
        for location in locations:
            # Create 3-5 samples per location/month/year combination
            for _ in range(np.random.randint(3, 6)):
                # Pattern-based crime selection for this location
                crime = np.random.choice(location_crime_patterns[location], p=[0.6, 0.4])
                crime_data.append({
                    'year': year,
                    'month': month,
                    'location': location,
                    'crime_type': crime
                })

data = pd.DataFrame(crime_data)
print(f"Training data shape: {data.shape}")
print(f"\nCrime type distribution:\n{data['crime_type'].value_counts()}")
print(f"\nLocation distribution:\n{data['location'].value_counts().sort_index()}")

# Prepare features and target
le = LabelEncoder()
y = le.fit_transform(data['crime_type'])
X = data[['year', 'month', 'location']]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Random Forest with optimized parameters
model = RandomForestClassifier(
    n_estimators=250,
    max_depth=18,
    min_samples_split=4,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1
)
model.fit(X_train, y_train)

# Evaluate model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f'\nCrime Prediction Accuracy: {accuracy:.2%}')
print(f'\nClassification Report:\n{classification_report(y_test, y_pred, target_names=le.classes_)}')

# Save model and encoder
save = os.path.dirname(__file__)
joblib.dump(model, os.path.join(save, 'crime_model.pkl'))
joblib.dump(le, os.path.join(save, 'label_encoder.pkl'))
print('\n✓ Saved crime_model.pkl and label_encoder.pkl')
print(f'✓ Model trained on {len(data)} samples across {len(locations)} states/UTs')

