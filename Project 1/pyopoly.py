"""
File:    pyopoly.py
Author:  Divij Raj Namdev
Date:    10/29/20
Section: 44
E-mail:  dnamdev1@umbc.edu
Description: This program runs a game that is similar to monopoly called Pyopoly.
"""
from sys import argv
from random import randint, seed
from board_methods import load_map, display_board

# possibly a lot more code here.
# this code can be anywhere from right under the imports to right # above if __name__ == '__main__':
if len(argv) >= 2:
    seed(argv[1])

STARTING_MONEY = 1500
PASS_GO_MONEY = 200


def play_game(STARTING_MONEY, pass_go_money, board_file):
    board = board_file
    the_board = []  # list that stores the values of 'Abbrev' in board file which is used to  build the board
    for line in board:  # runs through the entire  dictionary
        line['Owner'] = 'Bank'  # adds owner as bank as default to the entire list of the dictionary
        line['Building'] = 'No'
        line["Owned"] = False  # False means that no player owns that location
        if line['Abbrev']:  # triggers only when the index of a dictionary contains the key 'Abbrev'
            the_board.append((str(line['Abbrev'] + '   ') * 5)[0:5] + '\n' + (str(" ") * 5)[0:5])
            # ^------ adds the value tied to the key,'Abbrev', to the list

    player_one = {"name": input('First player, what is your name?: '),
                  "symbol": input('First player, what symbol do you want your character to use?: '),
                  'money': STARTING_MONEY,
                  'position': 0,
                  'Properties': [],
                  "Counter": 1}
    # ^-- holds the 1st player's name, symbol, position, properties, # of times looped around the board, and money

    while player_one['symbol'].islower() or len(
            player_one['symbol']) != 1:  # keeps asking if the symbol is not 1 letter or capital
        player_one['symbol'] = input('First player, what symbol do you what your character to use?: ')

    player_two = {"name": input('Second player, what is your name?: '),
                  "symbol": input('Second Player, what symbol do you want your character to use?: '),
                  'money': STARTING_MONEY,
                  "position": 0,
                  "Properties": [],
                  "Counter": 1}
    # ^-- holds the 2nd player's name, symbol, position, properties, # of times looped around the board, and money

    while player_two['symbol'].islower() or len(
            player_two['symbol']) != 1:  # keeps asking if the symbol is not 1 letter or capital
        player_one['symbol'] = input('First player, what symbol do you what your character to use?: ')

    all_players = [player_one, player_two]  # combines the dictionary of both players into to one list to access them
    # when both of them are necessary

    format_display(all_players, the_board)  # calls the format_display function
    take_turn(all_players, board)  # calls the take_turn function

    if player_one["money"] <= 0:  # ends the game if player 1 loses
        return print(player_one["name"], "has lost the game due to running out of money")
    elif player_two["money"] <= 0:  # ends the game if player 2 loses
        return print(player_two["name"], "has lost the game due to running out of money")


def take_turn(players, board):
    the_board = board
    go_money = PASS_GO_MONEY
    money_from_go(players, board, go_money)  # when a person passes go it would add 200 to their total money

    for i in the_board:
        if int(i['Position']) == players[0]['position']:  # gets the current player's location
            player_current_location = i
            print(players[0]['name'], "has landed on", player_current_location['Place'])

    if player_current_location["Owner"] == players[1]["name"] and player_current_location["Owned"] == True:
        # ^--- checks to see if location is owned and if the owner is the other player
        print("You have landed on", player_current_location["Owner"] + "'s property, you must pay the rent")
        players[0]["money"] = players[0]["money"] - int(player_current_location["Rent"])
        # ^--- subtracts the rent from the current player's money
        players[1]["money"] = players[1]["money"] + int(player_current_location["Rent"])
        # ^--- adds the rent to the owner's money pool
        print("You have payed", player_current_location["Rent"], "to", player_current_location["Owner"])

    print('\n', "1) Buy Property ", '\n', "2) Get Property Info", '\n', "3) Get Player Info", '\n',
          "4) Build a Building (not finished)", '\n', "5) End turn", '\n')

    counter = True
    while counter:
        choice = int(input("what do you want to do "))
        if choice == 1:
            'buy property'
            buy_property(players, player_current_location)

        elif choice == 2:  # gets the property information
            "Get Property info"
            property_info(the_board)

        elif choice == 3:  # gets each players information: money, symbol, name, and properties
            "Get Player info"
            players_info(players)

        elif choice == 4:
            "Build a Building"

        elif choice == 5:  # Ends current player's turn and switches to the other player's
            counter = False
            switch_turn(players, the_board)  # changes the turns of the players

        print('\n', "1) Buy Property ", '\n', "2) Get Property Info", '\n', "3) Get Player Info", '\n',
              "4) Build a Building", '\n', "5) End turn", '\n')


