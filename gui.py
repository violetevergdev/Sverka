import time
import tkinter as tk
import tkinter.messagebox as mb
from tkinter import filedialog
from main import main

folder_path = ""


def gui():
    def select_dir():
        global folder_path
        folder_path = filedialog.askdirectory()
        visible_path = folder_path.split("/")[-2:]
        if not folder_path:
            return
        label_dir['text'] = 'Выбранная директория: ' + str('/'.join(visible_path))
        start_button['state'] = 'normal'

    def start_work():
        global folder_path
        root.withdraw()
        time.sleep(1)
        mb.showinfo('ИДЕТ ОБРАБОТКА', 'Обработка выполняется, дождитесь сообщения об окончании...')

        err = main(folder_path)
        if err:
            mb.showinfo('Error', 'Ошибка: ' + str(err))

        mb.showinfo('Готово', 'Обработка завершена!')

        label_dir['text'] = "Выберите директорию:"
        start_button['state'] = 'disable'
        folder_path = ""
        root.deiconify()

    root = tk.Tk()
    root.geometry('400x200')
    root.resizable(False, False)
    x = (root.winfo_screenwidth() - root.winfo_reqwidth()) / 2
    y = (root.winfo_screenheight() - root.winfo_reqheight()) / 2
    root.wm_geometry("+%d+%d" % (x, y))
    root.title('Обработка РПВ списков')

    label_dir = tk.Label(root, text='Выберите директорию:')
    label_dir.pack(padx=5, pady=15)

    select_button = tk.Button(root, text='Выбрать директорию', command=select_dir)
    select_button.pack(padx=5, pady=15)

    start_button = tk.Button(root, text='Запустить обработку', state='disabled', command=start_work)
    start_button.pack(padx=5, pady=15)

    root.mainloop()


if __name__ == '__main__':
    gui()
