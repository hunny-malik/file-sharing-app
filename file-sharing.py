from tkinter import *
import socket
from tkinter import filedialog
from tkinter import messagebox
import os


root = Tk()
root.title('File Sharing App')
root.geometry('450x560+500+200')
root.configure(bg='#f4fdfe')
root.resizable(False, False)



#icon code
image_icon = PhotoImage(file = 'Images/icon.png')
root.iconphoto(False, image_icon)


Label(root, text = 'File Sharing', font = ('SangBleu', 20, 'bold'), bg = '#f4fdfe').place(x = 30, y = 30)

Frame(root, width = 400, height = 2, bg = '#f3f5f6').place(x = 25, y = 80)

send_image = PhotoImage(file = 'Images/send.png')
send = Button(root, image = send_image, bg = '#f4fdfe', bd = 0, width=100, height=50)
send.place(x = 50, y = 100)

receive_image = PhotoImage(file = 'Images/receive.png')
receive = Button(root, image = receive_image, bg = '#f4fdfe', bd = 0, width=100, height=50)
receive.place(x = 300, y = 100)


Label(root, text = 'Send', font = ('Acumin Variable concept', 17, 'bold'), bg = '#f4fdfe').place(x = 65, y = 150)
Label(root, text = 'Receive', font = ('Acumin Variable concept', 17, 'bold'), bg = '#f4fdfe').place(x = 305, y = 150)


background = PhotoImage(file = 'Images/background.png')
Label(root, image = background).place(x = -2, y = 334)

Label(root, text = 'Team Name', font = ('SangBleu', 30, 'bold'), bg = '#f4fdfe').place(x = 25, y = 265)



root.mainloop()