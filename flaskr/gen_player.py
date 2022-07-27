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
