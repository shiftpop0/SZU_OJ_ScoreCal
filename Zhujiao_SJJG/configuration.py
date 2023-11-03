import os
import re


# def has_letter(input_string: str):  # 判断是否有字母在字符串中
#     # 使用正则表达式来匹配字母
#     pattern = r'[a-zA-Z]'
#     if re.search(pattern, input_string):
#         return True
#     else:
#         return False


def find_experiment_file(directory, n):
    # 构建正则表达式以匹配文件名中包含"实验n"的部分
    pattern = re.compile(fr'.*实验{n}.*')

    # 获取目录中的文件列表
    file_list = os.listdir(directory)

    # 遍历文件列表，找到匹配的文件名
    matching_files = [filename for filename in file_list if pattern.match(filename)]

    return matching_files


def re_file_list(n: int) -> dict['str':'str']:
    directory = './EXCEL/'  # 将目录路径替换为你的目录路径
    n = 1  # 替换为你要查找的n的值
    matching_files = find_experiment_file(directory, n)
    if matching_files:
        print("找到匹配的文件：")
        for filename in matching_files:
            print(filename)
    else:
        print("未找到匹配的文件。")
