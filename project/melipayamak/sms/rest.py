from flask import jsonify

import requests


class Rest:
    PATH = "https://rest.payamak-panel.com/api/SendSMS/%s"

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def post(self, url, data):
        data['username'] = self.username
        data['password'] = self.password
        r = requests.post(url, data)
        return r.json()

    def get_data(self):
        return {
            'username': self.username,
            'password': self.password
        }

    def send(self, to, _from, text, isFlash=False):
        url = self.PATH % ('SendSMS')
        data = {
            'to': to,
            'from': _from,
            'text': text,
            'isFlash': isFlash
        }
        return self.post(url, data)

    def send_force(self,_from,to, text,bodyId):
        url = self.PATH % ('BaseServiceNumber')
        data = {
            'from': _from,
            'to': to,
            'text': text,
            'bodyId': bodyId
        }
        return self.post(url, data)

    def is_delivered(self, recId):
        url = self.PATH % ('GetDeliveries2')
        data = {
            'recId': recId
        }
        return self.post(url, {data,self.get_data()})

    def get_messages(self, location, index, count, _from=''):
        url = self.PATH % ('GetMessages')
        data = {
            'location': location,
            'index': index,
            'count': count,
            'from': _from
        }
        return self.post(url, {data,self.get_data()})

    def get_credit(self):
        url = self.PATH % ('GetCredit')
        return self.post(url, self.get_data())

    def get_base_price(self):
        url = self.PATH % ('GetBasePrice')
        return self.post(url, self.get_data())

    def get_numbers(self):
        url = self.PATH % ('GetUserNumbers')
        return self.post(url, self.get_data())
