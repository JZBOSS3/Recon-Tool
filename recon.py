import sys
import os  # importing os for clearing the terminal
import time  # for timer events like wait 3 seconds before clearing the screen
import subprocess  # to call other python files and run them here
from colorama import Style, Fore

def refresh():
    time.sleep(0.5)
    # Clear command as function of OS
    command = 'cls' if os.name == 'nt' else 'clear'
    os.system(command)

def print_terms_of_service():
    tos_text = """
[!] Terms of service:
[!] Legal/Ethical disclaimer:
=========================================
> recon.py is a tool designed to gather information about a target which is publicly available.
> Usage of recon.py for attacking targets without prior mutual consent is illegal.
> It is the end user's responsibility to obey all applicable local, state, and federal laws.
> Developers assume no liability and are not responsible for any misuse or damage caused by this program.
=========================================
Do you accept the Terms of Service/TOS that has been presented to you [Y/N]:"""
    print(Fore.GREEN + tos_text + Style.RESET_ALL, end=' ')

def print_ascii_art():
    magnifying_glass_art = """
                    __gggrgM**M#mggg__
                __wgNN@"B*P""mp""@d#"@N#Nw__
              _g#@0F_a*F#  _*F9m_ ,F9*__9NG#g_
           _mN#F  aM"    #p"    !q@    9NL "9#Qu_
          g#MF _pP"L  _g@"9L_  _g""#__  g"9w_ 0N#p
        _0F jL*"   7_wF     #_gF     9gjF   "bJ  9h_
       j#  gAF    _@NL     _g@#_      J@u_    2#_  #_
      ,FF_#" 9_ _#"  "b_  g@   "hg  _#"  !q_ jF "*_09_
      F N"    #p"      Ng@       `#g"      "w@    "# t
     j p#    g"9_     g@"9_      gP"#_     gF"q    Pb L
     0J  k _@   9g_ j#"   "b_  j#"   "b_ _d"   q_ g  ##
     #F  `NF     "#g"       "Md"       5N#      9W"  j#
     #k  jFb_    g@"q_     _*"9m_     _*"R_    _#Np  J#
     tApjF  9g  J"   9M_ _m"    9%_ _*"   "#  gF  9_jNF
      k`N    "q#       9g@        #gF       ##"    #"j
      `_0q_   #"q_    _&"9p_    _g"`L_    _*"#   jAF,'
       9# "b_j   "b_ g"    *g _gF    9_ g#"  "L_*"qNF
        "b_ "#_    "NL      _B#      _I@     j#" _#"
          NM_0"*g_ j""9u_  gP  q_  _w@ ]_ _g*"F_g@
           "NNh_ !w#_   9#g"    "m*"   _#*" _dN@"
              9##g_0@q__ #"4_  j*"k __*NF_g#@P"
                "9NN#gIPNL_ "b@" _2M"Lg#N@F"
                    ""P@*NN#gEZgNN@#@P""
    """
    credits ="""
                    recon.py by jzboss3
    """

    print(Fore.BLUE + magnifying_glass_art, end='\r' + Style.RESET_ALL)
    print(Fore.GREEN + credits + Style.RESET_ALL)

def print_banner():
    print(Fore.YELLOW + "-"*50 + Style.RESET_ALL)
    print(Fore.WHITE + "1- Brute Force Directories" + Style.RESET_ALL)
    print(Fore.WHITE + "2- Port Scanner" + Style.RESET_ALL)
    print(Fore.WHITE + "3- Email Address Harvesting" + Style.RESET_ALL)
    print(Fore.WHITE + "4- Social Media Profiling" + Style.RESET_ALL)
    print(Fore.WHITE + "5- Metadata Extraction" + Style.RESET_ALL)
    print(Fore.WHITE + "6- IP Geolocation" + Style.RESET_ALL)
    print(Fore.WHITE + "7- WHOIS Lookup" + Style.RESET_ALL)
    print(Fore.WHITE + "8- Subdomain Enumeration" + Style.RESET_ALL)
    print(Fore.WHITE + "9- Check Active Domains" + Style.RESET_ALL)
    print(Fore.WHITE + "10- ScreenShot Domains" + Style.RESET_ALL)
    print(Fore.LIGHTBLACK_EX + "Run help for more info" + Style.RESET_ALL)
    print(Fore.LIGHTBLACK_EX + "Run quit to exit" + Style.RESET_ALL)
    print(Fore.YELLOW + "-"*50 + Style.RESET_ALL)

