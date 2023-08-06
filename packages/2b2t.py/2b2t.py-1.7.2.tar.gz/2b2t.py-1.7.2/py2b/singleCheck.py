import requests
from colorama import Fore, init
import threading

def check(username, printOut=False):
    data = f'ign={username}'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
        }

    request = requests.request('POST', "https://donate.2b2t.org/category/738999", data=data, headers=headers)
    if not printOut:
        if 'rate limited' in request.text:
            return 0
        elif 'not a valid' in request.text:
            return 1
        elif 'Unable' in request.text:
            return 2
        elif 'banned' not in request.text:
            return False
        else:
            return True
    else:
        if 'rate limited' in request.text:
            print(Fore.LIGHTMAGENTA_EX + f"YOU'VE BEEN RATELIMITED!! :(")
        elif 'not a valid' in request.text:
            print(Fore.LIGHTRED_EX + f"{username} is not a valid username")
        elif 'Unable' in request.text:
            print(Fore.LIGHTRED_EX + f"Unable to find a player with the username: {username}")
        elif 'banned' not in request.text:
            print(Fore.LIGHTRED_EX + f"{username} is not currently banned")
        else:
            print(Fore.LIGHTGREEN_EX + f"{username} is currently banned")