def buy_property(players, player_current_location):  # executes the buy property option

    if int(player_current_location["Price"]) < 0:  # checks to see if the place is purchasable
        print(player_current_location, "can not be bought")
    elif player_current_location["Owned"]:  # tells you that the property is already owned and who the owner is
        print(player_current_location['Owner'], "is the current property owner, you can not buy it")
    else:
        want_to_buy = input('The property is unowned, do you want to buy it?: ')
        if player_current_location['Owned'] != True and int(players[0]['money']) >= int(
                player_current_location["Price"]):  # checks to see if you have enough money and it's not owned

            if want_to_buy == 'yes':  # if typed yes it will buy the property
                players[0]['money'] = int(players[0]["money"]) - int(player_current_location["Price"])
                player_current_location["Owned"] = True
                player_current_location['Owner'] = players[0]['name']
                players[0]['Properties'].append(player_current_location)  # adds it to the Properties list in the
                # Player's dictionary
                print("You have bought", player_current_location["Place"])
            else:
                print("You have decided not to buy", player_current_location)  # runs when you type in no
        elif player_current_location['Owned'] != True and int(players[0]['money']) < int(
                player_current_location[
                    "Price"]):  # this will run if you don't have enough money to buy and its not owned
            print('You don\'t have enough money')


def property_info(board):  # this shows the information on a property
    the_board = board
    prop_info = input('For which property do you want to get the information?: ')
    for info in the_board:  # runs through the entire board_file dictionary
        if prop_info == info['Abbrev']:  # checks to see user entered in the Abbreviation of the property and prints it
            print('\n' + 'Place:', info['Place'] + '\n' + "Price:", info["Price"] + '\n' + "Owner:",
                  info["Owner"]
                  + '\n' + "Building:", info['Building'] + '\n' + "Rent:",
                  info['Rent'] + ', ' + info['BuildingRent'], "(with Building)")


def players_info(players):  # gets information about the players
    print('The players:', '\n', players[0]['name'], '\n', players[1]['name'])
    choose_player = input('Which player do you wish to know?: ')  # asking what player you want to see
    if choose_player == players[0]['name']:  # shows the 1st player's information
        print('Player Name:', players[0]['name'] + '\n' + "Player's Symbol:", players[0]['symbol'] + '\n' +
              'Current money:', players[0]['money'])
        if len(players[0]['Properties']) == 0:  # checks to see if doesn't own any property
            print('Properties owned:', '\n', 'No properties yet')  # prints the person does not have properties
        else:  # if the player owns properties it will print the properties they own
            print('Properties owned:')
        for i in players[0]['Properties']:
            for j in i:  # runs through a list of dictionaries that have all the property information
                if j == "Place":  # checks to see if j is the key Place
                    print(i[j])  # Ex: dictionary[Place]
    elif choose_player == players[1]['name']:  # shows the 2nd player's information
        print('Player Name:', players[1]['name'] + '\n' + "Player's Symbol:", players[1]['symbol'] + '\n' +
              'Current money:', players[1]['money'])
        if len(players[1]['Properties']) == 0:  # checks to see if doesn't own any property
            print('Properties owned:', '\n', 'No properties yet')  # prints the person does not have properties
        else:  # if the player owns properties it will print the properties they own
            print('Properties owned:')
            for a in players[1]['Properties']:
                for b in a:  # runs through a list of dictionaries that have all the property information
                    if b == "Place":  # checks to see if b is the key Place
                        print(a[b])  # Ex: dictionary[Place]
    else:
        print('That player is not in the game.')


def switch_turn(players, board):  # function changes the players turn
    the_board = []  # has to recreate the board to show the updated positions after the switch
    for i in board:
        if i['Abbrev']:
            the_board.append((str(i['Abbrev'] + '   ') * 5)[0:5] + '\n' + (str(" ") * 5)[0:5])
    temp = players[0]  # temp variable
    players[0] = players[1]
    players[1] = temp  # switches the position in the list
    return format_display(players, the_board), take_turn(players, board)
    # ^---returns two functions to continue the game


def money_from_go(players, board, go_money):  # gives money to the player for passing go
    if players[0]["position"] / len(board) >= players[0]["Counter"]:
        players[0]["money"] += go_money
        players[0]["Counter"] += 1


def format_display(players, board):  # this will format the board and display the positions of the players
    the_board = board
    player_current = players[0]  # current player
    player_background = players[1]  # back ground player
    space = randint(1, 6) + randint(1, 6)
    flag = True
    while flag:
        player_current["position"] += space
        player_current["position"] %= len(the_board)
        copy_board = list(the_board)
        copy_board[player_current["position"]] = copy_board[player_current["position"]][0:6] + player_current["symbol"]
        copy_board[player_background["position"]] = copy_board[player_background["position"]][0:6] + player_background[
            "symbol"]
        display_board(copy_board)
        flag = False
    print(player_current['name'], "has rolled a", space)


if __name__ == '__main__':
    play_game(STARTING_MONEY, PASS_GO_MONEY, load_map("proj1_board1.csv"))
