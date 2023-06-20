import pymysql
from sys import exit
import json
from elasticsearch import Elasticsearch
es=Elasticsearch()
#检查是否连接成功
#print(es.ping())
try:
    if(not es.ping()):raise Exception("没有连接elasticsearch！")
except Exception as e:
    print("引发异常：",repr(e))
    exit(0)


def data(): #连接数据库，导入数据
    ##输入数据库密码##
    password="MySQL123!"

    conn=pymysql.connect(host='localhost',
                        port=3306,
                        user='root',
                        passwd=password,
                        db="TED",
                        charset='utf8')

    #print(conn.ping())

    cursor=conn.cursor()

    cursor.execute('SELECT * FROM basic_information')
    result=cursor.fetchall() #数据存入列表

    #print(result)
    conn.close()

    return result


my_mappings={
    "properties":{
        "title":{
            "type":"text"
        },
        "link":{
            "type":"text",
            "index":"false"
        },
        "cover_img_src":{
            "type":"text",
            "index":"false"
        },
        "post_time":{
            "properties":{
                "month":{"type":"integer"},
                "year":{"type":"integer"}
            }
        },
        "details":{
            "type":"text"
        },
        "tags":{
            "type":"keyword"
        },
        "views":{
            "type":"long","index":"false"
        },
        "speaker_name":{
            "type":"text"
        },
        "speaker_img_src":{
            "type":"text",
            "index":"false"
        },
        "speaker_position":{
            "type":"text"
        },
        "speaker_intro":{
            "type":"text"
        },
        "duration":{
            "type":"text"
        }
    }
}
my_analyzer={"type": "custom",
         # "char_filter": [],
          "tokenizer": "standard",
          "filter": ["lowercase"]}
my_settings={
    "analysis":{
        "filter":{},
        "char_filter":{},
        "analyzer":{
            "my_analyzer":my_analyzer,
            "search_analyzer":my_analyzer
        }
    }
}


title_list=["title","link","cover_img_src","post_time","details","tags","views","speaker_name","speaker_img_src",
"speaker_position","speaker_intro","duration"]#12
month_list=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
#print(month_list.index("Jan"))



# 插入文档的函数
#print(len(result))
def insert(result):
    for i in range(len(result)):#<=10000 len(result)
        body={}
        for j in range(12):
            if(title_list[j]=="tags"):
                body[title_list[j]]=result[i][j].split('*')
                continue
            if(title_list[j]=="post_time"):
                l=result[i][j].split(" ")
                if(len(l)==2):
                    m=month_list.index(l[0])+1
                    n=int(l[1])
                else:m=n=0#没有发布时间的设置为零
                body[title_list[j]]={"month":m,"year":n}
                continue
            body[title_list[j]]=result[i][j]
        es.index(index="ted", id=i,body=body)


# 创建索引
E=es.indices.exists(index="ted")
if not E: #如果不存在索引，就新建，并导入数据
    res=es.indices.create(index="ted",mappings=my_mappings,settings=my_settings)
    #print(res)
    r=data()#连接数据库，导入数据
    insert(r)
else: #已经存在，无需更新
    #print('index already exsits!') 
    pass


# 删除索引
#es.indices.delete(index="ted")


## json格式化显示函数
def json_print(string):
    print(json.dumps(string, sort_keys=True, indent=4, separators=(',', ':')))
    return

'''
# 查询文档
t=es.get(index="ted", id=0, ignore=404)
json_print(t)
'''


# 搜索部分
search_aim=["title","details","tags","speaker_name",
"speaker_position","speaker_intro"]

#按照观看数量降序排列
view_sort_desc={"views":{"order":"desc"}}
view_sort_asc={"views":{"order":"asc"}}
view_sort=[view_sort_asc,view_sort_desc]

#默认排序为相关性
default_sort={ "_score": { "order": "desc" }}

#按照时间排序
time_sort_desc={"post_time.year":{"order":"desc"},"post_time.month":{"order":"desc"}}
time_sort_asc={"post_time.year":{"order":"asc"},"post_time.month":{"order":"asc"}}
time_sort=[time_sort_asc,time_sort_desc]

