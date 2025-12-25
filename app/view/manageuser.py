import json
import traceback

from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import render, redirect

from .. import models
from ..views import faceRecSys


def manageuser(request):
    curID = cache.get('LoginID')
    if curID is None or curID != 1:
        return redirect('/login')

    if request.method == 'GET':
        return getmethod(request)
    elif request.method == 'POST':
        userid = request.POST.get('userid', None)
        username = request.POST.get('username', None)
        pwd = request.POST.get('pwd', None)
        linkstu = request.POST.get('linkstu', None)

        if userid is None or userid == '':
            return errmethod(request, '请输入用户ID')
        else:
            check = models.UserInfo.objects.filter(UserId=userid).count()
            if check == 0:
                return errmethod(request, '用户不存在')

        if username is not None and username != '':
            try:
                models.UserInfo.objects.filter(UserId=userid).update(username=username)
            except Exception as e:
                return errmethod(request, e)
        if pwd is not None and pwd != '':
            try:
                models.UserInfo.objects.filter(UserId=userid).update(password=pwd)
            except Exception as e:
                return errmethod(request, e)
        if linkstu is not None and  linkstu != '':
            try:
                models.UserStudentLink.objects.filter(userid=models.UserInfo.objects.get(UserId=userid)).delete()
                models.UserStudentLink.objects.create(userid=models.UserInfo.objects.get(UserId=userid),
                                                      stuid=models.StuInfo.objects.get(stuid=linkstu))
            except Exception as e:
                return errmethod(request, e)
        return redirect('/usermanage')


def getmethod(request):
    stu = models.StuInfo.objects.all()
    linked = models.UserStudentLink.objects.all().values('userid__username',
                                                         'userid__UserId',
                                                         'userid__password',
                                                         'stuid__stuname',
                                                         'stuid__stuid')
    if linked.count() == 0:
        alluser = models.UserInfo.objects.all()
        return render(request, 'manageuser.html', {'stu': stu, 'alluser': alluser})
    else:
        notlinked = models.UserInfo.objects.filter(UserId__gt=1).exclude(UserId__in=linked.values('userid__UserId'))
        return render(request, 'manageuser.html', {'stu': stu, 'linked': linked, 'notlinked': notlinked})


def errmethod(request, err):
    stu = models.StuInfo.objects.all()
    linked = models.UserStudentLink.objects.all().values('userid__username',
                                                         'userid__UserId',
                                                         'userid__password',
                                                         'stuid__stuname',
                                                         'stuid__stuid')
    if linked.count() == 0:
        alluser = models.UserInfo.objects.all()
        return render(request, 'manageuser.html', {'stu': stu, 'alluser': alluser})
    else:
        notlinked = models.UserInfo.objects.filter(UserId__gt=1).exclude(UserId__in=linked.values('userid__UserId'))
        return render(request, 'manageuser.html', {'stu': stu, 'linked': linked, 'notlinked': notlinked, 'err': err})
