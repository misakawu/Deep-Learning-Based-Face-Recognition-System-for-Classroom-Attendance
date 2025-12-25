import datetime
import traceback

from django.core.cache import cache
from django.shortcuts import render, redirect

from .. import models


def startcourse(request):
    """
    :url /course/start/
    :method 处理老师发出的考勤开始申请
    """
    curID = cache.get('LoginID')
    if curID is None or curID != 1:
        return redirect('/login')

    if request.method == 'GET':
        histories = models.AttendRequest.objects.all().order_by('starttime', 'endtime').values('id',
                                                                                               'starttime',
                                                                                               'endtime',
                                                                                               'courseid__coursename')
        courses = models.CourseInfo.objects.all()
        return render(request, 'startcourse.html', {'histories': histories, 'courses': courses})

    elif request.method == 'POST':
        courseid = request.POST.get('courseid')
        course = models.CourseInfo.objects.filter(id=courseid)
        if course.count() == 0:
            histories = models.AttendRequest.objects.all().order_by('starttime', 'endtime')
            courses = models.CourseInfo.objects.all()
            return render(request, 'startcourse.html',
                          {'histories': histories, 'courses': courses, 'err': '不存在该课程课程'})

        duration = int(request.POST.get('duration'))
        thisweek = request.POST.get('thisweek')
        cstime = course.first().starttime
        now = datetime.datetime.now()
        if thisweek == 'true':
            if course.first().weekday < now.weekday() or \
                    (course.first().weekday == now.weekday() + 1 and
                     course.first().endtime < now.time()):
                # 课程结束判断
                histories = models.AttendRequest.objects.all().order_by('starttime', 'endtime')
                courses = models.CourseInfo.objects.all()
                return render(request, 'startcourse.html',
                              {'histories': histories, 'courses': courses, 'err': '本周课程已结束，请预约下周考勤'})
            else:
                starttime = datetime.datetime(year=now.year, month=now.month, day=now.day,
                                              hour=cstime.hour, minute=cstime.minute, second=cstime.second)
                starttime = starttime + datetime.timedelta(days=course.first().weekday - now.weekday() - 1, minutes=-10)
        else:
            starttime = datetime.datetime(year=now.year, month=now.month, day=now.day + 7,
                                          hour=cstime.hour, minute=cstime.minute, second=cstime.second)
            starttime = starttime + datetime.timedelta(days=course.first().weekday - now.weekday() - 1, minutes=-10)
        # starttime为课程开始前10min endtime为课程开始时间+duration
        endtime = starttime + datetime.timedelta(minutes=duration+10)
        try:
            newrequest = models.AttendRequest()
            newrequest.starttime = starttime
            newrequest.endtime = endtime
            newrequest.courseid = course.first()
            newrequest.save()
        except Exception as e:
            traceback.print_exc()

        return redirect('/course/start')
