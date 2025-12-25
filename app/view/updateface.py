import json
import tkinter as tk
from tkinter import filedialog

from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import redirect

from .. import models
from ..views import faceRecSys


def updateface(request):
    curID = cache.get('LoginID')
    if curID is None:
        return redirect('/login')
    data = json.loads(request.body)
    updateid = data.get('id', None)
    stu = models.StuInfo.objects.filter(id=updateid)
    if stu.count() == 0:
        return JsonResponse({'err': '编号错误，不存在该学生'})

    local = data.get('local')
    if not local:
        if faceRecSys.updateOneFace(stu.first().stuid):
            return JsonResponse({'succ': stu.first().stuname + ' 人脸信息修改成功！'})
        else:
            return JsonResponse({'err': stu.first().stuname + ' 人脸信息修改失败！'})
    else:
        global lock
        lock.acquire()
        root = tk.Tk()
        root.withdraw()
        root.call('wm', 'attributes', '.', '-topmost', True)
        f_path = filedialog.askopenfilename(title="Select Face Picture", filetypes=[('Picture', '.jpg .jpeg .png')])
        root.destroy()
        lock.release()

        if f_path == '':
            return JsonResponse({'err': '未选中文件'})

        result = faceRecSys.updateOneFaceLocally(stu.first().stuid, f_path)
        return JsonResponse(result)
