# -*- coding: utf-8 -*-

import demjson
import httplib
import base64
import pytils

class Gate:
    
    def __init__(self, host, username, password):
        host = host.replace('http://', '')
        if host.find(':')!=-1:
            self.port = int(host[host.find(':')+1:])
            host = host[:host.find(':')]
        else:
            self.port = 80
        self.host = host
        self.username = username
        self.password = password
    
    def _sendRequest(self, body, method):
        connection = httplib.HTTPConnection(host = self.host, port = self.port)
        if 'text' in body:
            body['text'] = pytils.translit.translify(body['text'])
        req = demjson.encode(body)
        connection.request("POST", "/api/gate/%s/" % method, req)
        data = connection.getresponse().read()
        try:
            return demjson.decode(data)
        except demjson.JSONDecodeError:
            f = open('/home/entropius/GTD/job/ika/special_recordbook/gate-error.html', 'w')
            f.write(data)
            f.close()
            raise
    
    def checkUser(self, phone):
        body = {'schoolID': self.username, 'schoolAccessKey': self.password}
        body['phone'] = phone
        req = self._sendRequest(body, 'checkUser')
        return req['exists']
    
    def addUser(self, phone):
        '''
            Добавление пользователя, возращает его id
        '''
        body = {'schoolID': self.username, 'schoolAccessKey': self.password}
        body['phone'] = phone
        req = self._sendRequest(body, 'addUser')
        if 'id' in req: return req['id']
    
    def deleteUser(self, id):
        '''
            Удаление пользователя
        '''
        body = {'schoolID': self.username, 'schoolAccessKey': self.password}
        body['id'] = id
        self._sendRequest(body, 'deleteUser')
    
    def getBalance(self, id):
        body = {'schoolID': self.username, 'schoolAccessKey': self.password}
        body['id'] = id
        return self._sendRequest(body, 'getBalance')
    
    def changePhone(self, id, phone):
        body = {'schoolID': self.username, 'schoolAccessKey': self.password}
        body['id'] = id
        body['phone'] = phone
        self._sendRequest(body, 'changePhone')
    
    def getPaymentInfo(self):
        body = {'schoolID': self.username, 'schoolAccessKey': self.password}
        return self._sendRequest(body, 'getPaymentInfo')

    def sendMessage(self, id, text):
        body = {'schoolID': self.username, 'schoolAccessKey': self.password}
        body['id'] = id
        body['text'] = text
        self._sendRequest(body, 'sendMessage')
    
    
        