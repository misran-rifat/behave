import boto3
import pandas as pd


def authenticate_to_aws():
    try:
        credentials_path = '../data/aws_credential/aws_credentials.csv'
        credentials_df = pd.read_csv(credentials_path)
        aws_access_key_id = credentials_df['AWS_ACCESS_KEY_ID'].iloc[0]
        aws_secret_access_key = credentials_df['AWS_SECRET_ACCESS_KEY'].iloc[0]
        session = boto3.Session(aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
        return session
    except FileNotFoundError:
        print("The credentials file was not found.")
    except KeyError:
        print("The credentials file is missing required columns.")
    except Exception as e:
        print(f"An error occurred: {e}")
