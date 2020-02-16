import datetime
from itertools import zip_longest
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import Calendar, DateEntry

from thoughts.core_thoughts import *


class GuiThought(Tk):

    def __init__(self):
        super().__init__()

        self.title('Thoughts')

        main_nb = ttk.Notebook(self)
        main_nb.pack(expand=1, fill='both')

        thought_frame = ThoughtFrame(main_nb, padx=10, pady=10)
        main_nb.add(thought_frame, text='Thoughts')

        get_frame = ShowFrame(main_nb)
        main_nb.add(get_frame, text='Show')

        tag_frame = Frame(main_nb)
        main_nb.add(tag_frame, text='Tags')


class ThoughtFrame(Frame):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.thoughts = select(conn, 'thought')[1:]
        names = [thought[1] for thought in self.thoughts]

        Label(self, text='Thought:').grid(row=0, column=0, sticky=E)
        self.name = ttk.Combobox(self, values=names)
        self.name.grid(row=0, column=1, columnspan=2, pady=5, sticky=EW)
        self.name.bind("<<ComboboxSelected>>", self.update_mention_info)
        self.name.bind('<FocusOut>', self.update_mention_info)

        Label(self, text='Description:').grid(row=1, column=0, pady=5, sticky=NE)
        self.descr = Text(self, width=50, height=10)
        self.descr.grid(row=1, column=1, columnspan=2, pady=5, sticky=W)

        Label(self, text='Date, time:').grid(row=2, column=0, sticky=E)
        self.date = DateEntry(self, date_pattern='y-mm-dd')
        self.date.grid(row=2, column=1, pady=5, sticky=EW)

        self.time = Entry(self, )
        self.time.grid(row=2, column=2, pady=5, sticky=EW)
        self.time.insert(0, datetime.datetime.now().strftime("%H:%M:%S"))

        self.btn_add = Button(self,
                              text='Add',
                              width=15, height=1,
                              bg='white', fg='black')
        self.btn_add.bind('<Button-1>', self.submit)
        self.btn_add.grid(row=3, column=1, pady=5, sticky=W)

        self.btn_clear = Button(self,
                                text='Clear',
                                width=15, height=1,
                                bg='white', fg='black')
        self.btn_clear.bind('<Button-1>', self.clear)
        self.btn_clear.grid(row=3, column=2, pady=5, sticky=W)

        # Tags section

        self.added_tags_var = StringVar()
        self.added_tags = []
        self.available_tags = select(conn, 'tag')[1:]
        self.available_tags_var = StringVar(value=[tag[1] for tag in self.available_tags])

        self.tag_frame = Frame(self)
        self.tag_frame.grid(row=0,
                            column=3,
                            rowspan=3,
                            columnspan=3,
                            sticky=N+S,
                            padx=10,
                            pady=5)

        Label(self.tag_frame, text='Added tags:').grid(row=0, column=0, sticky=W)
        self.added_tags_box = Listbox(self.tag_frame,
                                      listvariable=self.added_tags_var,
                                      selectmode=EXTENDED,
                                      width=15)
        self.added_tags_box.grid(row=1, column=0, rowspan=2, sticky=N+S)
        self.added_tags_scroll = Scrollbar(self.tag_frame, command=self.added_tags_box.yview)
        self.added_tags_scroll.grid(row=1, column=1, rowspan=2, sticky=N+S)
        self.added_tags_box.config(yscrollcommand=self.added_tags_scroll.set)

        Label(self.tag_frame, text='Available tags:').grid(row=0, column=3, sticky=W)
        self.available_tags_box = Listbox(self.tag_frame,
                                          listvariable=self.available_tags_var,
                                          selectmode=EXTENDED,
                                          width=15)
        self.available_tags_box.grid(row=1, column=3, rowspan=2, sticky=N+S)
        self.available_tags_scroll = Scrollbar(self.tag_frame, command=self.added_tags_box.yview)
        self.available_tags_scroll.grid(row=1, column=4, rowspan=2, sticky=N+S)
        self.available_tags_box.config(yscrollcommand=self.available_tags_scroll.set)

        self.btn_add_tag = Button(self.tag_frame, text='<<', width=2)
        self.btn_add_tag.grid(row=1, column=2, sticky=S)
        self.btn_add_tag.bind('<Button-1>',
                              lambda event: self.move_tag(event, 'add'))
        self.btn_remove_tag = Button(self.tag_frame, text='>>', width=2)
        self.btn_remove_tag.grid(row=2, column=2, sticky=N)
        self.btn_remove_tag.bind('<Button-1>',
                                 lambda event: self.move_tag(event, 'remove'))


    def move_tag(self, event, action):

        from_list = self.available_tags
        to_list = self.added_tags
        from_box = self.available_tags_box
        if action == 'remove':
            from_list, to_list = to_list, from_list
            from_box = self.added_tags_box

        addition = list(map(lambda i: from_list[i], from_box.curselection()))

        to_list.extend(addition)
        for elem in addition:
            from_list.remove(elem)

        from_box.selection_clear(0, END)
        self.added_tags_var.set([item[1] for item in self.added_tags])
        self.available_tags_var.set([item[1] for item in self.available_tags])


    def update_mention_info(self, event):
        for thought in self.thoughts:
            if thought[1] == self.name.get():
                self.descr.delete('1.0', END)
                self.descr.insert(END, thought[2])

                self._clear_tags()
                tags = select(conn, 'last_mention_tag', thought[0])[1:]

                addition = list(map(lambda tag: self.available_tags[tag[0]], tags))

                self.added_tags.extend(addition)
                for elem in addition:
                    self.available_tags.remove(elem)

                self.added_tags_var.set([item[1] for item in self.added_tags])
                self.available_tags_var.set([item[1] for item in self.available_tags])
                break


    def _clear_tags(self):
        self.added_tags = []
        self.available_tags = select(conn, 'tag')[1:]
        self.added_tags_var.set([item[1] for item in self.added_tags])
        self.available_tags_var.set([item[1] for item in self.available_tags])


    def clear(self, event=None):
        self.name.delete(0, END)
        self.descr.delete('1.0', END)
        self.time.delete(0, END)
        self.time.insert(0, datetime.datetime.now().strftime("%H:%M:%S"))
        self._clear_tags()
        


    def submit(self, event=None):
        if self.name.get() != '':
            data_time = str(self.date.get_date()) + ' ' + str(self.time.get())
            insert(conn,
                   'all',
                   [self.name.get(),
                    self.descr.get('1.0', END).rstrip('\n'),
                    data_time,
                    list([item[0] for item in self.added_tags])
                    ])
            self.clear()
        else:
            messagebox.showwarning('Empty name', 'Name of thought can\'t be empty')


