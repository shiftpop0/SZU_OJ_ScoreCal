import requests
import pandas as pd
import json
from datetime import datetime


def time_to_seconds(h, m, s=0):
    """将时、分、秒转换为总秒数"""
    return h * 3600 + m * 60 + s


def seconds_to_time(total_seconds):
    """将总秒数转换为天、小时、分钟、秒的格式"""
    days, total_seconds = divmod(total_seconds, 24 * 3600)
    hours, total_seconds = divmod(total_seconds, 3600)
    minutes, seconds = divmod(total_seconds, 60)
    return days, hours, minutes, seconds


# s1 = "2023-09-04T14:10:00+08:00"
def time_difference(s1, s2) -> bool:
    time_format = "%Y-%m-%dT%H:%M:%S.%f%z"
    time_obj1 = datetime.strptime(s1, time_format)
    time_obj2 = datetime.strptime(s2, time_format)
    return time_obj1 > time_obj2


class Stu(object):

    def __init__(self, n: int):
        self.headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            "Cookie": "csrftoken=nNkbajKhYQ5wnFzuuduGVd9ywJI2Or585HYeK3bXTTgZAo8GF6SYQ2mW55GSfeQk; sessionid=uf6m1iipc67jugdnp0paavjnhlf7zsku",
            "Referer": "http://172.31.221.67/admin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
        }
        # 测试分值

        self.score_value_proto = {
            "score_value_1": [16, 16, 16, 16, 16, 20],
            "score_value_2": [20, 20, 20, 20, 20],
            "score_value_3": [20, 20, 20, 20, 20],
            "score_value_4": [20, 20, 20, 20, 20],
            "score_value_5": [25, 25, 25, 25],
            "score_value_6": [20, 20, 20, 20, 20]
        }
        self.file = {
            "file1": './EXCEL/测验149 【金融科技】【不计分】实验1——顺序表-编程排行榜2023_10_19 01_09_19.xlsx',
            "file2": './EXCEL/测验169 【金融科技】【计分】实验2——链表-编程排行榜2023_10_19 01_10_11.xlsx',
            "file3": './EXCEL/测验185 【金融科技】【计分】实验3——栈-编程排行榜2023_10_19 01_10_44.xlsx',
            "file4": './EXCEL/测验213 【金融科技】【计分】实验4——栈补充&队列-编程排行榜2023_10_19 00_51_28.xlsx',
            "file5": './EXCEL/测验223 【金融科技】【计分】实验5——串-编程排行榜2023_10_18 22_27_20.xlsx',
            "file6": './EXCEL/测验239 【金融科技】【计分】实验6——串补充&树-编程排行榜2023_11_2 12_54_13.xlsx'
        }
        self.exp_id = {
            '实验1': 149,
            '实验2': 169,
            '实验3': 185,
            '实验4': 213,
            '实验5': 223,
            '实验6': 239
        }
        self.n = n
        self.df = pd.read_excel(self.file['file{}'.format(n)], dtype={'用户名': str})
        self.df_cz = pd.read_excel('./EXCEL/查重{}.xlsx'.format(n), dtype={'用户A': str, '用户B': str})
        self.start_time = time_to_seconds(14, 10)  # 开始时间 14：10
        self.copy_dict: dict[str, list[str]] = {}  # 抄袭人名单
        self.copy_pro_dict: dict[str, list[str]] = {}  # 被抄袭名单
        self.cha_chong()

    def cha_chong(self):
        # 先获取题目id列表
        url = 'http://172.31.221.67/api/contests/problems_id/?contest={}'.format(self.exp_id['实验{}'.format(self.n)])
        problem_list: list = json.loads(requests.get(url, headers=self.headers).text)["problems_id"]["0"]

        # 再查表格
        for index, row in self.df_cz.iterrows():
            url = 'http://172.31.221.67/api/manage/clone-detect-task-log/{}/'.format(row['查重结果ID'])
            response = requests.get(url, headers=self.headers)
            sub_a = json.loads(response.text)["submission_a"]
            sub_b = json.loads(response.text)["submission_b"]
            # 如果 sub_a 的时间比 sub_b 的时间晚
            if (time_difference(sub_a['time'], sub_b['time'])):
                user_copy = sub_a
                user_copy_pro = sub_b
            else:
                user_copy = sub_b
                user_copy_pro = sub_a
            if 'szu' in str(user_copy['user']['username']) or 'szu' in str(user_copy_pro['user']['username']):
                continue
            problem_word: str = chr(problem_list.index(row['问题ID']) + 65)  # 将下标转化成字母ABCD
            # 抄袭成功：
            if user_copy['status'] == 0:
                # 记录抄袭者
                if self.copy_dict.get(user_copy['user']['username']):
                    if problem_word not in self.copy_dict[user_copy['user']['username']]:
                        self.copy_dict[user_copy['user']['username']].append(problem_word)
                else:
                    self.copy_dict[user_copy['user']['username']] = [problem_word]

                # 记录被抄袭者
                if row['问题ID'] == 167:  # 167问题特判
                    if self.copy_dict.get(user_copy_pro['user']['username']):
                        if problem_word not in self.copy_dict[user_copy_pro['user']['username']]:
                            self.copy_dict[user_copy_pro['user']['username']].append(problem_word)
                    else:
                        self.copy_dict[user_copy_pro['user']['username']] = [problem_word]
                else:
                    if self.copy_pro_dict.get(user_copy_pro['user']['username']):
                        if problem_word not in self.copy_pro_dict[user_copy_pro['user']['username']]:
                            self.copy_pro_dict[user_copy_pro['user']['username']].append(problem_word)
                    else:
                        self.copy_pro_dict[user_copy_pro['user']['username']] = [problem_word]

    # 记录新分数
    def get_new_record(self):
        col = self.df.columns.values[5:]
        list_score = [[] for _ in range(len(col) + 2)]  # 多一行总分与说明
        rows_to_delete = []  # 删除老师和助教
        for index, row in self.df.iterrows():
            if 'szu' in row['用户名'] or 'zhujiao' in row['用户名']:
                rows_to_delete.append(index)
                continue
            caption = ''  # 修正分数原因
            # 按提交时间给分数打折
            for i, problem_order in enumerate(col):
                if str(row[problem_order]) == 'nan':
                    list_score[i].append(0)
                    continue
                time = str(row[problem_order]).split('(')[0]

                if time != '':
                    h, m, s = map(int, time.split(":"))
                    total_seconds = self.start_time + time_to_seconds(h, m, s)
                    days, hours, minutes, seconds = seconds_to_time(total_seconds)
                    if days == 1:
                        discount = 0.8
                    elif days > 1:
                        discount = 0.6
                    else:
                        discount = 1.0
                else:
                    discount = 0
                score = self.score_value_proto['score_value_{}'.format(self.n)][i] * discount
                list_score[i].append(score)
            # 计算总分
            total_score = sum(lst[index] for lst in list_score[:len(col)])

            # 找出抄袭题
            if self.copy_dict.get(row['用户名']):
                total_score = min(60, total_score)
            list_score[len(col)].append(total_score)
            # 说明原因
            if self.copy_dict.get(row['用户名']):
                caption += '抄袭题：'
                for item in self.copy_dict[row['用户名']]:
                    caption += (item + ' ')
            if self.copy_pro_dict.get(row['用户名']):
                caption += '被抄袭题：' if len(caption) == 0 else ', 被抄袭题：'
                for item in self.copy_pro_dict[row['用户名']]:
                    caption += (item + ' ')
            list_score[-1].append(caption)

        for index, item in enumerate(list_score[:len(col)]):
            self.df.insert(len(self.df.columns), str(col[index]) + '修正分', item)
        self.df.insert(len(self.df.columns), '修正总分', list_score[-2])
        self.df.insert(len(self.df.columns), '说明（首日提交全额给分，次日8折，第三天6折；如有任意抄袭，总分将不高于60；\n被抄袭者获得警告，被抄袭者也可能是抄袭网上的）', list_score[-1])

        # 去掉无用列 并写入excel
        cols_to_drop = self.df.columns[4:5 + len(col)]
        self.df = self.df.drop(columns=cols_to_drop)
        self.df = self.df.drop(index=rows_to_delete)
        self.df.to_excel('./EXCEL/上机得分{}.xlsx'.format(self.n), index=False)


def main():
    stu = Stu(6)
    stu.get_new_record()


if __name__ == "__main__":
    main()
