'''
选课系统demo
用户：学生、管理员       Users:Student、Admin
功能：选课、增删改查课、查看信息等   Function: Select courses, add, delete, change, check information,etc
'''
import sys      #   用于 退出选课系统 exit方法
import pymysql
import hashlib
import time #用于判断时间是否合法
conn = pymysql.connect('localhost','root','123','LessonSystem') #链接数据库


class Student():
    def __init__(self,name):
        self.name = name
        print('Welcome Student')
        self.Menu()
    def Menu(self):
        self.functions = ['AlterLesson', 'Exit', 'SelectLesson', 'ShowLessons',]
        print('What do you Want?')
        for index,opt in enumerate(self.functions,1):
            print(index,opt)
        choiceNum = input('Input the order number')
        getattr(self,self.functions[int(choiceNum)-1])()
    def SelectLesson(self):
        lesson = input('The lesson you want select')
        sql = 'SELECT lessons FROM student WHERE name = %s'
        res = SubmitSql(sql,self.name)
        if res:
            selectlessons = res[-1]
            if lesson in selectlessons:
                print('You alreary select this lesson')
                self.Menu()
            else:
                selectlessons = selectlessons + ',' + lesson
            sql = 'UPDATE student SET lessons = %s WHERE name = %s'
            SubmitSql(sql,selectlessons,self.name)
            print('Select Sucess')

        else:
            sql = 'INSERT INTO student(name,lessons) VALUES (%s,%s)'
            SubmitSql(sql,self.name,lesson)
            print('Select Sucess')
    def ShowLessons(self):
        sql = 'SELECT lessons FROM student WHERE name = %s'
        ret = SubmitSql(sql,self.name)
        print('The lesson you selected',ret)
        self.Menu()
    def AlterLesson(self):
        pass
    def Exit(self):
        print('Are you sure to exit?')
        check = input('Y/N?:').upper()
        if check == 'Y':
            print('Good Bye')
            sys.exit()
        else:
            print('You cancled')


class Admin():
    def __init__(self,name):
        self.name = name
        print('Welcome Admin')
        self.Menu()
    def Menu(self):
        self.functions = ['CreateAccount','RemoveAccount','AddLessons','AlterLessons','DelteLessons'
                          ,'ViewDetails','Exit']
        print('What do you Want?')
        for index,opt in enumerate(self.functions,1):
            print(index,opt)
        choiceNum = input('Input the order number')
        getattr(self,self.functions[int(choiceNum)-1])()
    def CreateAccount(self):
        UserType = 'student'    #Default create student
        username = input('name:')
        password = input('password:(default:123)')
        if not password:
            password = GetMd5('123')
        else:
            password = GetMd5(password)
        sql = 'SELECT * FROM userinfo WHERE name = %s'  #检查用户名是否已被使用
        res = SubmitSql(sql,username)
        if res:
            print('此用户名已被使用-请更换')
        else:
            sql = 'INSERT INTO userinfo(name,password,type) VALUES (%s,%s,%s)'
            res = SubmitSql(sql,username,password,UserType)
    def RemoveAccount(self):
        username = input('The username you want remove:')
        sql = 'SELECT * FROM userinfo WHERE name = %s'  #检查用户名是否存在
        res = SubmitSql(sql,username)
        if res:
            print('Are you sure to delete?')
            check = input('Y/N?:').upper()
            if check == 'Y':
                sql= 'DELETE FROM userinfo WHERE name = %s'
                SubmitSql(sql,username)
                print('Delete Sucessful')
            else:
                print('You cancled')
        else:
            print('Not found this user')
    def AddLessons(self):
        Lessonname = input('Lesson name:')
        Teachername = input('Teacher name:')
        Startdate = input('Start date(Format like: 20200321)')
        try:
            check = time.strptime(Startdate,'%Y%m%d')
        except:
            print('Start date fomat not correct')
            return
        sql = 'SELECT * FROM lessons WHERE name = %s'
        res = SubmitSql(sql,Lessonname)
        if res:
            print('The lesson is alreay exists')
        else:
            sql = 'INSERT INTO lessons(name,tea_name,ldate) VALUES(%s,%s,%s)'
            res = SubmitSql(sql,Lessonname,Teachername,Startdate)
            print('Add sucessful')
    def AlterLessons(self):
        pass
    def DelteLessons(self):
        pass
    def ViewDetails(self):
        pass
    def Exit(self):
        print('Are you sure to exit?')
        check = input('Y/N?:').upper()
        if check == 'Y':
            print('Good Bye')
            sys.exit()
        else:
            print('You cancled')

def GetMd5(value):
    md5 = hashlib.md5()
    value = value.encode('utf-8')
    md5.update(value)
    res = md5.hexdigest()
    return res

def SubmitSql(sql,*args):
    cur = conn.cursor()
    try:
        cur.execute(sql,args)
        conn.commit()
    except Exception as err:
        print(err)
        conn.rollback()
    else:
        ret = cur.fetchone()
        cur.close()
        return ret
    raise Exception('Mysql发生错误')
def Login(username,password):
    password = GetMd5(password)
    sql = 'SELECT * FROM userinfo WHERE name = %s AND password = %s'
    res = SubmitSql(sql,username,password)
    if not res:
        print('登陆失败-用户名或密码错误')
    else:
        username = res[1].title()
        usertype = res[-1].title()
        print(f'登录成功,欢迎您:{username}，您的身份为：{usertype}')
        user = getattr(sys.modules[__name__],usertype)(username)    #通过反射方法 进行初始化类

def Menu():
    print('欢迎使用学生选课系统'.center(20, '-'))
    username = input('请先登录输入用户名:')
    password = input('输入密码:')
    Login(username,password)

if __name__ == '__main__':
    # temp = 'admin'
    # print(GetMd5(temp))
    Menu()
    # print(dir(Student))
    conn.close()
















