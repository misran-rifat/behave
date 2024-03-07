import sqlite3

import pandas as pd
from faker import Faker


def before_all(context):
    fake = Faker()
    context.conn = sqlite3.connect(':memory:')
    cursor = context.conn.cursor()
    cursor.execute('''CREATE TABLE customer
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, full_name TEXT, age INTEGER)''')
    for _ in range(10):
        full_name = fake.name()
        age = fake.random_int(min=18, max=80)
        cursor.execute("INSERT INTO customer (full_name, age) VALUES (?, ?)", (full_name, age))
    context.conn.commit()
    cursor.execute("SELECT * FROM customer")
    rows = cursor.fetchall()
    df = pd.DataFrame(rows, columns=['id', 'full_name', 'age'])
    context.df = df
    print(context.df.to_markdown(index=False))
    assert context.df['full_name'].isnull().sum() == 0, "full_name contains null values"


def after_all(context):
    context.conn.close()
