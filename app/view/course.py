from django.core.cache import cache
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect

from .. import models


@csrf_protect
def course(request):
    curID = cache.get('LoginID')
    if curID is None:
        return redirect('/login')

    if request.method == 'GET':
        courses = models.CourseInfo.objects.all()
        if curID == 1:
            return render(request, 'course.html', {'manager': True, 'courses': courses})
        return render(request, 'course.html', {'courses': courses})

    if request.method == 'POST':
        if curID != 1:
            return redirect('/login')

        list = ['coursename', 'starttime', 'endtime', 'weekday']
        err = ['课程名不能为空', '上课时间不能为空', '下课时间不能为空', '开课日期不能为空']
        datas = []
        for idx, li in enumerate(list):
            data = request.POST.get(li)
            if len(data) == 0:
                courses = models.CourseInfo.objects.all()
                return render(request, 'course.html', {'manager': True, 'courses': courses, 'err': err[idx]})
            datas.append(data)

        newCourse = models.CourseInfo()
        newCourse.coursename = datas[0]
        newCourse.starttime = datas[1]
        newCourse.endtime = datas[2]
        newCourse.weekday = datas[3]
        newCourse.save()
        courses = models.CourseInfo.objects.all()
        return render(request, 'course.html',
                      {'manager': True, 'courses': courses, 'succ': '添加课程成功'})
