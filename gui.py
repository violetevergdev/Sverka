import time
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as mb
from modules.sverka_RVP_main import sverka_RVP_main
from modules.sverka_MITS_main import sverka_MITS_main
from modules.vib_RVP_main import vib_RVP_main
from modules.vib_MITS_main import vib_MITS_main
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

    def vib_RVP():
        root.withdraw()
         # Пользователь указывает в какую папку сохранить файл
        out_path = filedialog.askdirectory().replace('/', "\\")
        vib_RVP_main(out_path)
        root.deiconify()

    def vib_MITS():
        root.withdraw()
        # Пользователь указывает в какую папку сохранить файл
        out_path = filedialog.askdirectory().replace('/', "\\")
        vib_MITS_main(out_path)
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

    start_RVP_btn = tk.Button(sverka_column, text='Обработать списки\nРВП', font=30, height=40, command=sver_RVP)
    start_RVP_btn.pack(side=tk.LEFT, padx=10, pady=10)

    start_MITS_btn = tk.Button(sverka_column, text='Обработать списки\nМиЦ', font=30, height=40, command=sver_MITS)
    start_MITS_btn.pack(side=tk.RIGHT, padx=10, pady=10)

    # Настройка фрейма выборки
    vib_column = ttk.Frame(viborka)
    vib_column.pack()

    start_vib_RVP_btn = tk.Button(vib_column, text="Выборка данных\nдля РВП", font=30, height=40, command=vib_RVP)
    start_vib_RVP_btn.pack(side=tk.LEFT, padx=10, pady=10)

    start_vib_MITS_btn = tk.Button(vib_column, text="Выборка данных\nдля МиЦ", font=30, height=40, command=vib_MITS)
    start_vib_MITS_btn.pack(side=tk.RIGHT, padx=10, pady=10)

    def destroyer():
        root.quit()

    root.protocol("WM_DELETE_WINDOW", destroyer)

    root.mainloop()




if __name__ == '__main__':
    gui()
