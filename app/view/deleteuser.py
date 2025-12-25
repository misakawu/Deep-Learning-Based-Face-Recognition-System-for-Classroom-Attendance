import json
import traceback

from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import render, redirect

from .. import models
from ..views import faceRecSys


def deleteuser(request):
    curID = cache.get('LoginID')
    if curID is None or curID != 1:
        return redirect('/login')

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # print(data)
            models.UserInfo.objects.filter(UserId=data['userid']).delete()
            return JsonResponse({'succ':'删除完成'})
        except Exception as e:
            traceback.print_exc()
            return JsonResponse({'err': e})
