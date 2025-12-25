import datetime
import json
import traceback

from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import redirect

from .. import models
from ..views import faceRecSys


def attend(request):
    curID = cache.get('LoginID')
    if curID is None or curID != 1:
        return redirect('/login')

    if request.method == 'POST':
        data = json.loads(request.body)
        reqid = data.get('reqid')
        # 检查时间合法性
        req = models.AttendRequest.objects.get(id=reqid)
        now = datetime.datetime.now()
        if not req.starttime < now < req.endtime:
            return JsonResponse({'err': "考勤时间错误"})

        try:
            stuidlist = faceRecSys.getAndCheckFace()
        except Exception as e:
            traceback.print_exc()
            return JsonResponse({'err': e})
        if len(stuidlist) == 0:
            return JsonResponse({"err": '没有检测有效人脸，请确定是否录入系统'})
        stuidlist = list(set(stuidlist))
        print('recognized faces:', stuidlist)

        stus = []
        for stuid in stuidlist:
            if stuid == '':
                continue
            stu = models.StuInfo.objects.filter(stuid=int(stuid))
            if stu.count() != 0:
                stus.append(stu.first())
        if len(stus) == 0:
            return JsonResponse({"err": '没有检测有效学生信息或人脸与当前用户不匹配'})

        logList = []
        stuNames = ''
        for stu in stus:
            areq = models.AttendRequest.objects.filter(id=reqid)
            if areq.count() != 0:
                # 判断是否选课
                coursesid = models.CourseSelect.objects.filter(stuid__stuid=stu.stuid).values_list('courseid__id',
                                                                                                   flat=True)
                coursesid = list(coursesid)
                if areq.first().courseid_id not in coursesid:
                    continue
                # 查重
                # logs = models.AttendenceLog.objects.filter(requestid__id=areq.first().id)
                logs = models.AttendenceLog.objects.filter(stuid__stuid=stu.stuid)
                if logs.count() == 0:
                    newlog = models.AttendenceLog()
                    newlog.stuid = stu
                    newlog.attendtime = now
                    newlog.requestid = areq.first()
                    logList.append(newlog)
                    stuNames += stu.stuname+','
        if len(logList) == 0:
            return JsonResponse({"err": '没有检测到未考勤学生'})
        for i in logList:
            i.save()
        return JsonResponse({'succ': "学生"+stuNames+"打卡成功"})
