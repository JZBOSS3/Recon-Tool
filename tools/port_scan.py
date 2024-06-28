import socket
import sys
import subprocess
import os
from colorama import Fore, Style

target = '<target>'
inp_file = '<file>'
outpFile = '<file>'
ports = 65535
verbose = False
quiet = False
timeout = 1

def refresh():
    # Clear command as function of OS
    command = 'cls' if os.name == 'nt' else 'clear'
    os.system(command)

def get_user_entry():
    entry = input().strip().lower()
    return entry  # Return the entered value

def print_ascii():
    ascii_text = r"""
      :::::::::   ::::::::  ::::::::: :::::::::::                                  
     :+:    :+: :+:    :+: :+:    :+:    :+:                                       
    +:+    +:+ +:+    +:+ +:+    +:+    +:+                                        
   +#++:++#+  +#+    +:+ +#++:++#:     +#+                                         
  +#+        +#+    +#+ +#+    +#+    +#+                                          
 #+#        #+#    #+# #+#    #+#    #+#                                           
###         ########  ###    ###    ###                                            
      ::::::::   ::::::::      :::     ::::    ::: ::::    ::: :::::::::: :::::::::
    :+:    :+: :+:    :+:   :+: :+:   :+:+:   :+: :+:+:   :+: :+:        :+:    :+:
   +:+        +:+         +:+   +:+  :+:+:+  +:+ :+:+:+  +:+ +:+        +:+    +:+ 
  +#++:++#++ +#+        +#++:++#++: +#+ +:+ +#+ +#+ +:+ +#+ +#++:++#   +#++:++#:   
        +#+ +#+        +#+     +#+ +#+  +#+#+# +#+  +#+#+# +#+        +#+    +#+   
#+#    #+# #+#    #+# #+#     #+# #+#   #+#+# #+#   #+#+# #+#        #+#    #+#    
########   ########  ###     ### ###    #### ###    #### ########## ###    ### """
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
    print(Fore.WHITE + f'Target\t{target}\tTarget to Scan' + Style.RESET_ALL)
    print(Fore.WHITE + f'InpFile\t{inp_file}\t\tTargets File' + Style.RESET_ALL)
    print(Fore.WHITE + f'OutFile\t{outpFile}\t\tFile To Print Result To' + Style.RESET_ALL)
    print(Fore.WHITE + f'Ports\t{ports}\t\tFile To Print Result To' + Style.RESET_ALL)
    print(Fore.WHITE + f'Timeout\t{timeout}\t\tTime between requests(in sec)' + Style.RESET_ALL)
    print(Fore.WHITE + f'Verbose\t{verbose}\t\tVerbose Mode' + Style.RESET_ALL)
    print(Fore.WHITE + f'Quiet\t{quiet}\t\tQuiet Mode' + Style.RESET_ALL)
    print(Fore.BLACK + '*'*50 + Style.RESET_ALL)

def check_if_target_alive(ip):
    # Use the ping command to check the host
    try:
        # `-c 1` means send 1 packet, `-W 1` means timeout after 1 second (Linux/Mac)
        # For Windows use `-n 1` for one packet and `-w 1000` for 1-second timeout
        if sys.platform != "win32":
            command = ["ping", "-c", "1", "-W", "1", ip] 
        else:
            command = ["ping", "-n", "1", "-w", "1000", ip]
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, universal_newlines=True)
        return True
    except subprocess.CalledProcessError:
        return False

def write_file(target, port, msg):
    scanned_targets = []
    scanned = False
    with open(outpFile, mode='a') as file:
        for target_ in scanned_targets:
            if target_ == target:
                scanned = True
        if not scanned:
            file.write(f'Scanning {target}...', end='\n')
        file.write(f'Port {port} is {msg}\n')

def run_tool(target):
    global ports
    if target == '<target>':
        print(Fore.RED + 'Target param is Empty!')
    else:
        base_target = target
        target_ = socket.gethostbyname(target)
        if check_if_target_alive(target_):
            for port in range(1, int(ports) + 1):
                s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                socket.setdefaulttimeout(timeout)
                result = s.connect_ex((target_, port))
                if not quiet:
                    if verbose:
                        if result != 0:
                            print(Fore.RED + f'Port {port} is Not Open' + Style.RESET_ALL)
                            if outpFile != '<file>':
                                write_file(base_target, port, 'not open')
                    if result == 0:
                        print(Fore.GREEN + f'Port {port} is Open' + Style.RESET_ALL)
                        if outpFile != '<file>':
                            write_file(base_target, port, 'not open')
                else:
                    if verbose:
                        if outpFile != '<file>':
                                write_file(base_target, port, 'not open')
                    else:
                        if outpFile != '<file>':
                            write_file(base_target, port, 'not open')

        else:
            print(Fore.RED + f'{base_target} is Unreachable' + Style.RESET_ALL)

def scan_targets(inpfile):
    scanned_targets = []
    scanned = False
    try:
        with open(inp_file, mode='r') as file:
            for line in file:
                for scan in scanned_targets:
                    if scan == line:
                        scanned = True
                if not scanned:
                    print(f'Scanning {line}')
                line = line.strip()
                if not line:
                    continue
                else:
                    run_tool(line)
    except FileNotFoundError:
        print(f"Error: File '{inp_file}' not found.")

def start_tool():
    global target, inp_file, ports, timeout, outpFile, verbose, quiet
    print_ascii()
    print(Fore.WHITE + 'Welcome To Port Scanner' + Style.RESET_ALL)
    print(Fore.LIGHTBLACK_EX + "Enter help for Help Menu" + Style.RESET_ALL)
    while True:
        print(Fore.WHITE + 'Enter your command:' + Style.RESET_ALL, end=' ')
        user_input = get_user_entry().lower()
        if user_input.strip() == 'run':
            if inp_file == "<file>":
                run_tool(target)
            else:
                scan_targets(inp_file)
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
                    if option == 'target':
                        target = parts[2]
                        if ('https://' in target) or ('http://' in target) or ('www.' in target):
                            print(Fore.RED + f'Enter a Valid Target!' + Style.RESET_ALL)
                            target = '<target>'
                    elif option == 'inpfile':
                        inp_file = parts[2]
                    elif option == 'ports':
                        ports = parts[2]
                    elif option == 'outfile':
                        outpFile = parts[2]
                    elif option == 'timeout':
                        timeout = float(parts[2])
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
                    print(Fore.RED + 'Enter a Valid Option' + Style.RESET_ALL)
        else:
            print(Fore.RED + "Invalid command. Please enter a valid command." + Style.RESET_ALL)


if __name__ == "__main__":
    try:
        start_tool()
    except KeyboardInterrupt:
        subprocess.run(['python', 'tools/port_scan.py'])