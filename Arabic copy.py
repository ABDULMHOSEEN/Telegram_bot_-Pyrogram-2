# import the libraries
import pyrogram
from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
import json
import os
import tgcrypto
# Responses file is a file that have some handleMessage
import Responses as responses
import profile as personal_info

# OPEN The file that include the api id and api hash
Password = open("PassWord.txt", "r")
# take and save the information
api_id = Password.readline().split()[1]
api_hash = Password.readline().split()[1]
# close the file
Password.close()

BOT_ID = 1779607655  # Define the bot id

# define a boss id which is mine and some of other
BOSS_ID_1 = 477758182
BOSS_ID_2 = 896399150

bot = Client("Bot_2", api_id, api_hash) # Make a client named Bot_2 which will be a session


# define a start command
@bot.on_message(filters.command(["start", "start@ABDULMOHSEEN_2_bot"]))
def start(self, message):
    # It can be used as a init function for some uses later
    message.reply("Hi! \n The bot is running")\


@bot.on_message(filters.command(["start2020"]))
def get_setup_bot(self, message):
    # setup the files of the chat
    user_id = message.from_user.id
    chat_id = message.chat.id
    if user_id == BOSS_ID_1:
        target1 = "Boss{}.json".format(chat_id)
        Boss_file = open(target1, "w")
        target2 = "archives{}.json".format(chat_id)
        Archives_file = open(target2, "w")
        target3 = "Lock{}.json".format(chat_id)
        Boss_file = open(target3, "w")
        message.reply("تم إنشاء الملفات بنجاح")


# send a message with a new person join the chat
@bot.on_message(filters.new_chat_members)
def new_person(self, message):
    message.reply(f"أهلا وسهلا {message.from_user.mention()} نورت قروب {message.chat.title} ")


# define the help command ti get the functions of the bot
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
    chat_id = message.chat.id
    archives_file = "archives{}.json".format(chat_id)
    # TAKE ALL The info and make it as a list than print the key of the list
    response_local = []
    # read info
    lines = read_json_file("archives.json")
    counter = 1

    # sort the keys ba make them a list than sort it
    key_list = list(lines.keys())
    key_list.sort()
    # print the keys in list with a good format
    for key in key_list:
        # make the correct format
        target = "{}- ".format(counter) + key
        # append it inside the list
        response_local.append(target)
        counter += 1
    # change the format after save inside the list
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
    # check if the user mentioned someone or not
    try:
        user_id = message.reply_to_message.from_user.id
        check = check_boss(user_id)
        if user_id == BOSS_ID_1:
            text_boss = "مدير كبير"
        elif user_id == BOT_ID:
            text_boss = "بوت"
        elif check:
            text_boss = "مدير في البوت"
        else:
            text_boss = "عضو في البوت"
        ID = message['reply_to_message']['from_user']['id']
        # if the user have a username so print it
        if message.reply_to_message.from_user.username is not None:
            target = f"👤 اسم المستخدم: "\
                    f'{message.reply_to_message.from_user.first_name}\n' \
                     f'🌐 اليوزر: ' \
                     f'@{message.reply_to_message.from_user.username}\n' \
                     f' 🆔' \
                     f'المعرف: ' \
                     f'{ID}\n' \
                     f' ⚜️ رتبة المستخدم:' \
                     f' {text_boss}'
            message.reply(target)
        else:
            target = f"👤 اسم المستخدم: " \
                     f'{message.reply_to_message.from_user.mention()}\n' \
                     f'🌐 اليوزر: لا يوجد' \
                     f'\n' \
                     f'🆔' \
                     f'المعرف: ' \
                     f'{ID}\n' \
                     f' ⚜️ رتبة المستخدم: ' \
                     f'{text_boss}'
            # if it doesn't have so make a mention by his name
            message.reply(target)
    except TypeError:
        # if there are no mention, print this message
        message.reply("You have to mention someone")


# this function is for take the information from the profile
@bot.on_message(filters.command("info"))    # close this function because some reasons
def get_profile(self, message):
    on_off = False
    if on_off:
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
    message.reply("نأسف تم تعطيل هذه الخاصية")


