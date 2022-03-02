from email.mime import image
from django.shortcuts import render,redirect
from django.contrib import messages
import pyrebase
import datetime, pytz
from .static.py import firebase_course
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
#หน้าhome
def Home(request):
     if 'uid' in request.session and request.session != '' :
          user = database.child('TeacherAll').child(request.session['uid']).get().val()
          courseAll = database.child('CourseAll').get().val()
          if courseAll  != None:
               courseAll = dict(courseAll)
          else:
               courseAll = {}
          myCourse = []
          if user != None:
               request.session['status'] = "teacher"
               for course in courseAll:
                    if 'teacherId' in courseAll[course] and courseAll[course]['teacherId'] == request.session['uid']:
                         courseCurrent = courseAll[course]
                         courseCurrent["count"]= 0
                         if 'studentList' in courseCurrent:
                              courseCurrent["count"]= len(courseCurrent['studentList'])
                         myCourse.append(courseAll[course]) 
                          
               return render(request,'Home/teacher.html',{'my_course': myCourse })
          else:
               user = database.child('StudentAll').child(request.session['uid']).get().val()
               if user != None:
                    request.session['status'] = "student"
                    my_courseKey =[]
                    if "courseList" in dict(user):
                         my_courseKey =  dict(user)["courseList"]
                    my_course =[]
                    for courseId in my_courseKey:
                         course = database.child('CourseAll').child(courseId).get().val()
                         my_course.append(dict(course))
                    return render(request,'Home/student.html',{'my_course': my_course })
               else:
                    messages.info(request,'Username ไม่ถูกต้อง')
                    return redirect('/logout')
     else:
          return redirect('/loginPage')
#ไปหน้า login
def loginPage(request):
     return render(request,'login.html')
#ไปหน้า register
def register(request):
     return render(request,'register.html')

#ส่งคำข้อlogin
def login(request):
     email=request.POST['email']
     password=request.POST['Password']

     #check username ,password
     try:
        # if there is no error then signin the user with given email and password
        user =authe.sign_in_with_email_and_password(email,password)
     except:
        messages.info(request,'ไม่พบข้อมูล ')
        return redirect('/loginPage')
     session_id= user['idToken']
     uid = user['localId']
     request.session['idToken']= str(session_id)
     request.session['uid']= str(uid)
     
     return redirect('/')
          
def createUser(request):
     firstname=request.POST['Firstname']
     lastname=request.POST['Lastname']
     email=request.POST['Email']
     password=request.POST['Password']
     repassword=request.POST['RePassword']
     status = request.POST['status']
     sex = request.POST['sex']
     phone = request.POST['phone']
     image_profile = request.FILES['material']
     if password==repassword :
          try:
               # creating a user with the given email and password
               user=authe.create_user_with_email_and_password(email,password) 
               uid = user['localId']
               file = image_profile.name.split(".")[1]
               cloud = storage.child("profile/" + uid + "/profile_"+ uid + "."+ file).put(image_profile)
          except:
               messages.info(request,'Email นี้เคยลงทะเบียนแล้ว')
               return redirect('/register')
          
          if status == 'student' :
               numberclass = request.POST['class']
               room = request.POST['room']
               no = request.POST['number']
               
               data = {"email":email,
                       "name": firstname,
                       "lastname":lastname ,
                       "sex":sex,
                       "room":room,
                       'class':numberclass,
                       "no":no,
                       'phone':phone,
                       "image": storage.child("profile/" + uid + "/profile_"+ uid + "."+ file).get_url(cloud["downloadTokens"])
                       }
               database.child("StudentAll").child(str(uid)).set(data)
          
          elif status == 'teacher' :
               subject = request.POST['subject']
               file = image_profile.name.split(".")[1]
               cloud = storage.child("profile/" + uid + "/profile_"+ uid + "."+ file).put(image_profile)
               data = {"email":email,
                       "name": firstname,
                       "lastname":lastname ,
                       "sex":sex,
                       "subject":subject,
                       'phone':phone,
                       "image": storage.child("profile/" + uid + "/profile_"+ uid + "."+ file).get_url(cloud["downloadTokens"])
                       }
               database.child("TeacherAll").child(str(uid)).set(data)
          return redirect('/loginPage')
     
     else :
          messages.info(request,'รหัสผ่านไม่ตรงกัน')
          return redirect('/register')



