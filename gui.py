import ctypes
import os
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as mb
from modules.sverka_main import sver_main
import sys

from settings.settings import env


def gui():
    def start_sver():
        root.withdraw()

        err = sver_main()
        if err:
            mb.showerror('Error', 'Ошибка: ' + str(err))
            root.focus()
        else:
            mb.showinfo('Готово', 'Обработка завершена!')

        root.deiconify()

       

    root = tk.Tk()
    root.geometry('400x160')
    root.resizable(False, False)
    x = (root.winfo_screenwidth() - root.winfo_reqwidth()) / 2
    y = (root.winfo_screenheight() - root.winfo_reqheight()) / 2
    root.wm_geometry("+%d+%d" % (x, y))
    root.title('Сверка [Погребение]')

    # Настройка фрейма сверки
    sver_frame = ttk.Frame(root)
    sver_frame.pack()
    
    title_lable = tk.Label(text='В директории IN должны располагаться файлы\nс именами "выплатной реестр" и "реестр заявлений"\nиные наименования выдадут ошибку\n', font=14)
    title_lable.pack()
    
    start_btn = tk.Button(root, text="Обработать списки", font=20, command=start_sver)
    start_btn.pack(padx=10, pady=10)


    def destroyer():
        root.quit()

    root.protocol("WM_DELETE_WINDOW", destroyer)
    
    if env == "prod":
        icon_path = os.path.join(sys._MEIPASS, "ic.ico")
    else:
        icon_path = "ic.ico"
    root.iconbitmap(icon_path)


    root.mainloop()


if __name__ == '__main__':
    myappid = "mycompany.myproduct.subproduct.version"
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    gui()