import os
import sys
import whois
import subprocess
from colorama import Fore, Style

url = '<url>'
dirFile = '<file>'
outpFile = '<file>'
quiet = False

def refresh():
    # Clear command as function of OS
    command = 'cls' if os.name == 'nt' else 'clear'
    os.system(command)

def get_user_entry():
    entry = input().strip().lower()
    return entry  # Return the entered value

def print_ascii():
    ascii_text = r"""
$$\      $$\$$\               $$$$$$\                          
$$ | $\  $$ $$ |              \_$$  _|                         
$$ |$$$\ $$ $$$$$$$\  $$$$$$\   $$ |  $$$$$$$\                 
$$ $$ $$\$$ $$  __$$\$$  __$$\  $$ | $$  _____|                
$$$$  _$$$$ $$ |  $$ $$ /  $$ | $$ | \$$$$$$\                  
$$$  / \$$$ $$ |  $$ $$ |  $$ | $$ |  \____$$\                 
$$  /   \$$ $$ |  $$ \$$$$$$  $$$$$$\$$$$$$$  |                
\__/     \__\__|  \__|\______/\______\_______/                 
$$$$$$$$\           $$\                                $$\     
$$  _____|          $$ |                               $$ |    
$$ |     $$\   $$\$$$$$$\   $$$$$$\ $$$$$$\  $$$$$$$\$$$$$$\   
$$$$$\   \$$\ $$  \_$$  _| $$  __$$\\____$$\$$  _____\_$$  _|  
$$  __|   \$$$$  /  $$ |   $$ |  \__$$$$$$$ $$ /       $$ |    
$$ |      $$  $$<   $$ |$$\$$ |    $$  __$$ $$ |       $$ |$$\ 
$$$$$$$$\$$  /\$$\  \$$$$  $$ |    \$$$$$$$ \$$$$$$$\  \$$$$  |
\________\__/  \__|  \____/\__|     \_______|\_______|  \____/ 
"""
    print(Fore.GREEN + ascii_text + Style.RESET_ALL)

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
    print(Fore.WHITE + f'URL\t{url}\tURL to get WHOIS Info(example.com)' + Style.RESET_ALL)
    print(Fore.WHITE + f'DirFile\t{dirFile}\tFile Containing URLs To Scan [OPTIONAL]' + Style.RESET_ALL)
    print(Fore.WHITE + f'OutFile\t{outpFile}\tFile To Print Result To' + Style.RESET_ALL)
    print(Fore.WHITE + f'Quiet\t{quiet}\tQuiet Mode' + Style.RESET_ALL)
    print(Fore.BLACK + '*'*50 + Style.RESET_ALL)

def get_whois_info(domain):
    try:
        # Construct the WHOIS command based on the operating system
        command = f'whois {domain}'
        # Execute the WHOIS command
        result = os.popen(command).read()
        if outpFile != '<file>':
            try:
                with open(outpFile, mode='a') as file:
                    file.write(f'WhoIs Results for {domain}\n')
                    file.write(result + '\n')
            except IOError:
                print(Fore.RED + f'Error While Writing to {outpFile}' + Style.RESET_ALL)
            except Exception as e:
                print(Fore.RED + f'Exception\n{e}' + Style.RESET_ALL)
        return result
    except Exception as e:
        return f"An error occurred: {e}"
    
def run_tool():
    if dirFile == '<file>' and not quiet:
        whois_result = get_whois_info(url.strip())
        print(Fore.CYAN + f'WhoIs Results for {url}' + Style.RESET_ALL)
        print(whois_result)
    else:
        try:
            with open(dirFile, mode='r') as file:
                for line in file:
                    whois_result = get_whois_info(line.strip())
                    if not quiet:
                        print(Fore.CYAN + f'WhoIs Results for {line}' + Style.RESET_ALL)
                        print(whois_result)
        except IOError:
                print(Fore.RED + f'Something Happened While Reading {dirFile}' + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f'Something Happened:\n {e}' + Style.RESET_ALL)


def start_tool():
    global url, dirFile, outpFile, quiet
    print_ascii()
    print(Fore.WHITE + 'Welcome To WhoIs Extractor' + Style.RESET_ALL)
    print(Fore.LIGHTBLACK_EX + "Enter help for Help Menu" + Style.RESET_ALL)
    while True:
        print(Fore.WHITE + 'Enter your command:' + Style.RESET_ALL, end=' ')
        user_input = get_user_entry().lower()
        if user_input.strip() == 'run':
            run_tool()
        elif user_input.strip() == 'help':
            print_banner()
        elif user_input.strip() == 'back':
            subprocess.run(['python', 'recon.py'])
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
                if option not in ['url', 'dirfile', 'outfile', 'quiet']:
                    print(Fore.RED + 'Enter a Valid Command' + Style.RESET_ALL)
                else:
                    if option == 'url':
                        url = parts[2]
                    elif option == 'dirfile':
                        dirFile = parts[2]
                    elif option == 'outfile':
                        outpFile = parts[2]
                    elif option == 'quiet':
                        value = parts[2].lower()
                        if value == 'true':
                            quiet = True
                        else:
                            quiet = False
                    else:
                        print(Fore.RED + 'Enter a Valid Option' + Style.RESET_ALL)

        else:
            print(Fore.RED + 'Invalid Command. Please enter a valid command' + Style.RESET_ALL)

if __name__ == "__main__":
    try:
        start_tool()
    except KeyboardInterrupt:
        print('',end='')
