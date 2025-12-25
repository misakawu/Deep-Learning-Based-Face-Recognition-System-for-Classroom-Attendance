from ..face import FaceSystem
from PIL import Image
import os
from databaseManager import databaseManager
from faceInfo import faceInfo
import json


# import matplotlib.pyplot as plt

def walk_through_directory(directory, fs, manager):
    for dirpath, dirnames, filenames in os.walk(directory):
        # dirpath 是一个字符串，表示当前正在遍历的文件夹的路径
        # dirnames 是一个列表，包含了当前文件夹中的所有子目录的名字
        # filenames 是一个列表，包含了当前文件夹中的所有非目录文件的名字
        if len(filenames) != 0:
            name = str(dirpath).split('\\')[-1]
            dir = 'D:\\GraduationProject\\lfw\\' + name + '\\\\' + filenames[0]
            image = Image.open(dir)

            result = fs.face_detect(image)
            # fs.show_face_boxes(image, result)
            fs.save_faces(image, result)

            face1 = Image.open('.\\images\\face_0.jpg')
            feature = fs.get_face_feature(face1)
            faceData = faceInfo(name, feature)

            manager.insertOneFace(faceData)


def compareFeature(fs, datas, img):
    minResult = 10
    resultName = ''
    result = fs.face_detect(img)
    fs.save_faces(img, result)

    for i in range(len(result)):
        faceImg = Image.open(
            'D:\\GraduationProject\\faceRecSys\\images\\face_' + str(i) + '.jpg')
        imsFeature = fs.get_face_feature(faceImg)

        for data in datas:
            databaseFeature = json.loads(data[2])
            cmpResult = fs.feature_compare(databaseFeature, imsFeature)
            if minResult > cmpResult:
                minResult = cmpResult
                resultName = data[1]
            print(data[1] + ' ' + str(cmpResult))
    print(resultName)


# fs = FaceSystem()
manager = databaseManager()
print(manager.selectByName('Aaron_Guiel'))
# datas = manager.getAllData()
# img = Image.open("D:\\GraduationProject\\lfw\\Adam_Sandler\\Adam_Sandler_0003.jpg")
# compareFeature(fs, datas, img)

# walk_through_directory("D:\GraduationProject\lfw",fs,manager)
