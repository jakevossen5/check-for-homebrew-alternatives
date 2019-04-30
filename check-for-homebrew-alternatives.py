import requests
import subprocess
import os
import multiprocessing
from multiprocessing import Pool

    # r = requests.get('https://formulae.brew.sh/api/cask.json')
    # homebrew_data = r.json()

installed_homebrew_apps_str = str(subprocess.check_output(r'brew cask list -1', shell = True))
installed_homebrew_apps_str = installed_homebrew_apps_str[2:]
installed_homebrew_apps = installed_homebrew_apps_str.split('\\n') # there might be one extra elemenent at the end here
print("installed homebrew apps", installed_homebrew_apps) 

installed_apps_str = str(subprocess.check_output(r'ls -1 /Applications/', shell = True)) # maybe take in /Applications as an option in the running of the programs
installed_apps = installed_apps_str.split('\\n')

all_avaliable_homebrew_apps_str = str(subprocess.check_output(r'brew search --casks | cat', shell = True))
# print(all_avaliable_homebrew_apps_str)
all_avaliable_homebrew_apps_str = all_avaliable_homebrew_apps_str[2:]

all_avaliable_homebrew_apps = all_avaliable_homebrew_apps_str.split('\\n')
# print(all_avaliable_homebrew_apps[1])
print("atom in hombrew apps:", "atom" in installed_homebrew_apps)
print("cd-to-terminal in hombrew apps:", "cd-to-terminal" in installed_homebrew_apps)

def main():
    # all_avaliable_homebrew_apps = ['cd-to-terminal']
    threads_count = multiprocessing.cpu_count()
    with Pool(threads_count) as p:
        p.map(check_for_homebrew_app, all_avaliable_homebrew_apps)

def check_for_homebrew_app(homebrew_app):
    # print("checking homrbew app", str(homebrew_app))
    r = requests.get('https://formulae.brew.sh/api/cask/' + str(homebrew_app) + '.json')
    try:
        r_data = r.json()
        for artifact_list in r_data['artifacts']:
            for a in artifact_list:
                if type(a) == dict:
                    for key, value in a.items():
                        if (value in installed_apps_str or os.path.exists(value) or os.path.exists('/Applications/' + value)) and homebrew_app not in installed_homebrew_apps:
                            print("Try installing", homebrew_app)
                            print("Value that triggered", value)
                elif a.endswith('.app') and str(a) in installed_apps_str and homebrew_app not in installed_homebrew_apps:
                    print("try installing", homebrew_app)

    except:
        pass

    # for item in homebrew_data:
    #     for artifact_list in item['artifacts']:
    
    # print(homebrew_data)
main()
