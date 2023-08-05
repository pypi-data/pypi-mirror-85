import pickle
from typing import Any

import boto3

BUCKET_NAME: str = 'robinhood-day-trader'
UTF: str = 'utf-8'


def get_s3():
    return boto3.resource('s3')


def get_s3_client():
    return boto3.client('s3')


def get_bucket():
    return get_s3().Bucket(BUCKET_NAME)


def get_s3_file(path: str):
    return pickle.loads(get_s3().Object(BUCKET_NAME, path).get()['Body'].read())


def upload_s3_file(path: str, data: Any) -> None:
    get_bucket().put_object(Key=path, Body=pickle.dumps(data))


if __name__ == '__main__':

    upload_s3_file(path='stocks.json', data=["AAPL", "FRAF", "IPI", "NLOK", "WHR", "FB", "BIIB", "PINS", "DRRX", "IDN"])

    print(get_s3_file(path='stocks.json'))


