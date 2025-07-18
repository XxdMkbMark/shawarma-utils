import os,sys,time,msvcrt
from colorama import Fore, Back, Style, just_fix_windows_console
just_fix_windows_console()
print(Style.RESET_ALL)

def clearConsole():
    os.system('cls' if os.name == 'nt' else 'clear')

def init():
    clearConsole()
    global absPath
    absPath = os.getcwd()
    if os.path.exists(absPath+"/config.conf"):
        pass
    else:
        log("warn", "Config file not found. Creating a new one...")
        time.sleep(1)
        temp=open(absPath+"\config.conf","w")
        temp.write("language=english\nworker=1\nburrito-machine=1\nwarpping-machine=1\ningredients-click-count=1\ngrilling-pan=1\ncup=1\nsoda-machine=1\nfrier=1\npotato-slicer=1\nshawarma-slicer=1\nforth-customer=false\ningredients-customization=false")
        temp.close()
        if not os.path.exists(absPath+"/config.conf"):
            log("error", "Failed to create config file, please check if you have premissions to write into the folder.")
            print("Press any key to quit...")
            msvcrt.getch()
            sys.exit(1)

def log(status, message):
    if status == "info":
        print(Back.BLUE + "[INFO]" + Style.RESET_ALL + " " + message)
    elif status == "warn":
        print(Back.YELLOW + "[WARN]" + Style.RESET_ALL + " " + message)
    elif status == "error":
        print(Back.RED + "[ERROR]" + Style.RESET_ALL + " " + message)

def optionInput(type):
    if type == "index":
        option=input(Fore.LIGHTCYAN_EX + "Choose an option: " + Style.RESET_ALL)
        return option
    elif type == "value":
        value=input(Fore.LIGHTCYAN_EX + "Enter a new value: " + Style.RESET_ALL)
        return value
    
def printTitle():
    print(Fore.LIGHTBLUE_EX + "        Shawarma Legend Utils - v1.0.6        " + Style.RESET_ALL)
    print("This is a utility for the game Shawarma Legend.")

def insertLines(filename, line, content):
    #读行
    with open(filename, 'r') as f:
        lines = f.readlines()
    #删除行原有内容并插入列表
    if 0 <= line < len(lines):
        del lines[line]
        lines.insert(line, content + '\n')
    else:
        log("error", "[Internal error: line number out of range, in func:insertLines.] This is definitely a bug, if you are seeing this, please report this on Github immediately.")
        time.sleep(1)
        sys.exit(1)
    #写行
    with open(filename, 'r+') as f:
        f.writelines(lines)

def readCurrentValue(filename, option): #只用于设置读取当前值！不要用在其他地方！
    with open(filename, 'r') as f:
        lines = f.readlines()
        for i in lines:
            if i.startswith(option):
                return i.split("=")[1].strip()
    '''
    temp = open(absPath+"/config.conf", "r")
        tempList=temp.readlines()
        for i in tempList:
            if i.startswith("language"):      
                print("Current value: "+i.split("=")[1].strip()+"\n")
                break
        temp.close()
    '''
    
def mainMenu():
    optionList=["1","2","3","4"]
    clearConsole()
    printTitle()
    print(Fore.LIGHTGREEN_EX + "----------------- [Main Menu] ----------------" + Style.RESET_ALL)
    print("1].Start")
    print("2].Settings")
    print("3].Quit")
    print("4].About")
    option=optionInput("index")
    if option in optionList:
        if option == "1":
            start()
        elif option == "2":
            settings()
        elif option == "3":
            log("info", "Exiting...")
            time.sleep(0.4)
            sys.exit(0)
        elif option == "4":
            about()
    else:
        log("error", "Invalid option")
        time.sleep(0.7)
        mainMenu()
def start():
    pass

def settings():
    optionList=["1","2","3","4","5","6","7","8","9","10","11","12","13","14"]
    clearConsole()
    if not os.path.exists(absPath+"/config.conf"):
        log("error", "Config file not found. Try to rerun the program to create a config file or create one manually.")
        print("Press any key to continue...")
        msvcrt.getch()
        mainMenu()
    printTitle()
    print(Fore.LIGHTGREEN_EX + "----------------- [Settings] -----------------" + Style.RESET_ALL)
    print("1].Languages")
    print("2].Worker level")
    print("3].Burrito Machine level")
    print("4].Warpping Machine level")
    print("5].Ingredients click count")
    print("6].Grilling Pan level")
    print("7].Cup level")
    print("8].Soda Machine level")
    print("9].Frier level")
    print("10].Potato Slicer level")
    print("11].Shawarma Slicer level")
    print("12].Forth customer")
    print("13].Ingredients customization\n")
    print("14].Back")
    option=optionInput("index")
    if option in optionList:
        for i in optionList:
            if option == i and i != "14":
                optionAdjust(int(option))
            elif i == "14":
                mainMenu()
    else:
        log("error", "Invalid option")
        time.sleep(0.7)
        settings()

def optionAdjust(index):
    clearConsole()
    printTitle()
    print(Fore.LIGHTGREEN_EX + "----------------- [Settings] -----------------" + Style.RESET_ALL)
    optionListLanguages=["1","2","3"]
    if index == 1:
        print("[Languages]")
        print("Current value: "+readCurrentValue(absPath+"/config.conf", "language")+"\n")
        print("1].English")
        print("2].中文(简体)\n")
        print("3].Back")
        option=optionInput("index")
        if option in optionListLanguages:
            if option == "1":
                insertLines(absPath+"/config.conf", 0, "language=english")
                settings()
            elif option == "2":
                insertLines(absPath+"/config.conf", 0, "language=chinese")
                settings()
            elif option == "3":
                settings()
        else:
            log("error", "Invalid option")
            time.sleep(0.7)
            optionAdjust(1)
        
    elif index == 2:
        print("[Worker level]")
        print("Current value: "+readCurrentValue(absPath+"/config.conf", "worker")+"\n")
        option=optionInput("value")
        insertLines(absPath+"/config.conf", 1, "worker="+option)
    elif index == 3:
        pass
    elif index == 4:
        pass
    elif index == 5:
        pass
    elif index == 6:
        pass
    elif index == 7:
        pass
    elif index == 8:
        pass
    elif index == 9:
        pass
    elif index == 10:
        pass
    elif index == 11:
        pass
    elif index == 12:
        pass
    elif index == 13:
        pass
    else:
        log("error", "It seems like that this option doesn't exist. If you believe this is a bug, please report it on Github.")
        time.sleep(2)
        settings()

def about():
    optionList=["1"]
    clearConsole()
    printTitle()
    print(Fore.LIGHTGREEN_EX + "------------------- [About] ------------------" + Style.RESET_ALL)
    print("Version: 1.0.6")
    print("Made by XxdMkb_Mark using Python")
    print("Github repository: https://github.com/XxdMkbMark/Shawarma-Legend-Utils \n")
    print("1].Back")
    option=input(Fore.LIGHTCYAN_EX + "Choose an option: " + Style.RESET_ALL)
    if option in optionList:
        if option == "1":
            mainMenu()
    else:
        log("error", "Invalid option")
        time.sleep(0.7)
        about()

init()
time.sleep(0.5)
mainMenu()