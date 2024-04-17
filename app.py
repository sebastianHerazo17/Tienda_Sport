from flask import Flask, render_template, request, redirect, url_for
from src.controllers import controller
from src.models.model import *



app = Flask(__name__)
app.config['SECRET_KEY']='security key momently'




@app.route('/')
def inicio():
    return controller.login()

@app.route('/login', methods=['GET', 'POST'])
def login():
    return controller.login()

@app.route('/index')
def index():
    return controller.index()

@app.route('/productos')
def productos():
    return controller.productos()

if __name__ == '__main__':
    app.run(debug=True)
