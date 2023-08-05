import argparse
import getpass
import re
import shutil
import os
from colorama import Fore, Style

command = ""
parser = argparse.ArgumentParser()
parser.add_argument(
    "--base_path", type=str, help="Стартовая директория")

current_path = parser.parse_args().base_path

if not current_path:
    current_path = os.getcwd()
if current_path[len(current_path) - 1] not in ['/', '\\']:
    current_path += '\\'


def ls():
    a = list()
    for i in os.listdir(current_path):
        if os.path.isdir(os.path.join(current_path, i)):
            a.append(Fore.BLUE + i + "/" + Style.RESET_ALL)
        else:
            a.append(i)
    return '\n'.join(a)


def mkdir(dir_name: str):
    try:
        os.mkdir(os.path.join(current_path, dir_name))
    except OSError:
        print(f"Directory {dir_name} already exists")
    except Exception:
        print("Something went wrong")
    finally:
        return None


def touch(file_path: str):
    if not re.match("[A-Za-z]:|/", file_path[0]):
        f = None
        try:
            f = open(os.path.join(current_path, file_path), 'r')
            raise FileExistsError
        except FileNotFoundError:
            f = open(os.path.join(current_path, file_path), 'w+')
        except FileExistsError:
            print(f"File {file_path} already exists")
        if f:
            f.close()
    else:
        f = None
        try:
            f = open(file_path, 'r')
            raise FileExistsError
        except FileNotFoundError:
            f = open(file_path, 'w+')
        except FileExistsError:
            print(f"File {os.path.basename(file_path)} already exists")
        if f:
            f.close()
    return None


def chmod(name: str, path: str, mode: int, r=False):
    try:
        if r:
            for f in os.walk(os.path.join(path, name)):
                os.chmod(f[0], mode)  # не работает на винде, замена вроде как icacls, но там группы/пользователи
                # определяются по SIDам, а они рандомные у всех и еще синтаксис виндовский у icacls
                # вери найс хаха гейтс гоес брррр
        else:
            os.chmod(os.path.join(path, name), 0o0664)
    except Exception:
        print("Some error occurred during execution")
    finally:
        return None


def mv(old, new):
    try:
        shutil.copy2(old, new)
        os.remove(old)
    except FileNotFoundError:
        print(f"No such file or directory {old}")
    except Exception:
        print("Some error occurred during execution")
    finally:
        return None


def rename(old, new):
    try:
        os.rename(old, new)
    except Exception:
        print("Something went wrong")
    return None


def cat(file_path):
    try:
        with open(file_path, 'r') as f:
            return ''.join(i for i in f)
    except FileNotFoundError:
        print(f"No such file or directory {file_path}")
        return None
    except Exception:
        print("Some error occured during execution")
        return None


def grep(pattern, result):
    a = list()
    result = re.split("\n", result)
    for i in result:
        if re.search(pattern, i):
            a.append(i)
    return '\n'.join(a)


def cd(path):
    try:
        global current_path
        if re.match("[A-Za-z]:|/", path[0:2]):
            if os.path.exists(path):
                current_path = path
                if path[len(path) - 1] not in ['\\', '/']:  # fix for cd'ing to disk letter (cd c: happens to cause
                    # a bad path_name as it does not have \ at the end so the next cd'ing doesn't work at all
                    current_path += '\\'
            else:
                raise IsADirectoryError(f"No such directory {path}")
        else:
            path = re.split("/+|\\\+", path)
            for i in path:
                if i == '..':
                    a = os.path.split(current_path)
                    if a[1] != "":
                        current_path = a[0]
                    else:
                        current_path = os.path.split(a[0])[0]
                else:
                    if i in ls():
                        current_path = os.path.join(current_path, i)
                    else:
                        raise IsADirectoryError(f"No such directory {i}")
    except IsADirectoryError as e:
        print(e)
    except Exception:
        print("Some error occurred")


def execute(cm: str, result=None):
    cm = cm.split()
    try:
        if cm[0] in ["ls", "dir"]:
            return ls()

        if cm[0] == 'mkdir':
            return mkdir(cm[1])

        if cm[0] == 'touch':
            return touch(cm[1])

        if cm[0] == 'chmod':
            if cm[1] == '-r':
                return chmod(cm[2], current_path, int(cm[3], 8), r=True)
            else:
                return chmod(cm[1], current_path, int(cm[2], 8))

        if cm[0] in ['mv', 'move']:
            return mv(cm[1], cm[2])

        if cm[0] == 'ren':
            return rename(cm[1], cm[2])

        if cm[0] == 'cat':
            return cat(cm[1])

        if cm[0] == 'grep':
            return grep(cm[1], result)

        if cm[0] == 'cd':
            cd(cm[1])

        else:
            raise IOError(f"{cm[0]}: command not found")

    except IndexError:
        print(f"Invalid syntax in {command}")
        return None
    except IOError as e:
        print(e)
        return None


def run():
    while True:
        result = None
        global command
        command = re.split('\\|', input(
            f"{Fore.GREEN + getpass.getuser() + Fore.YELLOW} " + current_path + f"{Style.RESET_ALL}\n$ "))
        for i in command:
            if i == 0:
                result = execute(i)
            else:
                result = execute(i, result=result)
        if result:
            print(result)
            print()