# make a new profile
@bot.on_message(filters.command("profile"))     # close this function because some reasons
def profile(self, message):
    #text = message.text.split("\n")
    #user_id = message.from_user.id
    #profile = personal_info.sample_responses(text, user_id)
    #message.reply(profile)
    message.reply("نأسف تم تعطيل هذه الخاصية")


# define archives to add a new responses
@bot.on_message(filters.command(["addR", "addR@ABDULMOHSEEN_2_bot"]))
def archives(self, message):
    # take the correct file name
    chat_id = message.chat.id
    archives_file = "archives{}.json".format(chat_id)

    # allow this function to the Boss only
    # if message.from_user.id == BOSS_ID:

    # take the text from the message
    text = message.text

    # split by each line
    text = text.split("\n")

    # delete the key word
    text.pop(0)

    # check the len
    if len(text) == 2:
        # check the key
        check = check_archives(text[0])
        # if the key is not existing add a new response
        if not check:
            # read the file information
            input_file: dict = read_json_file("archives.json")
            # add a new key:value
            input_file[text[0].rstrip(" ")] = text[1]
            # rewrite the information inside the file
            open_data = open("archives.json", "w")
            json.dump(input_file, open_data, indent=2)
            open_data.close()
            # print DONE message
            message.reply("✔️ تمت اضافة الرد")
        else:
            # if the key is existing, print this message
            message.reply("المفتاح موجود مسبقاً")
    else:
        try:
            check = check_archives(text[0])
            if not check:
                target = message.reply_to_message.text
                # read the file information
                input_file: dict = read_json_file("archives.json")
                # add a new key:value
                input_file[text[0].rstrip(" ")] = target
                # rewrite the information inside the file
                open_data = open("archives.json", "w")
                json.dump(input_file, open_data, indent=2)
                open_data.close()
                # print DONE message
                message.reply("✔️ تمت اضافة الرد")
            else:
                # if the key is existing, print this message
                message.reply("The key is already exiting")
        except AttributeError:
            message.reply("لأضافة رد يجب اتباع التعليمات الصحيحه"
                          "\nللمزيد اكتب (صيغة اضافة الرد)"
                          "\n"
                          "او اضغط هنا"
                          " /response_form")
        except IndexError:
            message.reply("لم يتم اضافة اسم المفتاح")


@bot.on_message(filters.command("chatR"))
def add_response_to_chat(self, message):
    # take the text from the message
    text = message.text

    # split by each line
    text = text.split("\n")

    # delete the key word
    text.pop(0)

    try:
        input_file: dict = read_json_file("chat.json")
        # add a new key:value
        input_file[text[0]] = text[1]
        # rewrite the information inside the file
        open_data = open("chat.json", "w")
        json.dump(input_file, open_data, indent=2)
        open_data.close()

    except:
        message.reply("حدث خطأ 404")



# make a function to delete a response
@bot.on_message((filters.command(["deleteR", "deleteR@ABDULMOHSEEN_2_bot"])))
def delete_response(self, message):
    chat_id = message.chat.id
    archives_file = "archives{}.json".format(chat_id)

    # this function is only for Boss
    check = check_boss(message.from_user.id)
    if check:
        # get the chat id
        chat_id = message.chat.id

        # get the message text
        text = message.text

        # split by line
        text = text.split("\n")

        # pop the command word
        text.pop(0)
        # check if the key is existing
        try:
            # read the information from the file
            lines = read_json_file("archives.json")
            # try to pop the key
            lines.pop(text[0])
            # rewrite the information
            open_data = open("archives.json", "w")
            json.dump(lines, open_data, indent=2)
            # close file
            open_data.close()
            message.reply("✔️ تم حذف الرد")
        except KeyError:
            # if the key is not existing
            message.reply("المفتاح غير موجود")

        except Exception:
            # else errors
            message.reply("حدث خطأ اثناء الحذف")
    else:
        message.reply("Just the boss can do it")


