from django.urls import path

from .view.deleteuser import deleteuser
from .view.addface import addface
from .view.addstu import add
from .view.assigncourse import assigncourse
from .view.attend import attend
from .view.attendlog import attendlog
from .view.course import course
from .view.delete import delete
from .view.deletecourse import coursedel
from .view.home import home
from .view.info import info
from .view.login import login
from .view.manageuser import manageuser
from .view.personal import personal
from .view.select import select
from .view.startcourse import startcourse
from .view.takecourse import takecourse, deltaked
from .view.updatecourse import courseupdate
from .view.updateface import updateface
from .view.updatestu import update
from .view.welcome import welcome

urlpatterns = [
    path('', home, name="首页"),
    path('add/', add, name="添加学生信息"),
    path('add/face', addface, name='添加人脸信息'),
    path('attend/', attend, name="打卡"),
    path('course/', course, name="课程查询、增加"),
    path('course/update', courseupdate, name="课程修改"),
    path('course/delete', coursedel, name="课程删除"),
    path('course/start', startcourse, name="课程打卡"),
    path('course/log', attendlog, name="考勤记录"),
    path('delete/', delete, name="删除学生信息"),
    path('info/', info, name="所有学生信息"),
    path('login/', login, name="登录"),
    path('personal/', personal, name="学生个人信息"),
    path('select/', select, name="查询学生相关信息"),
    path('takecourse/', takecourse, name="选课"),
    path('takecourse/assign', assigncourse, name="分配课程"),
    path('takecourse/delete', deltaked, name='删除选课'),
    path('update/', update, name="修改学生信息"),
    path('update/face', updateface, name='更新学生人脸信息'),
    path('welcome/', welcome, name="系统主界面"),
    path('usermanage/', manageuser, name="用户信息管理"),
    path('usermanage/delete/', deleteuser, name="删除用户")
]
