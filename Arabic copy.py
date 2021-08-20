# import the libraries
from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
# Responses file is a file that have some handleMessage
import Responses as responses
import profile as personal_info

# OPEN The file that include the api id and api hash
Password = open("PassWord.txt", "r")
api_id = Password.readline().split()[1]
api_hash = Password.readline().split()[1]

# Define the bot id
BOT_ID = 1779607655
# Make a boss id which is mine
BOSS_ID_1 = 477758182
BOSS_ID_2 = 896399150

# Make a client named Bot
bot = Client("Bot", api_id, api_hash)


# define a start command
@bot.on_message(filters.command(["start", "start@ABDULMOHSEEN_2_bot"]))
def start(self, message):
    message.reply("Hi! \n The bot is running")

# send a message with a new person
@bot.on_message(filters.new_chat_members)
def new_person(self, message):
    chat_id = message['chat']['id']
    self.send_message(chat_id, "أهلا وسهلا نورت القروب")


# define the help command
@bot.on_message(filters.command(["help", "help@ABDULMOHSEEN_2_bot"]))
def help_message(self, message):
    # print the list of Tasks
    message.reply("Here is the function that I can do..\n"
                  "1- /start - Check if the bot is running\n\n"
                  "2- /my_ID - Get your id number\n\n"
                  "3- /ID - you have to mention someone than you will get his ID number\n\n"
                  "4- /addR - for add some response\n\n"
                  "5- /Ans - to show all response\n\n"
                  "6- /profile_form - Take the form to make your own profile\n\n"
                  "7- /response_form - the correct form to write the response\n\n"
                  )


# define a response message to show all responses
@bot.on_message(filters.command(["Ans", "Ans@ABDULMOHSEEN_2_bot"]))
def get_the_response(self, message):
    # TAKE ALL The info and make it as a list than print the key of the list
    response_local = []
    # open the file
    input_file = open("archives.txt", "r")
    # read info
    lines = input_file.readlines()
    input_file.close()
    counter = 1
    for line in lines:
        line = line.split("*")
        target = "{}- ".format(counter) + line[0]
        response_local.append(target)
        counter += 1
        # change the format
    response_local = (str(response_local).replace(",", "\n")).replace("[", "")
    response_local = (str(response_local).replace(",", "\n")).replace("]", "")
    response_local = (str(response_local).replace(",", "\n")).replace("'", "")
    # print the output
    message.reply(response_local)


# define an ID command to get the user id
@bot.on_message(filters.command(["my_ID", "my_ID@ABDULMOHSEEN_2_bot"]))
def id_reply(self, message):
    # if the user have a username so print it
    if message.from_user.username is not None:
        message.reply(f"The person who's username is @{message.from_user.username} his ID is: {message.from_user.id}")
    else:
        # if it doesn't have so make a mention by his name
        message.reply(f"The person who's username is {message.from_user.mention()} his ID is: {message.from_user.id}")


# get the id for any person in group
@bot.on_message(filters.command("id"))
def get_id(self, message):
    try:
        ID = message['reply_to_message']['from_user']['id']
        # if the user have a username so print it
        if message.reply_to_message.from_user.username is not None:
            message.reply(
                f"The person who's username is @{message.reply_to_message.from_user.username} his ID is: {ID}")
        else:
            # if it doesn't have so make a mention by his name
            message.reply(f"The person who's username is {message.reply_to_message.from_user.username} his ID is: {ID}")
    except TypeError:
        # if there are no mention print this message
        message.reply("You have to mention someone")


# this function is for take the information from the profile
@bot.on_message(filters.command("info"))
def get_profile(self, message):
    # take the name from the user and split it to make it just a single name
    text = str(message["text"]).split()
    text.pop(0)
    name = str(text[0]).lower()
    # take the information from the output file
    information = personal_info.read_info()
    # check which line to print
    check = True
    for line in information:
        # take each line in the information nad make it in the correct form
        line = line.split(",")
        if name in line[1].lower():
            sol = str(line).replace(",", "\n")
            sol = sol.replace("[", "")
            sol = sol.replace("]", "")
            sol = sol.replace("'", "")
            sol = sol.rstrip("\ n")
            # finally print it
            check = False
            message.reply(sol)
    if check:
        # if the name is not found print this
        message.reply("Not Found")




