import pymysql
from werkzeug.utils import redirect
import search_ydn_v3 as sv3
from flask import Flask, render_template, request, url_for

conn=pymysql.connect(host='localhost',
                    port=3306,
                    user='root',
                    passwd='MySQL123!',
                    db='TED',
                    charset='utf8')
cursor=conn.cursor()





from flask import Flask, request, render_template
app = Flask(__name__)

@app.route('/results', methods=['GET'])
def index():
    keyword={}
    if request.args.get("title"):
        keyword.update({"title":request.args.get("title")})

    if request.args.get("details"):
        keyword.update({"details": request.args.get("details")})

    if request.args.get("tag"):
        keyword.update({"tags":request.args.get("tag")})

    if request.args.get("names"):
        keyword.update({"speaker_name": request.args.get("names")})

    if request.args.get("major"):
        keyword.update({"speaker_position":request.args.get("major")})





    print(keyword)
    '''
    "details": request.args.get("details"),
    "tags": request.args.get("tag"),
    "speaker_name": request.args.get("names"),
    "speaker_position": request.args.get("major"), 
    "speaker_intro": request.args.get("introduction")
    '''
    
    
    outcome,total_value_num,total_display_num = sv3.outerSearch(keyword,{"year":[2000, 2021],"month":[1,12]},{ "views":0, "post_time":0})
    ans=[]
     
    
    currentpage=int(request.args.get('currentpage',1))-1
    
    if(outcome):

        pages=[]
        page=len(outcome)
        for i in range(page):
            pages.append(i+1)

        for k in outcome[currentpage]:
            vedio = []
            vedio.append(k['title'])
            vedio.append(k['link'])
            vedio.append(k['cover_img_src'])
            vedio.append(k['details'])
            vedio.append('*'.join(k['tags']))
            vedio.append(k['views'])
            vedio.append(k['speaker_name'])
            vedio.append(k['speaker_img_src'])
            vedio.append(k['speaker_position'])
            vedio.append(k['speaker_intro'])
            vedio.append(k['duration'])
            vedio.append(str(k['post_time']['month'])+'-'+str(k['post_time']['year']))
            ans.append(vedio)
    print(ans)

    return render_template('result4.html',Vedios=ans,pages=pages)

@app.route("/search")
def search():
    if request.method == 'POST':
        title = request.form['title']
        tag = request.form['tag']
        names = request.form['names']
        major = request.form['major']
        introduction= request.form['introduction']
        details = request.form['details']
        return redirect(url_for('/results',
        title= title, 
        details= details,
        tags= tag,
        speaker_name= names,
        speaker_position= major, 
        speaker_intro= introduction))
    return render_template("search.html")

@app.route("/")
def frontpage():
    return render_template("frontpage1.html")

@app.route("/rank/")
def rank():
    return render_template("rank.html")

@app.route("/more")
def more():
    return render_template("more.html")

@app.route("/echarts_tags")
def echarts_tags():
    return render_template("echarts_tags.html")

@app.route("/echarts_views")
def echarts_views():
    return render_template("echarts_views.html")

@app.route("/gephi_tags")
def gephi_tags():
    return render_template("gephi_tags.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)





#页面背景图片由于宽度是由百分比定义，会随页面变动，而其他元素是由像素定位，不会随页面变动。
#<img src="https://tedxsydney.com/wp-content/uploads/2018/03/about-tedx-sydney-ted-talks-events-in-sydney.jpg" width="100%" alt="">
#<img src="C:\Users\geyuan\Desktop\demo\images\ted.jpg" width="100%" alt="">