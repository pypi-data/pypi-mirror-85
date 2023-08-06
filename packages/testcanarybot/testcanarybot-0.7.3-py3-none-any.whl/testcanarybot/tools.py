from datetime import datetime

from . import databases
from . import events
from . import expressions
from . import objects
from . import uploader

import asyncio
import io
import os
import random
import sys

class tools:
    def __init__(self, number, api):
        path = os.getcwd() + '\\assets\\'
        
        self.objects = objects
        self.assets = objects.assets(path)
        self.events = events.events
        self.__objects = expressions
        self.__db = databases.Databases(("canarycore", path + "canarycore.db"))
        self.get = self.__db.get

        self.plugin = "system"
        self.log = self.assets("log.txt", "a+", encoding="utf-8")

        self.group_id = number
        self.api = api
        self.upload = uploader.VkUpload(api, self.assets)

        asyncio.get_event_loop().run_until_complete(self.__setShort())

        self.group_mention = f'[club{self.group_id}|@{self.group_address}]'
        self.mentions = [self.group_mention]
        self.mentions_name_cases = []


        for print_test in self.getObject("LOGGER_START").value:
            print(print_test, 
                file = self.log
                )
                
        self.log.flush()

        self.name_cases = ['nom', 'gen', 'dat', 'acc', 'ins', 'abl']
        self.selfmention = {
            'nom': 'я', 
            'gen': 'меня', 'gen2': 'себя',
            'dat': 'мне', 'dat2': 'себе',
            'acc': 'меня', 'acc2': 'себя',
            'ins': 'мной', 'ins2': 'собой',
            'abl': 'мне', 'abl2': 'себе',
        }
        self.submentions = {
            'all': 'всех',
            'him': 'его',
            'her': 'её',
            'it': 'это',
            'they': 'их',
            'them': 'их',
            'us': 'нас',
            'everyone': '@everyone', 'everyone2': '@all', 'everyone3': '@все'
        }

    
    async def __setShort(self):
        self.group_address = (await self.api.groups.getById(group_id=self.group_id))[0]['screen_name']


    def system_message(self, textToPrint:str):
        response = f'@{self.group_address}.{self.plugin}: {textToPrint}'

        print(response)
        print(f"{self.getDateTime()} {response}", file=self.log)

        self.log.flush()


    def random_id(self):
        if not hasattr(self, "random") or self.random == 999999:
            self.random = 0

        else:
            self.random += 1

        return self.random


    def ischecktype(self, checklist, checktype):
        for i in checklist:
            if isinstance(checktype, list) and type(i) in checktype:
                return True
                
            elif isinstance(checktype, type) and isinstance(i, checktype): 
                return True
            
        return False


    def getDate(self, time = datetime.now()):
        return f'{"%02d" % time.day}.{"%02d" % time.month}.{time.year}'
    
    
    def getTime(self, time = datetime.now()):
        return f'{"%02d" % time.hour}:{"%02d" % time.minute}:{"%02d" % time.second}'


    def getDateTime(self, time = datetime.now()):
        return self.getDate(time) + ' ' + self.getTime(time)


    def setObject(self, nameOfObject: str, newValue):
        self.__objects.setExpression(nameOfObject, newValue)
        self.update_list()


    def getObject(self, nameOfObject: str):
        return getattr(self.__objects.expressions, nameOfObject)


    def update_list(self):
        self.expression_list = self.__objects.expressions.list


    def add(self, db_name):
        self.__db.add((db_name, self.assets.path + db_name))


    async def getMention(self, page_id: int, name_case = "nom"):
        if name_case == 'link':
            if page_id > 0:
                return f'[id{page_id}|@id{page_id}]'

            elif page_id == self.group_id:
                return self.group_mention

            else:
                test = await self.api.groups.getById(group_id = -page_id)
                return await f'[club{-page_id}|@{test[0]["screen_name"]}]'
        
        else:
            if page_id > 0:
                request = await self.api.users.get(
                    user_ids = page_id, 
                    name_case = name_case
                    )
                first_name = request[0]["first_name"]
                
                return f'[id{page_id}|{first_name}]'
            
            elif page_id == self.group_id:
                return self.selfmention[name_case]
            
            else:
                request = await self.api.groups.getById(
                    group_id = -page_id
                    )
                name = request[0]["name"]
                
                return f'[club{-page_id}|{name}]' 


    async def getManagers(self, group_id: int):
        lis = await self.api.groups.getMembers(group_id = group_id, sort = 'id_asc', filter='managers')
        return [i['id'] for i in lis['items'] if i['role'] in ['administrator', 'creator']]


    async def isManager(self, from_id: int, group_id: int):
        return from_id in await self.getManagers(group_id)


    async def getChatManagers(self, peer_id: int):
        res = await self.api.messages.getConversationsById(peer_ids = peer_id)
        res = res['items'][0]['chat_settings']
        response = [*res['admin_ids'], res['owner_id']]
        return response
        

    def isChatManager(self, from_id, peer_id: int):
        return from_id in self.getChatManagers(peer_id)


    async def getMembers(self, peer_id: int):
        response = await self.api.messages.getConversationMembers(peer_id = peer_id)
        return [i['member_id'] for i in response['items']]


    async def isMember(self, from_id: int, peer_id: int):
        return from_id in await self.getMembers(peer_id)


    def parse_mention(self, mention):
        response = mention.replace(mention[mention.find('|'):], '')

        response = response.replace('id', '')
        response = response.replace('club', '-')
        response = response.replace('public', '-')
            
        return self.objects.mention(int(response))


    def parse_link(self, link):
        response = link

        response.replace('https://', '')
        response.replace('http://', '')
        
        return response
