# i pretty sure my comment can confuse the marker, good luck :)
from tkinter import *
from random import *
from tkinter import messagebox
import copy 
import time as t
Origan_sudoku = [ # this is a origan sudoku. sloved. the random sudoku puzzle is generate from it but don't change the origanal one 
    [1,2,3,4,5,6,7,8,9],
    [4,5,6,7,8,9,1,2,3],
    [7,8,9,1,2,3,4,5,6],
    [2,3,4,5,6,7,8,9,1],
    [5,6,7,8,9,1,2,3,4],
    [8,9,1,2,3,4,5,6,7],
    [3,4,5,6,7,8,9,1,2],
    [6,7,8,9,1,2,3,4,5],
    [9,1,2,3,4,5,6,7,8]
]

sudoku=copy.deepcopy(Origan_sudoku) # like now, i don't change any data in the origan_sudoku. everythings changed is only happen in "sudoku"

PlayerRecord=[]
UsedTime=0 # a varible to record the player used time
timer_state=None # a varible to store the timer 
click_count=0 # a varible to lock the timmer (make sure the timer will only exercute once in a game)

def suffle(s): # god, this is the most complicated part (i am making a function to shuffle the hold solved board)
    def h_02(s): # no worries, this "s" means sudoku. i am not running out of variable name :(
        Aswap=randint(0,2) # i am doing the suffle agnist first three row (horizontally)
        Bswap=randint(0,2)
        temp=s[Aswap]
        s[Aswap]=s[Bswap]
        s[Bswap]=temp
    def h_35(s): # i am doing the suffle agnist second three row (horizontally)
        Aswap=randint(3,5)
        Bswap=randint(3,5)
        temp=s[Aswap]
        s[Aswap]=s[Bswap]
        s[Bswap]=temp
    def h_68(s): # i am doing the suffle agnist last three row (horizontally)
        Aswap=randint(6,8)
        Bswap=randint(6,8)
        temp=s[Aswap]
        s[Aswap]=s[Bswap]
        s[Bswap]=temp
    def V_02(s): # i am doing the suffle agnist the first three row (verticallly)
        temp=[]
        Aswap=randint(0,2)
        Bswap=randint(0,2)
        for i in range(9):
            temp.append(s[i][Aswap])
            s[i][Aswap] = s[i][Bswap]
            s[i][Bswap] = temp[i]
    def V_35(s): # i am doing the suffle agnist the second three row (verticallly)
        temp=[]
        Aswap=randint(3,5)
        Bswap=randint(3,5)
        for i in range(9):
            temp.append(s[i][Aswap])
        for i in range(9):
            s[i][Aswap]= s[i][Bswap]
        for i in range(9):
            s[i][Bswap]=temp[i]
    def V_68(s): # i am doing the suffle agnist the last three row (verticallly)
        temp=[]
        Aswap=randint(6,8)
        Bswap=randint(6,8)
        for i in range(9):
            temp.append(s[i][Aswap])
        for i in range(9):
            s[i][Aswap]= s[i][Bswap]
        for i in range(9):
            s[i][Bswap]=temp[i]
    for i in range(3333): # i am crazily suffle the sudoku. this allow me to generate a random sudoku everytime the player play a new game
        swap=randint(1,6)
        if swap==1 :
            h_02(s)
        elif swap==2:
            h_35(s)
        elif swap==3:
            h_68(s)
        elif swap==4:
            V_02(s)
        elif swap==5:
            V_35(s)
        elif swap==6:
            V_68(s)

def check(x, row, col): # a function to check is the player input correct
    for i in range(9):
        if x[row][col] == x[row][i] and i!= col: # checking the duplicate in row, but not the same box (otherwise always repeat.)
            return False
        if x[row][col] == x[i][col] and i!= row: # duplicate in column?
            return False
    
    #finding which box(considering in 3x3) player input his number in
    LocateCoorX = row//3
    LocateCoorY = col//3 
    # looping to find are there a duplicate number in that 3x3 boxes
    for i in range(3): 
        for j in range(3):
            if x[row][col] == x[3*LocateCoorX+i][3*LocateCoorY+j] and ((3*LocateCoorX+i) != row or (3*LocateCoorY + j) != col):
                return False
    # if eventually reach here, it means no problem, good to go! lol
    return True

