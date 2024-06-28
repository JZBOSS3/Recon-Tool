import requests
import sys
import os
import subprocess
from colorama import Fore, Style

dirFile = '<file>'
outpFile = '<file>'
quiet = False
verbose = False

def refresh():
  # Clear command as function of OS
  command = 'cls' if os.name == 'nt' else 'clear'
  os.system(command)

def get_user_entry():
  entry = input().strip().lower()
  return entry  # Return the entered value

def good_url(url):
    return 'https://' in url or 'http://' in url

def print_ascii():
    ascii_txt = r"""
  ______             __     __                                
 /      \           /  |   /  |                               
/$$$$$$  | _______ _$$ |_  $$/ __     __ ______               
$$ |__$$ |/       / $$   | /  /  \   /  /      \              
$$    $$ /$$$$$$$/$$$$$$/  $$ $$  \ /$$/$$$$$$  |             
$$$$$$$$ $$ |       $$ | __$$ |$$  /$$/$$    $$ |             
$$ |  $$ $$ \_____  $$ |/  $$ | $$ $$/ $$$$$$$$/              
$$ |  $$ $$       | $$  $$/$$ |  $$$/  $$       |             
$$/   $$/ $$$$$$$/   $$$$/ $$/    $/    $$$$$$$/              
 _______                                 __                   
/       \                               /  |                  
$$$$$$$  | ______  _____  ____   ______ $$/ _______   _______ 
$$ |  $$ |/      \/     \/    \ /      \/  /       \ /       |
$$ |  $$ /$$$$$$  $$$$$$ $$$$  |$$$$$$  $$ $$$$$$$  /$$$$$$$/ 
$$ |  $$ $$ |  $$ $$ | $$ | $$ |/    $$ $$ $$ |  $$ $$      \ 
$$ |__$$ $$ \__$$ $$ | $$ | $$ /$$$$$$$ $$ $$ |  $$ |$$$$$$  |
$$    $$/$$    $$/$$ | $$ | $$ $$    $$ $$ $$ |  $$ /     $$/ 
$$$$$$$/  $$$$$$/ $$/  $$/  $$/ $$$$$$$/$$/$$/   $$/$$$$$$$/"""
    print(Fore.GREEN + ascii_txt + Style.RESET_ALL)

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
  print(Fore.WHITE + f'DirFile\t{dirFile}\tFile Containing Domain To Scan [OPTIONAL]' + Style.RESET_ALL)
  print(Fore.WHITE + f'OutFile\t{outpFile}\tFile To Print Result To' + Style.RESET_ALL)
  print(Fore.WHITE + f'Quiet\t{quiet}\tQuiet Mode' + Style.RESET_ALL)
  print(Fore.WHITE + f'Verbose\t{verbose}\tVerbose Mode' + Style.RESET_ALL)
  print(Fore.BLACK + '*'*50 + Style.RESET_ALL)
    
def check_url_status(url):
    try:
        response = requests.head(url, allow_redirects=True, timeout=5)
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.ConnectionError:
        return False
    except requests.Timeout:
        return False
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return False

import requests
import sys
import os
import subprocess
from colorama import Fore, Style

dirFile = '<file>'
outpFile = '<file>'
quiet = False
verbose = False

def refresh():
  # Clear command as function of OS
  command = 'cls' if os.name == 'nt' else 'clear'
  os.system(command)

def get_user_entry():
  entry = input().strip().lower()
  return entry  # Return the entered value

def good_url(url):
    return 'https://' in url or 'http://' in url

