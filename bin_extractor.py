# -*- coding:utf-8 -*-
__author__ = 'StackOF'

# import logging
import os
import time
from subprocess import Popen, PIPE, STDOUT, TimeoutExpired, CalledProcessError

import fire as fire

"""
install binwalk https://github.com/ReFirmLabs/binwalk/blob/master/INSTALL.md
git clone https://github.com/ReFirmLabs/binwalk.git
cd binwalk
python3 setup.py install

install ubi_reader
sudo apt-get install liblzo2-dev
sudo pip install python-lzo
sudo pip install ubi_reader
"""


def execute_shell_command_get_return_code(shell_command, timeout=None):
    """
    Execute a shell command and return a tuple (program output, return code)
    Program output includes STDOUT and STDERR.
    This function shall not raise any errors

    :param shell_command: command to execute
    :type shell_command: str
    :param timeout: kill process after timeout seconds
    :type: timeout: int, optional
    :return: str, int
    """
    pl = Popen(shell_command, shell=True, stdout=PIPE, stderr=STDOUT)
    try:
        output = pl.communicate(timeout=timeout)[0].decode('utf-8', errors='replace')
        return_code = pl.returncode
    except TimeoutExpired:
        # logging.warning("Execution timeout!")
        pl.kill()
        output = pl.communicate()[0].decode('utf-8', errors='replace')
        output += "\n\nERROR: execution timed out!"
        return_code = 1
    return output, return_code


def execute_shell_command(shell_command, timeout=None, check=False):
    """
    Execute a shell command and return STDOUT and STDERR in one combined result string.
    This function shall not raise any errors

    :param shell_command: command to execute
    :type shell_command: str
    :param timeout: kill process after timeout seconds
    :type: timeout: int, optional
    :param check: raise CalledProcessError if the return code is != 0
    :type: check: bool
    :return: str
    """
    output, return_code = execute_shell_command_get_return_code(shell_command, timeout=timeout)
    if check and return_code != 0:
        raise CalledProcessError(return_code, shell_command)
    return output


# 按路径创建所有没有的目录
def mkdir(path):
    path = path.strip()
    path = path.rstrip("\\")
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        return True
    else:
        return False


def get_second():
    return time.strftime("%Y%m%d_%H%M%S", time.localtime())


def get_filename_ext(file_path):
    filename, ext = os.path.splitext(os.path.basename(file_path))
    return filename, ext


def get_all_file(folder_path, file_ext=''):
    file_list = []
    if folder_path is None:
        raise Exception("folder_path is None")
    for dir_path, dir_names, filenames in os.walk(folder_path):
        for name in filenames:
            if file_ext == '':
                file_list.append(os.path.join(dir_path, name))
            else:
                ext = '.' + file_ext
                if os.path.splitext(name)[1] == ext:
                    file_list.append(os.path.join(dir_path, name))
    return file_list


def extractor(file_path: str):
    print(f'extract bin file {file_path}')
    filename, ext = get_filename_ext(file_path)
    dir = os.path.dirname(file_path)
    tmp_dir = os.path.join(dir, filename + '_' + get_second() + '_extracted')
    sub_dir = '_' + filename + ext + '.extracted'
    output = execute_shell_command(f'binwalk -Me --directory  {tmp_dir} {file_path} --run-as=root')
    print(output)
    # execute_shell_command(f'cd {tmp_dir} && cd {sub_dir}')
    os.chdir(tmp_dir)

    ubi_file = get_all_file(os.path.join(tmp_dir, sub_dir), 'ubi')[0]
    ubi_basename = os.path.basename(ubi_file)
    print(f'extract ubi file {ubi_basename}')
    output = execute_shell_command(f'ubireader_extract_images -o {tmp_dir} {ubi_file} ')
    print(output)
    # os.chdir(os.path.join(dir,tmp_dir,sub_dir,'ubifs-root',ubi_basename))
    ubifs_file_lst = get_all_file('.', 'ubifs')

    for cur_file in ubifs_file_lst:
        print(f'extract ubifs file {cur_file}')
        output = execute_shell_command(f'binwalk -Me --run-as=root {cur_file}')
        print(output)


print(f'Need install binwalk ubi_reader.')
fire.Fire(extractor)
