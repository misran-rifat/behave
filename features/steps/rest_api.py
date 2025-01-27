import json

from behave import *
import requests

use_step_matcher("re")


@given("I use GET_request to call the (?P<endpoint>.+)")
def step_impl(context, endpoint):
    headers = {
        "Accept": "application/json",
        "Connection": "keep-alive"
    }
    try:
        context.response = requests.get(endpoint, headers=headers)
        context.logger.info(f'GET request to {endpoint}')
    except requests.exceptions.RequestException as e:
        context.logger.error(f'GET request failed: {str(e)}')
        raise


@then("the status code should be (?P<code>.+)")
def step_impl(context, code):
    actual_code = context.response.status_code
    context.logger.info(f'Response status code: {actual_code}')
    assert actual_code == int(code), f"Expected status code {code} but received {actual_code}"


@given("I use POST_request to call the (?P<endpoint>.+) with '(?P<payload>.+)'")
def step_impl(context, endpoint, payload):
    headers = {"Content-Type": "application/json"}
    try:
        context.response = requests.post(endpoint, data=json.dumps(payload), headers=headers)
        context.logger.info(f'POST request to {endpoint} with payload: {payload}')
    except requests.exceptions.RequestException as e:
        context.logger.error(f'POST request failed: {str(e)}')
        raise
