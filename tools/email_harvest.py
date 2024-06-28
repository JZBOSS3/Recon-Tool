import requests
import sys
import os
import re #regular expression => search for common expressions in strings,....
import subprocess
from urllib.parse import urljoin, urlparse
from colorama import Fore, Style
from bs4 import BeautifulSoup

url = '<url>'
dirFile = '<file>'
outpFile = '<file>'
verbose = False
discovered_mails = []

def refresh():
  # Clear command as function of OS
  command = 'cls' if os.name == 'nt' else 'clear'
  os.system(command)

def get_user_entry():
  entry = input().strip().lower()
  return entry  # Return the entered value

def print_ascii():
    ascii_text = r"""
 _______   _____ ______   ________  ___  ___                                                      
|\  ___ \ |\   _ \  _   \|\   __  \|\  \|\  \                                                     
\ \   __/|\ \  \\\__\ \  \ \  \|\  \ \  \ \  \                                                    
 \ \  \_|/_\ \  \\|__| \  \ \   __  \ \  \ \  \                                                   
  \ \  \_|\ \ \  \    \ \  \ \  \ \  \ \  \ \  \____                                              
   \ \_______\ \__\    \ \__\ \__\ \__\ \__\ \_______\                                            
 ___\|_______|\|__|  ___\|__|\|__|\|__|\|__|\|_______|________  _________  _______   ________     
|\  \|\  \|\   __  \|\   __  \|\  \    /  /|\  ___ \ |\   ____\|\___   ___|\  ___ \ |\   __  \    
\ \  \\\  \ \  \|\  \ \  \|\  \ \  \  /  / \ \   __/|\ \  \___|\|___ \  \_\ \   __/|\ \  \|\  \   
 \ \   __  \ \   __  \ \   _  _\ \  \/  / / \ \  \_|/_\ \_____  \   \ \  \ \ \  \_|/_\ \   _  _\  
  \ \  \ \  \ \  \ \  \ \  \\  \\ \    / /   \ \  \_|\ \|____|\  \   \ \  \ \ \  \_|\ \ \  \\  \| 
   \ \__\ \__\ \__\ \__\ \__\\ _\\ \__/ /     \ \_______\____\_\  \   \ \__\ \ \_______\ \__\\ _\ 
    \|__|\|__|\|__|\|__|\|__|\|__|\|__|/       \|_______|\_________\   \|__|  \|_______|\|__|\|__|
                                                        \|_________|                              
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
  print(Fore.WHITE + f'URL\t{url}\tURL to Extract Email Addresses from' + Style.RESET_ALL)
  print(Fore.WHITE + f'DirFile\t{dirFile}\tFile Containing URLS To Scan [OPTIONAL]' + Style.RESET_ALL)
  print(Fore.WHITE + f'OutFile\t{outpFile}\tFile To Print Result To' + Style.RESET_ALL)
  print(Fore.WHITE + f'Verbose\t{verbose}\tVerbose Mode' + Style.RESET_ALL)
  print(Fore.BLACK + '*'*50 + Style.RESET_ALL)

def good_url(url):
    return 'https://' in url or 'http://' in url

def get_html_code(url):
  try:
    response = requests.get(url)
    response_html_code = response.text
    return response_html_code
  except Exception:
    pass

def get_emails(url, response_html_code):
  global discovered_mails
  try:
    # Regular expression to find email addresses
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    emails = re.findall(email_pattern, response_html_code)
    if emails:
      #store emails
      for email in emails:
        discoverd = False
        for discovered_mail in discovered_mails:
          if discovered_mail == email:
            discoverd = True
        if not discoverd:
          discovered_mails.append(email)
        if verbose:
          # Print the list of email addresses found
          print(Fore.CYAN + f'Scanning {url}' + Style.RESET_ALL)
          print(Fore.LIGHTBLACK_EX + '*'*50 + Style.RESET_ALL)
          for mail in discovered_mails:
            print(Fore.WHITE + mail + Style.RESET_ALL)
          print(Fore.LIGHTBLACK_EX + '*'*50 + Style.RESET_ALL)
          if outpFile != '<file>':
            try:
              with open(outpFile, mode='a') as file:
                file.write(f'Scanning {url}\n')
                file.write('*'*50 + '\n')
                for mail in discovered_mails:
                  file.write(mail + '\n')
                file.write('*'*50 + '\n')
            except IOError:
              print(Fore.RED + f'Error While Writing to {outpFile}' + Style.RESET_ALL)

    else:
      print(Fore.CYAN + f'Scanning {url}' + Style.RESET_ALL)
      print(Fore.LIGHTBLACK_EX + '*'*50 + Style.RESET_ALL)
      print(Fore.WHITE + 'No Email Address Found' + Style.RESET_ALL)
      print(Fore.LIGHTBLACK_EX + '*'*50 + Style.RESET_ALL)
      if outpFile != '<file>':
        try:
          with open(outpFile, mode='a') as file:
            file.write(f'Scanning {url}\n')
            file.write('*'*50 + '\n')
            file.write('No Email Address Found\n')
            file.write('*'*50 + '\n')
        except IOError:
              print(Fore.RED + f'Error While Writing to {outpFile}' + Style.RESET_ALL)
  except Exception:
    pass

def get_pages(url, response_html_code):
    soup = BeautifulSoup(response_html_code, 'html.parser')
    links = soup.find_all('a', href=True)
    page_links = []
    for link in links:
      href = link['href']
      parsed_href = urlparse(href)
      # path = parsed_href.path
      #if path.endswith(('.html', '.css', '.js')):
      full_url = urljoin(url, href)
      page_links.append(full_url)
    if page_links != []:
      for link in page_links:
        get_emails(link, get_html_code(link))

def get_urls(response_html_code):
  #url pattern regex
  url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
  urls = re.findall(url_pattern, response_html_code)
  if urls:
    for url in urls:
      html_code = get_html_code(url)
      get_emails(url, html_code)

def print_mails():
  # Print the list of email addresses found
  print(Fore.CYAN + f'Result For {url} Scan' + Style.RESET_ALL)
  print(Fore.LIGHTBLACK_EX + '*'*50 + Style.RESET_ALL)
  for mail in discovered_mails:
    print(Fore.WHITE + mail + Style.RESET_ALL)
  print(Fore.LIGHTBLACK_EX + '*'*50 + Style.RESET_ALL)

def run_tool():
  global url
  if dirFile == '<file>':
    response_html_code = get_html_code(url)
    get_emails(url, response_html_code)
    get_pages(url, response_html_code)
    get_urls(response_html_code) 
    print_mails()
  else:
    try:
      with open(dirFile, mode='r') as file:
        for url in file:
          url = url.strip()
          response_html_code = get_html_code(url)
          get_emails(url, response_html_code)
          get_pages(url, response_html_code)
          get_urls(response_html_code) 
          print_mails()
    except IOError:
      print(Fore.RED + f'Error Reading {dirFile}' + Style.RESET_ALL)
    except Exception:
      print(Fore.RED + f'Error Reading {dirFile}' + Style.RESET_ALL)

def start_tool():
  global url, dirFile, outpFile, verbose
  print_ascii()
  print(Fore.WHITE + 'Welcome To Email Harvester' + Style.RESET_ALL)
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
        if option not in ['url', 'dirfile', 'outfile', 'verbose']:
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
          elif option == 'verbose':
            value = parts[2]
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