def search(keyword:dict,search_range={},search_sort={ "views":0 ,"post_time":0} ):#搜索关键字，搜索域，排序法
    query=[]
    search_aim=[]
    for key in keyword.keys():
        if(keyword[key]!="0"):
            if(key=="tags"):query.append({"terms":{"tags":keyword[key].split(' ')}})
            else:
                query.append({"match":{key:keyword[key]}})
            search_aim.append(key)
    sort=[]
    if(search_sort["views"]!=0):
        sort.append(view_sort[search_sort["views"]-1])
    if(search_sort["post_time"]!=0):
        sort.append(time_sort[search_sort["post_time"]-1])
    sort.append(default_sort)
    #print(sort)
    ymin=0
    ymax=9999
    mmin=0
    mmax=12
    if(search_range.get("year",-1)!=-1):
        ymin,ymax=search_range["year"][0],search_range["year"][1]
        if(search_range.get("month",-1)!=-1):mmin,mmax=search_range["month"][0],search_range["month"][1]
    range=[{"range":{"post_time.year":{"gte":ymin,"lte":ymax}}},{"range":{"post_time.month":{"gte":mmin,"lte":mmax}}}]
    #高亮搜索
    highlight={ 
        "fields":{}
    }
    for item in search_aim:
        highlight["fields"][item]={}
    bquery={"bool":{"must":query,"filter":range}}
    #print(bquery)
    return bquery,sort,highlight


####################################################################


#输入部分

'''
#示例1
keyword={
    "title": "Bird", "details": "universe"
    , "tags": "poetry performance painting"
    , "speaker_name": "sarah"
    ,  "speaker_position": "poet", "speaker_intro": "poet is"
    }
search_sort={ "views":0, "post_time":0}
search_range={}

#示例2
keyword={}
search_sort={ "views":1, "post_time":2}
search_range={"year":[2010, 2010]}

#示例3
keyword={}
search_sort={ "views":0, "post_time":0}
search_range={"year":[2010, 2010],"month":[10,10]}


'''



#########################搜索的外部使用###################################

def outerSearch(keyword,search_range,search_sort):#按照word中的要求输入参数，也可看上方的代码实例
    outcome=[]#输出结果
    total_value_num=0
    total_display_num=0
    for j in range(20):#最多分20页
        query,sort,highlight=search(keyword,search_range,search_sort)
        search_result=es.search(index="ted",query=query,sort=sort,highlight=highlight,size=20,from_=20*j)
        #json_print(search_result)
        hits=search_result["hits"]
        page_out=[]
        i=0
        for hit in hits["hits"]:
            i+=1
            if(hit.get("highlight",-1)!=-1):
                res_o={"_id":hit["_id"], "_score":hit["_score"], "highlight":hit["highlight"]}
            else:res_o={"_id":hit["_id"], "_score":hit["_score"], "highlight":{}}
            #print(hit["_id"],hit["_source"]["views"],hit["_source"]["post_time"],hit["_score"],hit["highlight"])
            for item in title_list:
                res_o[item]=hit["_source"][item]
            page_out.append(res_o)
            #print(res_o)
        #print("total value: ",hits["total"]["value"],i)
        total_value_num=hits["total"]["value"]
        total_display_num+=i
        if(i==0):
            break
        outcome.append(page_out)
    #测试
    '''
    #print(outcome)
    print("页数：",len(outcome)," 每页最大条目数：",20)
    print("结果总数：",total_value_num)
    print("实际显示数：",total_display_num)
    '''
    return outcome,total_value_num,total_display_num




#调用实例#

keyword={}
search_sort={ "views":0, "post_time":0}
search_range={"year":[2000, 2010],"month":[0,12]}

outcome,total_value_num,total_display_num=outerSearch(keyword,search_range,search_sort)

print(outcome)
print("页数：",len(outcome)," 每页最大条目数：",20)
print("结果总数：",total_value_num)
print("实际显示数：",total_display_num)

