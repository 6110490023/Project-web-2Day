from fileinput import filename
from multiprocessing import Value
from pydoc import describe
from tabnanny import check
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
import pyrebase
import datetime, pytz

Config = {
  "apiKey": "AIzaSyBKxDnby4-WmWtH1dXhBgOvR_E7BT6eBj0",
  "authDomain": "project-web-systemfile.firebaseapp.com",
  "databaseURL": "https://project-web-systemfile-default-rtdb.firebaseio.com",
  "projectId": "project-web-systemfile",
  "storageBucket": "project-web-systemfile.appspot.com",
  "messagingSenderId": "882562644579",
  "appId": "1:882562644579:web:dc7e0d31bc6e5f5b4b1656"
}
firebase = pyrebase.initialize_app(Config)
authe = firebase.auth()
database = firebase.database()
storage = firebase.storage()

def get_course_info(course_name):
    courseInfo = database.child("CourseAll").order_by_child("coursename").equal_to(course_name).get().val()
    course = {}
    course["key"] = list(dict(courseInfo).keys())[0]
    course["data"] = list(dict(courseInfo).values())
    return course

def get_folder(course ,folder_name):
    folderAll = course["folderAll"]
    folder = list(filter(lambda folder: folder["folder_name"] == folder_name, folderAll))
    folder["all_file"] = folder
    folder["index"] = -1
    return folder

def get_file(course, folder_name, file_name):
    folder = get_folder(course, folder_name)
    allfile = []
    if "fileAll" in folder:
        allfile = folder["fileAll"]
    return allfile
    