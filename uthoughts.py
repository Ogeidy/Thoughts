from tkinter import *
from tkinter import ttk
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

        Label(self, text='Thought:').grid(row=0, column=0)
        self.name = Entry(self, width=50)
        self.name.grid(row=0, column=1, pady=5)

        Label(self, text='Description:').grid(row=1, column=0, pady=5, sticky=N)
        self.descr = Text(self, width=50, height=10)
        self.descr.grid(row=1, column=1, pady=5)

        Label(self, text='Date:').grid(row=2, column=0)
        self.date = DateEntry(self, date_pattern='y-mm-dd', width=49)
        self.date.grid(row=2, column=1, pady=5)

        self.btn_ok = Button(self,
                    text='Ok',
                    width=10, height=1,
                    bg='white', fg='black')
        self.btn_ok.bind('<Button-1>', self.submit)
        self.btn_ok.grid(row=3, column=0, columnspan=2, pady=5)

    def submit(self, event):
        print(self.name.get())
        print(self.descr.get('1.0', END))
        print(self.date.get_date())



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
                    wrap='word')
        self.text.pack(side='left', fill='both')
        self.text_scroll = Scrollbar(self.info_frame, command=self.text.yview)
        self.text_scroll.pack(side='right', fill=Y)
        self.text.config(yscrollcommand=self.text_scroll.set)

        self.btn_all = Button(self.ctrl_frame,
                    text='All',
                    width=10, height=1,
                    bg='white', fg='black')
        self.btn_all.bind('<Button-1>', lambda event: self.get_data(event, type='all'))
        self.btn_all.pack()

        self.btn_thoughts = Button(self.ctrl_frame,
                    text='Thoughts',
                    width=10, height=1,
                    bg='white', fg='black')
        self.btn_thoughts.bind('<Button-1>', lambda event: self.get_data(event, type='thought'))
        self.btn_thoughts.pack()

        self.btn_mentions = Button(self.ctrl_frame,
                    text='Mentions',
                    width=10, height=1,
                    bg='white', fg='black')
        self.btn_mentions.bind('<Button-1>', lambda event: self.get_data(event, type='mention'))
        self.btn_mentions.pack()

        self.btn_tags = Button(self.ctrl_frame,
                    text='Tags',
                    width=10, height=1,
                    bg='white', fg='black')
        self.btn_tags.bind('<Button-1>', lambda event: self.get_data(event, type='tag'))
        self.btn_tags.pack()


    def get_data(self, event=None, type=None):
        self.text.delete('1.0', END)
        data = select(conn, type)
        lens = [max([len(str(row[i])) for row in data]) for i in range(len(data[0]))]
        self.text.insert(END, '┌'+'┬'.join(['─'*i for i in lens])+'┐\n')
        for th in data:
            self.text.insert(END, '│')
            for j in range(len(th)):
                self.text.insert(END, str(th[j]).ljust(lens[j])+'│')
            self.text.insert(END, '\n')
        self.text.insert('3.0', '├'+'┼'.join(['─'*i for i in lens])+'┤\n')
        self.text.insert(END, '└'+'┴'.join(['─'*i for i in lens])+'┘\n')


if __name__ == '__main__':
    conn = create_connection('test.sqlite')
    init_db(conn) # ???

    gui = GuiThought()
    gui.mainloop()

    conn.commit()
    conn.close()