# import the libraries
from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
import requests
import Responses as responses
import profile as personal_info

# OPEN The file that include the api id and hash
from pyrogram.scaffold import Scaffold

Password = open("PassWord.txt", "r")
api_id = Password.readline().split()[1]
api_hash = Password.readline().split()[1]

# Make a boss id which is mine
BOSS_ID = 477758182

# Make a client named Bot
bot = Client("Bot", api_id, api_hash)


# define a start command
@bot.on_message(filters.command("start"))
@bot.on_message(filters.command("start@ABDULMOHSEEN_2_bot"))
def start(self, message):
    message.reply("Hi! \n The bot is running")


@bot.on_chat_member_updated(filters.new_chat_members)
def new_person(self, message):
    chat_id = message['chat']['id']
    self.send_message(chat_id, "أهلا وسهلا نورت القروب")


# define the help command
@bot.on_message(filters.command("help"))
@bot.on_message(filters.command("help@ABDULMOHSEEN_2_bot"))
def help(self, message):
    # print the list of Tasks
    message.reply("/start - Check if the bot is running\n\n"
                  "/my_ID - Get your id number\n\n"
                  "/ID - you have to mention someone than you will get his ID number\n\n"
                  "/addR - for add some response\n\n"
                  "/Ans - to show all response\n\n"
                  "/profile_form - Take the form to make your own profile\n\n"
                  "/response_form - the correct form to write the response\n\n"
                  )


@bot.on_message(filters.command("Ans"))
@bot.on_message(filters.command("Ans@ABDULMOHSEEN_2_bot"))
def response(self, message):
    # TAKE ALL The info and make it as a dictionary
    dictionary = {}
    response_local = []
    # open the file
    input_file = open("archives.txt", "r")
    # read info
    lines = input_file.readlines()
    input_file.close()
    counter = 1
    for line in lines:
        line = line.split(":")
        target = "{}- ".format(counter) + line[0]
        response_local.append(target)
        counter += 1
        dictionary[line[0]] = line[1].rstrip("\n")
        # change the format
    response_local = (str(response_local).replace(",", "\n")).replace("[", "")
    response_local = (str(response_local).replace(",", "\n")).replace("]", "")
    response_local = (str(response_local).replace(",", "\n")).replace("'", "")
    # print the output
    message.reply(response_local)


# define an ID command
@bot.on_message(filters.command("my_ID"))
@bot.on_message(filters.command("my_ID@ABDULMOHSEEN_2_bot"))
def id_reply(self, message):
    if message.from_user.username is not None:
        message.reply(f"The person who's username is @{message.from_user.username} his ID is: {message.from_user.id}")
    else:
        message.reply(f"Your ID is: {message.from_user.id}")


# get the id for any person in group
@bot.on_message(filters.command("id"))
def get_id(self, message):
    try:
        ID = message['reply_to_message']['from_user']['id']
        if message.reply_to_message.from_user.username is not None:
            message.reply(
                f"The person who's username is @{message.reply_to_message.from_user.username} his ID is: {ID}")
        else:
            message.reply(f"His ID is: {ID}")
    except TypeError:
        message.reply("You have to mention someone")


# this function is for take the information from the profile
@bot.on_message(filters.command("info"))
def profile(self, message):
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
    text = message.text.split()
    user_id = message.from_user.id
    profile = personal_info.sample_responses(text, user_id)
    message.reply(profile)


# define archives
@bot.on_message(filters.command("addR"))
@bot.on_message(filters.command("addR@ABDULMOHSEEN_2_bot"))
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
        # TAKE ALL The info and make it as a dictionary
        dictionary = {}
        # open the file
        input_file = open("archives.txt", "r")
        # read info
        lines = input_file.readlines()
        input_file.close()
        for line in lines:
            line = line.split(":")
            dictionary[line[0]] = line[1].rstrip("\n")
        check = True
        # check if the key is existing
        for key, value in dictionary.items():
            if key in text[0]:
                # if it is existing make check to false
                check = False
                message.reply("The key is already exiting")

        if check:
            input_file = open("archives.txt", "a")
            # make the text as a dictionary and write it
            dictionary = "{}:{}\n".format(text[0], text[1])
            input_file.write(str(dictionary))
            message.reply("تمت اضافة الرد")
    else:
        message.reply("You have to write in the specific form (/response_form)")
# else:
# message.reply("Just the Boss can do it")


# this is a command to print the profile form
@bot.on_message(filters.command("profile_form"))
@bot.on_message(filters.command("profile_form@ABDULMOHSEEN_2_bot"))
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


@bot.on_message(filters.command("response_form@ABDULMOHSEEN_2_bot"))
@bot.on_message(filters.command("response_form"))
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


# this function for all other messages

def talk(self, message):
    if message.text is not None:
        text = message["text"]
        if text.lower() == "block":
            block(self, message)
        elif text.lower() == "make boss":
            make_boss(self, message)
        else:
            response = responses.sample_responses(text)
            if response is None:
                pass
            else:
                message.reply(response)
    else:
        pass


# for block the user
def block(self, message):
    # let the boss do this order
    input_file = open("Boss.txt", "r")
    boss_id = input_file.readlines()
    input_file.close()
    check = False
    # check if the is of the user is existing or not
    for id_file in boss_id:
        id_file = id_file.rstrip("\n")
        if int(message.from_user.id) == int(id_file):
            check = True
    if check:
        # take the user id and chat id
        try:
            chat_id = message.chat.id
            user_id = message.reply_to_message.from_user.id
            self.kick_chat_member(chat_id, user_id)
            self.send_message(chat_id, "The person who is named @{} has been kicked".format(message.reply_to_message.from_user.username))
        except:
            message.reply("You must mention someone-kick")
    else:
        message.reply("Just the boss can kick")
# make a function that will add a new boss in bot
def make_boss(self, message):
    if message.from_user.id == BOSS_ID:
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
                message.reply("New boss has been added @{}".format(message['reply_to_message']['from_user']['username']))
            else:
                message.reply("He is already a boss")
                #message.reply("You mush mention someone-2")
        except TypeError:
            message.reply("You mush mention someone-Boss")
    else:
        message.reply("Just big boss can do it")


bot.add_handler(MessageHandler(talk))

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
