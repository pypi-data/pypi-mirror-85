import requests




def serverStatus():
    request = requests.request("GET", "https://api.2b2t.dev/status")
    return request.json()

def prioqLength():
    request = requests.request("GET", "https://api.2b2t.dev/prioq")
    return request.json()