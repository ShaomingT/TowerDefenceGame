import advanced_view as av
import math
import tkinter as tk
from tkinter import ttk
from copy import copy
from tower import AbstractTower, MissileTower, PulseTower, SimpleTower, \
    AbstractObstacle, Missile, Pulse
from enhanced_tower import EnergyTower, Energy, BlazarTower, Gravity
import view

__author__ = "Alex Teng"

COLOUR = "#333366"


class ShopView(tk.Frame):
    """Shop view located in the right side of the main window"""
    _bg = COLOUR
    _fg = "white"
    _icon_width = 55

    _indent = 30
    tower_position = (_icon_width / 2, _icon_width / 2)
    tower_rotation = 0.8

    _towers = {
        "simple_tower": SimpleTower(_icon_width),
        "missile_tower": MissileTower(_icon_width),
        "pulse_tower": PulseTower(_icon_width),
        "energy_tower": EnergyTower(_icon_width),
        "blazar_tower": BlazarTower(_icon_width)}

    def __init__(self, master, parent, upgrade_instruc_view):
        """Intialize each shop view.
         """

        super().__init__(master)
        self._master = master
        self._parent = parent
        self._upgrade_instruc_view = upgrade_instruc_view

        self.tower_view = Enhanced_TowerView
        parent.select_tower(SimpleTower)

        # Initialise simple tower shop view, the following are similar
        self._simple_shop_frame = tk.Frame(self, bg=self._bg)
        self._simple_shop_frame.pack(side=tk.TOP, fill=tk.BOTH)

        self._missile_shop_frame = tk.Frame(self, bg=self._bg)
        self._missile_shop_frame.pack(side=tk.TOP, fill=tk.BOTH)

        self._pulse_shop_frame = tk.Frame(self, bg=self._bg)
        self._pulse_shop_frame.pack(side=tk.TOP, fill=tk.BOTH)

        self._energy_shop_frame = tk.Frame(self, bg=self._bg)
        self._energy_shop_frame.pack(side=tk.TOP, fill=tk.BOTH)

        self._blazar_shop_frame = tk.Frame(self, bg=self._bg)
        self._blazar_shop_frame.pack(side=tk.TOP, fill=tk.BOTH)

        # Change the position of the tower view in vancas
        for t in self._towers:
            self._towers[t].position = self.tower_position
            self._towers[t].rotation = self.tower_rotation
            # self._towers[t].cell_size = self._icon_width - 5

        # Initialise canvas
        self.init_simple()
        self.init_missile()
        self.init_pulse()
        self.init_energy()
        self.init_blazar()

        # bind mouse event.
        self.bind_frame()

    def init_simple(self):
        """initialize the simple tower canvas"""
        self._simple_icon = tk.Canvas(self._simple_shop_frame,
                                      width=self._icon_width,
                                      height=self._icon_width,
                                      bg=self._bg,
                                      highlightthickness=0)
        self.tower_view.draw(self._simple_icon, self._towers["simple_tower"])
        self._simple_icon.pack(side=tk.LEFT, padx=self._indent)
        self._simple_label_text = tk.Label(self._simple_shop_frame,
                                           text="Simple Tower\n40 coins",
                                           bg=self._bg,
                                           fg=self._fg)
        self._simple_label_text.pack(side=tk.LEFT, )

    def init_missile(self):
        """Initialize the missile tower canvas"""
        self._missile_icon = tk.Canvas(self._missile_shop_frame,
                                       width=self._icon_width,
                                       height=self._icon_width,
                                       bg=self._bg,
                                       highlightthickness=0)
        self.tower_view.draw(self._missile_icon, self._towers["missile_tower"])
        self._missile_icon.pack(side=tk.LEFT, padx=self._indent)
        self._missile_label_text = tk.Label(self._missile_shop_frame,
                                            text="Missile Tower\n80 coins",
                                            bg=self._bg,
                                            fg=self._fg)
        self._missile_label_text.pack(side=tk.LEFT, )

    def init_pulse(self):
        """Initialize the pulse tower canvas"""
        self._pulse_icon = tk.Canvas(self._pulse_shop_frame,
                                     width=self._icon_width,
                                     height=self._icon_width,
                                     bg=self._bg,
                                     highlightthickness=0)
        self.tower_view.draw(self._pulse_icon, self._towers["pulse_tower"])
        self._pulse_icon.pack(side=tk.LEFT, padx=self._indent)

        self._pulse_label_text = tk.Label(self._pulse_shop_frame,
                                          text="Pulse Tower\n120 coins", bg=self._bg,
                                          fg=self._fg)
        self._pulse_label_text.pack(side=tk.LEFT, )

    def init_energy(self):
        """Initialize the energy tower shop view"""
        self._energy_icon = tk.Canvas(self._energy_shop_frame,
                                      width=self._icon_width,
                                      height=self._icon_width,
                                      bg=self._bg,
                                      highlightthickness=0)
        self.tower_view.draw(self._energy_icon, self._towers["energy_tower"])
        self._energy_icon.pack(side=tk.LEFT, padx=self._indent)
        self._energy_label_text = tk.Label(self._energy_shop_frame,
                                           text="Energy Tower\n200 coins",
                                           bg=self._bg,
                                           fg=self._fg)
        self._energy_label_text.pack(side=tk.LEFT, )

    def init_blazar(self):
        """Initialize the blazar tower shop view"""
        self._blazar_icon = tk.Canvas(self._blazar_shop_frame,
                                      width=self._icon_width,
                                      height=self._icon_width,
                                      bg=self._bg,
                                      highlightthickness=0)
        self.tower_view.draw(self._blazar_icon, self._towers["blazar_tower"])
        self._blazar_icon.pack(side=tk.LEFT, padx=self._indent)
        self._blazar_label_text = tk.Label(self._blazar_shop_frame,
                                           text="Blazar Tower\n5000 coins",
                                           bg=self._bg,
                                           fg=self._fg)
        self._blazar_label_text.pack(side=tk.LEFT)

    def bind_frame(self):
        # give bind tag to widgets
        self.retag("SimpleTower", self._simple_shop_frame, self._simple_icon, self._simple_label_text)
        self.retag("MissileTower", self._missile_shop_frame, self._missile_icon, self._missile_label_text)
        self.retag("PulseTower", self._pulse_shop_frame, self._pulse_icon, self._pulse_label_text)
        self.retag("EnergyTower", self._energy_shop_frame, self._energy_icon, self._energy_label_text)
        self.retag("BlazarTower", self._blazar_shop_frame, self._blazar_icon, self._blazar_label_text)

        # Bind!!!!!
        self._simple_shop_frame.bind_class("SimpleTower", "<Button-1>",
                                           lambda event, arg="SimpleTower": self._select_tower(event, arg))

        self._simple_shop_frame.bind_class("SimpleTower", "<Button-2>",
                                           lambda event, arg=None: self._select_tower(event, arg))

        self._missile_shop_frame.bind_class("MissileTower", "<Button-1>",
                                            lambda event, arg="MissileTower": self._select_tower(event, arg))

        self._missile_shop_frame.bind_class("MissileTower", "<Button-2>",
                                            lambda event, arg=None: self._select_tower(event, arg))

        self._pulse_shop_frame.bind_class("PulseTower", "<Button-1>",
                                          lambda event, arg="PulseTower": self._select_tower(event, arg))
        self._pulse_shop_frame.bind_class("PulseTower", "<Button-2>",
                                          lambda event, arg=None: self._select_tower(event, arg))

        self._energy_shop_frame.bind_class("EnergyTower", "<Button-1>",
                                           lambda event, arg="EnergyTower": self._select_tower(event, arg))
        self._energy_shop_frame.bind_class("EnergyTower", "<Button-2>",
                                           lambda event, arg=None: self._select_tower(event, arg))

        self._blazar_shop_frame.bind_class("BlazarTower", "<Button-1>",
                                           lambda event, arg="BlazarTower": self._select_tower(event, arg))
        self._blazar_shop_frame.bind_class("BlazarTower", "<Button-2>",
                                           lambda event, arg=None: self._select_tower(event, arg))

    def retag(self, tag, *args):
        '''Add the given tag as the first bindtag for every widget passed in'''
        for widget in args:
            widget.bindtags((tag,) + widget.bindtags())

    def _select_tower(self, event, tower):
        """Select tower"""
        if tower is None:
            self._parent._current_tower = None
        else:
            towers = {"SimpleTower": SimpleTower,
                      "MissileTower": MissileTower,
                      "PulseTower": PulseTower,
                      "EnergyTower": EnergyTower,
                      "BlazarTower": BlazarTower}

            self._parent.select_tower(towers[tower])


