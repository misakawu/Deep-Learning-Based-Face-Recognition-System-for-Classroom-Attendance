import json
import traceback

from django.core.cache import cache
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from .. import models


def assigncourse(request):
    curID = cache.get('LoginID')
    if curID is None or curID != 1:
        return redirect('/login')

    if request.method == 'GET':
        allcourses = models.CourseInfo.objects.all()
        allstu = models.StuInfo.objects.all()
        return render(request, 'assigncourse.html', {'allcourses': allcourses, 'allstu': allstu})

    elif request.method == "POST":
        data = json.loads(request.body)
        courseid = data['courseid']
        stulist = data['stulist']
        stulist = list(set(stulist))

        stulist = models.StuInfo.objects.filter(id__in=stulist)
        if stulist.count() == 0:
            return JsonResponse({'err': "不存在有效学生"})
        course = models.CourseInfo.objects.filter(id=courseid)
        if course.count() == 0:
            return JsonResponse({'err': "不存在该课程"})

        for stu in stulist:
            # 检查是否已选
            if models.CourseSelect.objects.filter(stuid=stu, courseid=course.first()).count() != 0:
                continue
            try:
                newsel = models.CourseSelect()
                newsel.courseid = course.first()
                newsel.stuid = stu
                newsel.save()
            except:
                traceback.print_exc()
                return JsonResponse({'err': "数据库错误"})
        return JsonResponse({'succ': "分配成功"})