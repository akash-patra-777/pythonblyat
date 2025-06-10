import customtkinter as customtkinter
from getlogin import TikTokAccountManager, TikTokAccount
from checker import TikTokChecker
from publisher import TikTokPublisher
import tkinter.messagebox as messagebox

manager = TikTokAccountManager()



app = customtkinter.CTk()
app.geometry("800x600")
app.title("TikTok Traffic Manager")

app.resizable(False, False)

label = customtkinter.CTkLabel(app, text='by Akash-patra-777', width=40, height=28, fg_color='transparent')
label.place(x=680, y=550)

frame = customtkinter.CTkFrame(app, width=200, height=200)
frame.grid(column=0, row=1, columnspan=4, padx=10, pady=10, sticky="nsew")
app.grid_columnconfigure(0, weight=1)
app.grid_rowconfigure(1, weight=1)

def clear_content():
    for widget in frame.winfo_children():
        widget.destroy()

def button_getlogin():
    clear_content()

    label = customtkinter.CTkLabel(frame, text='Account Manager', width=40, height=28, fg_color='transparent', font=("Arial", 20, "bold"))
    label.pack(pady=20)
    
    add_frame= customtkinter.CTkFrame(frame)
    add_frame.pack(pady=(0,20), padx=20, fill='x')

    add_title = customtkinter.CTkLabel(add_frame, text='Add Account', width=40, height=28, fg_color='transparent', font=("Arial", 16, "bold"))
    add_title.pack(pady=10)

    input_frame = customtkinter.CTkFrame(add_frame)
    input_frame.pack(pady=(0,20), padx=10, fill='x')

    username_label = customtkinter.CTkLabel(input_frame, text='Username:', width=100, height=28)
    username_label.grid(column=0, row=0, padx=5, pady=5, sticky='w')
    username_entry = customtkinter.CTkEntry(input_frame, width=200)
    username_entry.grid(column=1, row=0, padx=5, pady=5)

    password_label = customtkinter.CTkLabel(input_frame, text='Password:', width=100, height=28)
    password_label.grid(column=2, row=0, padx=5, pady=5, sticky='w')
    password_entry = customtkinter.CTkEntry(input_frame, width=200)
    password_entry.grid(column=3, row=0, padx=5, pady=5)

    email_label = customtkinter.CTkLabel(input_frame, text='Email:', width=100, height=28)
    email_label.grid(column=0, row=1, padx=5, pady=5, sticky='w')
    email_entry = customtkinter.CTkEntry(input_frame, width=200)
    email_entry.grid(column=1, row=1, padx=5, pady=5)

    displayname_label = customtkinter.CTkLabel(input_frame, text='DisplayName(optional):', width=100, height=28)
    displayname_label.grid(column=2, row=1, padx=5, pady=5, sticky='w')
    displayname_entry = customtkinter.CTkEntry(input_frame, width=200)
    displayname_entry.grid(column=3, row=1, padx=5, pady=5)

    




button_login = customtkinter.CTkButton(app, text='Get Login', command=button_getlogin, width=140, height=28)
button_login.grid(column=0, row=0, padx=10, pady=10)

def button_checker():
    print('button pressed')

button_check = customtkinter.CTkButton(app, text='Checker', command=button_checker, width=140, height=28)
button_check.grid(column=1, row=0, padx=10, pady=10)

def button_publisher():
    print('button pressed')

button_pub = customtkinter.CTkButton(app, text='Publisher', command=button_publisher, width=140, height=28)
button_pub.grid(column=2, row=0, padx=10, pady=10)

def button_logs():
    print('button pressed')

button_log = customtkinter.CTkButton(app, text='Logs', command=button_logs, width=140, height=28)
button_log.grid(column=3, row=0, padx=10, pady=10)
app.mainloop()
