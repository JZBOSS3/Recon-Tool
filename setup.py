import subprocess

if __name__ == "__main__":
        subprocess.run(['sudo', 'wget', 'https://github.com/michenriksen/aquatone/releases/download/v1.7.0/aquatone_linux_amd64_1.7.0.zip'])
        subprocess.run(['sudo', 'unzip', 'aquatone_linux_amd64_1.7.0.zip'])
        subprocess.run(['sudo', 'mv' 'aquatone', '/usr/bin/'])
        subprocess.run(['sudo', 'rm', 'aquatone_linux_amd64_1.7.0.zip'])
