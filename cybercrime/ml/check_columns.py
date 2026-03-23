import pandas as pd
import os

path = os.path.join('cybercrime', 'ml', 'phishing.csv')
print('File exists:', os.path.exists(path))
df = pd.read_csv(path)
print(df.columns.tolist())
print(df.head())