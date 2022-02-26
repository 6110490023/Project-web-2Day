from django.shortcuts import render,redirect
from django.contrib.auth.models import User ,auth
from django.contrib import messages

def Home(request):
     if request.user.is_authenticated :
          if request.user.username[0:1] == 't':
               return render(request,'Home/teacher.html')
          elif request.user.username[0:1] == 's':
               print(555555)
               return render(request,'Home/student.html')
          else :
               auth.logout(request)
               messages.info(request,'Username ถูกต้อง')
               return redirect('/loginPage')
     else:
          return redirect('/loginPage')

def loginPage(request):
     return render(request,'login.html')

def register(request):
     return render(request,'register.html')

def createUser(request):
     username=request.POST['Username']
     firstname=request.POST['Firstname']
     lastname=request.POST['Lastname']
     email=request.POST['Email']
     password=request.POST['Password']
     repassword=request.POST['RePassword']
     status = request.POST['status']
     if status=='student' :
          numberclass = request.POST['class']
          room = request.POST['room']
     if password==repassword :
        if User.objects.filter(username=username).exists():
            messages.info(request,'UserName นีมีคนใช้แล้ว')
            return redirect('/register')
        elif User.objects.filter(email=email).exists():
            messages.info(request,'Email นี้เคยลงทะเบียนแล้ว')
            return redirect('/register')
        else :
            user=User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=firstname,
            last_name=lastname
            )

            user.save()    
            return redirect('/loginPage')
     else :
          messages.info(request,'รหัสผ่านไม่ตรงกัน')
          return redirect('/register')

def login(request):
     username=request.POST['Username']
     password=request.POST['Password']

     #check username ,password
     user=auth.authenticate(username=username,password=password)

     if user is not None :
          auth.login(request,user)
          return redirect('/')
     else :
          messages.info(request,'ไม่พบข้อมูล')
          return redirect('/loginPage')

def logout(request):
    auth.logout(request)
    return redirect('/loginPage')
    
def couse(request):
     status = request.user.username[0:1]
     return  render(request,'Home/couse.html',{"status":status})

def test(request):
     return  render(request,'test.html')

def addStudentPage(request):
     return  render(request,'Home/addstudent.html')

def profile(request):
     return  render(request,'Home/profile.html')

def editProfilePage(request):
     return  render(request,'Home/editProfile.html')

def studentCouse(request):
     return  render(request,'Home/studentcouse.html')

def newFolderPage(request):
     return  render(request,'Home/newfolder.html')

def createCousePage(request):
     return  render(request,'Home/createcouse.html')