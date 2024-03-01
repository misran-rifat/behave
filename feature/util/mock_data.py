import os

import pandas as pd
from faker import Faker


def generate_random_data(number_of_rows, file_format):
    fake = Faker()
    data = {
        'first_name': [fake.first_name() for _ in range(number_of_rows)],
        'last_name': [fake.last_name() for _ in range(number_of_rows)],
        'ssn': [fake.ssn() for _ in range(number_of_rows)],
        'dob': [fake.date_of_birth() for _ in range(number_of_rows)],
    }

    df = pd.DataFrame(data)
    root = '../data/'
    full_dir_path = os.path.join(root, file_format)
    if not os.path.exists(full_dir_path):
        os.makedirs(full_dir_path)

    if file_format == 'csv':
        df.to_csv(os.path.join(full_dir_path, 'random_data.csv'), index=False)
    elif file_format == 'excel':
        df.to_excel(os.path.join(full_dir_path, 'random_data.xlsx'), index=False, engine='openpyxl')
    elif file_format == 'parquet':
        df.to_parquet(os.path.join(full_dir_path, 'random_data.parquet'), index=False)
    else:
        raise ValueError("Unsupported file format. Please choose 'csv', 'excel', or 'parquet'.")


generate_random_data(1000, 'csv')
