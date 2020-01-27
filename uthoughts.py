from tkinter import *

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

    info_frame = Frame(root, bg='gray', bd=10)
    ctrl_frame = Frame(root, bg='#eeeeee', bd=10)
    info_frame.pack(side='left', fill='both')
    ctrl_frame.pack(side='right', ipadx=10, ipady=10, fill='both')

    textbox = Text(info_frame,
                   width=100,
                   font='Monospace 10',
                   wrap='word')
    textbox.pack()

    btn_all = Button(ctrl_frame,
                text='All',
                width=30, height=1,
                bg='white', fg='black')
    btn_all.bind('<Button-1>', lambda event: get_data(event, type='all'))
    btn_all.pack()

    btn_thoughts = Button(ctrl_frame,
                text='Thoughts',
                width=30, height=1,
                bg='white', fg='black')
    btn_thoughts.bind('<Button-1>', lambda event: get_data(event, type='thought'))
    btn_thoughts.pack()

    btn_mentions = Button(ctrl_frame,
                text='Mentions',
                width=30, height=1,
                bg='white', fg='black')
    btn_mentions.bind('<Button-1>', lambda event: get_data(event, type='mention'))
    btn_mentions.pack()

    btn_tags = Button(ctrl_frame,
                text='Tags',
                width=30, height=1,
                bg='white', fg='black')
    btn_tags.bind('<Button-1>', lambda event: get_data(event, type='tag'))
    btn_tags.pack()

    root.mainloop()

    conn.commit()
    conn.close()