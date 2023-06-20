import requests
import json
from lxml import etree
import time




url_main='https://www.ted.com/talks?page='
url_head='https://www.ted.com'

headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36 Edg/95.0.1020.53'
}

number=0

fp1=open('./dur0.txt','w',encoding='utf-8')
fp1.write('{')
fp1.close()

dur_info={}

#finished 2-149
#finished 
#finished 
#finished
for page in range(1,2):
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

    for div in div_list[19:]:
        number+=1
        print("now ",number)
        all_contents=div.xpath('.//div[@class="media media--sm-v"]')[0].xpath("./div")   #列表内有两个div
        title=all_contents[1].xpath("./h4[2]/a/text()")[0][1:-1]
        dur_lst=all_contents[0].xpath('.//span[@class="thumb__duration"]/text()')
        dur=''
        if dur_lst:
            dur=dur_lst[0][1:]
        
        dur_info[title]=dur
    # print(dur_info)
    # exit(0)

    fp1=open('./dur0.txt','a',encoding='utf-8')
    dic_str=json.dumps(dur_info)[1:-1]+','
    fp1.write(dic_str)
    fp1.close()
    dur_info.clear()

fp1=open('./dur0.txt','a',encoding='utf-8')
fp1.write('"remained_to_be_deleted":0}')
fp1.close()
print("FINISHED!!!")
        