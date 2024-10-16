# Beginning of Cell.py File

from tkinter import Button
from threading import Lock
import miscellaneous


lock = Lock()

class Cell:

    # list to add all the cells created to
    all = []

    def __init__(self, x, y):

        # indicates if the cell is part of the solution
        self.colored = False  
        # indicates if the cell is solved
        self.solved = False
        # indicates if the cell is marked by the user
        self.marked = False

        self.cell_btn_object = None
        self.x = x
        self.y = y

        Cell.all.append(self)

    # method to create a button/cell
    def create_btn_object(self, location):
        btn = Button(
            location, 
            width=5,
            height=2,
        )
        btn.bind('<Button-1>', self.left_click_actions)
        btn.bind('<Button-3>', self.right_click_actions)
        self.cell_btn_object = btn

    def left_click_actions(self, event):
        if self.colored and not self.solved:
            self.color_cell()
            self.solved = True
            miscellaneous.solved += 1
            if miscellaneous.solved == miscellaneous.total:
                miscellaneous.finished = True
        elif self.marked or self.solved:
            pass
        else: 
            miscellaneous.WCC += 1
            
    def right_click_actions(self, event):
        if not self.marked and not self.colored:
            self.mark_cell()
            self.marked = True
        elif self.marked or self.solved:
            pass
        else:
            miscellaneous.WCC += 1
         
    def mark_cell(self):
        self.cell_btn_object.configure(bg='grey', fg='white',text='X')
       
    def color_cell(self):
        self.cell_btn_object.configure(bg='black')
  
    # method that uses the level information to paint the cells that are required for solution
    @staticmethod
    def place_color(level):
        #miscellaneous.total = 0
        for cell in Cell.all:
            if level[cell.x][cell.y] == 1:
                cell.colored = True
               # miscellaneous.total += 1 

    @staticmethod
    def reset_board():
        for cell in Cell.all:
            cell.solved = False
            cell.colored = False
            cell.marked = False
                
    # for printing purposes
    def __repr__(self): 
        return f"Cell({self.x},{self.y})"
    
    # levelguide_vertical loops through each row of the "level" array and counts the number of consecutive 1's in each row, 
    # then adds those counts to a list called "rowcount". It then appends the "rowcount" list to the "guide" list, 
    # which eventually contains a list for each row of "level" that indicates the number of consecutive 1's in that row.
    @classmethod
    def levelguide_vertical(cls, level):
        guide = []
        for y in range(len(level)):
            rowcount = []
            count = 0
            for x in range(len(level)):
                if level[x][y] == 1:
                    count += 1
                elif count > 0:
                   rowcount.append(count)
                   count = 0
            if count > 0:
                rowcount.append(count)
            if not rowcount:
                rowcount.append(0)
            guide.append(rowcount)
        
        return guide
    


    # levelguide_horizontal loops through each row of the "level" array and counts the number of consecutive 1's in each row. 
    # If a row contains no 1's, it appends 0 to the "rowcount" list. It then appends the "rowcount" list to the "guide" list, 
    # which eventually contains a list for each row of "level" that indicates the number of consecutive 1's in that row. 
    # The method returns the final "guide" list.
    @classmethod
    def levelguide_horizontal(cls, level):
        guide = []
        for row in level:
            rowcount = []
            count = 0
            has_one = False
            for cell in row:
                if cell == 1:
                    count += 1
                    has_one = True
                elif count > 0:
                    rowcount.append(count)
                    count = 0
            if count > 0:
                rowcount.append(count)
            if not has_one:
                rowcount.append(0)
            guide.append(rowcount)
        
        return guide
    