def logout(request):
     try:
        del request.session['uid']
        del request.session['idToken']
        del request.session['status']
        request.session.clear()
     except:
        pass
     return redirect('/loginPage')


def course(request,name):
     if 'uid' in request.session and request.session != '':
          courseInfo = database.child("CourseAll").order_by_child("coursename").equal_to(name).get().val()
          course = list(dict(courseInfo).values())
          if course :
               course = course[0]
               
               if "folderAll" not in course:
                    course['folderAll'] = []
               if request.session['status'] == 'teacher' and request.session['uid']== course['teacherId']:
                    return  render(request,'Home/course.html',{'folder_All':course['folderAll'], 'coursename': name} )
               if request.session['status'] == 'student' and 'studentList' in course  and request.session['uid'] in course['studentList']:
                    return  render(request,'Home/course.html',{'folder_All':course['folderAll'], 'coursename': name})
               else:
                    return redirect('/error')
     else:
          return redirect('/loginPage')


def profile(request):
     if 'uid' in request.session and request.session != '':
          if request.session['status'] == 'teacher':
               profileInfo = database.child("TeacherAll").child(request.session['uid']).get().val()
          elif request.session['status'] == 'student':
               profileInfo = database.child("StudentAll").child(request.session['uid']).get().val()
          else:
               return redirect('/error')
          print(dict(profileInfo))
          return  render(request,'Home/profile.html',{'user': dict(profileInfo)})
     else:
          return redirect('/loginPage')

def editProfile(request):
     if 'uid' in request.session and request.session != '':
          firstname=request.POST['Firstname']
          lastname=request.POST['Lastname']
          password=request.POST['Password']
          status = request.session['status']
          phone = request.POST['phone']
          uid = request.session['uid']
          if status == "student":
               x = "StudentAll"
          elif status == "teacher":
               x = "TeacherAll"
          userInfo = database.child(x).child(uid).get().val()
          userInfo = dict(userInfo)
          try:
          # if there is no error then signin the user with given email and password
               user =authe.sign_in_with_email_and_password(userInfo['email'],password)
          except:
               messages.info(request,'รหัสผ่านไม่ถูกต้อง')
               return redirect('/editprofilepage')

          if status == 'student' :
               numberclass = request.POST['class']
               room = request.POST['room']
               no = request.POST['number']
                    
               userInfo["name"] = firstname
               userInfo["lastname"]=lastname
               userInfo["room"]=room
               userInfo["class"]=numberclass
               userInfo["no"]= no
               userInfo["phone"]=phone
               database.child("StudentAll").update({str(uid): userInfo})
          
          elif status == 'teacher' :
               subject = request.POST['subject']
               userInfo["name"] = firstname
               userInfo["lastname"]=lastname
               userInfo["subject"]=subject
               userInfo["phone"]=phone
               database.child("TeacherAll").update({str(uid): userInfo})
          return redirect('/profile')
     
     else :
          return redirect('/loginPage')

def editProfilePage(request):
     if 'uid' in request.session and request.session != '':
          if request.session['status'] == 'teacher':
               profileInfo = database.child("TeacherAll").child(request.session['uid']).get().val()
          elif request.session['status'] == 'student':
               profileInfo = database.child("StudentAll").child(request.session['uid']).get().val()
          else:
               return redirect('/error')
          return  render(request,'Home/editprofile.html', {'user': dict(profileInfo)})
     else:
          return redirect('/loginPage')

def addStudentPage(request,name):
     if 'uid' in request.session and request.session != '' :
          studentList =[]
          if request.method == "POST":
               request.session['class_room'] = request.POST['class_room']
          
          if 'class_room' in request.session:
               classnumber,room = str(request.session['class_room']).split('-')
               courseInfo = database.child("CourseAll").order_by_child("coursename").equal_to(name).get().val()
               courseInfo = dict(courseInfo)
               valusecourse= list(courseInfo.values())[0]
               studentInCourse= []
               if 'studentList' in valusecourse:
                    studentInCourse = valusecourse['studentList']
               studentDit = dict(database.child("StudentAll").order_by_child("room").equal_to(room).get().val())
               studentList =[]
               for sid in studentDit:
                    if studentDit[sid]['class'] == classnumber:
                         studentDit[sid]['sid']= sid
                         studentDit[sid]['is_incourse'] = (sid in studentInCourse)
                         studentList.append(studentDit[sid])
          return  render(request,'Home/addstudent.html',{"name":name,"studentList":studentList})
          
     else:
          return redirect('/loginPage')

