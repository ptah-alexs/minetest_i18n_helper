#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import sys
import random

def print_help():
    print('depends2modconf - convert depends.txt files mod.conf')
    print('')
    print('depends2modconf [-h, --help] [path]')
    print('')
    print('-h, --help - Print help')
    print('')
    print('[path] - minetest mod path, if argument not specified, used current path')
    print('')
    print('© ptah_alexs 2021.')
    quit()

def read_data(name):
    result = []
    with open(name,'r') as fin:
        fdata = fin.readlines()
    for entry in fdata:
        result.append(entry[:-1])
    return result

def write_data(name, data):
    with open(name,'w') as fout:
        fout.writelines(data)

def get_dir_name(path):
    if (path[-1] == os.sep):
        path = path[:-1]
    return path[path.rfind('/')+1:]

def make_modconf(path, name):
    dep_entry = []
    dep_entry_opt = []
    strings = [f'name = {name}\n', 'description = \n']
    dep_path = os.path.join(path,'depends.txt')
    if os.path.exists(dep_path):
        dep = read_data(dep_path)
        for entry in dep:
            if not (entry == ''):
                if entry.endswith('?'):
                    dep_entry_opt.append(entry[:-1])
                else:
                    dep_entry.append(entry)
    strings.append(f"depends = {', '.join(dep_entry)}\n")
    strings.append(f"optional_depends = {', '.join(dep_entry_opt)}\n")
    write_data(os.path.join(path, 'mod.conf'), strings)
    print('mod.conf created')
    os.remove(dep_path)
    print('depends.txt removed')

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
    mod_name = get_dir_name(current_path)
    make_modconf(current_path, mod_name)

if __name__ == "__main__":
    main()
