import requests
import sys
import subprocess
import os
import socket
from colorama import Style, Fore

url = '<url>'
dirFile = 'wordlists/Directories/common.txt'
outpFile = '<file>'
write = False
verbose = False
quiet = False

def refresh():
    # Clear command as function of OS
    command = 'cls' if os.name == 'nt' else 'clear'
    os.system(command)

def get_user_entry():
    entry = input().strip().lower()
    return entry  # Return the entered value

def print_ascii():
    folder_ascii = r"""
 ____  ____  _   _ _____ _____                              
| __ )|  _ \| | | |_   _| ____|                             
|  _ \| |_) | | | | | | |  _|                               
| |_) |  _ <| |_| | | | | |___                              
|____/|_| \_\\___/__|_|_|_____|_ ___  ____  ___ _____ ____  
|  _ \_ _|  _ \| ____/ ___|_   _/ _ \|  _ \|_ _| ____/ ___| 
| | | | || |_) |  _|| |     | || | | | |_) || ||  _| \___ \ 
| |_| | ||  _ <| |__| |___  | || |_| |  _ < | || |___ ___) |
|____/___|_| \_\_____\____| |_| \___/|_| \_\___|_____|____/     
"""
    print(Fore.GREEN + folder_ascii + Style.RESET_ALL)

def print_banner():
    print(Fore.BLACK + '*'*50 + Style.RESET_ALL)
    print(Fore.WHITE + 'run\t\t\tTo run the tool' + Style.RESET_ALL)
    print(Fore.WHITE + 'show options\t\tTo show all information about tool params' + Style.RESET_ALL)
    print(Fore.WHITE + 'set <param> <value>\tTo set a param with a value' + Style.RESET_ALL)
    print(Fore.WHITE + 'back\t\t\tTo go back to the main menu' + Style.RESET_ALL)
    print(Fore.WHITE + 'clear\t\t\tTo clear the terminal' + Style.RESET_ALL)
    print(Fore.WHITE + 'quit\t\t\tTo quit the tool' + Style.RESET_ALL)
    print(Fore.BLACK + '*'*50 + Style.RESET_ALL)

def print_options_menu():
    print(Fore.BLACK + '*'*50 + Style.RESET_ALL)
    print(Fore.WHITE + f'URL\t{url}\tURL to Brute Force' + Style.RESET_ALL)
    print(Fore.WHITE + f'DirFile\t{dirFile}\tFile Containing Directory Names [OPTIONAL]' + Style.RESET_ALL)
    print(Fore.WHITE + f'OutFile\t{outpFile}\tFile To Print Result To' + Style.RESET_ALL)
    print(Fore.WHITE + f'Verbose\t{verbose}\tVerbose Mode' + Style.RESET_ALL)
    print(Fore.WHITE + f'Quiet\t{quiet}\tQuiet Mode' + Style.RESET_ALL)
    print(Fore.BLACK + '*'*50 + Style.RESET_ALL)

def write_file(url, msg):
    global outpFile
    try:
        with open(outpFile, mode='a') as file:
            file.write(f'{url}{msg}\n')
    except IOError:
        print('Error Writing To The File... Try Again!')
    except Exception as e:
        print(f'Exception: {e}')

def run_tool():
    global url, dirFile, outpFile, verbose, quiet
    try:
        with open(dirFile, mode='r') as dirFile:
            for line in dirFile:
                dir = line.strip()
                base_url = f'{url}/{dir}'
                response = requests.get(base_url)
                if not quiet:
                    if response.status_code == 200:
                        print(Fore.GREEN + f'{base_url}: Code 200' + Style.RESET_ALL)
                        if outpFile != '<file>':
                            write_file(base_url, ': Code 200')
                    if verbose:    
                        if response.status_code == 301:
                            print(Fore.LIGHTBLACK_EX + f'{base_url}: Code 301' + Style.RESET_ALL)
                            if outpFile != '<file>':
                                write_file(base_url, ': Code 301')
                        elif response.status_code == 404:
                            print(Fore.RED + f'{base_url}: Code 404' + Style.RESET_ALL)
                            if outpFile != '<file>':
                                write_file(base_url, ': Code 404')
                        else:
                            print(Fore.LIGHTYELLOW_EX + f'{base_url}: Code {response.status_code}' + Style.RESET_ALL)
                            if outpFile != '<file>':
                                write_file(base_url, ': Code ' + str(response.status_code))
                    else:
                        if outpFile != '<file>':
                            write_file(url, ': Code ' + str(response.status_code))
    except FileNotFoundError:
        print(f"Error: File '{directories_file}' not found.")
    except requests.RequestException as e:
        print(f"Error: An error occurred with the request: {e}")
    except KeyboardInterrupt:
        file = dirFile
        print('Exiting Program...')
        dirFile = file
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def start_tool():
    global url, dirFile, outpFile, verbose, quiet
    print_ascii()
    print(Fore.WHITE + 'Welcome To Directory Brute Forcer' + Style.RESET_ALL)
    print(Fore.LIGHTBLACK_EX + "Enter help for Help Menu" + Style.RESET_ALL)
    while True:
        print(Fore.WHITE + 'Enter your command:' + Style.RESET_ALL, end=' ')
        user_input = get_user_entry().lower()
        if user_input.strip() == 'run':
            run_tool()
        elif user_input.strip() == 'back':
            refresh()
            subprocess.run(['python', 'recon.py'])
            break
        elif user_input.strip() in 'help':
            print_banner()
        elif user_input.strip() == 'clear':
            refresh()
        elif user_input.strip() == 'quit':
            sys.exit()
        elif len(user_input.split(' ')) >= 2:
            parts = user_input.split(' ')
            if parts[0] not in ['show', 'set']:
                print(Fore.RED + 'Enter a Valid Command' + Style.RESET_ALL)
                break
            elif parts[0] == 'show' and parts[1] == 'options':
                print_options_menu()
            elif parts[0] == 'set':
                option = parts[1].lower()
                valid_option = option in ['url', 'dirfile', 'outfile', 'verbose', 'quiet']
                if valid_option:
                    if option == 'url':
                        url = parts[2]
                    elif option == 'dirfile':
                        dirFile = parts[2]
                    elif option == 'outfile':
                        outpFile = parts[2]
                    elif option == 'verbose':
                        if parts[2].lower() == 'true':
                            verbose = True
                        else:
                            verbose = False
                    elif option == 'quiet':
                        if parts[2].lower() == 'true':
                            quiet = True
                        else:
                            quiet = False
                else:
                    print(Fore.RED + 'Option Not Available')
            else:
                print(Fore.RED + "Invalid command. Please enter a valid command." + Style.RESET_ALL)    
        else:
            print(Fore.RED + "Invalid command. Please enter a valid command." + Style.RESET_ALL)

if __name__ == "__main__":
    try:
        start_tool()
    except KeyboardInterrupt:
        print('',end='')
