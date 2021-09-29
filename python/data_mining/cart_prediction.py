#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-05-26 09:49:15
# @Author  : wuyan (msn734506700@live)
# @Version : V0.1
# @description: 数据挖掘算法
# 决策树-cart算法，预测波士顿房价

import graphviz
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, mean_squared_error, mean_absolute_error
from sklearn.tree import DecisionTreeClassifier, export_graphviz, DecisionTreeRegressor
from sklearn.datasets import load_iris, load_boston

# 准备数据集
boston = load_boston()

# 探索数据
print(boston.feature_names)

# 获取特征集和房价
features = boston.data
prices = boston.target

# 随机抽取33%的数据作为测试集，其余为训练集
train_features, test_features, train_price, test_price = train_test_split(features, prices, test_size=0.33)

# 创建cart回归树
dtr = DecisionTreeRegressor()
# 拟合构造cart回归树
dtr.fit(train_features, train_price)
# 预测测试集中的房价
predict_price = dtr.predict(test_features)
# 测试集的结果评价
print('回归树的二乘偏差均值: ', mean_squared_error(test_price, predict_price))
print('回归树的绝对值偏差均值: ', mean_absolute_error(test_price, predict_price))

# 参数是回归树模型名称，不输出文件。
dot_data = export_graphviz(dtr, out_file=None)
graph = graphviz.Source(dot_data)
# render 方法会在同级目录下生成 Boston PDF文件，内容就是回归树。
graph.render('cart-Boston')

