import os, sys, time, msvcrt, pyautogui, keyboard
from colorama import Fore, Back, Style, just_fix_windows_console
just_fix_windows_console()
print(Style.RESET_ALL)

def clearConsole():
    os.system('cls' if os.name == 'nt' else 'clear')

def log(status, message):
    color = {"info": Back.BLUE, "warn": Back.YELLOW, "error": Back.RED}.get(status, "")
    tag = f"[{status.upper():^5}]"
    print(color + tag + Style.RESET_ALL + " " + message)

def optionInput(type):
    if type == "index":
        return input(Fore.LIGHTCYAN_EX + "Choose an option: " + Style.RESET_ALL)
    elif type == "value":
        return input(Fore.LIGHTCYAN_EX + "Enter a new value: " + Style.RESET_ALL)
    elif type == "hotkey":
        return input(Fore.LIGHTCYAN_EX + "Enter a new hotkey: " + Style.RESET_ALL)

def set_config_value(filename, key, value):
    updated = False
    lines = []
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            for line in f:
                if line.startswith(key + "="):
                    lines.append(f"{key}={value}\n")
                    updated = True
                else:
                    lines.append(line)
    if not updated:
        lines.append(f"{key}={value}\n")
    with open(filename, 'w') as f:
        f.writelines(lines)

def get_config_value(filename, key):
    if not os.path.exists(filename):
        return None
    with open(filename, 'r') as f:
        for line in f:
            if line.startswith(key + "="):
                return line.strip().split("=", 1)[1]
    return None

def printTitle():
    print(Fore.LIGHTBLUE_EX + "        Shawarma Legend Utils - v1.0.7        " + Style.RESET_ALL)
    print("This is a utility for the game Shawarma Legend.")

def init():
    clearConsole()
    global absPath
    absPath = os.getcwd()
    config_path = os.path.join(absPath, "config.conf")
    hotkey_path = os.path.join(absPath, "hotkey.conf")
    if not os.path.exists(config_path):
        log("warn", "Config file not found. Creating a new one...")
        time.sleep(1)
        default_config = {
            "language": "english",
            "worker": "1",
            "burrito-machine": "1",
            "warpping-machine": "1",
            "ingredients-click-count": "1",
            "grilling-pan": "1",
            "cup": "1",
            "soda-machine": "1",
            "frier": "1",
            "potato-slicer": "1",
            "shawarma-slicer": "1",
            "forth-customer": "false",
            "ingredients-customization": "false",
            "first-time-use": "true"
        }
        with open(config_path, 'w') as f:
            for k, v in default_config.items():
                f.write(f"{k}={v}\n")
    if not os.path.exists(hotkey_path):
        with open(hotkey_path, 'w') as f:
            f.write("# hotkeys will be configured here\n")

def firstTimeUseGuide():
    clearConsole()
    printTitle()
    print(Fore.LIGHTGREEN_EX + "----------- [First time use guide] -----------" + Style.RESET_ALL)
    print("This guide will help you set hotkeys to control the game.")
    print("Continue? [y/n]")
    option = optionInput("index")
    if option != "y":
        mainMenu()

def start():
    clearConsole()
    flag = get_config_value(absPath + "/config.conf", "first-time-use")
    if flag == "true":
        firstTimeUseGuide()

def about():
    clearConsole()
    printTitle()
    print(Fore.LIGHTGREEN_EX + "------------------- [About] ------------------" + Style.RESET_ALL)
    print("Version: 1.0.7")
    print("Made by XxdMkb_Mark using Python")
    print("Github repository: https://github.com/XxdMkbMark/Shawarma-Legend-Utils \n")
    print("1].Back")
    if optionInput("index") == "1":
        mainMenu()
    else:
        log("error", "Invalid option")
        time.sleep(0.7)
        about()

settings_list = [
    ("language", "Languages", ["english", "chinese"]),
    ("worker", "Worker level"),
    ("burrito-machine", "Burrito Machine level"),
    ("warpping-machine", "Warpping Machine level"),
    ("ingredients-click-count", "Ingredients click count"),
    ("grilling-pan", "Grilling Pan level"),
    ("cup", "Cup level"),
    ("soda-machine", "Soda Machine level"),
    ("frier", "Frier level"),
    ("potato-slicer", "Potato Slicer level"),
    ("shawarma-slicer", "Shawarma Slicer level"),
    ("forth-customer", "Forth customer", ["true", "false"]),
    ("ingredients-customization", "Ingredients customization", ["true", "false"])
]

def settings():
    clearConsole()
    printTitle()
    print(Fore.LIGHTGREEN_EX + "----------------- [Settings] -----------------" + Style.RESET_ALL)
    for i, (_, name, *_) in enumerate(settings_list, start=1):
        print(f"{i}].{name}")
    print(f"{len(settings_list)+1}].Back")
    option = optionInput("index")
    try:
        index = int(option)
        if 1 <= index <= len(settings_list):
            optionAdjust(index - 1)
        elif index == len(settings_list) + 1:
            mainMenu()
        else:
            raise ValueError
    except ValueError:
        log("error", "Invalid option")
        time.sleep(0.7)
        settings()

def optionAdjust(index):
    clearConsole()
    printTitle()
    key, label, *values = settings_list[index]
    current = get_config_value(absPath + "/config.conf", key)
    print(f"[{label}]\nCurrent value: {current if current else '(undefined)'}\n")
    if values:
        for i, v in enumerate(values[0], start=1):
            print(f"{i}].{v.capitalize()}")
        print(f"{len(values[0])+1}].Back")
        option = optionInput("index")
        try:
            i = int(option)
            if 1 <= i <= len(values[0]):
                set_config_value(absPath + "/config.conf", key, values[0][i - 1])
            settings()
        except ValueError:
            log("error", "Invalid option")
            time.sleep(0.7)
            optionAdjust(index)
    else:
        new_value = optionInput("value")
        set_config_value(absPath + "/config.conf", key, new_value)
        settings()

def mainMenu():
    clearConsole()
    printTitle()
    print(Fore.LIGHTGREEN_EX + "----------------- [Main Menu] ----------------" + Style.RESET_ALL)
    print("1].Start")
    print("2].Settings")
    print("3].Quit")
    print("4].About")
    option = optionInput("index")
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

init()
time.sleep(0.5)
mainMenu()