class StatusBar(tk.Frame):
    """The status Bar view located in the top-right side"""

    # _wave = None
    # _score = None

    def __init__(self, master, parent):
        """Initialize the sub frames in status bar frame """
        super().__init__(master)
        self._parent = parent
        self._coins_image = tk.PhotoImage(file="images/coins.gif")
        self._lives_image = tk.PhotoImage(file="images/heart.gif")

        self._basic_frame = tk.Frame(self)
        self._basic_frame.pack(side=tk.TOP, expand=True, fill=tk.X)

        self._coins_lives_frame = tk.Frame(self)
        self._coins_lives_frame.grid_propagate(0)
        self._coins_lives_frame.pack(side=tk.TOP, fill=tk.X, expand=True)

        self._init_basic_frame()
        self._init_coins_lives_frame()

    def _init_basic_frame(self):
        """Initialize basic frame that contains sub frames"""
        self._wave = tk.Label(self._basic_frame, text="", )
        self._wave.pack(side=tk.TOP)

        self._score = tk.Label(self._basic_frame, text="")
        self._score.pack(side=tk.TOP)

    def _init_coins_lives_frame(self):
        """Initialize Coins and Lives frames"""
        _gold_frame = tk.Frame(self._coins_lives_frame)
        _gold_frame.pack(side=tk.LEFT, fill=tk.X, anchor=tk.W)

        _lives_frame = tk.Frame(self._coins_lives_frame)
        _lives_frame.pack(side=tk.RIGHT, fill=tk.X)

        self._gold_img_lab = tk.Label(_gold_frame, image=self._coins_image)
        self._gold_img_lab.pack(side=tk.LEFT, anchor=tk.W)

        self._gold = tk.Label(_gold_frame, text="")
        self._gold.pack(side=tk.LEFT, anchor=tk.W)

        self._lives_img_lab = tk.Label(_lives_frame, image=self._lives_image)
        self._lives_img_lab.pack(side=tk.LEFT, )

        self._lives = tk.Label(_lives_frame, text="")
        self._lives.pack(side=tk.LEFT)

    def set_wave(self, wave):
        """Set View"""
        self._wave.config(text="Wave: {}/{}".format(str(wave), self._parent._level.waves))

    def set_score(self, score):
        """Set socre"""
        self._score.config(text="{}".format(str(int(score))))

    def set_gold(self, gold):
        """Set coins"""
        self._gold.config(text="{}".format(str(int(gold))))

    def set_lives(self, lives):
        """Set Lives"""
        self._lives.config(text="{}".format(str(lives)))

    def set_all(self, wave, score, gold, lives):
        """Set wave, score, gold, lives at once"""
        self.set_wave(wave)
        self.set_score(score)
        self.set_gold(gold)
        self.set_lives(lives)


