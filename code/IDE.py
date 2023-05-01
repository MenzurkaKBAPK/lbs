import tkinter as tk
import tkinter.filedialog as fd
import os


def save_file(file_name):
    content = text.get(1.0, 'end')
    with open(file_name, 'w', encoding='UTF-8') as file:
        file.write(content)


def o_f():
    global file_name
    file_name = fd.askopenfilename(filetypes=(('lbs', '*.lbs'), ('ALL', '*')))
    with open(file_name, encoding='UTF-8') as file:
        text.delete(1.0, 'end')
        text.insert(1.0, file.read())
    path['text'] = 'Файл: ' + file_name


def save_as():
    global file_name
    file_name = fd.asksaveasfilename()
    save_file(file_name)
    path['text'] = 'Файл: ' + file_name


def save():
    global file_name
    if file_name != '':
        save_file(file_name)
    else:
        save_as()


def new_file():
    global file_name
    file_name = ''
    text.delete(1.0, 'end')
    path['text'] = 'Файл: ' + file_name


def run():
    os.system(f"echo \"{text.get(1.0, 'end')}\" |./ main.py")


if __name__ == '__main__':

    file_name = ''

    window = tk.Tk()
    window.geometry('400x500')
    window.title('lbs IDE')
    window.configure(bg='#ffffff')

    text = tk.Text(window, wrap='word')
    text.place(x=0, y=0, relwidth=1, relheight=1)

    path = tk.Label(window, text='Файл: ' + file_name)
    path.place(relx=0, rely=1, anchor='sw')

    control = tk.Menu(window)
    window.configure(menu=control)
    control2 = tk.Menu(control, tearoff=0)
    control.add_cascade(label='Файл', menu=control2)

    icon_new = tk.PhotoImage(file='new_file.gif')
    icon_open = tk.PhotoImage(file='open_file.gif')
    icon_save = tk.PhotoImage(file='save_file.gif')
    icon_run = tk.PhotoImage(file='run.png')

    control2.add_command(label='Новый файл', image=icon_new, compound='left', command=new_file)
    control2.add_command(label='Открыть...', image=icon_open, compound='left', command=o_f)
    control2.add_command(label='Сохранить', image=icon_save, compound='left', command=save)
    control2.add_command(label='Сохранить как...', image=icon_save, compound='left', command=save_as)
    control2.add_command(label='Запустить', image=icon_run, compound='left', command=run)

    window.mainloop()
