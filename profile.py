# define a function that take input from user and return some strings
def sample_responses(input_text):
    # open the out put file
    output_file = open("profile_info.txt", "a+")
    output_file.seek(0)
    check = output_file.readlines()

    # take the user message
    user_message = input_text

    # delete the /profile word
    user_message.pop(0)

    # check if the len is correct
    if len(user_message) == 4:
        # check if the name is existing or not
        check_key = True
        for line in check:
            line = line.split(",")
            # if it is existing so don't write
            ID_file = line[0].split("=")
            ID_file = ID_file[1].replace(" ","")

            if user_message[0] == ID_file:
                check_key = False
                return "The ID is existing"
        # else do it
        if check_key:
            output_file.seek(99999)
            text = "ID = {},Name = {},Master = {},Year = {}\n".format(user_message[0], user_message[1],
                                                                         user_message[2].upper(), user_message[3])
            output_file.write(str(text))
            return "Done successfully"
    else:
        return "You have to send the message using the /profile_form"

    output_file.close()


# This function for return the file information
def read_info():
    # open the file
    output_file = open("profile_info.txt", "r")
    # read the info
    information = output_file.readlines()
    # close the file and pass the info
    output_file.close()
    return information