def EnterValue(x,y): # a function to enter the player input from GUI 
    global ButtonPlayerClickX 
    global ButtonPlayerClickY
    global NumberPlayerSelecting

    if x != -1:   # this means the player NOT clicked the bottomest buttons (i.e. he NOT want to l)
        # store the coordinates of the button
        ButtonPlayerClickX=x
        ButtonPlayerClickY=y

        # input the number into the sudoku list 
        sudoku[ButtonPlayerClickX][ButtonPlayerClickY]=NumberPlayerSelecting 
        buttones[x][y].config(text=NumberPlayerSelecting,fg="green") # now display this input (and make it greennnnn)

    else: # he is going to change his current number selection
        NumberPlayerSelecting=y # storing the number the user is selecting (hope u know what i am saying)


# this function the mixing two function. Make this because the Tkinter button command only allow me to apply one function only
def EnterACheck(x,y): 
    global Nclue, ButtonPlayerClickX,ButtonPlayerClickY, PlayerRecord, click_count

    ButtonPlayerClickY=y # immediatelly update the player movement
    ButtonPlayerClickX=x 
    # and now let me make things being more fannntasy (when the player clicked the button, the row and col turn blue)
    # also the button with the same number turn light blueeeeee
    for i in range(9): # but first let me reset all the buttton to colour white
        for j in range(9):
            buttones[i][j].config(bg="white")
    # then conditionally change the buttones colour
    for i in range(9):
        for j in range(9):
            if x==i or j==y or sudoku[i][j]==sudoku[x][y]:
                buttones[i][j].config(bg="lightblue")
    # OMG this look so good
    # a bug will happen if i don't check is the button already have a answer there, otherwise, the player can 
    # inputing the same correct number 81 times and win. So i need to check is the player input a duplcate answer
    if sudoku[x][y]==0:
        EnterValue(x,y)
        # after enter the value, i need to chang the button colour again. cuz this function was origanally do outside this function
        for i in range(9): # but first let me reset all the buttton to colour white
            for j in range(9):
                buttones[i][j].config(bg="white")
        # then conditionally change the buttones colour
        for i in range(9):
            for j in range(9):
                if x==i or j==y or sudoku[i][j]==sudoku[x][y]:
                    buttones[i][j].config(bg="lightblue")

        # check if the player input valid, if yes, input it into the sudoku list. if no, help player delete it and delete the data in sudoku list 
        if check(sudoku,x,y)==False: 
            messagebox.showinfo(title="wrong",message="wrong !!!! you have made a mistake!!!!!")
            sudoku[x][y]=0
            buttones[x][y].config(fg="red")
        # if the input pass the test, means that Nclue need to minus 1
        else:
            Nclue-=1
        #when NOT clue ==0 , means that no more inorrect clue exist in my game board. means that the player have complete the hold board
        if Nclue==0:
            GameWindow.after_cancel(timer_state) # stop the clock !
            messagebox.showinfo(title="lol",message=f"You have won! it's meaningful. Time: {UsedTime}s")
            PlayerRecord.append(UsedTime)
            click_count=0 # reset the lock of the clock
# this is a function is for user to adjust the hardency. there'll be 3 level (god, medium , EZ)
def Level(d):
    global Nclue, sudoku, UsedTime, click_count
    suffle(Origan_sudoku)# reset the sudoku to advoid Bug appear(no reset, the cule in the board will all disapppear eventually)
    sudoku = copy.deepcopy(Origan_sudoku) # this ensure sudoku is not connecting to Origan_sudoku. allow the change to sudoku don't apply to origan soduku :)

    # the content of this seperated part is for the Function timer()
    UsedTime=0
    if click_count==0:  # i actually should use true or flase to make this timer lock. But anyway. hope u get what i mean. 
        click_count+=1 # maybe i should tell what this is going on in the ppt report. (check the report if u can't understand what i am doing here)
        timer()

    for i in range(9):
        for j in range(9):
            if d ==1:   # check player input
                randomnum=randint(1,81)   # using the probability, drawing 
                if randomnum < 10:
                    sudoku[i][j]=0
            if d ==2:
                randomnum=randint(1,81)
                if randomnum < 30:
                    sudoku[i][j]=0
            if d ==3:
                randomnum=randint(1,81)
                if randomnum < 50:
                    sudoku[i][j]=0
    # before the game start, i wanna count how many clue is NOT provided
    Nclue=0
    for i in range(9):
        for j in range(9):
            if sudoku[i][j]== 0 :
                Nclue+=1
    # dispaly the random board on the GUI
    for i in range(9):
        for j in range(9):
            buttones[i][j].config(text=sudoku[i][j] if sudoku[i][j]!= 0 else "",font=("Arial", 20), fg="black")