class Upgrade_and_Instruction_View(tk.Frame):
    """Upgrade and instruction view. Be displaied when click a existened tower."""
    _check_box_status = False
    _cost = 0
    _sufficient = ""

    def __init__(self, master, parent):
        """Initialise the basic frame and it's sub frame."""
        super().__init__(master)
        self._master = master
        self._parent = parent

        self._help_frame = tk.Frame(parent.upgrade_frame, bg=COLOUR)
        self._help_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self._info = tk.Label(self._help_frame, text='', justify=tk.LEFT, fg="white", bg=COLOUR)
        self._info.pack(side=tk.TOP, anchor=tk.NW)
        self._movingtower = None

    def show_detailed_upgraded_info(self):
        """show upgrade information"""

        if self._parent._selected_tower is None:
            self._info.config(text="""Not Selected""")
            if self._parent._moving_tower is None:
                self._info.config(text="""Not Selected""")
                return

        current_name = self._parent._selected_tower.name
        current_value = self._parent._selected_tower.get_value()
        current_level = self._parent._selected_tower.level
        current_damage = self._parent._selected_tower.get_damage()
        current_cool_down = self._parent._selected_tower.cool_down_steps

        if self._parent._selected_tower.highest_level == True:
            self._info.config(
                text=
                f'''        Cannot upgrade
        Tower Type:   {current_name}
        Value:               {current_value}
        Damage:           {current_damage}
        Cood Down Step:       {current_cool_down}
        Already highest level
        ''')
            return

        upgraded_tower = copy(self._parent._selected_tower)
        upgraded_tower.level += 1
        upgraded_cost = upgraded_tower.level_cost
        upgraded_value = upgraded_tower.get_value()
        upgraded_level = upgraded_tower.level
        upgraded_damage = upgraded_tower.get_damage()

        # if self._parent._coins < upgraded_cost:
        self._info.config(
            text=
            f'''        Click To Upgrade
    Tower Type:   {current_name}
    Value:               {current_value} --> {upgraded_value}
    Damage:           {current_damage} --> {upgraded_damage}
    Cood Down Step:       {current_cool_down-1}
    cost:                   {self._cost}
                            {self._sufficient}''')

    def show_upgrade_check_box(self):
        """display the upgrade chaeck box"""

        self.del_check_when_exist()
        self._check_box_status = True

        self.show_detailed_upgraded_info()
        self.reduce_cd = tk.IntVar()
        self.increase_dam = tk.IntVar()

        self.rc_cb = tk.Checkbutton(self._help_frame, text="Reduced CD", variable=self.reduce_cd,
                                    command=self.display_cost)
        if self._parent._selected_tower.cool_down_steps <= 1:
            self.rc_cb.config(state=tk.DISABLED)

        self.in_da = tk.Checkbutton(self._help_frame, text="Increase Damage", variable=self.increase_dam,
                                    command=self.display_cost, )

        self.ugrade_button = tk.Button(self._help_frame, text="Upgrade", command=self.judge_upgrade, width=10)
        self.cancel_button = tk.Button(self._help_frame, text="Cancel", command=self.delete_check_box, width=10)
        self.rc_cb.pack(fill=tk.X)
        self.in_da.pack(fill=tk.X)
        self.ugrade_button.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        self.cancel_button.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        if self._parent._selected_tower.name == "Blazar Tower":
            self._info.config(text="One Blazar Tower Can only be used once\n No upgrade option \n\n\n\n\n")
            self.rc_cb.config(state=tk.DISABLED)
            self.reduce_cd.set(0)
            self.in_da.config(state=tk.DISABLED)
            self.increase_dam.set(0)
            self.ugrade_button.config(state=tk.DISABLED)
            return

    def display_cost(self):
        """display the cost by the states of the check boxes"""

        cd = self.reduce_cd.get()
        damage = self.increase_dam.get()
        cost = 0
        print(self._parent._selected_tower.cool_down_steps)
        if self._parent._selected_tower.cool_down_steps <= 1:
            print("sds")
            self.rc_cb.config(state=tk.DISABLED)
            self.reduce_cd.set(0)

        if cd:
            cost += self._parent._selected_tower.get_value() * 5
        if damage:
            cost += self._parent._selected_tower.level_cost * self._parent._selected_tower.level

        self._cost = cost

        if self._parent._selected_tower.level >= 15:
            self.in_da.config(state=tk.DISABLED)
            self.increase_dam.set(0)
            self._parent._selected_tower.highest_level = True
            self.show_detailed_upgraded_info()
            return

        if self._parent._coins < cost:
            self._sufficient = """Insufficient Funds"""

        self.show_detailed_upgraded_info()

    def judge_upgrade(self):
        """Check whether the upgrade can be processed or not"""
        self.display_cost()
        cd = self.reduce_cd.get()
        damage = self.increase_dam.get()

        if self._parent._coins < self._cost:
            self._sufficient = """Insufficient Funds"""

        else:
            if cd:
                self._parent._selected_tower.cool_down_steps -= 1
            if damage:
                self._parent._selected_tower.level += 1

            self._parent._coins -= self._cost

            self.show_detailed_upgraded_info()

    def delete_check_box(self):
        """forget the check boxes"""
        self._check_box_status = False
        self.rc_cb.pack_forget()
        self.in_da.pack_forget()
        self.ugrade_button.pack_forget()
        self.cancel_button.pack_forget()
        self._info.config(text="")
        self._cost = 0

    def delete_all(self):
        """Delete all info that is displaing"""
        self.del_check_when_exist()
        self._info.config(text="")

    def del_check_when_exist(self):
        """delete the checkbox view when it is existing"""
        if self._check_box_status == False:
            return
        else:
            self.delete_check_box()


