import time
from arcade import *
import arcade.color as color
from PyQt5.QtCore import QThread
import desktop


class ai_main_game(Window):
    def __init__(self, width: int, height: int, title: str, visible: bool = True, is_myself: bool = True, piece: str = "black"):
        super().__init__(width, height, title, visible=visible)

        self.piece = piece
        self.is_myself = is_myself

        self.set_up()

    def set_up(self):
        set_background_color(color.SKY_BLUE)

        self.dx = 0
        self.dy = 0
        self.mouse_press_x = 0
        self.mouse_press_y = 0
        self.title = 0
        self.title_show = True

        # 按钮
        self.huiqi = desktop.buttom(
            900, 650, "./library/buttom/悔棋.png", "./library/buttom/悔棋_2.png", 0.4)
        self.huiqi.is_can = False

        self.fanhui2 = desktop.buttom(
            900, 550, "./library/buttom/返回主界面.png", "./library/buttom/返回主界面_2.png", 0.4)

        self.edge_lenght = 25                                           # 边缘位置
        self.grid_count = 19                                            # 一共19行19列
        self.grid_lenght = (self.height-2*self.edge_lenght) / \
            (self.grid_count-1)  # 格子边长
        self.start_x = 0                                                # 起始位置
        self.start_y = self.height

        self.winner = None  # 一起触发
        self.gameover = None
        self.grid = []  # 棋盘
        for i in range(self.grid_count):
            self.grid.append(list('.'*self.grid_count))

    def on_close(self):
        import os
        os._exit(0)

    def on_draw(self):  # 着色
        start_render()
        self.draw()

    def on_update(self, delta_time: float):
        if (self.gameover):
            self.title += 1
            if (self.title % 60 == 0):
                self.title_show = False

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
            draw_text("Black plays chess", 900, 750, color.BLACK, 15,
                      bold=True, anchor_x="center", anchor_y="center")
        else:
            draw_text("White plays chess", 900, 750, color.WHITE, 15,
                      bold=True, anchor_x="center", anchor_y="center")

        if (self.gameover):
            # draw_rectangle_filled(self.width/2-50, self.height/2,
            #                      self.width/2+50, self.height/2+50, color.GREEN_YELLOW)
            if (self.title_show):
                if (self.winner == "black"):
                    draw_text("Black Win!", self.width/2-200,
                              self.height/2, color.RED_ORANGE, 50)
                    
                else:
                    draw_text("White Win!", self.width/2-200,
                              self.height/2, color.RED_ORANGE, 50)

        # 按钮
        # if (self.gameover):
        #     self.fanhui.draw()
        self.huiqi.draw()
        self.fanhui2.draw()

    def get_continuous_count(self, r, c, dr, dc):  # 统计一个方向的同颜色棋子数量
        piece = self.grid[r][c]
        result = 0
        i = 1
        while True:
            new_r = r + dr * i
            new_c = c + dc * i
            if 0 <= new_r < self.grid_count and 0 <= new_c < self.grid_count:
                if self.grid[new_r][new_c] == piece:  # 该方向颜色相同则加上
                    result += 1
                else:
                    break
            else:
                break
            i += 1
        return result

    def check_win(self, r, c):
        n_count = self.get_continuous_count(r, c, -1, 0)  # 上方向相周颜色棋子数量
        s_count = self.get_continuous_count(r, c, 1, 0)  # 下方相同颜色棋子数量
        w_count = self.get_continuous_count(r, c, 0, -1)  # 左方
        e_count = self.get_continuous_count(r, c, 0, 1)  # 右方
        nw_count = self.get_continuous_count(r, c, -1, -1)  # 左上方
        ne_count = self.get_continuous_count(r, c, -1, 1)  # 右上方
        sw_count = self.get_continuous_count(r, c, 1, -1)  # 左下方
        se_count = self.get_continuous_count(r, c, 1, 1)  # 右下方
        if (n_count + s_count + 1 >= 5) or (e_count + w_count + 1 >= 5) or (se_count + nw_count + 1 >= 5) or (
                ne_count + sw_count + 1 >= 5):
            self.winner = self.grid[r][c]
            self.gameover = True

    def set_piece(self, r, c):
        if self.grid[r][c] == ".":  # 该位置没有棋子
            self.grid[r][c] = self.piece
            self.dx = r
            self.dy = c
            self.huiqi.is_can = True
            if (self.is_myself):
                if self.piece == "black":  # 交替使用棋子
                    self.piece = "white"
                else:
                    self.piece = "black"
            return True
        return False

    def handle_event(self, e):
        origin_x = self.start_x - self.edge_lenght
        origin_y = self.start_y - self.edge_lenght
        chessboard_lenght = (self.grid_count - 1) * \
            self.grid_lenght + self.edge_lenght * 2
        mouse_pos = e  # 鼠标位置在棋盘坐标内
        if (mouse_pos[0] > origin_x and mouse_pos[0] <= origin_x + chessboard_lenght) and (
                mouse_pos[1] <= origin_y and mouse_pos[1] >= origin_y - chessboard_lenght):
            if not self.gameover:
                x = mouse_pos[0] - origin_x  # X轴方向距离
                c = round(x / self.grid_lenght)-1  # 换算出X轴第几格
                y = origin_y - mouse_pos[1]
                r = round(y / self.grid_lenght)  # 换算出Y轴第几格
                if self.piece == 'black':
                    if self.set_piece(r, c):
                        self.check_win(r, c)

    def on_mouse_press(self, x, y, button, key_modifiers):  # 检测鼠标位置
        if (button == MOUSE_BUTTON_LEFT):
            self.mouse_press_x = x
            self.mouse_press_y = y

    def on_mouse_release(self, x: float, y: float, button: int,
                         modifiers: int):
        # 检测鼠标位置
        if (button == MOUSE_BUTTON_LEFT):
            if (self.fanhui2.on_move(x, y)):
                self.has_exit = True
                self.close()
            if self.mouse_press_y == y and self.mouse_press_x == x:
                self.handle_event((x, y))
            if (self.huiqi.on_move(x, y)):  # 检测悔棋
                if (self.gameover == False or self.gameover == None):
                    if (self.huiqi.is_can):
                        self.huiqi.is_can = False
                        if (self.is_myself):
                            if self.piece == "black":  # 交替使用棋子
                                self.piece = "white"
                            else:
                                self.piece = "black"
                        self.grid[self.dx][self.dy] = "."

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        if (self.huiqi.on_move(x, y)):
            self.huiqi.update(2)
        else:
            self.huiqi.update(1)

        if (self.fanhui2.on_move(x, y)):
            self.fanhui2.update(2)
        else:
            self.fanhui2.update(1)


