import datetime

from django.core.cache import cache
from django.shortcuts import render, redirect

from .. import models


def select(request):
    curID = cache.get('LoginID')
    stuID = cache.get('StuID')
    if curID is None:
        return redirect('/login')
    if stuID is None and curID != 1:
        return redirect('/personal')

    if curID != 1:
        stureq, selectcourse = utilfunc(stuID)
        return render(request, 'select.html', {'stureq': stureq, 'courses': selectcourse})
    else:
        if request.method == 'GET':
            return render(request, 'select.html', {'loginid': curID})
        if request.method == 'POST':
            selectId = request.POST.get('stuid', None)
            stureq, selectcourse = utilfunc(selectId)
            return render(request, 'select.html', {'stureq': stureq, 'loginid': curID, 'courses': selectcourse})


def utilfunc(searchdata):
    attendedlogs = models.AttendenceLog.objects.filter(stuid__stuid=searchdata)
    reqid = list(attendedlogs.values_list('requestid__id', flat=True))
    courseid = models.CourseSelect.objects.filter(stuid__stuid=searchdata).values('courseid__id')
    stureq = models.AttendRequest.objects.filter(courseid__id__in=courseid).values('id',
                                                                                   'courseid__coursename',
                                                                                   'starttime',
                                                                                   'endtime')
    now = datetime.datetime.now()
    stureq = list(stureq)
    for req in stureq:
        if req['id'] in reqid:
            req['state'] = True
        else:
            req['state'] = False
            if req['endtime'] > now:
                req['able'] = True  # 未打卡
            else:
                req['able'] = False  # 已过期
    selectcourse = models.CourseSelect.objects.values('stuid__stuid',
                                                      'stuid__stuname',
                                                      'courseid__coursename',
                                                      'courseid__starttime',
                                                      'courseid__endtime',
                                                      'courseid__weekday').filter(stuid__stuid=searchdata)
    return stureq, selectcourse
