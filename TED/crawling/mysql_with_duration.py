import pymysql
import json
with open('./basic_information.txt','r',encoding='utf-8') as fp:
    info=json.load(fp)
print(type(info),len(info))
with open('./dur1.txt','r',encoding='utf-8') as fp:
    durs=json.load(fp)
print(type(durs),len(durs))
for title in durs:
    if title not in info:
        durs[title]=0
for title in info:
    if title not in durs:
        info[title]=0

print(len(info),len(durs))




def set_database(password:str):
    conn=pymysql.connect(host='localhost',
                     port=3306,
                     user='root',
                     passwd=password,
                     charset='utf8')
    cursor=conn.cursor()

    cursor.execute("drop database if exists TED")
    conn.commit()

    cursor.execute('create database if not exists TED character set UTF8mb4 collate \
    utf8mb4_general_ci')
    conn.commit()

    cursor.close()
    conn.close()

    conn=pymysql.connect(host='localhost',
                     port=3306,
                     user='root',
                     passwd=password,
                     db='TED',
                     charset='utf8')
    cursor=conn.cursor()
    
    cursor.execute('CREATE TABLE `Basic_information`(\
        `title` VARCHAR(100) NOT NULL,\
        `link` TEXT NOT NULL,\
        `cover_img_src` TEXT NULL,\
        `post_time` VARCHAR(100) NULL,\
        `details` TEXT NULL,\
        `tags` TEXT NULL,\
        `views` VARCHAR(100) NULL,\
        `speaker_name` VARCHAR(100) NULL,\
        `speaker_img_src` TEXT NULL,\
        `speaker_position` TEXT NULL,\
        `speaker_intro` TEXT NULL,\
        `duration` TEXT NULL,\
        PRIMARY KEY(`title`),\
        INDEX `title` USING BTREE (`title`))\
        ENGINE=InnoDB,\
        DEFAULT CHARACTER SET =utf8mb4'
    )
    conn.commit()

    cursor.close()
    conn.close()

def write_in(password:str,info:dict):
    

    conn=pymysql.connect(host='localhost',
                     port=3306,
                     user='root',
                     passwd=password,
                     db='TED',
                     charset='utf8')
    cursor=conn.cursor()

    

    #写入数据
    insert_cmd="INSERT INTO Basic_information (title,link,cover_img_src,post_time,details,tags,views,speaker_name,speaker_img_src,speaker_position,speaker_intro,duration) \
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    for title in info:
        if info[title]==0 or durs[title]==0:
            continue
        lis=[title]+info[title]+[durs[title]]
        tp=tuple(lis)
        cursor.execute(insert_cmd,tp)
        conn.commit()
        # print(kv)
        # exit(0)
    cursor.close()
    conn.close()

password=input("输入密码：")
set_database(password)
write_in(password,info)
print("FINISHED")