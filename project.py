from flask import Flask, render_template, flash, request, session,send_file
from flask import render_template, redirect, url_for, request
#from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from werkzeug.utils import secure_filename
import datetime
import mysql.connector
import sys
import tensorflow as tf
import numpy as np

from tkinter import *
import os
from tkinter import filedialog
import cv2
import time
from matplotlib import pyplot as plt
from tkinter import messagebox
app = Flask(__name__)
app.config['DEBUG']
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

@app.route("/")
def homepage():

    return render_template('index.html')

@app.route("/AdminLogin")
def AdminLogin():

    return render_template('AdminLogin.html')
@app.route("/tdataset")
def tdataset():

    return render_template('tdataset.html')
@app.route("/train")
def train():
    import ResNet

    return "Train SuccessFull"
@app.route("/AdminHome")
def AdminHome():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1leafdb')
    cursor = conn.cursor()
    cursor.execute("SELECT * from regtb")
    data = cursor.fetchall()


    return render_template('AdminHome.html',data=data)
@app.route("/adminlogin", methods=['GET', 'POST'])
def adminlogin():

    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['password']
        session['uname'] = request.form['uname']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1leafdb')
        cursor = conn.cursor()
        cursor.execute("SELECT * from admin where username='" + username + "' and Password='" + password + "'")
        data = cursor.fetchone()
        if data is None:

            alert = 'Username or Password is wrong'
            return render_template('goback.html', data=alert)



        else:
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1leafdb')
            cursor = conn.cursor()
            cursor.execute("SELECT * from regtb")
            data = cursor.fetchall()

            return render_template('AdminHome.html',data=data)



@app.route("/UserLogin")
def UserLogin():
    return render_template('UserLogin.html')

@app.route("/NewUser")
def NewUser():
    return render_template('NewUser.html')



@app.route("/UserHome")
def UserHome():
    user = session['uname']

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1leafdb')
    # cursor = conn.cursor()
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb where username='" + user + "'")
    data = cur.fetchall()
    return render_template('UserHome.html',data=data)


@app.route("/userlogin", methods=['GET', 'POST'])
def userlogin():

    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['password']
        session['uname'] = request.form['uname']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1leafdb')
        cursor = conn.cursor()
        cursor.execute("SELECT * from regtb where username='" + username + "' and Password='" + password + "'")
        data = cursor.fetchone()
        if data is None:

            alert = 'Username or Password is wrong'
            return render_template('goback.html', data=alert)



        else:

            return render_template('UserHome.html')

@app.route("/newuser", methods=['GET', 'POST'])
def newuser():
    if request.method == 'POST':

        name1 = request.form['name']
        gender1 = request.form['gender']
        Age = request.form['age']
        email = request.form['email']
        pnumber = request.form['phone']
        address = request.form['address']

        uname = request.form['uname']
        password = request.form['psw']


        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1leafdb')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO regtb VALUES ('" + name1 + "','" + gender1 + "','" + Age + "','" + email + "','" + pnumber + "','" + address + "','" + uname + "','" + password + "')")
        conn.commit()
        conn.close()
        # return 'file register successfully'


    return render_template('UserLogin.html')

@app.route("/result", methods=['GET', 'POST'])
def result():

    if request.method == 'POST':

        f = request.files['file']
        txt =f.filename

        x1 = txt.split("_")

        f.filename = "test.jpg"
        #f.save(secure_filename(f.filename))
        f.save("static/upload/" + secure_filename(f.filename))
        filename = 'Output/Out/Test.jpg'
        f.save("static/"+secure_filename(f.filename))



        from tensorflow.keras.layers import Input, Lambda, Dense, Flatten
        from tensorflow.keras.models import Model
        from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
        from tensorflow.keras.preprocessing import image
        from tensorflow.keras.preprocessing.image import ImageDataGenerator, load_img
        from tensorflow.keras.models import Sequential
        import scipy
        import numpy as np
        from glob import glob
        import matplotlib.pyplot as plt
        # Paths
        train_Path = 'train'
        test_Path = 'test'
        # Set Resize variable
        IMAGE_SIZE = [224, 224]  # This is my desired image size... and also ResNet50 accepts image of 224*224.
        from tensorflow.keras.models import load_model
        model = load_model('model.h5')
        model.summary()

        img = image.load_img('static/upload/test.jpg', target_size=IMAGE_SIZE)
        x = image.img_to_array(img)
        print(x)
        print(x.shape)
        x = x / 255
        x = np.expand_dims(x, axis=0)
        img_data = preprocess_input(x)
        x.shape, img_data.shape
        s = model.predict(img_data)
        # pred = np.argmax(model.predict(input_arr_img))

        print(s)
        a = np.argmax(model.predict(img_data), axis=1)
        print(a)
        classes_dir = ["Fake", "Real"]
        # Loading Image
        # img = image.load_img(path,target_size=(224, 224))
        # Normalizing Image
        norm_img = image.img_to_array(img) / 255
        # Converting Image to Numpy Array
        input_arr_img = np.array([norm_img])
        # Getting Predictions
        pred = np.argmax(model.predict(input_arr_img))
        # Printing Model Prediction
        print(classes_dir[pred])

        return render_template('result.html', data1=classes_dir[pred],data=str(x1[0]))

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
