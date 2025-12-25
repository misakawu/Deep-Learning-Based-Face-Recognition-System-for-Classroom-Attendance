import traceback

from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import render, redirect

from .. import models
from ..views import faceRecSys


def personal(request):
    curID = cache.get('LoginID')
    if curID is None:
        return redirect('/login')

    if request.method == 'GET':
        stuID = cache.get('StuID')
        if stuID is not None:
            selcourse = models.CourseSelect.objects.values('courseid__starttime',
                                                           'courseid__weekday',
                                                           'courseid__coursename',
                                                           'courseid__endtime',
                                                           'courseid__id').filter(stuid__stuid=stuID)
            info = models.StuInfo.objects.filter(stuid=stuID).first()
            return render(request, 'personal.html', {'courses': selcourse, 'info': info})
        else:
            return render(request, 'personal.html', {'notlink': True})
    elif request.method == 'POST':
        stuid = faceRecSys.getAndCheckFace()
        if len(stuid) == 0:
            return JsonResponse({"err": '没有检测人脸'})
        print('检测到的人脸：', stuid)
        old = models.UserStudentLink.objects.filter(stuid__stuid__in=stuid)
        if old.count() != 0:
            return JsonResponse({"err": '该学生已被验证'})

        stus = []
        for id in stuid:
            info = models.StuInfo.objects.filter(stuid=id)
            if info.count() != 0:
                stus.append(info.first())
        # print(stus)

        if len(stus) == 0:
            return JsonResponse({"err": '没有检测有效学生信息，请确定是否录入系统'})

        try:
            newlink = models.UserStudentLink()
            newlink.stuid = models.StuInfo.objects.get(stuname=stus[0].stuname)
            newlink.userid = models.UserInfo.objects.get(UserId=curID)
            newlink.save()
            cache.set('StuID', stus[0].stuid)
            return JsonResponse({'succ': '匹配完成'})
        except Exception as e:
            traceback.print_exc()
            JsonResponse({"err": e})
