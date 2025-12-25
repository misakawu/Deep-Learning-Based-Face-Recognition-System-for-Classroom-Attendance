import sqlite3
import traceback

from faceRecSys.database.faceInfo import faceInfo


class databaseManager:
    def __init__(self):
        try:
            # 连接到SQLite数据库文件，如果不存在则创建它
            self.conn = sqlite3.connect('../faceFeature.db', check_same_thread=False)
            # 创建一个游标对象
            self.cursor = self.conn.cursor()
            self.cursor.execute('SELECT name FROM sqlite_master WHERE type="table";')
            tables = self.cursor.fetchall()
            print("Tables in database:", tables)
        except sqlite3.Error as e:
            print('facesys 数据库错误')
            traceback.print_exc()

    def __init__(self, conn):
        self.conn = conn
        self.cursor = self.conn.cursor()
        self.cursor.execute('SELECT name FROM sqlite_master WHERE type="table";')
        tables = self.cursor.fetchall()
        print("Tables in database:", tables)

    def __del__(self):
        self.cursor.close()
        self.conn.close()

    def getAllData(self):
        try:
            self.cursor.execute("SELECT * FROM faces")
            self.conn.commit()
            result = self.cursor.fetchall()
            return result

        except sqlite3.Error as e:
            print('facesys 数据库Select错误')
            traceback.print_exc()
            self.conn.rollback()  # 如果出现错误，回滚事务

    def getPageData(self, start=0, page=100):
        try:
            self.cursor.execute("SELECT * FROM faces LIMIT ? OFFSET ?", (page, start))
            self.conn.commit()
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print('facesys 数据库Select错误')
            traceback.print_exc()
            self.conn.rollback()  # 如果出现错误，回滚事务

    def insertOneFace(self, face):
        try:
            self.cursor.execute("INSERT INTO faces (name,feature) values (?,?)", face.getInfo())
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print('facesys 数据库Insert错误')
            traceback.print_exc()
            self.conn.rollback()  # 如果出现错误，回滚事务
            return False

    def selectByName(self, name):
        try:
            self.cursor.execute("SELECT * FROM faces WHERE name='" + str(name) + "'")
            self.conn.commit()
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print('facesys 数据库Select错误')
            traceback.print_exc()
            self.conn.rollback()  # 如果出现错误，回滚事务

    def deleteByName(self, name):
        try:
            self.cursor.execute("DELETE FROM faces WHERE name='" + str(name) + "'")
            self.conn.commit()
            return self.cursor.rowcount
        except sqlite3.Error as e:
            print('facesys 数据库Delete错误')
            traceback.print_exc()
            self.conn.rollback()  # 如果出现错误，回滚事务

    def updateName(self, oldname, newname):
        try:
            self.cursor.execute("UPDATE faces SET name='"+str(newname)+"' WHERE name= '" + str(oldname) + "'")
            self.conn.commit()
            return self.cursor.rowcount
        except sqlite3.Error as e:
            print('facesys 数据库Update错误')
            traceback.print_exc()
            self.conn.rollback()  # 如果出现错误，回滚事务


if __name__ == '__main__':
    manager = databaseManager()
    data = manager.getAllData()
    # print(data)
