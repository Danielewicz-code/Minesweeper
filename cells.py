from tkinter import Button, Label
import settings
import random
import time
import ctypes
import sys

class Cell:
    all = []
    cell_count = settings.CELL_COUNT
    cell_count_label_object = None
    timer_label = None
    elapsed_seconds = 0
    timer_running = False
    timer_id = None

    def __init__(self, x, y, is_mine=False) -> None:
        self.is_mine = is_mine
        self.is_open = False
        self.cell_btn_object = None
        self.is_mine_candidate = False
        self.x = x
        self.y = y
        Cell.all.append(self)

    def create_btn_object(self, location):
        btn = Button(
            location,
            width=12,
            height=4,
        )
        btn.bind('<Button-1>', self.left_click_actions)
        btn.bind('<Button-3>', self.right_click_actions)
        self.cell_btn_object = btn

    @staticmethod
    def create_cell_count_label(location):
        lbl = Label(
            location,
            text=f"Cells left: {Cell.cell_count}",
            width=12,
            height=3,
            bg="#2980b9",
            fg="#ecf0f1",
            font=("Helvetica", 20, "bold")
        )
        Cell.cell_count_label_object = lbl

    #Actions for left click
    def left_click_actions(self, event):
        if self.is_mine:
            self.cell_btn_object.configure(bg="red")
            self.cell_btn_object.update_idletasks()
            self.show_mine()
        else:
            self.reveal_cells()
            if Cell.cell_count == settings.MINES_COUNT:
                self.show_victory_message()

        self.cell_btn_object.unbind('<Button-3>')

    def show_victory_message(self):
        message = "              YOU WON THE GAME!!!\n                    Play again?"
        result = ctypes.windll.user32.MessageBoxW(0, message, "Game Over", settings.MB_YESNO)
        if result == settings.IDYES:
            Cell.restart_game()
        else:
            sys.exit()

    def reveal_cells(self):
        if self.is_open:
            return

        self.show_cell()
        if self.surrounded_cells_mines_length == 0:
            for cell in self.surrounded_cells:
                cell.reveal_cells()

    def get_cell_by_axis(self, x, y):
        for cell in Cell.all:
            if cell.x == x and cell.y == y:
                return cell

    #logic for getting the outside cells when the pressed one is 0
    @property
    def surrounded_cells(self):
        cells = [
            self.get_cell_by_axis(self.x - 1, self.y - 1),
            self.get_cell_by_axis(self.x - 1, self.y),
            self.get_cell_by_axis(self.x - 1, self.y + 1),
            self.get_cell_by_axis(self.x, self.y - 1),
            self.get_cell_by_axis(self.x + 1, self.y - 1),
            self.get_cell_by_axis(self.x + 1, self.y),
            self.get_cell_by_axis(self.x + 1, self.y + 1),
            self.get_cell_by_axis(self.x, self.y + 1)
        ]

        return [cell for cell in cells if cell is not None]

    @property
    def surrounded_cells_mines_length(self):
        return sum(1 for cell in self.surrounded_cells if cell.is_mine)

    def show_cell(self):
        if not self.is_open:
            Cell.cell_count -= 1
            #Changing colors when they are not mines, two different hues to represent different levels: #DCDCDC, "#D3D3D3"
            bg_color = "#DCDCDC" if self.surrounded_cells_mines_length != 0 else "#D3D3D3"
            self.cell_btn_object.configure(text=self.surrounded_cells_mines_length if self.surrounded_cells_mines_length != 0 else "", bg=bg_color)
            self.cell_btn_object.update()

            if Cell.cell_count_label_object:
                Cell.cell_count_label_object.configure(text=f"Cells left: {Cell.cell_count}")

        self.is_open = True

    def show_mine(self):
        self.cell_btn_object.configure(bg="red")
        message = "              That was a mine.\n                    Play again?"
        result = ctypes.windll.user32.MessageBoxW(0, message, "Game Over", settings.MB_YESNO)
        if result == settings.IDYES:
            Cell.restart_game()
        else:
            sys.exit()

    @staticmethod
    def restart_game():
        for cell in Cell.all:
            cell.reset()
        
        Cell.cell_count = settings.CELL_COUNT
        if Cell.cell_count_label_object:
            Cell.cell_count_label_object.configure(text=f"Cells left: {Cell.cell_count}")
        Cell.reset_time()
        Cell.randomize_mines()

    #reset logic
    def reset(self):
        self.is_mine = False
        self.is_open = False
        self.is_mine_candidate = False
        if self.cell_btn_object:
            self.cell_btn_object.configure(text="", bg="SystemButtonFace")
            self.cell_btn_object.bind('<Button-1>', self.left_click_actions)
            self.cell_btn_object.bind('<Button-3>', self.right_click_actions)

    #right click actions to mark possible bombs
    def right_click_actions(self, event):
        if not self.is_mine_candidate and not self.is_open:
            self.cell_btn_object.configure(bg="orange")
            self.is_mine_candidate = True
        elif self.is_open:
            None
        else:
            self.cell_btn_object.configure(bg="SystemButtonFace")
            self.is_mine_candidate = False

    @staticmethod
    def randomize_mines():
        random_mines = random.sample(Cell.all, settings.MINES_COUNT)
        for mine in random_mines:
            mine.is_mine = True

    #timer logic and management
    @staticmethod
    def timer(label):
        Cell.timer_label = label
        Cell.elapsed_time = 0
        Cell.timer_running = True

        def update():
            if Cell.elapsed_time < settings.MAX_SECONDS:
                Cell.elapsed_time += 1
                elapsed_minutes = time.strftime("%M:%S", time.gmtime(Cell.elapsed_time))
                label.config(text=f"TIME LEFT:\n {elapsed_minutes}")
                Cell.timer_id = label.after(1000, update)
            else:
                label.config(text="Time's up!")
                message = "              You are out of time!\n                    Play again?"
                result = ctypes.windll.user32.MessageBoxW(0, message, "Game Over", settings.MB_YESNO)
                if result == settings.IDYES:
                    Cell.restart_game()
                else:
                    sys.exit()

        update()

    @staticmethod
    def reset_time():
        if Cell.timer_id is not None:
            Cell.timer_label.after_cancel(Cell.timer_id)
        Cell.elapsed_seconds = 0
        Cell.timer_running = False
        if Cell.timer_label:
            Cell.timer_label.config(text="TIME LEFT\n 00:00")
        Cell.timer(Cell.timer_label)

    def __repr__(self) -> str:
        return f"Cell({self.x}, {self.y})"