@bot.on_message(filters.command("profile"))
def profile(self, message):
    text = message.text.split("\n")
    user_id = message.from_user.id
    profile = personal_info.sample_responses(text, user_id)
    message.reply(profile)


# define archives to add a new responses
@bot.on_message(filters.command(["addR", "addR@ABDULMOHSEEN_2_bot"]))
def archives(self, message):
# if message.from_user.id == BOSS_ID:
    # take the text
    text = message.text
    # split by each line
    text = text.split("\n")
    # delete the key word
    text.pop(0)
    # check the len
    if len(text) == 2:
        # check the key
        check = check_archives(text[0])
        if not check:
            input_file = open("archives.txt", "a")
            # make the text as a dictionary and write it
            dictionary = "{}*{}\n".format(text[0], text[1])
            input_file.write(str(dictionary))
            message.reply("تمت اضافة الرد")
        else:
            message.reply("The key is already exiting")
    else:
        message.reply("You have to write in the specific form (/response_form)")
# else:
# message.reply("Just the Boss can do it")


# make a function to delete a response
@bot.on_message((filters.command(["deleteR", "deleteR@ABDULMOHSEEN_2_bot"])))
def delete_response(self, message):
    check = check_boss(message.from_user.id)
    chat_id = message.chat.id
    if check:
        # get the message text
        text = message.text
        # split by line
        text = text.split("\n")
        # pop the command word
        text.pop(0)
        check = check_archives(text[0])
        if check:
            input_file = open("archives.txt", "r")
            # read info
            lines = input_file.readlines()
            input_file.close()
            dictionary = {}
            for line in lines:
                line = line.split("*")
                dictionary[line[0]] = line[1].rstrip("\n")
            for key, value in dictionary.items():
                if key.lower() == text[0].lower():
                    dictionary.pop(key)
                    break
            input_file = open("archives.txt", "w")
            for key, value in dictionary.items():
                target = "{}*{}\n".format(key,value)
                input_file.write(str(target))
            message.reply("تم حذف الرد")
        else:
            message.reply("Not Found")
    else:
        message.reply("Just the boss can do it")


@bot.on_message(filters.command("pin"))
def pin_message(self, message):
    chat_id = message.chat.id
    message_id = message.reply_to_message.message_id
    self.pin_chat_message(chat_id, message_id)


@bot.on_message(filters.command("Unpin"))
def unpin_message(self, message):
    chat_id = message.chat.id
    message_id = message.reply_to_message.message_id
    self.unpin_chat_message(chat_id, message_id)


def edit_bot_message(self, message):
    chat_id = message.chat.id
    message_id = message.reply_to_message.message_id
    self.edit_message_text(chat_id, message_id, text="Sorry")

# this is a command to print the profile form
@bot.on_message(filters.command(["profile_form", "profile_form@ABDULMOHSEEN_2_bot"]))
def profile_form(self, message):
    message.reply("This is the form for profile\n"
                  "\n###########\n"
                  "/profile\n"
                  "Name\n"
                  "Major\n"
                  "Year\n"
                  "###########\n"
                  "\nYou have to replace each one by your information\nLike this:\n"
                  "\n########\n"
                  "/profile\n"
                  "Abdulmohseen\n"
                  "SWE\n"
                  "2020\n")


# define a function that give the form to add a new response
@bot.on_message(filters.command(["response_form", "response_form@ABDULMOHSEEN_2_bot"]))
def response_form(self, message):
    message.reply("This is the correct form to make a new response\n\n"
                  "/addR\n"
                  "key_word\n"
                  "The response\n"
                  "\n For example:\n\n"
                  "/addR\n"
                  "book\n"
                  "The meaning of the book is...\n")


# function for raed the message
@bot.on_message(filters.command("readMessage"))
def readMessage(self, message):
    print(message)
    message.reply(message)



# for block the user
def block(self, message):
    # let the boss do this order
    check = check_boss(message.from_user.id)
    if check:
        # take the user id and chat id
        try:
            chat_id = message.chat.id
            user_id = message.reply_to_message.from_user.id
            if user_id == BOT_ID:
                message.reply("You try to kick me?")
                self.kick_chat_member(chat_id, message.from_user.id)
            else:
                if message.reply_to_message.from_user.username is not None:
                    self.send_message(chat_id, "The person who is named @{} has been kicked".format(message.reply_to_message.from_user.username))
                    self.kick_chat_member(chat_id, user_id)
                else:
                    self.send_message(chat_id, "The person who is named {} has been kicked".format(message.reply_to_message.from_user.mention()))
                    self.kick_chat_member(chat_id, user_id)
        except:
            message.reply("You must mention someone-kick")
    else:
        message.reply("Just the boss can kick")


