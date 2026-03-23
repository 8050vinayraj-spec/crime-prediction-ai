import numpy as np, pandas as pd, joblib, os
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

np.random.seed(0)
n = 600
data = pd.DataFrame({
    'url_length':          np.random.randint(10, 200, n),
    'has_ip':              np.random.randint(0, 2, n),
    'suspicious_keywords': np.random.randint(0, 10, n),
    'has_https':           np.random.randint(0, 2, n),
    'label':               np.random.choice(['legitimate','phishing'], n)
})
le = LabelEncoder()
y  = le.fit_transform(data['label'])
X  = data[['url_length','has_ip','suspicious_keywords','has_https']]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
model = GaussianNB()
model.fit(X_train, y_train)
print(f'Cyber Accuracy: {accuracy_score(y_test, model.predict(X_test)):.2%}')
save = os.path.dirname(__file__)
joblib.dump(model, os.path.join(save, 'cyber_model.pkl'))
joblib.dump(le,    os.path.join(save, 'cyber_encoder.pkl'))
print('Saved cyber_model.pkl and cyber_encoder.pkl')