def addStudent(request,namecourse):
     if 'uid' in request.session and request.session != '' :
          if request.method == "POST":
               sid = request.POST['sid']
               courseInfo = database.child("CourseAll").order_by_child("coursename").equal_to(namecourse).get().val()
               courseInfo = dict(courseInfo)
               keycourse = list(courseInfo.keys())[0]
               valusecourse= list(courseInfo.values())[0]
               studentInCourse = []
               if 'studentList' in valusecourse:
                    studentInCourse = valusecourse['studentList']
               if sid not in studentInCourse:
                    studentInCourse.append(sid)
               database.child("CourseAll").child(keycourse).update({'studentList': studentInCourse })
               studentInfo = database.child("StudentAll").child(sid).get().val()
               student = list(dict(studentInfo).values())[0]
               courseList= []
               if "courseList" in student:
                    courseList = student['Student']
               courseList.append(keycourse)
               database.child("StudentAll").child(sid).update({"courseList": courseList})
               return redirect('/addstudentpage/'+ namecourse) 
          else:
               return redirect('/addstudentpage/'+ namecourse)    
     else:
          return redirect('/loginPage')

def deleteStudent(request,namecourse):
     if 'uid' in request.session and request.session != '' :
          if request.method == "POST":
               sid = request.POST['sid']
               path = request.POST['path'] 
               courseInfo = database.child("CourseAll").order_by_child("coursename").equal_to(namecourse).get().val()
               courseInfo = dict(courseInfo)
               keycourse = list(courseInfo.keys())[0]
               valusecourse= list(courseInfo.values())[0]
               studentInCourse = []
               if 'studentList' in valusecourse:
                    studentInCourse = valusecourse['studentList']
               if sid in studentInCourse:
                    studentInCourse.remove(sid)
               database.child("CourseAll").child(keycourse).update({'studentList': studentInCourse })
               studentInfo = database.child("StudentAll").child(sid).get().val()
               student = list(dict(studentInfo).values())[0]
               courseList= []
               if "courseList" in student:
                    courseList = student['Student']
               courseList.remove(keycourse)
               database.child("StudentAll").child(sid).update({"courseList": courseList})
               return redirect(path) 
          else:
               return redirect(path)    
     else:
          return redirect('/loginPage')

def studentCourse(request,name):
     if 'class_room' in request.session:
          try:
               del request.session['class_room']
          except:
               pass
     courseInfo = database.child("CourseAll").order_by_child("coursename").equal_to(name).get().val()
     courseInfo = dict(courseInfo)
     value = list(courseInfo.values())[0]
     studentList =[]
     if 'studentList' in value:
          for  sid in value['studentList']:
               student =  database.child('StudentAll').child(sid).get().val()
               student['sid'] = sid
               studentList.append(student)
     return  render(request,'Home/studentcourse.html',{'namecourse':name,'studentList':studentList})

def newFolderPage(request,name):
     if 'uid' in request.session and request.session != '' :
          return  render(request,'Home/newfolder.html',{"name":name})
     else:
          return redirect('/loginPage')

def newFolder(request):
     if 'uid' in request.session and request.session != '' :
          course = request.POST["course"]
          foldername = request.POST["foldername"]
          courseInfo = database.child("CourseAll").order_by_child("coursename").equal_to(course).get().val()
          courseInfo = dict(courseInfo)
          key = list(courseInfo.keys())[0]
          value = list(courseInfo.values())[0]
          folderAll = []
          if 'folderAll' in value:
               folderAll = value['folderAll']
          folder = list(filter(lambda folder: folder["folder_name"] == foldername, folderAll))
          if len(folder) >0:
               messages.info(request,'ใช้ชือซ้ำ')
               return  render(request,'Home/newfolder.html',{"name":course})
          else:
               folderAll.append(
                    {
                         'folder_name':foldername,
                         "fileAll":[]
                    }
               )
               database.child("CourseAll").child(str(key)).update({'folderAll':folderAll})
               return  redirect('course/'+course)
     else:
          return redirect('/loginPage')


