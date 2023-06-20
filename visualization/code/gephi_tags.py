from flask import Flask,request,render_template
app = Flask(__name__)

@app.route('/',methods=['GET'])
def gephi():
    return render_template('gephi_tags.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)