# -*- coding:utf-8 -*-
__author__ = 'StackOF'

import os
import pandas as pd


def get_all_file(folder_path, file_ext=''):
    file_list = []
    if folder_path is None:
        raise Exception("folder_path is None")
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for name in filenames:
            if file_ext == '':
                file_list.append(os.path.join(dirpath, name))
            else:
                ext = '.' + file_ext
                if os.path.splitext(name)[1] == ext:
                    file_list.append(os.path.join(dirpath, name))
    return file_list

def get_filename_ext(file_path):
    full_filename = os.path.basename(file_path)
    filename, ext = os.path.splitext(full_filename)
    return file_path,full_filename,filename, ext

def get_book_file_df(path:str)->pd.DataFrame:
    book_file_lst = get_all_file(path)
    book_df = pd.DataFrame.from_records(pd.DataFrame(book_file_lst)[0].apply(get_filename_ext),columns=['filepath','full_filename','filename','ext'])
    book_df['full_duplicated'] = book_df.duplicated('full_filename',keep=True)
    book_df['filename_duplicated'] = book_df.duplicated('filename',keep=False)
    return book_df

path = ''
book_df_all = get_book_file_df(path)
for cur_row,cur_file_info in book_df_all:
    if cur_file_info['full_duplicated'] is True or (cur_file_info['filename'] is True and cur_file_info['ext'] != 'mobi'):
        try:
            os.remove(cur_file_info['filepath'])
        except Exception as e:
            print(cur_file_info['filepath'],e)




