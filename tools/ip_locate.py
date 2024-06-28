import requests
import sys
import os
import subprocess
from colorama import Fore, Style

ip = '<ip>'
inp_file = '<file>'
out_file = '<file>'
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
    ascii_txt = r"""
     ::::::::::: :::::::::                                                                        
         :+:     :+:    :+:                                                                        
        +:+     +:+    +:+                                                                         
       +#+     +#++:++#+                                                                           
      +#+     +#+                                                                                  
     #+#     #+#                                                                                   
########### ###                                                                                    
      ::::::::  :::::::::: ::::::::  :::        ::::::::   ::::::::      ::: ::::::::::: ::::::::::
    :+:    :+: :+:       :+:    :+: :+:       :+:    :+: :+:    :+:   :+: :+:   :+:     :+:        
   +:+        +:+       +:+    +:+ +:+       +:+    +:+ +:+         +:+   +:+  +:+     +:+         
  :#:        +#++:++#  +#+    +:+ +#+       +#+    +:+ +#+        +#++:++#++: +#+     +#++:++#     
 +#+   +#+# +#+       +#+    +#+ +#+       +#+    +#+ +#+        +#+     +#+ +#+     +#+           
#+#    #+# #+#       #+#    #+# #+#       #+#    #+# #+#    #+# #+#     #+# #+#     #+#            
########  ########## ########  ########## ########   ########  ###     ### ###     ########## """
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
    print(Fore.WHITE + f'IP\t{ip}\tIP Address To Locate' + Style.RESET_ALL)
    print(Fore.WHITE + f'DirFile\t{inp_file}\tFile Containing IP Addresses [OPTIONAL]' + Style.RESET_ALL)
    print(Fore.WHITE + f'OutFile\t{out_file}\tFile To Print Result To' + Style.RESET_ALL)
    print(Fore.WHITE + f'Verbose\t{verbose}\tVerbose Mode' + Style.RESET_ALL)
    print(Fore.WHITE + f'Quiet\t{quiet}\tQuiet Mode' + Style.RESET_ALL)
    print(Fore.BLACK + '*'*50 + Style.RESET_ALL)

def get_ip_geolocation(ip):
    url = f'http://ip-api.com/json/{ip}'
    response = requests.get(url)
    data = response.json()
    return data

def print_to_file(ip, info_to_get, keys, geolocate_ip):
    scanned_targets = []
    scanned = False
    if out_file != '<file>':
        for scan in scanned_targets:
            if scan == ip:
                scanned = True
            if not scanned:
                file.write(f'Getting Location Of: {ip.strip()}\n')
                scanned_targets.append(ip)
        try:
            with open(out_file, mode='a') as file:
                if not verbose:
                    for info in info_to_get:
                        if info == 'query':
                            file.write(f'IP: {geolocate_ip.get(info)}\n')
                        else:
                            file.write(f'{info}: {geolocate_ip.get(info)}\n')
                else:
                    for key in keys:
                        if key == 'query':
                            file.write(f'IP: {geolocate_ip.get(key)}\n')
                        else:
                            file.write(f'{key}: {geolocate_ip.get(key)}\n')
                file.write('\n')
        except IOError:
            print(Fore.RED + f'Something Happened While Writing to the File {out_file}!' + Style.RESET_ALL)
        except KeyboardInterrupt:
            refresh()
            subprocess.run(['python','tools/ip_locate.py'])
                       
