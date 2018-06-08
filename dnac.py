import requests
import json
import time
import logging
from dnac_config import DNAC, DNAC_PORT, DNAC_USER, DNAC_PASSWORD
from requests.auth import HTTPBasicAuth
requests.packages.urllib3.disable_warnings()

# -------------------------------------------------------------------
# Custom exception definitions
# -------------------------------------------------------------------
class TaskTimeoutError(Exception):
    pass

class TaskError(Exception):
    pass

# API ENDPOINTS
ENDPOINT_TICKET = "ticket"
ENDPOINT_TASK_SUMMARY ="task/%s"
RETRY_INTERVAL=2

# -------------------------------------------------------------------
# Helper functions
# -------------------------------------------------------------------
def create_url(path, controller_ip=DNAC):
    """ Helper function to create a DNAC API endpoint URL
    """

    return "https://%s:%s/api/v1/%s" % (controller_ip, DNAC_PORT, path)


def get_auth_token(controller_ip=DNAC, username=DNAC_USER, password=DNAC_PASSWORD):
    """ Authenticates with controller and returns a token to be used in subsequent API invocations
    """

    login_url = "https://{0}:{1}/api/system/v1/auth/token".format(controller_ip, DNAC_PORT)
    result = requests.post(url=login_url, auth=HTTPBasicAuth(DNAC_USER, DNAC_PASSWORD), verify=False)
    result.raise_for_status()

    token = result.json()["Token"]
    return {
        "controller_ip": controller_ip,
        "token": token
    }

def wait_on_task(task_id, token, timeout=(5*RETRY_INTERVAL), retry_interval=RETRY_INTERVAL):
    """ Waits for the specified task to complete
    """

    task_url = create_url(ENDPOINT_TASK_SUMMARY % task_id, token["controller_ip"])

    headers = {
        "x-auth-token": token["token"]
    }
    start_time = time.time()

    while True:
        result = requests.get(url=task_url, headers=headers, verify=False)
        result.raise_for_status()

        response = result.json()["response"]
        #print json.dumps(response)
        if "endTime" in response:
            return response
        else:
            if timeout and (start_time + timeout < time.time()):
                raise TaskTimeoutError("Task %s did not complete within the specified timeout "
                                       "(%s seconds)" % (task_id, timeout))

            print("Task=%s has not completed yet. Sleeping %s seconds..." %(task_id, retry_interval))
            time.sleep(retry_interval)

        if response['isError'] == True:
            raise TaskError("Task %s had error %s" % (task_id, response['progress']))

    return response