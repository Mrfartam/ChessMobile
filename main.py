from kivy.app import App
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
import numpy
from Chess import *


class MyApp(App):

    def __init__(self, game):
        super().__init__()
        self.game = game
        Window.size = (600, 800)
        wind = str(Window.size)
        self.wid = int(wind[1:wind.find(',')])
        self.hei = int(wind[wind.find(' ') + 1:-1])
        self.razm = (self.wid / self.hei)
        self.fl = FloatLayout()
        self.back = Image(source='Board.png')
        self.btn_mate = Button(text='', size_hint=(1/5, self.razm/10),
                               pos=(2*self.wid/5, self.hei * (1 - self.razm/10)),
                               background_normal='Mate.png', background_down='', font_size=35, bold=True, italic=True,
                               color=[0, 1, 1, 0.5])
        self.btn_exit = Button(text='Выйти', size_hint=(1/5, self.razm/10),
                               pos=(2*self.wid/5, self.hei/2-self.wid/10),
                               background_normal='Start.jpg', background_down='', font_size=35, bold=True,
                               color=[243/255, 14/255, 255/255, 1])
        self.btn_exit.bind(on_press=self.Exit)
        self.btn_start = Button(text='Новая игра', size_hint=(1/5, self.razm/10), pos=(2*self.wid/5, self.hei/2),
                                background_normal='Exit.jpg', background_down='', font_size=35, bold=True,
                                color=[16/255, 1, 81/255, 1])
        self.btn_start.bind(on_press=self.Start)
        pos = [['000' for i in range(8)] for x in range(8)]
        self.position = numpy.array(pos)
        self.imgs = numpy.zeros((8, 8), dtype=Image)
        self.objs = numpy.zeros((8, 8), dtype=Button)
        # self.figures = {"black_king": chr(9812), "black_queen": chr(9813), "black_rook": chr(9814), "black_bishop": chr(9815), "black_knight": chr(9816), "black_pawn": chr(9817), "white_king": chr(9818), "white_queen": chr(9819), "white_rook": chr(9820), "white_bishop": chr(9821), "white_knight": chr(9822), "white_pawn": chr(9823)}
        self.figures = {"black_king": "BK.png", "black_queen": "BQ.png", "black_rook": "BR.png", "black_bishop": "BB.png", "black_knight": "BKN.png", "black_pawn": "BP.png", "white_king": "WK.png", "white_queen": "WQ.png", "white_rook": "WR.png", "white_bishop": "WB.png", "white_knight": "WKN.png", "white_pawn": "WP.png"}
        self.last_move = [None, None]
        self.pawn_move = [[None, None], [None, None]]
        self.trans = FloatLayout()
        self.trans_pawn = numpy.zeros(4, dtype=Image)
        self.pawn_to_knight = Button(size_hint=(0.115, self.razm * 0.115),
                                     pos=(self.wid / 2 - 0.25 * self.wid, 0.06525 * self.wid),
                                     background_down='', background_normal='')
        self.pawn_to_knight.bind(on_press=self.Transformation_KN)
        self.trans.add_widget(self.pawn_to_knight)
        self.pawn_to_bishop = Button(size_hint=(0.115, self.razm * 0.115),
                                     pos=(self.wid / 2 - 0.125 * self.wid, 0.06525 * self.wid),
                                     background_down='', background_normal='')
        self.pawn_to_bishop.bind(on_press=self.Transformation_B)
        self.trans.add_widget(self.pawn_to_bishop)
        self.pawn_to_rook = Button(size_hint=(0.115, self.razm * 0.115),
                                   pos=(self.wid / 2 + 0.01 * self.wid, 0.06525 * self.wid),
                                   background_down='', background_normal='')
        self.pawn_to_rook.bind(on_press=self.Transformation_R)
        self.trans.add_widget(self.pawn_to_rook)
        self.pawn_to_queen = Button(size_hint=(0.115, self.razm * 0.115),
                                    pos=(self.wid / 2 + 0.135 * self.wid, 0.06525 * self.wid),
                                    background_down='', background_normal='')
        self.pawn_to_queen.bind(on_press=self.Transformation_Q)
        self.trans.add_widget(self.pawn_to_queen)

    def Exit(self, z):
        Window.close()

    def Start(self, z):
        self.fl.clear_widgets()
        self.fl.add_widget(self.back)
        self.back.fit_mode = 'fill'
        for i in range(8):
            for j in range(8):
                '''self.objs[j][i] = Button(size_hint=(0.115, self.razm * 0.115),
                                         pos=(0.005 * self.wid + j * self.wid / 8, 0.255 * self.wid + i * self.wid / 8),
                                         background_normal='', background_down='')'''
                self.objs[j][i] = Button(size_hint=(0.115, self.razm * 0.115),
                                         pos=(0.005 * self.wid + j * self.wid / 8, 0.005 * self.wid + i * self.wid / 8),
                                         background_normal='', background_down='')
                self.objs[j][i].bind(on_press=self.Click)
                self.fl.add_widget(self.objs[j][i])
        self.Standart_board()
        self.position[0][0] = self.position[7][0] = "WR"
        self.position[1][0] = self.position[6][0] = "WB"
        self.position[2][0] = self.position[5][0] = "WKN"
        self.position[3][0] = "WQ"
        self.position[4][0] = "WK"
        for i in range(8):
            self.position[i][1] = "WP"
        self.position[0][7] = self.position[7][7] = "BR"
        self.position[1][7] = self.position[6][7] = "BB"
        self.position[2][7] = self.position[5][7] = "BKN"
        self.position[3][7] = "BQ"
        self.position[4][7] = "BK"
        for i in range(8):
            self.position[i][6] = "BP"
        self.Create(self.position)
        self.fl.add_widget(self.btn_mate)

    def Click(self, cell):
        '''x, y = int(cell.pos[0] - self.wid * 0.005) * 8 // self.wid, int(cell.pos[1] - self.wid * 0.255) * 8 // self.wid'''
        x, y = int(cell.pos[0] - self.wid * 0.005) * 8 // self.wid, int(cell.pos[1] - self.wid * 0.005) * 8 // self.wid
        x_old, y_old = self.last_move
        print(x, y)
        if x == x_old and y == y_old:
            self.Standart_board()
        active_cell = True if self.objs[x][y].background_color == [0, 1, 0, 0.5] else False
        if not active_cell:
            # self.Get_motion()
            self.Standart_board()
            type = self.position[x][y]
            self.last_move = [x, y]
            if type[0] == "B" and game.status_game == 1:
                # x,y - coordinate new figure
                # ищем фигуру и получаем возможные действия
                figure = game.search_board([7 - y, x])
                interactive_motion = figure.motion(self.game)
                for i in interactive_motion:
                    self.objs[i[1]][7 - i[0]].background_color = [0, 1, 0, 0.5]
            if type[0] == "W" and game.status_game == -1:
                # x,y - coordinate new figure
                # ищем фигуру и получаем возможные действия
                figure = game.search_board([7 - y, x])
                interactive_motion = figure.motion(self.game)

                for i in interactive_motion:
                    self.objs[i[1]][7 - i[0]].background_color = [0, 1, 0, 0.5]
        else:
            self.Standart_board()
            #изщменение в маину
            figure = game.search_board([7 - y_old, x_old])

            if self.position[x_old][y_old][1] == 'P':
                if y_old == 6 and game.status_game == -1:
                    self.pawn_move = [[x_old, y_old], [x, y]]
                    self.Begin_transformation('W')
                    return
                elif y_old == 1 and game.status_game == 1:
                    self.pawn_move = [[x_old, y_old], [x, y]]
                    self.Begin_transformation('B')
                    return

            figure.interactive([7 - y, x], [7 - y_old, x_old], game)

            if figure.gettype == "King":
                if figure.rook == 1:
                    #1 - short
                    if game.status_game == 1:
                        #white
                        self.position[5][0] = self.position[7][0]
                        self.position[7][0] = '000'
                    elif game.status_game == -1:
                        self.position[5][7] = self.position[7][7]
                        self.position[7][7] = '000'
                elif figure.rook == 2:
                    #2 - long
                    if game.status_game == -1:
                        if game.status_game == 1:
                            # white
                            self.position[3][0] = self.position[7][0]
                            self.position[7][0] = '000'
                        elif game.status_game == -1:
                            self.position[3][7] = self.position[7][7]
                            self.position[7][7] = '000'
            self.position[x][y] = self.position[x_old][y_old]
            self.position[x_old][y_old] = '000'
            self.Delete()
            self.Create(self.position)
            self.last_move = [x, y]

    def Begin_transformation(self, color):
        if color == 'W':
            self.trans_pawn[0] = Image(source=self.figures['white_knight'], size_hint=self.pawn_to_knight.size_hint, pos=self.pawn_to_knight.pos)
            self.trans_pawn[1] = Image(source=self.figures['white_bishop'], size_hint=self.pawn_to_bishop.size_hint, pos=self.pawn_to_bishop.pos)
            self.trans_pawn[2] = Image(source=self.figures['white_rook'], size_hint=self.pawn_to_rook.size_hint, pos=self.pawn_to_rook.pos)
            self.trans_pawn[3] = Image(source=self.figures['white_queen'], size_hint=self.pawn_to_queen.size_hint, pos=self.pawn_to_queen.pos)
        elif color == 'B':
            self.trans_pawn[0] = Image(source=self.figures['black_knight'], size_hint=self.pawn_to_knight.size_hint, pos=self.pawn_to_knight.pos)
            self.trans_pawn[1] = Image(source=self.figures['black_bishop'], size_hint=self.pawn_to_bishop.size_hint, pos=self.pawn_to_bishop.pos)
            self.trans_pawn[2] = Image(source=self.figures['black_rook'], size_hint=self.pawn_to_rook.size_hint, pos=self.pawn_to_rook.pos)
            self.trans_pawn[3] = Image(source=self.figures['black_queen'], size_hint=self.pawn_to_queen.size_hint, pos=self.pawn_to_queen.pos)
        for tr in self.trans_pawn:
            self.trans.add_widget(tr)
        self.fl.add_widget(self.trans)

    def Transformation_KN(self, z):
        x_old, y_old = self.pawn_move[0]
        x, y = self.pawn_move[1]
        figure = game.search_board([7 - y_old, x_old])
        figure.interactive([7 - y, x], [7 - y_old, x_old], game, "Bishop")
        for tr in self.trans_pawn:
            self.trans.remove_widget(tr)
        self.fl.remove_widget(self.trans)
        if y_old == 6:
            self.position[x][y] = 'WKN'
        elif y_old == 1:
            self.position[x][y] = 'BKN'
        self.position[x_old][y_old] = '000'
        self.Delete()
        self.Create(self.position)
        self.last_move = [x, y]
        a = Button()

    def Transformation_B(self, z):
        x_old, y_old = self.pawn_move[0]
        x, y = self.pawn_move[1]
        figure = game.search_board([7 - y_old, x_old])
        figure.interactive([7 - y, x], [7 - y_old, x_old], game, "Knight")
        for tr in self.trans_pawn:
            self.trans.remove_widget(tr)
        self.fl.remove_widget(self.trans)
        if y_old == 6:
            self.position[x][y] = 'WB'
        elif y_old == 1:
            self.position[x][y] = 'BB'
        self.position[x_old][y_old] = '000'
        self.Delete()
        self.Create(self.position)
        self.last_move = [x, y]

    def Transformation_R(self, z):
        x_old, y_old = self.pawn_move[0]
        x, y = self.pawn_move[1]
        figure = game.search_board([7 - y_old, x_old])
        figure.interactive([7 - y, x], [7 - y_old, x_old], game, "Rook")
        for tr in self.trans_pawn:
            self.trans.remove_widget(tr)
        self.fl.remove_widget(self.trans)
        if y_old == 6:
            self.position[x][y] = 'WR'
        elif y_old == 1:
            self.position[x][y] = 'BR'
        self.position[x_old][y_old] = '000'
        self.Delete()
        self.Create(self.position)
        self.last_move = [x, y]

    def Transformation_Q(self, z):
        x_old, y_old = self.pawn_move[0]
        x, y = self.pawn_move[1]
        figure = game.search_board([7 - y_old, x_old])
        figure.interactive([7 - y, x], [7 - y_old, x_old], game, "Queen")
        for tr in self.trans_pawn:
            self.trans.remove_widget(tr)
        self.fl.remove_widget(self.trans)
        if y_old == 6:
            self.position[x][y] = 'WQ'
        elif y_old == 1:
            self.position[x][y] = 'BQ'
        self.position[x_old][y_old] = '000'
        self.Delete()
        self.Create(self.position)
        self.last_move = [x, y]

    def Standart_board(self):
        for x in range(8):
            for y in range(8):
                if (x + y) % 2:
                    self.objs[x][y].background_color = [184/255, 161/255, 107/255, 1]
                    self.objs[x][y].background_normal = 'WhiteCell.png'
                else:
                    self.objs[x][y].background_color = [115/255, 65/225, 33/255, 1]
                    self.objs[x][y].background_normal = 'BlackCell.png'

    def Delete(self):
        for x in range(8):
            for y in range(8):
                if self.imgs[x][y]:
                    self.fl.remove_widget(self.imgs[x][y])

    def Create(self, position):
        for x in range(8):
            for y in range(8):
                if position[x][y] == 'BP':
                    self.imgs[x][y] = Image(source=self.figures['black_pawn'], size_hint=self.objs[x][y].size_hint, pos=self.objs[x][y].pos)
                    self.fl.add_widget(self.imgs[x][y])
                elif position[x][y] == 'BQ':
                    self.imgs[x][y] = Image(source=self.figures['black_queen'], size_hint=self.objs[x][y].size_hint, pos=self.objs[x][y].pos)
                    self.fl.add_widget(self.imgs[x][y])
                elif position[x][y] == 'BK':
                    self.imgs[x][y] = Image(source=self.figures['black_king'], size_hint=self.objs[x][y].size_hint, pos=self.objs[x][y].pos)
                    self.fl.add_widget(self.imgs[x][y])
                elif position[x][y] == 'BB':
                    self.imgs[x][y] = Image(source=self.figures['black_bishop'], size_hint=self.objs[x][y].size_hint, pos=self.objs[x][y].pos)
                    self.fl.add_widget(self.imgs[x][y])
                elif position[x][y] == 'BKN':
                    self.imgs[x][y] = Image(source=self.figures['black_knight'], size_hint=self.objs[x][y].size_hint, pos=self.objs[x][y].pos)
                    self.fl.add_widget(self.imgs[x][y])
                elif position[x][y] == 'BR':
                    self.imgs[x][y] = Image(source=self.figures['black_rook'], size_hint=self.objs[x][y].size_hint, pos=self.objs[x][y].pos)
                    self.fl.add_widget(self.imgs[x][y])
                elif position[x][y] == 'WP':
                    self.imgs[x][y] = Image(source=self.figures['white_pawn'], size_hint=self.objs[x][y].size_hint,
                                pos=self.objs[x][y].pos)
                    self.fl.add_widget(self.imgs[x][y])
                elif position[x][y] == 'WQ':
                    self.imgs[x][y] = Image(source=self.figures['white_queen'], size_hint=self.objs[x][y].size_hint,
                                pos=self.objs[x][y].pos)
                    self.fl.add_widget(self.imgs[x][y])
                elif position[x][y] == 'WK':
                    self.imgs[x][y] = Image(source=self.figures['white_king'], size_hint=self.objs[x][y].size_hint,
                                pos=self.objs[x][y].pos)
                    self.fl.add_widget(self.imgs[x][y])
                elif position[x][y] == 'WB':
                    self.imgs[x][y] = Image(source=self.figures['white_bishop'], size_hint=self.objs[x][y].size_hint,
                                pos=self.objs[x][y].pos)
                    self.fl.add_widget(self.imgs[x][y])
                elif position[x][y] == 'WKN':
                    self.imgs[x][y] = Image(source=self.figures['white_knight'], size_hint=self.objs[x][y].size_hint,
                                pos=self.objs[x][y].pos)
                    self.fl.add_widget(self.imgs[x][y])
                elif position[x][y] == 'WR':
                    self.imgs[x][y] = Image(source=self.figures['white_rook'], size_hint=self.objs[x][y].size_hint,
                                pos=self.objs[x][y].pos)
                    self.fl.add_widget(self.imgs[x][y])

    def build(self):
        self.fl.add_widget(self.back)
        self.back.fit_mode = 'fill'
        self.fl.add_widget(self.btn_exit)
        self.fl.add_widget(self.btn_start)
        return self.fl

black_stuff = [0]*16

for i in range(8):
    black_stuff[i] = Pawn([6, i], -1)

black_stuff[8] = Rook([7, 0], -1)
black_stuff[9] = Rook([7, 7], -1)
black_stuff[10] = Knight([7,1], -1)
black_stuff[11] = Knight([7,6], -1)
black_stuff[12] = Bishop([7,2], -1)
black_stuff[13] = Bishop([7,5], -1)
black_stuff[14] = Queen([7,3], -1)
black_stuff[15] = King([7,4], -1)


white_stuff = [0]*16
for i in range(8):
    white_stuff[i] = Pawn([1, i], 1)

white_stuff[8] = Rook([0,0], 1)
white_stuff[9] = Rook([0,7], 1)
white_stuff[10] = Knight([0,1], 1)
white_stuff[11] = Knight([0,6], 1)
white_stuff[12] = Bishop([0,2], 1)
white_stuff[13] = Bishop([0,5], 1)
white_stuff[14] = Queen([0,3], 1)
white_stuff[15] = King([0,4], 1)

game = Board(black_stuff, white_stuff)
game.build()

if __name__ == '__main__':
    MyApp(game).run()