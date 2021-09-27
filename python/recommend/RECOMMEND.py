#!/usr/bin/python3
# coding=utf-8
import random
import math
import sys
from collections import defaultdict
from operator import itemgetter
import pandas as pd

RECOMMEND_K = 40
TRAIN_DATA = {}
USER_SIMILARITY_W = {}

def split_data(data, M, K, seed):
    test = {}
    train = {}
    random.seed(seed)
    for user, item in data:
        if random.randint(0, M) != K:
            if user not in train:
                train[user] = {}
            train[user][item] = 1
        else:
            if user not in test:
                test[user] = {}
            test[user][item] = 1
    return train, test

def read_csv_data(data_set_file):
    data = []
    count = 0
    with open(data_set_file) as f:
        for line in f:
            # 数据量太大，运行不了，缩小数据量
            if count > 500000:
                break
            if not line.startswith("userId"):
                arr = line.split(',')
                data.append([arr[0], arr[1]])
                count += 1
            
    return data

def recall(train, test, N, K, w):
    """召回率算法.
    @param train: {user1: xxx, user2: xxx}
    @param test: {user1: xxx, user2: xxx, user3: xxx}
    @param N: 推荐N种 
    @param K: 推荐协同过滤K个用户 
    """
    hit = 0
    all = 0
    for user in train.keys():
        # 可能测试数据集中无此用户，遇到了冷用户
        tu = test[user] if user in test else {}
        # rank = user_recommend(user, train, w, K)
        rank = item_recommend(user, train, w, K)
        new_rank = []
        if len(rank.keys()) > N:
            new_rank = sorted(rank.items(), key=itemgetter(1), reverse=True)[0:N]
            # new_rank = sorted(rank.items(), key=itemgetter(1), reverse=True)
            # print(new_rank)
        else:
            new_rank = sorted(rank.items(), key=itemgetter(1), reverse=True)
        for item, pui in new_rank:
            if item in tu:
                hit += 1
        all += len(tu)
    return hit / (all * 1.0)

def precision(train, test, N, K, w):
    """准确率算法
    @param train: {user1: xxx, user2: xxx}
    @param test: {user1: xxx, user2: xxx, user3: xxx}
    @param N: 推荐N种 
    @param K: 推荐协同过滤K个用户 
    """
    hit = 0
    all = 0
    for user  in train.keys():
        tu = test[user] if user in test else {}
        # tu = test[user]
        # rank = user_recommend(user, train, w, K)
        rank = item_recommend(user, train, w, K)
        new_rank = []
        if len(rank.keys()) > N:
            new_rank = sorted(rank.items(), key=itemgetter(1), reverse=True)[0:N]
            # new_rank = sorted(rank.items(), key=itemgetter(1), reverse=True)
            # print(new_rank)
        else:
            new_rank = sorted(rank.items(), key=itemgetter(1), reverse=True)
        for item, pui in new_rank:
            if item in tu:
                hit += 1
        all +=  len(new_rank)
    return hit / (all * 1.0)

def coverage(train, test, N, K, w):
    """覆盖度.
    @param train: {user1: xxx, user2: xxx}
    @param test: {user1: xxx, user2: xxx, user3: xxx}
    @param N: 推荐N种 
    @param K: 推荐协同过滤K个用户 
    """
    recommend_items = set()
    all_items = set()
    for user in train.keys():
        for item in train[user].keys():
            all_items.add(item)
        # rank = user_recommend(user, train, w, K)
        rank = item_recommend(user, train, w, K)
        new_rank = []
        if len(rank.keys()) > N:
            new_rank = sorted(rank.items(), key=itemgetter(1), reverse=True)[0:N]
            # new_rank = sorted(rank.items(), key=itemgetter(1), reverse=True)
            # print(new_rank)
        else:
            new_rank = sorted(rank.items(), key=itemgetter(1), reverse=True)
        for item, pui in new_rank:
            recommend_items.add(item)
    return len(recommend_items) / (len(all_items) * 1.0)


def polularity(train, test, N, K, w):
    """流行度算法
    @param train: {user1: xxx, user2: xxx}
    @param test: {user1: xxx, user2: xxx, user3: xxx}
    @param N: 推荐N种 
    @param K: 推荐协同过滤K个用户 
    """
    item_popularity = dict()
    for user, items in train.items():
        for item in items.keys():
            if item not in item_popularity:
                item_popularity[item] = 0
            item_popularity[item] += 1
    ret = 0
    n = 0
    for user in train.keys():
        # rank = user_recommend(user, train, w, K)
        rank = item_recommend(user, train, w, K)
        new_rank = []
        if len(rank.keys()) > N:
            new_rank = sorted(rank.items(), key=itemgetter(1), reverse=True)[0:N]
            # new_rank = sorted(rank.items(), key=itemgetter(1), reverse=True)
            # print(new_rank)
        else:
            new_rank = sorted(rank.items(), key=itemgetter(1), reverse=True)
        for item, pui in new_rank:
            ret += math.log(1 + item_popularity[item])
            n += 1
    ret /= n * 1.0
    return ret


