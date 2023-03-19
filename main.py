import LRU

import customtkinter as CTk
import tkinter as Tk
import os
from tkinter import messagebox

from LFU import LFUCache
from LRU import LRUCache

Text = []


class App(CTk.CTk):

    def __init__(self):
        """ Функция инициализации и отрисовки окна """
        super().__init__()

        self.LFU = LFUCache(capacity=5)
        self.LRU = LRUCache(capacity=5)

        self.title("Алгоритмы кеширования LFU и LRU")
        self.geometry('1920x1080')
        # self.resizable(False, False)

        self.main_frame = CTk.CTkFrame(master=self,
                                       width=500,
                                       height=600, fg_color= ('black', 'purple'))
        self.main_frame.pack()

        self.cache_LabelLFU = CTk.CTkLabel(master=self.main_frame, text='Данные в кэше LFU', width=40, height=2)
        self.cache_LabelLRU = CTk.CTkLabel(master=self.main_frame, text='Данные в кэше LRU', width=40, height=2)
        self.data_Label = CTk.CTkLabel(master=self.main_frame, text='Данные для загрузки', width=40, height=2)
        self.cache_LFU_Listbox = Tk.Listbox(master=self.main_frame, width=150, height=10, bg='black', fg='white')
        self.cache_LRU_Listbox = Tk.Listbox(master=self.main_frame, width=150, height=10, bg='black', fg='white')
        self.data_Listbox = Tk.Listbox(master=self.main_frame, width=150, height=10, bg='black', fg='white')



        self.cache_LabelLFU.grid(row=0, column=0, padx=(5, 5), pady=(5, 5))
        self.cache_LabelLRU.grid(row=2, column=0, padx=(5, 5), pady=(5, 5))
        self.data_Label.grid(row=0, column=2, padx=(5, 5), pady=(30, 5))
        self.cache_LFU_Listbox.grid(row=1, column=0, padx=(5, 5), pady=(5, 5))
        self.cache_LRU_Listbox.grid(row=3, column=0, padx=(5, 5), pady=(5, 5))
        self.data_Listbox.grid(row=1, column=2, padx=(5, 5), pady=(5, 5))

        self.set_listdir()

        self.btn_getFileDataLFU = CTk.CTkButton(master=self.main_frame, text='Получить данные LFU',
                                             width=100, command=self.data_get_lfu, )
        self.btn_getFileDataLRU = CTk.CTkButton(master=self.main_frame, text='Получить данные LRU',
                                             width=100, command=self.data_get_lru, )
        self.btn_getFileDataLFU.grid(row=3, column=2, padx=(10, 100), pady=(5, 5))
        self.btn_getFileDataLRU.grid(row=3, column=2, padx=(400, 100), pady=(5, 5))


        self.text_Label = CTk.CTkLabel(master=self.main_frame, text='Содержмиое файла:', width=40, height=5)
        self.text_Label.grid(row=4, column=2, padx=(5, 5), pady=(5, 5))
        self.text = CTk.CTkTextbox(master=self.main_frame, width=800, height=350, fg_color= ('black', 'black'))
        self.text.grid(row=5, column=2, padx=(5, 5), pady=(5, 5))

    def data_get_lfu(self):
        if len(self.data_Listbox.curselection()) == 0:
            messagebox.showerror('Ошибка',
                                 'Не выбран файл для считывания\nВыберите файл в списке "Данные для загрузки"')
        else:
            selected_file = self.data_Listbox.get(self.data_Listbox.curselection())
            file = os.getcwd() + '\\Data\\' + selected_file

            data = self.LFU.get(file)
            if data == -1:
                # messagebox.showinfo('Инфо', 'Текст из файла')
                with open(file, 'r', encoding='utf-8') as f:
                    text = f.read()
                    self.LFU.put(file, text)
                    data = text
            else:
                # messagebox.showinfo('Инфо', 'Текст из кэша')
                pass
            self.text.delete(1.0, 'end')
            self.text.insert(index=1.0, text=data)
            self.set_cache(1)

    def data_get_lru(self):
        if len(self.data_Listbox.curselection()) == 0:
            messagebox.showerror('Ошибка',
                                 'Не выбран файл для считывания\nВыберите файл в списке "Данные для загрузки"')
        else:
            selected_file = self.data_Listbox.get(self.data_Listbox.curselection())
            file = os.getcwd() + '\\Data\\' + selected_file

            data = self.LRU.getitem(file)
            if data == -1:
                # messagebox.showinfo('Инфо', 'Текст из файла')
                with open(file, 'r', encoding='utf-8') as f:
                    text = f.read()
                    self.LRU.setitem(file, text)
                    data = text
            else:
                # messagebox.showinfo('Инфо', 'Текст из кэша')
                pass
            self.text.delete(1.0, 'end')
            self.text.insert(index=1.0, text=data)
            self.set_cache(2)


    def set_cache(self, algorithm):
        if algorithm == 1:
            self.cache_LFU_Listbox.delete(first=0, last='end')
            for key, value in self.LFU.freq_to_dll.items():
                for item in value.get_value():
                    if item is not None:
                        self.cache_LFU_Listbox.insert('end', f'{key}-{item}')
        elif algorithm == 2:
            self.cache_LRU_Listbox.delete(first=0, last='end')
            print(self.LRU.keys())
            for k in self.LRU.keys():
                self.cache_LRU_Listbox.insert('end', f'{k}-{self.LRU.__getitem__(k)}')

    def set_listdir(self):
        """Заполняем Listbox файлами доступными для чтения"""
        content = os.listdir(os.getcwd() + '/Data')
        for filename in content:
            self.data_Listbox.insert(0, filename)


if __name__ == '__main__':
    app = App()
    app.mainloop()

