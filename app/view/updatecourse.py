from django.core.cache import cache
from django.shortcuts import render, redirect

from .. import models


def courseupdate(request):
    curID = cache.get('LoginID')
    if curID is None:
        return redirect('/login')

    if curID != 1:
        return render(request, 'course.html')

    list = ['oldname', 'newname', 'starttime', 'endtime', 'weekday']
    err = ['课程名不能为空', '上课时间不能为空', '下课时间不能为空', '开课日期不能为空']
    datas = []
    for idx, li in enumerate(list):
        data = request.POST.get(li)
        if len(data) == 0:
            courses = models.CourseInfo.objects.all()
            return render(request, 'course.html', {'manager': True, 'courses': courses, 'err': err[idx]})
        datas.append(data)

    old = models.CourseInfo.objects.get(coursename=datas[0])
    old.coursename = datas[1]

    courses = models.CourseInfo.objects.all()
    return render(request, 'course.html', {'manager': True, 'courses': courses, 'succ': '添加课程成功'})
