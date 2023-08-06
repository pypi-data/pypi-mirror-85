class events:
    def __init__(self):
        self.list = []


class expressions:
    def __init__(self):
        self.list = []


class mention:
    def __init__(self, page_id):
        self.id = page_id


class event:
    def __init__(self, variable):
        self.value = variable
        
        
class expression:
    def __init__(self, variable):
        self.value = variable


class assets():
    """
    assets(filename, mode, encoding): open path.
    """
    def __init__(self, path):
        self.path = path


    def __call__(self, filename, mode, encoding = None):
        return open(file = self.path + filename, mode = mode, encoding = encoding)


class object_handler_resource:
    from_id = ['deleter_id', 'liker_id', 'user_id']
    peer_id = ['market_owner_id', 'owner_id', 'object_owner_id', 
                'post_owner_id', 'photo_owner_id', 'topic_owner_id', 
                'video_owner_id', 'to_id'
                ]


package_sample = {
        'id': 0,
        'date': 0,
        'random_id': 0,
        'peer_id': 1,
        'from_id': 1,
        'attachments': [],
        'payload': '',
        'keyboard': {},
        'fwd_messages': [],
        'reply_message': {},
        'action': {},
        'conversation_message_id': '',
        'plugin_type': '',
        'text': [],
        'initial_text': ''
    }


def object_handler(tools, event, obj):
    package = objects.package_sample
    package['peer_id'] = tools.group_id

    for key, value in package.items():
        if key in object_handler_resource.peer_id: 
            package['peer_id'] = value

        if key in object_handler_resource.from_id: 
            package['from_id'] = value

        package[key] = value
    
    package['text'].append(event)
    package['text'].append(tools.getObject("ENDLINE"))
    package['type'] = getattr(tools.events, event)

    return package