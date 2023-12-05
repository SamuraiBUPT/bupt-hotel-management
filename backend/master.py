import inspect
import threading
import pymysql
import json
import os
import time
from queue import Queue
from slave import *
import copy
# import csv
from mysqlTable import *

NORMAL_TEMPERATURE = 25

DATABASE_USER_NAME = "root"
# DATABASE_USER_PASSWORD = "13125188529Wyh10" # change to your own pwd
DATABASE_USER_PASSWORD = "1234"
DATABASE_SCHEMA = "backend" # create a db in your machine(schema), utf8, utf8_bin
DATABASE_USER_PORT = 3306
DATABASE_USER_HOST = "localhost"
lock = threading.Lock()


def trans_roomid_to_id(roomid):
    id = ((int(roomid) - 100) // 100) * 10 + (int(roomid) - 1) % 100
    return id
def trans_id_to_roomid(id):
    roomid = ((id//10)+1)*100 + id % 10 + 1
    return roomid

class Master(Base):
    def __init__(self):
        self.db = pymysql.connect(
            host=DATABASE_USER_HOST,  # 默认用主机名
            port=DATABASE_USER_PORT,
            user=DATABASE_USER_NAME,  # 默认用户名
            password=DATABASE_USER_PASSWORD,  # mysql密码
            database=DATABASE_SCHEMA,  # 库名
            charset='utf8'  # 编码方式
        )
        self.cursor = self.db.cursor()  # 使用 cursor() 方法创建一个游标对象 cursor

        # 建表
        self.cursor.execute(identity_drop)
        self.cursor.execute(identity_create)

        self.cursor.execute(slave_drop)
        self.cursor.execute(slave_create)

        self.cursor.execute(oprecord_drop)
        self.cursor.execute(oprecord_create)

        self.cursor.execute(checkrecord_drop)
        self.cursor.execute(checkrecord_create)

        self.cursor.execute(bill_drop)
        self.cursor.execute(bill_create)
        self.db.commit()

        self.add_identity('admin', 'password', '0')
        self.add_identity('reception', 'password', '1')

        self.power = False
        self.state = 'Standby'
        self.mode = "Cold"
        self.temp = 25
        self.rate = 1   # 费率为一元一度

        self.frequence = 120  # 刷新频率120s
        self.opened_time = 0

        # 直接将各个slave抽象成为master的一个部件
        self.SLAVE_NUM = 40
        # self.slaves = [Slave(str(i), "") for i in range(self.SLAVE_NUM)]
        self.slaves = []
        # for i in range(4):
        #     for j in range(10):
        #         k = (i+1)*100+j+1
        #         self.slaves.append(Slave(str(k), ''))
        #         self.init_slave(self.slaves[-1].__dict__)
        roomid = [101,102,103,104,105,106,107,108,109,110,201,202,203,204,205,206,207,208,209,210,
                301,302,303,304,305,306,307,308,309,310,401,402,403,404,405,406,407,408,409,410]
        for i in range(self.SLAVE_NUM):
            self.slaves.append(Slave(int(roomid[i]), ''))
            self.init_slave(self.slaves[i].__dict__)

        self.slave_init = copy.deepcopy(self.slaves)

        # HTTP请求队列
        self.signals = [threading.Condition() for i in range(self.SLAVE_NUM)]
        self.request_queue = Queue()

        # 调度队列
        self.blowing_list = []  # 送风队列（工作）
        self.schedule_queue = []

        self.socketio = None

    # center_page

    def center_data(self) -> dict:
        center = {}
        center['power'] = self.power
        center['state'] = self.state
        center['mode'] = self.mode
        center['temp'] = self.temp
        center['freq'] = self.frequence
        return center

    # def __del__(self):
    #     self.cursor.close()  # 关闭游标
    #     self.db.close()     # 关闭数据库连接

    # init_room

    def init_slave(self, d: dict):
        try:
            sql = 'insert into slave values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
            self.cursor.execute(sql, (d['id'], d['name'], d['idCard'], d['checkInDate'],
                                      d['cost'], d['expectTemp'], d['speed'], d['temp'], False, '0', False, False))
            self.db.commit()
            # print("insert slave", end=' ')
        except:  # 主键约束
            sql = 'update slave set name=%s, idCard=%s, checkInDate=%s, cost=%s, expectTemp=%s, speed=%s, temp=%s, \
                    power=%s, timer=%s, haveCheckIn=%s, showDetails=%s where id = %s'
            self.cursor.execute(sql, (d['name'], d['idCard'], d['checkInDate'], d['cost'],
                                      d['expectTemp'], d['speed'], d['temp'], False, '0', False, False, d['id']))
            self.db.commit()
            # print("update slave", end=' ')

    # /rooms/路由 all_rooms_info

    def get_all_room(self) -> list:
        rooms = []
        db = pymysql.connect(
            host=DATABASE_USER_HOST,  # 默认用主机名
            port=DATABASE_USER_PORT,
            user=DATABASE_USER_NAME,  # 默认用户名
            password=DATABASE_USER_PASSWORD,  # mysql密码
            database=DATABASE_SCHEMA,  # 库名
            charset='utf8'  # 编码方式
        )  # 打开数据库连接
        cursor = db.cursor()
        lock.acquire()
        cursor.execute("select * from slave")
        lock.release()
        db.commit()
        while 1:
            res = cursor.fetchone()
            if res is None:  # 表示已经取完结果集
                break
            id=trans_roomid_to_id(int(res[0]))
            d = {
                'id': res[0],
                'haveCheckIn': False if res[10] == '0' else True,
                'name': res[1],
                'idCard': res[2],
                'checkInDate': res[3],
                'cost': res[4],
                'expectTemp': res[5],
                'speed': res[6],
                'temp': res[7],
                'power': False if res[8] == '0' else True,
                '_showDetails': False if res[11] == '0' else True,
                'is_blowing_in': self.slaves[id].is_blowing_in
            }
            rooms.append(d)
        cursor.close()
        db.close()
        return rooms

    # 获取当前房间的记录号
    def get_CheckRecord_Record(self, roomId: str):
        # 对于当前房间号，获取其入住状态为1的记录，即入住中的记录
        sql = 'select Record from CheckRecord where id = %s and state =%s'
        lock.acquire()
        self.cursor.execute(sql, (roomId, '1'))
        self.db.commit()
        lock.release()
        rec_no = ''
        if self.cursor is not None:  # 注意这里: 单纯判断cursor是否为None是不够的
            row = self.cursor.fetchone()
            if row is not None:
                rec_no = row[0]

        return rec_no

    # 从控机获取当前房间的状态
    def get_slave_power(self, roomId: str):
        try:  # 如果开始数据库没有数据怎么办...
            sql = 'select power from slave where id = %s'
            lock.acquire()
            self.cursor.execute(sql, (roomId))
            power = self.cursor.fetchone()[0]
            self.db.commit()
            lock.release()
        except Exception as reason:
            power = '0'
            print(reason)
        return power  # 对于当前房间号，获取其从控机的开关机情况

    # 获取当前的入住记录数
    def get_CheckRecord_count(self):
        query = " select count(*) from CheckRecord "
        db = pymysql.connect(
            host=DATABASE_USER_HOST,  # 默认用主机名
            port=DATABASE_USER_PORT,
            user=DATABASE_USER_NAME,  # 默认用户名
            password=DATABASE_USER_PASSWORD,  # mysql密码
            database=DATABASE_SCHEMA,  # 库名
            charset='utf8'  # 编码方式
        )  # 打开数据库连接
        cursor = db.cursor()
        cursor.execute(query)
        count = cursor.fetchone()[0]
        db.commit()
        cursor.close()
        db.close()
        return count

    # 获取操作记录记录数
    def get_OpRecord_count(self):
        query = " select count(*) from OpRecord "
        lock.acquire()
        self.cursor.execute(query)
        count = self.cursor.fetchone()[0]
        self.db.commit()
        lock.release()
        return count

    # 获取送风时间,读出计时器的值
    def get_slave_timer(self, roomId: str):
        sql = 'select timer from slave where id = %s'
        db = pymysql.connect(
            host=DATABASE_USER_HOST,  # 默认用主机名
            port=DATABASE_USER_PORT,
            user=DATABASE_USER_NAME,  # 默认用户名
            password=DATABASE_USER_PASSWORD,  # mysql密码
            database=DATABASE_SCHEMA,  # 库名
            charset='utf8'  # 编码方式
        )  # 打开数据库连接
        cursor = db.cursor()
        cursor.execute(sql, (roomId))
        tim = cursor.fetchone()[0]
        db.commit()
        cursor.close()
        db.close()
        return tim

    # 更新计时器的值
    def update_slave_timer(self, roomId: str, timer: str):
        sql = 'update slave set timer=%s where id = %s'
        lock.acquire()
        self.cursor.execute(sql, (timer, roomId))
        lock.release()
        self.db.commit()

    # 获取风速
    def get_slave_speed(self, roomId: str):
        sql = 'select speed from slave where id = %s'
        db = pymysql.connect(
            host=DATABASE_USER_HOST,  # 默认用主机名
            port=DATABASE_USER_PORT,
            user=DATABASE_USER_NAME,  # 默认用户名
            password=DATABASE_USER_PASSWORD,  # mysql密码
            database=DATABASE_SCHEMA,  # 库名
            charset='utf8'  # 编码方式
        )  # 打开数据库连接
        cursor = db.cursor()
        cursor.execute(sql, (roomId))
        speed = cursor.fetchone()[0]
        db.commit()
        cursor.close()
        db.close()
        return speed

    # 获取新的阶段用电量 = 功率 * 时间
    def cal_power(self, roomId: str, speed: str):
        current_power = 0
        tim = self.get_slave_timer(roomId)
        if speed == 'high':
            current_power = 1 * float(tim) / 60
        if speed == 'medium':
            current_power = 0.5 * float(tim) / 60
        if speed == 'low':
            current_power = (1/3) * float(tim) / 60
        return current_power

    # 获取新的总费用 = 原花费 + 费率 * 功率
    def cal_cost(self, roomId: str, current_power: float):
        # 获取原先费用
        sql = 'select cost from slave where id = %s'

        lock.acquire()
        self.cursor.execute(sql, roomId)
        lock.release()
        cost = self.cursor.fetchone()[0]
        # 获取价钱
        cost = round(float(cost), 2) + self.rate * round(float(current_power), 2)
        return cost

    # 更新某房间的送风量和费用，插入新记录
    # type初始为0；1，开关机；2，设定温度 temp1 -> temp2；3，设定风速 speed1 -> speed2;4，每一分钟的例行更新；
    def update_cost_and_wind(self, roomId: str, typ: str, old: str, new: str):  # time以秒为单位
        speed = ' '
        if typ != '3':
            speed = self.get_slave_speed(roomId)  # 如果不是变更风速就按从原来的风速变化
        else:
            speed = old  # 如果是变更风速，把老风速保留，计算上一阶段的cost
        current_power = self.cal_power(roomId, speed)
        cost = self.cal_cost(roomId, current_power)
        # 对于当前房间号，获取其入住状态为1的记录，即入住中的记录
        rec_no = self.get_CheckRecord_Record(roomId)
        print("this op is oprated by rec_no = %s" % (rec_no))
        now_time = time.strftime('%Y-%m-%d %H:%M:%S ',time.localtime(time.time()))
        # 将slave和oprecord中的cost和wind更新
        # print("roomid = %s  wind=%s cost = %s timer = %s" %(roomId,wind, cost, run_time))
        sql = 'insert into OpRecord(Record,time, type, old, new, wind, cost) values(%s, %s,%s, %s, %s, %s, %s)'

        db = pymysql.connect(
            host=DATABASE_USER_HOST,  # 默认用主机名
            port=DATABASE_USER_PORT,
            user=DATABASE_USER_NAME,  # 默认用户名
            password=DATABASE_USER_PASSWORD,  # mysql密码
            database=DATABASE_SCHEMA,  # 库名
            charset='utf8'  # 编码方式
        )  # 打开数据库连接
        cursor = db.cursor()
        cursor.execute(sql, (rec_no, now_time, typ, old, new, str(round(current_power, 2)), str(round(cost, 2))))
        db.commit()
        cursor.execute("update slave set cost=%s where id=%s", (round(cost, 2), roomId))
        cursor.execute("update bill set cost=%s where roomid=%s", (round(cost, 2), roomId))
        db.commit()
        cursor.close()
        db.close()

    # room checkIn
    def checkIn(self, roomId: str, name: str, idCard: str, date: str, show: bool):
        db = pymysql.connect(
            host=DATABASE_USER_HOST,  # 默认用主机名
            port=DATABASE_USER_PORT,
            user=DATABASE_USER_NAME,  # 默认用户名
            password=DATABASE_USER_PASSWORD,  # mysql密码
            database=DATABASE_SCHEMA,  # 库名
            charset='utf8'  # 编码方式
        )  # 打开数据库连接
        cursor = db.cursor()
        lock.acquire()
        sql = 'update slave set name=%s, idCard=%s, checkInDate=%s, timer=%s, haveCheckIn=%s, showDetails=%s where id = %s'
        cursor.execute(sql, (name, idCard, date, '0', True, show, roomId))
        lock.release()
        db.commit()
        # 入住，check in会增加一次开房记录
        sql = 'insert into CheckRecord(Record,idcard, id, checkInDate, checkOutDate, state) values(%s, %s, %s, %s, %s, %s)'
        sql1 = 'insert into bill( record, roomid,checkInDate, checkOutDate, cost) values(%s, %s, %s, %s, %s)'
        sql2 = 'insert into identity( account,password,identity) values(%s, %s, %s)'
        rec_num = self.get_CheckRecord_count()
        lock.acquire()
        cursor.execute(sql, (rec_num, idCard, roomId, date, 'NULL', '1'))
        cursor.execute(sql1, (rec_num, roomId, date, 'NULL', 'NULL'))
        cursor.execute(sql2, (roomId, idCard, '2'))
        lock.release()
        cursor.close()
        db.commit()
        # 把开房编号赋值给从控机
        id = trans_roomid_to_id(int(roomId))
        self.slaves[id].record = rec_num

    # 离开，把这一次入住记录改为离开
    def checkOut(self, roomId: str, date: str):
        # 查看房间空调状态是否为关机，不是关机就计算费用，插入记录
        sql = 'select power from slave where id = %s'

        lock.acquire()
        self.cursor.execute(sql, roomId)
        lock.release()
        res = self.cursor.fetchone()[0]
        if res != '0':  # 数据库中状态变为关机就计算费用，同时清零原计时，后台运行的线程会停止计时
            self.update_cost_and_wind(roomId, '1', '1', '0')
            sql = 'update slave set power=(not power), showDetails=%s, haveCheckIn = %s where id = %s'
            lock.acquire()
            self.cursor.execute(sql, (False, '0', roomId))
            lock.release()
            self.db.commit()
            self.update_slave_timer(roomId, 0)
        # 对于当前房间号，获取其入住状态为1的记录，即入住中的记录
        id = trans_roomid_to_id(roomId)
        rec_no = self.get_CheckRecord_Record(roomId)
        #print(rec_no)
        # 将这个记录号的状态改为离开
        sql = 'update CheckRecord set checkOutDate=%s, state=%s where Record=%s'
        sql1 = 'update bill set checkOutDate=%s where Record=%s'
        sql2 = 'DELETE FROM identity WHERE account = %s'
        lock.acquire()
        self.cursor.execute(sql, (date, '0', rec_no))
        self.cursor.execute(sql1, (date, rec_no))
        self.cursor.execute(sql2, str(roomId))
        lock.release()
        self.slave_init[id].temp = self.slaves[id].temp
        self.init_slave(self.slave_init[id])
        self.db.commit()

    # 添加人员
    def add_identity(self, account: str, password: str,identity: str) -> bool:
        try:
            sql = 'insert into identity values(%s, %s,%s )'
            lock.acquire()
            self.cursor.execute(sql, (account, password,identity))
            self.db.commit()  # 需要commit才可以提交插入
            lock.release()
        except Exception as reason:
            print("add_identity", reason)
            return False
        return True

    # 管理员登录
    def login(self, account: str, passowrd: str) -> bool:
        sql = "select * from identity where account = %s"
        lock.acquire()
        self.cursor.execute(sql, account)
        res = self.cursor.fetchone()
        lock.release()
        self.db.commit()
        if res == None or res[0] != account or res[1] != passowrd:
            return False
        else:
            return res[2]

    # 获取一个房间信息
    def get_one_room(self, roomId: str) -> dict:
        db = pymysql.connect(
            host=DATABASE_USER_HOST,  # 默认用主机名
            port=DATABASE_USER_PORT,
            user=DATABASE_USER_NAME,  # 默认用户名
            password=DATABASE_USER_PASSWORD,  # mysql密码
            database=DATABASE_SCHEMA,  # 库名
            charset='utf8'  # 编码方式
        ) # 打开数据库连接
        cursor = db.cursor()
        #lock.acquire()
        cursor.execute("select * from slave where id = %s", roomId)
        #lock.release()
        db.commit()
        res = cursor.fetchone()
        id = trans_roomid_to_id(int(res[0]))
        d = {
            'roomid': res[0],
            'name': res[1],
            'idCard': res[2],
            'checkInDate': res[3],
            'cost': res[4],
            'expectTemp': res[5],
            'speed': res[6],
            'temp': res[7],
            'power': False if res[8] == '0' else True,
            'haveCheckIn': False if res[10] == '0' else True,
            '_showDetails': False if res[11] == '0' else True,
            'init_temper': self.slaves[id].init_temper,
            'is_blowing_in': self.slaves[id].is_blowing_in
        }
        cursor.close()
        db.close()
        return d

    # slave/flipPower
    def slaveFilpPower(self, roomId: str):
        db = pymysql.connect(
            host=DATABASE_USER_HOST,  # 默认用主机名
            port=DATABASE_USER_PORT,
            user=DATABASE_USER_NAME,  # 默认用户名
            password=DATABASE_USER_PASSWORD,  # mysql密码
            database=DATABASE_SCHEMA,  # 库名
            charset='utf8'  # 编码方式
        )  # 打开数据库连接
        sql = 'update slave set power=(not power), showDetails=%s where id = %s'
        cursor = db.cursor()
        cursor.execute(sql, (True, roomId))
        db.commit()
        sql = 'select power from slave where id = %s'
        lock.acquire()
        cursor.execute(sql, roomId)
        lock.release()
        res = cursor.fetchone()[0]
        if res == '0':
            # 数据库中状态变为关机就计算费用，同时清零原计时，后台运行的线程会停止计时
            self.update_cost_and_wind(roomId, '1', '1', '0')
            self.update_slave_timer(roomId, 0)
        else:
            # 数据库中状态变为开机开始计算费用，同时后台运行的线程会开始计时
            self.update_cost_and_wind(roomId, '1', '0', '1')
        cursor.close()
        db.close()

    # 设置预期温度
    def ExpectTemSet(self, roomId: str, temp: int):
        self.db.ping(reconnect=True)
        #lock.acquire()
        self.cursor.execute("select expectTemp from slave where id=%s", roomId)
        res = self.cursor.fetchone()[0]
        exp_temp = temp
        self.cursor.execute(
            "update slave set expectTemp=%s, showDetails=%s where id=%s", (str(exp_temp), True, roomId))
        #lock.release()
        self.update_cost_and_wind(roomId, '2', res, exp_temp)
        self.update_slave_timer(roomId, 0)
        self.db.commit()
    # 设置房间初始温度
    def InitTemSet(self, roomId: str, temp: int):
        self.db.ping(reconnect=True)
        lock.acquire()
        self.cursor.execute(
            "update slave set temp=%s, showDetails=%s where id=%s", (str(temp), True, roomId))
        lock.release()
        self.db.commit()
    # 速度变化，送风计时清零，计算上一阶段的费用
    def setSpeed(self, roomId: str, wind: str):
        res = self.get_slave_speed(roomId)
        lock.acquire()
        self.cursor.execute(
            "update slave set speed=%s, showDetails=%s where id=%s", (wind, True, roomId))
        lock.release()
        self.update_cost_and_wind(roomId, '3', res, wind)
        self.update_slave_timer(roomId, 0)
        self.db.commit()

    def get_OpRecord_id(self, Record: str):
        sql = 'select id from CheckRecord where Record = {}'.format(Record)
        lock.acquire()
        self.cursor.execute(sql)
        lock.release()
        id = self.cursor.fetchone()[0]
        self.db.commit()
        return id

    def get_room_list(self):
        db = pymysql.connect(
            host=DATABASE_USER_HOST,  # 默认用主机名
            port=DATABASE_USER_PORT,
            user=DATABASE_USER_NAME,  # 默认用户名
            password=DATABASE_USER_PASSWORD,  # mysql密码
            database=DATABASE_SCHEMA,  # 库名
            charset='utf8'  # 编码方式
        )  # 打开数据库连接
        cursor = db.cursor()
        lock.acquire()
        cursor.execute("select * from slave")
        lock.release()
        db.commit()
        ret = []
        while 1:
            t = cursor.fetchone()
            temp = {}
            if t is None:
                break
            temp = {
                'id': t[0],
                'name': t[1],
                'idCard': t[2],
                'checkInDate': t[3],
                'cost': t[4],
                'expectTemp': t[5],
                'speed': t[6],
                'temp': t[7],
                'power': t[8],
                'timer': t[9],
                'haveCheckIn': t[10],
                'showDetails': t[11]
            }
            ret.append(temp)
        cursor.close()
        db.close()
        return ret

    # 获取表单staring date,ending date,starting room,ending room
    def get_form(self, sd, ed, sr, er):
        sql = "select * from OpRecord where time between \"{}\" and \"{}\"".format(sd, ed)
        self.cursor.execute(sql)
        ret = []
        all_record = self.cursor.fetchall()
        count = 0
        if all_record is not None:
            count = len(all_record)
        i = 0
        while i < count:
            t = all_record[i]
            if t is None:
                break
            rid = self.get_OpRecord_id(t[0])
            if int(sr[0]) <= int(rid) and int(rid) <= int(er[0]):
                ret.append({
                    "id": rid,
                    "time": t[1],
                    "type": t[2],
                    "old": t[3],
                    "new": t[4],
                    "wind": t[5],
                    "cost": t[6]
                })
            i = i + 1
        self.db.commit()
        return ret

    def update_state(self):
        db = pymysql.connect(
            host=DATABASE_USER_HOST,  # 默认用主机名
            port=DATABASE_USER_PORT,
            user=DATABASE_USER_NAME,  # 默认用户名
            password=DATABASE_USER_PASSWORD,  # mysql密码
            database=DATABASE_SCHEMA,  # 库名
            charset='utf8'  # 编码方式
        )  # 打开数据库连接
        wind = {'low': 60, 'medium': 60, 'high': 60, 'Shutdown': 60} #不管开关机都是每分钟变化0.5度

        for idx, slave in enumerate(self.slaves):
            #print(slave.jsonify())
            if slave['power'] == True:
                if abs(float(slave.expectTemp) - float(slave.temp)) >= 0.5:
                    if idx not in self.blowing_list and idx not in self.schedule_queue:
                        # 温度未达到要求,且没有加入队列,那么将其加入到等待队列
                        self.schedule_queue.append(idx)
                        if self.mode == 'Cold' and int(slave.expectTemp) > int(slave.temp):
                            self.schedule_queue.remove(idx)
                        if self.mode == 'Hot' and int(slave.expectTemp) < int(slave.temp):
                            self.schedule_queue.remove(idx)
                    else:
                        if idx in self.blowing_list:
                            # 该机器被调度到送风队列了,开启送风
                            if slave['is_blowing_in'] == False:
                                roomid = trans_id_to_roomid(idx)
                                self.update_cost_and_wind(roomid, '5', '0', '1')
                                #print("update_cost_and_wind")
                                slave['is_blowing_in'] = True
                            else:
                                # 已经在送风了,啥也不用管
                                pass
                else:
                    if idx in self.blowing_list:
                        self.blowing_list.remove(idx)
                    if idx in self.schedule_queue:
                        self.schedule_queue.remove(idx)
                    if slave['is_blowing_in'] == True:
                        # 温度已经达到要求,送风停止
                        roomid = trans_id_to_roomid(idx)
                        self.update_cost_and_wind(roomid, '5', '1', '0')
                        slave['is_blowing_in'] = False
            else:
                if idx in self.blowing_list:
                    self.blowing_list.remove(idx)
                if idx in self.schedule_queue:
                    self.schedule_queue.remove(idx)
                if slave['is_blowing_in'] == True:
                    # 空调关机,送风停止
                    roomid = trans_id_to_roomid(idx)
                    self.update_cost_and_wind(roomid, '5', '1', '0')
                    slave['is_blowing_in'] = False
            if slave['power'] == True and slave['is_blowing_in'] == True:
                # 开机状态温度变化
                roomid = trans_id_to_roomid(idx)
                tim = int(self.get_slave_timer(str(roomid)))
                if tim != 0:
                    if tim % wind[slave.speed] == 0:
                        if float(slave.expectTemp) - float(slave.temp) >= 0.5:
                            slave.temp = str(float(slave.temp) + 0.5)
                            #print("更新")
                        elif float(slave.expectTemp) - float(slave.temp) <= -0.5:
                            slave.temp = str(float(slave.temp) - 0.5)
                            #print("更新")
            else:  # 关机状态温度变化
                if self.opened_time % wind['Shutdown'] == 0:
                    if slave.init_temper > float(slave.temp):
                        slave.temp = str(float(slave.temp) + 0.5)
                    elif slave.init_temper < float(slave.temp):
                        slave.temp = str(float(slave.temp) - 0.5)
            detail_str = "%s" % "1" if slave._showDetails else "0"
            cursor = db.cursor()
            roomid = trans_id_to_roomid(idx)
            lock.acquire()
            cursor.execute("update slave set name=%s, idCard=%s, temp=%s, expectTemp=%s,showDetails=%s where id=%s",
                           (slave.name, slave.idCard, slave.temp, slave.expectTemp,detail_str, str(roomid)))
            lock.release()
            db.commit()
        cursor.close()
        db.close()

    def schedule(self):
        # 各种调度算法
        # self.blowing_list = list(set(self.blowing_list))
        # self.schedule_queue = list(set(self.schedule_queue))

        # 时间片轮转
        # if self.opened_time % 4 == 0:
        #     if self.blowing_list.__len__() > 0:
        #         temp_idx = self.blowing_list[0]
        #         self.blowing_list.remove(temp_idx)
        #         self.schedule_queue.append(temp_idx)

        #         self.slaves[temp_idx]['is_blowing_in'] = False
        #         self.update_cost_and_wind(temp_idx,'5','1','0')

        # print("\033c\n")
        #print("送风队列:",self.blowing_list)
        #print("等待队列:", self.schedule_queue)

        if self.blowing_list.__len__() < 3:
            # 如果存在空余,且有空调等待送风
            #print("<3")
            if self.schedule_queue.__len__() != 0:
                # 取队首元素加入到送风集合
                #print(self.schedule_queue)
                idx = self.schedule_queue[0]
                self.schedule_queue.pop(0)
                self.blowing_list.append(idx)
                #print("blowing_list.append",idx)
                # 将目标设置为正在送风
                # self.slaves[idx].is_blowing_in = True



    def background(self):
        """后台处理"""
        while 1:
            try:
                self.opened_time += 1
                #print(self.opened_time)
                time.sleep(1)
                # self.respond_to_request()
                self.schedule()
                self.update_state()
                # 增加送风计时的代码
                # 当修改风速时，重新计时，原来的用来计算那一段的费用
                # 每计时一分钟，也输出一个结果，用来计算费用
                for i in range(self.SLAVE_NUM):
                    roomid = trans_id_to_roomid(i)
                    power = self.get_slave_power(str(roomid))
                    Record = self.get_CheckRecord_Record(str(roomid))
                    if Record is not None and power == '1':  # 如果已经入住且当前是开机状态，就计时,并且检查计时状态，进行
                        tim = int(self.get_slave_timer(str(roomid)))
                        Record = Record[0]
                        if tim % 60 == 0 and tim != 0:  # 如果当前计满了60s，就更新一次，然后计时器归0
                            print("now time = %s" % (tim))
                            self.update_cost_and_wind(str(roomid), '4', '0', '0')
                            self.update_slave_timer(str(roomid), 0)
                        else:
                            if self.slaves[i].is_blowing_in == False:
                                self.update_slave_timer(str(roomid), 0)
                            else:
                                self.update_slave_timer(str(roomid), tim + 1)
            except Exception as e:
                print(e)
                print("********出现了一下错误***********:", e)
                time.sleep(1)
                print("尝试重连")
                self.db.ping(reconnect=True)
                print("重连成功")


    def respond_to_request(self):
        while not self.request_queue.empty():
            request = self.request_queue.get()
            request()



if __name__ == "__main__":
    master = Master()
    print(master.keys())

# 操作记录[当前时间，住房记录号(主键)，操作类型，原来值，请求值，总送风量，总花费]

# 用户所有按钮操作都记录下来：
# 每一分钟就更新一次费用
# 从控机开机时，计时器从0开始
# 从控机关机时，更新费用，状态变为关机，计时器更新的时候发现状态关机，停止计时，
# 修改风速时，计时器导出值，清零开始，更新费用
# 签退时，如果计时器还开着，就关闭计时器，更新费用；如果关了，就不用管了
