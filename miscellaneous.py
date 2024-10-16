# Beginning of miscellaneous.py File
import Levels
import random
import  mongopass
import datetime
from pymongo import MongoClient
from tkinter import *

#BACKGROUNDPATH = r"C:\Users\a7-id\OneDrive\سطح المكتب\College\1214 AML\AML Assignment\bk2.jpg" # Background image file path
connection_string = f"mongodb+srv://bigelk:bimZmiran@tutorial.wqhr5nb.mongodb.net/test" # MongoDB Connection String

WIDTH=600   # Size of Window
HEIGHT=650
BOARD_SIZE = 10 # defines the board size
SCORE = 1500 # defines the score starting point
SCORE_DECREASE_RATE = 1 # the rate which the score decreases by
WCC = 0 # Wrong Cell Clicked Flag
solved = 0 # counts the number of solved cells by the user
total = 0 # counts the number of total cells to be solved
won = False # flag for when a user wins
finished = False # flag for when a user have solved all the required cells 
current_user = ""
retry = False
quit = False


def switch_quit_flag():
    global quit
    if quit:
        quit = False
    else:
        quit = True

def switch_retry_flag():
    global retry
    if retry:
        retry = False
    else:
        retry = True

def reset_game():
    global SCORE, solved, won, finished, retry
    # generating a random number and using that number to pick a level from the All_Levels list (in case the user is not retrying the level)
    if retry:
        pass
    else:
        rndnum = random.randint(0, 7)
        Levels.Level = Levels.All_Levels[rndnum]
    # resets the variables for a new game session
    SCORE = 1500
    solved = 0
    won = False
    finished = False

def save_score():

    client = MongoClient(connection_string)
    db = client["Game_Database"]
    usersDB = db["Users"]

    session_data = {
        "Score": SCORE,
        "Date": datetime.datetime.now(),
        "Level": (Levels.level_indx + 1)
    }

    try:
        # Get the current user document
        user = usersDB.find_one({"username": current_user})
        
        # If the user document doesn't exist, create a new one
        if user is None:
            user = {"username": current_user, "Game_sessions": [session_data]}
            usersDB.insert_one(user)
        else:
            # Check if 'game_sessions' key exists in the user dictionary
            if 'Game_sessions' not in user:
                user['Game_sessions'] = []  # create the key if it doesn't exist
                
            # Add the new session data to the "game_sessions" subcollection
            user["Game_sessions"].append(session_data)
            usersDB.update_one({"_id": user["_id"]}, {"$set": {"Game_sessions": user["Game_sessions"]}})
    except Exception as e:
        print("Error occurred while saving score:", e)
    finally:
        client.close()

def height_percentage(percentage):
    return ((HEIGHT/100) * percentage)

def width_percentage(percentage):
    return ((WIDTH/100) * percentage)