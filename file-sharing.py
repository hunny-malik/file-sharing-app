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

def Send():
    window = Toplevel(root)
    window.title('Send')
    window.geometry('450x560+500+200')
    window.configure(bg = '#f4fdfe')
    window.resizable(False, False)


    def select_file():
        global filename
        filename = filedialog.askopenfilename(initialdir = os.getcwd(),
                                                title = 'Select File',
                                                filetype = (('file_type (*.txt)', '*.txt'),('all files (*.*)', '*.*')))


    def sender():
        s = socket.socket()
        host = socket.gethostname()
        port = 8080
        s.bind((host,port))
        s.listen(1)
        print(host)
        conn, addr = s.accept()
        with open(filename, 'rb') as file:
            file_data = file.read(1024)
            while file_data:
                conn.send(file_data)  # Continuously send file data in chunks
                file_data = file.read(1024)
        conn.close()




    image_icon1 = PhotoImage(file = 'Images/send.png')
    window.iconphoto(False, image_icon1)

    Sbackground = PhotoImage(file = 'Images/sender.png')
    Label(window, image = Sbackground).place(x = -2, y = 0)

    Mbackground = PhotoImage(file = 'Images/id.png')
    Label(window, image = Mbackground, bg = '#f4fdfe').place(x = 100, y = 260)

    host = socket.gethostname()
    Label(window, text = f'ID: {host}', bg = 'white', fg = 'black', font = 'arial 15').place(x = 140, y = 290)


    Button(window, text = '+ Select File', width = 10, height = 1, font = 'arial 14 bold', bg = '#fff', fg = '#000', command = select_file).place(x = 160, y = 150)
    Button(window, text = 'Send', width = 8, height = 1, font = 'arial 14 bold', bg = '#000', fg = '#fff', command = sender).place(x = 300, y = 150)

    window.mainloop()


def Receive():
    main = Toplevel(root)
    main.title('Receive')
    main.geometry('450x560+500+200')
    main.configure(bg = '#f4fdfe')
    main.resizable(False, False)


    def receiver():
        ID = SenderID.get()
        filename1 = incoming_file.get()

        s = socket.socket()
        port = 8080
        s.connect((ID, port))
        with open(filename1, 'wb') as file:
            while True:
                file_data = s.recv(1024)
                if not file_data:  # If no more data is received, stop reading
                    break
                file.write(file_data)
        s.close()


    image_icon2 = PhotoImage(file = 'Images/receive.png')
    main.iconphoto(False, image_icon2)

    Hbackground = PhotoImage(file = 'Images/reciver.png')
    Label(main, image = Hbackground).place(x = -2, y = 0)

    logo = PhotoImage(file = 'Images/logo.png')
    Label(main, image = logo, bg = '#f4fdfe').place(x =10, y = 250)

    Label(main, text = 'Receive', font = ('arial', 20), bg = '#f4fdfe').place(x = 100, y = 280)

    Label(main, text = 'Input sender ID', font = ('arial 10 bold'), bg = '#f4fdfe').place(x = 20, y = 340)
    SenderID = Entry(main, width = 25, fg = 'black', border = 2, bg = 'white', font = ('arial', 15))
    SenderID.place(x = 20, y = 370)
    SenderID.focus()

    Label(main, text = 'Filename for the incoming file:', font = ('arial 10 bold'), bg = '#f4fdfe').place(x = 20, y = 420)
    incoming_file = Entry(main, width = 25, fg = 'black', border = 2, bg = 'white', font = ('arial', 15))
    incoming_file.place(x = 20, y = 450)

    rr = Button(main, text = 'Receive', compound = LEFT, width = 13, bg = '#39c790', font = 'arial 14 bold', command = receiver)
    rr.place(x = 20, y = 500)




    main.mainloop()





#icon code
image_icon = PhotoImage(file = 'Images/icon.png')
root.iconphoto(False, image_icon)


Label(root, text = 'File Sharing', font = ('SangBleu', 20, 'bold'), bg = '#f4fdfe').place(x = 30, y = 30)

Frame(root, width = 400, height = 2, bg = '#f3f5f6').place(x = 25, y = 80)

send_image = PhotoImage(file = 'Images/send.png')
send = Button(root, image = send_image, bg = '#f4fdfe', bd = 0, width=100, height=100, command = Send)
send.place(x = 50, y = 85)

receive_image = PhotoImage(file = 'Images/receive.png')
receive = Button(root, image = receive_image, bg = '#f4fdfe', bd = 0, width=100, height=100, command = Receive)
receive.place(x = 300, y = 85)


Label(root, text = 'Send', font = ('Acumin Variable concept', 17, 'bold'), bg = '#f4fdfe').place(x = 65, y = 165)
Label(root, text = 'Receive', font = ('Acumin Variable concept', 17, 'bold'), bg = '#f4fdfe').place(x = 305, y = 165)


background = PhotoImage(file = 'Images/background.png')
Label(root, image = background).place(x = -2, y = 335)

Label(root, text = 'Team Name', font = ('SangBleu', 30, 'bold'), bg = '#f4fdfe').place(x = 25, y = 266)



root.mainloop()