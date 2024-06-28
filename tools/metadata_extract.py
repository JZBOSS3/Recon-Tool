import os
from PIL import Image
from exif import Image as ExifImage
import PyPDF2
from PyPDF2 import PdfReader
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
import ffmpeg
from colorama import Fore, Style
import subprocess
import sys

file = '<file>'
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
    txt = r"""
$$\      $$\            $$\               $$$$$$$\             $$\                     $$$$$$$$\             $$\     
$$$\    $$$ |           $$ |              $$  __$$\            $$ |                    $$  _____|            $$ |    
$$$$\  $$$$ | $$$$$$\ $$$$$$\    $$$$$$\  $$ |  $$ | $$$$$$\ $$$$$$\    $$$$$$\        $$ |      $$\   $$\ $$$$$$\   
$$\$$\$$ $$ |$$  __$$\\_$$  _|   \____$$\ $$ |  $$ | \____$$\\_$$  _|   \____$$\         $$$$$\    \$$\ $$  |\_$$  _|  
$$ \$$$  $$ |$$$$$$$$ | $$ |     $$$$$$$ |$$ |  $$ | $$$$$$$ | $$ |     $$$$$$$ |      $$  __|    \$$$$  /   $$ |    
$$ |\$  /$$ |$$   ____| $$ |$$\ $$  __$$ |$$ |  $$ |$$  __$$ | $$ |$$\ $$  __$$ |      $$ |       $$  $$<    $$ |$$\ 
$$ | \_/ $$ |\$$$$$$$\  \$$$$  |\$$$$$$$ |$$$$$$$  |\$$$$$$$ | \$$$$  |\$$$$$$$ |      $$$$$$$$\ $$  /\$$\   \$$$$  |
\__|     \__| \_______|  \____/  \_______|\_______/  \_______|  \____/  \_______|      \________|\__/  \__|   \____/ """
    print(Fore.GREEN + txt + Style.RESET_ALL)

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
    print(Fore.WHITE + f'File\t{file}\tFile to Extract MetaData' + Style.RESET_ALL)
    print(Fore.WHITE + f'DirFile\t{dirFile}\tFile Containing Files To Scan [OPTIONAL]' + Style.RESET_ALL)
    print(Fore.WHITE + f'OutFile\t{outpFile}\tFile To Print Result To' + Style.RESET_ALL)
    print(Fore.WHITE + f'Quiet\t{quiet}\tQuiet Mode' + Style.RESET_ALL)
    print(Fore.BLACK + '*'*50 + Style.RESET_ALL)

def extract_image_metadata(file_path):
    try:
        with Image.open(file_path) as img:
            img_exif = img._getexif()
            if img_exif:
                return img_exif
            else:
                return "No EXIF metadata found"
    except Exception as e:
        return f"Error reading image metadata: {e}"

def extract_pdf_metadata(file_path):
    try:
        with open(file_path, 'rb') as file:
            reader = PdfReader(file)
            return reader.metadata
    except Exception as e:
        return f"Error reading PDF metadata: {e}"

def extract_audio_metadata(file_path):
    try:
        audio = MP3(file_path, ID3=EasyID3)
        return audio.pprint()
    except Exception as e:
        return f"Error reading audio metadata: {e}"

def extract_video_metadata(file_path):
    try:
        probe = ffmpeg.probe(file_path)
        return probe
    except Exception as e:
        return f"Error reading video metadata: {e}"

def extract_metadata(file_path):
    _, file_extension = os.path.splitext(file_path)
    file_extension = file_extension.lower()
    if file_extension in ['.jpg', '.jpeg', '.png', '.tiff']:
        return extract_image_metadata(file_path)
    elif file_extension == '.pdf':
        return extract_pdf_metadata(file_path)
    elif file_extension in ['.mp3', '.flac', '.ogg', '.wav', '.aac']:
        return extract_audio_metadata(file_path)
    elif file_extension in ['.mp4', '.mkv', '.avi', '.mov']:
        return extract_video_metadata(file_path)
    else:
        return "Unsupported file type"

def print_meta(metadata):
    can_print = True
    if metadata == 'No EXIF metadata found':
        print('No EXIF metadata found')
        can_print = False
    elif metadata == 'Unsupported file type':
        print('Unsupported file type')
        can_print = False
    if can_print:
        keys = metadata.keys()
        for key in keys:
            desc = key.split('/')
            print(Fore.LIGHTBLUE_EX + f'{desc[1]}: {metadata.get(key)}' + Style.RESET_ALL)

def write_file(to_scan, metadata):
    scanned_targets = []
    scanned = False
    can_write = True
    for scan in scanned_targets:
        if scan == metadata.get('/title'):
            scanned = True
    try:
        with open(outpFile, mode='a') as file:
            if not scanned:
                file.write(f'Scanning {to_scan}\n')
            if metadata == 'No EXIF metadata found':
                file.write('No EXIF metadata found')
                can_write = False
            elif metadata == 'Unsupported file type':
                file.write('Unsupported file type')
                can_write = False
            if can_write:    
                keys = metadata.keys()
                for key in keys:
                    desc = key.split('/')
                    file.write(f'{desc[1]}: {metadata.get(key)}\n')
                scanned_targets.append(metadata.get('/title'))
    except IOError:
        print(Fore.RED + f'There was an Error Writing to {outpFile}' + Style.RESET_ALL)
    except KeyboardInterrupt:
        print('CTRL+C Detected. Exiting....')
    except Exception as e:
        print(e)

def start_tool():
    global file, dirFile, outpFile, quiet
    print_ascii()
    print(Fore.WHITE + 'Welcome To MetaData Extracter' + Style.RESET_ALL)
    print(Fore.LIGHTBLACK_EX + "Enter help for Help Menu" + Style.RESET_ALL)
    while True:
        print(Fore.WHITE + 'Enter your command:' + Style.RESET_ALL, end=' ')
        user_input = get_user_entry().lower()
        if user_input.strip() == 'run':
            if dirFile == '<file>':
                metadata = extract_metadata(file)
                if not quiet:
                    print_meta(metadata)
                if outpFile != '<file>':
                    write_file(file, metadata)
            else:
                try:
                    with open(dirFile, mode='r') as file:
                        for line in file:
                            metadata = extract_metadata(line.strip())
                            #print(line, metadata)
                            if not quiet:
                                print_meta(metadata)
                            if outpFile != '<file>':
                                write_file(line, metadata)
                except IOError:
                    print(Fore.RED + f'Error While Reading {dirFile}' + Style.RESET_ALL)
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
                if option not in ['file', 'dirfile', 'outfile', 'quiet']:
                    print(Fore.RED + 'Enter a Valid Command' + Style.RESET_ALL)
                else:
                    if option == 'file':
                        file = parts[2]
                    elif option == 'dirfile':
                        dirFile = parts[2]
                    elif option == 'outfile':
                        outpFile = parts[2]
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
        print('',end='')