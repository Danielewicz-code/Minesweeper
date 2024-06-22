from tkinter import *
import settings
import utils
from cells import Cell

root = Tk()

root.configure(bg="#2c3e50")
root.geometry(f"{settings.width}x{settings.height}")
root.title("Mineswreeper")
root.resizable(False, False)

# Top frame
top_frame = Frame(
    root,
    bg="#34495e",
    width=settings.width,
    height=utils.height_prct(26),
    highlightbackground="#1abc9c",
    highlightthickness=2,
    bd=0
)
top_frame.place(x=0, y=0)

#title
game_title = Label(
    top_frame,
    bg="#34495e",
    fg="white",
    text="Minesweeper",
    font=("Helvetica", 40, "bold")
)

game_title.place(
    x=utils.width_prct(35), 
    y=utils.height_prct(5)
)


instructions = Label(
    top_frame,
    bg="#34495e",
    fg="white",
    text="Left-click to reveal a cell. \nRight-click to mark it as a potential bomb.",
    font=("Helvetica", 12)
)
instructions.place(
    x=utils.width_prct(1),
    y=utils.height_prct(18)
)

#Zerowicz mentioned juas juas
zerowicz = Label(
    top_frame,
    bg="#34495e",
    fg="white",
    text="Zerowicz",
    font=("Helvetica", 14, "bold")
)
zerowicz.place(
    x=utils.width_prct(86),
    y=utils.height_prct(18)
)


#sidebar
left_sidebar = Frame(
    root,
    bg="#34495e",
    width=utils.width_prct(25),
    height=settings.height,
    highlightbackground="#1abc9c",
    highlightthickness=2,
    bd=0
)

left_sidebar.place(x=0, y=utils.height_prct(26))


#main game frame
game_frame = Frame(
    root,
    bg="#ecf0f1",
    width=utils.width_prct(75),
    height=utils.height_prct(80),
    highlightbackground="#1abc9c",
    highlightthickness=3,
    bd=0
)

game_frame.place(
    x=utils.width_prct(25),
    y=utils.height_prct(26)
)

#reset game button
reset_button = Button(
    root,
    text="Restart",
    width=12,
    height=2,
    bg="#e74c3c",
    fg="white",
    font=("Helvetica", 12, "bold"),
    command=Cell.restart_game,
    bd=0,
    relief="solid",
    highlightbackground="#e74c3c",
    highlightthickness=3,
    cursor="hand2"
)

reset_button.place(
    x=utils.width_prct(84.5),
    y=utils.height_prct(37)
)

#time management
time_holder = Label(
    left_sidebar,
    height=2,
    width=12,
    text="TIME ELAPSED:\n00:00",
    font=("Helvetica", 20, "bold"),
    bg="#e67e22",
    fg="white",
    bd=0,
    relief="solid",
    highlightbackground="#d35400",
    highlightthickness=1
)

time_holder.place(
    x=utils.width_prct(2),
    y=utils.height_prct(35)
)

Cell.timer(time_holder)

#cells creation
for x in range(settings.GRID_SIZE):
    for y in range(settings.GRID_SIZE):
        c = Cell(x, y)
        c.create_btn_object(game_frame)
        c.cell_btn_object.grid(column=x, row=y)


Cell.create_cell_count_label(left_sidebar)
Cell.cell_count_label_object.config(
    bg="#2980b9",  # Background color
    fg="#ecf0f1",  # Text color
    font=("Helvetica", 16, "bold"),
    bd=0,
    relief="solid",
    highlightbackground="#3498db",
    highlightthickness=1
)
Cell.cell_count_label_object.place(x=utils.width_prct(5), y=utils.height_prct(5))


Cell.randomize_mines()

#run window
root.mainloop()
