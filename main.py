import os
import sys
from tkinter import *
from tkinter import ttk
from tkinter import Menu
from tkinter import messagebox

timer = ""


def abort():
    window.after_cancel(timer)
    os.system("shutdown /a")

    button_start.config(text="Timer starten", command=calc)
    list_hours.config(state=NORMAL)
    list_minutes.config(state=NORMAL)
    label_countdown.config(text="-")
    list_hours.set(hours_list[0])
    list_minutes.set(hours_list[0])


def calc():
    calc_hours = int(list_hours.get())
    calc_minutes = int(list_minutes.get())
    calc_seconds = ((calc_hours * 60) * 60) + (calc_minutes * 60)

    if calc_seconds == 0:
        messagebox.showerror(title="Fehler!", message="Es muss eine Dauer angeben werden.")
    else:
        button_start.config(text="Abbrechen", command=abort, width=10)
        list_hours.config(state=DISABLED)
        list_minutes.config(state=DISABLED)

        os.system(f"shutdown /s /f /t {calc_seconds}")
        print(f"Shutdown in: {calc_seconds}")
        countdown(calc_seconds)


def countdown(seconds):
    global timer
    counter = seconds
    c_min, c_sec = divmod(counter, 60)
    c_hrs, c_min = divmod(c_min, 60)

    if counter > 0:
        label_countdown.config(text=f"{c_hrs:02d}:{c_min:02d}:{c_sec:02d}")
        timer = window.after(1000, countdown, counter - 1)
    elif counter == 0:
        label_countdown.config(text=f"00:00:00")


def info():
    messagebox.showinfo(title="Info", message="Shutdownbox v 1.0\n\n"
                                              "2022 Jörg Rüggeberg - All rights reserved")


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


def shutdown():
    return


# ---------------------------- UI SETUP ------------------------------- #
# Window
window = Tk()
window.title("Shutdown Box - JR")
window.config(pady=20, padx=20)

# Canvas
canvas = Canvas(height=42, width=250, highlightthickness=0)
PATH = resource_path("logo.png")
logo_img = PhotoImage(file=PATH)
canvas.create_image(125, 21, image=logo_img)
canvas.grid(column=0, row=0, columnspan=4)

# Menu bar
menubar = Menu(window)
window.config(menu=menubar)

# Menu category
menu_menu = Menu(menubar, tearoff=False)

# Menu item
menu_menu.add_command(label="Info", command=info)
menu_menu.add_command(label="Schließen", command=window.destroy)

# add to bar
menubar.add_cascade(label="Menü", menu=menu_menu)

# label
label_none_01 = Label(text="", pady=5)
label_hours = Label(text="Stunden: ", pady=5)
label_minutes = Label(text="Minuten: ", pady=5)
label_none_02 = Label(text="", pady=5)
label_remaining = Label(text="Shutdown: ", pady=5)
label_countdown = Label(text="-", pady=5)

label_none_01.grid(column=0, row=1, sticky="w")
label_hours.grid(column=0, row=2, sticky="w")
label_minutes.grid(column=2, row=2, sticky="w")
label_none_02.grid(column=0, row=3, sticky="w")
label_remaining.grid(column=0, row=4, sticky="w")
label_countdown.grid(column=1, row=4, sticky="w")

# list
hours_list = [str(n) for n in range(0, 13)]
minutes_list = [str(n) for n in range(0, 60)]

list_hours = ttk.Combobox(window, values=hours_list, width=5)
list_hours.set(hours_list[0])
list_minutes = ttk.Combobox(window, values=minutes_list, width=5)
list_minutes.set(minutes_list[0])

list_hours.grid(column=1, row=2, padx=5, pady=5, sticky="w")
list_minutes.grid(column=3, row=2, padx=5, pady=5, sticky="e")

# Button
button_start = Button(text="Timer starten", command=calc, width=10)
button_start.grid(columnspan=2, column=2, row=4, sticky="e")

window.mainloop()
