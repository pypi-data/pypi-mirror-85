import random


class Main(object):

    library_response = "Библиотека, с которой работает {mention}:\n\n{plugins}\n\n Чтобы получить описание модуля, отправьте {mention} ассеты описание [название модуля]"

    async def start(self, tools):
        self.version = 0.7
        self.name = """canarycore"""
        self.description = """Модуль для управления системой testcanarycore версии 0.6
            {group_mention} плагины описание [ссылка на модуль без пробелов] - показать описание модуля
            {group_mention} плагины - показать библиотеку testcanarybot
            {group_mention} выполнить + [пересланные сообщения] - выполнить сообщения
            """.format(group_mention = tools.group_mention)
        self.packagetype = [
                    tools.events.MESSAGE_NEW
                ]
            
        self.assets = simple()
        self.assets.commands = simple()
        self.assets.commands.standart = [
            "модули", "модуль",
            "modules", "module",
            ]
        self.assets.commands.descr = [
            "описание", "оп", 
            "description", "descr"
            ]

        self.parser = simple()
        self.parser.run = [
            "выполнить", "run"
            ]
        self.parser.command = [
            "команду", "command"
            ]


    async def package_handler(self, tools, package):
        if package["text"][0] == "управление":
            return tools.getObject("LIBRARY"), "canarycore"

        if package["text"][0] in self.assets.commands.standart:
            if package["text"][1] in self.assets.commands.descr:

                # @canarybot plugins description

                if package["text"][2] == tools.getObject("ENDLINE"):
                    await tools.api.messages.send(
                        random_id = tools.random_id(), 
                        peer_id = package["peer_id"], 
                        message=tools.getObject("ASSETS_ERROR").value.format(
                            mention = tools.group_mention
                            )
                        )

                    return 1

                elif package["text"][3] == tools.getObject("ENDLINE"):

                    return tools.getObject("LIBRARY"), package["text"][2]
                    
            elif package["text"][1] == tools.getObject("ENDLINE"):

                # @canarybot plugins

                return tools.getObject("LIBRARY"), tools.getObject("LIBRARY_NOSELECT")

        elif package["text"][0] in self.parser.run and package["text"][1] is tools.getObject("ENDLINE"):
            
            # @canarybot run
            # + forwarded messages

            response = [
                tools.getObject("PARSER")
                ]

            if "fwd_messages" in package: response.extend(package["fwd_messages"])
            if "reply_message" in package: response.append(package["reply_message"])

            response.append(tools.getObject("ENDLINE"))

            return response


    async def error_handler(self, tools, package):
        if package["text"][0] == tools.getObject("LIBRARY"):
            response = "response"

            if type(package["text"][1]) is list: # RESPONSED A LIST OF PLUGINS FROM LIBRARY
                response_list = []
                for i in package["text"][1]:
                    codename, name = i
                    response_list.append(tools.getObject("LIBRARY_RESPONSE_LIST_LINE").value.format(
                        listitem = tools.getObject("LIBRARY_RESPONSE_LIST_ITEM").value,
                        codename = codename,
                        name = name
                    ))

                response = self.library_response.format(
                        plugins = '\n'.join(response_list),
                        mention = tools.group_mention
                    )



            elif package["text"][1] == tools.getObject("LIBRARY_ERROR"): # NO PLUGIN FOUND
                response = tools.getObject("LIBRARY_RESPONSE_ERROR").value

            else: # RESPONSED DESCRIPTION
                response = package["text"][3].format(listitem = tools.getObject("LIBRARY_RESPONSE_LIST_ITEM").value)

            await tools.api.messages.send(
                random_id = tools.random_id(), 
                peer_id = package["peer_id"], 
                message = response, 
                attachment = tools.getObject("LIBRARY_PIC").value
                )


    async def command_handler(self, tools, package):
        if 'action' in package:
            package['text'] = self.parse_action(package['action'])
            return package

        elif 'payload' in package:
            package['text'] = self.parse_payload(package['payload'])
            return package

        elif 'text' in package:
            if package['text'] != '':
                package['text'] = self.parse_message(package['text'])
                
                if package['text'][0] != self.tools.getObject("ENDLINE"):
                    return package


    # async def command_handler(self, tools, package):
    #     # if you want to parse message text before parsing in package_handler in all plugins
    #     return package


    def parse_message(self, messagetoreact):
        for i in self.tools.expression_list:
            value = self.tools.getObject(i).value

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


class simple:
    pass