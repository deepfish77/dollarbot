from datetime import datetime, timedelta
import pytz
from datetime import date, time, timedelta, datetime
from retrying import retry
import requests

import boto3

ssm = boto3.client("ssm")


def get_call(url, header, params={}):
    status_code = None
    try:
        response = requests.get(url, headers=header, params=params)
        print("status_code", response.status_code)

        if response.status_code:
            status_code = response.status_code
        response.raise_for_status()
    except requests.HTTPError:
        if status_code >= 400 and status_code < 500:
            print(f"Bad Request, status: {status_code}")
        elif status_code >= 500:
            print(f"Internal Server Error, status code : {status_code}")
        elif status_code != 200:
            print(f"Please Check issue with status code: {status_code}")

    except requests.Timeout:
        print("Timeout")
    return response


@retry(wait_exponential_multiplier=1000, wait_exponential_max=32000)
def get_call_retries(url, header, params={}):
    return get_call(url, header, params)
