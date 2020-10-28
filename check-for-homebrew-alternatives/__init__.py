#!/usr/local/bin/python3
import urllib.request
import json
import subprocess
import os
import multiprocessing
from multiprocessing import Pool
import sys
    # r = requests.get('https://formulae.brew.sh/api/cask.json')
    # homebrew_data = r.json()

installed_homebrew_apps_str = str(subprocess.check_output(r'brew list --cask -1', shell = True))
installed_homebrew_apps_str = installed_homebrew_apps_str[2:]
installed_homebrew_apps = installed_homebrew_apps_str.split('\\n') # there might be one extra elemenent at the end here
# print("installed homebrew apps", installed_homebrew_apps)

installed_apps_str = str(subprocess.check_output(r'ls -1 /Applications/', shell = True)) # maybe take in /Applications as an option in the running of the programs
installed_apps = installed_apps_str.split('\\n')

all_avaliable_homebrew_apps_str = str(subprocess.check_output(r'brew search --casks | cat', shell = True))
# print(all_avaliable_homebrew_apps_str)
all_avaliable_homebrew_apps_str = all_avaliable_homebrew_apps_str[2:]

all_avaliable_homebrew_apps = all_avaliable_homebrew_apps_str.split('\\n')
# print(all_avaliable_homebrew_apps[1])
#print("atom in hombrew apps:", "atom" in installed_homebrew_apps)
#print("cd-to-terminal in hombrew apps:", "cd-to-terminal" in installed_homebrew_apps)

# Progress method: Copyright (c) 2016 Vladimir Ignatev
# https://gist.github.com/vladignatyev/06860ec2040cb497f0f3
def progress(count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
sys.stdout.flush() # As suggested by Rom Ruben (see: http://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console/27871113#comment50529068_27871113)


def main():
    # all_avaliable_homebrew_apps = ['cd-to-terminal']
        # p.map(check_for_homebrew_app, all_avaliable_homebrew_apps)

    for i in range(len(all_avaliable_homebrew_apps)):
        progress(i, len(all_avaliable_homebrew_apps), 'checking homebrew apps...')
        check_for_homebrew_app(all_avaliable_homebrew_apps[i])

def check_for_homebrew_app(homebrew_app):
    url = 'https://formulae.brew.sh/api/cask/' + str(homebrew_app) + '.json'
    req = urllib.request.Request(url)

    # parsing response
    try:
        r = urllib.request.urlopen(req).read()
        # print("checking homrbew app", str(homebrew_app))
        # r = requests.get('https://formulae.brew.sh/api/cask/' + str(homebrew_app) + '.json')
        try:
            r_data = json.loads(r.decode('utf-8'))
            for artifact_list in r_data['artifacts']:
                for a in artifact_list:
                    if type(a) == dict:
                        for key, value in a.items():
                            if not_installed_and_valid_string(value, homebrew_app):
                                print("Try installing", homebrew_app, "to replace", value)
                    elif not_installed_and_valid_string(a, homebrew_app):
                        print("try installing", homebrew_app, "to replace", a)

        except:
            pass
    except:
        pass

    # for item in homebrew_data:
    #     for artifact_list in item['artifacts']:

    # print(homebrew_data)
def not_installed_and_valid_string(a, homebrew_app):
    return ((a.endswith('.app') and a in installed_apps)) and homebrew_app not in installed_homebrew_apps

def not_installed_and_valid_array(value, homebrew_app):
    return (value in installed_apps_str or os.path.exists(value) or os.path.exists('/Applications/' + value)) and homebrew_app not in installed_homebrew_apps
main()
