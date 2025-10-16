# import xlsxwriter
import pandas as pd
import os, re
import numpy as np

from utils import *

data_root_dir = '../Datasets/original/'
save_dir = "../Datasets/preprocessed_data/"

char_to_remove = ['+', '-', '*', '/', '=', '++', '--', '\\', '<str>', '<char>', '|', '&', '!']

if not os.path.exists(save_dir):
    os.makedirs(save_dir)

file_lvl_dir = data_root_dir + 'File-level/'
line_lvl_dir = data_root_dir + 'Line-level/'


def is_comment_line(code_line, comments_list):

    code_line = code_line.strip()

    if len(code_line) == 0:
        return False
    elif code_line.startswith('//'):
        return True

    return False

def is_head_line(code_line):
    if code_line.startswith("import") or code_line.startswith("package"):
        return True
    return False

def is_empty_line(code_line):


    if len(code_line.strip()) == 0:
        return True

    return False


def preprocess_code_line(code_line):

    code_line = re.sub("\'\'", "\'", code_line)
    code_line = re.sub("\".*?\"", "<str>", code_line)
    code_line = re.sub("\'.*?\'", "<char>", code_line)
    code_line = re.sub('\b\d+\b', '', code_line)
    code_line = re.sub("\\[.*?\\]", '', code_line)
    code_line = re.sub("[\\.|,|:|;|{|}|(|)]", ' ', code_line)

    for char in char_to_remove:
        code_line = code_line.replace(char, ' ')
    code_line = code_line.strip()
    return code_line


def create_code_df(code_str, filename):


    df = pd.DataFrame()

    code_lines = code_str.splitlines()

    preprocess_code_lines = []
    is_comments = []
    is_heads = []
    is_blank_line = []

    comments = re.findall(r'(/\*\*[\s\S]*?\*/)', code_str, re.DOTALL)
    comments_str = '\n'.join(comments)
    comments_list = comments_str.split('\n')
    is_comment=False
    for l in code_lines:
        l = l.strip()
        if l.startswith('/*'):
            is_comment=True
        line_is_comment = is_comment|is_comment_line(l, comments_list)
        is_comments.append(line_is_comment)
        if l.endswith('*/'):
            is_comment=False
        is_head = is_head_line(l)
        is_heads.append(is_head)

        is_blank_line.append(is_empty_line(l))
        preprocess_code_lines.append(l)
    if 'test' in filename:
        is_test = True
    else:
        is_test = False

    df['filename'] = [filename] * len(code_lines)
    df['is_test_file'] = [is_test] * len(code_lines)
    df['code_line'] = preprocess_code_lines
    df['line_number'] = np.arange(1, len(code_lines) + 1)
    df['is_comment'] = is_comments
    df['is_head'] = is_heads
    df['is_blank'] = is_blank_line

    return df


def preprocess_data(proj_name):
    cur_all_rel = all_releases[proj_name]
    for rel in cur_all_rel:
        file_level_data = pd.read_csv(file_lvl_dir + rel + '_ground-truth-files_dataset.csv', encoding='latin')
        line_level_data = pd.read_csv(line_lvl_dir + rel + '_defective_lines_dataset.csv', encoding='latin')

        file_level_data = file_level_data.fillna('')

        buggy_files = list(line_level_data['File'].unique())

        preprocessed_df_list = []

        for idx, row in file_level_data.iterrows():

            filename = row['File']

            if '.java' not in filename:
                continue

            code = row['SRC']
            label = row['Bug']
     
            code_df = create_code_df(code, filename)
       
            code_df['file-label'] = [label] * len(code_df)
            code_df['line-label'] = [False] * len(code_df)

            if filename in buggy_files:
                buggy_lines = list(line_level_data[line_level_data['File'] == filename]['Line_number'])
                code_df['line-label'] = code_df['line_number'].isin(buggy_lines)

            if len(code_df) > 0:
                preprocessed_df_list.append(code_df)

        all_df = pd.concat(preprocessed_df_list)
        all_df=all_df[(all_df['is_comment']==False)&(all_df['is_blank']==False)]
        all_df=all_df.drop(['is_comment','is_blank'],axis=1)
        all_df.to_csv(save_dir + rel + ".csv", index=False)

        print('finish release {}'.format(rel))


for proj in list(all_releases.keys()):
    preprocess_data(proj)
