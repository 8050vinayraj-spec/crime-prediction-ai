import pandas as pd, numpy as np, joblib, os
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

np.random.seed(42)
n = 500
data = pd.DataFrame({
    'year':       np.random.randint(2018, 2025, n),
    'month':      np.random.randint(1, 13, n),
    'location':   np.random.randint(1, 20, n),
    'crime_type': np.random.choice(['Theft','Assault','Cybercrime','Fraud','Vandalism'], n)
})
le = LabelEncoder()
y  = le.fit_transform(data['crime_type'])
X  = data[['year','month','location']]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
print(f'Crime Accuracy: {accuracy_score(y_test, model.predict(X_test)):.2%}')
save = os.path.dirname(__file__)
joblib.dump(model, os.path.join(save, 'crime_model.pkl'))
joblib.dump(le,    os.path.join(save, 'label_encoder.pkl'))
print('Saved crime_model.pkl and label_encoder.pkl')
