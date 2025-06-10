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
    
    def add_account():
        username = username_entry.get().strip()
        password = password_entry.get().strip()
        email = email_entry.get().strip()
        display_name = displayname_entry.get().strip()

        if not username or not password or not email:
            messagebox.showerror("Error", "All fields are required!")
            return
        if manager.add_account(username, password, email, display_name):
            messagebox.showinfo("Success", f"Account {username} added successfully!")
            username_entry.delete(0, 'end')
            password_entry.delete(0, 'end')
            email_entry.delete(0, 'end')
            displayname_entry.delete(0, 'end')
        else:
            messagebox.showerror("Error", f"Failed to add account {username}. It may already exist.")
    def import_accounts():
        import tkinter.filedialog as filedialog
        file_path = filedialog.askopenfilename(
            title="Select TXT File",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if file_path:
            if manager.import_accounts_txt(file_path):
                messagebox.showinfo("Success", "Accounts imported successfully!")
            else:
                messagebox.showerror("Error", "Failed to import accounts. Please check the file format.")
    buttons_frame = customtkinter.CTkFrame(frame)
    buttons_frame.pack(pady=10)

    add_button = customtkinter.CTkButton(buttons_frame, text="➕ Add Account", command=add_account, width=120)
    add_button.pack(side="left", padx=(0, 10))

    import_button = customtkinter.CTkButton(buttons_frame, text="📁 Import TXT", command=import_accounts, width=120)
    import_button.pack(side="left")

    list_frame = customtkinter.CTkFrame(frame)
    list_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))

    list_title = customtkinter.CTkLabel(list_frame, text='Account List', width=40, height=28, fg_color='transparent', font=("Arial", 16, "bold"))
    list_title.pack(pady=10)

    accounts_scroll = customtkinter.CTkScrollableFrame(list_frame, height=200)
    accounts_scroll.pack(expand=True, fill="both", padx=10, pady=(0, 10))

    def refresh_accounts():
    # Clear existing widgets
        for widget in accounts_scroll.winfo_children():
            widget.destroy()

        accounts = manager.list_accounts()
        if not accounts:
           no_accounts = customtkinter.CTkLabel(accounts_scroll, text="No accounts found")
           no_accounts.pack(pady=20)
        else:
            for account in accounts:
                account_frame = customtkinter.CTkFrame(accounts_scroll)
                account_frame.pack(fill="x", padx=5, pady=5)
            
            # Account info
                info_text = f"👤 {account.username} | 📧 {account.email} | 📝 {account.display_name}"
                account_label = customtkinter.CTkLabel(account_frame, text=info_text)
                account_label.pack(side="left", padx=10, pady=5)
            
            # Remove button
                def remove_account(username=account.username):
                    if messagebox.askyesno("Confirm", f"Remove account '{username}'?"):
                        if manager.remove_account(username):
                             messagebox.showinfo("Success", f"Account '{username}' removed!")
                             refresh_accounts()
                    else:
                        messagebox.showerror("Error", "Failed to remove account!")
            
                remove_btn = customtkinter.CTkButton(account_frame, text="❌", 
                                               command=remove_account, width=40, height=25)
                remove_btn.pack(side="right", padx=10, pady=5)

# Refresh button
    refresh_button = customtkinter.CTkButton(list_frame, text="🔄 Refresh", command=refresh_accounts)
    refresh_button.pack(pady=5)

# Initial load
    refresh_accounts()



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