# define a pin function
@bot.on_message(filters.command("pin"))
def pin_message(self, message):
    # this function for Boss
    # take the chat id and the message id
    chat_id = message.chat.id
    message_id = message.reply_to_message.message_id
    # use a function to pin the message
    self.pin_chat_message(chat_id, message_id)

# define a Unpin function
@bot.on_message(filters.command("Unpin"))
def unpin_message(self, message):
    # this function for Boss
    # take the chat id and the message id
    chat_id = message.chat.id
    message_id = message.reply_to_message.message_id
    # use a function to unpin the message
    self.unpin_chat_message(chat_id, message_id)

# define an edit function
def edit_bot_message(self, message):
    # in future I will add an API for talking with the peoples and He might be rude so I make a handler for that

    # take the chat id and the message id
    chat_id = message.chat.id
    message_id = message.reply_to_message.message_id
    # edit the text message
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
                  "\nYou have to replace each one by your information")


# define a function that give the form to add a new response
@bot.on_message(filters.command(["response_form", "response_form@ABDULMOHSEEN_2_bot"]))
def response_form(self, message):
    message.reply("لأضافة رد يجب اتباع الطريقة التالية\n\n"
                  "اضافة رد\n"
                  "اسم المفتاح\n"
                  "حدد الرسالة المطلوب حفظها")


# function for raed the message
@bot.on_message(filters.command("readMessage"))     # this function is for some programing use
def readMessage(self, message):
    print(message)
    message.reply(message)


# for block the user
def block(self, message):
    # This function is for Boss only
    check = check_boss(message.from_user.id)
    if check:
        try:
            # take the user id and chat id
            chat_id = message.chat.id
            user_id = message.reply_to_message.from_user.id
            # if the boss try to kick the Bot so the boss will be kicked
            if user_id == BOT_ID and user_id != BOSS_ID_1:
                # send message before kick
                message.reply("You try to kick me?")
                # kick
                self.kick_chat_member(chat_id, message.from_user.id)
            else:
                # in normal use kick the person
                if message.reply_to_message.from_user.username is not None: # if the person has a user name so mention
                    self.kick_chat_member(chat_id, user_id)
                    self.send_message(chat_id, "The person who is named @{} has been kicked".format(message.reply_to_message.from_user.username))
                else:   # if the person does not have a user name so use a mention method
                    self.kick_chat_member(chat_id, user_id)
                    self.send_message(chat_id, "The person who is named {} has been kicked".format(message.reply_to_message.from_user.mention()))
        except AttributeError:
            # except the None mention error
            message.reply("You must mention someone-kick")
        except pyrogram.errors.exceptions.bad_request_400.UserAdminInvalid:
            # except kick admin
            message.reply("لا يمكن طرد المشرفين")
        except:
            # else
            message.reply("حدث خطأ اثناء الطرد")
    else:
        message.reply("🚫 Just the Boss can kick")



# make a function that will add a new boss in bot
def make_boss(self, message):
    chat_id = message.chat.id
    Boss_file = "Boss{}.json".format(chat_id)
    # this function is for ths BIG BOSS only
    if message.from_user.id == BOSS_ID_1:
        try:
            # try to take the new boss id
            new_boss_id = message['reply_to_message']['from_user']['id']
            new_boss_username = message['reply_to_message']['from_user']['username']
            # check if he is a boss or not
            check = check_boss(new_boss_id)
            if not check:
                # if not
                # read the information
                new_data: dict = read_json_file("Boss.json")
                # add the user to the dict
                new_data[new_boss_id] = new_boss_username
                # rewrite the information
                open_data = open("Boss.json", "w")
                json.dump(new_data, open_data, indent=2)
                open_data.close()

                if message['reply_to_message']['from_user']['username'] is not None:    # if the user has a username so mention
                    message.reply("New boss has been added @{}".format(message['reply_to_message']['from_user']['username']))
                else:   # if the user does not have a username use a mention method
                    message.reply(
                        "New boss has been added {}".format(message.reply_to_message.from_user.mention()))
            else:
                message.reply("He is already a boss")
                #message.reply("You mush mention someone-2")
        except AttributeError:
            message.reply("You mush mention someone-Boss")
        except Exception:
            message.reply("حدث خطأ اثناء العملية")
    else:
        message.reply("🚫 Just Big Boss can do it")

