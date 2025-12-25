import json
import traceback

from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import render, redirect

from .. import models


# 选课
def takecourse(request):
    curID = cache.get('LoginID')
    if curID is None or curID == 1:
        return redirect('/login')
    curStu = cache.get('StuID')
    if curStu is None:
        return redirect('/personal')

    if request.method == 'GET':
        allcourses = models.CourseInfo.objects.all()
        selcourse = models.CourseSelect.objects.values('courseid__coursename',
                                                       'courseid__starttime',
                                                       'courseid__endtime',
                                                       'courseid__weekday',
                                                       'courseid_id',
                                                       'id').filter(stuid__stuid=curStu)
        sel = models.CourseSelect.objects.filter(stuid__stuid=curStu)
        blockcourse = allcourses.filter(id__in=sel.values_list('courseid__id', flat=True))
        restcourse = allcourses.exclude(id__in=blockcourse.values_list('id'))

        return render(request, 'takecourse.html',
                      {'restcourse': restcourse, 'selcourse': selcourse, 'blockcourse': blockcourse})

    elif request.method == 'POST':
        courseid = json.loads(request.body).get('courseid')

        new = models.CourseInfo.objects.filter(id=courseid).first()
        selected = models.CourseSelect.objects.values('courseid',
                                                      'courseid__starttime',
                                                      'courseid__endtime',
                                                      'courseid__weekday').filter(stuid__stuid=curStu)

        for sel in selected:
            if sel['courseid__starttime'] < new.starttime < sel['courseid__endtime'] \
                    and new['weekday'] == sel['weekday']:
                return JsonResponse({'err': "课程时间冲突"})
            if sel['courseid'] == courseid:
                return JsonResponse({'err': "重复选课"})

        try:
            newsel = models.CourseSelect()
            stu = models.StuInfo.objects.filter(stuid=curStu).first()
            newsel.stuid = stu
            newsel.courseid = new
            newsel.save()
            return JsonResponse({'succ': '选课成功'})
        except Exception as e:
            traceback.print_exc()
            return JsonResponse({'err': e})


def deltaked(request):
    curID = cache.get('LoginID')
    if curID is None:
        return redirect('/login')
    curStu = cache.get('StuID')
    if curStu is None:
        return redirect('/personal')

    delid = json.loads(request.body).get('delid')
    if delid is not None:
        try:
            ob = models.CourseSelect.objects.filter(courseid__id=delid)
            if ob.count() == 0:
                return JsonResponse({"err": "记录为空"})
            ob.all().delete()
            return JsonResponse({'succ': '删除完成'})
        except Exception as e:
            traceback.print_exc()
            return JsonResponse({'err': e})
    else:
        return JsonResponse({'err': '错误请求，delid为空'})
