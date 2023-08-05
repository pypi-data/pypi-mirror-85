#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#--
# wine-ctl, manage Wine prefixes
# Copyright (C) 2019-2020  Marc Dequènes (Duck)

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#++
# You can find the code here: https://projects.duckcorp.org/projects/wine-ctl

VERSION = "1.0.1"


import argparse
import yaml
import jsonschema
import os
from pathlib import Path
import subprocess
import fnmatch
import re
import shutil
import shlex



class WinePrefix():
    def __init__(self, config, name):
        self.name = name
        self.config = config

        self.path = Path(config['install_path']).joinpath(self.name)

    def exists(self):
        return self.path.exists()

    @staticmethod
    def find_exe(exe_name, exe_list):
        for exe in exe_list:
            path = shutil.which(exe)
            if path:
                return path

        print("{} executable not found".format(exe_name))

    def run(self, command, debug=False, check_prefix=True):
        if check_prefix and not prefix.exists():
            print("This wine prefix does not exist")
            return False

        if debug:
            exe_path = self.__class__.find_exe("winedbg", ['winedbg-development', 'winedbg'])
        else:
            exe_path = self.__class__.find_exe("wine", ['wine-development', 'wine'])
        if not exe_path:
            return False

        os.environ['WINEPREFIX'] = str(self.path)
        if isinstance(command, str):
            if re.match(r'[\'"]?/', command):
                return subprocess.run([exe_path, 'start', '/unix'] + shlex.split(command))
            else:
                return subprocess.run([exe_path] + shlex.split(command))
        else:
            return subprocess.run(command)

    def create(self, update=False):
        exe_path = self.__class__.find_exe('wineboot', ['wineboot-development', 'wineboot'])
        if not exe_path:
            return False

        if not self.exists():
            self.path.mkdir(parents=True)
            r = self.run([exe_path, '-i'], check_prefix=False)
        elif update:
            r = self.run([exe_path, '-u'], check_prefix=False)
        else:
            return True
        return r.returncode == 0

    def configure(self):
        exe_path = self.__class__.find_exe('winecfg', ['winecfg-development', 'winecfg'])
        if not exe_path:
            return False

        if not self.exists():
           return False

        return self.run([exe_path])



exe_ignore_re = re.compile(r"(/(windows|Windows NT|Internet Explorer|Windows Media Player)/|unins\d+.exe|Unity|vc_?redist)", flags=re.IGNORECASE)

def find_and_launch(path):
    l = []
    for root, dirs, files in os.walk(path.resolve()):
        for name in files:
            f = Path(root).joinpath(name)
            if fnmatch.fnmatch(name, "*.exe") and not exe_ignore_re.search(str(f)):
                l.append(f)

    if len(l) == 0:
        print("-- no selection available --")
        return False

    for idx, inst in enumerate(l):
        print("  {}: {}".format(idx, inst.name))
    c = input("Selection (enter to exit): ")
    if c and c.isdigit() and int(c) < len(l):
        return prefix.run('"{}"'.format(str(l[int(c)])))
    return False


def action_list(config, args):
    print("List of Wine prefixes:")

    l = {}
    with os.scandir(config['install_path']) as it:
        for entry in it:
            if not entry.name.startswith('.') and entry.is_dir():
                if Path(config['install_path']).joinpath(entry.name, 'dosdevices').is_dir():
                    in_lib = Path(config['app_lib_path']).joinpath(entry.name).exists() if 'app_lib_path' in config else False
                    l[entry.name] = in_lib

    for app in sorted(l):
        lib_flag = 'L' if l[app] else ' '
        print("{}  {}".format(lib_flag, app))


def action_create(config, prefix, args):
    if args.lib:
        if 'app_lib_path' not in config:
            print("library path (app_lib_path) not defined in configuration")
            exit(1)

        app_path = Path(config['app_lib_path']).joinpath(prefix.name)
        if not app_path.exists():
            print("application '{}' is not in library".format(prefix.name))
            exit(1)

    if not prefix.create(update=args.update):
        print("prefix preparation failed")
        exit(2)

    if 'home_skel' in config:
        user_win_home = prefix.path.joinpath('drive_c', 'users', os.environ['USER'])
        user_win_home.mkdir(parents=True, exist_ok=True)
        # distutils.dir_util.copy_tree fails to update symlinks with "File exists"
        #copy_tree(config['home_skel'], str(user_win_home), preserve_symlinks=True, update=True)
        r = subprocess.run(['cp', '-a', config['home_skel'], str(user_win_home)])
        if r.returncode != 0:
            print("could not update the user home with the skeleton")
            exit(2)

    if not args.lib:
        return

    print("Available Installers:")
    r = find_and_launch(app_path)
    if r and r.returncode != 0:
        print("Installation failed")
        exit(2)


