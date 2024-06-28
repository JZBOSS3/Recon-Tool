import os
import sys
import requests
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

def good_url(url):
    return 'https://' not in url or 'http://' not in url

def print_ascii():
    ascii_txt = r"""
 _______   ________   ___  ___  _____ ______                                                   
|\  ___ \ |\   ___  \|\  \|\  \|\   _ \  _   \                                                 
\ \   __/|\ \  \\ \  \ \  \\\  \ \  \\\__\ \  \                                                
 \ \  \_|/_\ \  \\ \  \ \  \\\  \ \  \\|__| \  \                                               
  \ \  \_|\ \ \  \\ \  \ \  \\\  \ \  \    \ \  \                                              
   \ \_______\ \__\\ \__\ \_______\ \__\    \ \__\                                             
 ___\|_______|\|__| \|__|\|_______|\|__| ____\|__| _____ ______   ________  ___  ________      
|\   ____\|\  \|\  \|\   __  \|\   ___ \|\   __  \|\   _ \  _   \|\   __  \|\  \|\   ___  \    
\ \  \___|\ \  \\\  \ \  \|\ /\ \  \_|\ \ \  \|\  \ \  \\\__\ \  \ \  \|\  \ \  \ \  \\ \  \   
 \ \_____  \ \  \\\  \ \   __  \ \  \ \\ \ \  \\\  \ \  \\|__| \  \ \   __  \ \  \ \  \\ \  \  
  \|____|\  \ \  \\\  \ \  \|\  \ \  \_\\ \ \  \\\  \ \  \    \ \  \ \  \ \  \ \  \ \  \\ \  \ 
    ____\_\  \ \_______\ \_______\ \_______\ \_______\ \__\    \ \__\ \__\ \__\ \__\ \__\\ \__\
   |\_________\|_______|\|_______|\|_______|\|_______|\|__|     \|__|\|__|\|__|\|__|\|__| \|__|
   \|_________|"""
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
  print(Fore.WHITE + f'URL\t{url}\tURL to Extract Social Media Profiles from' + Style.RESET_ALL)
  print(Fore.WHITE + f'DirFile\t{dirFile}\tFile Containing URLS To Scan [OPTIONAL]' + Style.RESET_ALL)
  print(Fore.WHITE + f'OutFile\t{outpFile}\tFile To Print Result To' + Style.RESET_ALL)
  print(Fore.WHITE + f'Quiet\t{quiet}\tQuiet Mode' + Style.RESET_ALL)
  print(Fore.BLACK + '*'*50 + Style.RESET_ALL)

def find_subdomains(domain):
    # Define a public API for subdomain enumeration
    url = f'https://api.hackertarget.com/hostsearch/?q={domain}'
    
    # Send a request to the API
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data for {domain}")
    
    # Parse the response
    subdomains = response.text.split('\n')
    
    # Process and return the subdomains
    result = []
    for entry in subdomains:
        if entry:
            subdomain, ip = entry.split(',')
            result.append(subdomain)
    return result

def write_file(url, subdomains):
    try:
        with open(outpFile, mode='a') as file:
            file.write(f'{url} Enumeration\n')
            for domain in subdomains:
              file.write(f'https://{domain}\n')
              file.write(f'http://{domain}\n')
            file.write('\n')
    except IOError:
       print(Fore.RED + f'Error Writing {outpFile}' + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f'Error\n{e}' + Style.RESET_ALL)

def run_tool():
    if dirFile == '<file>':
        subdomains = find_subdomains(url.strip())
        if not quiet:
            print(Fore.CYAN + f"Subdomains of {url}:" + Style.RESET_ALL)
            for subdomain in subdomains:
                print(f"  - https://{subdomain}")
                print(f"  - http://{subdomain}")
        if outpFile != '<file>':
           write_file(url, subdomains)
    else:
        try:
            with open(dirFile, mode='r') as file:
                for line in file:
                    subdomains = find_subdomains(line.strip())
                    if not quiet:
                        print(Fore.CYAN + f"Subdomains of {line}:" + Style.RESET_ALL)
                        for subdomain in subdomains:
                            print(f"  - {subdomain}")
                    if outpFile != '<file>':
                        write_file(line, subdomains)
        except IOError:
           print(Fore.RED + f'Error Reading {dirFile}' + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f'Error\n{e}' + Style.RESET_ALL)

def start_tool():
  global url, dirFile, outpFile, quiet
  print_ascii()
  print(Fore.WHITE + 'Welcome To Subdomain Enumerator' + Style.RESET_ALL)
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
                    if(good_url(parts[2])):
                        url = parts[2]
                    else:
                        print(Fore.RED + 'Enter a Valid URL' + Style.RESET_ALL)
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
      print(Fore.RED + 'Enter a Valid Command' + Style.RESET_ALL)

if __name__ == "__main__":
    try:
        start_tool()
    except KeyboardInterrupt:
        print('',end='')