# make a function that will delete a boss
def delete_boss(self, message):
    chat_id = message.chat.id
    Boss_file = "Boss{}.json".format(chat_id)
    # this function is for ths BIG BOSS only
    if message.from_user.id == BOSS_ID_1:
        try:
            # try to take the new boss id
            boss_id = message['reply_to_message']['from_user']['id']
            new_boss_username = message['reply_to_message']['from_user']['username']
            # read the information
            new_data: dict = read_json_file("Boss.json")
            # add the user to the dict
            new_data.pop(str(boss_id))
            # rewrite the information
            open_data = open("Boss.json", "w")
            json.dump(new_data, open_data, indent=2)
            open_data.close()

            if message['reply_to_message']['from_user']['username'] is not None:    # if the user has a username so mention
                message.reply("تم طرد @{} من قائمة المدراء".format(message['reply_to_message']['from_user']['username']))
            else:   # if the user does not have a username use a mention method
                message.reply(
                    "تم طرد {} من قائمة المدراء".format(message.reply_to_message.from_user.mention()))

        except AttributeError:
            message.reply("حدد شخص عشان اعرف اتعامل معه")

        except KeyError:
            message.reply("الأيدي غير موجود")

        except Exception:
            message.reply("حدث خطأ اثناء العملية")
    else:
        message.reply("🚫 Just Big Boss can do it")


# define a deleting message function
def delete_message(self, message):
    # this function for Boss
    user_id = message.from_user.id
    if check_boss(user_id):
        try:
            # try to take the number of message to delete
            num = message.text.split()
            num = num[1]
            # get the chat id and message id
            chat_id = message.chat.id
            message_id = message.message_id
            # make a for loop
            for times in range(int(num) + 1):
                # this is the method of deleting
                self.delete_messages(chat_id=chat_id, message_ids=message_id)
                # go bake the to old messages
                message_id -= 1
        # if the user didn't add a number
        except IndexError:                # delete the message that mention
            try:
                # get the chat and message id
                message_id = message.reply_to_message.message_id
                chat_id = message.chat.id
                # delete the messages
                self.delete_messages(chat_id=chat_id, message_ids=message.message_id)
                self.delete_messages(chat_id=chat_id, message_ids=message_id)

            except AttributeError:  # if there are no mention print this message
                message.reply("حدد رسالة او حدد رقم")
        except ValueError: # if the value error print this message
            message.reply("ادخل عدد وليس احرف او رموز")
        except Exception: # for any error
            message.reply("حدث خطأ أثناء حذف الرسائل")
    else:
        message.reply("🚫 Just The Boss can do it")



def lock(self, message):
    chat_id = message.chat.id
    Lock_file = "Lock{}.json".format(chat_id)

    check = check_boss(message.from_user.id)
    if check:
        try:
            user_id = message.reply_to_message.from_user.id
            user_username = message.reply_to_message.from_user.username
            message_id = message.reply_to_message.message_id
            output = read_json_file("Lock.json")
            # add a new key:value
            check_key = check_keys(user_id, output.keys())
            if check_key:
                if user_id != BOSS_ID_1:
                    output[user_id] = user_username
                    # rewrite the information inside the file
                    open_data = open("Lock.json", "w")
                    json.dump(output, open_data, indent=2)
                    open_data.close()
                    # print DONE message
                    self.send_message(
                        chat_id=message.chat.id,
                        text="✔️ تم التقييد",
                        reply_to_message_id=message_id
                    )
                else:
                    message.reply("ههههه حلوه منك")
                    output[message.from_user.id] = message.from_user.username
                    # rewrite the information inside the file
                    open_data = open("Lock.json", "w")
                    json.dump(output, open_data, indent=2)
                    open_data.close()
                    # print DONE message
                    self.send_message(
                        chat_id=message.chat.id,
                        text="✔️ تم التقييد",
                        reply_to_message_id=message.message_id
                    )


            else:
                message.reply("الشخص غير مقيد اصلا")


        except AttributeError:
            message.reply("حدد الرسالة عشان اعرف الشخص")
    else:
        message.reply("شف يحسب نفسه مدير")


