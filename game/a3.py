import tkinter as tk
from enhanced_view import ShopView, StatusBar, Upgrade_and_Instruction_View, ScoreBoard, Game_Over_Box
from enhanced_object import MyLevel
from tkinter import messagebox
from model import TowerGame
from utilities import Stepper
from enhanced_view import Enhanced_GameView
import high_score_manager as hsm
from tower import AbstractTower

__author__ = "Alex Teng"
__copyright__ = "Copyright Alex Teng"

BACKGROUND_COLOUR = "#333366"  # The background color of the shopview.
GRID_SIZE = (8, 10)  # The grid size


class TowerGameApp(Stepper):
    """Top-level GUI application for a simple tower defence game"""

    # All private attributes for ease of reading
    _current_tower = None
    _moving_tower = None
    _selected_tower = None

    _paused = False
    _won = None

    _level = None
    _wave = None
    _score = None
    _coins = None
    _lives = None

    _master = None
    _game = None
    _view = None

    def __init__(self, master: tk.Tk, delay: int = 20):
        """Construct a tower defence game in a root window

        Parameters:
            master (tk.Tk): Window to place the game into
        """

        self._master = master
        super().__init__(master, delay=delay)

        # instantiate score board manager
        self._score_borad_manag = hsm.HighScoreManager()
        self._score_borad_manag.load('high_scores.json')

        self._game = game = TowerGame(size=GRID_SIZE)
        # instantiate game over box
        self._game_over_box = Game_Over_Box(master, self, self._score_borad_manag)

        # instantiate Scoreboard
        self._score_board = ScoreBoard(self._master, self._score_borad_manag)

        self.setup_menu()

        # create a game view and draw grid borders
        self._view = view = Enhanced_GameView(master, size=game.grid.cells,
                                              cell_size=game.grid.cell_size,
                                              bg='antique white')
        view.pack(side=tk.LEFT, expand=True)

        # instantiate status bar
        self._statusbar = StatusBar(master, self)
        self._statusbar.grid_propagate(0)  # Fix the size of StatusBar frame

        # instantiate upgrade and instruction view
        self.upgrade_frame = tk.Frame(master, bg=BACKGROUND_COLOUR)

        self.upgrade_instruc_view = Upgrade_and_Instruction_View(master, self)

        # instantiate shop view
        self._shopview = ShopView(master, self, self.upgrade_instruc_view)

        # main windows view structure

        self._statusbar.pack(side=tk.TOP, ipadx=40, fill=tk.X)
        self._shopview.pack(side=tk.TOP, ipadx=120)
        self.upgrade_frame.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
        self.upgrade_instruc_view.pack(side=tk.TOP, anchor=tk.N)

        # instantiate widgets here
        self.setup_playcontrol()

        # bind game events
        game.on("enemy_death", self._handle_death)
        game.on("enemy_escape", self._handle_escape)
        game.on("cleared", self._handle_wave_clear)

        # bind mouse events to canvas here
        self._view.bind("<Motion>", self._move)
        self._view.bind("<Leave>", self._mouse_leave)
        self._view.bind("<Button-1>", self._left_click)
        # self._view.bind("<Button-1>", self._left_click_on_tower)
        self._view.bind("<Button-2>", self._right_click)

        # Level
        self._level = MyLevel()

        view.draw_borders(game.grid.get_border_coordinates())

        # Get ready for the game
        self._setup_game()

    def setup_menu(self):
        """Setup menu for the main window."""

        menubar = tk.Menu(self._master)
        self._master.config(menu=menubar)
        filemenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="Scores Board", command=self._score_board.show_window)
        filemenu.add_command(label="Restart Game", command=self._new_game)
        filemenu.add_command(label="Exit", command=self._exit)

    def setup_playcontrol(self):
        """Setup placycontrol buttons

        """
        self._button_next = tk.Button(self._master, text="Next Wave Play", command=self.next_wave, width=30)
        self._button_next.pack(side=tk.BOTTOM)
        self._button_pause_resume = tk.Button(self._master, text="Click to Pause", command=self._toggle_paused,
                                              width=30)
        self._button_pause_resume.pack(side=tk.BOTTOM)

    def _toggle_paused(self, paused=None):
        """Toggles or sets the paused state

        Parameters:
            paused (bool): Toggles/pauses/unpauses if None/True/False, respectively
        """
        if paused is None:
            paused = not self._paused

        if paused is True:
            self._button_pause_resume.config(text="Click to Start")
        elif paused is False:
            self._button_pause_resume.config(text="Click to Pause")

        if paused:
            self.pause()
        else:
            self.start()

        self._paused = paused

    def _setup_game(self):
        """Setup game for playing"""
        self._wave = 0
        self._score = 0
        self._coins = 300
        self._lives = 20

        self._won = False

        self._statusbar.set_all(self._wave, self._score, self._coins, self._lives)
        self._game.reset()

        self._button_next.config(state=tk.NORMAL)
        # Auto-start the first wave

        # self.next_wave()
        self._toggle_paused(paused=False)

    def _new_game(self):
        """Start a new game."""
        reply = messagebox.askquestion(type=messagebox.YESNO,
                                       title="Warning",
                                       message="Are you sure to restart the game?", icon="warning")
        if reply == messagebox.YES:
            self._restart_all_game()

        elif reply == messagebox.CANCEL:
            pass

    def _restart_all_game(self):
        """Remove all the units in canvas, and restart all game"""
        self._game.reset()
        self._setup_game()
        self._game.enemies = []
        self._game.towers = {}
        self._view.delete('enemy', 'tower', 'obstacle')
        self.upgrade_instruc_view.delete_all()
        # self._view.delete('tower')

    def _exit(self):
        """Destroy the main window."""
        reply = messagebox.askquestion(type=messagebox.YESNO,
                                       title="Exit",
                                       message="Are you sure to exit the game?", icon="warning")
        if reply == messagebox.YES:
            self._master.destroy()
        elif reply == messagebox.CANCEL:
            pass

    def refresh_view(self):
        """Refreshes the game view"""

        if self._step_number % 2 == 0:
            self._view.draw_enemies(self._game.enemies)
        self._view.draw_towers(self._game.towers)
        self._view.draw_obstacles(self._game.obstacles)

    def _step(self):
        """
        Perform a step every interval

        Triggers a game step and updates the view

       Returns:
            (bool) True if the game is still running
        """
        self._game.step()
        self.refresh_view()

        return not self._won

    def _move(self, event):
        """
        Handles the mouse moving over the game view canvas

        Parameter:
            event (tk.Event): Tkinter mouse event
        """
        # Do not draw preview while is paused
        if self._paused:
            return

        # Do not show preview is current tower is None
        if self._current_tower is None:
            return

        # move the shadow tower to mouse position
        position = event.x, event.y
        self._current_tower.position = position
        legal, grid_path = self._game.attempt_placement(position)

        # find the best path and covert positions to pixel positions
        path = [self._game.grid.cell_to_pixel_centre(position)
                for position in grid_path.get_shortest()]

        self._view.draw_path(path)
        self._view.draw_preview(self._current_tower, legal=legal)

        cell_position = self._game.grid.pixel_to_cell(position)
        if cell_position in self._game.towers:
            self._moving_tower = self._game.towers[cell_position]
        else:
            self._moving_tower = None

    def _mouse_leave(self, event):
        """
        Handles the mouse leaving event the game view canvas

        Parameter:
            event (tk.Event): Tkinter mouse event
        """
        self._view.delete('path', 'range', 'shadow')

    def _left_click(self, event):
        """
        Handles left click of mouse

        Parameter:
            event (tk.Event): Tkinter mouse event
        """
        # move the shadow tower to mouse position
        position = event.x, event.y

        # Cannot place while is paused
        if self._paused:
            return

        # retrieve position to place tower

        cell_position = self._game.grid.pixel_to_cell(position)

        # If cell_position has a tower, show the tower's info or checkbox
        if cell_position in self._game.towers:
            if cell_position in self._game.towers:
                self._selected_tower = self._game.towers[cell_position]
                # print("selected")
            else:
                # print("Not selected")
                self._selected_tower = None
            self.upgrade_instruc_view.show_upgrade_check_box()

        if self._current_tower is None:
            return

        if self._current_tower.get_value() > self._coins:
            # print("Insufficient Fund")
            return

        if self._game.place(cell_position, tower_type=self._current_tower.__class__):
            # Task 1.2 (Tower placement): Attempt to place the tower being previewed

            self._coins -= int(self._current_tower.get_value())
            self._game.place(position, tower_type=self._current_tower)

    def _right_click(self, event):
        """
        Handles double right click of mouse

        Parameter:
            event (tk.Event): Tkinter mouse event
        """

        # if self._current_tower is not None:
        #     return
        position = event.x, event.y
        cell_position = self._game.grid.pixel_to_cell(position)

        if cell_position not in self._game.towers:
            return

        if self._current_tower is not None:

            self._game.remove(cell_position)

            if self._current_tower.name == "Blazar Tower":
                self._coins -= self._current_tower.get_value() * 2
            else:
                self._coins += self._current_tower.get_value() * 0.8

    def next_wave(self):
        """Sends the next wave of enemies against the player"""
        if self._wave == self._level.get_max_wave():
            return

        self._wave += 1

        self._statusbar.set_wave(self._wave)
        if self._wave == self._level.get_max_wave():
            self._button_next.config(state=tk.DISABLED)
        else:
            self._button_next.config(state=tk.NORMAL)

        # Generate wave and enqueue
        wave = self._level.get_wave(self._wave)
        for step, enemy in wave:
            enemy.set_cell_size(self._game.grid.cell_size)

        self._game.queue_wave(wave)

    def select_tower(self, tower):
        """
        Set 'tower' as the current tower

        Parameters:
            tower (AbstractTower): The new tower type
        """
        self._current_tower = tower(self._game.grid.cell_size)


    def _handle_death(self, enemies):
        """
        Handles enemies dying

        Parameters:
            enemies (list<AbstractEnemy>): The enemies which died in a step
        """
        bonus = len(enemies) ** .5
        for enemy in enemies:
            self._coins += enemy.points
            self._score += int(enemy.points * bonus)

        # Task 1.3 (Status Bar): Update coins & score displays here
        self._statusbar.set_gold(self._coins)
        self._statusbar.set_score(self._score)

    def _handle_escape(self, enemies):
        """
        Handles enemies escaping (not being killed before moving through the grid

        Parameters:
            enemies (list<AbstractEnemy>): The enemies which escaped in a step
        """
        self._lives -= len(enemies)
        if self._lives < 0:
            self._lives = 0

        self._statusbar.set_lives(self._lives)

        # Handle game over
        if self._lives == 0:
            self._handle_game_over(won=False)

    def _handle_wave_clear(self):
        """Handles an entire wave being cleared (all enemies killed)"""
        if self._wave == self._level.get_max_wave():
            self._handle_game_over(won=True)

        # self.next_wave()

    def _handle_game_over(self, won=False):
        """Handles game over

        Parameter:
            won (bool): If True, signals the game was won (otherwise lost)
        """
        self._won = won
        self.stop()

        self._game_over_box._show_game_over_box(self._won)

    def select_current_tower(self):
        """Return current tower"""
        return self._current_tower



def main():
    """The main function."""
    root = tk.Tk()
    root.title("Tower")
    # Let it not resizeable
    root.resizable(width=False, height=False)
    root.config(bg=BACKGROUND_COLOUR)
    root.geometry('740x600')
    game_window = TowerGameApp(root, 20)
    root.mainloop()


if __name__ == "__main__":
    main()
