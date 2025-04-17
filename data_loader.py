# data_loader.py
import pandas as pd
import sqlite3

# Replace with your drive file path (after downloading the file)
df = pd.read_csv('HR_Analytics.csv')

conn = sqlite3.connect('database.db')
df.to_sql('employees', conn, if_exists='replace', index=False)

conn.commit()
conn.close()
