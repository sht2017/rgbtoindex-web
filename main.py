from flask import Flask, render_template, request, make_response, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
#from PIL import Image #old
from magapi import * #new
from random import random
import os,base64
app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    global bmpName
    resp=make_response(render_template("index.html"))
    resp.set_cookie('uuid',str(base64.b64encode(str(random()).encode('utf-8'))).split("'")[1])
    if request.method == 'POST':
        file=request.files['file']
        fullname=secure_filename(file.filename)
        originalName=app.root_path.replace("\\","/")+"/tmp/"+\
                fullname.replace("."+fullname.split(".")[-1],"")+"."+\
                request.cookies.get('uuid')[:-2]+\
                "."+fullname.split(".")[-1]
        try:
            os.remove(bmpName)
        except:
            pass
        bmpName=originalName.replace("."+originalName.split(".")[-1],"")+".bmp"
        file.save(originalName)
        #Image.open(originalName).convert('P').save(bmpName) #old
        magick(originalName,bmpName).process()
        if originalName!=bmpName:
            os.remove(originalName)
        return redirect(url_for('download'))
    
    return resp

@app.route("/download", methods=['GET'])
def download():
    resp=make_response(send_from_directory(
        app.root_path.replace("\\","/")+"/tmp/",
        bmpName.split("/")[-1]
    ))
    resp.headers["Content-Disposition"]="attachment; filename="+bmpName.split("/")[-1]+";"
    return resp


if __name__ == '__main__':
    app.debug = False
    app.run(host='0.0.0.0',port=80)