import requests


class player():

    def __init__(self, username):
        self.username = username

    def info(self):
        self.request = requests.request("GET", f"https://api.2b2t.dev/stats?username={self.username}")
        return self.request.json()

    def lastSeen(self):
        self.request = requests.request("GET", f"https://api.2b2t.dev/seen?username={self.username}")
        return self.request.json()
    
    def lastDeath(self):
        self.request = requests.request("GET", f"https://api.2b2t.dev/stats?lastdeath={self.username}")
        return self.request.json()

    def lastKill(self):
        self.request = requests.request("GET", f"https://api.2b2t.dev/stats?lastkill={self.username}")
        return self.request.json()


