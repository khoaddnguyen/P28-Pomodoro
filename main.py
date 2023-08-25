from tkinter import *
import math

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"  # use for foreground fg
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
timer = None


# ---------------------------- TIMER RESET ------------------------------- #
def reset_timer():
    window.after_cancel(timer)
    # timer_text 00:00
    canvas.itemconfig(timer_text, text="00:00")
    # title_label "Timer"
    timer_label.config(text="Timer")
    # reset check_marks
    checks_label.config(text="")
    # reset lap to 0 to restart
    global reps
    reps = 0



# ---------------------------- TIMER MECHANISM ------------------------------- # 
def start_timer():
    global reps
    reps += 1

    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    # If it's the 8th rep:
    if reps % 8 == 0:
        count_down(long_break_sec)
        timer_label.config(text="Break", fg=RED)
    # If it's the 2nd/4th/6th rep:
    elif reps % 2 == 0:
        count_down(short_break_sec)
        timer_label.config(text="Break", fg=PINK)
    # If it's the 1st/3rd/5th/7th rep:
    else:
        count_down(work_sec)
        timer_label.config(text="Work", fg=GREEN)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):

    count_min = math.floor(count / 60)
    count_sec = count % 60
    if count_sec == 0:
        count_sec = "00"
    elif 0 < count_sec < 10:
        count_sec = "0" + f"{count_sec}"

    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)
    else:  # when done counting 1 lap, timer restart for new lap
        start_timer()
        marks = ""
        work_sessions = math.floor(reps/2)
        for _ in range(work_sessions):
            marks += "✔"
        checks_label.config(text=marks)

        # ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)

timer_label = Label(text="Timer", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 50))
timer_label.grid(column=1, row=0)

tomato_image = PhotoImage(file="tomato.png")  # file directory
canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)  # pixels are even numbers only
canvas.create_image(100, 112, image=tomato_image)
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1, row=1)

start_button = Button(text="Start", highlightbackground="#f7f5dd", command=start_timer)
start_button.grid(column=0, row=2)

reset_button = Button(text="Reset", highlightbackground="#f7f5dd", command=reset_timer)
reset_button.grid(column=2, row=2)

checks_label = Label(fg=GREEN, bg=YELLOW)
checks_label.grid(column=1, row=3)

window.mainloop()