class ShowFrame(Frame):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.info_frame = Frame(self, padx=10, pady=10)
        self.ctrl_frame = Frame(self, padx=10, pady=10)
        self.info_frame.pack(side='left', fill='both')
        self.ctrl_frame.pack(side='right', ipadx=10, ipady=10, fill='both')

        self.text = Text(self.info_frame,
                         width=100,
                         font='Courier 10',
                         wrap=NONE)
        self.text_scrollx = Scrollbar(self.info_frame,
                                      command=self.text.xview,
                                      orient=HORIZONTAL)
        self.text_scrolly = Scrollbar(self.info_frame,
                                      command=self.text.yview)
        self.text_scrollx.pack(side='bottom', fill=X)
        self.text_scrolly.pack(side='right', fill=Y)
        self.text.pack(side='left', fill='both')
        self.text.config(yscrollcommand=self.text_scrolly.set,
                         xscrollcommand=self.text_scrollx.set)

        self.btn_all = Button(self.ctrl_frame,
                              text='All',
                              width=10, height=1,
                              bg='white', fg='black')
        self.btn_all.bind('<Button-1>', lambda event: self.get_data(event, req_type='all'))
        self.btn_all.pack()

        self.btn_thoughts = Button(self.ctrl_frame,
                                   text='Thoughts',
                                   width=10, height=1,
                                   bg='white', fg='black')
        self.btn_thoughts.bind('<Button-1>', lambda event: self.get_data(event, req_type='thought'))
        self.btn_thoughts.pack()

        self.btn_mentions = Button(self.ctrl_frame,
                                   text='Mentions',
                                   width=10, height=1,
                                   bg='white', fg='black')
        self.btn_mentions.bind('<Button-1>', lambda event: self.get_data(event, req_type='mention'))
        self.btn_mentions.pack()

        self.btn_tags = Button(self.ctrl_frame,
                               text='Tags',
                               width=10, height=1,
                               bg='white', fg='black')
        self.btn_tags.bind('<Button-1>', lambda event: self.get_data(event, req_type='tag'))
        self.btn_tags.pack()


    def get_data(self, event=None, req_type=None):
        self.text.delete('1.0', END)
        data = select(conn, req_type)
        # Get length of all columns
        lens = [
            max(
                [self._line_length(str(row[i])) for row in data]
                ) for i in range(len(data[0]))
            ]
        # Extend data list by splitting rows that contains newlines
        new_data = []
        for th in data:
            tmp = []
            for col in th:
                tmp.append(str(col).split('\n'))
            new_data.extend(list(zip_longest(*tmp, fillvalue='')))
        data = new_data
        # Drawing table line by line
        self.text.insert(END, '┌'+'┬'.join(['─'*i for i in lens])+'┐\n')
        for th in data:
            self.text.insert(END, '│')
            for col, cell in enumerate(th):
                self.text.insert(END, str(cell).ljust(lens[col])+'│')
            self.text.insert(END, '\n')
        self.text.insert('3.0', '├'+'┼'.join(['─'*i for i in lens])+'┤\n')
        self.text.insert(END, '└'+'┴'.join(['─'*i for i in lens])+'┘\n')

    @staticmethod
    def _line_length(line):
        nl = 0
        length = 0
        while nl != -1:
            last_nl = nl
            nl = line.find('\n', nl+1)
            if nl != -1:
                length = max(nl - last_nl, length)
            else:
                length = max(len(line) - last_nl, length)
        return length


if __name__ == '__main__':
    conn = create_connection('test.sqlite')
    init_db(conn) # TODO: ???

    gui = GuiThought()
    gui.mainloop()

    # conn.commit() # TODO
    conn.close()