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

def replace_i18n_engine(mod_path, mod_name, input_file):
    lua_file = read_data(os.path.join(path, input_file))
    rewrite = 0
    for fnum, fstr in enumerate(lua_file):
        if not (fstr.find('lord.require_intllib()') == -1):
            print('Найден IntlLib')
            lua_file[fnum] = fstr.replace('lord.require_intllib()',f'minetest.get_translator("{mod_name}")')
            rewrite = 1
            is_old_engine = 1
            break
    if (rewrite == 1):
        write_data(os.path.join(path, input_file), lua_file)

def create_list_locale_files(mod_path):
    files = []
    locale_path = os.path.join(mod_path, 'locale')
    if os.path.exists(locale_path):
        for entry in os.scandir(locale_path):
            if entry.is_file() and entry.name.endswith('.txt'):
                if (entry.name.find('template') == -1):
                    files.append(os.path.join(mod_path, 'locale', entry.name))
        files.sort()
    return files

def create_list_lua_files(mod_path):
    files = []
    for entry in os.scandir(mod_path):
        if entry.is_file() and entry.name.endswith('.lua'):
            files.append(os.path.join(mod_path, entry.name))
    files.sort()
    return files

def read_all_i18n(flist):
    result = {}
    for elem in flist:
        file_data = read_data(elem)
        result.update({elem: file_data})
    return result

def create_template(data):
    str_list = []
    for key, value in data.items():
        for elem in value:
            if not elem.startswith('###'):
                s_index = elem.find('=')
                if not (s_index == -1):
                    str_list.append(f'{elem[:s_index-1].strip()}=\n')
    return list(set(str_list))

def create_locale_file(data):
    strings = []
    for elem in data:
        if not elem.startswith('###'):
            s_index = elem.find('=')
            if not (s_index == -1):
                strings.append(f'{elem[:s_index-1].strip()}={elem[s_index+1:-1].strip()}\n')
    return strings

def write_i18n_files(mod_name, header, data):
    for key, value in data.items():
        base_name = path_parts(key)[-1][:-4]
        if not (base_name == 'template'):
            new_file_name = f'{mod_name}.{base_name}.tr'
            write_data(os.path.join(path, 'locale', new_file_name), header + create_locale_file(value) + ['\n'])
            os.remove(key)

def main():
    mod_name = get_mod_name()
    i18n_header = [f'# textdomain: {mod_name}\n']
    flist = create_list_locale_files(path)
    for elem in create_list_lua_files(path):
        replace_i18n_engine(path, mod_name,elem)
    if not (flist == []):
        i18n_data = read_all_i18n(flist)
        write_data(os.path.join(path, 'locale','template.txt'), i18n_header + create_template(i18n_data) + ['\n'])
        write_i18n_files(mod_name, i18n_header, i18n_data)

if __name__ == "__main__":
    main()
