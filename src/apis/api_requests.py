from datetime import datetime, timedelta
from retrying import retry
import requests

import boto3

ssm = boto3.client("ssm")


import requests


def get_call(url, header, params={}, timeout=30):
    """
    Makes a GET request to the specified URL with error handling.

    Args:
        url (str): The target URL for the GET request.
        header (dict): A dictionary of HTTP headers to send with the request.
        params (dict, optional): Query parameters to include in the request. Defaults to an empty dictionary.
        timeout (int, optional): The maximum time, in seconds, to wait for a response. Defaults to 30 seconds.

    Returns:
        requests.Response: The response object from the GET request if successful.

    Raises:
        requests.HTTPError: If an HTTP error occurs (status code 4xx or 5xx).
        requests.Timeout: If the request times out.
        Exception: If an unexpected error occurs.
    """
    status_code = None
    response = None

    try:
        response = requests.get(url, headers=header, params=params, timeout=timeout)
        print("status_code", response.status_code)

        if response.status_code:
            status_code = response.status_code
        response.raise_for_status()
    except requests.HTTPError:
        if status_code and 400 <= status_code < 500:
            print(f"Bad Request, status: {status_code}")
        elif status_code and status_code >= 500:
            print(f"Internal Server Error, status code: {status_code}")
        elif status_code and status_code != 200:
            print(f"Please check the issue with status code: {status_code}")
    except requests.Timeout:
        print("Timeout")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return response


def post_call(url, header, data=None, json=None, params={}, timeout=30):
    """
    Makes a POST request to the specified URL with error handling.

    Args:
        url (str): The target URL.
        header (dict): The headers for the request.
        data (dict, optional): The form-encoded data to send in the request body.
        json (dict, optional): The JSON data to send in the request body.
        params (dict, optional): The query parameters for the request.
        timeout (int, optional): The timeout for the request in seconds. Default is 30.

    Returns:
        requests.Response: The response object.
    """
    status_code = None
    response = None

    try:
        response = requests.post(
            url, headers=header, data=data, json=json, params=params, timeout=timeout
        )
        print("status_code", response.status_code)

        if response.status_code:
            status_code = response.status_code
        response.raise_for_status()
    except requests.HTTPError:
        if status_code and status_code >= 400 and status_code < 500:
            print(f"Bad Request, status: {status_code}")
        elif status_code and status_code >= 500:
            print(f"Internal Server Error, status code : {status_code}")
        elif status_code != 200:
            print(f"Please Check issue with status code: {status_code}")
    except requests.Timeout:
        print("Timeout")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return response


import requests


def make_request(
    method, url, headers=None, params=None, data=None, json=None, timeout=30
):
    """
    Makes an HTTP request with error handling.

    Args:
        method (str): HTTP method (e.g., 'GET', 'POST', 'PUT', 'DELETE').
        url (str): The target URL.
        headers (dict, optional): Headers for the request.
        params (dict, optional): Query parameters for the request.
        data (dict, optional): Form-encoded data for the request body.
        json (dict, optional): JSON data for the request body.
        timeout (int, optional): Timeout for the request in seconds. Default is 30.

    Returns:
        requests.Response: The response object, or None if an error occurs.
    """
    status_code = None
    response = None

    try:
        # Make the request using the provided method
        response = requests.request(
            method,
            url,
            headers=headers,
            params=params,
            data=data,
            json=json,
            timeout=timeout,
        )
        print("status_code", response.status_code)

        if response.status_code:
            status_code = response.status_code
        response.raise_for_status()
    except requests.HTTPError:
        if status_code and 400 <= status_code < 500:
            print(f"Client Error: {status_code}")
        elif status_code and status_code >= 500:
            print(f"Server Error: {status_code}")
        else:
            print(f"Unexpected status code: {status_code}")
    except requests.Timeout:
        print("Request timed out.")
    except requests.RequestException as e:
        print(f"An unexpected error occurred: {e}")

    return response


@retry(wait_exponential_multiplier=1000, wait_exponential_max=32000)
def get_call_retries(url, header, params={}):
    return get_call(url, header, params)
