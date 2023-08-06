from .tools import *
import os
import traceback
import importlib
import json
import asyncio

class plugins():
    def __init__(self, v, group_id, api):
        self.loop = asyncio.get_event_loop()

        path = os.getcwd()
        self.tools = tools(group_id, api)

        self.error_handlers = ['canarycore']
        self.package_handlers = self.error_handlers
        self.command_handlers = self.error_handlers

        self.defattr = {
            "error_handler", 
            "package_handler", 
            "command_handler"
            }

        self.needattr = {
            'name',
            'version',
            'description',
        }
        self.supp_v = v
        self.upload()


    def upload(self):
        self.plugins = {}
        self.tools.plugin = "library"
        response = ['canarycore']

        try:
            response.extend(os.listdir(os.getcwd() + '\\library\\'))
            
        except Exception as e:
            self.tools.system_message(e)
        
        for name in ['sampleplugin', '__pycache__']:
            if name in response: response.remove(name)

        self.loop.run_until_complete(asyncio.gather(*[
                                self.pluginload(plugin) for plugin in response
                                ])) 


    async def pluginload(self, plugin):
        if plugin != 'canarycore':
            self.tools.plugin = "library"
            self.tools.system_message(self.tools.getObject("PLUGIN_INIT").value.format(plugin))

            try:
                if plugin.endswith('.py'):
                    pluginObj = getattr(
                        importlib.import_module("library." + plugin[:-3]),
                        "Main")()
                else:
                    pluginObj = getattr(
                        importlib.import_module("library." + plugin + ".main"),
                        "Main")()
                await pluginObj.start(self.tools)

            except Exception as e:
                self.tools.system_message(self.tools.getObject("PLUGIN_FAILED_BROKEN").value.format(e))
                self.all = [i for i in self.all if i != plugin]

                return None
            
            attributes = set(dir(pluginObj))
            if self.needattr & attributes != self.needattr:
                self.tools.system_message(self.tools.getObject("PLUGIN_FAILED_ATTRIBUTES").value)
                return None


            if self.defattr & attributes != {}:
                if plugin.endswith(".py"): plugin = plugin.replace(".py", "")

                if 'package_handler' in attributes:
                    if hasattr(pluginObj, "packagetype"):
                        self.package_handlers.append(plugin)

                    else:
                        self.tools.system_message(self.tools.getObject("PLUGIN_FAILED_PACKAGETYPE").value)

                if 'command_handler' in attributes:
                    self.command_handlers.append(plugin)

                if 'error_handler' in attributes:
                    self.error_handlers.append(plugin)
                    
                self.plugins[plugin] = pluginObj

            else:
                self.tools.system_message(self.tools.getObject("PLUGIN_FAILED_HANDLERS").value)
            

        else:
            from . import core as lib_plugin

            self.tools.system_message(self.tools.getObject("PLUGIN_INIT").value.format("canarycore"))
            
            canarycore = lib_plugin.Main()
            await canarycore.start(self.tools)

            self.plugins[plugin] = canarycore


    def send(self, event):
        event['type'] = event['type'].upper()
        if event['type'] == "MESSAGE_NEW":
            self.parse(event['object']['message'])

        else:
            if event['type'] in self.tools.events.list:
                package = self.tools.objects.object_handler(self.tools, event['type'], event['object'])
                self.parse_package(package)
        

    def parse(self, message):
        message['type'] = self.tools.events.MESSAGE_NEW
        message['initial_text'] = message['text']

        if 'action' in message:
            message['text'] = self.parse_action(message['action'])
            self.parse_package(message)

        elif 'payload' in message:
            message['text'] = self.parse_payload(message['payload'])
            self.parse_package(message)

        elif 'text' in message:
            if message['text'] != '':
                message['text'] = self.parse_command(message['text'])
                
                if message['text'][0] != self.tools.getObject("ENDLINE"):
                    self.parse_package(message)


    def parse_payload(self, messagepayload):
        response = [self.tools.getObject("PAYLOAD")]

        response.append(json.loads(messagepayload))
        response.append(selftools.getObject("ENDLINE"))
        
        return response


    def parse_action(self, messageaction):
        response = [self.tools.getObject("ACTION")]

        response.extend(messageaction.values())
        response.append(self.tools.getObject("ENDLINE"))

        return response


    def parse_command(self, messagetoreact):
        for i in self.tools.expression_list:
            value = self.tools.getObject(i)

            if type(value) is str and value in messagetoreact:
                messagetoreact = messagetoreact.replace(i, 'system_message')

        response = []
        message = messagetoreact.split()

        if len(message) > 1:
            if message[0] in [*self.tools.getObject("MENTIONS").value]:
                message.pop(0)

                for i in message:
                    if i[0] == '[' and i[-1] == ']' and i.count('|') == 1:
                        response.append(self.tools.parse_mention(i[1:-1]))

                    else:
                        response.append(self.tools.parse_link(i))

        elif response == []:
            for word in message:
                if word.lower() in [*self.tools.getObject("MENTIONS").value, 
                                    *self.tools.getObject("MENTION_NAME_CASES").value]: 
                    response.append(self.tools.getObject("MENTION"))

        response.append(self.tools.getObject("ENDLINE"))

        return response


    def getCompactible(self, packagetype):
        for plugin in self.package_handlers:
            if packagetype in self.plugins[plugin].packagetype: yield plugin


    def parse_package(self, package):
        plugins = [asyncio.ensure_future(self.plugins[i].package_handler(self.tools, package)
                ) for i in self.getCompactible(package['type'])]
                
        self.tools.plugin = 'message_handler'
        
        results = self.loop.run_until_complete(
            asyncio.gather(*plugins)
            )

        self.error_handler(package, results)


    def error_handler(self, package, reaction):
        if len(reaction) == 0:
            reaction.append([self.tools.getObject("NOREACT")])

        for i in reaction:
            if isinstance(i, (list, set)):
                if isinstance(i, set): i = list(i)
                package['text'] = i

                try:
                    if package['text'][0] == self.tools.getObject("LIBRARY"):
                        if package['text'][1] == self.tools.getObject("LIBRARY_NOSELECT"):
                            package['text'][1] = [
                                (e, self.plugins[e].name) for e in self.plugins.keys() if e != 'canarycore'
                            ]

                        elif package['text'][1] in self.all:
                            package['text'].append(self.plugins[package['text'][1]].version)
                            package['text'].append(self.plugins[package['text'][1]].description)
                                

                        else:
                            package['text'][1] = self.tools.getObject("LIBRARY_ERROR")

                    elif package['text'][0] == self.tools.getObject("PARSER"):
                        for message in package['text'][1:-1]:
                            message['from_id'] = package['from_id']
                            message['peer_id'] = package['peer_id']

                            if 'fwd_messages' in message: message['fwd_messages'] = None
                            if 'reply_message' in message: message['reply_message'] = None

                            self.parse(message)

                        del package['text'][1:]

                        package['text'].append(self.tools.getObject("FWD_MES"))
                        package['text'].append(self.tools.getObject("ENDLINE"))

                    plugins = [self.loop.create_task(
                            self.plugins[i].error_handler(self.tools, package)
                            ) for i in self.error_handlers]

                    self.loop.run_until_complete(asyncio.wait(plugins))

                except Exception as e:
                    self.tools.system_message(traceback.format_exc())

        self.tools.system_message(f"chat{package['peer_id']}-{package['from_id']}: {package['text'][:-1]}")
        

        

