from django.core.cache import cache
from django.shortcuts import render, redirect

from .. import models


def welcome(request):
    curID = cache.get('LoginID')
    if curID is None:
        return redirect('/login')
    elif curID == 1:
        return render(request, 'welcome.html')
    else:
        stuID = cache.get('StuID')
        if stuID is None:
            return render(request, 'welcomestu.html')
        else:
            info = models.StuInfo.objects.filter(stuid=stuID).first()
            return render(request, 'welcomestu.html', {'info': info})