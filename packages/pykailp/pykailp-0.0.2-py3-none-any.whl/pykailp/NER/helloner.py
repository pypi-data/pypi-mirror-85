# -*- coding: utf-8 -*-
# @Time    : 2020/8/12-23:39
# @Author  : 贾志凯
# @File    : helloner.py
# @Software: win10  python3.6 PyCharm
class sum():
    def __init__(self):
        pass

    def sum(self):
        print("hello ner")



# from pysoftNLP.similarities import similar
# test_vec =  '自然语言处理与人工智能'
# sentences = ['逍遥派掌门人无崖子为寻找一个色艺双全、聪明伶俐的徒弟，设下“珍珑”棋局，为少林寺虚字辈弟子虚竹误撞解开。',
#                  '慕容复为应召拒绝王语嫣的爱情；众人救起伤心自杀的王语嫣，后段誉终于获得她的芳心。',
#                  '鸠摩智贪练少林武功，走火入魔，幸被段誉吸去全身功力，保住性命，大彻大悟，成为一代高僧。',
#                  '张无忌历尽艰辛，备受误解，化解恩仇，最终也查明了丐帮史火龙之死乃是成昆、陈友谅师徒所为',
#                  '武氏与柯镇恶带着垂死的陆氏夫妇和几个小孩相聚，不料李莫愁尾随追来，打伤武三通',
#                  '人工智能亦称智械、机器智能，指由人制造出来的机器所表现出来的智能。',
#                  '人工智能的研究是高度技术性和专业的，各分支领域都是深入且各不相通的，因而涉及范围极广。',
#                  '自然语言认知和理解是让计算机把输入的语言变成有意思的符号和关系，然后根据目的再处理。']
# args = {'encode': 'bert', 'sentence_length': 50, 'num_classes': 9, 'batch_size': 128, 'epochs': 100}
# similar.similar(sentences,test_vec,args,3)


from pysoftNLP.extraction import keyword
text = '6月19日,《2012年度“中国爱心城市”公益活动新闻发布会》在京举行。' + \
       '中华社会救助基金会理事长许嘉璐到会讲话。基金会高级顾问朱发忠,全国老龄' + \
       '办副主任朱勇,民政部社会救助司助理巡视员周萍,中华社会救助基金会副理事长耿志远,' + \
       '重庆市民政局巡视员谭明政。'
print(text)
pos = True
seg_list = keyword.seg_to_list(text, pos)
filter_list = keyword.word_filter(seg_list, pos)

print('TF-IDF模型结果：')
keyword.tfidf_extract(filter_list)
print('TextRank模型结果：')
keyword.textrank_extract(text)
print('LSI模型结果：')
keyword.topic_extract(filter_list, 'LSI', pos)
print('LDA模型结果：')
keyword.topic_extract(filter_list, 'LDA', pos)