class ScoreBoard(object):
    """Score Board class, display a child window to show the score and ranking."""

    def __init__(self, master, _score_board_manag):
        """Construct a score board window.
        Parameters:
            master(Tk): Window to place the score board.
            """
        self._master = master
        self._score_board_manag = _score_board_manag

    def show_window(self):
        """Display Scoreboard Window"""
        scoreboard = tk.Toplevel(self._master)
        scoreboard.resizable(width=False, height=False)
        entries = self._score_board_manag.get_entries()
        tree = ttk.Treeview(scoreboard)

        tree["columns"] = ("Ranking", "Name", "Score")
        tree['show'] = 'headings'

        tree.column("Ranking", width=100)
        tree.column("Name", width=100)
        tree.column("Score", width=100)

        tree.heading("Ranking", text="Ranking")
        tree.heading("Name", text="Name")
        tree.heading("Score", text="Score")

        for i in range(len(entries)):
            tree.insert("", i, text=i + 1, values=(str(i + 1), entries[i]['name'], entries[i]['score']))

        tree.pack(side=tk.TOP)

        tk.Button(scoreboard, text='OK', command=self._score_board_destory).pack(side=tk.TOP)
        self.scoreboard = scoreboard

    def _score_board_destory(self):
        """Cloase score board child window."""
        self.scoreboard.destroy()

    def get_score_board_manag(self):
        """Return score_board_manager class
        Return(HighScoreManager): Return High Score Manager
        """
        return self.get_score_board_manag()


