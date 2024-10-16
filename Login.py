# Beginning of Login.py File
from tkinter import *
from tkinter import messagebox
from pymongo import MongoClient
import Game_ui
import miscellaneous


def signup_window(main_menu, my_score_frame, game_frame, start_menu, root):
    # create a new top-level window for signup
    signup_window = Toplevel()
    signup_window.title("Sign Up")
    signup_window.geometry("300x450")
    signup_window.configure(bg="Black")

    # create username label and entry
    username_label = Label(signup_window, text="Username:",fg="White", bg="Black")
    username_label.pack(pady=35)
    username_entry = Entry(signup_window)
    username_entry.pack(pady=0)

    # create password label and entry
    password_label = Label(signup_window, text="Password:", fg="White", bg="Black")
    password_label.pack(pady=15)
    password_entry = Entry(signup_window, show="*")
    password_entry.pack(pady=0)

    # create confirm password label and entry
    confirm_password_label = Label(signup_window, fg="White", bg="Black", text="Confirm Password:")
    confirm_password_label.pack(pady=15)
    confirm_password_entry = Entry(signup_window, show="*")
    confirm_password_entry.pack(pady=0)

    # create sign up button
    signup_button = Button(signup_window, text="Sign Up",bg="White",fg="Black", command=lambda: signup(username_entry.get(), password_entry.get(), confirm_password_entry.get(), signup_window, main_menu, my_score_frame, game_frame, start_menu, root))
    signup_button.pack(pady=40)

    # make the window modal
    signup_window.grab_set()
    signup_window.mainloop()

def login_window(main_menu, my_score_frame, game_frame, start_menu, root):
    # create a new top-level window for login
    login_win = Toplevel()
    login_win.title("Login")
    login_win.geometry("250x300")
    login_win.configure(bg="Black")

    # create username label and entry
    username_label = Label(login_win, text="Username:", bg="Black", fg="White")
    username_label.pack(pady=20)
    username_entry = Entry(login_win)
    username_entry.pack(pady=0)

    # create password label and entry
    password_label = Label(login_win, text="Password:", bg="Black", fg="White")
    password_label.pack(pady=10)
    password_entry = Entry(login_win, show="*")
    password_entry.pack(pady=0)

    # create login button
    login_button = Button(login_win, text="Login", bg="White", fg="Black", command=lambda: login(username_entry.get(), password_entry.get(), login_win, main_menu, my_score_frame, game_frame, start_menu, root))
    login_button.pack(pady=40)

    # make the window modal
    login_win.grab_set()
    login_win.mainloop()

def signup(username, password, confirm_password, signup_win, main_menu, my_score_frame, game_frame, start_menu, root):
  
    if password != confirm_password:
        messagebox.showerror("Error", "Passwords do not match!")
        return
    
    # connect to MongoDB
    client = MongoClient(miscellaneous.connection_string)
    db = client["Game_Database"]
    users = db["Users"]
    
    # check if the username already exists
    if users.count_documents({"username": username}) > 0:
        messagebox.showerror("Error", "Username already exists!")
        return
    
    # create a new user document
    user_doc = {"username": username, "password": password}
    
    # insert the new user document into the users collection
    result = users.insert_one(user_doc)
    
    if result.inserted_id:
        messagebox.showinfo("Success", "Account created successfully!")
        miscellaneous.current_user = username
        Game_ui.create_main_menu_elements(main_menu, my_score_frame, game_frame, start_menu, root)
        Game_ui.switch_frame(start_menu, main_menu)
        client.close()
    else:
        messagebox.showerror("Error", "Failed to create account!")
    
    # Close the signup window
    signup_win.destroy()

def login(username, password, login_win, main_menu, my_score_frame, game_frame, start_menu, root):
    # Connect to MongoDB
    client = MongoClient(miscellaneous.connection_string)
    db = client["Game_Database"]
    users = db["Users"]

    # Query the database for the user's credentials
    user = users.find_one({"username": username})

    # Check if the user exists and if the password matches
    if user and user["password"] == password:
        messagebox.showinfo("Success", "Login successful!")
        # Close the login window
        login_win.destroy()
        miscellaneous.current_user = username
        Game_ui.create_main_menu_elements(main_menu, my_score_frame, game_frame, start_menu, root)
        Game_ui.switch_frame(start_menu, main_menu)
        client.close()
    else:
        messagebox.showerror("Error", "Invalid username or password")

def guest_login(main_menu, my_score_frame, game_frame, start_menu, root):
    # logic for guest login
    miscellaneous.current_user = "Guest"
    # create main menu elements
    Game_ui.create_main_menu_elements(main_menu, my_score_frame, game_frame, start_menu, root)
    Game_ui.switch_frame(start_menu, main_menu)