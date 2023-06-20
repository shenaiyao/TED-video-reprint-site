import requests
import json
from lxml import etree
import time

def video_page_crwaler(link:str):
    response=requests.get(url=link,headers=headers)
    #time.sleep(0.5)
    video_page_text=response.text
    in_tree=etree.HTML(video_page_text)
    try:
        script=in_tree.xpath('//*[@id="shoji"]//script[@data-spec="q"]/text()')[0]
    except IndexError:
        response=requests.get(url=link,headers=headers)
        time.sleep(2)
        video_page_text=response.text
        in_tree=etree.HTML(video_page_text)
        script=in_tree.xpath('//*[@id="shoji"]//script[@data-spec="q"]/text()')[0]
    information=json.loads('['+script[2:-1]+']')[1]["__INITIAL_DATA__"]
    #print(information)
    details,speaker_img,speaker_position,speaker_intro,tags,views='','','','','',''
    if "description" in information and information["description"]:
        details=information["description"]

    if "speakers" in information and information["speakers"]:
        speaker=information["speakers"][0]
        speaker_img=speaker["photo_url"]
        speaker_position=speaker["description"]
        speaker_intro=speaker["whotheyare"]
        tags_list=in_tree.xpath('/html/head/meta[@property="og:video:tag"]/@content')
        tags='*'.join(tags_list)
        views=str(information["viewed_count"])

    return details,speaker_img,speaker_position,speaker_intro,tags,views



url_main='https://www.ted.com/talks?page='
url_head='https://www.ted.com'

headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36 Edg/95.0.1020.53'
}

number=0

fp1=open('./basic_information_1.txt','w',encoding='utf-8')
fp1.write('{')
fp1.close()

basic_info={}

#finished 111-148
#finished 74-110
#finished 38-73
#finished
for page in range(1,38):
    print("running page ",page)
    
    url=url_main+str(page)
    page_text=requests.get(url=url,headers=headers).text

    tree=etree.HTML(page_text)
    try:
        div_list=tree.xpath('//div[@id="browse-results"]/div[1]/div[@class="col"]')
    except IndexError:
        response=requests.get(url=url,headers=headers)
        time.sleep(2)
        page_text=response.text
        tree=etree.HTML(page_text)
        div_list=tree.xpath('//div[@id="browse-results"]/div[1]/div[@class="col"]')
    #print(div_list)

    for div in div_list:
        number+=1
        print("now ",number)
        all_contents=div.xpath('.//div[@class="media media--sm-v"]')[0].xpath("./div")   #列表内有两个div
        cover_img_src_lst=all_contents[0].xpath(".//img/@src")
        speaker_name_lst=all_contents[1].xpath("./h4[1]/text()")
        link=url_head+all_contents[1].xpath("./h4[2]/a/@href")[0]
        title=all_contents[1].xpath("./h4[2]/a/text()")[0][1:-1]
        post_time_lst=all_contents[1].xpath('.//span[@class="meta__val"]/text()')[0][1:-1]

        cover_img_src=''
        speaker_name=''
        post_time=''
        if cover_img_src_lst:
            cover_img_src=cover_img_src_lst[0]
            
        if speaker_name_lst:
            speaker_name=speaker_name_lst[0]

        if post_time_lst:
            post_time=post_time_lst[0][1:-1]
       
        # print(cover_img_src)
        # print(speaker)
        #print(link)
        # print(title)
        # print(post_time)
        details,speaker_img,speaker_position,speaker_intro,tags,views=video_page_crwaler(link)
        # print(details)
        # print(speaker_img)
        # print(speaker_position)
        # print(speaker_intro)
        # print(tags)
        #print(views)
        info_list=[link,cover_img_src,post_time,details,tags,views,speaker_name,speaker_img,speaker_position,speaker_intro]
        basic_info[title]=info_list
    
    fp1=open('./basic_information_1.txt','a',encoding='utf-8')
    dic_str=json.dumps(basic_info)[1:-1]+','
    fp1.write(dic_str)
    fp1.close()
    basic_info.clear()

fp1=open('./basic_information_1.txt','a',encoding='utf-8')
fp1.write('"remained_to_be_deleted":0}')
fp1.close()

# fp=open('./basic_info.json','w',encoding='utf-8')
# json.dump(obj=basic_info,fp=fp,ensure_ascii=False)
# fp.close()



print("FINISHED!!!")