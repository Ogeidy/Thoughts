from tkinter import *

from thoughts.core_thoughts import *


def hello(event):
    for th in select_thought(conn):
        print(th)
        textbox.insert('1.0', str(th)+'\n')


if __name__ == '__main__':
    conn = create_connection('test.sqlite')
    init_db(conn) # ???

    root = Tk()

    textbox = Text(root, font='Arial 14', wrap='word')
    textbox.pack()
    btn = Button(root,
                text='Click me',
                width=30, height=5,
                bg='white', fg='black')
    btn.bind('<Button-1>', hello)
    btn.pack()

    root.mainloop()

    conn.commit()
    conn.close()