def eraser():
    global buttones,sudoku, Nclue
    for i in range(9):
            for j in range(9):
                    buttones[i][j].config(bg="white")
    if ButtonPlayerClickX != -1: # see if the button is valid
        if buttones[ButtonPlayerClickX][ButtonPlayerClickY].cget("fg") == "red": # see if the input valid
            sudoku[ButtonPlayerClickX][ButtonPlayerClickY]=0    # delete things
            buttones[ButtonPlayerClickX][ButtonPlayerClickY].config(text="", fg="black") # change back the setting
# this split is needed to advoid the player click a correct input for 81 times, and Nclue keep decrease and win the game            
        elif buttones[ButtonPlayerClickX][ButtonPlayerClickY].cget("fg") == "green":  # see if the input valid
            sudoku[ButtonPlayerClickX][ButtonPlayerClickY]=0                          # green means player past input
            buttones[ButtonPlayerClickX][ButtonPlayerClickY].config(text="", fg="black") # change back the setting
            Nclue+=1
# this is dectecting the button text colour (is it purple). purple means hint **
        elif buttones[ButtonPlayerClickX][ButtonPlayerClickY].cget("fg") == "purple":  # see if the input valid
            sudoku[ButtonPlayerClickX][ButtonPlayerClickY]=0    # delete things
            buttones[ButtonPlayerClickX][ButtonPlayerClickY].config(text="", fg="black") # change back the setting
            Nclue+=1  # don't forgot the Nclue :)

def hint():
    global sudoku, buttones, Nclue, PlayerRecord, click_count
    possibilities=0 # the is used to count how many possibilities of number a button can have (e.g. 1 or 2 or 3)
    The_only_one=0 # this is used to store the 100 % work number
    for i in range(9):
        for j in range(9):
            if sudoku[i][j]==0: 
                possibilities=0 
                The_only_one=0
                for k in range(9):   # just sub all the number, see if how many posibilities
                    sudoku[i][j]=k+1 
                    if check(sudoku,i,j)==True:
                        possibilities+=1
                if possibilities > 1:   #  if i can't make sure the number in that button is absolutly true, then i just left it a blank
                    sudoku[i][j]=0
                else:     # but if we found that button is 100 % ocrrect
                    for k in range(0,9):  
                        sudoku[i][j]=k+1 
                        if check(sudoku,i,j)==True:
                            The_only_one=k+1
                            break
                    if The_only_one != 0: # it can be no answer. cuz some button just can't be 100 % correct, so the_only_one can be 0
                        buttones[i][j].config(text=The_only_one,fg="purple") 
                        sudoku[i][j]=The_only_one
                        Nclue-=1
                    if Nclue==0:
                        GameWindow.after_cancel(timer_state) # stop the clock !
                        messagebox.showinfo(title="lol",message=f"You have won! Even it's some kind of unmeaningful. Time: {UsedTime}s")
                        PlayerRecord.append(UsedTime) # adding new record to the list
                        click_count=0 # reset the lock of the clock
                    return # this return is actaully a break for the for loop here. breake is not working well in def. but return can do a similar function here
                
# WTF why this thing is working wwtftwtftwfwwfwtfwftwtfwtfwfwf
                    
def answer(): # this is a function to provide pure answer. technicquiely just he is just doing 81 times of hint()
    for i in range(Nclue):
        hint()
    while 0 in sudoku:
        pass  


# this is a function to output user used time (per game)
def timer():
    global UsedTime , timer_state
    UsedTime+=1 
    time_used_Button.config(text=UsedTime, fg="blue")
    # time_state is used to store this process, allow me to change the state (like shut off the clock)
    timer_state=GameWindow.after(1000, timer) # i used after to call timer() himself every 1000ms. to count time.

def record(): # this is a function for button. when the player click the button, the past record will show to the player
    showtext=""
    if PlayerRecord!=[]:  # just prevent the player click it before the game start
        for i in range(len(PlayerRecord)):
            showtext+=f"your {i+1} attemtion record is: {PlayerRecord[i]}s \n " # creating a text with line breaking
        messagebox.showinfo(title="past record",message=showtext )   # and show it 
    else:
        messagebox.showinfo(title="past record",message="you haven't try things yet. click the difficulty to play !")