class Game_Over_Box(object):
    """Game Over Box, display a child window to display game over"""

    def __init__(self, master, parent, score_board_manag):
        self._master = master
        self._parent = parent
        self._score_board_manag = score_board_manag

    def _show_game_over_box(self, _won):
        """Dis the game over box in a child window"""
        self.gameoverwin = tk.Toplevel(self._parent._view)

        if _won:
            l = tk.Label(self.gameoverwin, text="Congrulation, You Won.\n Enter your name.")
            l.pack()
        else:
            l = tk.Label(self.gameoverwin, text="Game Over\n Enter your name.")
            l.pack()

        self.e = tk.Entry(self.gameoverwin)
        self.e.pack()

        b = tk.Button(self.gameoverwin, text='Ok', command=self.destory)
        b.pack()

    def destory(self):
        """Distory the the child window"""
        current_name = self.e.get()
        if self._score_board_manag.does_score_qualify(self._parent._score):
            self._score_board_manag.add_entry(current_name, self._parent._score)
            self._score_board_manag.save()

        self._parent._restart_all_game()
        self.gameoverwin.destroy()


class Enhanced_TowerView(av.TowerView):
    draw_methods = av.sort_draw_methods([
        (SimpleTower, '_draw_simple'),
        (MissileTower, '_draw_missile'),
        (PulseTower, '_draw_pulse'),
        (EnergyTower, '_draw_energy'),
        (BlazarTower, '_draw_blazar'),
        (AbstractTower, '_draw_simple'),
    ])

    @classmethod
    def _draw_pulse(cls, canvas: tk.Canvas, tower_: SimpleTower):
        """Draws a pulse tower"""

        x, y = tower_.position

        x_diameter, y_diameter = tower_.grid_size
        top_left, bottom_right = tower_.get_bounding_box()

        cell_size = tower_.cell_size

        colour = tower_.colour

        body = canvas.create_oval(top_left, bottom_right, tag='tower', fill=colour, width=tower_.level*0.5)
        tags = [body]

        angle_step = math.pi / 2
        for i in range(4):
            angle = i * angle_step

            dx = (x_diameter / 2) * cell_size * math.cos(angle)
            dy = (y_diameter / 2) * cell_size * math.sin(angle)

            tag = canvas.create_line(x + dx / 2, y + dy / 2, x + dx, y + dy, tag='tower', width=tower_.level * 0.5)

            tags.append(tag)

        return tags

    @classmethod
    def _draw_missile(cls, canvas: tk.Canvas, tower_: MissileTower):
        """Draws a missile tower"""

        x, y = tower_.position
        angle = tower_.rotation

        x_diameter, y_diameter = tower_.grid_size
        top_left, bottom_right = tower_.get_bounding_box()

        cell_size = tower_.cell_size

        colour = tower_.colour

        body = canvas.create_oval(top_left, bottom_right, tag='tower', fill=colour, width=tower_.level*0.5)

        tags = [body]

        for delta_angle in (-math.pi / 12, math.pi / 12):
            tags.append(
                canvas.create_line(x, y, x + (x_diameter / 2) * cell_size * math.cos(angle + delta_angle),
                                   y + (y_diameter / 2) * cell_size * math.sin(angle + delta_angle),
                                   width=tower_.level * 0.5,
                                   tag='tower')
            )

        return tags

    @classmethod
    def _draw_energy(cls, canvas: tk.Canvas, tower_: EnergyTower):
        """Draws a energy tower"""

        x, y = tower_.position
        angle = tower_.rotation

        x_diameter, y_diameter = tower_.grid_size
        top_left, bottom_right = tower_.get_bounding_box()

        cell_size = tower_.cell_size

        colour = tower_.colour

        body = canvas.create_oval(top_left, bottom_right, tag='tower', fill=colour, width=tower_.level)

        tags = [body]

        for delta_angle in (-math.pi / 12, math.pi / 12):
            tags.append(
                canvas.create_line(x, y, x + (x_diameter / 2) * cell_size * math.cos(angle + delta_angle),
                                   y + (y_diameter / 2) * cell_size * math.sin(angle + delta_angle),
                                   x + (x_diameter / 1.5) * cell_size * math.cos(angle),
                                   y + (y_diameter / 1.5) * cell_size * math.sin(angle), width=tower_.level * 0.3,
                                   tag='tower')
            )

        return tags

    @classmethod
    def _draw_blazar(cls, canvas: tk.Canvas, tower_: BlazarTower):
        """Draws blazae tower"""

        top_left, bottom_right = tower_.get_bounding_box()

        vi = []
        colour = ['black', 'white']
        colour_num = 0
        dis = 4
        for i in range(5):
            vi.append(canvas.create_oval(top_left, bottom_right, fill=colour[colour_num], tag='tower'))
            # dis += 5

            top_left = top_left[0] + dis, top_left[1] + dis
            bottom_right = bottom_right[0] - dis, bottom_right[1] - dis

            colour_num += 1
            if colour_num >= len(colour):
                colour_num = 0

        return vi


