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
    context.response = requests.get(endpoint, headers=headers)


@then("the status code should be (?P<code>.+)")
def step_impl(context, code):
    assert context.response.status_code == int(code), f"Expected status code {code} but received {context.response.status_code}"


@given("I use POST_request to call the (?P<endpoint>.+) with '(?P<payload>.+)'")
def step_impl(context, endpoint, payload):
    headers = {"Content-Type": "application/json"}
    context.response = requests.post(endpoint, data=json.dumps(payload), headers=headers)