def action_config(config, prefix, args):
    r = prefix.configure()
    if r and r.returncode != 0:
        print("Execution failed")
        exit(2)


def action_run(config, prefix, args):
    if args.exe:
        r = prefix.run(args.exe, debug=args.debug)
    else:
        print("Available Executables:")
        r = find_and_launch(prefix.path)
    if r and r.returncode != 0:
        print("Execution failed")
        exit(2)


def action_dxvk(config, prefix, args):
    if not args.action:
        test_lib = prefix.path.joinpath('dosdevices', 'c:', 'windows', 'system32', 'dxgi.dll')
        status = "installed" if 'dxvk' in str(test_lib.resolve()) else "not installed"
        print("DXVK is {}".format(status))
        exit(0)

    exe_path = WinePrefix.find_exe('dxvk-setup', ['dxvk-setup'])
    if not exe_path:
        exit(2)

    r = prefix.run([exe_path, args.action, '-d'])
    if r and r.returncode != 0:
        print("Execution failed")
        exit(2)


def action_trick(config, prefix, args):
    exe_path = WinePrefix.find_exe('winetricks', ['winetricks'])
    if not exe_path:
        exit(2)

    r = prefix.run([exe_path, args.trick])
    if r and r.returncode != 0:
        print("Execution failed")
        exit(2)



if __name__ == "__main__":

    config_path = '~/.config/wine-ctl.yml'
    try:
        stream = open(Path(config_path).expanduser(), 'r')
    except Exception as e:
        print("Unable to open configuration file ({})".format(config_path))
        exit(1)
    try:
        config = yaml.safe_load(stream)
    except Exception as e:
        print("configuration file could not be parsed (not a valid YAML file)")
        exit(1)

    config_schema = """
    type: object
    properties:
      app_lib_path:
        type: string
      install_path:
        type: string
      home_skel:
        type: string
      env:
        type: object
    required: ['install_path']
    additionalProperties: False
    """
    try:
      jsonschema.validate(config, yaml.safe_load(config_schema))
    except jsonschema.exceptions.ValidationError as e:
      print("configuration error: {}".format(e.message))
      exit(1)


    # declare available subcommands and options
    parser = argparse.ArgumentParser(description='Manage Wine Prefixes')
    parser.add_argument('--version', '-v', action='version', version='%(prog)s {}'.format(VERSION))
    parser.add_argument('--quiet', '-q', action='store_true', help='less verbose display')
    subparsers = parser.add_subparsers(help='sub-command help')
    parser_list = subparsers.add_parser('list', help='list Wine prefixes')
    parser_list.set_defaults(func=action_list)
    parser_create = subparsers.add_parser('create', help='create a new Wine prefix')
    parser_create.set_defaults(func=action_create)
    parser_create.add_argument('--lib', '-l', action='store_true', help='search installer in library')
    parser_create.add_argument('--update', '-u', action='store_true', help='rerun wineboot even if the prefix already exist')
    parser_create.add_argument('name', help='Wine prefix name')
    parser_config = subparsers.add_parser('config', help='configure a Wine prefix (shorthand for running winecfg)')
    parser_config.set_defaults(func=action_config)
    parser_config.add_argument('name', help='Wine prefix name')
    parser_run = subparsers.add_parser('run', help='run application in the Wine prefix')
    parser_run.set_defaults(func=action_run)
    parser_run.add_argument('name', help='Wine prefix name')
    parser_run.add_argument('exe', nargs='?', help='optional path of the executable to run (or choice of available exe in the prefix)')
    parser_run.add_argument('--debug', '-d', action='store_true', help='run executable with the debugger')
    parser_dxvk = subparsers.add_parser('dxvk', help='setup DXVK support')
    parser_dxvk.set_defaults(func=action_dxvk)
    parser_dxvk.add_argument('name', help='Wine prefix name')
    parser_dxvk.add_argument('action', nargs='?', choices=('i', 'u'), help='install or uninstall DXVK (the default is to inform if installed)')
    parser_trick = subparsers.add_parser('trick', help='install winetrick component')
    parser_trick.set_defaults(func=action_trick)
    parser_trick.add_argument('name', help='Wine prefix name')
    parser_trick.add_argument('trick', help='winetricks component to install')



    # let's parse
    args = parser.parse_args()

    # set environment
    if 'env' in config:
        for e_var, e_val in config['env'].items():
            if e_val:
                os.environ[e_var] = str(e_val)
            elif e_var in os.environ:
                os.environ.pop(e_var)

    # action!
    if hasattr(args, 'func'):
        if hasattr(args, 'name'):
            prefix = WinePrefix(config, args.name)
            exit(args.func(config, prefix, args))
        else:
            exit(args.func(config, args))
    else:
        parser.print_help()

