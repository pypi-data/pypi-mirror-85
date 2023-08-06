def List():
    userList = []
    userInput = str(input("Enter your item: "))
    
    
    def PrintList(list):
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
    
    
    while userInput.lower() != "done":
        if userInput.lower() == "showlist":
            PrintList(userList)
        elif userInput.lower().startswith("remove"):
            remove = userInput.lower().replace("remove", "").strip()
            if remove != "*":
                userList.remove(remove)
            else:
                userList = []
        elif userInput.strip == 1:
            userInput = "done"
        userInput = str(input("Enter your item: "))
    PrintList(userList)