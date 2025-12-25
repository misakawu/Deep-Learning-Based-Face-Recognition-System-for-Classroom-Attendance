from django.core.cache import cache
from django.shortcuts import render, redirect

from .. import models


def info(request):
    curID = cache.get('LoginID')
    if curID is None:
        return redirect('/login')

    info = models.StuInfo.objects.all()
    # print(info)
    return render(request, 'info.html', {"info": info})
