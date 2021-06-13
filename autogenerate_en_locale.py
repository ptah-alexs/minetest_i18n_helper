#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import sys
import random

path = os.getcwd()

def read_data(name):
    with open(name,'r') as fin:
        return fin.readlines()

def write_data(name, data):
    with open(name,'w') as fout:
        fout.writelines(data)

def path_parts(path, direction = 0):
    folders = []
    while 1:
        path, folder = os.path.split(path)
        if folder != "":
            folders.append(folder)
        else:
            if path != "":
                folders.append(path)
                break
    if (direction == 0):
        folders.reverse()
    return folders

def get_mod_name():
    modconf_path = os.path.join(path, 'mod.conf')
    if os.path.exists(modconf_path):
        inf_file = read_data(modconf_path)
        for fnum, fstr in enumerate(inf_file):
            if not (fstr.find('name') == -1):
                s_index = fstr.find('=')
                if not (s_index == -1):
                    return fstr[s_index+1:-1].strip()
    return path_parts(path)[-1]

def generate_from_template(file_path, name):
    strings = []
    strings.append(f'# textdomain: {name}\n')
    data = read_data(os.path.join(file_path, 'locale', 'template.txt'))
    for elem in data:
        if not elem.startswith('# '):
            strings.append(f'{elem[:-1]}{elem[:-2]}\n')
    write_data(os.path.join(file_path, 'locale', f'{name}.en.tr'), strings)

def main():
    mod_name = get_mod_name()
    if os.path.exists(os.path.join(path, 'locale', 'template.txt')):
        if not os.path.exists(os.path.join(path, 'locale', f'{mod_name}.en.tr')):
            generate_from_template(path, mod_name)
    else:
        print('Не найден шаблон')
        quit()

if __name__ == "__main__":
    main()