NumberPlayerSelecting=1
# you can just look directlly into my report, a flow chart is explaining all the code bellow
GameWindow=Tk() #creat the basic game pad
GameWindow.configure(bg='black') # set the blaclkground colour of the game pad  
GameWindow.title("sudoku game") # set the name of the window
GameWindow.geometry("700x750")# adjust the initial size of the game window

ChooseDiffcultyLable=Label(GameWindow, text="mode :").grid(row=0, column=1, columnspan=1,sticky="nsew") # creating choosing level buttones
group2=IntVar(value=-1) 
EzButton=Radiobutton(GameWindow,
                    text="EZ",
                    variable=group2,
                    value=1,
                    command=lambda:Level(1) # adding lambda here is advioding the function execute immediately, Level works only when i click on the button :)
                    ).grid(row=0, column=2, sticky="nsew",columnspan=1) # level ez
EZButton=Radiobutton(GameWindow, text="medium",value=2,variable=group2,command=lambda:Level(2)).grid(row=0, column=3, sticky="nsew",columnspan=1) # level medium
EzButton=Radiobutton(GameWindow, text="god",value=3,variable=group2,command=lambda:Level(3)).grid(row=0, column=4, sticky="nsew",columnspan=1) # level hard
GameWindow.grid_rowconfigure(0, weight=0, minsize=30)  # Fixed height top bar
GameWindow.grid_rowconfigure(1, weight=0, minsize=10)  # Fixed height separator (even this is totally not working)

# Me myslef pls notice that this kind of fommat usaually cause eraserbutton = None, there's nothings actucally inside this varible
eraserbutton=Button(GameWindow, text="eraser",command=lambda:eraser()   # a button for user to delete their input
              ).grid(row=0,column=5,sticky="nsew",columnspan=1,padx=(1,0))

#this is a button for user to have hint (when the player click, the system automatically help player do the sudoku)
hintbutton=Button(GameWindow, text="hint",command=lambda:hint()).grid(row=0,column=6,sticky="nsew",columnspan=1) 

timerlabel=Label(GameWindow, text="used time(s) :").grid(row=0,column=7,sticky="nsew",columnspan=1, padx=(2,0))# just a nomal information display label

# this is my record check button, play click, they can check their past record
time_used_Button=Button(GameWindow, text="",command=lambda:record())
time_used_Button.grid(row=0,column=8,sticky="nsew",columnspan=1) 

for i in range(2, 12):  # these are two very fast function to adjust all the element in once. no need additonal code
    GameWindow.grid_rowconfigure(i, weight=1)
for i in range(9):
    GameWindow.grid_columnconfigure(i, weight=1, uniform='sudoku_cols')  # Critical for equal widths 

InformButton=Button(GameWindow, text="click me",command=lambda: messagebox.showinfo(title="this is the rule :)",message="Fill the 9×9 grid so that each row, column, and 3×3 box contains the numbers 1 to 9 exactly once, without repeating any number.")
                    ).grid(row=0, column=0, sticky="nsew",columnspan=1) #adding a button to explain all the rule of the game

seperator= Label(GameWindow, text="").grid(row=1,column=0,columnspan=9,sticky=EW,pady=4)#created a seperator between the play zone and setting zone
buttones=[] # a 2D list to store button i will create
buttonRow=[] # this is a good thing to help me to create the 2D list "buttones" 

# if my code and comment is still too messy, report helps everything, further explaintion in my report 
for i in range(9): # start to make that 81 button
    for j in range(9):
        pading_V = 4 if (j+1)%3==0 else 1 # setting the pading of each button by tricky skill
        pading_H = 4 if (i+1)%3==0 else 1 
        button=Button(GameWindow, text="", # make the button blank there if that button isn't a hint
                    command=lambda x=i,y=j: EnterACheck(x,y) # creating a lambda to store the coor of the button
                    ) 
        button.grid(row=i+2,column=j,sticky="nsew",pady=(1,pading_H),padx=(1,pading_V))
        buttonRow.append(button)# add that hold row of button into the 2D list
    buttones.append(buttonRow)
    buttonRow=[]# delete all the button in buttonRow
    
group1=IntVar()# the paperation for making player input button (radiobutton)
for i in range(9):# using forloop to generate some player enter buttton
    player_enterbutton=Radiobutton(GameWindow,text=i+1,variable=group1,value=i,
                                   command=lambda r=i+1:EnterValue(-1,r) # creating a lambda to store the coor of the button
                                   ).grid(row=11, column=i, sticky="nsew")

GameWindow.mainloop()
