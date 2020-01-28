from tkinter import *
from tkinter import ttk

from thoughts.core_thoughts import *


def get_data(event=None, type=None):
    textbox.delete('1.0', END)
    data = select(conn, type)
    lens = [max([len(str(row[i])) for row in data]) for i in range(len(data[0]))]
    textbox.insert(END, '┌'+'┬'.join(['─'*i for i in lens])+'┐\n')
    for th in data:
        textbox.insert(END, '│')
        for j in range(len(th)):
            textbox.insert(END, str(th[j]).ljust(lens[j])+'│')
        textbox.insert(END, '\n')
    textbox.insert('3.0', '├'+'┼'.join(['─'*i for i in lens])+'┤\n')
    textbox.insert(END, '└'+'┴'.join(['─'*i for i in lens])+'┘\n')


if __name__ == '__main__':
    conn = create_connection('test.sqlite')
    init_db(conn) # ???

    root = Tk()
    root.title('Thoughts')

    main_nb = ttk.Notebook(root)
    main_nb.pack(expand=1, fill='both')
    get_frame = Frame(main_nb)
    thought_frame = Frame(main_nb, padx=10, pady=10)
    tag_frame = Frame(main_nb)
    main_nb.add(thought_frame, text='Thoughts')
    main_nb.add(get_frame, text='Show')
    main_nb.add(tag_frame, text='Tags')

    info_frame = Frame(get_frame, padx=10, pady=10)
    ctrl_frame = Frame(get_frame, padx=10, pady=10)
    info_frame.pack(side='left', fill='both')
    ctrl_frame.pack(side='right', ipadx=10, ipady=10, fill='both')

    textbox = Text(info_frame,
                   width=100,
                   font='Monospace 10',
                   wrap='word')
    textbox.pack(side='left', fill='both')
    scroll = Scrollbar(info_frame, command=textbox.yview)
    scroll.pack(side='right', fill=Y)
    textbox.config(yscrollcommand=scroll.set)

    btn_all = Button(ctrl_frame,
                text='All',
                width=10, height=1,
                bg='white', fg='black')
    btn_all.bind('<Button-1>', lambda event: get_data(event, type='all'))
    btn_all.pack()

    btn_thoughts = Button(ctrl_frame,
                text='Thoughts',
                width=10, height=1,
                bg='white', fg='black')
    btn_thoughts.bind('<Button-1>', lambda event: get_data(event, type='thought'))
    btn_thoughts.pack()

    btn_mentions = Button(ctrl_frame,
                text='Mentions',
                width=10, height=1,
                bg='white', fg='black')
    btn_mentions.bind('<Button-1>', lambda event: get_data(event, type='mention'))
    btn_mentions.pack()

    btn_tags = Button(ctrl_frame,
                text='Tags',
                width=10, height=1,
                bg='white', fg='black')
    btn_tags.bind('<Button-1>', lambda event: get_data(event, type='tag'))
    btn_tags.pack()

    Label(thought_frame, text='Thought').grid(row=0, column=0)
    th_name = Entry(thought_frame)
    th_name.grid(row=0, column=1)
    Label(thought_frame, text='Description').grid(row=1, column=0)
    th_descr = Entry(thought_frame)
    th_descr.grid(row=1, column=1)
    

    root.mainloop()

    conn.commit()
    conn.close()