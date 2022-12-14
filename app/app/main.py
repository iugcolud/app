from http import client
from imp import new_module
from pickle import APPEND
from flask import render_template, request 
from app import webapp, memcache
from flask import json
import pymysql



conn = pymysql.connect(host='localhost', user='root', password='', db='cloude_dp')
cur = conn.cursor()
UPLOAD_FOLDER = 'app/static/img'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


webapp.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@webapp.route('/')
def main():
    return render_template("index.html")


def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData


def put():
    key = request.form.get('key')
    value = request.form.get('value')
    memcache[key] = value
    response = webapp.response_class(
        response=json.dumps("OK"),
        status=200,
        mimetype='application/json'
    )
    return response



@webapp.route("/upload", methods = ['GET','POST'])
def addimg():
    conn = pymysql.connect(host='localhost', user='root', password='', db='cloude_dp')
    cur = conn.cursor()
    if request.method == 'GET':
        return render_template("page2.html")
    if request.method == 'POST':
        keyy = request.form["keyy"]
        file = request.files['image']
        file_name = file.filename or ''
        destination = '/'.join([UPLOAD_FOLDER, file_name])
        file.save(destination)
        convertToBinaryData(file.filename)
        cur.execute("INSERT INTO img (keyy,image) VALUES (%s, %s)", [keyy,file])
        
        # print(memcache.setdefault(keyy, file [, 3]))
        print(put())
        print(memcache.get(keyy))
        # time.sleep(300)
        # memcache.pop(keyy)
        # print("memcach after 3 s " )
        # print(memcache.get(keyy))
        conn.commit()
        cur.close()
        return render_template('index.html')
    else:
        return render_template('index.html')
        

# @webapp.route('/get',methods=['POST'])
# def get():
#     key = request.form.get('key')

#     if key in memcache:
#         value = memcache[key]
#         response = webapp.response_class(
#             response=json.dumps(value),
#             status=200,
#             mimetype='application/json'
#         )
#     else:
#         response = webapp.response_class(
#             response=json.dumps("Unknown key"),
#             status=400,
#             mimetype='application/json'
#         )

#     return response




