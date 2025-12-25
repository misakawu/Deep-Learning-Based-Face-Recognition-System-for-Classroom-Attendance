import json
import traceback

from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import redirect

from .. import models
from ..views import faceRecSys


def delete(request):
    curID = cache.get('LoginID')
    if curID is None or curID != 1:
        return redirect('/login')

    id = json.loads(request.body).get('stuid', None)

    emp = models.StuInfo.objects.filter(stuid=id)
    if id is None or len(emp) == 0:
        return JsonResponse({'err': '编号错误，请重新删除'})

    try:
        faceRecSys.deleteOneFace(emp.first().stuid)
        emp.delete()
        return JsonResponse({'succ': '删除成功'})
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({'err': e})
