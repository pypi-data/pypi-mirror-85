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


def list():
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