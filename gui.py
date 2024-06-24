import time
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as mb
from tkinter import filedialog
from sverka_main import sverka_main
from vib_main import vib_main

folder_path = ""


def gui():
    def select_dir():
        global folder_path
        folder_path = filedialog.askdirectory()
        visible_path = folder_path.split("/")[-2:]
        if not folder_path:
            return
        label_sver_dir['text'] = 'Выбранная директория: ' + str('/'.join(visible_path))
        start_sver_btn['state'] = 'normal'

    def sver():
        global folder_path
        root.withdraw()
        time.sleep(1)
        mb.showinfo('ИДЕТ ОБРАБОТКА', 'Обработка выполняется, дождитесь сообщения об окончании...')

        err = sverka_main(folder_path)
        if err:
            mb.showinfo('Error', 'Ошибка: ' + str(err))

        mb.showinfo('Готово', 'Обработка завершена!')

        label_sver_dir['text'] = "Выберите директорию:"
        start_sver_btn['state'] = 'disable'
        folder_path = ""
        root.deiconify()

    def vib():
        root.withdraw()
        # Пользователь указывает в какую папку сохранить файл
        out_path = filedialog.askdirectory().replace('/', "\\")

        vib_main(out_path)
        root.deiconify()


    root = tk.Tk()
    root.geometry('400x200')
    root.resizable(False, False)
    x = (root.winfo_screenwidth() - root.winfo_reqwidth()) / 2
    y = (root.winfo_screenheight() - root.winfo_reqheight()) / 2
    root.wm_geometry("+%d+%d" % (x, y))
    root.title('Обработка РПВ списков')

    # Создаем вкладки
    notebook = ttk.Notebook(root,height=200, width=400)
    sverka = ttk.Frame(notebook)
    viborka = ttk.Frame(notebook)

    notebook.add(sverka, text='Обработка')
    notebook.add(viborka, text='Выборка')

    notebook.pack()

    # Настройка фрейма сверки
    label_sver_dir = tk.Label(sverka, text='Выберите директорию:')
    label_sver_dir.pack(padx=5, pady=15)

    select_button = tk.Button(sverka, text='Выбрать директорию', command=select_dir)
    select_button.pack(padx=5, pady=15)

    start_sver_btn = tk.Button(sverka, text='Запустить обработку', state='disabled', command=sver)
    start_sver_btn.pack(padx=5, pady=15)

    # Настройка фрейма выборки
    label_vib_info = tk.Label(viborka, text="При запуске программы\nукажите директорию для скачивания файлов")
    label_vib_info.pack(padx=5, pady=15)

    start_vib_btn = tk.Button(viborka, text="Начать выборку данных", command=vib)
    start_vib_btn.pack(padx=5, pady=15)

    root.mainloop()


if __name__ == '__main__':
    gui()
