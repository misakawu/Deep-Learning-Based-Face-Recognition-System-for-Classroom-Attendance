~~# FaceRecognition-System

## 简介

本项目为一个完整的人脸识别系统，该系统提供了如下功能：

1. 人脸识别
2. 人脸特征提取
3. 人脸对比

## 使用

### 环境

如需独立安装：

```
pip install -r requirement.txt
```

### 下载权重

链接: [链接: https://pan.baidu.com/s/1Kol-FSGFv2_Hl6qIrrzgiA?pwd=1234 提取码: 1234](https://pan.baidu.com/s/1Kol-FSGFv2_Hl6qIrrzgiA?pwd=1234)

将权重放到 /face/facenet/weights 文件夹下


## 算法介绍

人脸识别算法使用了MTCNN算法，人脸特征提取算法使用了FaceNet算法；

MTCNN算法**采用级联CNN结构，通过多任务学习，同时完成了两个任务——人脸检测和人脸对齐，输出人脸的Bounding Box以及人脸的关键点（眼睛、鼻子、嘴）位置**

FaceNet算法**直接学习图像到欧式空间上点的映射，两张图像所对应的特征的欧式空间上的点的距离直接对应着两个图像是否相似**

## API 接口介绍

```python
fs = FaceSystem()
```

```python
# 预测人脸的例子
image = Image.open("./images/1.jpg")
result = fs.face_detect(image)
fs.show_face_boxes(image, result)
```

```python
# 打开摄像头进行识别
fs.video_face_reg()
```

```
# 将人脸切割保存
fs.save_faces(image, result)
```

```python
# 提取人脸特征
face1 = Image.open('./images/face_0.jpg')
feature1 = fs.get_face_feature(face1)
face2 = Image.open('./images/face_1.jpg')
feature2 = fs.get_face_feature(face1)
```

```python
# 人脸特征对比
dist = fs.feature_compare(feature1, feature2)
dist2 = fs.feature_compare(feature1, feature1)
```

## faceRecInterface封装

封装数据库操作和人脸识别接口，方便使用。  
主要功能：
* 初始化：通过传入数据库连接对象 conn 来初始化 FaceSystem 和 databaseManager 对象。
* 人脸识别：从摄像头捕获人脸并与数据库中的人脸特征进行比对，返回识别结果。
* 插入人脸：支持从摄像头或本地图片插入新人脸。
* 更新人脸：支持从摄像头或本地图片更新已有人脸。
* 删除人脸：从数据库中删除指定的人脸。
* 更新人脸名称：更改数据库中的人脸名称。

注意事项：  
* 在使用摄像头功能时，确保摄像头正常工作且摄像头内仅有一人。
* 在使用本地图片功能时，确保提供的图片路径正确且图片中仅有一张人脸。
* 数据库连接对象 conn 需要提前创建并传入 faceRecInterface 类的构造函数中。