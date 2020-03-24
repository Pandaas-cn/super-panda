import pymysql
import requests
import mysql.connector
import datetime
import time
from cqhttp import CQHttp, Error
from flask import Flask, render_template, request, redirect,send_file,send_from_directory,make_response
from flask import session
app = Flask(__name__, static_folder='C:\\Python_web\\Student_Check\\static',
            template_folder='C:\\Python_web\\Student_Check\\templates')
app.config['SECRET_KEY'] = '6676'
app.secret_key = '6676'
#app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root:root@localhost/stu_check"
conn = pymysql.connect('localhost','root','root','stu_check',charset='utf8mb4')
#con = mysql.connector.connect(host = "127.0.0.1",user = "root",password = "root", database = "stu_check"，charset = 'utf8mb4')

bad_guys = []

def sendqq():
    bot = CQHttp(api_root='http://your ip ')
    groupid = 1007326881 #1808A
    userid=1225753951
    message = '[自动提醒]\n'+'辅导员\老师 已开启签到，请同学们80秒之内打开下方链接进行签到！如打不开请多刷新几次\nhttp://pandaas.cn:1808/'
    qqmessage_url = f'http://your ip /send_private_msg?user_id={userid}&message={message}'
    # qqmessage_url = f'http://your ip /send_group_msg?group_id={groupid}&message={message}'
    res = requests.get(qqmessage_url)
    return res.json()

def sendqq2(v1,v2,v3):
    bot = CQHttp(api_root='http://your ip ')
    groupid = 1007326881 #1808A
    userid=1225753951
    message = '[自动提醒]\n'+'签到已经结束，'+'未签到人数:' + str(v1) + '\n未签到名单\n' + str(v2) + '\n作弊名单\n' + str(v3)
    qqmessage_url = f'http://your ip /send_private_msg?user_id={userid}&message={message}'
    # qqmessage_url = f'http://your ip /send_group_msg?group_id={groupid}&message={message}'
    res = requests.get(qqmessage_url)
    return res.json()

def submit_sql(sql,*args):
    cur = conn.cursor()
    try:
        conn.ping(reconnect=True)
        cur.execute(sql,args)
        conn.commit()
    except Exception as err:
        print('mysql发生错误',err)
        conn.rollback()
    else:
        ret = cur.fetchall()
        cur.close()
        return ret
    raise Exception('Mysql发生错误')

app = Flask(__name__)
app.config['SECRET_KEY'] = '6676'
app.secret_key = '6676'

NAMELIST = ['高艺铭','王昆仑','刘书言','陈佳宁','魏文超','夏迪','武鑫','王一博','赵自乾','曹晋鸣','李涛','王颢然','姜雪莲','党磊','段旭航','耿铭泽','宫玉','黄苗苗','史天宇','王银庆','李金磊','张佳正','张莹莹','李子豪','纪明扬','张玉丰','牛牧原','蔺奕雯','刘琢','贾鹏桥','高宇翔','苏科铭','陈姝婕','马志成','夏振钧','姚京奥','张浩然','胡晨曦','杨鹏','樊小刚','杨小毛','王子龙','赵培廷','张哲','张银龙','魏风顺','马飞凡','尚子晗','许晓波','左耀童','张晓亮','杨智博','周紫阳','刘国成','胡子瑜','盛萌龙','宋贺庆','赵金鹏','杨小龙']
checked_num = []
checked_name = []
server_start = False
check_start = False
start_time = ''
@app.route('/start_check',methods=("GET","POST"))
def start_check():
    global server_start
    global check_start
    global start_time
    if request.method == 'POST':
        password = request.form.get('pwd')
        if password == '1201':
            notcheck_name = {}
            checked_num.clear()
            checked_name.clear()
            notcheck_name.clear()
            bad_guys.clear()
            server_start = True
            sql = 'TRUNCATE TABLE info'
            submit_sql(sql)
            start_time = time.time()
            check_start = True
            sendqq()
            time.sleep(80)
            for i in checked_num:
                checked_name.append(NAMELIST[i - 1])
            notcheck_name = set(NAMELIST).difference(set(checked_name))
            server_start = False
            sql = 'SELECT DISTINCT name FROM info WHERE ip in (SELECT ip FROM info GROUP BY ip HAVING count(*) > 1) or session in (SELECT session FROM info GROUP BY session HAVING count(*) > 1) ;'
            res = submit_sql(sql)
            notcheck_num = len(notcheck_name)
            check_start = False
            sendqq2(notcheck_num,notcheck_name,res)
            return '签到结束-请在QQ查看结果'
    # if request.method =='GET':
    #     if start_time =='':
    #         return '还未开始签到'
    #     if time.time() - start_time >= 60:
            # return '未签到人数:' + str(notcheck_num) + '<br>未签到名单<br>' + str(notcheck_name) + '<br>作弊名单<br>' + str(res)
        # else:
        #     return '正在签到中\....请等待'

@app.route('/',methods=("GET","POST"))
def index():
    if not server_start:
        return render_template('false.html')
    ip = request.remote_addr
    if request.method =="GET":
        return render_template('all_student.html')
    elif request.method =="POST":
        stu_num = int(request.form.get('stu_name'))
        if stu_num in checked_num:
            return render_template('false2.html')
        sess_name = session.get('uid')
        if sess_name == None:
            session.permanent = True
            app.permanent_session_lifetime = datetime.timedelta(seconds=80)
            session['uid'] = stu_num
            sql = 'INSERT INTO info(name,ip,session) VALUES (%s,%s,%s)'
            submit_sql(sql, NAMELIST[stu_num - 1], ip,stu_num)
            checked_num.append(stu_num)
            return render_template('sucess.html')
        else:
            sql = 'INSERT INTO info(name,ip,session) VALUES (%s,%s,%s)'
            submit_sql(sql, NAMELIST[stu_num - 1], ip,sess_name)
            checked_num.append(stu_num)
            return render_template('sucess.html')


@app.route('/start',methods=("GET","POST"))
def cheat_check():
    if request.method =='GET':
        return render_template('start_check.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=1808,debug=False)
