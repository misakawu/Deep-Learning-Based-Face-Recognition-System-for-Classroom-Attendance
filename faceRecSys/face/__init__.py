import traceback

from .mtcnn import Detector
from .mtcnn import draw_bboxes
from .mtcnn import get_max_boxes
from .mtcnn.utils import multiple_draw_bboxes
from .utils import *
from .facenet import FaceExtractor
import matplotlib.pyplot as plt
import os
import cv2
import numpy as np
from PIL import Image


class FaceSystem:
    def __init__(self):
        self.face_detector = Detector()
        self.face_extractor = FaceExtractor()

    def face_detect(self, image):
        """
        predict the locations of faces in the image
        """
        boxes, landmarks = self.face_detector.detect_faces(image)
        return boxes

    def save_faces(self, image, boxes, save_path='D:\\GraduationProject\\Djangotest\\faceRecSys\\images'):
        image = np.array(image)
        for i in range(len(boxes)):
            box = boxes[i]
            x1, y1, x2, y2 = int(box[0]), int(box[1]), int(box[2]), int(box[3])
            face = image[y1: y2, x1: x2, :]
            try:
                face = cv2.cvtColor(face, cv2.COLOR_RGB2BGR)
                path = os.path.join(save_path, "face_" + str(i) + ".jpg")
                result = cv2.imwrite(path, face)
                print('[face_save] ' + str(result))
            except Exception as e:
                traceback.print_exc()
        return len(boxes)

    def multiple_save_faces(self, image, mul_boxes, save_path='D:\\GraduationProject\\Djangotest\\faceRecSys\\images'):
        image = np.array(image)
        i = 0
        for boxes in mul_boxes:
            for box in boxes:
                x1, y1, x2, y2 = int(box[0]), int(box[1]), int(box[2]), int(box[3])
                face = image[y1: y2, x1: x2, :]
                try:
                    face = cv2.cvtColor(face, cv2.COLOR_RGB2BGR)
                    path = os.path.join(save_path, "face_" + str(i) + ".jpg")
                    result = cv2.imwrite(path, face)
                    i = i + 1
                    print('[face_save] ' + str(result))
                except Exception as e:
                    traceback.print_exc()
        return i

    def show_face_boxes(self, image, boxes):
        """
        draw face boxes on the image
        """
        result = draw_bboxes(image, boxes)
        show_image(result)

    def video_face_reg(self, cam_id=0):
        cap = cv2.VideoCapture(cam_id, cv2.CAP_DSHOW)
        faceNum = 0
        try:
            while True:
                ret, image = cap.read()
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # 将BGR转换为RGB
                image = Image.fromarray(image)
                multiple_faces = []
                for i in range(2):
                    try:
                        faces = self.face_detect(image)
                        multiple_faces.append(faces)
                    except Exception:
                        pass
                if len(multiple_faces) != 0:
                    image = multiple_draw_bboxes(image, multiple_faces)
                image = np.array(image)
                image = image.astype(np.uint8)

                # 在图像上绘制文本
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(image, 'press 1 to continue, press 2 to quit'
                            , (10, 30), font, 1, (0, 255, 0), 2, cv2.LINE_AA)

                cv2.namedWindow('face', 0)
                cv2.resizeWindow('face', 1280, 720)
                cv2.moveWindow('face', 0, 0)
                cv2.imshow("face", cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
                key = cv2.waitKey(100)
                if key == ord('1'):
                    faceNum = self.multiple_save_faces(image, multiple_faces)
                    break
                elif key == ord('2'):
                    break

            cv2.destroyAllWindows()
            cap.release()
            return faceNum
        except Exception as e:
            traceback.print_exc()
            cv2.destroyAllWindows()
            cap.release()
            print('[video_face_reg]:' + str(e))
            return 0

    def get_face_feature(self, face):
        feature = self.face_extractor.extractor(face)
        return feature

    def feature_compare(self, feature1, feature2):
        dist = np.sqrt(np.sum(np.square(np.abs(feature1 - feature2))))
        return dist

    def local_face_reg(self, path):
        image = Image.open(path)
        faces = self.face_detect(image)
        return self.save_faces(image, faces)