def print_help_menu():
    print(Fore.RED + "-"*50 + Style.RESET_ALL)
    # Directory Brute Forcer
    print(Fore.WHITE + "1- Brute Force Directories" + Style.RESET_ALL)
    print(Fore.LIGHTBLUE_EX + "\tFind hidden directories and files on web servers." + Style.RESET_ALL)
    # Port Scanner
    print(Fore.WHITE + "2- Port Scanner" + Style.RESET_ALL)
    print(Fore.LIGHTBLUE_EX + "\tRetrieve Open/Closed Ports for an IP address or a Domain." + Style.RESET_ALL)
    # Email Harvester
    print(Fore.WHITE + "3- Email Address Harvesting" + Style.RESET_ALL)
    print(Fore.LIGHTBLUE_EX + "\tExtract email addresses associated with a target url" + Style.RESET_ALL)
    # Social Media Profiling
    print(Fore.WHITE + "4- Social Media Profiling" + Style.RESET_ALL)
    print(Fore.LIGHTBLUE_EX + "\tGather Social Media Profiles from a URL." + Style.RESET_ALL)
    # MetaData Extraction
    print(Fore.WHITE + "5- Metadata Extraction" + Style.RESET_ALL)
    print(Fore.LIGHTBLUE_EX + "\tExtract Metadata from a File" + Style.RESET_ALL)
    # IP Geolocation
    print(Fore.WHITE + "6- IP Geolocation" + Style.RESET_ALL)
    print(Fore.LIGHTBLUE_EX + "\tGet Location of an IP Address." + Style.RESET_ALL)
    # WHOIS
    print(Fore.WHITE + "7- WHOIS Lookup" + Style.RESET_ALL)
    print(Fore.LIGHTBLUE_EX + "\tRetrieve WHOIS information for domains and IP addresses." + Style.RESET_ALL)
    # Subdomain Enumeration
    print(Fore.WHITE + "8- Subdomain Enumeration" + Style.RESET_ALL)
    print(Fore.LIGHTBLUE_EX + "\tDiscover and list subdomains associated with a target domain." + Style.RESET_ALL)
    # Check for active domains
    print(Fore.WHITE + "9- Check Active Domains" + Style.RESET_ALL)
    print(Fore.LIGHTBLUE_EX + "\tDiscover acive domains from a list." + Style.RESET_ALL)
    #ScreenShot Domains
    print(Fore.WHITE + "10- ScreenShot Domains" + Style.RESET_ALL)
    print(Fore.LIGHTBLUE_EX + "\tTake a screenshot of the domain's home page." + Style.RESET_ALL)
    print(Fore.RED + "-"*50 + Style.RESET_ALL)

def get_user_entry():
    entry = input().strip().lower()
    return entry

def handle_menu_option(option):
    if option == '1':  # Directory BruteForcing
        subprocess.run(['python3', 'tools/dir_bruter.py'])
        sys.exit()
    elif option == '2':  # Port Scanner
        subprocess.run(['python3', 'tools/port_scan.py'])
        sys.exit()
    elif option == '3':  # Email Address Harvesting
        subprocess.run(['python3', 'tools/email_harvest.py'])
        sys.exit()
    elif option == '4':  # Social Media Profiling
        subprocess.run(['python3', 'tools/social_media.py'])
        sys.exit()
    elif option == '5':  # Metadata Extraction
        subprocess.run(['python3', 'tools/metadata_extract.py'])
        sys.exit()
    elif option == '6':  # IP Geolocation
        subprocess.run(['python3', 'tools/ip_locate.py'])
        sys.exit()
    elif option == '7':  # WHOIS Lookup
        subprocess.run(['python3', 'tools/whois.py'])
        sys.exit()
    elif option == '8':  # Subdomain Enumeration
        subprocess.run(['python3', 'tools/subdomain.py'])
        sys.exit()
    elif option == '9': #active domains
        subprocess.run(['python3', 'tools/active_domains.py'])
        sys.exit()
    elif option == '10': #screenshot domains
        subprocess.run(['python3', 'tools/screenshot_domains.py']);
        sys.exit()
    elif option == 'help':
        print_help_menu()
    elif option == 'clear':
        refresh()
    elif option == 'quit':
        sys.exit()
    else:
        print(Fore.RED + "Invalid option. Please enter a valid option." + Style.RESET_ALL)

def main():
    print_terms_of_service()
    user_tos_entry = get_user_entry()
    if user_tos_entry == 'y':
        print(Fore.RED + 'Thank you!' + Style.RESET_ALL)
        refresh()
        print_ascii_art()
        print_banner()
        while True:
            print('Choose an Option: ', end='')
            user_option_entry = get_user_entry()
            refresh()
            handle_menu_option(user_option_entry)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(Fore.RED + '\nCTRL+C Detected. Exiting Program....' + Style.RESET_ALL)
