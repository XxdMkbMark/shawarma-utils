import os
import sys
import time
import msvcrt
import pyautogui
import keyboard
from colorama import Fore, Back, Style, just_fix_windows_console


just_fix_windows_console()
print(Style.RESET_ALL)

CONFIG_FILE = "config.conf"
HOTKEY_FILE = "hotkey.conf"
VERSION = "1.0.7"
GITHUB_URL = "https://github.com/XxdMkbMark/Shawarma-Legend-Utils"

# 玛德，你特么写一个切换语言结果，切换的语言的呢？？？？？？？？？？？？？？
LANGUAGES = {
    "english": None,
    "chinese": None
}

files = ["locales/en.json","locales/zh.json"]

if all(os.path.exists(f) for f in files):
    print("Translation file already exists. Skip downloading.")
else:
    print("The localization file does not exist. The localization file on the server is about to be downloaded.")
    


current_language = "english"
absPath = os.getcwd()

def get_translation(key):
    """Get translated string for current language"""
    return LANGUAGES[current_language].get(key, key)

def clearConsole():
    """Clear the console screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def log(status, message):
    """Log messages with different status levels"""
    status_colors = {
        "info": Back.BLUE,
        "warn": Back.YELLOW,
        "error": Back.RED
    }
    print(status_colors.get(status, "") + f"[{status.upper()}]" + Style.RESET_ALL + " " + message)

def optionInput(input_type):
    """Get user input with appropriate prompt"""
    prompts = {
        "index": get_translation("prompts")["choose_option"],
        "value": get_translation("prompts")["enter_value"],
        "hotkey": get_translation("prompts")["enter_hotkey"]
    }
    return input(Fore.LIGHTCYAN_EX + prompts.get(input_type, "") + Style.RESET_ALL)

def init():
    """Initialize the application"""
    clearConsole()
    global absPath, current_language
    absPath = os.getcwd()
    
    
    if not os.path.exists(os.path.join(absPath, CONFIG_FILE)):
        log("warn", get_translation("messages")["config_not_found"])
        time.sleep(1)
        
        default_config = [
            "language=english",
            "worker=1",
            "burrito-machine=1",
            "warpping-machine=1",
            "ingredients-click-count=1",
            "grilling-pan=1",
            "cup=1",
            "soda-machine=1",
            "frier=1",
            "potato-slicer=1",
            "shawarma-slicer=1",
            "forth-customer=false",
            "ingredients-customization=false",
            "first-time-use=true"
        ]
        
        try:
            with open(os.path.join(absPath, CONFIG_FILE), "w") as f:
                f.write("\n".join(default_config))
            
           
            with open(os.path.join(absPath, HOTKEY_FILE), "w") as f:
                pass
                
            if not os.path.exists(os.path.join(absPath, CONFIG_FILE)):
                raise IOError("Config file creation failed")
                
        except Exception as e:
            log("error", get_translation("messages")["config_error"])
            print(get_translation("messages")["press_any_key"] + "quit...")
            msvcrt.getch()
            sys.exit(1)
    
    
    lang = readCurrentValue(CONFIG_FILE, "language")
    if lang in LANGUAGES:
        current_language = lang

def readCurrentValue(filename, option):
    """Read a value from config file"""
    filepath = os.path.join(absPath, filename)
    try:
        with open(filepath, 'r') as f:
            for line in f:
                if line.startswith(option):
                    return line.split("=")[1].strip()
    except FileNotFoundError:
        return None

def insertLines(filename, line_number, content):
    """Insert or replace a line in a file"""
    filepath = os.path.join(absPath, filename)
    try:
        with open(filepath, 'r') as f:
            lines = f.readlines()
        
        if 0 <= line_number < len(lines):
            lines[line_number] = content + '\n'
        else:
            log("error", get_translation("messages")["internal_error"])
            time.sleep(1)
            sys.exit(1)
            
        with open(filepath, 'w') as f:
            f.writelines(lines)
    except Exception as e:
        log("error", f"Error modifying file: {str(e)}")

def printTitle():
    """Print the application title"""
    print(Fore.LIGHTBLUE_EX + f"        {get_translation('title')}        " + Style.RESET_ALL)
    print(get_translation("description"))

def mainMenu():
    """Display the main menu"""
    while True:
        clearConsole()
        printTitle()
        print(Fore.LIGHTGREEN_EX + "----------------- [Main Menu] ----------------" + Style.RESET_ALL)
        
        for i, option in enumerate(get_translation("menu_options"), 1):
            print(f"{i}]. {option}")
        
        option = optionInput("index")
        
        if option == "1":
            start()
        elif option == "2":
            settings()
        elif option == "3":
            log("info", get_translation("messages")["exiting"])
            time.sleep(0.4)
            sys.exit(0)
        elif option == "4":
            about()
        else:
            log("error", get_translation("messages")["invalid_option"])
            time.sleep(0.7)

def start():
    """Start the main functionality"""
    clearConsole()
    flag = readCurrentValue(CONFIG_FILE, "first-time-use")
    if flag == "true":
        firstTimeUseGuide()

def firstTimeUseGuide():
    """Guide for first-time users"""
    clearConsole()
    printTitle()
    print(Fore.LIGHTGREEN_EX + "----------- [First time use guide] -----------" + Style.RESET_ALL)
    print(get_translation("messages")["first_time_guide"])
    print(get_translation("prompts")["continue"])
    
    option = optionInput("index")
    if option.lower() != 'y':
        mainMenu()
    

def settings():
    """Display and handle settings menu"""
    while True:
        clearConsole()
        if not os.path.exists(os.path.join(absPath, CONFIG_FILE)):
            log("error", get_translation("messages")["config_not_found"])
            print(get_translation("messages")["press_any_key"] + "continue...")
            msvcrt.getch()
            return mainMenu()
            
        printTitle()
        print(Fore.LIGHTGREEN_EX + "----------------- [Settings] -----------------" + Style.RESET_ALL)
        
        for i, option in enumerate(get_translation("settings_options"), 1):
            print(f"{i}]. {option}")
        
        option = optionInput("index")
        
        try:
            option_num = int(option)
            if 1 <= option_num <= 13:
                optionAdjust(option_num)
            elif option_num == 14:
                return mainMenu()
            else:
                log("error", get_translation("messages")["invalid_option"])
                time.sleep(0.7)
        except ValueError:
            log("error", get_translation("messages")["invalid_option"])
            time.sleep(0.7)

def optionAdjust(index):
    """Adjust specific settings"""
    while True:
        clearConsole()
        printTitle()
        print(Fore.LIGHTGREEN_EX + "----------------- [Settings] -----------------" + Style.RESET_ALL)
        
        if index == 1:  
            print(f"[{get_translation('settings_options')[0]}]")
            print(f"Current value: {readCurrentValue(CONFIG_FILE, 'language')}\n")
            
            for i, lang in enumerate(get_translation("language_options"), 1):
                print(f"{i}]. {lang}")
            print(f"\n{len(get_translation('language_options')) + 1}]. Back")
            
            option = optionInput("index")
            
            if option == "1":
                insertLines(CONFIG_FILE, 0, "language=english")
                global current_language
                current_language = "english"
                return
            elif option == "2":
                insertLines(CONFIG_FILE, 0, "language=chinese")
                current_language = "chinese"
                return
            elif option == "3":
                return
            else:
                log("error", get_translation("messages")["invalid_option"])
                time.sleep(0.7)
                
        elif index == 12:  
            print(f"[{get_translation('settings_options')[11]}]")
            print(f"Current value: {readCurrentValue(CONFIG_FILE, 'forth-customer')}\n")
            
            for i, opt in enumerate(get_translation("toggle_options"), 1):
                print(f"{i}]. {opt}")
            print(f"\n{len(get_translation('toggle_options')) + 1}]. Back")
            
            option = optionInput("index")
            
            if option == "1":
                insertLines(CONFIG_FILE, 11, "forth-customer=true")
                return
            elif option == "2":
                insertLines(CONFIG_FILE, 11, "forth-customer=false")
                return
            elif option == "3":
                return
            else:
                log("error", get_translation("messages")["invalid_option"])
                time.sleep(0.7)
                
        elif index == 13:  
            print(f"[{get_translation('settings_options')[12]}]")
            print(f"Current value: {readCurrentValue(CONFIG_FILE, 'ingredients-customization')}\n")
            
            for i, opt in enumerate(get_translation("toggle_options"), 1):
                print(f"{i}]. {opt}")
            print(f"\n{len(get_translation('toggle_options')) + 1}]. Back")
            
            option = optionInput("index")
            
            if option == "1":
                insertLines(CONFIG_FILE, 12, "ingredients-customization=true")
                return
            elif option == "2":
                insertLines(CONFIG_FILE, 12, "ingredients-customization=false")
                return
            elif option == "3":
                return
            else:
                log("error", get_translation("messages")["invalid_option"])
                time.sleep(0.7)
                
        elif 2 <= index <= 11:  
            option_names = [
                "worker", "burrito-machine", "warpping-machine", 
                "ingredients-click-count", "grilling-pan", "cup", 
                "soda-machine", "frier", "potato-slicer", "shawarma-slicer"
            ]
            option_key = option_names[index-2]
            
            current_value = readCurrentValue(CONFIG_FILE, option_key)
            if current_value is None:
                log("error", get_translation("messages")["config_incorrect"])
                return settings()
                
            print(f"[{get_translation('settings_options')[index-1]}]")
            print(f"Current value: {current_value}\n")
            
            new_value = optionInput("value")
            insertLines(CONFIG_FILE, index-1, f"{option_key}={new_value}")
            return
        else:
            log("error", "It seems like that this option doesn't exist. If you believe this is a bug, please report it on Github.")
            time.sleep(2)
            return settings()

def about():
    """Display about information"""
    while True:
        clearConsole()
        printTitle()
        print(Fore.LIGHTGREEN_EX + "------------------- [About] ------------------" + Style.RESET_ALL)
        print(f"Version: {VERSION}")
        print("Made by XxdMkb_Mark using Python")
        print(f"Github repository: {GITHUB_URL}\n")
        print("1]. Back")
        
        option = optionInput("index")
        if option == "1":
            return mainMenu()
        else:
            log("error", get_translation("messages")["invalid_option"])
            time.sleep(0.7)


if __name__ == "__main__":
    init()
    time.sleep(0.5)
    mainMenu()