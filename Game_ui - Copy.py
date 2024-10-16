# Beginning of Game_UI.py File
from tkinter import *
import miscellaneous
from cell import *
import Levels
import Login
import time
from pymongo import MongoClient
from threading import Thread

def switch_frame(current_frame, next_frame):
    destroy_widgets(current_frame)
    current_frame.place_forget()
    next_frame.place(x=0, y=0)

def destroy_widgets(current_frame):
    for widget in current_frame.winfo_children():
        try:
            widget.destroy()
        except EXCEPTION as e:
            print("Error: ", e)

def signout(main_menu, start_menu):
    miscellaneous.current_user = ''
    destroy_widgets(main_menu)
    switch_frame(main_menu, start_menu)

def create_root():
    root = Tk()
    root.configure(bg="Black")
    root.geometry(f'{miscellaneous.WIDTH}x{miscellaneous.HEIGHT}')
    root.title("Pixel Logic")
    root.resizable(False, False)
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (miscellaneous.WIDTH // 2)
    y = (screen_height // 2) - ((miscellaneous.HEIGHT // 2)+50)
    root.geometry(f"+{x}+{y}")
    return root

def create_start_menu_elements(main_menu, my_score_frame, game_frame, start_menu, root):

    game_title = Label(
    start_menu,
    text="Pixel Logic",
    font=("Helvetica", 64),
    fg="White",
    bg="Black"
    )
    game_title.place(x=miscellaneous.width_percentage(15),y=miscellaneous.height_percentage(42))

    # creating login button
    login_button = Button(start_menu, text="Log In", font=("Helvetica", 16), height=1, width=15, fg="black", bg="white", command=lambda:Login.login_window(main_menu, my_score_frame, game_frame, start_menu, root))
    login_button.place(x=miscellaneous.width_percentage(35), y=miscellaneous.height_percentage(65))

    # creating sign up button
    signup_button = Button(start_menu, text="Sign Up", font=("Helvetica", 16), height=1, width=15, fg="black", bg="white", command=lambda:Login.signup_window(main_menu, my_score_frame, game_frame, start_menu, root))
    signup_button.place(x=miscellaneous.width_percentage(35), y=miscellaneous.height_percentage(75))

    # creating guest button
    guest_button = Button(start_menu, text="Play as Guest", font=("Helvetica", 16), height=1, width=15, fg="black", bg="white", command=lambda:Login.guest_login(main_menu, my_score_frame, game_frame, start_menu, root))
    guest_button.place(x=miscellaneous.width_percentage(35), y=miscellaneous.height_percentage(85))

def create_main_menu_elements(main_menu, my_score_frame, start_menu, game_frame, root):
    
    client = MongoClient(miscellaneous.connection_string)
    db = client["Game_Database"]
    users = db["Users"]
    # Query the database for the user's data
    user_data = users.find_one({"username": miscellaneous.current_user})

    user_label = Label(main_menu, text=miscellaneous.current_user, bg="Black",fg="White", font=("Helvetica", 28, "bold"))
    user_label.place(x=miscellaneous.width_percentage(40), y=miscellaneous.height_percentage(25))

    # return highest score from database, if not found put 0
    if "Game_sessions" in user_data:
        highest_score = max([data.get("Score", 0) for data in user_data["Game_sessions"]])
    else:
        highest_score = 0

    # Create a label for the highest score
    highest_score_label = Label(main_menu, text=f"Highest Score: {highest_score}", bg="Black", fg="White", font=("Helvetica", 14, "bold"), padx=miscellaneous.width_percentage(5), pady=miscellaneous.height_percentage(5))
    highest_score_label.place(x=miscellaneous.width_percentage(30), y=miscellaneous.height_percentage(35))
    
    play_button = Button(
        main_menu, text="PLAY", font=("Helvetica", 18), height=1, width=15, fg="black", bg="white",
        command=lambda: create_game_elements(game_frame, main_menu, root, my_score_frame, start_menu)
    )
    play_button.place(x=miscellaneous.width_percentage(30), y=miscellaneous.height_percentage(65))
    
    my_scores_button = Button(
        main_menu, text="My Scores", font=("Helvetica", 18), height=1, width=15, fg="black", bg="white",
        command=lambda: display_user_data(my_score_frame, main_menu, start_menu, game_frame, root)
    )
    my_scores_button.place(x=miscellaneous.width_percentage(30), y=miscellaneous.height_percentage(75))
    
    # swtiching Labeling text between sign-out/sign up button depending on user status (either signed in or guest)
    if miscellaneous.current_user == 'Guest':    
        btn_text="Sign-up / Login"
    else:
        btn_text="Sign-out"
    signout_button = Button(
        main_menu, text=btn_text, font=("Helvetica", 18), height=1, width=15, fg="black", bg="white",
        command=lambda: (signout(main_menu, start_menu), create_start_menu_elements(main_menu, my_score_frame, game_frame, start_menu, root))
    )
    signout_button.place(x=miscellaneous.width_percentage(30), y=miscellaneous.height_percentage(85))

def display_user_data(my_score_frame, main_menu, start_menu, game_frame, root):

    switch_frame(main_menu, my_score_frame)

    client = MongoClient(miscellaneous.connection_string)
    db = client["Game_Database"]
    users = db["Users"]

    # Query the database for the user's data
    user_data = users.find_one({"username": miscellaneous.current_user})

    user_label = Label(my_score_frame, text=miscellaneous.current_user, bg="Black",fg="White", font=("Helvetica", 28, "bold"))
    user_label.grid(row=0, column=1, columnspan=1, sticky="N", pady=18)

    # Create a table header
    header_labels = ["Score", "Level", "Date"]
    for i, label in enumerate(header_labels):
        header_label = Label(my_score_frame, text=label, bg="Black",fg="White", font=("Helvetica", 14, "bold"), padx=miscellaneous.width_percentage(5), pady=miscellaneous.height_percentage(5))
        header_label.grid(row=1, column=i)
    
    canvas = Canvas(my_score_frame, bg="black")
    canvas.grid(row=2, column=0, columnspan=3, padx=miscellaneous.width_percentage(2), pady=miscellaneous.height_percentage(2), sticky="NSEW")

    # Add a scrollbar to the canvas
    scrollbar = Scrollbar(my_score_frame, orient="vertical", command=canvas.yview)
    scrollbar.grid(row=2, column=3, sticky="NS")

    # Configure the canvas to use the scrollbar
    canvas.configure(yscrollcommand=scrollbar.set)

    # Create a frame inside the canvas to hold the table
    table_frame = Frame(canvas, bg="black")

    # Add the table frame to the canvas
    canvas.create_window((0, 0), window=table_frame, anchor="nw")

    # Set the width of the canvas to match the width of the table frame
    table_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"), width=e.width))

    # Loop through the user's data and add each row to the table
    if "Game_sessions" in user_data:
        for i, data in enumerate(user_data["Game_sessions"]):
            score_label = Label(table_frame, text=data["Score"], font=("Helvetica", 12), bg="Black",fg="White", padx=miscellaneous.width_percentage(10), pady=miscellaneous.height_percentage(1))
            score_label.grid(row=i+2, column=0)
            date_label = Label(table_frame, text=data["Date"].strftime("%Y\%m\%d - (%H:%M)"), bg="Black",fg="White", font=("Helvetica", 12), padx=miscellaneous.width_percentage(10), pady=miscellaneous.height_percentage(1))
            date_label.grid(row=i+2, column=2)
            level_label = Label(table_frame, text=data["Level"], font=("Helvetica", 12), bg="Black",fg="White", padx=miscellaneous.width_percentage(10), pady=miscellaneous.height_percentage(1))
            level_label.grid(row=i+2, column=1)
        back_button = Button(
        my_score_frame, text="Back", font=("Helvetica", 12), height=1, width=8, fg="black", bg="white",
        command=lambda:  (create_main_menu_elements(main_menu, my_score_frame, start_menu, game_frame, root), switch_frame(my_score_frame, main_menu))
        )
        back_button.grid(row=len(user_data["Game_sessions"])+3, column=1, columnspan=1, pady=18)
    else:
        empty_label = Label(table_frame, text="empty", font=("Helvetica", 12), bg="Black", fg="White", padx=miscellaneous.width_percentage(10), pady=miscellaneous.height_percentage(1))
        empty_label.grid(row=2, column=0)
        empty_label.grid(row=2, column=1)
        empty_label.grid(row=2, column=2)

        back_button = Button(
        my_score_frame, text="Back", font=("Helvetica", 12), height=1, width=8, fg="black", bg="white",
        command=lambda: (create_main_menu_elements(main_menu, my_score_frame, start_menu, game_frame, root), switch_frame(my_score_frame, main_menu))
        )
        back_button.grid(row=3, column=1, columnspan=1, pady=18)

# Game Frame Functions

def start_thread(game_frame, main_menu, root, my_score_frame, start_menu):
    # creating a thread that will run the score_thread function and starting the thread
    t = Thread(target=score_thread, args=(game_frame, main_menu, root, my_score_frame, start_menu))
    t.start()

def create_game_elements(frame, main_menu, root, my_score_frame, start_menu):
    miscellaneous.reset_game()
    create_centerframe(frame)
    create_sidecenterframe(frame)
    create_abovecenterframe(frame)
    start_thread(frame, main_menu, root, my_score_frame, start_menu)
    switch_frame(main_menu, frame)

def create_centerframe(root):

    centerframe = Frame(
        root,
        bg='green',
        width=miscellaneous.width_percentage(50),
        height=miscellaneous.height_percentage(50)
    )
    centerframe.place(x=miscellaneous.width_percentage(12),y=miscellaneous.height_percentage(28))

    # reseting the list containg all cells
    Cell.all.clear()

    # generating board cells 
    for x in range(miscellaneous.BOARD_SIZE):
        for y in range(miscellaneous.BOARD_SIZE):
            c = Cell(x, y)
            c.create_btn_object(centerframe)
            c.cell_btn_object.grid(
                column=y, row=x
            )

    # reseting all the cell's values
    Cell.reset_board()

    # placing the level onto the cells
    Cell.place_color(Levels.Level)

    return centerframe

def create_abovecenterframe(root):
    abovecenterframe = Frame(
        root,
        bg='black',
        width=miscellaneous.width_percentage(50),
        height=miscellaneous.height_percentage(15)
    )
    abovecenterframe.place(x=miscellaneous.width_percentage(12),y=miscellaneous.height_percentage(15))
    
    # Creating the labels for the guide into above the center frame created
    for i, row in enumerate(Cell.levelguide_vertical(Levels.Level)):
        # if there is only one item in the row, create a label for it
        if len(row) == 1:
            row_label = Label(
                abovecenterframe,
                text=row[0],
                bg='black',
                fg='white',
                padx=17
            )
            row_label.grid(row=0, column=i)
        # if there are multiple items, create a label for each and stack them vertically
        else:
            for j, item in enumerate(row):
                row_label = Label(
                    abovecenterframe,
                    text=item,
                    bg='black',
                    fg='white',
                    padx=18
                )
                row_label.grid(row=j, column=i)

    return abovecenterframe

def create_sidecenterframe(root):
    sidecenterframe = Frame(
        root,
        bg='black',
        width=miscellaneous.width_percentage(10),
        height=miscellaneous.height_percentage(50)
    )
    sidecenterframe.place(x=miscellaneous.width_percentage(5),y=miscellaneous.height_percentage(28))

    # Creating the labels for the guide into the side frame created
    for i, row in enumerate(Cell.levelguide_horizontal(Levels.Level)):
        row_label = Label(
            sidecenterframe,
            text=row,
            bg='black',
            fg='white',
            pady=11,
            padx=5
        )
        row_label.grid(row=i, column=0)

    return sidecenterframe

def score_thread(currframe, nextframe, root, my_score_frame, start_menu):
    # reseting total number of cells to be solved
    miscellaneous.total = 0
    miscellaneous.quit = False

    # counting the number of cell's to be solved
    for cell in Cell.all:
        if cell.colored:    
            miscellaneous.total += 1
    
    title_frame = Frame(currframe, bg='white', width=miscellaneous.WIDTH, height=miscellaneous.height_percentage(12))
    title_frame.propagate(False)
    title_frame.place(x=0, y=0)
        
    quit_button = Button(title_frame, text="Quit", bg="Black", fg="White", command=lambda: miscellaneous.switch_quit_flag())
    quit_button.place(x=miscellaneous.width_percentage(5), y=miscellaneous.height_percentage(5))
    
    game_title = Label(title_frame, text="Pixel Logic", font=("Helvetica", 24), fg="Black", bg="white")
    game_title.place(x=miscellaneous.width_percentage(35), y=miscellaneous.height_percentage(3))

    score_label = Label(title_frame, font=("Helvetica", 12), fg="Black", bg="white", text=f"SCORE: {miscellaneous.SCORE}")
    score_label.place(x=miscellaneous.width_percentage(80), y=miscellaneous.height_percentage(5))

    user_label = Label(title_frame, font=("Helvetica", 12), fg="Black", bg="white", text=miscellaneous.current_user)
    user_label.place(x=miscellaneous.width_percentage(15), y=miscellaneous.height_percentage(5))

    # loops runs while the user has remaining score and hasn't won yet
    while not miscellaneous.won:

        # lock aquire and release is used to manage a shared variables, 
        # when aquiring only one thread can manage the variable, 
        # when releasing the thread leaves the shared variable making it available for other threads
        lock.acquire()

        # in case a user made a mistake, the score subtracts 150
        if miscellaneous.SCORE > 150 and miscellaneous.WCC > 0:
            miscellaneous.SCORE -= 150 * miscellaneous.WCC
            #reseting WCC (wrong cell clicked) flag
            miscellaneous.WCC = 0

        elif miscellaneous.quit:
            miscellaneous.won = True
            create_main_menu_elements(nextframe, my_score_frame, start_menu, currframe, root)
            switch_frame(currframe,nextframe)

        # in case the user is finised with the solution
        elif miscellaneous.finished:
            miscellaneous.save_score()
            miscellaneous.won = True
            show_win_message(root)
            if miscellaneous.retry:
                miscellaneous.switch_retry_flag()
            else:    
                create_main_menu_elements(nextframe, my_score_frame, start_menu, currframe, root)
                switch_frame(currframe,nextframe)
            

        # case the user makes a mistake and the current score is 150 or less
        elif miscellaneous.SCORE <= 150 and miscellaneous.WCC > 0:
            miscellaneous.SCORE = 0
            miscellaneous.won = True
            miscellaneous.WCC = 0
            show_lose_message(root, currframe, nextframe, my_score_frame, start_menu, root)
            

        # decrease the score by 1 each second
        else:
            miscellaneous.SCORE -= miscellaneous.SCORE_DECREASE_RATE
        lock.release()

        # updating the frame to update the score count
        root.after(0, score_label.config, {"text": f"SCORE: {miscellaneous.SCORE}"})
        root.update()

        # making the thread sleep for one second to make sure the score is subtracted by 1 each second
        time.sleep(1)

def run_retry_functions(game_frame, main_menu, frame, win, my_score_frame, start_menu):
    switch_frame(game_frame, main_menu)
    if not miscellaneous.retry:
        miscellaneous.switch_retry_flag()
    create_game_elements(game_frame, main_menu, frame, my_score_frame, start_menu)
    win.destroy()

def run_quit_functions(currframe, nextframe, win, my_score_frame, start_menu, game_frame, root):
        create_main_menu_elements(nextframe, my_score_frame, start_menu, game_frame, root)
        switch_frame(currframe,nextframe)
        win.destroy()

def show_lose_message(frame, game_frame, main_menu, my_score_frame, start_menu, root):
    # create a new top-level window
    win = Toplevel(frame)
    win.title("You Lost!")
    win.geometry("350x200")
    win.configure(bg="Black")
    
    # create a message label with the score
    message = Label(win, text="Better luck next time\nSCORE: {}".format(miscellaneous.SCORE), font=("Helvetica", 14), bg="Black", fg="White")
    message.pack(pady=20)
    
    # create an retry button 
    retry_button = Button(win, text="retry", command=lambda: run_retry_functions(game_frame, main_menu, frame, win, my_score_frame, start_menu), bg="White", fg="Black", width=6, height=1)
    retry_button.pack(pady=10)

    # create an quit button 
    quit_button = Button(win, text="quit", command=lambda: run_quit_functions(game_frame, main_menu, win, my_score_frame, start_menu, game_frame, root), bg="White", fg="Black", width=6, height=1)
    quit_button.pack(pady=15)
    
    # make the window modal (focus must be returned to main window)
    win.grab_set()
    frame.wait_window(win)

def show_win_message(frame):

    # create a new top-level window
    win = Toplevel(frame)
    win.title("Congratulations!")
    win.geometry("350x150")
    win.configure(bg="Black")

    # create a message label with the score
    message = Label(win, text="You won!\nSCORE: {}".format(miscellaneous.SCORE), font=("Helvetica", 14), bg="Black", fg="White")
    message.pack(pady=20)
    
    # create an OK button to close the window
    ok_button = Button(win, text="OK", command=win.destroy, bg="White", fg="Black")
    ok_button.pack(pady=10)
    
    # make the window modal (focus must be returned to main window)
    win.grab_set()
    frame.wait_window(win)
