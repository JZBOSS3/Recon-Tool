import os
import sys
import subprocess
from colorama import Style, Fore
from urllib.parse import urlparse

domain = '<domain>'
file = '<file>'
quiet = False

def refresh():
    # Clear command as function of OS
    command = 'cls' if os.name == 'nt' else 'clear'
    os.system(command)

def get_user_entry():
    entry = input().strip().lower()
    return entry  # Return the entered value

def print_ascii():
    ascii_txt = r"""
 ____                        _                        
|  _ \  ___  _ __ ___   __ _(_)_ __                   
| | | |/ _ \| '_ ` _ \ / _` | | '_ \                  
| |_| | (_) | | | | | | (_| | | | | |                 
|____/ \___/|_| |_| |_|\__,_|_|_|_|_| _           _   
/ ___|  ___ _ __ ___  ___ _ __ / ___|| |__   ___ | |_ 
\___ \ / __| '__/ _ \/ _ \ '_ \\___ \| '_ \ / _ \| __|
 ___) | (__| | |  __/  __/ | | |___) | | | | (_) | |_ 
|____/ \___|_|  \___|\___|_| |_|____/|_| |_|\___/ \__|"""
    print(Fore.GREEN + ascii_txt + Style.RESET_ALL)

def print_banner():
    print(Fore.BLACK + '*'*50 + Style.RESET_ALL)
    print(Fore.WHITE + 'run\t\t\tTo run the tool' + Style.RESET_ALL)
    print(Fore.WHITE + 'show options\t\tTo show all information about tool params' + Style.RESET_ALL)
    print(Fore.WHITE + 'set <param> <value>\tTo set a param with a value' + Style.RESET_ALL)
    print(Fore.WHITE + 'usage\t\t\tShow Usage Examples' + Style.RESET_ALL)
    print(Fore.WHITE + 'back\t\t\tTo go back to the main menu' + Style.RESET_ALL)
    print(Fore.WHITE + 'clear\t\t\tTo clear the terminal' + Style.RESET_ALL)
    print(Fore.WHITE + 'quit\t\t\tTo quit the tool' + Style.RESET_ALL)
    print(Fore.BLACK + '*'*50 + Style.RESET_ALL)

def print_options_menu():
    print(Fore.BLACK + '*'*50 + Style.RESET_ALL)
    print(Fore.WHITE + f'Domain\t{domain}\tDomain to ScreenShot' + Style.RESET_ALL)
    print(Fore.WHITE + f'File\t{file}\tFile Containing Domains to ScreenShot' + Style.RESET_ALL)
    print(Fore.WHITE + f'Quiet\t{quiet}\tQuiet Mode' + Style.RESET_ALL)
    print(Fore.BLACK + '*'*50 + Style.RESET_ALL)

def print_usage_examples():
    print(Fore.BLACK + '*'*50 + Style.RESET_ALL)
    print(Fore.LIGHTGREEN_EX + 'set domain https://example.com' + Style.RESET_ALL)
    print(Fore.LIGHTGREEN_EX + 'set file domains.txt' + Style.RESET_ALL)
    print(Fore.LIGHTGREEN_EX + 'set quiet true' + Style.RESET_ALL)
    print(Fore.BLACK + '*'*50 + Style.RESET_ALL)

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False
def take_screenshot(domains_file, flag= ''):
        try:
            subprocess.run(f'cat {domains_file} | aquatone {flag}', shell=True)
        except FileNotFoundError:
            print(Fore.RED + 'aquatone tool is not installed or not found in PATH.' + Style.RESET_ALL)

def run_tool():
    if not quiet:
        if file == '<file>' and domain != '<domain>':
            with open('domain.txt', 'w') as f:
                f.write(domain + '\n')
            take_screenshot('domain.txt')
        elif file != '<file>' and domain == '<domain>':
            take_screenshot(file)
        else:
            print(Fore.RED + 'Choose 1 Option' + Style.RESET_ALL)
    else:
        if file == '<file>' and domain != '<domain>':
            with open('domain.txt', 'w') as f:
                f.write(domain + '\n')
            take_screenshot('domain.txt', '-silent')
        elif file != '<file>' and domain == '<domain>':
            take_screenshot(file, '-silent')
        else:
            print(Fore.RED + 'Choose 1 Option' + Style.RESET_ALL)


def start_tool():
    global domain, file, quiet
    print_ascii()
    print(Fore.WHITE + 'Welcome To Domain ScreenShotter' + Style.RESET_ALL)
    print(Fore.LIGHTBLACK_EX + "Enter help for Help Menu" + Style.RESET_ALL)
    while True:
        print(Fore.WHITE + 'Enter your command:' + Style.RESET_ALL, end=' ')
        user_input = get_user_entry().lower().strip()
        if user_input == 'run':
            run_tool()
        elif user_input == 'help':
            print_banner()
        elif user_input == 'usage':
            print_usage_examples()
        elif user_input == 'back':
            refresh()
            subprocess.run(['python3', 'recon.py'])
            sys.exit()
        elif user_input == 'clear':
            refresh()
        elif user_input == 'quit':
            sys.exit()
        elif len(user_input.split(' ')) >= 2:
            parts = user_input.split(' ')
            if parts[0] not in ['show', 'set']:
                print(Fore.RED + 'Enter a Valid Command' + Style.RESET_ALL)
                break
            elif parts[0] == 'show' and parts[1] == 'options':
                print_options_menu()
            elif parts[0] == 'set':
                opt = parts[1].lower()
                valid_option = opt in ['domain', 'file', 'quiet']
                if valid_option:
                    option = parts[2]
                    if opt == 'domain':
                        if is_valid_url(option):
                            domain = option
                        else:
                            print(Fore.RED + f'{option} is not a valid domain!' + Style.RESET_ALL)
                    elif opt == 'file':
                        file = option
                    elif opt == 'quiet':
                        value = parts[2].lower()
                        if value == 'true':
                            quiet = True
                        elif value == 'false':
                            quiet = False
                        else:
                            print(Fore.RED + 'Enter a Valid Value' + Style.RESET_ALL)
                    else:
                        print(Fore.RED + 'Enter a Valid Options' + Style.RESET_ALL)                                                
        else:
            print(Fore.RED + "Invalid command. Please enter a valid command." + Style.RESET_ALL)        


if __name__ == "__main__":
    try:
        start_tool()
    except KeyboardInterrupt:
        subprocess.run(['python', 'tools/ip_locate.py'])