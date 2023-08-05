import os
import json
import requests
import time
import logging


def auth_cookie():
    sst = super_secured_token()
    temp_token = temporary_token(sst)
    return temp_token


def get_username():
    if os.getenv('GOODDATA_USER') is None:
        raise ValueError(
            "Please set your env var GOODDATA_USER"
        )
    else:
        return os.getenv('GOODDATA_USER')


def get_password():
    if os.getenv('GOODDATA_PASSWORD') is None:
        raise ValueError(
            "Please set your env var GOODDATA_PASSWORD"
        )
    return os.getenv('GOODDATA_PASSWORD')


def get_useragent():
    return "PyGyver-ETL/1.0"


def super_secured_token():

    """
    Sends username and password to POST requests
    verify_level - 0: HTTP Cookie, use GDCAuthSST in header
                 - 2: customHTTP header, use X-GDC-AuthSST in header (selected)

    Returns
    -------
        sst (string) - SuperSecured Token

    """

    url = os.getenv('GOODDATA_DOMAIN') + "/gdc/account/login/"
    values = json.dumps({"postUserLogin": {"login": get_username(),
                                           "password": get_password(),
                                           "remember": 1,
                                           "verify_level": 2
                                           }
                         })
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "User-Agent": get_useragent(),
    }

    response = requests.post(
        url=url,
        data=values,
        headers=headers
    )

    # Check response's Status Code
    if 200 <= response.status_code < 300:
        content = json.loads(response.content)
        sst_cookie = response.headers['X-GDC-AuthSST']
    else:
        raise ValueError(json.loads(response.content))

    return sst_cookie


def temporary_token(sst):

    """
    Include the returned TT (Temporary Token) when making API calls
    to the GoodData Platform.

    The TT is valud for a short period of time. If you receive status code
    401 (Unauthorized) while calling any API resource, get a new TT -- the
    SST must still be valid, which can be specified by the 'remember' option.

    Parameters
    ----------
    sst (string)

    Returns
    -------

    """

    url = os.getenv('GOODDATA_DOMAIN') + "/gdc/account/token/"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "User-Agent": get_useragent(),
        "X-GDC-AuthSST": sst
    }

    response = requests.get(
        url=url,
        headers=headers
    )

    # Check response's Status Code
    if 200 <= response.status_code < 300:
        content = json.loads(response.content)
        temp_token = content['userToken']['token']
    else:
        raise ValueError(response.content)

    return temp_token
def get_header():
    header = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "User-Agent": get_useragent(),
        "X-GDC-AuthTT": auth_cookie()
    }
    return header

def execute_schedule(schedule_id, retry=False):
    """ Executes GoodData schedule.

    Parameters:
        - schedule_id (string): The ID of the GoodData schedule you want to execute.
        - retry (boolean): If True, applies the reschedule property if the schedule has it set. When not set, defaults to False.

    Required:
        - GOODDATA_DOMAIN   - Usually http://reports.made.com
        - GOODDATA_PROJECT  - The GoodData Project ID
        - GOODDATA_USER     - The login credentials for GoodData Report
        - GOODDATA_PASSWORD - The login credentials for GoodData Report

    Returns:
        - URI link to schedule execution.

    Usage:
        - execute_schedule(a1bc3xyz, retry=True)
    """

    if os.getenv('GOODDATA_DOMAIN') is None:
        raise ValueError(
            "Please set your env var GOODDATA_DOMAIN"
        )

    if os.getenv('GOODDATA_PROJECT') is None:
        raise ValueError(
            "Please set your env var GOODDATA_PROJECT"
        )

    values = json.dumps({
        "execution": {
            "params": {
                "retry": str(retry).lower()
            }
        }
    })

    api_url = os.getenv('GOODDATA_DOMAIN') + "/gdc/projects/" + os.getenv('GOODDATA_PROJECT') + "/schedules/" + schedule_id + "/executions"

    response = requests.post(
        url=api_url, 
        data=values,
        headers=get_header()
    )

    if 200 <= response.status_code < 300:
        content = json.loads(response.content)
        uri = os.getenv('GOODDATA_DOMAIN') + content['execution']['links']['self']
        while True:
            response = requests.get(
                url=uri,
                headers=get_header()
            )   
            content = json.loads(response.content)
            status = content['execution']['status']
            if status in ['RUNNING', 'SCHEDULED']:
                logging.info("Graph has not completed, entering sleep for 15 seconds")
                time.sleep(15)
            elif status == 'OK':
                logging.info('Graph completed with a OK status')
                return status
            else:
                logging.info('Graph completed with a non OK status')
                raise ValueError(status)
    else:
        raise ValueError(json.loads(response.content))
