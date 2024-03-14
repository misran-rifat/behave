import io

import boto3
import pandas as pd


def authenticate_to_aws():
    try:
        session = boto3.Session()
        return session
    except Exception as e:
        print(f"An error occurred: {e}")


def read_file_from_s3(bucket_name, file_key):
    session = authenticate_to_aws()
    if session:
        s3 = session.resource('s3')
        obj = s3.Object(bucket_name, file_key)
        body = obj.get()['Body'].read()

        if file_key.endswith('.csv'):
            return pd.read_csv(io.BytesIO(body))
        elif file_key.endswith('.xlsx'):
            return pd.read_excel(io.BytesIO(body))
        elif file_key.endswith('.parquet'):
            return pd.read_parquet(io.BytesIO(body))
        else:
            print("Unsupported file format")
            return None
    else:
        print("Failed to authenticate to AWS")
        return None
