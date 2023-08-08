#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 09:01:20 2022

Main:
    opening statement
    initializes variables,tableau, and foundation and displays initial board
    gets option from user and loops until valid
    while option is not quit:
        saves current board by appending tableau foundation and option
        moves desired card and sets move to true if valid move
        error prompt if move invalid
        if u is input resaves tableau foundation 
        if r is input starts a new game
        prints menu if h is input
        starts new game if game is won
        displays and reprompts for option
    closing statement

"""

#DO NOT DELETE THESE LINES
import cards, random,copy
random.seed(100) #random number generator will always generate 
                 #the same 'random' number (needed to replicate tests)

MENU = '''     
Input options:
    MTT s d: Move card from Tableau pile s to Tableau pile d.
    MTF s d: Move card from Tableau pile s to Foundation d.
    MFT s d: Move card from Foundation s to Tableau pile d.
    U: Undo the last valid move.
    R: Restart the game (after shuffling)
    H: Display this menu of choices
    Q: Quit the game       
'''
                
def initialize():
    '''
    creates a deck and shuffles
    initialzies foundation and tableau and deals cards to tableau
    returns tableau and foundation as tuple
    '''
    my_deck = cards.Deck()#creates deck
    my_deck.shuffle()#shuffles deck
    foundation = [[],[],[],[]]#initialzies foundation
    tableau = [[],[],[],[],[],[],[],[]]#initializes tableau
    for listt in tableau:#goes through each list
        if tableau.index(listt) %2 == 0:#even index
            for i in range(7):
                listt.append(my_deck.deal())#deals 7 cards
        elif tableau.index(listt) %2 == 1:#odd index
            for i in range(6):
                listt.append(my_deck.deal())#deals 6 cards
    return (tableau,foundation)#returns tuple

def display(tableau, foundation):
    '''Each row of the display will have
       tableau - foundation - tableau
       Initially, even indexed tableaus have 7 cards; odds 6.
       The challenge is the get the left vertical bars
       to line up no matter the lengths of the even indexed piles.'''
    
    # To get the left bars to line up we need to
    # find the length of the longest even-indexed tableau list,
    #     i.e. those in the first, leftmost column
    # The "4*" accounts for a card plus 1 space having a width of 4
    max_tab = 4*max([len(lst) for i,lst in enumerate(tableau) if i%2==0])
    # display header
    print("{1:>{0}s} | {2} | {3}".format(max_tab+2,"Tableau","Foundation","Tableau"))
    # display tableau | foundation | tableau
    for i in range(4):
        left_lst = tableau[2*i] # even index
        right_lst = tableau[2*i + 1] # odd index
        # first build a string so we can format the even-index pile
        s = ''
        s += "{}: ".format(2*i)  # index
        for c in left_lst:  # cards in even-indexed pile
            s += "{} ".format(c)
        # display the even-indexed cards; the "+3" is for the index, colon and space
        # the "{1:<{0}s}" format allows us to incorporate the max_tab as the width
        # so the first vertical-bar lines up
        print("{1:<{0}s}".format(max_tab+3,s),end='')
        # next print the foundation
        # get foundation value or space if empty
        found = str(foundation[i][-1]) if foundation[i] else ' '
        print("|{:^12s}|".format(found),end="")
        # print the odd-indexed pile
        print("{:d}: ".format(2*i+1),end="") 
        for c in right_lst:
            print("{} ".format(c),end="") 
        print()  # end of line
    print()
    print("-"*80)
          
def valid_tableau_to_tableau(tableau,s,d):
    '''
    checks if move is valid
    returns true if valid, false if invalid
    '''
    if tableau[d] == []:#if empty tableau
        return True#returns true
    try:
        #tries to set source and destination cards
        source = tableau[s][-1]
        destination = tableau[d][-1]
    except:#except if index out of range
        return False#returns false
    if destination.rank()-1 == source.rank():#if dest card is one above source card
        return True#returns true
    else:#if card is not one below
        return False#return false
def move_tableau_to_tableau(tableau,s,d):
    '''
    checks if move is valid
    if valid, removes source card and adds to destination
    returns true if valid and false if not
    '''
    if valid_tableau_to_tableau(tableau, s, d) == True:#if valid move
        source = tableau[s].pop()#removes source card
        tableau[d].append(source)#adds it to dest tableau
        return True#returns true
    else:#if not valid
        return False#returns false
    

def valid_foundation_to_tableau(tableau,foundation,s,d):
    '''
    checks if move is valid
    returns true if valid, false if invalid
    '''
    if tableau[d] == []:#if empty 
        return True#return true
    try:
        #tries to set source and destination cards
        source = foundation[s][-1]
        destination = tableau[d][-1]
    except:#except if index out of range
        return False#returns false
    if destination.rank()-1 == source.rank():#if dest rank one greater than source
        return True#return true
    else:#if card is not one below
        return False#return false

def move_foundation_to_tableau(tableau,foundation,s,d):
    '''
    checks if move is valid
    if valid, removes source card and adds to destination
    returns true if valid and false if not
    '''
    if valid_foundation_to_tableau(tableau, foundation, s, d) == True:#if valid move
        source = foundation[s].pop()#removes source card
        tableau[d].append(source)#adds it to dest tableau
        return True#returns true
    else:#if not valid
        return False#returns false

def valid_tableau_to_foundation(tableau,foundation,s,d):
    '''
    checks if move is valid
    returns true if valid, false if invalid
    '''
    try:
        if tableau[s][-1].rank()==1 and foundation[d] == []:#if ace and empty foundation
            return True#returns true
        #tries to set source and destination
        source = tableau[s][-1]
        destination = foundation[d][-1]
    except:#except if index out of range
        return False#returns false
    if destination.rank()+1 == source.rank() and destination.suit()==source.suit():#if dest is one less than source
        return True#returns true
    else:#if card is not one above
        return False#returns false
    
def move_tableau_to_foundation(tableau, foundation, s,d):
    '''
    checks if move is valid
    if valid, removes source card and adds to destination
    returns true if valid and false if not
    '''
    if valid_tableau_to_foundation(tableau, foundation, s, d) == True:#if valid move
        source = tableau[s].pop()#removes source card
        foundation[d].append(source)#adds to foundation
        return True#returns true
    else:#if invalid move
        return False#returns false

def check_for_win(foundation):
    '''
    checks if user wins game
    returns true if won
    false if not
    '''
    for listt in foundation:#goes through each line in foundation
        if len(listt)==13:#if foundation is full
            booll = True#sets variable to true
        else:#if any foundation is not full
            return False#return false
    return booll#returns booll variable

def get_option():
    '''
    prompts for option
    creates list from input
    checks if input is valid, if not prints error returns none
    if valid return option
    '''
    option = input("\nInput an option (MTT,MTF,MFT,U,R,H,Q): " )#prompts for option
    opt_list = option.split()#creates list
    valid_moves,valid_opts = ['MTT','MTF','MFT'],['U','R','H','Q']#inits valid ans
    if opt_list[0].upper() in valid_opts:#checks for valid input
        return [opt_list[0].upper()]#returns input
    if not opt_list[0].upper() in valid_moves:#if not valid
        print("Error in option:")#error mess
        return None#returns none
    for i in range(1,3):
        opt_list[i]=int(opt_list[i])#sets values to ints
    #checks to see if valid ranges of numbers input, error and returns none if not valid
    if opt_list[0].upper() == 'MTT':
        if not 0<=opt_list[1]<=7:
            print("Error in Source.")
            return None
        if not 0<=opt_list[2]<=7:
            print("Error in Destination")
            return None
    if opt_list[0].upper() == 'MTF':
        if not 0<=opt_list[1]<=7:
            print("Error in Source.")
            return None
        if not 0<=opt_list[2]<=3:
            print("Error in Destination")
            return None
    if opt_list[0].upper() == 'MFT':
        if not 0<=opt_list[1]<=3:
            print("Error in Source.")
            return None
        if not 0<=opt_list[2]<=7:
            print("Error in Destination")
            return None
    return opt_list#returns option as list if valid

            
    

def main():  
    print("\nWelcome to Streets and Alleys Solitaire.\n")#opening statement
    undo_list = []#inits undo list
    tableau,foundation = initialize()#sets tableau and foundation using function
    display(tableau, foundation)#displays board
    print(MENU)#prints menu of opts
    option = get_option()#gets option
    while option == None:#loops until valid
        option=get_option()#reprompts
    win = False#inits variable
    while option[0].lower()!='q':#loops until quit
        undo_list.append((copy.deepcopy(tableau),copy.deepcopy(foundation),option))#saves each move
        if option[0].upper() == 'MTT':#if mtt input moves cards
            move =move_tableau_to_tableau(tableau, option[1], option[2])#sets move to true if valid, false if not
        elif option[0].upper()=='MTF':#if mtf input moves cards
            move = move_tableau_to_foundation(tableau, foundation, option[1], option[2])#sets move to true if valid, false if not
        elif option[0].upper()=='MFT':#if mtf input moves cards
            move = move_foundation_to_tableau(tableau, foundation, option[1], option[2])#sets move to true if valid, false if not
        if move == False:#if invalid move
            print("Error in move: {} , {} , {}".format(option[0].upper(),option[1],option[2]))#error prompt
            undo_list.pop()#unsaves move
        if option[0].upper() == 'U':#if undo
            undo_list.pop()#removes current board
            if undo_list != []:#if not empty list
                temp_tup = undo_list.pop()#sets variable to last move
                print("Undo:",temp_tup[2][0].upper(),temp_tup[2][1],temp_tup[2][2])#displays move to undo
                tableau,foundation = temp_tup[0],temp_tup[1]#saves tableau and foundation to old values
            else:#if list empty
                print("No moves to undo.")#prints error mess
                move = False#sets move to invalid
        if option[0].upper()== 'R':#if restart
            print("\n- - - - New Game. - - - -\n")#new game message
            tableau,foundation = initialize()#resets variables
            display(tableau, foundation)#displays
            print(MENU)#prints menu
            option = get_option()#prompts for option
            win = True#sets win to true
        if option[0].upper()=='H':#if h
            print(MENU)#shows menu
        if check_for_win(foundation):#if won
            print("You won!\n")#win messsage
            display(tableau,foundation)#displays final board
            print("\n- - - - New Game. - - - -\n")#new game prompt
            tableau,foundation = initialize()#resets board
            display(tableau, foundation)#displays
            print(MENU)#prints menu
            option = get_option()#prompts for option
            win = True#sets win to true
        if win == False and move ==True:#if not won and valid move
            display(tableau,foundation)#displays board
        if win == False or move == False:#if not won or invalid move
            option=get_option()#prompts for option
            while option == None:#error checks
                option=get_option()#reprompts
        
        win = False#sets win to false
    print("Thank you for playing.")#closing statement
    
        
        
    
    
    
if __name__ == '__main__':
     main()