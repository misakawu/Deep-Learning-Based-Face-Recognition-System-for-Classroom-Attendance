import json
import tkinter as tk
from tkinter import filedialog

from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import redirect

from app.views import faceRecSys
from app.views import lock


def addface(request):
    curID = cache.get('LoginID')
    if curID is None:
        return redirect('/login')

    if request.method == 'POST':
        data = json.loads(request.body)
        stuid = data['stuid']
        local = data['local']

        if local:
            lock.acquire()
            root = tk.Tk()
            root.withdraw()
            root.call('wm', 'attributes', '.', '-topmost', True)
            f_path = filedialog.askopenfilename()
            root.destroy()
            lock.release()

            if f_path == '':
                return JsonResponse({'err': '未选中文件'})
            result = faceRecSys.insertOneFaceByLocal(stuid, f_path)

        else:
            result = faceRecSys.insertOneFace(stuid)
        return JsonResponse(result)
