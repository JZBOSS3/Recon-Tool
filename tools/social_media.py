import requests
import sys
import os
import subprocess
from colorama import Fore, Style
from bs4 import BeautifulSoup

url = '<url>'
dirFile = '<file>'
outpFile = '<file>'

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
$$\   $$\                                               $$\     
$$ |  $$ |                                              $$ |    
$$ |  $$ |$$$$$$\  $$$$$$\$$\    $$\ $$$$$$\  $$$$$$$\$$$$$$\   
$$$$$$$$ |\____$$\$$  __$$\$$\  $$  $$  __$$\$$  _____\_$$  _|  
$$  __$$ |$$$$$$$ $$ |  \__\$$\$$  /$$$$$$$$ \$$$$$$\   $$ |    
$$ |  $$ $$  __$$ $$ |      \$$$  / $$   ____|\____$$\  $$ |$$\ 
$$ |  $$ \$$$$$$$ $$ |       \$  /  \$$$$$$$\$$$$$$$  | \$$$$  |
\__|  \__|\_______\__|        \_/    \_______\_______/   \____/ 
 $$$$$$\                   $$\         $$\                      
$$  __$$\                  \__|        $$ |                     
$$ /  \__|$$$$$$\  $$$$$$$\$$\ $$$$$$\ $$ |                     
\$$$$$$\ $$  __$$\$$  _____$$ |\____$$\$$ |                     
 \____$$\$$ /  $$ $$ /     $$ |$$$$$$$ $$ |                     
$$\   $$ $$ |  $$ $$ |     $$ $$  __$$ $$ |                     
\$$$$$$  \$$$$$$  \$$$$$$$\$$ \$$$$$$$ $$ |                     
 \______/ \______/ \_______\__|\_______\__|"""
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
  print(Fore.BLACK + '*'*50 + Style.RESET_ALL)

def extract_social_media_profiles(url):
    # Send a request to the webpage
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to load page {url}: HTTP Code {response.status_code}")
    
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Define regex patterns for different social media platforms
    patterns = {
        'Facebook': r'https?://(www\.)?facebook\.com/[A-Za-z0-9_.-]+',
        'Twitter': r'https?://(www\.)?twitter\.com/[A-Za-z0-9_.-]+',
        'LinkedIn': r'https?://(www\.)?linkedin\.com/in/[A-Za-z0-9_.-]+',
        'Instagram': r'https?://(www\.)?instagram\.com/[A-Za-z0-9_.-]+',
        'YouTube': r'https?://(www\.)?youtube\.com/(channel|user|c)/[A-Za-z0-9_.-]+',
        'Pinterest': r'https?://(www\.)?pinterest\.com/[A-Za-z0-9_.-]+',
        'TikTok': r'https?://(www\.)?tiktok\.com/@[A-Za-z0-9_.-]+',
        'Snapchat': r'https?://(www\.)?snapchat\.com/add/[A-Za-z0-9_.-]+',
        'Reddit': r'https?://(www\.)?reddit\.com/user/[A-Za-z0-9_.-]+',
        'Tumblr': r'https?://[A-Za-z0-9_.-]+\.tumblr\.com',
        'GitHub': r'https?://(www\.)?github\.com/[A-Za-z0-9_.-]+',
        'Medium': r'https?://(www\.)?medium\.com/@[A-Za-z0-9_.-]+',
        'Vimeo': r'https?://(www\.)?vimeo\.com/[A-Za-z0-9_.-]+',
        'SoundCloud': r'https?://(www\.)?soundcloud\.com/[A-Za-z0-9_.-]+',
        'Pi Network': r'https?://(www\.)?minepi\.com/[A-Za-z0-9_.-]+',
        'Bitcoin': r'bitcoin:[13][a-km-zA-HJ-NP-Z1-9]{25,34}',
        'Linktree': r'https?://(www\.)?linktr\.ee/[A-Za-z0-9_.-]+'
    }
    
    # Find all links in the HTML
    links = soup.find_all('a', href=True)

    # Create an empty dictionary to store the social media profiles
    profiles = {}
    for platform in patterns.keys():
        profiles[platform] = []
    
    # Check each link to see if it matches any social media patterns
    for link in links:
        href = link['href']
        for platform, pattern in patterns.items():
            if re.match(pattern, href):
                profiles[platform].append(href)
    
    return profiles

def print_to_file(url, profiles):
    try:
        with open(outpFile, mode='a') as file:
            file.write(f'{url} Scan Result:\n')
            urls = []
            for platform, links in profiles.items():
                file.write(f"{platform} profiles:\n")
                can_print = True
                for link in links:
                    for url in urls:
                        if url == link:
                           can_print = False
                    if can_print:
                       file.write(f"  - {link}\n")
                       urls.append(link)
            file.write('\n')
                       
    except IOError:
       print(Fore.RED + f'Error writing to {outpFile}' + Style.RESET_ALL)
           

def print_results(url, profiles):
    printed_profiles = []
    if outpFile != '<file>':
        print_to_file(url, profiles)
    for platform, links in profiles.items():
        can_print = True
        print(f"{platform} profiles:")
        for link in links:
            for profile in printed_profiles:
                if profile == link:
                    can_print = False
            if can_print:
                print(f"  - {link}")
                printed_profiles.append(link)

def run_tool():
    global url
    if dirFile == '<file>':
        profiles = extract_social_media_profiles(url)
        print(Fore.GREEN + f'{url} Scan Results' + Style.RESET_ALL)
        print_results(url, profiles)
    else:
        try:
            with open(dirFile, mode='r') as file:
                for line in file:
                    profiles = extract_social_media_profiles(line)
                    print(Fore.GREEN + f'{line} Scan Results' + Style.RESET_ALL)
                    print_results(line, profiles)    
        except IOError:
            print(Fore.RED + f'Error While reading {dirFile}' + Style.RESET_ALL)
        except Exception as e:
           print(Fore.RED + f'Exception\n{e}' + Style.RESET_ALL)

def start_tool():
  global url, dirFile, outpFile
  print_ascii()
  print(Fore.WHITE + 'Welcome To Socials Harvester' + Style.RESET_ALL)
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
        if option not in ['url', 'dirfile', 'outfile']:
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
    else:
      print(Fore.RED + 'Enter a Valid Command' + Style.RESET_ALL)

if __name__ == "__main__":
  try:
    start_tool()
  except KeyboardInterrupt:
    print('',end='')