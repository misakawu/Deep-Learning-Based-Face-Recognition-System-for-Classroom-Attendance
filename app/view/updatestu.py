from django.core.cache import cache
from django.shortcuts import render, redirect

from .. import models
from ..views import faceRecSys


def update(request):
    curID = cache.get('LoginID')
    if curID is None or curID != 1:
        return redirect('/login')

    if request.method == 'GET':
        info = models.StuInfo.objects.all()
        return render(request, 'update.html', {'info': info})

    list = ['id', 'stuname', 'stuid']
    data = []
    for li in list:
        data.append(request.POST.get(li))

    s = models.StuInfo.objects.filter(id=data[0])

    if s.count() == 0:
        info = models.StuInfo.objects.all()
        return render(request, 'update.html', {'err': '没有此学生信息，无法修改', 'info': info})

    s = s.first()
    if data[1] != '':
        s.stuname = data[1]
    if data[2] != '':
        if not faceRecSys.updateName(s.stuid, data[2]):
            print('Sqlite Update ERR')
        s.stuid = data[2]
    s.save()

    info = models.StuInfo.objects.all()
    return render(request, 'update.html', {'success': '学生信息修改成功！', 'info': info})
