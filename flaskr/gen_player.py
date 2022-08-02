import csv
import random
import os
from . import config
import time

direc = os.path.dirname(__file__)
PATH = os.path.join(direc, '..', 'data', 'metsplayers.csv')

#generate random number to decide which player is chosen
def gen_rand():
    return random.randint(1,44)

#add random player to g with attribute 'player'
def set_player(seconds):
    while(True):
        return_player = []
        player_id = gen_rand()

        with open(PATH, 'r') as infile:
            reader = csv.reader(infile, delimiter=",")
            for i in range(player_id):
                next(reader)
            return_player = next(reader)


        config.act_player = return_player
        print(config.act_player)
        time.sleep(seconds)



def gen_return_response(guess):
    is_met = False #change to true so long as the guess is an actual mets player
    guess_atrs = [] #an array that holds the attributes of the player that was guesses
    atrs_adjust = [] #an array that holds values to describe how close the guess was/how much adjustment is needed

    with open(PATH, 'r') as infile:
        reader = csv.reader(infile, delimiter=",")
        reader_list = list(reader) #create array of all the mets players
        for i in range(43):
            if reader_list[i][0].upper() == guess.upper(): #check if the guess is correct
                guess_atrs = reader_list[i]
                is_met = True
                break
            else:
                pass

    #make sure the guess was an actual mets player
    if not is_met:
        return False
    else:
        pass

    if guess.upper() == config.act_player[0].upper():
        atrs_adjust = ['tdCorrect','tdCorrect','tdCorrect','tdCorrect','tdCorrect','tdCorrect','tdCorrect','tdCorrect']
        atrs_adjust.append(True)
        return [guess_atrs, atrs_adjust]
    else:
        atrs_adjust = adjust(guess_atrs)
        atrs_adjust.append(False)
        return [guess_atrs, atrs_adjust]
    
           
            
#'tdCorrect' = correct (green), 'tdPartial' = close (orange), 'tdWrong' = wrong (red)
def adjust(guess):
    name_adjust = 'tdWrong'
    adjust_attrs = []
    adjust_attrs.append(name_adjust)
    #birthplace is either correct or not
    if guess[1] == config.act_player[1]:
        adjust_attrs.append('tdCorrect')
    else:
        adjust_attrs.append('tdWrong')
    #position
    if guess[2] == config.act_player[2]:
        adjust_attrs.append('tdCorrect')
    elif guess[2] == 'RP' or guess[2] == 'SP':
        if config.act_player[2] == 'SP' or config.act_player[2] == 'RP':
            adjust_attrs.append('tdPartial')
        else:
            adjust_attrs.append('tdWrong')
    elif guess[2] == '1B' or guess[2] == '2B' or guess[2] == 'SS' or guess[2] == '3B':
        if config.act_player[2] == '1B' or config.act_player[2] == '2B' or config.act_player[2] == 'SS' or config.act_player[2] == '3B':
            adjust_attrs.append('tdPartial')
        else:
            adjust_attrs.append('tdWrong')
    elif guess[2] == 'LF' or guess[2] == 'CF' or guess[2] == 'RF':
        if config.act_player[2] == 'LF' or config.act_player[2] == 'CF' or config.act_player[2] == 'RF':
            adjust_attrs.append('tdPartial')
        else:
            adjust_attrs.append('tdWrong')
    else:
        if config.act_player[2] == 'C':
            adjust_attrs.append('tdCorrect')
        else:
            adjust_attrs.append('tdWrong')
    #age
    if guess[3] == config.act_player[3]:
        adjust_attrs.append('tdCorrect')
    elif (int(guess[3]) - int(config.act_player[3])) >= -2 and (int(guess[3]) - int(config.act_player[3])) <= 2:
        adjust_attrs.append('tdPartial')
    else:
        adjust_attrs.append('tdWrong')
    #bat
    if guess[4] == config.act_player[4]:
        adjust_attrs.append('tdCorrect')
    elif guess[4] == 'S' or config.act_player[4] == 'S':
        adjust_attrs.append('tdPartial')
    else:
        adjust_attrs.append('tdWrong')
    #throws
    if guess[5] == config.act_player[5]:
        adjust_attrs.append('tdCorrect')
    else:
        adjust_attrs.append('tdWrong')
    #height
    guess_height_list = guess[6][:4].split("'")
    g_player_height_list = config.act_player[6][:4].split("'")
    guess_height = int(guess_height_list[0])*12 + int(guess_height_list[1])
    player_height = int(g_player_height_list[0])*12 + int(g_player_height_list[1])
    if guess[6] == config.act_player[6]:
        adjust_attrs.append('tdCorrect')
    elif (guess_height - player_height) <= 5 and (guess_height - player_height) >= -5:
        adjust_attrs.append('tdPartial')
    else:
        adjust_attrs.append('tdWrong')
    #weight
    guess_weight = int(guess[7])
    g_player_weight = int(config.act_player[7])
    if guess_weight == g_player_weight:
        adjust_attrs.append('tdCorrect')
    elif (guess_weight - g_player_weight) >= -20 and (guess_weight - g_player_weight) <= 20:
        adjust_attrs.append('tdPartial')
    else:
        adjust_attrs.append('tdWrong')
    
    return adjust_attrs