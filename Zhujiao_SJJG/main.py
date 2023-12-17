import requests
import pandas as pd
import json
from datetime import datetime, timedelta
import configuration as cf



def days_diff(begin_time:str,time2:str)->int:
    time_obj1 = datetime.fromisoformat(begin_time)
    time_obj2 = datetime.fromisoformat(time2)
    first_day = time_obj1.day
    second_day = (time_obj1 + timedelta(days=1)).day
    if time_obj2.day == first_day:
        return 0
    elif time_obj2.day == second_day:
        return 1
    else:
        return -1
# days_diff('2023-12-12T10:10:00+08:00','2023-12-11T14:10:00+08:00')

# s1 = "2023-09-04T14:10:00+08:00"
def time_difference(s1, s2) -> bool:
    time_obj1 = datetime.fromisoformat(s1)
    time_obj2 = datetime.fromisoformat(s2)
    return time_obj1 > time_obj2


class Stu(object):

    def __init__(self, n: int):
        self.headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            "Cookie": "csrftoken=32QgxMDZkT7tx8ed97g40ppJZmpGghWRVh4wsBlSMOtx85ElnWgZt5doEGWYiwfY; sessionid=rfal6q7hmssxr67png474pfed8nejwmq",
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
            "score_value_6": [20, 20, 20, 20, 20],
            "score_value_7": [20, 20, 20, 20, 20],
            "score_value_8": [20, 20, 20, 20, 20],
            "score_value_9": [20, 20, 20, 20, 20],
            "score_value_10": [20, 20, 20, 20, 20],
            "score_value_11": [20, 20, 20, 20, 20],
            "score_value_12": [20, 20, 20, 20, 20],
            "score_value_13": [16, 16, 16, 16, 16, 20]
        }

        self.exp_id = {
            '实验1': 149,
            '实验2': 169,
            '实验3': 185,
            '实验4': 213,
            '实验5': 223,
            '实验6': 239,
            '实验7': 252,
            '实验8': 266,
            '实验9': 280,
            '实验10': 295,
            '实验11': 317,
            '实验12': 332,
            '实验13': 347
        }
        self.n = n
        self.df_cz = pd.read_excel('./EXCEL/查重{}.xlsx'.format(n), dtype={'用户A': str, '用户B': str})
        # self.start_time = time_to_seconds(14, 10)  # 开始时间 14：10
        self.copy_dict: dict[str, list[str]] = {}  # 抄袭人名单
        self.copy_pro_dict: dict[str, list[str]] = {}  # 被抄袭名单
        self.problem_list = self.pre_process()  # 预处理：删除助教和老师
        self.cha_chong()
        self.stu_dict, self.stu_list, self.group_id = self.get_stu_list()
        self.exp_begin_time=self.get_exp_begin_time()

    def get_exp_begin_time(self):
        # limit = 10 默认
        url = "http://172.31.221.67/api/contests/?offset=0&limit=100&group={}".format(self.group_id)
        response = requests.get(url, headers=self.headers)
        exp_list = json.loads(response.text)['results']
        exp_dict = {}
        for index,item in enumerate(exp_list):
            exp_dict[item.pop('id')]=item
        return exp_dict

    def get_stu_list(self) -> (dict,list,int): #获取人员名单
        #先获取班级group id
        url = "http://172.31.221.67/api/manage/groups/?limit=10"
        response = requests.get(url, headers=self.headers)
        group_id = json.loads(response.text)['results'][0]['id']
        url = "http://172.31.221.67/api/groups/{}/".format(group_id)
        response = requests.get(url, headers=self.headers)
        stu_user:list = json.loads(response.text)['users']
        sorted_list = sorted(stu_user, key=lambda x: int(x['username'])) # 按学号升序
        final_dict: dict[str: dict] = {}
        final_list: list[int] = []
        for item in sorted_list:
            final_list.append(item['username'])
            final_dict[item.pop('username')] = item # {username :{id,nickname,name}}
        return final_dict, final_list, group_id


    def pre_process(self):
        # 先获取题目id列表
        url = 'http://172.31.221.67/api/contests/problems_id/?contest={}'.format(self.exp_id['实验{}'.format(self.n)])
        problem_list: list = json.loads(requests.get(url, headers=self.headers).text)["problems_id"]["0"]

        # 删除老师和助教
        rows_to_delete_cz = []
        for index, row in self.df_cz.iterrows():
            if any(substring in str(row['用户A']) + str(row['用户B']) for substring in ['szu', 'zhujiao']):
                rows_to_delete_cz.append(index)
        self.df_cz = self.df_cz.drop(index=rows_to_delete_cz)
        self.df_cz = self.df_cz.reset_index(drop=True)
        return problem_list

    def cha_chong(self):

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
            # if 'szu' in str(user_copy['user']['username']) or 'szu' in str(user_copy_pro['user']['username']):
            #     continue
            problem_word: str = chr(self.problem_list.index(row['问题ID']) + 65)  # 将下标转化成字母ABCD
            # 抄袭成功：
            if user_copy['status'] == 0:
                # 记录抄袭者
                if self.copy_dict.get(user_copy['user']['username']):
                    if problem_word not in self.copy_dict[user_copy['user']['username']]:
                        self.copy_dict[user_copy['user']['username']].append(problem_word)
                else:
                    self.copy_dict[user_copy['user']['username']] = [problem_word]

                # 记录被抄袭者
                if row['问题ID'] == 167:  # 167问题特判 抄和被抄都记到抄的名单copy_dict
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
        file_data = {'用户名': [], '姓名': []}
        for i in range(len(self.problem_list)):
            key = '题{}'.format(chr(i + 65))  # 将下标转化成字母ABCD
            file_data[key] = []
        # 加入所有AC记录
        url = "http://172.31.221.67/api/code-submission/?offset=0&limit=100&contest={}&problem=&search=&status=".format(self.exp_id['实验{}'.format(self.n)])
        response = json.loads(requests.get(url, headers=self.headers).text)
        sub_AC_count = int(response['count'])
        sub_AC_results = list(response['results'])
        tmp_num = 100
        while tmp_num < sub_AC_count:
            url = "http://172.31.221.67/api/code-submission/?offset={}&limit=100&contest={}&problem=&search=&status=".format(tmp_num, self.exp_id['实验{}'.format(self.n)])
            response = json.loads(requests.get(url, headers=self.headers).text)
            sub_AC_results.extend(list(response['results']))
            tmp_num += 100

        # list_score = [[] for _ in range(len(self.problem_list) + 2)]  # 多一行总分与说明p
        user_dict: dict[tuple, dict] = {}  # （ (用户名, 题) ：item）
        for index, item in enumerate(sub_AC_results):
            if any(substring in item['user']['username'] for substring in ['szu', 'zhujiao']):
                continue
            tmp_tuple = (item['user']['username'], item['problem'])
            if (not user_dict.get(tmp_tuple)) or (not time_difference(user_dict[tmp_tuple]['time'], item['time'])):  # 保留时间更晚的记录
                user_dict[tmp_tuple] = item
        caption_list = []  # 修正分数原因
        total_score_list = []
        for index,xuehao in enumerate(self.stu_list):
            file_data['用户名'].append(xuehao)
            file_data['姓名'].append(self.stu_dict[xuehao]['name'])
            for i in range(len(self.problem_list)):
                problem = '题{}'.format(chr(i + 65))
                key=(xuehao,self.problem_list[i])
                if user_dict.get(key):
                    days = days_diff(self.exp_begin_time[self.exp_id['实验{}'.format(self.n)]]['begin_time'],user_dict[key]['time'])
                    if days == 0:
                        discount = 1.0
                    elif days ==1:
                        discount = 0.8
                    else:
                        discount = 0.6
                else:
                    discount=0
                score = self.score_value_proto['score_value_{}'.format(self.n)][i] * discount
                file_data[problem].append(score if user_dict.get(key) and user_dict[key]['status']==0 else 0)
            caption = ''
            total_score = sum(lst[index] for lst in list(file_data.values())[-len(self.problem_list):])

            # 找出抄袭题
            if self.copy_dict.get(xuehao):
                total_score = min(60, total_score)
            total_score_list.append(total_score)
            # 说明原因
            if self.copy_dict.get(xuehao):
                caption += '抄袭题：'
                for item in self.copy_dict[xuehao]:
                    caption += (item + ' ')
            if self.copy_pro_dict.get(xuehao):
                caption += '被抄袭题：' if len(caption) == 0 else ', 被抄袭题：'
                for item in self.copy_pro_dict[xuehao]:
                    caption += (item + ' ')
            caption_list.append(caption)
        file_data['修正总分'] = total_score_list
        file_data['说明（首日提交全额给分，次日8折，第三天6折；如有任意抄袭，总分将不高于60；\n被抄袭者获得警告，被抄袭者也可能是抄袭网上的）'] = caption_list
        df = pd.DataFrame(file_data)
        df.to_excel('./EXCEL/new上机得分{}.xlsx'.format(self.n), index=False)


def main():
    stu = Stu(13)
    stu.get_new_record()


if __name__ == "__main__":
    main()
