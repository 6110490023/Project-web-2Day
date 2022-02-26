from django.urls import path
from . import views
urlpatterns = [   
path('',views.Home, name = 'Home'),
path('loginPage',views.loginPage , name = 'loginPage'),
path('register',views.register , name = 'register'),
path('createUser',views.createUser , name = 'createUser'),
path('login',views.login , name = 'login'),
path('logout',views.logout , name = 'logout'),
path('couse',views.couse , name = 'couse'),
path('addstudentpage',views.addStudentPage , name = 'addStudentPage'),
#path('test',views.test , name = 'test'),
path('profile',views.profile , name = 'profile'),
path('editprofilepage',views.editProfilePage , name = 'editProfilePage'),
path('studentcouse',views.studentCouse , name = 'studentCouse'),
path('newfolderpage',views.newFolderPage, name = 'newFolderPage'),
path('createcousepage',views.createCousePage, name = 'createCousePage'),


]