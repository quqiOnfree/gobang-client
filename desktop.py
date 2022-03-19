from tkinter.font import BOLD
import ai_game
from createroom import Ui_createroom
from PyQt5 import sip
from PyQt5.QtWidgets import QWidget
import socket
from arcade import *
import arcade.color as color
import single_game
import time
import json
import os
import struct
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QMessageBox
import model,sys

globalist = sys.modules['__main__'].__dict__

class receive_thread(QThread):
    # 接收信息系统，在连接之后才创建
    msglist = list()
    receivemsg = bytes()
    can_get = 0

    def __init__(self):
        super().__init__()

    def run(self):
        while True:
            try:
                self.receivemsg += s.recv(1024)
                head = self.receivemsg[:8]
                head = struct.unpack("Q", head)[0]
                if (len(self.receivemsg[8:]) >= head):
                    self.msglist.append(self.receivemsg[8:8+head])
                    self.receivemsg = self.receivemsg[8+head:]
                    self.can_get += 1
            except:
                time.sleep(0.1)

    def get_msg(self):
        # 获取解包后的信息
        while True:
            if (self.can_get > 0):
                msg = self.msglist.pop(0)
                self.can_get -= 1
                return msg
            time.sleep(0.01)


def sendmsg(string: bytes):
    s.send(struct.pack("Q", len(string))+string)


def receivemsg() -> bytes:
    return receive_system.get_msg()


class buttom():  # buttom class类，处理事务
    def __init__(self, x, y, img, img2, scale) -> None:
        self.x, self.y, self.scale = x, y, scale
        self.sprite1 = Sprite(img, scale, hit_box_algorithm='Detailed')
        self.sprite1.center_x = x
        self.sprite1.center_y = y
        self.sprite2 = Sprite(img2, scale, hit_box_algorithm='Detailed')
        self.sprite2.center_x = x
        self.sprite2.center_y = y
        self.state = 1

    def draw(self):  # 将按钮画在屏幕上
        if (self.state == 1):
            self.sprite1.draw()
        else:
            self.sprite2.draw()

    def on_move(self, x, y):  # 检测是否在按钮之内
        if (self.state == 1):
            if (self.sprite1._get_top() > y and self.sprite1._get_bottom() < y and self.sprite1._get_left() < x and self.sprite1._get_right() > x):
                return True
            return False
        else:
            if (self.sprite2._get_top() > y and self.sprite2._get_bottom() < y and self.sprite2._get_left() < x and self.sprite2._get_right() > x):
                return True
            return False

    def update(self, state: int):
        self.state = state

    def get_sprite(self):
        if (self.state == 1):
            return self.sprite1
        else:
            return self.sprite2


class room_buttom():
    def __init__(self, x, y, img, img2, img3, scale, name: str, host: str, state: str) -> None:
        self.x, self.y = x, y
        if (len(name) > 10):
            self.name = name[:10]
        else:
            self.name = name
        if (len(host) > 10):
            self.host = host[:10]
        else:
            self.host = host
        self.hostname = host
        self.room_state = state
        self.state = 1

        self.sprite1 = Sprite(img, scale, hit_box_algorithm='Detailed')
        self.sprite1.center_x = x
        self.sprite1.center_y = y

        self.sprite2 = Sprite(img2, scale, hit_box_algorithm='Detailed')
        self.sprite2.center_x = x
        self.sprite2.center_y = y

        self.sprite3 = Sprite(img3, scale, hit_box_algorithm='Detailed')
        self.sprite3.center_x = x
        self.sprite3.center_y = y

        self.name_x = x-450
        self.host_x = x+200
        self.state_x = x+350

    def draw(self):
        if (self.state == 1):
            self.sprite1.draw()
        elif (self.state == 2):
            self.sprite2.draw()
        else:
            self.sprite3.draw()
        draw_text(self.name, self.name_x, self.y, color.WHITE,
                  20, bold=True, anchor_y="center")
        draw_text(self.host, self.host_x, self.y, color.WHITE,
                  20, bold=True, anchor_y="center")
        draw_text(self.room_state, self.state_x, self.y,
                  color.WHITE, 20, bold=True, anchor_y='center')
        if (self.room_state == "已开始"):
            self.update(3, 0)

    def update(self, state: int, change_y: int):
        self.state = state
        self.y += change_y
        self.sprite1.center_y = self.y
        self.sprite2.center_y = self.y

    def on_move(self, x, y):
        if (self.state == 1):
            if (self.sprite1._get_top() > y and self.sprite1._get_bottom() < y and self.sprite1._get_left() < x and self.sprite1._get_right() > x):
                return True
            return False
        elif (self.state == 2):
            if (self.sprite2._get_top() > y and self.sprite2._get_bottom() < y and self.sprite2._get_left() < x and self.sprite2._get_right() > x):
                return True
            return False
        else:
            if (self.sprite3._get_top() > y and self.sprite3._get_bottom() < y and self.sprite3._get_left() < x and self.sprite3._get_right() > x):
                return True
            return False


