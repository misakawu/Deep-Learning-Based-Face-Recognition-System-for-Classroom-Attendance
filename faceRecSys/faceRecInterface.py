# from ..face import *

import json

from faceRecSys.database.databaseManager import *
from faceRecSys.database.faceInfo import faceInfo
from faceRecSys.face import *


class faceRecInterface:
    def __init__(self, conn):
        self.fs = FaceSystem()
        self.manager = databaseManager(conn)

    def getAndCheckFace(self):
        """
        使用本地摄像头，返回检测到的人脸名称列表
        return
        """
        resultList = []
        try:
            faceNum = self.fs.video_face_reg()
            datas = self.manager.getAllData()
            # print(len(datas))
            if faceNum != 0:
                for i in range(faceNum):
                    img = Image.open('D:\\GraduationProject\\Djangotest\\faceRecSys\\images\\face_' + str(i) + '.jpg')
                    feature = self.fs.get_face_feature(img)

                    minResult = 10
                    resultName = ''
                    for data in datas:
                        databaseFeature = json.loads(data[2])
                        cmpResult = self.fs.feature_compare(databaseFeature, feature)
                        # print(data[1] + ' ' + str(cmpResult), end='|')
                        if cmpResult < 1 and cmpResult < minResult:
                            minResult = cmpResult
                            resultName = data[1]
                    # print('')
                    resultList.append(resultName)

            return resultList
        except Exception as e:
            print(e)
            return resultList

    def insertOneFace(self, name):
        """
        使用摄像头插入一个人脸，需要保证摄像头内仅一人
        :param name: 需要插入的人脸名称
        :return: (dir)成功或错误信息
        """
        if len(self.manager.selectByName(name)) == 0:
            faceNum = self.fs.video_face_reg()
            if faceNum != 0:
                img = Image.open('D:\\GraduationProject\\Djangotest\\faceRecSys\\images\\face_0.jpg')
                feature = self.fs.get_face_feature(img)
                data = faceInfo(name, feature)
                if self.manager.insertOneFace(data):
                    return {"succ": "数据添加成功"}
                else:
                    return {'err': '人脸插入失败'}
            else:
                return {"err": "未检测到有效人脸"}
        else:
            print(name + ' already exit')
            return {'err': name + "已存在"}

    def insertOneFaceByLocal(self, name, f_path):
        """
        使用本地图片插入一个人脸
        :param name: 需要插入的人脸名称
        :param f_path: 人脸图片路径
        :return: (dir)成功或错误信息
        """
        if len(self.manager.selectByName(name)) == 0:
            if f_path is not None:
                faceNum = self.fs.local_face_reg(f_path)
                if faceNum != 0:
                    img = Image.open('D:\\GraduationProject\\Djangotest\\faceRecSys\\images\\face_0.jpg')
                    feature = self.fs.get_face_feature(img)
                    data = faceInfo(name, feature)
                    if self.manager.insertOneFace(data):
                        return {"succ": "人脸添加成功"}
                    else:
                        return {'err': '人脸插入失败'}
                else:
                    return {"err": "未检测到有效人脸"}
            else:
                return {'err': '未选中文件'}
        else:
            print(name + '已存在')
            return {'err': name + "已存在"}

    def updateOneFace(self, name):
        """
        使用摄像头更新一个人脸，需要保证摄像头内仅一人
        :param name: 需要更新的人脸名称
        :return: (bool)成功或错误信息
        """
        if len(self.manager.selectByName(name)) != 0:
            faceNum = self.fs.video_face_reg()
            if faceNum != 0:
                img = Image.open('D:\\GraduationProject\\Djangotest\\faceRecSys\\images\\face_0.jpg')
                feature = self.fs.get_face_feature(img)
                data = faceInfo(name, feature)
                self.manager.deleteByName(name)
                self.manager.insertOneFace(data)
            return True
        else:
            print(name + ' not exit')
            return False

    def updateOneFaceLocally(self, name, dir):
        """
        使用本地图片更新一个人脸
        :param name: 需要更新的人脸名称
        :param dir: 人脸图片路径
        :return: (dir)成功或错误信息
        """
        if len(self.manager.selectByName(name)) != 0:
            faceNum = self.fs.local_face_reg(dir)
            if faceNum != 0:
                img = Image.open('D:\\GraduationProject\\Djangotest\\faceRecSys\\images\\face_0.jpg')
                feature = self.fs.get_face_feature(img)
                data = faceInfo(name, feature)
                self.manager.deleteByName(name)
                self.manager.insertOneFace(data)
            return {'succ': name + ' 人脸数据更新完成'}
        else:
            print(name + ' not exit')
            return {'err': name + ' 人脸数据更新失败'}

    def deleteOneFace(self, name):
        """
        删除一个人脸
        :param name: 需要删除的人脸名称
        :return: (bool)成功或错误信息
        """
        if len(self.manager.selectByName(name)) != 0:
            try:
                self.manager.deleteByName(name)
                return True
            except Exception as e:
                print(e)
                return False
        else:
            print(name + ' not exit')
            return False

    def updateName(self, oldname, newname):
        """
        更新人脸名称
        :param oldname: 旧人脸名称
        :param newname: 新人脸名称
        :return: (bool)成功或错误信息
        """
        try:
            if self.manager.updateName(oldname, newname) != 0:
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return False


if __name__ == '__main__':
    conn = sqlite3.connect('faceFeature.db', check_same_thread=False)
    fs = faceRecInterface(conn)
