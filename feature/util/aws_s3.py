import boto3


def authenticate_to_aws():
    try:
        session = boto3.Session()
        return session
    except Exception as e:
        print(f"An error occurred: {e}")
