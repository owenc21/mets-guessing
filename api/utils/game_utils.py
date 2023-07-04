import os

from res import player


def check_guess(guess):
    """
    Function to ensure a guessed player exits
    """
    if guess in player.players.keys():
        return True
    else:
        return False


def correct_check(guess):
    """
    Function to check if guess is correct player
    """
    if guess == os.environ.get("PLAYER"):
        return True
    else:
        return False


def gen_guess_response(guess):
    """
    Generates a dictionary, based on the player
    that was guessed, containing information on 
    how close the guess was from the correct
    player's attributes

    @param guess    The guessed player
    @returns    Dictionary containing states for 
    closeness to correct player's attributes
    0 = incorrect, 1 = close, 2 = correct
    """

    # Get dictionary of player attributes for guessed player
    player_guess = player.players.get(guess)
    if player_guess is None:
        raise Exception("Player not in player dictionary")
    
    # Get dictionary of correct player
    player_true = player.players.get(str(os.environ.get("PLAYER")))

    response = {}

    # In unoptimized fashion, go through each attribute and
    # determine relative closeness to correct guess

    """
    Age
    if within 2 years, partial
    """
    if player_true["age"] == player_guess["age"]:
        response["age"] = 2
    elif abs(player_true["age"]-player_guess["age"]) <= 2:
        response["age"] = 1
    else:
        response["age"] = 0

    """
    Bats
    only partial if batter is switch and guess is not
    """
    if player_true["bats"] == player_guess["bats"]:
        response["bats"] = 2
    elif player_true["bats"] == 2 and player_guess["bats"] != 2:
        response["bats"] = 1
    else:
        response["bats"] = 0
    
    """
    Throws
    never partial, only correct or incorrect
    """
    if player_true["throws"] == player_guess["throws"]:
        response["throws"] = 2
    else:
        response["throws"] = 0
    
    """
    Position
    logic gets difficult here
    partial if guess wrong but guess was outfield and player outfield,
    guess infield and player infield, or guess starter/reliever and player
    the opposite
    """
    if player_true["position"] == player_guess["position"]:
        response["position"] = 2
    elif player_true["subpos"] == player_guess["subpos"]:
        response["position"] = 1
    else:
        response["position"] = 0

    """
    Birth (nation)
    never partial, only correct or incorrect
    """
    if player_true["birth"] == player_guess["birth"]:
        response["birth"] = 2
    else:
        response["birth"] = 0
    
    """
    Height
    partial if within 2 inches
    """
    if player_true["height"] == player_guess["height"]:
        response["height"] = 2
    elif abs(player_true["height"]-player_guess["height"]) <= 2:
        response["height"] = 1
    else:
        response["height"] = 0

    """
    Weight
    partial if within 7 pounds
    """
    if player_true["weight"] == player_guess["weight"]:
        response["weight"] = 2
    elif abs(player_true["weight"]-player_guess["weight"]) <= 7:
        response["weight"] = 1
    else:
        response["weight"] = 0
    
    return response