def print_ascii():
    ascii_txt = r"""
  ______             __     __                                
 /      \           /  |   /  |                               
/$$$$$$  | _______ _$$ |_  $$/ __     __ ______               
$$ |__$$ |/       / $$   | /  /  \   /  /      \              
$$    $$ /$$$$$$$/$$$$$$/  $$ $$  \ /$$/$$$$$$  |             
$$$$$$$$ $$ |       $$ | __$$ |$$  /$$/$$    $$ |             
$$ |  $$ $$ \_____  $$ |/  $$ | $$ $$/ $$$$$$$$/              
$$ |  $$ $$       | $$  $$/$$ |  $$$/  $$       |             
$$/   $$/ $$$$$$$/   $$$$/ $$/    $/    $$$$$$$/              
 _______                                 __                   
/       \                               /  |                  
$$$$$$$  | ______  _____  ____   ______ $$/ _______   _______ 
$$ |  $$ |/      \/     \/    \ /      \/  /       \ /       |
$$ |  $$ /$$$$$$  $$$$$$ $$$$  |$$$$$$  $$ $$$$$$$  /$$$$$$$/ 
$$ |  $$ $$ |  $$ $$ | $$ | $$ |/    $$ $$ $$ |  $$ $$      \ 
$$ |__$$ $$ \__$$ $$ | $$ | $$ /$$$$$$$ $$ $$ |  $$ |$$$$$$  |
$$    $$/$$    $$/$$ | $$ | $$ $$    $$ $$ $$ |  $$ /     $$/ 
$$$$$$$/  $$$$$$/ $$/  $$/  $$/ $$$$$$$/$$/$$/   $$/$$$$$$$/"""
    print(Fore.GREEN + ascii_txt + Style.RESET_ALL)

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
  print(Fore.WHITE + f'DirFile\t{dirFile}\tFile Containing Domain To Scan [OPTIONAL]' + Style.RESET_ALL)
  print(Fore.WHITE + f'OutFile\t{outpFile}\tFile To Print Result To' + Style.RESET_ALL)
  print(Fore.WHITE + f'Quiet\t{quiet}\tQuiet Mode' + Style.RESET_ALL)
  print(Fore.WHITE + f'Verbose\t{verbose}\tVerbose Mode' + Style.RESET_ALL)
  print(Fore.BLACK + '*'*50 + Style.RESET_ALL)
    
def check_url_status(url):
    try:
        response = requests.head(url, allow_redirects=True, timeout=5)
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.ConnectionError:
        return False
    except requests.Timeout:
        return False
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return False

def run_tool():
    global dirFile, outpFile, verbose, quiet
    try:
        with open(dirFile, mode='r') as urls:
            for url in urls:
                url = url.strip()
                if good_url(url):
                    url_status = check_url_status(url)
                    if not quiet:
                        if url_status:
                            print(Fore.GREEN + url + Style.RESET_ALL)
                        if verbose:
                            if not url_status:
                                print(Fore.YELLOW + url + ' Not Active' + Style.RESET_ALL)
                    if outpFile != '<file>':
                        try:
                            with open(outpFile, mode='a') as file:
                                if url_status:
                                    file.write(url + '\n')
                                if verbose:
                                    if not url_status:
                                        file.write(url + ' Not Active\n')
                        except IOError:
                            print(Fore.RED + f'Error Writing to {outpFile}' + Style.RESET_ALL)
                        except Exception as e:
                            print(Fore.RED + f'Error:\n{e}' + Style.RESET_ALL)
    except IOError:
       print('EOROROROROROR')
    except Exception as e:
       print(e)

def start_tool():
  global url, dirFile, outpFile, quiet, verbose
  print_ascii()
  print(Fore.WHITE + 'Welcome To Active Domains' + Style.RESET_ALL)
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
            if option not in ['dirfile', 'outfile', 'quiet', 'verbose']:
                print(Fore.RED + 'Enter a Valid Command' + Style.RESET_ALL)
            else:
                if option == 'dirfile':
                    dirFile = parts[2]
                elif option == 'outfile':
                    outpFile = parts[2]
                elif option == 'quiet':
                    value = parts[2].lower()
                    if value == 'true':
                      quiet = True
                    else:
                       quiet = False
                elif option == 'verbose':
                    value = parts[2].lower()
                    if value == 'true':
                      verbose = True
                    else:
                       verbose = False
    else:
      print(Fore.RED + 'Enter a Valid Command' + Style.RESET_ALL)

if __name__ == "__main__":
    try:
        start_tool()
    except KeyboardInterrupt:
        print('',end='')

def start_tool():
  global url, dirFile, outpFile, quiet, verbose
  print_ascii()
  print(Fore.WHITE + 'Welcome To Active Domains' + Style.RESET_ALL)
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
            if option not in ['dirfile', 'outfile', 'quiet', 'verbose']:
                print(Fore.RED + 'Enter a Valid Command' + Style.RESET_ALL)
            else:
                if option == 'dirfile':
                    dirFile = parts[2]
                elif option == 'outfile':
                    outpFile = parts[2]
                elif option == 'quiet':
                    value = parts[2].lower()
                    if value == 'true':
                      quiet = True
                    else:
                       quiet = False
                elif option == 'verbose':
                    value = parts[2].lower()
                    if value == 'true':
                      verbose = True
                    else:
                       verbose = False
    else:
      print(Fore.RED + 'Enter a Valid Command' + Style.RESET_ALL)

if __name__ == "__main__":
    try:
        start_tool()
    except KeyboardInterrupt:
        print('',end='')