def scan_target(ip):
    scanned_targets = []
    scanned = False
    for scan in scanned_targets:
        if scan == ip:
            scan = True
    geolocate_ip = get_ip_geolocation(ip)
    info_to_get = ['query', 'country', 'city', 'regionName', 'isp']
    keys = geolocate_ip.keys()
    if not quiet:
        if geolocate_ip:
            if not scanned:
                print(Fore.CYAN + f'\nLocating {ip.strip()}' + Style.RESET_ALL, end='')
                scanned_targets.append(ip)
            if not verbose:
                print()
                print(Fore.BLACK + '*'*50 + Style.RESET_ALL)
                print(Fore.GREEN + "IP Geolocation Information:" + Style.RESET_ALL)
                for info in info_to_get:
                    if info == 'query': 
                        print(Fore.WHITE + f"IP: {geolocate_ip.get('query')}" + Style.RESET_ALL)
                    else:
                        print(Fore.WHITE + f"{info}: {geolocate_ip.get(info)}" + Style.RESET_ALL)
                print(Fore.BLACK + '*'*50 + Style.RESET_ALL)
            else:
                print(Fore.BLACK + '*'*50 + Style.RESET_ALL)
                print(Fore.GREEN + "IP Geolocation Information:" + Style.RESET_ALL)
                for key in keys:
                    if key == 'query':
                        print(Fore.WHITE + f'IP: {geolocate_ip.get(key)}' + Style.RESET_ALL)
                    else:
                        print(Fore.WHITE + f'{key}: {geolocate_ip.get(key)}' + Style.RESET_ALL)
                print(Fore.BLACK + '*'*50 + Style.RESET_ALL)
        else:
            print("Failed to retrieve geolocation information.")
    else:
        print('')
    #write to file if specified
    print_to_file(ip, info_to_get, keys, geolocate_ip)

def run_tool():
    global ip, inp_file, out_file, verbose, quiet
    if inp_file == '<file>':
        scan_target(ip)
    else:
        try:
            with open(inp_file, mode='r') as file:
                for line in file:
                    scan_target(line.strip())
        except IOError:
            print(Fore.RED + f'Something Happened While Reading The File {inp_file}!' + Style.RESET_ALL)
        except KeyboardInterrupt:
            refresh()
            subprocess.run(['python', 'tools/ip_locate.py'])
    

def start_tool():
    global ip, inp_file, out_file, verbose, quiet
    print_ascii()
    print(Fore.WHITE + 'Welcome To IP Geolocate' + Style.RESET_ALL)
    print(Fore.LIGHTBLACK_EX + "Enter help for Help Menu" + Style.RESET_ALL)
    while True:
        print(Fore.WHITE + 'Enter your command:' + Style.RESET_ALL, end=' ')
        user_input = get_user_entry().lower()
        if user_input.strip() == 'run':
            run_tool()
        elif user_input.strip() == 'help':
            print_banner()
        elif user_input.strip() == 'back':
            refresh()
            subprocess.run(['python', 'recon.py'])
            break
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
                opt = parts[1].lower()
                valid_option = opt in ['ip', 'dirfile', 'outfile', 'verbose', 'quiet']
                if valid_option:
                    option = parts[2]
                    if opt == 'ip':
                        if ('https' in option) or ('http' in option) or ('www' in option):
                            print(Fore.RED + 'Enter a Valid IP Address' + Style.RESET_ALL)
                            break
                        else:
                            ip = option
                    elif opt == 'dirfile':
                        inp_file = option
                    elif opt == 'outfile':
                        out_file = option
                    elif opt == 'verbose':
                        value = parts[2].lower()
                        if value == 'true':
                            verbose = True
                        elif value == 'false':
                            verbose = False
                        else:
                            print(Fore.RED + 'Enter a Valid Value' + Style.RESET_ALL)
                            break
                    elif opt == 'quiet':
                        value = parts[2].lower()
                        if value == 'true':
                            quiet = True
                        elif value == 'false':
                            quiet = False
                        else:
                            print(Fore.RED + 'Enter a Valid Value' + Style.RESET_ALL)
                            break
                else:
                    print(Fore.RED + 'Enter a Valid Options' + Style.RESET_ALL)
                        
        else:
            print(Fore.RED + "Invalid command. Please enter a valid command." + Style.RESET_ALL)        

if __name__ == "__main__":
    try:
        start_tool()
    except KeyboardInterrupt:
        subprocess.run(['python', 'tools/ip_locate.py'])