def createCoursePage(request):
     if 'uid' in request.session and request.session != '' :
          return  render(request,'Home/createcourse.html')
     else:
          return redirect('/loginPage')


def createCourse(request):
     if 'uid' in request.session and request.session != '' :
          name = request.POST['coursename']
          image = request.POST['Image']
          description= request.POST['description']
          owner_data = database.child('TeacherAll').child(request.session['uid']).get().val()
          teacher_name = dict(owner_data)['name'] + ' ' + dict(owner_data)['lastname']
          if image == 'Upload':

               imgCourse = request.FILES['img']
               namecourse = imgCourse.name
               path_on_cloud = name + "/" + imgCourse.name
               cloud = storage.child(path_on_cloud).put(imgCourse)
               imgCourse = storage.child(path_on_cloud).get_url(cloud["downloadTokens"])
          else:
               namecourse = request.POST['imgCourse']
               imgCourse = "/static/img/courses/"+request.POST['imgCourse']
          data = {
               'nameImageCourse':namecourse,
               'imgcourse':imgCourse,
               'coursename':name,
               'description': description,
               'teacherId': request.session['uid'],
               'teacherName': teacher_name,
               'teacherSubject': dict(owner_data)['subject']
          }
          database.child('CourseAll').push(data)
          return redirect('/')
     else:
          return redirect('/loginPage')
     
def openFolder(request, namecourse, namefolder):
     if 'uid' in request.session and request.session != '' :
          course = dict(database.child("CourseAll").order_by_child("coursename").equal_to(namecourse).get().val())
          course_data = list(course.values())[0]
          allFolder = course_data["folderAll"]
          folder_list = list(filter(lambda folder: folder["folder_name"] == namefolder, allFolder))
          if not folder_list:
               return redirect('/error')
          else:
               folder = folder_list[0]
          data = {}
          data["foldername"] = namefolder
          data["coursename"] = namecourse
          data["allFile"] = []
          if "fileAll" in folder:
               data["allFile"] = folder["fileAll"]
          return render(request, "Home/folder.html", data)
     else:
          return redirect('/loginPage')

def newFilePage(request, namecourse, namefolder):
     if 'uid' in request.session and request.session != '':
          data = {}
          data["namecourse"] = namecourse
          data["namefolder"] = namefolder
          return render(request, "Home/newfilepage.html", data)
     else:
          return redirect('/loginPage')
     
def error(request):
     return render(request, "error.html")

def uploadFile(request, namecourse, namefolder):
     if 'uid' in request.session and request.session != '':
          file = request.FILES['material']
          path_on_cloud = namecourse + "/" + namefolder + "/" + file.name
          cloud = storage.child(path_on_cloud).put(file)
          courseInfo = database.child("CourseAll").order_by_child("coursename").equal_to(namecourse).get().val()
          courseKey =list(dict(courseInfo).keys())[0]
          course = list(dict(courseInfo).values())
          if course:
               course = course[0]
          else:
               return redirect("/error")
          folderAll = course["folderAll"]
          folder = list(filter(lambda folder: folder["folder_name"] == namefolder, folderAll))
          folderIndex = -1
          if folder:
               folder = folder[0]
               folderIndex = folderAll.index(folder)
          else:
               return redirect("/error")
          allfile = []
          if "fileAll" in folder:
               allfile = folder["fileAll"]
          tz = pytz.timezone('Asia/Bangkok')
          now1 = datetime.datetime.now(tz)
          time_str = now1.strftime('%H:%M:%S')
          date_str = now1.date()
          total = str(date_str)+" "+ time_str
          file_metadata = {
               "filename": file.name,
               "download_url": storage.child(path_on_cloud).get_url(cloud["downloadTokens"]),
               "type": file.content_type,
               "size": file.size,
               "data" : total
          }
          allfile.append(file_metadata)
          database.child("CourseAll").child(courseKey).child('folderAll').child(folderIndex).update({'fileAll': allfile})
          
          return redirect('/openfolder/'+namecourse+'/'+namefolder)
     else:
          return redirect('/loginPage')

