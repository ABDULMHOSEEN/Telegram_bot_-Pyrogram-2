# import the libraries
from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
import requests
import Responses as responses
import profile as personal_info


# OPEN The file that include the api id and hash
Password = open("PassWord.txt", "r")
api_id = Password.readline().split()[1]
api_hash = Password.readline().split()[1]

# Make a client named Bot
bot = Client("Bot", api_id, api_hash)


# define a start command
@bot.on_message(filters.command("start"))
@bot.on_message(filters.command("start@ABDULMOHSEEN_2_bot"))
def start(self, message):
    message.reply("Hi! \n The bot is running")


# define the help command
@bot.on_message(filters.command("help"))
@bot.on_message(filters.command("help@ABDULMOHSEEN_2_bot"))
def help(self, message):
    # print the list of Tasks
    message.reply("/start - Check if the bot is running\n"
                  "/my_ID - Get your id number\n"
                  "/profile_from - Take the form to make your own profile")


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
            message.reply(f"The person who's username is @{message.reply_to_message.from_user.username} his ID is: {ID}")
        else:
            message.reply(f"His ID is: {ID}")
    except TypeError:
        message.reply("You have to mention someone")

# this is a command to print the profile form
@bot.on_message(filters.command("profile_form"))
@bot.on_message(filters.command("profile_form@ABDULMOHSEEN_2_bot"))
def profile_form(self, message):
    message.reply("This is the form for profile\n"
                  "\n###########\n"
                  "/profile\n"
                  "/my_ID\n"
                  "Name\n"
                  "Master\n"
                  "Year\n"
                  "###########\n"
                  "\nYou have to replace each one by your information\nLike this:\n"
                  "\n########\n"
                  "/profile\n"
                  "477758182\n"
                  "Abdulmohseen\n"
                  "SWE\n"
                  "2020\n")


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
            message.reply(sol)


@bot.on_message(filters.command("readMessage"))
def readMessage(self,message):
    print(message)
    message.reply(message)




# this function for all other messages

def talk(client, message):
    text = message["text"]
    response = responses.sample_responses(text)
    if response is None:
        pass
    else:
        message.reply(response)


bot.add_handler(MessageHandler(talk))
















# define a code that print username of sender and his message
#@bot.on_message()
#def log(client, message):
#    print(message["from_user"]["username"])
#    print(message["text"])


bot.run()
