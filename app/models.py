from django.db import models


# 创建用户类
class UserInfo(models.Model):
    UserId = models.AutoField(primary_key=True)
    username = models.CharField(max_length=16, blank=False, verbose_name="用户名", unique=True)
    password = models.CharField(max_length=16, blank=False, verbose_name="密码")


# 创建学生信息类
class StuInfo(models.Model):
    id = models.AutoField(primary_key=True)
    stuname = models.CharField(max_length=32, verbose_name="学生姓名")
    stuid = models.CharField(max_length=16, verbose_name="学生学号", unique=True)


class CourseInfo(models.Model):
    id = models.AutoField(primary_key=True)
    coursename = models.CharField(max_length=16, verbose_name="课程名")
    starttime = models.TimeField(auto_now=False, auto_now_add=False, verbose_name="课程开始时间")
    endtime = models.TimeField(auto_now=False, auto_now_add=False, verbose_name="课程结束时间")
    weekday = models.IntegerField(verbose_name="课程设置日期")


class CourseSelect(models.Model):
    id = models.AutoField(primary_key=True)
    stuid = models.ForeignKey(StuInfo, on_delete=models.CASCADE, null=False, verbose_name="选课学生")
    courseid = models.ForeignKey(CourseInfo, on_delete=models.CASCADE, null=False, verbose_name="课程")


class AttendRequest(models.Model):
    id = models.AutoField(primary_key=True)
    courseid = models.ForeignKey(CourseInfo, on_delete=models.CASCADE, null=False, verbose_name="课程")
    starttime = models.DateTimeField(auto_now=False, auto_now_add=False, verbose_name="考勤开始时间")
    endtime = models.DateTimeField(auto_now=False, auto_now_add=False, verbose_name="考勤结束时间")


class AttendenceLog(models.Model):
    id = models.AutoField(primary_key=True)
    stuid = models.ForeignKey(StuInfo, on_delete=models.CASCADE, null=False, verbose_name="学生")
    requestid = models.ForeignKey(AttendRequest, on_delete=models.CASCADE, null=False, verbose_name="课程")
    attendtime = models.DateTimeField(auto_now=False, auto_now_add=False, verbose_name="考勤时间")


class UserStudentLink(models.Model):
    id = models.AutoField(primary_key=True)
    stuid = models.ForeignKey(StuInfo, on_delete=models.CASCADE, null=False, verbose_name="学生id")
    userid = models.ForeignKey(UserInfo, on_delete=models.CASCADE, null=False, verbose_name="用户id")
