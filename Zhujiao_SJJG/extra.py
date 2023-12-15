# 实验8和9的 176 Huffman树题，选1做对即可
import pandas as pd


def extra_1():
    df8 = pd.read_excel('./EXCEL/new上机得分8.xlsx', dtype={'用户名': str})
    df9 = pd.read_excel('./EXCEL/new上机得分8.xlsx', dtype={'用户名': str})
    cj = {}
    for index, row in df8.iterrows():
        cj[row['用户名']] = row['题D']
    for index, row in df9.iterrows():
        cj[row['用户名']] = max(row['题A'], cj[row['用户名']])
    for index, row in df8.iterrows():
        if (str(row.iloc[-1]) != 'nan' and len(row.iloc[-1].split('被')[0]) > 1):
            if 'D' in row.iloc[-1].split('被')[0]:
                continue
        df8.loc[index,'题D'] = cj[row['用户名']]
        total = row['题A'] + row['题B'] + row['题C'] + cj[row['用户名']] + row['题E']
        modify_total = min(total, 60) if (str(row.iloc[-1]) != 'nan' and len(row.iloc[-1].split('被')[0]) > 1) else total
        df8.loc[index,'修正总分'] = modify_total
    for index, row in df9.iterrows():
        if (str(row.iloc[-1]) != 'nan' and len(row.iloc[-1].split('被')[0]) > 1):
            if 'A' in row.iloc[-1].split('被')[0]:
                continue
        df9.loc[index,'题A'] = cj[row['用户名']]
        total = cj[row['用户名']] + row['题B'] + row['题C'] + row['题D'] + row['题E']
        modify_total = min(total, 60) if (str(row.iloc[-1]) != 'nan' and len(row.iloc[-1].split('被')[0])>1) else total
        df9.loc[index,'修正总分'] = modify_total
    df8.to_excel('./EXCEL/new上机得分8.xlsx', index=False)
    df9.to_excel('./EXCEL/new上机得分9.xlsx', index=False)

if __name__ == "__main__":
    extra_1()