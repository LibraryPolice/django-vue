# -*-coding:utf-8 -*-
from collections import defaultdict
import csv
import jieba
import pickle
import chardet
import codecs
stop_words = {'.', ' ', 'the', ':', ',', '-','a'}
save_file = "/home/www/upload/pokemon_data.csv"
index_label= ['姓名','类型1','类型2','总计','生命值','攻击力','防御力','速度']
i_change = False
#为不同行分别建立倒排索引 实现不同属性之间的条件查找
def index_file(file):
    global save_file,stop_words,index_label,i_change
    i_change=True
    inverted_index = []

    tt = open(file, 'rb')
    ff = tt.readline()
    # 这里试着换成read(5)也可以，但是换成readlines()后报错
    enc = chardet.detect(ff)
    tt.close()
    header_row=list()
    if(enc['encoding']!="utf-8-sig"):
        with codecs.open(file, "r", "gbk") as f:
            ff=f.read()
            with codecs.open(file, "w", 'utf8') as fd:
                fd.write(ff)
                fd.close()
            f.close()
        with open(file) as f:
            reader = csv.reader(f)
            #表头属性存在全局变量
            header_row=next(reader)
            index_label=header_row
            #根据表头个数建立多个倒排表,其中一个表是一个string=>set 的dict
            for value in header_row:
                inverted_index.append(defaultdict(set))
            for index,row in enumerate(reader):

                for col,label in enumerate(row):
                    cut = jieba.cut(label)
                    for mini in cut:
                        if (mini not in stop_words):
                            # if (mini not in stop_words) and not (mini.isdigit()) :
                            mini = mini.lower()

                            inverted_index[col][mini].add(index)
        #set无法直接序列化 将其转为list
    for col in range(len(inverted_index)):
        for value in inverted_index[col].keys():
            inverted_index[col][value] = list(set(inverted_index[col][value]))
    save_obj(inverted_index,'result')
    save_file =file
    return inverted_index,header_row


def index_init():
    global index_label,save_file
    save_file = "/home/www/upload/pokemon_data.csv"

    index_label = ['姓名', '类型1', '类型2', '总计', '生命值', '攻击力', '防御力', '速度']
    lis = list(load_obj('ini_result'))
    return lis,index_label

def search(search_index_list,header_list):
    # 读取
    search_index_po=search_index_list.split('?')
    header_po=header_list.split('?')
    global save_file, stop_words
    if(i_change):
        dic_list = list(load_obj('result'))
    else:
        dic_list = list(load_obj('ini_result'))
    #print(dic.keys())
    midset = set()
    first_set = True
    first_mid_set = True
    result_in = list()
    for i,search_index in enumerate(search_index_po):
        if(search_index == ""):
            break
        cut = jieba.cut(search_index)
        first_set = True
        midmidset=set()
        for mini in cut:
            mini = mini.lower()
            if mini in dict(dic_list[int(header_po[i])]).keys():
                 if first_set:
                     midmidset = set(dict(dic_list[int(header_po[i])])[mini])
                     first_set= False

                 midmidset = midmidset | set(dict(dic_list[int(header_po[i])])[mini])
        if( first_mid_set ):
            midset=midmidset
            first_mid_set=False
        else:
            midset =midset & midmidset
    with open(save_file) as f:
        reader = csv.reader(f)
        header_row = next(reader)
        for index, row in enumerate(reader):
            if index in midset:
                result_in.append(row)
    return result_in


def save_obj(obj, name ):
    with open('/home/www/upload/obj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name ):
    with open('/home/www/upload/obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)