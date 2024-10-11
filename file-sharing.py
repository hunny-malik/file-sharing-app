import socket
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import os
import time

root = Tk()
root.title('File Sharing App')
root.geometry('450x560+500+200')
root.configure(bg='#f4fdfe')
root.resizable(False, False)

selected_files = []  # List to hold selected files

def Send():
    window = Toplevel(root)
    window.title('Send')
    window.geometry('450x560+500+200')
    window.configure(bg='#f4fdfe')
    window.resizable(False, False)

    def select_files():
        global selected_files
        selected_files = filedialog.askopenfilenames(initialdir=os.getcwd(),
                                                     title='Select Files',
                                                     filetypes=(('All files', '*.*'),))
        # Check if files are selected
        if selected_files:
            file_label.config(text=f"{len(selected_files)} files selected")
        else:
            file_label.config(text='No files selected')

    def sender():
        if not selected_files:
            messagebox.showwarning("Warning", "No files selected!")
            return

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
                conn.send("ALLOWED".encode())
                break
            temp += 0.1
            time.sleep(0.1)
            if temp >= 15:
                conn.send("DENIED".encode())
                conn.close()
                return

        print(f"Connection allowed from {client_address}")
        conn.send(str(len(selected_files)).encode())
        time.sleep(0.1)

        for filename in selected_files:
            conn.send(os.path.basename(filename).encode())
            time.sleep(0.1)

            file_size = os.path.getsize(filename)
            conn.send(str(file_size).encode())
            time.sleep(0.1)

            with open(filename, 'rb') as file:
                file_data = file.read(1024)
                while file_data:
                    conn.send(file_data)
                    file_data = file.read(1024)

        conn.close()
        messagebox.showinfo("File Sent", "Files sent successfully!")

    image_icon1 = PhotoImage(file='Images/send.png')
    window.iconphoto(False, image_icon1)

    Sbackground = PhotoImage(file='Images/sender.png')
    Label(window, image=Sbackground).place(x=-2, y=0)

    Mbackground = PhotoImage(file='Images/id.png')
    Label(window, image=Mbackground, bg='#f4fdfe').place(x=100, y=260)

    host = socket.gethostname()
    Label(window, text=f'ID: {host}', bg='white', fg='black', font='arial 15').place(x=140, y=290)

    Button(window, text='+ Select Files', width=15, height=1, font='arial 14 bold', bg='#fff', fg='#000', command=select_files).place(x=160, y=150)
    Button(window, text='Send', width=8, height=1, font='arial 14 bold', bg='#000', fg='#fff', command=sender).place(x=300, y=150)

    file_label = Label(window, text='No files selected', fg='black', font=('arial', 15), bg='#f4fdfe')
    file_label.place(x=160, y=65)

    window.mainloop()

def Receive():
    main = Toplevel(root)
    main.title('Receive')
    main.geometry('450x560+500+200')
    main.configure(bg='#f4fdfe')
    main.resizable(False, False)

    def receiver():
        ID = SenderID.get()
        if not ID:
            messagebox.showerror("Error", "Please input sender ID!")
            return

        s = socket.socket()
        port = 8080

        try:
            s.connect((ID, port))
        except ConnectionRefusedError:
            messagebox.showerror("Connection Error", "No connection could be made. Make sure the sender is active.")
            return

        confirmation = s.recv(1024).decode()

        if confirmation == "ALLOWED":
            print("Confirmation received: ALLOWED")

            num_files = int(s.recv(1024).decode())
            print(f"Number of files to receive: {num_files}")

            if num_files > 0:
                for _ in range(num_files):
                    file_name = s.recv(1024).decode()
                    print(f"Receiving file: {file_name}")

                    file_size = int(s.recv(1024).decode())
                    print(f"File size: {file_size} bytes")

                    download_path = os.path.join(os.path.expanduser("~"), "Downloads", file_name)
                    with open(download_path, 'wb') as file:
                        total_received = 0
                        while total_received < file_size:
                            file_data = s.recv(1024)
                            total_received += len(file_data)
                            file.write(file_data)

                    print(f"File {file_name} received and saved to {download_path}")

                messagebox.showinfo("Success", "Files received successfully!")
            else:
                messagebox.showinfo("No Files", "No files were sent.")
        else:
            messagebox.showwarning("Denied", "Connection was denied by the sender.")

        s.close()

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

    rr = Button(main, text='Receive', width=13, bg='#39c790', font='arial 14 bold', command=receiver)
    rr.place(x=20, y=500)

    main.mainloop()

# Main Window Setup
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
