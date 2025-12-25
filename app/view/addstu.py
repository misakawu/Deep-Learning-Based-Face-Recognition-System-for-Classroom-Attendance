import traceback

from django.core.cache import cache
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .. import models
from ..views import faceRecSys


def add(request):
    curID = cache.get('LoginID')
    if curID is None or curID != 1:
        return redirect('/login')

    if request.method == 'GET':
        info = models.StuInfo.objects.all()
        return render(request, 'add.html', {'info': info})
    elif request.method == 'POST':
        list = ['stuname', 'stuid']
        info = []
        for li in list:
            info.append(request.POST.get(li))
        s = models.StuInfo.objects.filter(stuid=info[1])
        # 判断是否已存在重复的数据
        if len(s) != 0:
            return render(request, 'add.html', {'err': '该学号已存在，请勿重复添加'})

        try:
            stu = models.StuInfo()
            stu.stuname = info[0]
            stu.stuid = info[1]
            stu.save()  # 保存数据
        except Exception as e:
            traceback.print_exc()
            faceRecSys.deleteOneFace(info[1])
            return render(request, 'add.html', {'err': '数据库错误'})
        return redirect('/add')
