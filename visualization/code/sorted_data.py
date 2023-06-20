from flask import Flask, request, render_template
app = Flask(__name__)

import pymysql
conn = pymysql.connect(host='localhost',
                       port=3306,
                       user='root',
                       passwd='say410822',
                       charset='utf8',
                       database='ted')
cursor = conn.cursor()

views = []
title = []
tags = []

# views_information is a database which saves 5326 videos' titles and views and sorted by descending order of views
# views is a list which saves all views
cursor.execute('SELECT views FROM views_information')
for i in range(5326):
    item = cursor.fetchone()[0]
    if item>='0':
        views.append(int(item))
    else:
        views.append(0)

# print top 10 views of 5326 videos

# print("views")
# for i in range(10):
#     print(views[i],end="")
#     print(",")

# title is a list which saves all titles

cursor.execute('SELECT title FROM views_information')
for i in range(5326):
    title.append(cursor.fetchone()[0])

# print the top 10 titles

# print("title")
# for i in range(10):
#     # print(title[i])
#     print("\"{}\",".format(title[i]))

# basic_information is a database which saves all the information of videos

cursor.execute('SELECT tags FROM basic_information')

# tags is a list which saves every video's tags, is a nested list
for i in range(5326):
    item = list(cursor.fetchone()[0].split("*"))
    tags.append(item)

# print videos' tags, sliced by video

# print("tags")
# for i in range(100):
#     print(i)
#     for item in tags[i]:
#         print(item)


# dt is a dict that saves all the tags and its reference time
# ndt is a list whose elements are tuple and saves the tags and its reference time, sorted by reference time
length = 0
dt = {}
for i in range(5326):
    # print(i)
    for item in tags[i]:
        if item in dt:
            dt[item]+=1
        else:
            dt[item]=1
            length+=1
ndt = sorted(dt.items(),key=lambda kv:kv[1],reverse=True)
# print(length)
# print(dt)
# print(ndt)   
# ndt生成了nodes.xlxs，按照引用量的降序排列编id，引用量最多的tag的id是0

# nodes is a dict that saves tags' name as keys and id as values, nodes的顺序和nodes.xlxs的顺序完全相同
nodes = {}
for i in range(348):
    nodes[ndt[i][0]]=i
# print(nodes)   


# edge is a class that haves source, target, weight
class Edge:
    def __init__(self,source=0,target=0,weight=0):
        self.source,self.target,self.weight = source,target,weight
    def set_weight(self):
        self.weight+=1


edges = []
for i in range(5326):
    max = 0
    for item in tags[i]:
        if nodes[item]>max:
            max = nodes[item]
            # print(item)
    L = len(edges)

    j = 0
    while j<L and edges[j].source!=max:
        j+=1

    if j==L:
        for item in tags[i]:
            if nodes[item]!=max:
                edge = Edge(max,nodes[item],1)
                edges.append(edge)
    else:
        k = j
        while k<L and edges[k].source==max:
            k+=1

        for item in tags[i]:
            if nodes[item]!=max:
                flag = False
                for m in range(j,k):
                    if edges[m].target==nodes[item]:
                        edges[m].set_weight()
                        flag = True
                        break
                if flag==False:
                    edge = Edge(max,nodes[item],1)
                    edges.insert(k,edge)

# 生成source，target，weight序列
S = []
T = []
W = []
for item in edges:
    S.append(item.source)
    T.append(item.target)
    W.append(item.weight)
# print(len(S))
# print(S)
# print(T)
# print(W)

# print edges information

# for i in range(10000,13520):
#     if W[i]<4:
#         pass
#     else:
#         print("{",end="")
#         print("\"sourceID\": {}, \"targetID\": {}, \"weight\": {}".format(S[i],T[i],W[i]),end="")
#         print("},")


# print nodes information

# import numpy as np
# datanumber = 348
# np.random.seed(28041990)
# x = np.random.normal(0, 1000000, size=datanumber)
# y = np.random.normal(0, 1000000, size=datanumber)
# colorList = [
#                                             "#c23531",
#                                             "#2f4554",
#                                             "#61a0a8",
#                                             "#d48265",
#                                             "#91c7ae",
#                                             "#749f83",
#                                             "#ca8622",
#                                             "#bda29a",
#                                             "#6e7074",
#                                             "#546570",
#                                             "#c4ccd3",
#                                             "#4BABDE",
#                                             "#FFDE76",
#                                             "#E43C59",
#                                             "#37A2DA"
#                                         ]
# for i in range(348):
#     print("{",end="")
#     print("\"x\":{},\"y\":{},\"id\":{},\"name\":\"{}\",\"symbolSize\":{},\"itemstyle\":".format(x[i],y[i],i,ndt[i][0],ndt[i][1]/15),end="")
#     print("{",end="")
#     print("\"color\":",end="")
#     print("\"{}\"".format(colorList[i%15]),end="")
#     print("}",end="")
#     print("},")


# 将source，target，weight序列写入data.xls中

# from xlwt import *
# workbook = Workbook(encoding='utf-8')  #写入excel文件
# sheet = workbook.add_sheet('Sheet1',cell_overwrite_ok=True)  #新增一个sheet工作表
# headlist=[u'Source',u'Target',u'Weight']   #写入数据头
  
# row = 0
# col = 0
# for head in headlist:
#     sheet.write(row,col,head)
#     col += 1
# for i in range(1,13520):
#     sheet.write(i,0,S[i-1])
#     sheet.write(i,1,T[i-1])
#     sheet.write(i,2,W[i-1])

# workbook.save('data.xls')