class ai_system(QThread):
    def __init__(self, window: ai_main_game):
        super().__init__()
        self.window = window

    # 统计一个方向的同颜色棋子数量
    def get_continuous_count(self, r, c, dr, dc, piece: str, chessboard: list):
        result = 0
        i = 1
        while True:
            new_r = r + dr * i
            new_c = c + dc * i
            if 0 <= new_r < self.window.grid_count and 0 <= new_c < self.window.grid_count:
                if chessboard[new_r][new_c] == piece:  # 该方向颜色相同则加上
                    result += 1
                else:
                    break
            else:
                break
            i += 1
        return result

    # 统计一个方向的同颜色棋子数量
    def get_continuous_is_live(self, r, c, dr, dc, piece: str, chessboard: list):
        i = 1
        while True:
            new_r = r + dr * i
            new_c = c + dc * i
            if 0 <= new_r < self.window.grid_count and 0 <= new_c < self.window.grid_count:
                if self.window.grid[new_r][new_c] != piece:  # 该方向颜色相同则加上
                    if chessboard[new_r][new_c] != ".":
                        return False
                    else:
                        break
            else:
                break
            i += 1
        return True

    def get_third(self, elem):
        return elem[2]

    def get_score_func(self, chessboard: list):
        score = 0
        model = []
        for i in range(len(chessboard)):
            for j in range(len(chessboard)):
                if (chessboard[i][j] == '.'):
                    n_count = self.get_continuous_count(
                        i, j, -1, 0, 'white', chessboard)  # 上方向相周颜色棋子数量
                    n_islive = self.get_continuous_is_live(
                        i, j, -1, 0, 'white', chessboard)
                    s_count = self.get_continuous_count(
                        i, j, 1, 0, 'white', chessboard)  # 下方相同颜色棋子数量
                    s_islive = self.get_continuous_is_live(
                        i, j, 1, 0, 'white', chessboard)
                    w_count = self.get_continuous_count(
                        i, j, 0, -1, 'white', chessboard)  # 左方
                    w_islive = self.get_continuous_is_live(
                        i, j, 0, -1, 'white', chessboard)
                    e_count = self.get_continuous_count(
                        i, j, 0, 1, 'white', chessboard)  # 右方
                    e_islive = self.get_continuous_is_live(
                        i, j, 0, 1, 'white', chessboard)
                    nw_count = self.get_continuous_count(
                        i, j, -1, -1, 'white', chessboard)  # 左上方
                    nw_islive = self.get_continuous_is_live(
                        i, j, -1, -1, 'white', chessboard)
                    ne_count = self.get_continuous_count(
                        i, j, -1, 1, 'white', chessboard)  # 右上方
                    ne_islive = self.get_continuous_is_live(
                        i, j, -1, 1, 'white', chessboard)
                    sw_count = self.get_continuous_count(
                        i, j, 1, -1, 'white', chessboard)  # 左下方
                    sw_islive = self.get_continuous_is_live(
                        i, j, 1, -1, 'white', chessboard)
                    se_count = self.get_continuous_count(
                        i, j, 1, 1, 'white', chessboard)  # 右下方
                    se_islive = self.get_continuous_is_live(
                        i, j, 1, 1, 'white', chessboard)
                    if (n_count + s_count + 1 >= 6) or (e_count + w_count + 1 == 6) or (se_count + nw_count + 1 == 6) or (ne_count + sw_count + 1 == 6):
                        score += 100000000
                    if (n_count + s_count + 1 == 5) or (e_count + w_count + 1 == 5) or (se_count + nw_count + 1 == 5) or (ne_count + sw_count + 1 == 5):
                        score += 1000000
                        model.append(("白连5", i, j))
                    if (n_count + s_count + 1 == 4 or e_count + w_count + 1 == 4 or se_count + nw_count + 1 == 4 or ne_count + sw_count + 1 == 4):
                        if ((n_count == 1 and s_count == 2) or (n_count == 2 and s_count == 1)):
                            score += 400
                        if ((n_count == 2 and s_count == 1) or (e_count == 1 and w_count == 2)):
                            score += 400
                        if ((se_count == 2 and nw_count == 1) or (se_count == 1 and nw_count == 2)):
                            score += 400
                        if ((sw_count == 2 and ne_count == 1) or (ne_count == 1 and sw_count == 2)):
                            score += 400
                        if (n_count == 3):
                            score += 5000
                            model.append(('白活4', i, j))
                        if (s_count == 3):
                            score += 5000
                            model.append(('白活4', i, j))
                        if (e_count == 3):
                            score += 5000
                            model.append(('白活4', i, j))
                        if (w_count == 3):
                            score += 5000
                            model.append(('白活4', i, j))
                        if (se_count == 3):
                            score += 5000
                            model.append(('白活4', i, j))
                        if (nw_count == 3):
                            score += 5000
                            model.append(('白活4', i, j))
                        if (ne_count == 3):
                            score += 5000
                            model.append(('白活4', i, j))
                        if (sw_count == 3):
                            score += 5000
                            model.append(('白活4', i, j))
                    if (n_count + s_count + 1 == 3 or e_count + w_count + 1 == 3 or se_count + nw_count + 1 == 3 or ne_count + sw_count + 1 == 3):
                        if (n_count == 2 and n_islive):
                            score += 400
                        else:
                            score += 20
                        if (s_count == 2 and s_islive):
                            score += 400
                        else:
                            score += 20
                        if (e_count == 2 and e_islive):
                            score += 400
                        else:
                            score += 20
                        if (w_count == 2 and w_islive):
                            score += 400
                        else:
                            score += 20
                        if (se_count == 2 and se_islive):
                            score += 400
                        else:
                            score += 20
                        if (nw_count == 2 and nw_islive):
                            score += 400
                        else:
                            score += 20
                        if (ne_count == 2 and ne_islive):
                            score += 400
                        else:
                            score += 20
                        if (sw_count == 2) and sw_islive:
                            score += 400
                        else:
                            score += 20
                    if (n_count + s_count + 1 == 2 or e_count + w_count + 1 == 2 or se_count + nw_count + 1 == 2 or ne_count + sw_count + 1 == 2):
                        if (n_count == 1 and n_islive):
                            score += 20
                        else:
                            score += 1
                        if (s_count == 1 and s_islive):
                            score += 20
                        else:
                            score += 1
                        if (e_count == 1 and e_islive):
                            score += 20
                        else:
                            score += 1
                        if (w_count == 1 and w_islive):
                            score += 20
                        else:
                            score += 1
                        if (se_count == 1 and se_islive):
                            score += 20
                        else:
                            score += 1
                        if (nw_count == 1 and nw_islive):
                            score += 20
                        else:
                            score += 1
                        if (ne_count == 1 and ne_islive):
                            score += 20
                        else:
                            score += 1
                        if (sw_count == 1 and sw_islive):
                            score += 20
                        else:
                            score += 1
                    if (n_count + s_count + 1 == 1 or e_count + w_count + 1 == 1 or se_count + nw_count + 1 == 1 or ne_count + sw_count + 1 == 1):
                        score += 1
                    n_count = self.get_continuous_count(
                        i, j, -1, 0, 'black', chessboard)  # 上方向相周颜色棋子数量
                    n_islive = self.get_continuous_is_live(
                        i, j, -1, 0, 'black', chessboard)
                    s_count = self.get_continuous_count(
                        i, j, 1, 0, 'black', chessboard)  # 下方相同颜色棋子数量
                    s_islive = self.get_continuous_is_live(
                        i, j, 1, 0, 'black', chessboard)
                    w_count = self.get_continuous_count(
                        i, j, 0, -1, 'black', chessboard)  # 左方
                    w_islive = self.get_continuous_is_live(
                        i, j, 0, -1, 'black', chessboard)
                    e_count = self.get_continuous_count(
                        i, j, 0, 1, 'black', chessboard)  # 右方
                    e_islive = self.get_continuous_is_live(
                        i, j, 0, 1, 'black', chessboard)
                    nw_count = self.get_continuous_count(
                        i, j, -1, -1, 'black', chessboard)  # 左上方
                    nw_islive = self.get_continuous_is_live(
                        i, j, -1, -1, 'black', chessboard)
                    ne_count = self.get_continuous_count(
                        i, j, -1, 1, 'black', chessboard)  # 右上方
                    ne_islive = self.get_continuous_is_live(
                        i, j, -1, 1, 'black', chessboard)
                    sw_count = self.get_continuous_count(
                        i, j, 1, -1, 'black', chessboard)  # 左下方
                    sw_islive = self.get_continuous_is_live(
                        i, j, 1, -1, 'black', chessboard)
                    se_count = self.get_continuous_count(
                        i, j, 1, 1, 'black', chessboard)  # 右下方
                    se_islive = self.get_continuous_is_live(
                        i, j, 1, 1, 'black', chessboard)
                    if (n_count + s_count + 1 >= 6) or (e_count + w_count + 1 == 6) or (se_count + nw_count + 1 == 6) or (ne_count + sw_count + 1 == 6):
                        score += -100000000000
                    if (n_count + s_count + 1 == 5) or (e_count + w_count + 1 == 5) or (se_count + nw_count + 1 == 5) or (ne_count + sw_count + 1 == 5):
                        score += -1000000000
                        model.append(("黑连5", i, j))
                    if (n_count + s_count + 1 == 4 or e_count + w_count + 1 == 4 or se_count + nw_count + 1 == 4 or ne_count + sw_count + 1 == 4):
                        if ((n_count == 1 and s_count == 2) or (n_count == 2 and s_count == 1)):
                            score += -8000
                        if ((n_count == 2 and s_count == 1) or (e_count == 1 and w_count == 2)):
                            score += -8000
                        if ((se_count == 2 and nw_count == 1) or (se_count == 1 and nw_count == 2)):
                            score += -8000
                        if ((sw_count == 2 and ne_count == 1) or (ne_count == 1 and sw_count == 2)):
                            score += -8000
                        if (n_count == 3):
                            score += -100000
                            model.append(('黑活4', i, j))
                        if (s_count == 3):
                            score += -100000
                            model.append(('黑活4', i, j))
                        if (e_count == 3):
                            score += -100000
                            model.append(('黑活4', i, j))
                        if (w_count == 3):
                            score += -100000
                            model.append(('黑活4', i, j))
                        if (se_count == 3):
                            score += -100000
                            model.append(('黑活4', i, j))
                        if (nw_count == 3):
                            score += -100000
                            model.append(('黑活4', i, j))
                        if (ne_count == 3):
                            score += -100000
                            model.append(('黑活4', i, j))
                        if (sw_count == 3):
                            score += -100000
                            model.append(('黑活4', i, j))
                    if (n_count + s_count + 1 == 3 or e_count + w_count + 1 == 3 or se_count + nw_count + 1 == 3 or ne_count + sw_count + 1 == 3):
                        if (n_count == 2 and n_islive):
                            score += -8000
                        else:
                            score += -50
                        if (s_count == 2 and s_islive):
                            score += -8000
                        else:
                            score += -50
                        if (e_count == 2 and e_islive):
                            score += -8000
                        else:
                            score += -50
                        if (w_count == 2 and w_islive):
                            score += -8000
                        else:
                            score += -50
                        if (se_count == 2 and se_islive):
                            score += -8000
                        else:
                            score += -50
                        if (nw_count == 2 and nw_islive):
                            score += -8000
                        else:
                            score += -50
                        if (ne_count == 2 and ne_islive):
                            score += -8000
                        else:
                            score += -50
                        if (sw_count == 2) and sw_islive:
                            score += -8000
                        else:
                            score += -50
                    if (n_count + s_count + 1 == 2 or e_count + w_count + 1 == 2 or se_count + nw_count + 1 == 2 or ne_count + sw_count + 1 == 2):
                        if (n_count == 1 and n_islive):
                            score += -50
                        else:
                            score += -3
                        if (s_count == 1 and s_islive):
                            score += -50
                        else:
                            score += -3
                        if (e_count == 1 and e_islive):
                            score += -50
                        else:
                            score += -3
                        if (w_count == 1 and w_islive):
                            score += -50
                        else:
                            score += -3
                        if (se_count == 1 and se_islive):
                            score += -50
                        else:
                            score += -3
                        if (nw_count == 1 and nw_islive):
                            score += -50
                        else:
                            score += -3
                        if (ne_count == 1 and ne_islive):
                            score += -50
                        else:
                            score += -3
                        if (sw_count == 1 and sw_islive):
                            score += -50
                        else:
                            score += -3
                    if (n_count + s_count + 1 == 1 or e_count + w_count + 1 == 1 or se_count + nw_count + 1 == 1 or ne_count + sw_count + 1 == 1):
                        score += -3
        return score, model

    def get_elem(self, elem):
        return elem[0][0]

    def run(self):
        while True:
            if (self.window.has_exit):
                return
            time.sleep(0.01)
            if (self.window.piece == 'white'):
                scores = []
                chessboard = []
                for i in range(self.window.grid_count):
                    chess = []
                    for j in range(self.window.grid_count):
                        chess.append(self.window.grid[i][j])
                    chessboard.append(chess)
                for i in range(self.window.grid_count):
                    for j in range(self.window.grid_count):
                        if (chessboard[i][j] == '.'):
                            chessboard[i][j] = 'white'
                            scores.append(
                                (self.get_score_func(chessboard), i, j))
                            chessboard[i][j] = '.'
                scores.sort(key=self.get_elem, reverse=True)
                cancon = False
                for i in range(len(scores[0][0][1])):
                    if (scores[0][0][1][i][0]=="白连5"):
                        if (self.window.set_piece(scores[0][1], scores[0][2])):
                            self.window.check_win(scores[0][1], scores[0][2])
                            cancon = True
                            break
                    if (scores[0][0][1][i][0]=="白活4"):
                        if (self.window.set_piece(scores[0][0][1][i][1], scores[0][0][1][i][2])):
                            self.window.check_win(scores[0][0][1][i][1], scores[0][0][1][i][2])
                            cancon = True
                            break
                if (cancon):
                    continue
                if (self.window.set_piece(scores[0][1], scores[0][2])):
                    self.window.check_win(scores[0][1], scores[0][2])
