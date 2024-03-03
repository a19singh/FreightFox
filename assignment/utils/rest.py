import requests

def rest_helper(url, params={}, body={}, headers={}):
    """
    Utility for external rest apis.
    """
    # Verify false is added as the setup is hosted on localhost
    response = requests.request("GET", url, params=params, headers=headers, data=body, verify=False)
    return response.json()

