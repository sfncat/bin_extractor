# -*- coding:utf-8 -*-
__author__ = 'StackOF'

import os
import time

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
    book_df['full_duplicated'] = book_df.duplicated('full_filename',keep='first')
    book_df['filename_duplicated'] = book_df.duplicated('filename',keep=False)
    book_df.sort_values(by=['filename'],inplace=True)
    book_df.reset_index()
    return book_df
def get_second():
    return time.strftime("%Y%m%d_%H%M%S", time.localtime())

def write_df_lst_to_xlsx(xlsx_file:str,df_lst:list,sheet_lst:list,index_int=0):
    try:
        xf = xlsx_file
        ew = pd.ExcelWriter(xlsx_file,engine='xlsxwriter')
    except Exception as e:
        print(f'can not open {xlsx_file}')
        pre,ext = os.path.splitext(xlsx_file)
        ts = get_second()
        xf = pre+'_'+ts+ext
        ew = pd.ExcelWriter(xf,engine='xlsxwriter')
    with ew as writer:
        for cur_pos in range(len(df_lst)):
            df_lst[cur_pos].to_excel(writer,sheet_name=sheet_lst[cur_pos],index=index_int,freeze_panes=(1,0))
            column_widths = (
                df_lst[cur_pos].columns.to_series().apply(lambda x:len(x.encode('gbk'))+5).values
            )
            writer.sheets[sheet_lst[cur_pos]].autofilter(0,0,0,len(df_lst[cur_pos].columns)-1)
            for i,width in enumerate(column_widths):
                writer.sheets[sheet_lst[cur_pos]].set_column(i,i,width)
        print(f'write the {sheet_lst} to {xf}')
def delete_dup_file(path):
    file_lst = get_all_file(path,file_ext='epub')
    for cur_file in file_lst:
        file_path, full_filename, filename, ext = get_filename_ext(cur_file)
        if filename[-1] == ")" and filename[-3] =="(":
            try:
                os.remove(cur_file)
            except Exception as e:
                print(cur_file,e)
# path = '/home/kali/SSD4T_1/Book'
path = '/home/kali/backup/ePUBee-backup'
delete_dup_file(path)
# book_df_all = get_book_file_df(path)
# write_df_lst_to_xlsx('/home/kali/SSD4T_1/book_info_0104.xlsx',[book_df_all],['bookinfo'])
# for cur_row,cur_file_info in book_df_all.iterrows():
#     if cur_file_info['full_duplicated'] is True or (cur_file_info['filename'] is True and cur_file_info['ext'] != '.mobi'):
#         try:
#             os.remove(cur_file_info['filepath'])
#         except Exception as e:
#             print(cur_file_info['filepath'],e)