# class thr(QThread):  # 异步检测
#     signal = pyqtSignal(bool)

#     def __init__(self, is_ai: bool = False) -> None:
#         super().__init__()
#         self.is_ai = is_ai

#     def run(self):
#         while True:
#             if (globalist['modelGame'].has_exit):
#                 if (self.is_ai):
#                     self.signal.emit(True)
#                 else:
#                     self.signal.emit(False)
#                 return
#             time.sleep(0.01)


class main_desk(model.BaceGame):  # 主界面class
    def __init__(self, soc: socket.socket, name: str, receive_system_: receive_thread):
        super().__init__(1000, 800, "曲奇五子棋")
        global username, s, receive_system
        receive_system = receive_system_
        s = soc
        username = name
        self.setup()
        self.draw = True

    def setup(self):  # 加载主界面、按钮
        self.duoren = buttom(
            200, 400-40, "./library/buttom/多人游戏.png", "./library/buttom/多人游戏_2.png", 0.8)
        self.danren = buttom(
            200, 280-60, "./library/buttom/单人游戏.png", "./library/buttom/单人游戏_2.png", 0.8)
        self.aiduizhan = buttom(
            200, 160-80, "./library/buttom/AI对战.png", "./library/buttom/AI对战_2.png", 0.8)
        self.title = buttom(500, 650, "./library/title/五子棋2.png",
                            "./library/title/五子棋2.png", 1)
        set_background_color(color.SKY_BLUE)
        sendmsg(json.dumps({"get_data": {"name": username}},
                ensure_ascii=False).encode('gb18030'))
        self.user_data = json.loads(receivemsg().decode('gb18030'))['get_data']

    def on_draw(self):  # 将按钮等画在屏幕上
        start_render()
        if (self.draw):
            self.duoren.draw()
            self.danren.draw()
            self.aiduizhan.draw()
            self.title.draw()
            draw_text('name :'+self.user_data['name'],
                      500, 380, color.WHITE, 20, bold=True)
            draw_text('level:'+self.user_data['level'],
                      500, 380-40, color.WHITE, 20, bold=True)
            draw_text('score:'+self.user_data['score'],
                      500, 380-80, color.WHITE, 20, bold=True)
            draw_text(
                '多人游戏胜利:'+self.user_data['socket_win_game'], 500, 380-120, color.WHITE, 20, bold=True)
            draw_text(
                'AI游戏胜利:'+self.user_data['ai_win_game'], 500, 380-160, color.WHITE, 20, bold=True)
            draw_text('注册时间:'+self.user_data['reg_time'],
                      500, 380-200, color.WHITE, 20, bold=True)
            draw_text(
                '上次登录时间:'+self.user_data['login_time'], 500, 380-240, color.WHITE, 20, bold=True)

    def on_update(self, delta_time: float):
        pass

    def on_close(self):
        import os
        os._exit(0)

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        # 检测鼠标的行动轨迹
        # 检测鼠标是否在按钮中
        if (self.duoren.on_move(x, y)):
            self.duoren.update(2)
        else:
            self.duoren.update(1)
        if (self.danren.on_move(x, y)):
            self.danren.update(2)
        else:
            self.danren.update(1)
        if (self.aiduizhan.on_move(x, y)):
            self.aiduizhan.update(2)
        else:
            self.aiduizhan.update(1)

    def open(self, is_ai: bool):  # 接收信号之后调用的函数
        #self.set_visible(True)
        # self.game.close()
        # if (is_ai):
        #     winner = self.game.winner
        # else:
        #     winner = None
        # del self.game
        # set_window(self)
        # self.draw = True
        # if is_ai == True:
        #     if (winner == 'black'):
        #         sendmsg(json.dumps(
        #             {"add_ai_score": {"name": username}}, ensure_ascii=False).encode('gb18030'))
        #         receivemsg()
        # while True:
        #     sendmsg(json.dumps({"get_data": {"name": username}},
        #             ensure_ascii=False).encode('gb18030'))
        #     self.user_data = json.loads(receivemsg().decode('gb18030'))
        #     if (type(self.user_data) == type({})):
        #         if ('get_data' in list(self.user_data.keys())):
        #             if('error' not in list(self.user_data['get_data'])):
        #                 self.user_data = self.user_data['get_data']
        #                 break
        pass

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        # 鼠标点击事件
        global globalist
        if (button == MOUSE_BUTTON_LEFT):
            if (self.duoren.on_move(x, y)):
                self.draw = False
                globalist['modelGame'] = socket_desktop((s,username,receive_system))
            if (self.danren.on_move(x, y)):
                self.draw = False
                globalist['modelGame'] = single_game.main_game(1000, 800, "曲奇五子棋",(s,username,receive_system))
            if (self.aiduizhan.on_move(x, y)):
                self.draw = False
                globalist['modelGame'] = ai_game.ai_main_game(1000, 800, "曲奇五子棋",(s,username,receive_system), False)


