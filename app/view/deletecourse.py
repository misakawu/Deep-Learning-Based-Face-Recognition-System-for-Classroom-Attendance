import json
import traceback

from django.core.cache import cache
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from .. import models


def coursedel(request):
    curID = cache.get('LoginID')
    if curID is None or curID != 1:
        return redirect('/login')

    try:
        delid = json.loads(request.body).get('id')
        data = models.CourseInfo.objects.filter(id=delid)
        # print(delid, data)
        if data.count() == 0:
            return JsonResponse({'err': '不存在该课程'})
        else:
            data.delete()
            return JsonResponse({'succ':'删除成功'})
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({'err': e})
