from tkinter import *
import math
    # from PIL import Image, ImageTk
# import winsound for windows. winsound.Beep(430,1000) to use
# ---------------------------- CONSTANTS ------------------------------- #
from tkinter import messagebox, simpledialog

PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 0.1
SHORT_BREAK_MIN = 0.1
LONG_BREAK_MIN = 0.1
reps = 0
timer = None


# -------------------------- POP window Infront -------------------------- #
def raise_above_all(window):
    window.state("normal")
    window.attributes('-topmost', 1)
    window.attributes('-topmost', 0)


# ---------------------------- TIMER RESET ------------------------------- # 
def reset_timer():
    global reps
    reps = 0
    window.after_cancel(timer)
    # timer text 00:00
    canvas.itemconfig(timer_text, text="00:00")
    # title label to timer
    timer_label.config(text="Timer")
    # reset checkmarks
    check_marks.config(text="")
    timer_label.config(text="Timer", fg=GREEN)
    start_button.config(state="normal")
    reset_button.config(state="disabled")


# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer():
    global reps
    reps += 1
    window.bell()
    start_button.config(state="disabled")
    reset_button.config(state="normal")
    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60
    raise_above_all(window)
    # If it's the 8th rep
    if reps % 8 == 0:
        count_down(long_break_sec)
        timer_label.config(text="Break", fg=RED)
        # messagebox.showinfo(title="Break", message="Long break!")
    # if it's the 2nd/4th,6th rep
    elif reps % 2 == 0:
        count_down(short_break_sec)

        timer_label.config(text="Break", fg=PINK)
        # messagebox.showinfo(title="Break", message="Short break!")
    else:
        count_down(work_sec)
        timer_label.config(text="Work", fg=GREEN)

    start_button.config(state="disabled")

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
# The way we change something on canvas is slightly different from say label. With label,we write label.config(text="f")
# Tap into particular canvas you want to change, call the item config method, pass in the particular item
# you want configured and then pass the thing abt it that you want changed in terms of kwargs

def count_down(count):

    count_min = math.floor(count/60)
    count_sec = count % 60
    # Using Dynamic Typing
    if count_sec < 10:
        count_sec = f"0{count_sec}"
    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count-1)
    else:
        start_timer()
        marks = ""
        work_sessions = math.floor(reps/2)
        for _ in range(work_sessions):
            marks += "✔️️"
        check_marks.config(text=marks)


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)

canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
# Since we have taken the canvas the size of the image, so we'd place the image at center of the canvas
tomato_img = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_img)
# to be able to change the text, we'll assign timer_text as the text that was created on the canvas
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1, row=1)


# Timer Label
timer_label = Label(text="Timer", fg=GREEN, font=(FONT_NAME, 48, "bold"), bg=YELLOW)
timer_label.grid(column=1, row=0)

# Start & Reset Buttons
start_button = Button(text="start", highlightthickness=0, command=start_timer, state="normal")
start_button.grid(column=0, row=2)

reset_button = Button(text="reset", highlightthickness=0, command=reset_timer, state="disabled")
reset_button.grid(column=2, row=2)

check_marks = Label(fg=GREEN, bg=YELLOW)
check_marks.grid(column=1, row=3)

# window.update_idletasks()
WORK_MIN = simpledialog.askinteger(title="Study Session Times", prompt="How long are the study sessions?", parent=window)

# tomato_icon = ImageTk.PhotoImage(Image.open('tomato_icon.png'))
# window.iconphoto(False, tomato_icon)


window.mainloop()
# Other things that can be added
# from pygame import mixer

# mixer.init()

# mixer.music.load("my.mp3")
# mixer.music.play()