class get_room_data(QThread):
    signal = pyqtSignal(dict)

    def __init__(self):
        super().__init__()

    def run(self):
        sendmsg(json.dumps({"get_room": {}},
                ensure_ascii=False).encode('gb18030'))
        msg = json.loads(receivemsg().decode('gb18030'))
        self.signal.emit(msg)


class createRoom(QWidget, Ui_createroom):
    signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.createroom)

    def createroom(self):
        sendmsg(json.dumps({"create_room": {"roomname": self.lineEdit.text(
        ).strip(), "hostname": username}}, ensure_ascii=False).encode('gb18030'))
        msg = json.loads(receivemsg().decode('gb18030'))['create_room']
        if ('error' in list(msg.keys())):
            QMessageBox.warning(self, '警告', msg['error'])
            return
        if ('success' in list(msg.keys())):
            QMessageBox.information(self, '信息', msg['success'])
            self.close()
            self.signal.emit(self.lineEdit.text().strip())
            sip.delete(self)


class socketroom_receive(QThread):
    msglist = []

    def __init__(self):
        super().__init__()
        self.gameover = None
        self.start_ = None
        self.winner = None
        self.has_exit = False

    def run(self):
        while True:
            is_msg = False
            msg = json.loads(receive_system.get_msg().decode('gb18030'))
            if (type(msg) == type({})):
                if ('start' in list(msg.keys())):
                    self.start_ = msg['start']
                    is_msg = True
                if ("gameover" in list(msg.keys())):
                    self.winner = msg["winner"]
                    self.gameover = msg['gameover']
                    is_msg = True
                if ("leaveroom" in list(msg.keys())):
                    self.gameover = True
                    self.winner = "someone left the room"
                    self.has_exit = True
                    is_msg = True
            if (is_msg == False):
                self.msglist.append(json.dumps(
                    msg, ensure_ascii=False).encode('gb18030'))
            time.sleep(0.01)

    def get_msg(self):
        while True:
            if (len(self.msglist) != 0):
                return self.msglist.pop(0)
            time.sleep(0.01)


