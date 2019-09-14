from flask import Flask, redirect, url_for, render_template
import os
import sys
import glob
import subprocess

app = Flask(__name__)

# Methods
def get_directories():
    return [dir for dir in os.listdir('/tmp/soundlib') if os.path.isdir(os.path.join('/tmp/soundlib', dir))]

def get_files(dir):
    return os.listdir(dir)

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/controllers/<controller>')
def set_controller(controller):
    if controller=="webbrowser":
        elements=list(get_directories())
        return render_template('list.html', subdir='/directories/', elements=elements)
    else:
        return controller

@app.route('/files/<file>')
def handle_file(file):
    return file

@app.route('/directories/<dir>')
def print_directory(dir):
    files=get_files('/tmp/soundlib/{0}'.format(dir))
    return render_template('list.html', subdir='/files/', elements=files)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
