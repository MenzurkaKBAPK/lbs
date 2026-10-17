import tkinter as tk
import tkinter.filedialog as fd
import tkinter.messagebox as messagebox
from pathlib import Path

from .errors import LbsError
from .interpreter import run_source


ASSETS_DIR = Path(__file__).with_name('assets')


class Editor:
    def __init__(self, window):
        self.window = window
        self.file_name = ''

        self.text = tk.Text(window, wrap='word')
        self.text.place(x=0, y=0, relwidth=1, relheight=1)

        self.path = tk.Label(window, text='Файл: ')
        self.path.place(relx=0, rely=1, anchor='sw')

        self.icon_new = self._load_icon('new_file.gif')
        self.icon_open = self._load_icon('open_file.gif')
        self.icon_save = self._load_icon('save_file.gif')
        self.icon_run = self._load_icon('run.png')
        self._create_menu()

    @staticmethod
    def _load_icon(name):
        return tk.PhotoImage(file=str(ASSETS_DIR / name))

    def _create_menu(self):
        control = tk.Menu(self.window)
        file_menu = tk.Menu(control, tearoff=0)
        control.add_cascade(label='Файл', menu=file_menu)
        self.window.configure(menu=control)

        file_menu.add_command(
            label='Новый файл', image=self.icon_new, compound='left', command=self.new_file
        )
        file_menu.add_command(
            label='Открыть...', image=self.icon_open, compound='left', command=self.open_file
        )
        file_menu.add_command(
            label='Сохранить', image=self.icon_save, compound='left', command=self.save
        )
        file_menu.add_command(
            label='Сохранить как...', image=self.icon_save, compound='left', command=self.save_as
        )
        file_menu.add_command(
            label='Запустить', image=self.icon_run, compound='left', command=self.run_program
        )

    def _update_path(self):
        self.path['text'] = f'Файл: {self.file_name}'

    def _save_file(self):
        content = self.text.get('1.0', 'end-1c')
        Path(self.file_name).write_text(content, encoding='utf-8')

    def open_file(self):
        file_name = fd.askopenfilename(filetypes=(('LBS', '*.lbs'), ('Все файлы', '*.*')))
        if not file_name:
            return

        self.file_name = file_name
        self.text.delete('1.0', 'end')
        self.text.insert('1.0', Path(file_name).read_text(encoding='utf-8'))
        self._update_path()

    def save_as(self):
        file_name = fd.asksaveasfilename(
            defaultextension='.lbs', filetypes=(('LBS', '*.lbs'), ('Все файлы', '*.*'))
        )
        if not file_name:
            return

        self.file_name = file_name
        self._save_file()
        self._update_path()

    def save(self):
        if self.file_name:
            self._save_file()
        else:
            self.save_as()

    def new_file(self):
        self.file_name = ''
        self.text.delete('1.0', 'end')
        self._update_path()

    def run_program(self):
        try:
            output = run_source(self.text.get('1.0', 'end-1c'))
        except LbsError as exc:
            messagebox.showerror('Ошибка LBS', str(exc), parent=self.window)
            return

        result = '\n'.join(output) if output else 'Нет присвоенных переменных.'
        messagebox.showinfo('Результат', result, parent=self.window)


def main():
    window = tk.Tk()
    window.geometry('400x500')
    window.title('LBS IDE')
    window.configure(bg='#ffffff')
    Editor(window)
    window.mainloop()


if __name__ == '__main__':
    main()
