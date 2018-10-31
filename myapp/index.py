# -*-coding:utf-8 -*-
from collections import defaultdict
from collections import Counter
import csv
import jieba
import pickle
import chardet
import codecs
import math
import numpy as np
doc_num = 630
save_root = "C:/Users/PAI/"
save_file = save_root+"pokemon.csv"
index_label= ['姓名','类型1','类型2','总计','生命值','攻击力','防御力','速度']
field_weight = [ 10, 2, 2, 5]
i_change = False
# 为不同行分别建立倒排索引 实现不同属性之间的条件查找


def index_file(file):

    global save_root, save_file, index_label, i_change, doc_num
    stop_word = []
    with open(save_root+'stop.txt', 'r',encoding='utf-8') as f:
        for line in f:
            stop_word.append(line.strip('\n'))
    doc_num = 0
    i_change=True
    inverted_index = []
    inverted_to_df = []
    tt = open(file, 'rb')
    ff = tt.readline()
    # 这里试着换成read(5)也可以，但是换成readlines()后报错
    enc = chardet.detect(ff)
    tt.close()
    header_row=list()
    # if(enc['encoding']!="utf-8-sig"):
    #     with codecs.open(file, "r", "utf8") as f:
    #         ff=f.read()
    #         with codecs.open(file, "w", 'utf8') as fd:
    #             fd.write(ff)
    #             fd.close()
    #         f.close()
    with open(file) as f:
        reader = csv.reader(f)
        # 表头属性存在全局变量

        header_row = next(reader)
        index_label = header_row

        # 为每个词每个域建立倒排表 用于计算文档频率
        for value in header_row:
            inverted_to_df.append(defaultdict(set))
        invert_length = len(inverted_to_df)

        # 为每一个文档建立倒排表 用于建立向量模型
        for index,row in enumerate(reader):
            doc_num += 1
            inverted_index.append([])
            doc_index = []
            doc_length =0
            for col,label in enumerate(row):
                # 调用结巴分词器
                cut = jieba.cut(label)
                cut_off=[]
                for value in cut:
                    if (value not in stop_word) and not (value.isdigit()):    # 小写
                        value = value.lower()
                        cut_off.append(value)

                        # 为计算df建立倒排
                        inverted_to_df[col][value].add(index)

                # 计算域文档长度
                inverted_index[index].append(len(cut_off))
                doc_length += len(cut_off)

                # 为域单独建立倒排
                cut_off = dict(Counter(cut_off).items())
                inverted_index[index].append(cut_off)

    # 计算每个词在不同域的df(文档频率)
    df = []
    for value in header_row:
        df.append(defaultdict(int))
    df.append(defaultdict(int))
    for index,row in enumerate(inverted_to_df):
        for key, value in row.items():
            df[index][key] = len(value)

    # 计算tf-idf
    for index in inverted_index:
        for pos in range(invert_length):
            for key, item in index[2*pos+1].items():
                idf = math.log(doc_num / df[pos][key])
                index[2 * pos + 1][key] = (math.log(index[2 * pos + 1][key]) + 1) * idf
            index[2 * pos] = 0
            for key, item in index[2*pos+1].items():
                index[2 * pos] += item*item
            index[2 * pos] = math.sqrt(index[2*pos])

    # 保存至磁盘
    save_obj(inverted_index, 'result_doc')
    save_obj(df, 'result_df')
    save_file = file
    return inverted_index,header_row


def index_init():
    global index_label, save_file, save_root
    save_file = save_root + "pokemon.csv"

    index_label = ['名字','基本信息','出场信息','关键属性']
    return index_label


# 向量空间模型计算每个文档得分
def rank(input_doc_list, fieldlist):
    global field_weight
    doc = list(load_obj('result_doc'))
    scores = [0]*len(doc)
    for index, value in enumerate(doc):
        field_num = 0
        for field in fieldlist:
            field = int(field)
            field_doc = dict(value[field*2+1])
            field_doc_length = value[field*2]

            # 计算某个域中的sim(d1,d2)
            score = 0.0
            for key, pos in input_doc_list[field_num].items():
                if key in field_doc.keys():
                    score += pos * field_doc[key] * field_weight[field]
                    score /= field_doc_length
            scores[index] += score
            field_num += 1
    return scores


# search_mode代表搜索模式 0:普通搜索 1:精确搜索
def search(search_mode, search_index_list, header_list=None):
    global save_file, stop_words, doc_num
    # 精确搜索
    answer_doc = []
    scores = []
    if search_mode == '0':
        cut = jieba.cut(search_index_list)
        cut_off = []
        for mini in cut:
            mini = mini.lower()
            if mini != " ":
                cut_off.append(mini)
        cut_vector =dict(Counter(cut_off).items())
        df = list(load_obj('result_df'))
        cut_vector_list = []
        for key, value in cut_vector.items():
            for index in range(len(df)-1):
                cut_vector = dict(Counter(cut_off).items())
                if key in dict(df[index]).keys():
                    df_m = dict(df[index])[key]
                    if dict(df[index])[key] != 0:
                        idf = math.log(doc_num / df_m)
                        cut_vector[key] = (math.log(cut_vector[key]) + 1) * idf
                    else:
                        cut_vector[key] = 0
                else:
                    cut_vector[key] = 0
                cut_vector_list.append(cut_vector)
        scores = rank(cut_vector_list, range(len(df)-1))

    if search_mode == '1':
        # 读取
        search_index_po = search_index_list.split('?')
        header_po = header_list.split('?')
        cut_vector_list = []
        for i, search_index in enumerate(search_index_po):
            df = list(load_obj('result_df'))
            if search_index == "":
                header_po.pop()
                break
            # 输入切割
            cut = jieba.cut(search_index)
            cut_off = []
            for mini in cut:
                mini = mini.lower()
                cut_off.append(mini)
            cut_vector = dict(Counter(cut_off).items())

            # 输入计算tf-idf
            header_po[i] = int(header_po[i])
            for key, value in cut_vector.items():
                if key in dict(df[header_po[i]]):
                    df_m = dict(df[header_po[i]])[key]
                    if df_m != 0:
                        idf = math.log(doc_num / df_m)
                        cut_vector[key] = (math.log(cut_vector[key]) + 1) * idf
                    else:
                        cut_vector[key] = 0
                else:
                    cut_vector[key] = 0
            cut_vector_list.append(cut_vector)

        # 计算文档得分
        scores = rank(cut_vector_list, header_po)

    with open(save_file) as f:
        reader = csv.reader(f)
        header_row = next(reader)
        reader_list = list(reader)
        max_index = list(np.argsort(scores))
        print(max_index)
        for index in reversed(max_index):
            if scores[index] != 0.0:
                answer_doc.append(reader_list[index])
            else:
              break
    return answer_doc


def save_obj(obj, name ):
    global  save_root
    with open(save_root+'obj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name ):
    global save_root
    with open(save_root+'obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)
