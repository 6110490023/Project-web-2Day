from django.urls import path
from . import views
from . import views_test
urlpatterns = [   
path('',views.Home),

path('loginPage',views.loginPage , name = 'loginPage'),
path('register',views.register , name = 'register'),
path('createUser',views.createUser , name = 'createUser'),
path('login',views.login , name = 'login'),
path('logout',views.logout , name = 'logout'),
path('course/<str:name>',views.course , name = 'course'),
path('addstudentpage/<str:name>',views.addStudentPage , name = 'addStudentPage'),
path('profile',views.profile , name = 'profile'),
path('editprofilepage',views.editProfilePage , name = 'editProfilePage'),
path('studentcourse/<str:name>',views.studentCourse , name = 'studentcourse'),
path('newfolderpage/<str:name>',views.newFolderPage, name = 'newFolderPage'),
path('newfolder',views.newFolder, name = 'newFolder'),
path('createcoursepage',views.createCoursePage, name = 'createcoursePage'),
path('createcourse',views.createCourse, name = 'createCourse'),
path('openfolder/<str:namecourse>/<str:namefolder>', views.openFolder, name='openfolder'),
path('newfilepage/<str:namecourse>/<str:namefolder>', views.newFilePage, name = 'newFilePage'),
path('upload/<str:namecourse>/<str:namefolder>', views.uploadFile, name='upload'),
path('error', views.error, name="errorPage"),
path('addstudent/<str:namecourse>',views.addStudent, name="addstudent"),
path('deletefile/<str:namecourse>/<str:namefolder>/<str:namefile>', views.deleteFile, name="deleteFile"),
path('deletefolder/<str:namecourse>/<str:namefolder>', views.deleteFolder, name="deleteFolder"),
path('deletestudent/<str:namecourse>', views.deleteStudent, name="deleteStudent"),
path('deletecourse/<str:namecourse>', views.deleteCourse, name='deleteCourse'),
path('editprofile', views.editProfile, name='editprofile'),
]