class Enhanced_ObstacleView(av.ObstacleView):
    draw_methods = av.sort_draw_methods([
        (AbstractObstacle, '_draw_invisible'),
        (Missile, '_draw_missile'),
        (Pulse, '_draw_pulse'),
        (Energy, '_draw_energy'),
        (Gravity, '_draw_gravity')
    ])

    @classmethod
    def _draw_gravity(cls, canvas: tk.Canvas, gravity: Gravity):
        """Draws a gravity"""

        x, y = gravity.position
        radius = 40
        large_radius = 210
        colour_num = 0

        graviry_effects = []
        con = True
        for i in range(gravity.layer):
            if con is True:
                large_radius -= 14
            else:
                large_radius += 14

            if large_radius <= radius:
                con = False

            head = x + large_radius, y + large_radius
            tail = x - large_radius, y - large_radius

            graviry_effects.append(canvas.create_oval(head, tail, fill=gravity.colour[colour_num], tag='obstacle'))
            colour_num += 1

            if colour_num >= len(gravity.colour):
                colour_num = 0

        return graviry_effects  # canvas.create_oval(head, tail, fill=gravity.colour[0], tag='obstacle')

    @classmethod
    def _draw_energy(cls, canvas: tk.Canvas, energy: Energy):
        """Draws a energy"""

        x, y = energy.position
        radius = energy.size[0]

        head = x + radius, y + radius
        tail = x - radius, y - radius

        return canvas.create_oval(head, tail, fill=energy.colour, tag='obstacle'),


class Enhanced_GameView(view.GameView):
    def __init__(self, master, *args, size=(6, 6), cell_size=40,
                 tower_view_class=Enhanced_TowerView, range_view_class=None,
                 enemy_view_class=None, obstacle_view_class=Enhanced_ObstacleView,
                 **kwargs):
        super().__init__(master, *args, size=size, cell_size=cell_size,
                         tower_view_class=Enhanced_TowerView, obstacle_view_class=Enhanced_ObstacleView,
                         **kwargs)
