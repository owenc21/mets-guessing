import csv
import random
from flask import g

PATH = r"C:\Users\owenc\Documents\Programming\repos\mets-guessing\data\metsplayers.csv"

#generate random number to decide which player is chosen
def gen_rand():
    return random.randint(1,44)

#add random player to g with attribute 'player'
def set_player():
    return_player = []
    player_id = gen_rand()

    with open(PATH, 'r') as infile:
        reader = csv.reader(infile, delimiter=",")
        for i in range(player_id):
            next(reader)
        return_player = next(reader)


    g.player = return_player


def gen_return_response(guess):
    guess_atrs = [] #an array that holds the attributes of the player that was guesses
    atrs_adjust = [] #an array that holds values to describe how close the guess was/how much adjustment is needed

    if guess.upper() == g.player[0].upper():
        pass #write logic if the guess is correct
    else:
        with open(PATH, 'r') as infile:
            reader = csv.reader(infile, delimiter=",")
            next(reader)
            for i in range(43):
                if reader[0].upper() == guess.upper():
                    guess_atrs = reader
                else:
                    pass
    
    

    return_comb = [guess_atrs, atrs_adjust] #an array that will hold two arrays: the values of the guessed player and what to do with the web elements
    return return_comb        
            
#1 = correct (green), 2 = close (orange), 3 = wrong (red)
def adjust(guess):
    name_adjust = 3
    adjust_attrs = []
    adjust_attrs.append(name_adjust)
    #birthplace is either correct or not
    if guess[1] == g.player[1]:
        adjust_attrs.append(1)
    else:
        adjust_attrs.append(3)
    #position
    if guess[2] == g.player[2]:
        adjust_attrs.append(1)
    elif guess[2] == 'RP' or guess[2] == 'SP':
        if g.player[2]