def deleteFile(request, namecourse, namefolder, namefile):
     if 'uid' in request.session and request.session != '':
          courseInfo = database.child("CourseAll").order_by_child("coursename").equal_to(namecourse).get().val()
          courseKey =list(dict(courseInfo).keys())[0]
          course = list(dict(courseInfo).values())
          if course:
               course = course[0]
          else:
               return redirect("/error")
          folderAll = course["folderAll"]
          folder = list(filter(lambda folder: folder["folder_name"] == namefolder, folderAll))
          folderIndex = -1
          if folder:
               folder = folder[0]
               folderIndex = folderAll.index(folder)
          else:
               return redirect("/error")
          allfile = []
          if "fileAll" in folder:
               allfile = folder["fileAll"]
          else:
               return redirect("/error")
          file = list(filter(lambda file: file["filename"] == namefile, allfile))
          if file:
               file = file[0]
          else:
               return redirect("/error")
          download_url = file["download_url"]
          download_token = download_url.split("token=")[1]
          allfile.remove(file)
          path_on_cloud = namecourse + "/" + namefolder + "/" + namefile
          storage.delete(path_on_cloud, download_token)
          database.child("CourseAll").child(courseKey).child('folderAll').child(folderIndex).update({'fileAll': allfile})
          return redirect('/openfolder/' + namecourse + '/' + namefolder)
     else:
          return redirect('/loginPage')

def deleteFolder(request, namecourse, namefolder):
     if 'uid' in request.session and request.session != '':
          courseInfo = database.child("CourseAll").order_by_child("coursename").equal_to(namecourse).get().val()
          courseKey =list(dict(courseInfo).keys())[0]
          course = list(dict(courseInfo).values())
          if course:
               course = course[0]
          else:
               return redirect("/error")
          folderAll = course["folderAll"]
          folder = list(filter(lambda folder: folder["folder_name"] == namefolder, folderAll))
          folderIndex = -1
          if folder:
               folder = folder[0]
               folderIndex = folderAll.index(folder)
          else:
               return redirect("/error")
          allfile = []
          if "fileAll" in folder:
               allfile = folder["fileAll"]
          else:
               return redirect("/error")
          for file in allfile:
               print(file)
               download_url = file["download_url"]
               download_token = download_url.split("token=")[1]
               path_on_cloud = namecourse + "/" + namefolder + "/" + file["filename"]
               storage.delete(path_on_cloud, download_token)
          database.child("CourseAll").child(courseKey).child('folderAll').child(folderIndex).remove()
          return redirect('/course/' + namecourse)
     else:
          return redirect('/loginPage')

def deleteCourse(request, namecourse):
     if 'uid' in request.session and request.session != '':
          course = firebase_course.get_course_info(namecourse)
          
          if course["data"]:
               course["data"] = course["data"][0]
          else:
               return redirect("/error")
          img = course["data"]['imgcourse']
          nameimg =course["data"]['nameImageCourse'] 
          img_token = img.split("token=")
          if len(img_token) > 1:
               img_token= img_token[1]
               path_on_cloud = namecourse + "/" + nameimg
               storage.delete(path_on_cloud, img_token)
          folderAll = []
          if "folderAll" in course["data"]:
               folderAll = course["data"]["folderAll"]
               
          for folder in folderAll:
               allfile = []
               if "fileAll" in folder:
                    allfile = folder["fileAll"]
               # else:
               #      return redirect("/error")
               for file in allfile:
                    
                    download_url = file["download_url"]
                    download_token = download_url.split("token=")[1]
                    path_on_cloud = namecourse + "/" + folder["folder_name"] + "/" + file["filename"]
                    storage.delete(path_on_cloud, download_token)
          studentList = []
          if "studentList" in course["data"]:
               studentList = course["data"]["studentList"]
          for sid in studentList:
               studentInfo = database.child("StudentAll").child(sid).get().val()
               student = dict(studentInfo)
               courseList= []
               if "courseList" in student:
                    courseList = student["courseList"]
               print(student)
               print(course["key"])
               courseList.remove(course["key"])
               database.child("StudentAll").child(sid).update({"courseList": courseList})
          database.child("CourseAll").child(course["key"]).remove()
          return redirect('/')
     else:
          return redirect('/loginPage')
     