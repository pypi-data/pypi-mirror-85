def _print_list(list):
    num = 1
    if len(list) != 0:
        print("\nYour list:")
        for l in list:
            if num >= len(list):
                print("    " + str(num) + ") " + l + "\n")
            else:
                print("    " + str(num) + ") " + l)
            num += 1
    else:
        print("\nYour list is empty.\n")


def shopping_list():
    userList = []
    userInput = str(input("Enter your item: "))

    while userInput.lower() != "done":
        if userInput.lower() == "showlist":
            _print_list(userList)
        elif userInput.lower().startswith("remove"):
            remove = userInput.lower().replace("remove", "").strip()
            if remove != "*":
                userList.remove(remove)
            else:
                userList = []
        else:
            userList.append(userInput)
        userInput = str(input("Enter your item: "))
    _print_list(userList)
    saveFile = str(input("Save file to txt? (y/n) "))
    num = 1
    fileWrite = ""
    if len(userList) != 0:
        fileWrite += "Your list:\n"
        for l in userList:
            if num <= len(userList):
                fileWrite += "    " + str(num) + ") " + str(l) + "\n"
            else:
                fileWrite += "    " + str(num) + ") " + str(l)
            num += 1
    else:
        fileWrite += print("\nYour list is empty.\n")

    if saveFile == "y":
        filePath = str(input("File path: ").replace("\\", "\\\\"))
        with open(filePath + "\\Your_List.txt", "w") as file:
            file.write(fileWrite)
            file.close()
    else:
        return