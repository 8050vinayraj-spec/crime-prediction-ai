import pandas as pd
import joblib, os
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

save = os.path.dirname(__file__)
df   = pd.read_csv(os.path.join(save, 'phishing.csv'))

print("Columns:", df.columns.tolist())
print("Class values:", df['class'].unique())

X = df[['UsingIP', 'LongURL', 'ShortURL', 'HTTPS', 'SubDomains',
        'PrefixSuffix-', 'WebsiteTraffic', 'PageRank', 'GoogleIndex',
        'LinksPointingToPage']]

y = df['class'].apply(lambda x: 'phishing' if x == -1 else 'legitimate')

le = LabelEncoder()
y  = le.fit_transform(y)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

model = RandomForestClassifier(n_estimators=100, random_state=0)
model.fit(X_train, y_train)

acc = accuracy_score(y_test, model.predict(X_test))
print(f'Cyber Accuracy: {acc:.2%}')

joblib.dump(model, os.path.join(save, 'cyber_model.pkl'))
joblib.dump(le,    os.path.join(save, 'cyber_encoder.pkl'))
print('Cyber model saved successfully.')