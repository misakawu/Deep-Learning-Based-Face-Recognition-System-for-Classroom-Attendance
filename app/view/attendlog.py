import json
import traceback

from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import render, redirect

from .. import models


def attendlog(request):
    """
    :url /course/log
    :method 处理查看某次课程考勤的所有考勤记录
    """
    curID = cache.get('LoginID')
    if curID is None or curID != 1:
        return redirect('/login')
    data = json.loads(request.body)
    requestid = data['requestid']

    try:
        logs = models.AttendenceLog.objects.values('id',
                                                   'requestid__courseid__coursename',
                                                   'stuid__stuname',
                                                   'attendtime').filter(requestid_id=requestid)
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({'err': e})
    logs = list(logs)
    # print(logs)
    return JsonResponse({'succ': True, 'logs': logs})