class socket_room(model.BaceGame):
    def __init__(self,arr:list):
        super().__init__(1000, 800, '曲奇五子棋', visible=False)
        self.width = 1000
        self.height = 800
        self.setup()
        self.arr = arr

    def setup(self):
        set_background_color(color.SKY_BLUE)
        self.dx = 0
        self.dy = 0
        self.mouse_press_x = 0
        self.mouse_press_y = 0
        self.title = 0
        self.title_show = True
        self.piece = '.'
        self.yourpiece = '.'
        self.draw_start = True
        self.lastpiece = (-1, -1)
        self.host = False
        self.userexit = False

        self.lastpiece_sprite = Sprite(
            "./library/buttom/准心.png", 0.4, center_x=-100, center_y=-100)

        # 按钮
        self.huiqi = buttom(
            900, 650, "./library/buttom/悔棋.png", "./library/buttom/悔棋_2.png", 0.4)
        self.huiqi.is_can = False

        self.fanhui2 = buttom(
            900, 550, "./library/buttom/返回主界面.png", "./library/buttom/返回主界面_2.png", 0.4)

        self.edge_lenght = 25                                           # 边缘位置
        self.grid_count = 19                                            # 一共19行19列
        self.grid_lenght = (self.height-2*self.edge_lenght) / \
            (self.grid_count-1)  # 格子边长
        self.start_x = 0                                                # 起始位置
        self.start_y = self.height

        # self.winner = None  # 一起触发
        # self.gameover = None
        # self.start = None
        self.receive = socketroom_receive()
        self.receive.start()

        self.grid = []  # 棋盘
        for i in range(self.grid_count):
            self.grid.append(list('.'*self.grid_count))

        self.update_chessboard = 0

    def on_close(self):
        if (self.receive.gameover != True or self.host):
            sendmsg(json.dumps(
                {"leave_room": {"name": username}}, ensure_ascii=False).encode('gb18030'))
            self.receive.has_exit = True
            self.userexit = True
        else:
            self.receive.has_exit = True
            self.userexit = True
        os._exit(0)

    def on_draw(self):
        start_render()
        self.draw()
        if (self.draw_start):
            draw_rectangle_filled(500, 400, 700, 400, color.BLUE_GRAY)
            draw_text("waiting for player...", 500, 400, color.WHITE,
                      50, anchor_x='center', anchor_y='center', bold=True)
        if (self.title_show and self.receive.gameover):
            if (self.receive.winner == "black"):
                draw_text("Black Win!", self.width/2-200,
                          self.height/2, color.RED_ORANGE, 50)
            else:
                draw_text("White Win!", self.width/2-200,
                          self.height/2, color.RED_ORANGE, 50)
        if (self.lastpiece[0] >= 0 and self.lastpiece[1] >= 0):
            self.lastpiece_sprite.draw()

    def on_update(self, delta_time: float):
        if (self.receive.start_ == None or self.receive.start_ == False):
            self.draw_start = True
        else:
            self.draw_start = False
        if (self.receive.gameover and self.title_show):
            self.title += 1
            if (self.title % 60 == 0):
                self.title_show = False
        if (self.receive.has_exit):
            if (self.receive.gameover != True or self.userexit == True):
                self.receive.terminate()
                for i in range(5):
                    self.receive.msglist.clear()
                    receive_system.msglist.clear()
                self.has_exit = True
                global globalist
                globalist['modelGame'] = socket_desktop((self.arr[0],self.arr[1],self.arr[2]))
        if (self.receive.start_):
            self.update_chessboard += 1
            if (self.update_chessboard % 10 == 0):
                sendmsg(json.dumps(
                    {"get_chessboard": {"name": username}}, ensure_ascii=False).encode('gb18030'))
                msg = json.loads(self.receive.get_msg().decode('gb18030'))
                if (type(msg) == type({})):
                    if ('get_chessboard' in list(msg.keys())):
                        if (type(msg['get_chessboard']) == type({})):
                            if ('chessboard' in list(msg['get_chessboard'].keys())):
                                self.grid = msg['get_chessboard']['chessboard']

                sendmsg(json.dumps(
                    {"get_yourpiece": {'name': username}}).encode('gb18030'))
                msg = json.loads(self.receive.get_msg().decode('gb18030'))[
                    'get_yourpiece']
                if (type(msg) == type({})):
                    if ('yourpiece' in list(msg.keys())):
                        self.yourpiece = msg['yourpiece']

                sendmsg(json.dumps(
                    {"get_nowpiece": {'name': username}}).encode('gb18030'))
                msg = json.loads(self.receive.get_msg().decode('gb18030'))[
                    'get_nowpiece']
                if (type(msg) == type({})):
                    if ('nowpiece' in list(msg.keys())):
                        self.piece = msg['nowpiece']

                sendmsg(json.dumps(
                    {"get_lastpiece": {'name': username}}).encode('gb18030'))
                msg = json.loads(self.receive.get_msg().decode('gb18030'))[
                    'get_lastpiece']
                if (type(msg) == type({})):
                    if ('lastpiece' in list(msg.keys())):
                        self.lastpiece = (
                            msg['lastpiece']['x'], msg['lastpiece']['y'])
                        self.lastpiece_sprite.center_x = self.lastpiece[1] * \
                            self.grid_lenght+self.edge_lenght
                        self.lastpiece_sprite.center_y = 800 - \
                            self.lastpiece[0]*self.grid_lenght-self.edge_lenght

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        if (self.huiqi.on_move(x, y)):
            self.huiqi.update(2)
        else:
            self.huiqi.update(1)

        if (self.fanhui2.on_move(x, y)):
            self.fanhui2.update(2)
        else:
            self.fanhui2.update(1)

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        if (button == MOUSE_BUTTON_LEFT):
            if (self.fanhui2.on_move(x, y)):
                if (self.receive.gameover != True or self.host):
                    sendmsg(json.dumps(
                        {"leave_room": {"name": username}}, ensure_ascii=False).encode('gb18030'))
                    self.receive.has_exit = True
                    self.userexit = True
                else:
                    self.receive.has_exit = True
                    self.userexit = True
            if (0 < x < 800 and 0 < y < 800):
                self.handle_event((x, y))
            if (self.huiqi.on_move(x, y)):
                if (self.receive.gameover != True):
                    sendmsg(json.dumps(
                        {"regret_piece": {'name': username}}, ensure_ascii=False).encode('gb18030'))

    def draw(self):  # 着色
        draw_point(self.height/2, self.height/2, color.BLACK, self.height+10)
        draw_point(self.height/2, self.height/2,
                   color.LIGHT_YELLOW, self.height)
        for i in range(self.grid_count):
            draw_line(self.start_x+self.edge_lenght, self.height-self.edge_lenght-i*self.grid_lenght, self.start_x +
                      self.edge_lenght+(self.grid_count-1)*self.grid_lenght, self.height-self.edge_lenght-i*self.grid_lenght, color.BLACK, 2)
        for i in range(self.grid_count):
            draw_line(self.start_x+self.edge_lenght+i*self.grid_lenght, self.height-self.edge_lenght, self.start_x +
                      self.edge_lenght+i*self.grid_lenght, self.height-self.edge_lenght-self.grid_lenght*(self.grid_count-1), color.BLACK, 2)
        draw_point(self.height/2, self.height/2, color.BLACK, 10)
        draw_point(self.edge_lenght+self.grid_lenght*3, self.height -
                   self.edge_lenght-15*self.grid_lenght, color.BLACK, 10)
        draw_point(self.edge_lenght+self.grid_lenght*3, self.height -
                   self.edge_lenght-3*self.grid_lenght, color.BLACK, 10)
        draw_point(self.edge_lenght+self.grid_lenght*15, self.height -
                   self.edge_lenght-15*self.grid_lenght, color.BLACK, 10)
        draw_point(self.edge_lenght+self.grid_lenght*15, self.height -
                   self.edge_lenght-3*self.grid_lenght, color.BLACK, 10)
        for i in range(self.grid_count):
            for j in range(self.grid_count):
                if (self.grid[i][j] == "black"):
                    draw_circle_filled(self.edge_lenght+self.grid_lenght*j, self.height -
                                       self.grid_lenght*i-self.edge_lenght, 20, color.BLACK)
                elif (self.grid[i][j] == "white"):
                    draw_circle_filled(self.edge_lenght+self.grid_lenght*j, self.height -
                                       self.grid_lenght*i-self.edge_lenght, 20, color.BLACK)
                    draw_circle_filled(self.edge_lenght+self.grid_lenght*j, self.height -
                                       self.grid_lenght*i-self.edge_lenght, 19, color.WHITE)
        if (self.piece == "black"):
            draw_text("Black plays chess", 900, 775, color.BLACK, 15,
                      bold=True, anchor_x="center", anchor_y="center")
        elif (self.piece == "white"):
            draw_text("White plays chess", 900, 775, color.WHITE, 15,
                      bold=True, anchor_x="center", anchor_y="center")

        if (self.yourpiece == "black"):
            draw_text("你是黑方", 900, 730, color.BLACK, 15,
                      bold=True, anchor_x="center", anchor_y="center")
        elif (self.yourpiece == "white"):
            draw_text("你是白方", 900, 730, color.WHITE, 15,
                      bold=True, anchor_x="center", anchor_y="center")

        if (self.receive.gameover):
            if (self.title_show):
                if (self.receive.winner == "black"):
                    draw_text("Black Win!", self.width/2-200,
                              self.height/2, color.RED_ORANGE, 50)
                else:
                    draw_text("White Win!", self.width/2-200,
                              self.height/2, color.RED_ORANGE, 50)

        self.huiqi.draw()
        self.fanhui2.draw()

    def handle_event(self, e):
        origin_x = self.start_x - self.edge_lenght
        origin_y = self.start_y - self.edge_lenght
        chessboard_lenght = (self.grid_count - 1) * \
            self.grid_lenght + self.edge_lenght * 2
        mouse_pos = e  # 鼠标位置在棋盘坐标内
        if (mouse_pos[0] > origin_x and mouse_pos[0] <= origin_x + chessboard_lenght) and (
                mouse_pos[1] <= origin_y and mouse_pos[1] >= origin_y - chessboard_lenght):
            if not self.receive.gameover:
                x = mouse_pos[0] - origin_x  # X轴方向距离
                c = round(x / self.grid_lenght)-1  # 换算出X轴第几格
                y = origin_y - mouse_pos[1]
                r = round(y / self.grid_lenght)  # 换算出Y轴第几格
                sendmsg(json.dumps({'fall_piece': {
                        "name": username, 'x': r, 'y': c}}, ensure_ascii=False).encode('gb18030'))