def unlock(self, message):
    chat_id = message.chat.id
    Lock_file = "Lock{}.json".format(chat_id)
    check = check_boss(message.from_user.id)
    if check:
        try:
            user_id = str(message.reply_to_message.from_user.id)
            message_id = message.reply_to_message.message_id
            output = read_json_file("Lock.json")
            # add a new key:value
            output.pop(user_id)
            # rewrite the information inside the file
            open_data = open("Lock.json", "w")
            json.dump(output, open_data, indent=2)
            open_data.close()
            # print DONE message
            self.send_message(
                chat_id=message.chat.id,
                text="✔️ تم فك التقييد",
                reply_to_message_id=message_id
            )

        except AttributeError:
            message.reply("حدد الرسالة عشان اعرف الشخص")

        except KeyError:
            message.reply("الشخص غير مقيد اصلا")

    else:
        message.reply("شف يحسب نفسه مدير")





# this function for all other messages
def global_handler(self, message):
    check_of_lock = check_lock(self, message)
    if check_of_lock:
        if message.text is not None:
            text = message["text"]

            # to show the help message
            if text.lower() == "المهام":
                help_message(self, message)

            # get all of the responses keys
            elif text == "الردود" or text == "ردود":
                get_the_response(self, message)

            # get the id for some one
            elif text.lower() == "كشف":
                get_id(self, message)

            # make a profile
            elif text.split("\n")[0] == "ملف تعريفي":
                #profile(self, message)
                message.reply("نأسف تم تعطيل هذه الخاصية")

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

            elif text == "تنزيل مدير":
                delete_boss(self, message)

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

            # deleting messages
            elif text.split()[0] == "حذف" or text.split()[0] == "مسح":
                delete_message(self, message)

            # lock someone
            elif text == "تقييد" or text == "تقيد" or text == "اسكت" or text == "انطم" or text == "كتم":
                lock(self, message)

            #nulock
            elif text == "الغاء التقييد" or text == "الغاء التقيد" or text == "تكلم":
                unlock(self, message)


            # This is a function that will tell some jokes
            elif text.lower() == "joke" or text.lower() == "نكته" or text.lower() == "نكتة":
                target = responses.jokesFunction()
                message.reply(target)

            else:
                response = responses.sample_responses(text)
                if response is None:
                    pass
                else:
                    message.reply(response)
        else:
            pass
    else:
        pass

# function that will check a word in dictionary
def check_archives(message):
    chat_id = message.chat.id
    archives_file = "archives{}.json".format(chat_id)
    dictionary = {}
    # open the file
    # read info
    input_file = read_json_file("archives.json")
    # check if the key is existing
    for key, value in input_file.items():
        if key.lower() == message.lower():
            # if it is existing make check to false
            return True

    return False


def check_boss(user_id):
    #chat_id = message.chat.id
    #Boss_file = "Boss{}.json".format(chat_id)
    boss_id = read_json_file("Boss.json")
    # check if the is of the user is existing or not
    for id_file in boss_id.keys():
        if int(user_id) == int(id_file):
            return True
    return False


def check_keys(user_id, key_list):
    for key in key_list:
        print(key)
        if user_id == int(key):
            return False
    return True

def check_lock(self, message):
    chat_id = message.chat.id
    Lock_file = "Lock{}.json".format(chat_id)

    user_id = message.from_user.id
    message_id = message.message_id
    input_info = read_json_file("Lock.json")
    for key in input_info.keys():
        if user_id == int(key):
            self.delete_messages(chat_id=chat_id, message_ids=message_id)
            return False
    return True
def read_json_file(filename):
    if not os.path.isfile(filename):
        o = open(filename, "x")
        o.write("{}")
        o.close()
    open_data = open(filename, "r")
    data: dict = json.load(open_data)
    open_data.close()
    return data




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
