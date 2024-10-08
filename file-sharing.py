from tkinter import *
import socket
from tkinter import filedialog
from tkinter import messagebox
import os
import time


root = Tk()
root.title('File Sharing App')
root.geometry('450x560+500+200')
root.configure(bg='#f4fdfe')
root.resizable(False, False)

def Send():
    window = Toplevel(root)
    window.title('Send')
    window.geometry('450x560+500+200')
    window.configure(bg='#f4fdfe')
    window.resizable(False, False)

    def select_file():
        global filename
        filename = filedialog.askopenfilename(initialdir=os.getcwd(),
                                                title='Select File',
                                                filetypes=(('file_type (.txt)', '.txt'), ('all files (.)', '.')))

    def sender():
        global allow
        s = socket.socket()
        host = socket.gethostname()
        port = 8080
        s.bind((host, port))
        s.listen(1)
        print(f"Host: {host}. Waiting for connection...")

        conn, addr = s.accept() 

        # Retrieve the hostname from the client's IP address
        client_hostname = socket.gethostbyaddr(addr[0])[0]
        client_address = f"{client_hostname}:{addr[1]}"

        temp = 0
        while True:
            allow = messagebox.askyesno("Connection Request", f"Allow connection from {client_address}?")
            if allow:
                # Send a confirmation to the receiver
                conn.send("ALLOWED".encode())
                break
            temp += 0.1
            time.sleep(0.1)
            if temp == 15:
                allow = False
                conn.send("DENIED".encode())
                break

        if allow:
            print(f"Connection allowed from {client_address}")
            with open(filename, 'rb') as file:
                file_data = file.read(1024)
                while file_data:
                    conn.send(file_data) 
                    file_data = file.read(1024)
            conn.close()
            messagebox.showinfo("File Sent", "File sent successfully!")
        else:
            print("Connection denied")
            conn.close() 
            messagebox.showinfo("Connection Denied", "You denied the connection.")


    image_icon1 = PhotoImage(file='Images/send.png')
    window.iconphoto(False, image_icon1)

    Sbackground = PhotoImage(file='Images/sender.png')
    Label(window, image=Sbackground).place(x=-2, y=0)

    Mbackground = PhotoImage(file='Images/id.png')
    Label(window, image=Mbackground, bg='#f4fdfe').place(x=100, y=260)

    host = socket.gethostname()
    Label(window, text=f'ID: {host}', bg='white', fg='black', font='arial 15').place(x=140, y=290)

    Button(window, text='+ Select File', width=10, height=1, font='arial 14 bold', bg='#fff', fg='#000', command=select_file).place(x=160, y=150)
    Button(window, text='Send', width=8, height=1, font='arial 14 bold', bg='#000', fg='#fff', command=sender).place(x=300, y=150)

    window.mainloop()


def Receive():
    main = Toplevel(root)
    main.title('Receive')
    main.geometry('450x560+500+200')
    main.configure(bg='#f4fdfe')
    main.resizable(False, False)

    def receiver():
        global allow
        ID = SenderID.get()

        s = socket.socket()
        port = 8080
        s.connect((ID, port))

        # Wait for the confirmation from the sender
        confirmation = s.recv(1024).decode()

        if confirmation == "ALLOWED":
            # Open a save dialog to select the file location and name
            filename1 = filedialog.asksaveasfilename(
                defaultextension=".txt",  # Set default extension
                filetypes=[("All files", "."), ("Text files", "*.txt")],  # Specify file types
                title="Save File As"  # Title for the dialog
            )

            if not filename1:  # If the user cancels the dialog
                s.close()
                return

            # Proceed to receive the file
            with open(filename1, 'wb') as file:
                while True:
                    file_data = s.recv(1024)
                    if not file_data:
                        break
                    file.write(file_data)
            s.close()
            messagebox.showinfo("Success", f"File received and saved as {os.path.basename(filename1)}")
        else:
            s.close()
            messagebox.showinfo("Connection Denied", "File transfer was denied.")


    image_icon2 = PhotoImage(file='Images/receive.png')
    main.iconphoto(False, image_icon2)

    Hbackground = PhotoImage(file='Images/reciver.png')
    Label(main, image=Hbackground).place(x=-2, y=0)

    logo = PhotoImage(file='Images/logo.png')
    Label(main, image=logo, bg='#f4fdfe').place(x=10, y=250)

    Label(main, text='Receive', font=('arial', 20), bg='#f4fdfe').place(x=100, y=280)

    Label(main, text='Input sender ID', font=('arial 10 bold'), bg='#f4fdfe').place(x=20, y=340)
    SenderID = Entry(main, width=25, fg='black', border=2, bg='white', font=('arial', 15))
    SenderID.place(x=20, y=370)
    SenderID.focus()

    rr = Button(main, text='Receive', compound=LEFT, width=13, bg='#39c790', font='arial 14 bold', command=receiver)
    rr.place(x=20, y=500)

    main.mainloop()


# Icon code
image_icon = PhotoImage(file='Images/icon.png')
root.iconphoto(False, image_icon)

Label(root, text='File Sharing', font=('SangBleu', 20, 'bold'), bg='#f4fdfe').place(x=30, y=30)

Frame(root, width=400, height=2, bg='#f3f5f6').place(x=25, y=80)

send_image = PhotoImage(file='Images/send.png')
send = Button(root, image=send_image, bg='#f4fdfe', bd=0, width=100, height=100, command=Send)
send.place(x=50, y=85)

receive_image = PhotoImage(file='Images/receive.png')
receive = Button(root, image=receive_image, bg='#f4fdfe', bd=0, width=100, height=100, command=Receive)
receive.place(x=300, y=85)

Label(root, text='Send', font=('Acumin Variable concept', 17, 'bold'), bg='#f4fdfe').place(x=65, y=165)
Label(root, text='Receive', font=('Acumin Variable concept', 17, 'bold'), bg='#f4fdfe').place(x=305, y=165)

background = PhotoImage(file='Images/background.png')
Label(root, image=background).place(x=-2, y=335)

Label(root, text='Connection Crew', font=('SangBleu', 25, 'bold'), bg='#f4fdfe').place(x=25, y=272)

root.mainloop()