class socket_desktop(model.BaceGame):
    def __init__(self,arr:list):
        super().__init__(1000, 800, "曲奇五子棋", visible=False)
        self.setup()
        self.arr =arr
        self.width = 1000
        self.height = 800

    def setup(self):
        set_background_color(color.SKY_BLUE)
        self.roomlist = []
        # 按钮
        self.spritelist = SpriteList()
        self.chuangjian = buttom(
            100, 750, "./library/buttom/创建房间.png", "./library/buttom/创建房间_2.png", 0.4)
        self.fanhui = buttom(
            300, 750, "./library/buttom/返回主界面.png", "./library/buttom/返回主界面_2.png", 0.4)
        self.shuaxin = buttom(
            500, 750, "./library/buttom/刷新.png", "./library/buttom/刷新_2.png", 0.4)

        self.get_room = get_room_data()
        self.get_room.signal.connect(self.getRoom)
        self.get_room.start()

        self.can_draw = True

    def getRoom(self, msg):
        if (type(msg) == type({})):
            if ('get_room' in list(msg.keys())):
                msg = msg['get_room']
                if (type(msg) == type({})):
                    if ('error' in list(msg.keys())):
                        pass
                elif (type(msg) == type([])):
                    for i in range(len(msg)):
                        self.roomlist.append(room_buttom(500, 650-i*100, './library/buttom/多人游戏框.png',
                                                         './library/buttom/多人游戏框_2.png', './library/buttom/多人游戏框_3.png', 0.8, msg[i]['roomname'], msg[i]['hostname'], msg[i]['state']))

    def on_draw(self):
        start_render()
        if (self.can_draw):
            for i in range(len(self.roomlist)):
                self.roomlist[i].draw()

            draw_rectangle_filled(500, 850, 1000, 300, color.SKY_BLUE)
            self.chuangjian.draw()
            self.fanhui.draw()
            self.shuaxin.draw()
            draw_text("房间名", 500-450, 720, color.WHITE,
                      20, bold=True, anchor_y='center')
            draw_text("用户名", 500+200, 720, color.WHITE,
                      20, bold=True, anchor_y='center')
            draw_text("状态", 500+350, 720, color.WHITE,
                      20, bold=True, anchor_y='center')

    def on_update(self, delta_time: float):
        pass

    def open(self, is_on: bool):
        #self.set_visible(True)
        self.can_draw = True
        del self.roomlist
        self.roomlist = []
        sendmsg(json.dumps({"get_room": {}},
                ensure_ascii=False).encode('gb18030'))
        msg = json.loads(receivemsg().decode('gb18030'))
        if (type(msg) == type({})):
            if ("get_room" in list(msg.keys())):
                if (type(msg["get_room"]) == type({})):
                    if ('error' in list(msg['get_room'].keys())):
                        pass
                elif (type(msg["get_room"]) == type([])):
                    for i in range(len(msg["get_room"])):
                        self.roomlist.append(room_buttom(500, 650-i*100, './library/buttom/多人游戏框.png',
                                                         './library/buttom/多人游戏框_2.png', './library/buttom/多人游戏框_3.png', 0.8, msg["get_room"][i]['roomname'], msg["get_room"][i]['hostname'], msg["get_room"][i]['state']))

    def success_create_room(self, msg: str):
        global globalist
        globalist['modelGame'] = socket_room((s,username,receive_system))
        if (msg != '[nohost]'):
            globalist['modelGame'].host = True
        #globalist['modelGame'].set_visible(True)

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        if (button == MOUSE_BUTTON_LEFT):
            if (self.fanhui.on_move(x, y)):
                self.has_exit = True
                global globalist
                globalist['modelGame'] = main_desk(self.arr[0],self.arr[1],self.arr[2])
            if (self.chuangjian.on_move(x, y)):
                self.can_draw = False
                self.ui = createRoom()
                self.ui.signal.connect(self.success_create_room)
                self.ui.show()
            if (self.shuaxin.on_move(x, y)):
                self.get_room = get_room_data()
                self.get_room.signal.connect(self.getRoom)
                self.get_room.start()
            for i in range(len(self.roomlist)):
                if (self.roomlist[i].on_move(x, y)):
                    if (self.roomlist[i].room_state == '等待中'):
                        self.can_draw = False
                        self.success_create_room("[nohost]")
                        sendmsg(json.dumps({"join_room": {
                                "name": username, "hostname": self.roomlist[i].hostname}}, ensure_ascii=False).encode('gb18030'))

    def on_mouse_scroll(self, x: int, y: int, scroll_x: int, scroll_y: int):
        if (len(self.roomlist) > 8 and ((self.roomlist[0].y > 650 and scroll_y > 0) or (self.roomlist[-1].y < 100 and scroll_y < 0))):
            for i in range(len(self.roomlist)):
                self.roomlist[i].update(self.roomlist[i].state, scroll_y*-10)

    def on_close(self):
        import os
        os._exit(0)

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        if (self.chuangjian.on_move(x, y)):
            self.chuangjian.update(2)
        else:
            self.chuangjian.update(1)
        if (self.fanhui.on_move(x, y)):
            self.fanhui.update(2)
        else:
            self.fanhui.update(1)
        if (self.shuaxin.on_move(x, y)):
            self.shuaxin.update(2)
        else:
            self.shuaxin.update(1)
        for i in range(len(self.roomlist)):
            if (self.roomlist[i].room_state == "等待中"):
                if (self.roomlist[i].on_move(x, y)):
                    self.roomlist[i].update(2, 0)
                else:
                    self.roomlist[i].update(1, 0)
            else:
                self.roomlist[i].update(3, 0)
