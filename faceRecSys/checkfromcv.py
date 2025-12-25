from face import *
from PIL import Image
# import matplotlib.pyplot as plt
from database.databaseManager import databaseManager
import json
import os


def getAndCheckFace(fs, manager):
    faceNum = fs.video_face_reg()
    if faceNum != 0:
        for i in range(faceNum):
            img = Image.open('D:\\GraduationProject\\faceRecSys\\images\\face_' + str(i) + '.jpg')
            feature = fs.get_face_feature(img)
            datas = manager.getAllData()
            minResult = 10
            resultName = ''
            for data in datas:
                databaseFeature = json.loads(data[2])
                cmpResult = fs.feature_compare(databaseFeature, feature)
                if minResult > cmpResult:
                    minResult = cmpResult
                    resultName = data[1]
                # print(data[1] + ' ' + str(cmpResult))
            print(resultName)


fs = FaceSystem()
manager = databaseManager()
getAndCheckFace(fs, manager)