def user_similarity_source(train):
    """用户余弦相似度计算，暴力计算"""
    w = dict()
    for u in train.keys():
        for v in train.keys():
            if u == v:
                continue
            w[u][v] = len(train[u] & train[v])
            w[u][v] /= math.sqrt(len(train[u]) * len(train[v]) * 1.0)
    return w

def user_similarity_inverse(train):
    """用户倒置相似度算法
    @param train: {user1: {item1: 1, item2: 1, item3: 1}}
    """
    # build inverse table for item_users
    item_users = defaultdict(set)
    for u, items in train.items():
        for i in items.keys():
            item_users[i].add(u)
    
    # calculate co-rated items between users
    c = {}
    n = defaultdict(int)
    for i, users in item_users.items():
        for u in users:
            n[u] += 1
            for v in users:
                if u == v:
                    continue
                if u not in c:
                    c[u] = defaultdict(int)
                c[u][v] += 1
    
    # calculate finial similarity matrix w
    w = {}
    for u, related_users in c.items():
        for v, cuv in related_users.items():
            if u not in w:
                w[u] = defaultdict(float)
            w[u][v] = cuv / math.sqrt(n[u] * n[v])
    return w


def user_similarity_iif(train):
    """用户倒置相似度算法
    @param train: {user1: {item1: 1, item2: 1, item3: 1}}
    """
    # build inverse table for item_users
    item_users = defaultdict(set)
    for u, items in train.items():
        for i in items.keys():
            item_users[i].add(u)
    # calculate co-rated items between users
    c = {}
    n = defaultdict(int)
    for i, users in item_users.items():
        for u in users:
            n[u] += 1
            for v in users:
                if u == v:
                    continue
                if u not in c:
                    c[u] = defaultdict(int)
                c[u][v] += 1 / math.log(1+len(users))
    
    # calculate finial similarity matrix W
    w = {}
    for u, related_users in c.items():
        for v, cuv in related_users.items():
            if u not in w:
                w[u] = defaultdict(float)
            w[u][v] = cuv / math.sqrt(n[u] * n[v])
    return w

def user_recommend(user, train, w, K):
    """用户推荐算法.
    @param train: {user: {item1: 1, item2: 1, item3: 1}}
    @param w: {user1: {user2: xxx, user3: xxx}, user2: {user1: xxx, user3: xxx}}
    @param K: 推荐商品个数
    """
    rank = defaultdict(float)
    # if user not in train:
    #     print(train)
    #     print('遇到了冷数据')
    interacted_items = train[user]
    for v, wuv in sorted(w[user].items(), key=itemgetter(1), reverse=True)[0: K]:
        for i, rvi in train[v].items():
            # we should filter items user interacted before
            if i in interacted_items:
                continue
            rank[i] += wuv * rvi
    # TODO 若遇到冷启动客户，如何处理
    return rank


class ItemRecommendEntry(object):
    def __init__(self):
        self.weight = 0.0
        self.reason = {}

def item_similarity(train):
    """item相似度算法
    @param train: {user1: {item1: 1, item2: 1, item3: 1}}
    """
    # calculate co-rated items between users
    c = {}
    n = defaultdict(int)
    for u, items in train.items():
        for i in items:
            n[i] += 1
            for j in items:
                if i == j:
                    continue
                if i not in c:
                    c[i] = defaultdict(int)
                c[i][j] += 1
    
    # calculate finial similarity matrix W
    w = {}
    for i, related_items in c.items():
        for j, cij in related_items.items():
            if i not in w:
                w[i] = defaultdict(float)
            w[i][j] = cij / math.sqrt(n[i] * n[j])
    return w

def item_similarity_iuf(train):
    """item iuf相似度算法
    认为活跃用户对物品相似度的贡献应该小于不活跃的用户，
    所以增加一个IUF（Inverse User Frequence）参数来修正物品相似度的计算公式
    @param train: {user1: {item1: 1, item2: 1, item3: 1}}
    """
    # calculate co-rated items between users
    c = {}
    n = defaultdict(int)
    for u, items in train.items():
        for i in items:
            n[i] += 1
            for j in items:
                if i == j:
                    continue
                if i not in c:
                    c[i] = defaultdict(int)
                c[i][j] += 1 / math.log(1 + len(items) * 1.0)
    
    # calculate finial similarity matrix W
    w = {}
    for i, related_items in c.items():
        for j, cij in related_items.items():
            if i not in w:
                w[i] = defaultdict(float)
            w[i][j] = cij / math.sqrt(n[i] * n[j])
    return w