# make a function that will add a new boss in bot
def make_boss(self, message):
    if message.from_user.id == BOSS_ID_1:
        try:
            # try to take the new boss id
            new_boss = message['reply_to_message']['from_user']['id']

            # open the file and read the info
            input_file = open("Boss.txt", "r")
            boss_id = input_file.readlines()
            input_file.close()
            check = True
            # check if the is of the user is existing or not
            for id_file in boss_id:
                id_file = id_file.rstrip("\n")
                if int(new_boss) == int(id_file):
                    check = False
            if check:
                output_file = open("Boss.txt", "a")
                target = "{}\n".format(new_boss)
                output_file.write(target)
                output_file.close()
                if message['reply_to_message']['from_user']['username'] is not None:
                    message.reply("New boss has been added @{}".format(message['reply_to_message']['from_user']['username']))
                else:
                    message.reply(
                        "New boss has been added {}".format(message.reply_to_message.from_user.mention()))
            else:
                message.reply("He is already a boss")
                #message.reply("You mush mention someone-2")
        except TypeError:
            message.reply("You mush mention someone-Boss")
    else:
        message.reply("Just Big Boss can do it")


# this function for all other messages

def global_handler(self, message):
    if message.text is not None:
        text = message["text"]

        # to show the help message
        if text.lower() == "المهام":
            help_message(self, message)

        # get all of the responses keys
        elif text.lower() == "الردود":
            get_the_response(self, message)

        # get the id for some one
        elif text.lower() == "كشف":
            get_id(self, message)

        # make a profile
        elif text.split("\n")[0] == "ملف تعريفي":
            profile(self, message)

        # get a profile for someone
        elif text.split("\n")[0] == "معلومات":
            get_profile(self, message)

        # add a response
        elif text.split("\n")[0] == "اضافة رد" or text.split("\n")[0] == "اضافه رد" or text.split("\n")[0] == "اضف رد":
            archives(self, message)

        # delete a response
        elif text.split("\n")[0] == "حذف رد":
            delete_response(self, message)

        # get the profile form
        elif text.lower() == "صيغة الملف التعريفي" or text.lower() == "صيغة ملف تعريفي":
            profile_form(self, message)

        # get the add response form
        elif text.lower() == "صيغة اضافة رد" or text.lower() == "صيغة اضافة الرد":
            response_form(self, message)

        # make a user as a boss
        elif text.lower() == "رفع مدير":
            make_boss(self, message)

        # block user
        elif text.lower() == "طرد" or text.lower() == "حظر":
            block(self, message)

        # pin a message
        elif text == "تثبيت" or text == "ثبت":
            pin_message(self, message)

        # pin a message
        elif text == "الغاء تثبيت" or text == "إلغاء تثبيت":
            unpin_message(self, message)

        #
        elif text == "عيب":
            edit_bot_message(self, message)

        else:
            response = responses.sample_responses(text)
            if response is None:
                pass
            else:
                message.reply(response)
    else:
        pass


# function that will check a word in dictionary
def check_archives(message):
    dictionary = {}
    # open the file
    input_file = open("archives.txt", "r")
    # read info
    lines = input_file.readlines()
    input_file.close()
    for line in lines:
        line = line.split("*")
        dictionary[line[0]] = line[1].rstrip("\n")
    # check if the key is existing
    for key, value in dictionary.items():
        if key.lower() == message.lower():
            # if it is existing make check to false
            return True


def check_boss(user_id):
    input_file = open("Boss.txt", "r")
    boss_id = input_file.readlines()
    input_file.close()
    # check if the is of the user is existing or not
    for id_file in boss_id:
        id_file = id_file.rstrip("\n")
        if int(user_id) == int(id_file):
            return True





bot.add_handler(MessageHandler(global_handler))





# define a code that print username of sender and his message
# @bot.on_message()
# def log(client, message):
#    print(message["from_user"]["username"])
#    print(message["text"])


# @bot.on_deleted_messages()
# def s(self, message):
#    self.send_message(-476715212, "why??")
#    print(message)

bot.run()
