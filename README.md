# SZU_OJ_ScoreCal
计算SZU OJ系统的分数，根据AC时间以及查重结果对分数加权
评分规则：
1、周一14：10开放做题，24：00之前完成的题目给100%；
2、周二00：00到23：59完成的题目给80%；
3、周三00：00到14：10完成的题目给60%；
4、有抄袭的当次测试总成绩最高为60分。
5、所有成绩按最后一次提交为准。
6、被抄袭者目前没有处分。

运行指南：
建议使用python3.7以上版本
使用前下载查重文档并重命名成“查重{}.xlsx"
修改cookies, score_value_proto, exp_id