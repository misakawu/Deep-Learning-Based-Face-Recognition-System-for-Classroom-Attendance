import sqlite3
import threading

from faceRecSys.faceRecInterface import faceRecInterface


conn = sqlite3.connect('D:\\GraduationProject\\Djangotest\\faceRecSys\\faceFeature.db', check_same_thread=False)
faceRecSys = faceRecInterface(conn)
lock = threading.Lock()