def item_similarity_iuf_norm(train):
    """item 归一化相似度算法
    Karypis在研究中发现如果将ItemCF的相似度矩阵按最大值归一化，可以提高推荐的准确度。
    其研究表明，如果已经得到了物品相似度矩阵w，那么可用如下公式得到归一化之后的相似度矩阵w'：
    @param train: {user1: {item1: 1, item2: 1, item3: 1}}
    """
    # calculate co-rated items between users
    c = {}
    n = defaultdict(int)
    for u, items in train.items():
        for i in items:
            n[i] += 1
            for j in items:
                if i == j:
                    continue
                if i not in c:
                    c[i] = defaultdict(int)
                c[i][j] += 1 / math.log(1 + len(items) * 1.0)
    
    # calculate finial similarity matrix W
    w = {}
    #记录每一列的最大值
    w_max = defaultdict(float)
    # 记录每一列的最小值
    w_min = defaultdict(float)
    for i, related_items in c.items():
        for j, cij in related_items.items():
            if j not in w_min:
                # 赋予最大值
                w_min[j] = sys.maxsize
            if i not in w:
                w[i] = defaultdict(float)
            w[i][j] = cij / math.sqrt(n[i] * n[j])
            if w[i][j] > w_max[j]:
                #记录第j列的最大值，按列归一化
                w_max[j] = w[i][j]
            if w[i][j] < w_min[j]:
                w_min[j] = w[i][j]

    for i, related_items in c.items():  
        for j, cij in related_items.items():
            # min-max normalization
            w[i][j]= (w[i][j] - w_min[j]) / (w_max[j] - w_min[j]) 
    return w

def item_recommend(user, train, w, K):
    """物品协同过滤推荐算法.
    @param user: 用户编号
    @param train: {user: {item1: 1, item2: 1, item3: 1}}
    @param w: {user1: {user2: xxx, user3: xxx}, user2: {user1: xxx, user3: xxx}}
    @param K: 推荐商品个数
    """
    # rank = {}
    rank = defaultdict(float)
    # if user not in train:
    #     print(train)
    #     print('遇到了冷数据')
    ru = train[user]

    for i, pi in ru.items():
        for j, wij in sorted(w[i].items(), key=itemgetter(1), reverse=True)[0:K]:
            if j in ru:
                continue
            # if j not in rank:
                # rank[j] = ItemRecommendEntry()
            # rank[j].weight += pi * wij
            # rank[j].reason[i] += pi * wij
            rank[j] += pi * wij
    return rank

def main_test():
    train = {
        'A': {'a': 1, 'b': 1, 'd': 1},
        'B': {'a': 1, 'c': 1},
        'C': {'b': 1, 'e': 1},
        'D': {'c': 1, 'd': 1, 'e': 1}
    }
    w = user_similarity_inverse(train)
    # df = pd.DataFrame.from_dict(w)
    # df = df.fillna(0.0)
    # df.sort_index(inplace=True)
    # print(df)
    # print(w)
    # for u, d in w.items():
    #     print(u, ": ", sep="", end="")
    #     for v, s in d.items():
    #         print("{}={}".format(v, s), end=", ")
    #     print()
    a_rank = user_recommend('A', train, w, 3)
    b_rank = user_recommend('B', train, w, 3)
    print(a_rank)
    print(b_rank)

def main():
    data_set_file = r"E:/datasets/groupLens-movieLens/ml-25m/ratings.csv"
    seed = "fadstgwaretopqewrqwerlkjewr"
    data = read_csv_data(data_set_file)
    # [[user, item], [user, item]]
    train_data, test_data = split_data(data, 8, 0, seed)
    # train_temp = {}
    # test_temp = {}
    # for t in train_data:
    #     if t[0] not in train_temp:
    #         train_temp[t[0]] = defaultdict(int)
    #     train_temp[t[0]][t[1]] = 1
    # TRAIN_DATA = train_temp
    # train_data = train_temp

    # for t in test_data:
    #     if t[0] not in test_temp:
    #         test_temp[t[0]] = defaultdict(int)
    #     test_temp[t[0]][t[1]] = 1
    # test_data = test_temp

    TRAIN_DATA = train_data

    # USER_SIMILARITY_W = user_similarity_inverse(train_data)
    # USER_SIMILARITY_W = user_similarity_iif(train_data)
    
    # for RECOMMEND_K in [5, 10, 20, 40, 60, 80, 100]:
    #     recall_val = recall(train_data, test_data, 5, RECOMMEND_K, USER_SIMILARITY_W)
    #     precision_val = precision(train_data, test_data, 5, RECOMMEND_K, USER_SIMILARITY_W)
    #     coverage_val = coverage(train_data, test_data, 5, RECOMMEND_K, USER_SIMILARITY_W)
    #     polularity_val = polularity(train_data, test_data, 5, RECOMMEND_K, USER_SIMILARITY_W)
    #     print("{}| {} | {} | {} | {}".format(RECOMMEND_K, recall_val, precision_val, coverage_val, polularity_val))
    
    ite_cf_w = item_similarity_iuf_norm(train_data)
    for RECOMMEND_K in [5, 10, 20, 40, 80, 160]:
        recall_val = recall(train_data, test_data, 5, RECOMMEND_K, ite_cf_w)
        precision_val = precision(train_data, test_data, 5, RECOMMEND_K, ite_cf_w)
        coverage_val = coverage(train_data, test_data, 5, RECOMMEND_K, ite_cf_w)
        polularity_val = polularity(train_data, test_data, 5, RECOMMEND_K, ite_cf_w)
        print("{}| {} | {} | {} | {}".format(RECOMMEND_K, recall_val, precision_val, coverage_val, polularity_val))

if __name__ == "__main__":
    main()
    # main_test()