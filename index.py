
import sys
import logging
import os
import string
import random
import cv2
from os.path import join, dirname, realpath


import argparse

import numpy as np
from flask import *
from werkzeug.utils import secure_filename

app = Flask(__name__,static_url_path = "/static", static_folder = "static")
UPLOAD_FOLDER = '/static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'gif','jpeg'])
app.config['SECRET_KEY'] = os.urandom(24)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def processimage(input,output,cutnum):
    img = cv2.imread(input)

    print(img.shape)

    height, width, c = img.shape

    width = width - (width % cutnum)
    height = height - (height % cutnum)
    imageArray = np.zeros((height, width, 3), np.uint8)
    px = 0

    htmp = 0
    wtmp = 0
    for h in range(0, height):
        if h % cutnum == 0 and htmp + cutnum < height:
            htmp += cutnum

        wtmp = 0
        for w in range(0, width):
            if w % cutnum == 0 and wtmp + cutnum < width:
                wtmp += cutnum
            px = img[htmp,wtmp]


            b = px[0]
            g = px[1]
            r = px[2]

            imageArray[h, w] = [b, g,r]

    cv2.imwrite(output, imageArray)

def random_str(n):
    return ''.join([random.choice(string.ascii_letters + string.digits) for i in range(n)])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/show/<filename>')
def uploaded_file(filename):
    filename = 'http://127.0.0.1:8000/uploads/' + filename
    return render_template('index.html', filename=filename)

@app.route('/uploads/<filename>')
def send_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/')
def index():
    return render_template('index.html')



@app.route('/send', methods=['GET', 'POST'])
def send():
    if request.method == 'POST':
        img_file = request.files['img_file']
        if img_file:
            
            filename = secure_filename(img_file.filename)
              
            
            DIR = os.path.abspath(os.path.dirname(__file__)) + app.config['UPLOAD_FOLDER'] 
            filelen = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
            imgfilename =  str(filelen)+'A'+secure_filename(img_file.filename)
            resultfilename =  str(filelen)+'B'+secure_filename(img_file.filename)
        
            savedir = os.path.abspath(os.path.dirname(__file__)) + app.config['UPLOAD_FOLDER']+ imgfilename
            resultdir = os.path.abspath(os.path.dirname(__file__)) + app.config['UPLOAD_FOLDER']+ resultfilename
          
            
            print(savedir,sys.stdout)

            file_name=savedir
            cutindex = int(request.form['selected'])

            img_file.save(savedir)
            processimage(savedir,resultdir,cutindex)
            
           
            
            return render_template('index.html', before="Before:",beforefilename=imgfilename,after="After:",afterfilename=resultfilename)
        else:
            return ''' <p>画像ではありません</p> '''
    else:
        return redirect(url_for('index'))







if __name__ == "__main__":


  app.run(port=8000, debug=True,threaded=True)
















