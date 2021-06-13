#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import sys
import random

def print_help():
    print('minetest_i18n_helper - convert i18n files from IntlLib to minetest.get_traslator format')
    print('')
    print('minetest_i18n_helper [-h, --help] [path]')
    print('')
    print('-h, --help - Print help')
    print('')
    print('[path] - minetest mod path, if argument not specified, used current path')
    print('')
    print('© ptah_alexs 2021.')
    quit()

def read_data(name):
    with open(name,'r') as fin:
        return fin.readlines()

def write_data(name, data):
    with open(name,'w') as fout:
        fout.writelines(data)

def path_parts(path, direction = 0):
    folders = []
    if (path[-1] == os.sep):
        path = path[:-1]
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

def get_mod_name(path):
    modconf_path = os.path.join(path, 'mod.conf')
    if os.path.exists(modconf_path):
        inf_file = read_data(modconf_path)
        for fnum, fstr in enumerate(inf_file):
            if not (fstr.find('name') == -1):
                s_index = fstr.find('=')
                if not (s_index == -1):
                    return fstr[s_index+1:-1].strip()
    return path_parts(path)[-1]

def create_list_files(path, extention):
    files_list = []
    for root, subFolders, files in os.walk(path):
        for file_0 in files:
            if file_0.endswith(f'.{extention}'):
                files_list.append(os.path.join(root,file_0))
    return files_list

def replace_i18n_engine(name, input_file):
    lua_file = read_data(input_file)
    rewrite = 0
    for fnum, fstr in enumerate(lua_file):
        if not (fstr.find('lord.require_intllib()') == -1):
            print(f'{input_file} - Найден IntlLib')
            lua_file[fnum] = fstr.replace('lord.require_intllib()',f'minetest.get_translator("{name}")')
            rewrite = 1
            break
    if (rewrite == 1):
        write_data(input_file, lua_file)

def lua_files_processing(path, name):
    for elem in create_list_files(path,'lua'):
        replace_i18n_engine(name, elem)

def clean_files_list(data):
    result = []
    for elem in data:
        if elem.find('template.txt') == -1:
            result.append(elem)
    return result

def read_all_i18n(flist):
    result = {}
    for elem in flist:
        file_data = read_data(elem)
        result.update({elem: file_data})
    return result

def create_template(path, mod_name, data):
    str_list = []
    for _, value in data.items():
        for elem in value:
            if not elem.startswith('###'):
                s_index = elem.find('=')
                if not (s_index == -1):
                    str_list.append(f'{elem[:s_index-1].strip()}=\n')
    str_list = [f'# textdomain: {mod_name}\n'] + list(set(str_list))
    if not(str_list[-1] == '\n'):
        str_list.append('\n')
    write_data(os.path.join(path,'template.txt'), str_list)

def create_locale_file(data):
    strings = []
    for elem in data:
        if not elem.startswith('###'):
            s_index = elem.find('=')
            if not (s_index == -1):
                strings.append(f'{elem[:s_index-1].strip()}={elem[s_index+1:-1].strip()}\n')
    return strings

def write_i18n_files(path, mod_name, data):
    for key, value in data.items():
        base_name = key[key.rfind('/')+1:-4]
        new_file_name = f'{mod_name}.{base_name}.tr'
        str_list = [f'# textdomain: {mod_name}\n'] + create_locale_file(value) 
        if not(str_list[-1] == '\n'):
            str_list.append('\n')
        write_data(os.path.join(path, new_file_name), str_list)
        os.remove(key)

def i18n_files_processing(path, name):
    locale_path = os.path.join(path, 'locale')
    i18n_files = clean_files_list(create_list_files(locale_path,'txt'))
    if not (i18n_files == []):
        i18n_data = read_all_i18n(i18n_files)
        create_template(locale_path, name, i18n_data)
        write_i18n_files(locale_path, name, i18n_data)

def generate_from_template(file_path, name):
    strings = []
    strings.append(f'# textdomain: {name}\n')
    data = read_data(os.path.join(file_path, 'locale', 'template.txt'))
    for elem in data:
        if not elem.startswith('# '):
            strings.append(f'{elem[:-1]}{elem[:-2]}\n')
    write_data(os.path.join(file_path, 'locale', f'{name}.en.tr'), strings)

def create_missing_en_locale(path, name):
    if not os.path.exists(os.path.join(path, 'locale', f'{name}.en.tr')):
        generate_from_template(path, name)

def main():
    current_path = os.getcwd()
    args = sys.argv[1:]
    if not (len(args) == 0):
        if args[0] in ('-h', '--help'):
            print_help()
        elif os.path.exists(args[0]):
            current_path = args[0]
        else:
            print('Directory not found')
            quit()
    mod_name = get_mod_name(current_path)
    lua_files_processing(current_path, mod_name)
    i18n_files_processing(current_path, mod_name)
    create_missing_en_locale(current_path, mod_name)

if __name__ == "__main__":
    main()
