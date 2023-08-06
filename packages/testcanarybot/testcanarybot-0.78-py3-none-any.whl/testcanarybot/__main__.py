import argparse
import os
copy_sample = """
class Main(object):
    async def start(self, tools): 
        # important attributes:
        self.name = \"\"\"testcanarybot plugin\"\"\"
        self.version = 0.7
        self.description = \"\"\"plugin descr\"\"\"
        
        # important to exist if function package_handler exists at this object
        self.packagetype = [
            # tools.events.MESSAGE_NEW,
            # tools.events.LIKE_ADD,
            # tools.events.LIKE_REMOVE

            # list of all types you can find via tools.events.list_of_types
        ]

    # async def package_handler(self, tools, package):
    #     # if you want to parse packages
    #     # if you resulted truly, please run method tools.finish(*list_of_args)
    #     # list_of_args can be empty
    #     # send descr --> return tools.getObject("LIBRARY"), "sampleplugin"
    #     PS look an example after guides at 118th line


    # async def error_handler(self, tools, package):
    #     # if you want to handle Exceptions of testcanarybot, for example, tools.getObject("NOREACT")
    #     return None

    # TOOLS MODULE GUIDE

    # VARIABLES:

    # tools.events = list of event types
    # tools.expression_list --> list of names of objects. You can you use it to check all values through tools.getObject(name, value)
    # tools.group_id --> identificator of your group
    # tools.group_address --> short address of your group
    # tools.group_mention --> mention of your group via @ + tools.group_address

    # FUNCTIONS:
    # await tools.api --> vkontakte API, for methods look vk.com/dev/methods
    # await tools.upload --> uploader, look example at send_log.py
    # tools.assets(file_name, file_mode, encoding = "utf-8") --> opens files from your folder "assets". similar to open

    # tools.add(db_name) --> add new database from assets
    # tools.get(db_name) --> get database by his name

    # tools.getDate(time = datetime.now()) --> returns date in format mm/dd/yyyy
    # tools.getTime(time = datetime.now()) --> returns time in 24 hour format
    # tools.getDateTime(time = datetime.now()) --> returns tools.getDate + tools.getTime
    
    # tools.system_message(textToPrint: str) --> prints your text into command line and into assets/log.txt
    
    # tools.random_id() --> returns integer from interval from 0 to 999999
    
    # await tools.getMention(page_id: int, name_case = "nom") --> returns a mention. for name_case look tools.name_cases
    # await tools.getManagers(group_id: int) --> get administators and owner from selected group
    # await tools.isManager(from_id: int, group_id: int) --> check if it is admin of selected group
    # await tools.getChatManagers(peer_id: int) --> get administators and owner from selected chat
    # await tools.isChatManager(peer_id: int, from_if: int) --> check for rights at selected chat 
    # await tools.getMembers(peer_id: int) --> get members of selected chat
    # await tools.isMember(from_id: int, peer_id: int) --> check if it is member of this chat
    # tools.ischecktype(checklist: list, checktype: list or type object) --> check if this list have types from checktype
    # tools.setObject(nameOfObject: str, newValue) --> set object by finding him by his name
    # tools.getObject(nameOfObject: str) --> find object by his name

    # TOOLS.ASSETS MODULE GUIDE

    # so assets object works like open
    # for example, log file you can open by this method:
    # await tools.assets("log.txt", mode = "r+", encoding = "utf-8")

    # await tools.UPLOAD MODULE GUIDE

    # await tools.upload.photo(self, photos, album_id,
            # latitude=None, longitude=None, caption=None, description=None,
            # group_id=None)
    # await tools.upload.photo_messages(self, photos, peer_id=None)
    # await tools.upload.photo_group_widget(self, photo, image_type)
    # await tools.upload.photo_profile(self, photo, owner_id=None, crop_x=None, crop_y=None,
            # crop_width=None)
    # await tools.upload.photo_chat(self, photo, chat_id)
    # await tools.upload.photo_wall(self, photos, user_id=None, group_id=None, caption=None)
    # await tools.upload.photo_market(self, photo, group_id, main_photo=False,
            # crop_x=None, crop_y=None, crop_width=None)
    # await tools.upload.photo_market_album(self, photo, group_id)

    # await tools.upload.audio(self, audio, artist, title)

    # await tools.upload.video(self, video_file=None, link=None, name=None, description=None,
            # is_private=None, wallpost=None, group_id=None,
            # album_id=None, privacy_view=None, privacy_comment=None,
            # no_comments=None, repeat=None)

    # await tools.upload.document(self, doc, title=None, tags=None, group_id=None,
            # to_wall=False, message_peer_id=None, doc_type=None)

    # await tools.upload.document_wall(self, doc, title=None, tags=None, group_id=None)
    # await tools.upload.document_message(self, doc, title=None, tags=None, peer_id=None)

    # await tools.upload.audio_message(self, audio, peer_id=None, group_id=None)

    # await tools.upload.graffiti(self, image, peer_id=None, group_id=None)
    # await tools.upload.photo_cover(self, photo, group_id,
            # crop_x=None, crop_y=None,
            # crop_x2=None, crop_y2=None)

    # await tools.upload.story(self, file, file_type, add_to_news=True, user_ids=None,
            # reply_to_story=None, link_text=None,
            # link_url=None, group_id=None):
            # 

    # PACKAGE HANDLER EXAMPLE:

    # async def package_handler(self, tools, package):
    #     if package['text'][0] == 'string': # checking for string
    #         if package['text'][1] == tools.getObject("ENDLINE"): # end of line
    #             await tools.api.messages.send(
    #                 random_id = tools.random_id(), 
    #                 peer_id = package['peer_id'], 
    #                 message = 'Hello World!'
    #                 )
    #             return 1 # if you don't want to get error after sending

    #     elif package['text'][0] in ['list', 'of', 'strings']: # checking for list
    #         if package['text'][1] == tools.getObject("ENDLINE"): # end of line
    #             await tools.api.messages.send(
    #                 random_id = tools.random_id(), 
    #                 peer_id = package['peer_id'], 
    #                 message = 'Hello World!'
    #                 )
    #             tools.finish() # if you don't want to get error after sending
    #             # show descr --> tools.finish(
    #             #                   tools.getObject("LIBRARY"), 
    #             #                   "name of your package/module, for example canarycore"
    #             # )

    #     elif package['text'][0] == 'sendhelp':
    #         if package['text'][1] == tools.getObject("ENDLINE"):
    #             return tools.getObject("LIBRARY"), "sampleplugin"


    #     elif package['text'][0] == 'sendtest':
    #         if package['text'][1] == tools.getObject("ENDLINE"):
    #             img = await tools.upload.photo_messages(
    #                 photos = "test.jpg", 
    #                 peer_id = package['peer_id']
    #                 )
                    
    #             images = ", ".join(["photo{owner_id}_{id}".format(**i) for i in img])

    #             await tools.api.messages.send(
    #                 random_id = tools.random_id(), 
    #                 peer_id = package['peer_id'],
    #                 attachment = images
    #                 )

    #             return 1          



"""
parser = argparse.ArgumentParser(description='manager for testcanarybot')
parser.add_argument("--copy_sample", type = bool, default = False, help='copy a sample project to your library folder')

args = parser.parse_args()

if args.copy_sample:
    try:
        os.mkdir(os.getcwd() + '\\library\\sampleplugin')
    except:
        pass

    with open(os.getcwd() + '\\library\\sampleplugin\\main.py', mode="w+") as new_file:
        new_file.write(copy_sample)
    test = os.getcwd() + '\\library\\sampleplugin\\main.py'
    print(f"Executed! [{test}]")

