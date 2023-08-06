from .plugins import plugins
from . import exceptions


import aiohttp
import atexit
import asyncio
import json
import logging
import os
import random
import threading
import time
import traceback
import six

os.mkdir(os.getcwd() + '\\assets\\')
os.mkdir(os.getcwd() + '\\library\\')

supporting = [0.7]

class application():    
    __RPS_DELAY = 1 / 20.0
    headers = {
            'User-agent': 'Mozilla/5.0 (Windows NT 6.1; rv:52.0) '
                            'Gecko/20100101 Firefox/52.0'
        }

    def __init__(self, token: str, group_id: int, api_version='5.126'):
        """
        Token = token you took from VK Settings: https://vk.com/{yourgroupaddress}?act=tokens
        group_id = identificator of your group where you want to install CanaryBot Framework :)
        """
        self.last_request = 0.0

        self.__token = token
        self.__group_id = group_id
        self.api_version = api_version

        self.longpoll = None
        self.http = aiohttp.ClientSession()
        self.api = api(self.http, self.method)
        self.library = plugins(supporting, group_id, self.api)
        
        
        self.loop = asyncio.get_event_loop()
        self.atexit = atexit
        self.atexit.register(self.__close_session)

        text = self.library.tools.getObject('SESSION_START').value
        print(f"\n@{self.library.tools.group_address}: {text}")
        print(f"\n{self.library.tools.getDateTime()} @{self.library.tools.group_address}: {text}", file=self.library.tools.log)
        


    def __close_session(self):
        self.loop.run_until_complete(self.http.close())
        self.library.tools.system_message(self.library.tools.getObject("SESSION_CLOSE").value)
        self.library.tools.log.close()


    async def method(self, method: str, values=None):
        """ Вызов метода API

        :param method: название метода
        :type method: str

        :param values: параметры
        :type values: dict
        """
        data = values if values else dict()

        data['v'] = self.api_version

        data['access_token'] = self.__token
        if 'group_id' in data: data['group_id'] = self.__group_id

        delay = self.__RPS_DELAY - (time.time() - self.last_request)

        if delay > 0:
            await asyncio.sleep(delay)

        response = await self.http.post(
            'https://api.vk.com/method/' + method, 
            data = data, 
            headers = self.headers
        )

        self.last_request = time.time()

        response = await response.json()
        if 'error' in response:
            
            raise TypeError(f"[{response['error']['error_code']}] {response['error']['error_msg']}")

        return response['response']    


    def setMentions(self, *args):
        """
        Use custom mentions instead "@{groupadress}"
        """
        self.library.tools.setObject("MENTIONS", [self.library.tools.group_mention, *args])


    def setNameCases(self, *args):
        """Use custom mentions instead \"@{groupaddress}\""""
        self.library.tools.setObject("MENTION_NAME_CASES", args)


    def getObject(self, string: str):
        self.library.tools.getObject(string)
    

    def setObject(self, string: str, value):
        self.library.tools.setObject(string, value)


    def listen(self, count = None):
        """count: how many packages should take Canarybot. If you don't send this, it takes packages forever"""
        self.library.tools.system_message(self.library.tools.getObject("SESSION_LISTEN_START").value)
        if not count:
            while True:
                self.check()

        else:
            for i in range(count):
                self.check()

            self.library.tools.system_message(self.library.tools.getObject("SESSION_LISTEN_CLOSE").value)


    def installLongpoll(self):
        """set up longpoll application to work with 'library' folder"""

        self.longpoll = longpoll(self.http, self.method, self.__group_id)
        self.library.tools.system_message(self.library.tools.getObject("SESSION_LONGPOLL_START").value)


    def check(self):
        """Check VK for updates once time, like canarybot.listen(1)"""
        self.library.tools.update_list()

        if not self.longpoll:
            raise exceptions.LongpollError(self.library.tools.getObject("SESSION_LONGPOLL_ERROR"))

        response = self.loop.run_until_complete(self.longpoll.check())

        for event in response:
            self.library.send(event)


class longpoll():
    def __init__(self, session, method, group_id):
        self.session = session
        self.method = method
        self.group_id = str(group_id)
        
        self.url = None
        self.key = None
        self.server = None
        self.ts = None

        self.timeout = aiohttp.ClientTimeout(total = 35)

        asyncio.get_event_loop().run_until_complete(self.update_longpoll_server())
        

    async def update_longpoll_server(self, update_ts=True):
        values = {
            'group_id': self.group_id
        }
        response = await self.method('groups.getLongPollServer', values)

        self.key = response['key']
        self.server = response['server']

        self.url = self.server

        if update_ts:
            self.ts = response['ts']


    async def check(self):
        values = {
            'act': 'a_check',
            'key': self.key,
            'ts': self.ts,
            'wait': 25,
        }

        response = await self.session.get(
            self.url,
            params = values,
            timeout = self.timeout
        )
        response = await response.json()

        if 'failed' not in response:
            self.ts = response['ts']
            return response['updates']

        elif response['failed'] == 1:
            self.ts = response['ts']

        elif response['failed'] == 2:
            self.update_longpoll_server(update_ts=False)

        elif response['failed'] == 3:
            self.update_longpoll_server()

        return []

class api(object):
    __slots__ = ('_http', '_method', '_string')

    def __init__(self, http, method, string = None):
        self._http = http
        self._method = method    
        self._string = string


    def __getattr__(self, method):
        if '_' in method:
            m = method.split('_')
            method = m[0] + ''.join(i.title() for i in m[1:])

        self._string = self._string + "." if self._string else ""

        return api(
            self._http, self._method,
            (self._string if self._method else '') + method
        )

    async def __call__(self, **kwargs):
        for k, v in six.iteritems(kwargs):
            if isinstance(v, (list, tuple)):
                kwargs[k] = ','.join(str(x) for x in v)

        return await self._method(self._string, kwargs)