from . import objects


expressions = objects.expressions()


def setExpression(name, value = None):
    global expressions
    if not value:
        value = f":::TESTCANARYBOT:{name}:::"

    setattr(expressions, name, objects.expression(value))
    expressions.list.append(name)


setExpression("LOGGER_START", [
    'TESTCANARYBOT 0.7',
    'KENSOI.GITHUB.IO 2020', ''
])
setExpression("SESSION_START", "started")
setExpression("SESSION_LONGPOLL_START", "connected")
setExpression("SESSION_LONGPOLL_ERROR", "is not connected [LongpollError Exception]")
setExpression("SESSION_CLOSE", "session closed")
setExpression("SESSION_LISTEN_START", "listenning is started")
setExpression("SESSION_LISTEN_CLOSE", "listenning is finished")

setExpression("ENDLINE")
setExpression("ASSETS_ERROR")

setExpression("MENTION")
setExpression("ACTION")
setExpression("PAYLOAD")

setExpression("NOREACT")
setExpression("PARSER")
setExpression("LIBRARY")
setExpression("LIBRARY_ERROR")
setExpression("LIBRARY_NOSELECT")
setExpression("LIBRARY_PIC")

setExpression("LIBRARY_RESPONSE_ERROR")
setExpression("LIBRARY_RESPONSE_LIST")
setExpression("LIBRARY_RESPONSE_LIST_LINE", "{listitem} {codename} - {name}")
setExpression("LIBRARY_RESPONSE_LIST_ITEM", "\u2022")
setExpression("LIBRARY_RESPONSE_DESCR", "{name}: \n{descr} ")

setExpression("FWD_MES", "forwarded messages")
setExpression("BEEPA_PAPASA", ":::NYASHKA:NYASHKA:::")

setExpression("PLUGIN_INIT", "{} is loading")
setExpression("PLUGIN_FAILED_BROKEN", "{} error: broken {}")
setExpression("PLUGIN_FAILED_ATTRIBUTES", "{} error: check for \"name\", \"description\" and \"version\" attributes")
setExpression("PLUGIN_FAILED_PACKAGETYPE", "{} error: plugin has \"package_handler\" coroutine, but does not have attribute \"packagetype\"")
setExpression("PLUGIN_FAILED_HANDLERS", "{} does not have any handlers. \n\t\tYou can put one of these functions:\n\t\tasync def error_handler(self, tools, package)\n\t\tasync def package_handler(self, tools, package)")
