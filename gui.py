import os
import threading
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as mb
from tkinter.simpledialog import askstring
import json
from modules.sverka_main import sver_main
import sys

def check_login():
    with open('config/Common/login.json', 'r') as f:
        login_json = json.load(f)
    if login_json['login'] == "" and login_json['password'] == "":
        login_entry = askstring(title="Отсутствует логин и пароль", prompt='Введите логин от НВП:')
        password_entry = askstring(title="Отсутствует логин и пароль", prompt='Введите пароль от НВП:')

        login_json['login'] = login_entry
        login_json['password'] = password_entry

        with open('config/Common/login.json', 'w') as f:
            json.dump(login_json, f, indent=2)

    elif login_json['login'] == "":
        login_entry = askstring(title="Отсутствует логин", prompt='Введите логин от НВП:')
        login_json['login'] = login_entry

        with open('config/Common/login.json', 'w') as f:
            json.dump(login_json, f, indent=2)

    elif login_json['password'] == "":
        password_entry = askstring(title="Отсутствует пароль", prompt='Введите пароль от НВП:')
        login_json['password'] = password_entry
        with open('config/Common/login.json', 'w') as f:
            json.dump(login_json, f, indent=2)


def gui():
    def start_sver():
        type_of_sver = selected_type_of_sver.get()
        vib_state = check_vib_state.get()

        root.withdraw()

        def run_processing():
            err = sver_main(type_of_sver, vib_state)
            if err:
                mb.showerror('Error', 'Ошибка: ' + str(err))
                root.focus()
            else:
                mb.showinfo('Готово', 'Обработка завершена!')

            root.deiconify()

        processing_thread = threading.Thread(target=run_processing)
        processing_thread.start()

        mb.showinfo('ИДЕТ ОБРАБОТКА', 'Обработка выполняется, дождитесь сообщения об окончании...')

    root = tk.Tk()
    root.geometry('400x160')
    root.resizable(False, False)
    x = (root.winfo_screenwidth() - root.winfo_reqwidth()) / 2
    y = (root.winfo_screenheight() - root.winfo_reqheight()) / 2
    root.wm_geometry("+%d+%d" % (x, y))
    root.title('Обработка списков')

    check_login()

    # Настройка фрейма сверки
    sver_frame = ttk.Frame(root)
    sver_frame.pack()

    selected_type_of_sver = tk.StringVar(value='МСП')

    type_MITS_radio = tk.Radiobutton(sver_frame, text="МСП", font=20, variable=selected_type_of_sver, value="МСП")
    type_MITS_radio.pack(side=tk.LEFT, padx=5, pady=10)

    type_RVP_radio = tk.Radiobutton(sver_frame, text="РВП", font=20, variable=selected_type_of_sver, value="РВП")
    type_RVP_radio.pack(side=tk.LEFT, padx=5, pady=10)

    type_FSS_radio = tk.Radiobutton(sver_frame, text="ФСС", font=20, variable=selected_type_of_sver, value="ФСС")
    type_FSS_radio.pack(side=tk.LEFT, padx=5, pady=10)

    type_FSS_BASE_radio = tk.Radiobutton(sver_frame, text="ФСС-БАЗА", font=20, variable=selected_type_of_sver, value="ФСС-БАЗА")
    type_FSS_BASE_radio.pack(side=tk.LEFT, padx=5, pady=10)

    check_vib_state = tk.BooleanVar()

    vib_radio = tk.Checkbutton(root, text="с выборкой", font=5, variable=check_vib_state)
    vib_radio.pack(side=tk.TOP, padx=10, pady=10)

    start_btn = tk.Button(root, text='Обработать списки', font=20, command=start_sver)
    start_btn.pack(padx=10, pady=10)

    def destroyer():
        root.quit()

    root.protocol("WM_DELETE_WINDOW", destroyer)

    root.mainloop()


if __name__ == '__main__':
    gui()