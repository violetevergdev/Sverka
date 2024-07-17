import time
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as mb
from modules.sverka_RVP_main import sverka_RVP_main
from modules.sverka_MITS_main import sverka_MITS_main
from modules.sverka_FSS_main import sverka_FSS_main
from modules.vib_RVP_main import vib_RVP_main
from modules.vib_MITS_main import vib_MITS_main
from modules.vib_FSS_main import vib_FSS_main

import os
from tkinter import filedialog

def gui():
    def sver_RVP():
        root.withdraw()
        time.sleep(1)
        mb.showinfo('ИДЕТ ОБРАБОТКА', 'Обработка выполняется, дождитесь сообщения об окончании...')

        err = sverka_RVP_main()
        if err:
            mb.showerror('Error', 'Ошибка: ' + str(err))

        mb.showinfo('Готово', 'Обработка завершена!')

        root.deiconify()

    def sver_MITS():
        root.withdraw()
        time.sleep(1)
        mb.showinfo('ИДЕТ ОБРАБОТКА', 'Обработка выполняется, дождитесь сообщения об окончании...')

        err = sverka_MITS_main()
        if err:
            mb.showerror('Error', 'Ошибка: ' + str(err))

        mb.showinfo('Готово', 'Обработка завершена!')

        root.deiconify()

    def sver_FSS():
        root.withdraw()
        time.sleep(1)
        mb.showinfo('ИДЕТ ОБРАБОТКА', 'Обработка выполняется, дождитесь сообщения об окончании...')

        err = sverka_FSS_main()
        if err:
            mb.showerror('Error', 'Ошибка: ' + str(err))

        mb.showinfo('Готово', 'Обработка завершена!')

        root.deiconify()

    def vib_RVP():
        root.withdraw()
         # Пользователь указывает в какую папку сохранить файл
        out_path = os.path.join(os.getcwd(), 'IN\\РВП\\НВП')
        vib_RVP_main(out_path)
        root.deiconify()

    def vib_MITS():
        root.withdraw()
        # Пользователь указывает в какую папку сохранить файл
        out_path = os.path.join(os.getcwd(), 'IN\\МСП\\VIB')
        vib_MITS_main(out_path)
        root.deiconify()

    def vib_FSS():
        root.withdraw()
        # Пользователь указывает в какую папку сохранить файл
        out_path = os.path.join(os.getcwd(), 'IN\\ФСС\\VIB')
        vib_FSS_main(out_path)
        root.deiconify()


    root = tk.Tk()
    root.geometry('400x200')
    root.resizable(False, False)
    x = (root.winfo_screenwidth() - root.winfo_reqwidth()) / 2
    y = (root.winfo_screenheight() - root.winfo_reqheight()) / 2
    root.wm_geometry("+%d+%d" % (x, y))
    root.title('Обработка списков')

    # Создаем вкладки
    notebook = ttk.Notebook(root,height=200, width=400)
    sverka = ttk.Frame(notebook)
    viborka = ttk.Frame(notebook)

    notebook.add(sverka, text='Обработка')
    notebook.add(viborka, text='Выборка')

    notebook.pack()

    # Настройка фрейма сверки
    sverka_column = ttk.Frame(sverka)
    sverka_column.pack()

    l_col__sver = ttk.Frame(sverka_column)
    l_col__sver.pack(side=tk.LEFT)

    r_col__sver = ttk.Frame(sverka_column)
    r_col__sver.pack(side=tk.RIGHT)

    start_RVP_btn = tk.Button(l_col__sver, text='Обработать списки\nРВП', font=5, command=sver_RVP)
    start_RVP_btn.pack(side=tk.TOP, padx=5, pady=20)

    start_MITS_btn = tk.Button(l_col__sver, text='Обработать списки\nМиЦ', font=5, command=sver_MITS)
    start_MITS_btn.pack(side=tk.BOTTOM, padx=5)

    start_FSS_btn = tk.Button(r_col__sver, text='Обработать списки\nФСС', font=5, command=sver_FSS)
    start_FSS_btn.pack(side=tk.TOP, padx=5, pady=5)

    # Настройка фрейма выборки
    vib_column = ttk.Frame(viborka)
    vib_column.pack()

    l_col__vib = ttk.Frame(vib_column)
    l_col__vib.pack(side=tk.LEFT)

    r_col__vib = ttk.Frame(vib_column)
    r_col__vib.pack(side=tk.RIGHT)

    start_vib_RVP_btn = tk.Button(l_col__vib, text="Выборка данных\nдля РВП", font=5, command=vib_RVP)
    start_vib_RVP_btn.pack(side=tk.TOP, padx=5, pady=20)

    start_vib_MITS_btn = tk.Button(l_col__vib, text="Выборка данных\nдля МиЦ", font=5, command=vib_MITS)
    start_vib_MITS_btn.pack(side=tk.BOTTOM, padx=5)

    start_vib_FSS_btn = tk.Button(r_col__vib, text="Выборка данных\nдля ФСС", font=5, command=vib_FSS)
    start_vib_FSS_btn.pack(side=tk.TOP, padx=5, pady=5)

    def destroyer():
        root.quit()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", destroyer)

    root.mainloop()




if __name__ == '__main__':
    gui()
