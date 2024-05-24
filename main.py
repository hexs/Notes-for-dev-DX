import json
import subprocess
import os
import shutil
import time
from pprint import pprint
# from mdutils.mdutils import MdUtils
# from mdutils import Html
from urllib.request import urlopen
from constant import *


def get_latest_package_version(package):
    if type(package) == str:
        with urlopen(f'https://pypi.org/pypi/{package}/json') as response:
            data = json.load(response)
        return data['info']['version']

    with urlopen(f'https://pypi.org/pypi/{package.__name__}/json') as response:
        data = json.load(response)
    return data['info']['version']


def get_current_package_version(package):
    return package.__version__


def current_is_latest_package_version(package):
    return get_current_package_version(package) == get_latest_package_version(package)


def get_installed_libraries(lib_name):
    print(f'get_installed_libraries {lib_name}')
    if 'whl' in os.listdir():
        shutil.rmtree('whl')
    os.makedirs('whl', exist_ok=True)

    dir_path = (os.path.dirname(__file__))
    whl_path = os.path.join(dir_path, 'whl')
    subprocess.check_output(f'pip download --proxy http://agyc026730:op90-===@150.61.8.70:10080 {lib_name}'
                            # ['pip', "download", "--proxy", "http://agyc026730:op90-===@150.61.8.70:10080", 'ultralytics']
                            , cwd=whl_path)
    library_list = []
    for lib in os.listdir(whl_path):
        name = lib.split('-')[0]
        version = lib.split('-')[1]
        # name, version, type1, type2, device = lib.split('-')
        library_list.append([name, version])
    return library_list


def main():
    with open('libs.json', encoding='utf-8') as f:
        libs_dict = json.loads(f.read())

    # use function get_installed_libraries
    for lib_name, v in libs_dict.items():
        # ถ้าไม่มี project used ให้สร้าง key
        if v.get('project used') is None:
            v['project used'] = ''

        # ถ้ามี library_list อยู่แล้ว ให้ข้าม
        if v.get('library_list'):
            continue
        # get_installed_libraries
        try:
            v['library_list'] = get_installed_libraries(lib_name)
            with open('libs.json', 'w', encoding='utf-8') as file:
                json.dump(libs_dict, file, ensure_ascii=False, indent=4)
        except:
            print(f'{lib_name} error')

    pprint(libs_dict)
    with open('libs.json', 'w', encoding='utf-8') as file:
        json.dump(libs_dict, file, ensure_ascii=False, indent=4)


# main()

def check_lib():
    with open('libs.json', encoding='utf-8') as f:
        libs_dict = json.loads(f.read())
    for i, (lib_name, v) in enumerate(libs_dict.items(), start=1):
        print(i, lib_name)
    while True:
        ip = input('>')
        if ip not in libs_dict.keys():
            print(RED, ip, ENDC)
