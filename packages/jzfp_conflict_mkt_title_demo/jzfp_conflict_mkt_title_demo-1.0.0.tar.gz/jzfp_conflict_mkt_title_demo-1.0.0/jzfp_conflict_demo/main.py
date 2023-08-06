#!/usr/bin/env python3
# coding:utf-8
# ===============================================================================

import datetime
import pandas as pd
import re
from configparser import RawConfigParser
# RawConfigParser是最基础的INI文件读取类，ConfigParser、SafeConfigParser支持对%(value)s变量的解析。

def getYesterday(dd):
    today = datetime.date.today()
    oneday = datetime.timedelta(days=dd)
    yesterday = today - oneday
    return yesterday.strftime('%Y-%m-%d')

def is_contains_chinese(strs):
    # 是否包含中文
    for _char in strs:
        if '\u4e00' <= _char <= '\u9fa5':
            return True
    return False

def conflict(cate3_id,df2,fea_out):
    # 初始化
    out_put_dict = {}
    mkt_output = []
    title_output = []

    # 配置文件传参
    print('=== Read cfg profiles ===')
    # 初始化类
    cp = RawConfigParser()
    cp.read("setup.cfg")
    sections = cp.sections()[0]

    # 01 属性字典
    attr_dict = eval(eval(cp.get(sections, "attr_dict")))  # 第一次eval还是str再包一层eval
    # 02 营销标签字典
    mkt_dict = eval(eval(cp.get(sections, "mkt_dict")))
    mkt_df = pd.DataFrame(mkt_dict)
    # 02 类目字典
    cate_list = eval(eval(cp.get(sections, "cate_list")))
    cate_s = ",".join(["'" + i + "'" for i in [i for i in cate_list.keys()]])[1:-1]
    # 03 互斥字典--total
    conflict_dict = eval(eval(cp.get(sections, "conflict_dict")))
    # 04 互斥字典--营销标签和营销标签
    conflict_mkts = eval(eval(cp.get(sections, "conflict_mkts")))
    df_mkts = pd.DataFrame(conflict_mkts)
    # 05 互斥字典--标题词和标题词
    conflict_words = eval(eval(cp.get(sections, "conflict_words")))
    df_words = pd.DataFrame(conflict_words)
    # 05 相似度阈值
    sim_threshold = cp.getfloat(sections, "sim_threshold")
    # 06 最少相似sku阈值
    sku_num_threshold = cp.getint(sections, "sku_num_threshold")
    # 07 返回标题词数
    title_N = cp.getint(sections, "title_N")

    fea_list = fea_out.split(",")
    fea_id_list = [attr_dict[i] for i in fea_list if i in attr_dict]
    print('fea_id_list:',fea_id_list)
    # 结合相似度计算tag得分 然后返回topN
    # 剔除大括号
    parttern = re.compile("{|}|'")
    df3 = df2.copy()
    df3['titlewords'] = df3.titlewords.map(lambda x: re.sub(parttern, "", x.lower()))
    df3['mktwordsname'] = df3.mktwordsname.map(lambda x: re.sub(parttern, "", x.lower()))

    # --01 过滤相似度 并similarity**10
    # 把小于阈值但是在topN的sku也包括进来 --update 2020-11-04
    if df3[df3.similarity.map(lambda x: float(x) >= sim_threshold)].shape[0] >= sku_num_threshold:
        df3 = df3[df3.similarity.map(lambda x: float(x) >= sim_threshold)]  # 注意调整！！！
    else:
        df3 = df3.sort_values(by='similarity', ascending=False).head(sku_num_threshold)

    print('参与计算的sku数', df3.shape[0])

    df3['similarity'] = df3.similarity.map(lambda x: float(x) ** 10)

    # --02 explode
    # title
    df31 = df3.set_index(["sku_id", "similarity"])["titlewords"].str.split(",", expand=True). \
        stack().reset_index(drop=False, level=0).reset_index().rename(columns={0: "subtype_word4title"})
    # 剔除空数据
    df31 = df31[df31.subtype_word4title.map(lambda x: len(x) >= 3)]
    df31['title_word_subtype'] = df31.apply(lambda x: x.subtype_word4title.split("_")[0], axis=1)
    df31['title_word'] = df31.apply(lambda x: x.subtype_word4title.split("_")[1].split(":")[0], axis=1)
    df31['title_word_score'] = df31.apply(lambda x: x.subtype_word4title.split("_")[1].split(":")[1], axis=1)
    df31['final_score'] = df31.apply(lambda x: float(x.similarity) * float(x.title_word_score), axis=1)
    df31 = df31[df31['title_word'].map(lambda x: is_contains_chinese(x) == True
                                                 or x in ['ins', 'bf', 'bm', 'logo', 'polo', 'cos', 'oversize'])]
    df41 = df31[['title_word_subtype', 'title_word', 'final_score']] \
        .groupby(['title_word_subtype', 'title_word']).sum() \
        .sort_values('final_score', axis=0, ascending=False, inplace=False, kind='quicksort',
                     na_position='last').reset_index()
    # 营销标签
    if df3[df3['mktwordsname'] != '0'].shape[0] == 0:
        df42 = pd.DataFrame()
        print("营销标签为null")
    else:
        df32 = df3.set_index(["sku_id", "similarity"])["mktwordsname"].str.split(",", expand=True). \
            stack().reset_index(drop=False, level=0).reset_index().rename(columns={0: "subtype_word4mkt"})
        # 剔除空数据
        df32 = df32[df32.subtype_word4mkt.map(lambda x: len(x) >= 3)]
        df32['mkt_word'] = df32.apply(lambda x: x.subtype_word4mkt.split(":")[0]
        if ":" in x.subtype_word4mkt else -1, axis=1)
        df32['mkt_word_score'] = df32.apply(lambda x: x.subtype_word4mkt.split(":")[1]
        if ":" in x.subtype_word4mkt else -1, axis=1)
        df32['final_score'] = df32.apply(lambda x: float(x.similarity) * float(x.mkt_word_score), axis=1)

        df42 = df32[['mkt_word', 'final_score']] \
            .groupby('mkt_word').sum() \
            .sort_values('final_score', axis=0, ascending=False, inplace=False, kind='quicksort',
                         na_position='last').reset_index()

    # 输出候选标签和标题词  df42 和 df41
    if df42.shape[0] == 0:
        mkt_output = []
    else:
        # 过滤这个类目不能推荐的标签 & 剔除和属性互斥的mkt
        df42 = pd.merge(mkt_df[mkt_df['cate3id'] == cate3_id], df42, left_on='mkt_name', right_on='mkt_word')
        df42['hc_attr_id'] = df42.apply(
            lambda x: conflict_dict['mkt_rules'][x.mkt_id]['attr_id'] if x.mkt_id in conflict_dict['mkt_rules'] else '-1', axis=1)
        mkt_num_org = df42.shape[0]
        df42 = df42[df42.hc_attr_id.map(lambda x: len(set(x.split(",")) - set(fea_id_list)) == len(x.split(",")))]

        # 处理 mkt 和mkt的互斥（简化处理：剔除所有互斥对中较小的，会牺牲精度）
        drop_42 = pd.merge(df_mkts, df42[['mkt_id', 'mkt_name', 'final_score']], left_on='mkt_name_x',
                           right_on='mkt_name')
        drop_42 = drop_42.drop(['mkt_id_x', 'mkt_name_x'], axis=1)
        drop_42.columns = ['mkt_id_y', 'mkt_name_y', 'mkt_id_x', 'mkt_name_x', 'final_score_x']
        drop_42 = pd.merge(drop_42, df42[['mkt_id', 'mkt_name', 'final_score']], left_on='mkt_name_y',
                           right_on='mkt_name')
        drop_42 = drop_42.drop(['mkt_id_y', 'mkt_name_y'], axis=1)
        drop_42.columns = ['mkt_id_x', 'mkt_name_x', 'final_score_x', 'mkt_id_y', 'mkt_name_y', 'final_score_y']

        if drop_42.shape[0] == 0:
            print("*** 不存在不同类别营销标签之间的互斥 ***")
        else:
            # 剔除需要被剔除的mkt
            drop_42_list = list(drop_42[drop_42.final_score_x >= drop_42.final_score_y]['mkt_name_y'].unique())
            df42 = df42[~df42.mkt_name.isin(drop_42_list)]

        # 同类的mkt输出top1
        df42['type'] = df42.apply(lambda x: "_".join(x.mkt_name.split("_")[0:2]), axis=1)
        for k in df42['type'].unique():
            mkt_output += list(
                df42[df42['type'] == k].sort_values(by='final_score', ascending=False).head(1)['mkt_name'])

        # print(">" * 15, '最终输出的营销标签:\n', mkt_output)

    # 处理 title 和 mkt+attr 的互斥
    # 汇总属性和已经输出的营销标签 并去重 & 剔除这些标题词
    attr_mkt_out = list(set([i.split("_")[2] for i in mkt_output] + [i.split("_")[1] for i in fea_list]))
    a = [conflict_dict['title_rules'][i] for i in attr_mkt_out if i in conflict_dict['title_rules']]
    b = []
    for i in a:
        b += i.split(",")
    df41 = df41[~df41['title_word'].isin(list(set(b)))]

    # 处理 title 和 title 的互斥
    drop_41 = pd.merge(df_words, df41[['title_word', 'final_score']], left_on='tag1', right_on='title_word')
    drop_41 = drop_41.drop(['title_word'], axis=1)
    drop_41.columns = ['tag1', 'tag2', 'final_score_1']
    drop_41 = pd.merge(drop_41, df41[['title_word', 'final_score']], left_on='tag2', right_on='title_word')
    drop_41 = drop_41.drop(['title_word'], axis=1)
    drop_41.columns = ['tag1', 'tag2', 'final_score_1', 'final_score_2']

    if drop_41.shape[0] == 0:
        print("*** 不存在标题词之间的互斥 ***")
    else:
        # 剔除需要被剔除的mkt
        drop_41_list = list(drop_41[drop_41.final_score_1 >= drop_41.final_score_2]['tag2'].unique())
        df41 = df41[~df41.title_word.isin(drop_41_list)]

    # 输出标题词topN
    title_output += list(df41.sort_values(by='final_score', ascending=False).head(title_N)['title_word'])
    # print(">" * 15, '最终输出的标题词:\n', title_output, '\n')
    # 输出
    out_put_dict.update({'mkt_output': ",".join(mkt_output), 'title_output': ",".join(title_output)})
    print(out_put_dict, '\nWork Done')

    return out_put_dict

# if __name__ == '__main__':
#     # input
#     # 1）过滤了类目的sku的特征（三级类目id、标题、标签）和相似度 = 拍照购返回相似sku列表 + es返回相似sku的特征 + 商家输入的cateid
#     # 2）过完互斥的属性 list
#
#     # 外部入参
#     cate3_id = '9733'
#     df2 = pd.read_csv('/Users/liuyaqi/PycharmProjects/pypi_test/package_test.csv') # 临时测试
#     fea_out = '厚度_常规,图案_纯色,基础风格_青春流行,版型_修身型,袖长_短袖,适用人群_青少年,适用场景_商务,适用季节_夏季,风格_商务休闲'
#     out_put_dict = main(cate3_id,df2,fea_out)
#
#     print('Work Done')


