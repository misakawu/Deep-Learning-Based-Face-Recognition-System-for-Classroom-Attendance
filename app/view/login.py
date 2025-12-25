from django.core.cache import cache
from django.shortcuts import render, redirect

from .. import models

from ..views import faceRecSys


def login(request):
    if request.method == "GET":
        cache.set('LoginID', None)
        cache.set('StuID', None, 600)
        return render(request, "login.html")
    else:
        # 从前端表单中获取输入的数据，即账号和密码
        name = request.POST.get("username", None)
        pwd = request.POST.get("password", None)
        type = request.POST.get("type", None)
        if name == '' or pwd == '':
            return render(request, "login.html", {"msg": "错误信息,账户或密码不能为空"})
        if type != 'login' and type != 'register':
            return render(request, "login.html", {"msg": "登录失败,请合法登录"})

        if type == 'login':
            emp = models.UserInfo.objects.values("username", "password", "UserId").filter(username=name)
            if emp.count() == 0:
                return render(request, "login.html", {"msg": "登录失败,账号不存在"})
            else:
                if emp[0]['password'] == pwd:
                    curID = emp[0]['UserId']
                    cache.set('LoginID', curID, 600)
                    link = models.UserStudentLink.objects.filter(userid__UserId=curID).first()
                    if link is not None:
                        stu = models.StuInfo.objects.filter(id=link.stuid_id).first()
                        cache.set('StuID', stu.stuid, 600)
                    return redirect('/welcome')
                else:
                    return render(request, "login.html", {'msg': '登陆失败,密码错误'})
        else:
            emp = models.UserInfo.objects.values("username", "password", "UserId").filter(username=name)
            if emp.count() == 0:
                try:
                    newuser = models.UserInfo()
                    newuser.username = name
                    newuser.password = pwd
                    newuser.save()
                    return render(request, "login.html", {'msg': '注册成功，请重新登录'})
                except Exception as e:
                    return render(request, "login.html", {"msg": e})
            else:
                return render(request, "login.html", {"msg": "注册失败，账号已存在"})
