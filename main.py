import random
import os



Game = {  #this will hold all Game-related properties and attributes

    "deck": [],
    "played_cards": [],
    "players": [],
    "turn_order": [],
    "turn_index": 0,
    "recent_card": "",
    "plus_stack": 0

}


def create_deck():
    icons = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "block", "reverse", "+2"]
    colors = ["red", "blue", "green", "yellow"]

    Game["deck"] = []

    for color in colors:
        for icon in icons:
            Game["deck"].append([color, icon])

    for i in range(4):
        Game["deck"].append(["special", "+4"])
        Game["deck"].append(["special", "change color"])

    random.shuffle(Game["deck"])


def add_players():

    while True:
        print("The game only supports a max of 6 players.")

        for i in range(6):
            name = input("Please enter the name of the player (leave blank to end): ")
            if not name:
                break

            name = {"name": name, "plus": False, "blocked": False, "inventory": []}
            Game["players"].append(name)


        if len(Game["players"]) == 1 or len(Game["players"]) == 0:
            clear_screen()
            print("\nThe game requires at least 2 players at minimum.")
            Game["players"] = []
            continue

        else:
            break


def refresh_game_deck():
    if len(Game["deck"]) == 0:
        Game["deck"].extend(Game["played_cards"])  #put the played cards back into game deck
        random.shuffle(Game["deck"])  # then shuffle them
        Game["played_cards"] = []  # clear the played cards pile
        print("The deck has been refreshed")


def draw_card(index, count):

    self = Game["turn_order"][index]

    for i in range(count):

        refresh_game_deck()
        self["inventory"].append(Game["deck"].pop(0))








def play_game():

    create_deck()
    add_players()
    Game["turn_order"] = Game["players"]

    Game["recent_card"] = Game["deck"].pop(0)  # add first card to recent
    Game["played_cards"].append(Game["recent_card"])  # add recent card to played cards

    # to ensure that no first card is "special"
    first_card_verify()


    for i in Game["turn_order"]:
        index = Game["turn_order"].index(i)
        draw_card(index, 7)

    while True:

        Game["turn_index"] = 0

        while Game["turn_index"] < len(Game["turn_order"]):

            take_turn(Game["turn_index"])
            check_win_condition(Game["turn_index"])

            if len(Game["turn_order"]) == 1:
                print(f"{Game['turn_order'][0]['name']} lost the game.")

                exit(0)


            Game["turn_index"] += 1


def first_card_verify():
    while Game["recent_card"][0] == "special":
        Game["deck"].append(Game["played_cards"].pop(0))  # remove the played card

        Game["recent_card"] = Game["deck"].pop(0)  # play a new one
        Game["played_cards"].append(Game["recent_card"])


def show_deck(turn_index):

    self = Game["turn_order"][turn_index]

    print(f"Your cards: {self['inventory']}")



def take_turn(turn_index):
    while True:
        try:

            clear_screen()

            self = Game["turn_order"][turn_index]

            if self["blocked"]:
                self["blocked"] = False
                break

            if self["plus"]:
                plus_take_turn(turn_index)
                break

            print(f"There are {len(Game['deck'])} cards left in the game deck.")

            turn_list = []

            for i in Game["turn_order"]:
                turn_list.append(i["name"])

            print(f"The current turn order: {turn_list}")

            print(f"The last played card is: ({Game['recent_card'][0]}, {Game['recent_card'][1]})\n")
            print(f"{self['name']}'s turn")

            show_deck(turn_index)

            print("1. Play a card")
            print("2. Draw a card")
            choice = int(input("Input your choice: "))
            print("")

            if choice < 1 or choice > 2 or not choice:
                clear_screen()
                print("Invalid input. Please try again\n")
                continue
            if choice == 1:
                play_card(turn_index)
                break
            if choice == 2:
                refresh_game_deck()
                draw_card(turn_index, 1)
                break


        except ValueError:
            clear_screen()
            print("\nInput a valid choice.")
            continue


def play_card(turn_index):
    try:

        self = Game["turn_order"][turn_index]

        index = int(input("input the index of the card: "))
        print("")


        index -= 1

        if index < 0 or index > len(self["inventory"]):
            clear_screen()
            print("Input a valid index!")
            take_turn(turn_index)
            return


        color = self["inventory"][index][0]
        icon = self["inventory"][index][1]

        if color == Game["recent_card"][0] or icon == Game["recent_card"][1] or color == "special":

            # this runs if cards are valid

            # actually playing the card (adding to played deck)
            removed_item = self["inventory"].pop(index)
            Game["recent_card"] = removed_item
            Game["played_cards"].append(removed_item)

            # factoring in special cards i.e. color change

            if icon == "reverse":
                reverse(turn_index)

            if icon == "change color":
                change_color()

            if icon == "block":
                block_next_player(turn_index)

            if icon == "+2":
                plus_two_to_next(turn_index)

            if icon == "+4":
                plus_four_to_next(turn_index)

        else:
            clear_screen()
            print("\n\nPlease use a card that matches the recent card's icon or color.")
            take_turn(turn_index)

    except ValueError:
        clear_screen()
        print("Please input a valid index")
        take_turn(turn_index)


def reverse(turn_index):

    self = Game["turn_order"][turn_index]
    Game["turn_order"].reverse()
    Game["turn_index"] = Game["turn_order"].index(self)


def block_next_player(turn_index):

    unfortunate_victim = turn_index + 1

    if unfortunate_victim > len(Game["turn_order"])-1:
        unfortunate_victim = 0

    Game["turn_order"][unfortunate_victim]["blocked"] = True


def change_color():
    while True:
        try:
            print("1. Red")
            print("2. Blue")
            print("3. Yellow")
            print("4. Green")

            color = int(input("Input the new color: "))

            if color > 4 or color < 0 or not color:
                clear_screen()
                print("Invalid input. Please try again.")
                continue

            if color == 1:
                Game["recent_card"][0] = "red"
                break
            if color == 2:
                Game["recent_card"][0] = "blue"
                break
            if color == 3:
                Game["recent_card"][0] = "yellow"
                break
            if color == 4:
                Game["recent_card"][0] = "green"
                break

            if color > 4 or color < 1:
                clear_screen()
                print("Use a valid input")
                continue

        except ValueError:
            clear_screen()
            print("Please use a positive number")


def plus_two_to_next(turn_index):

    unfortunate_victim = turn_index + 1

    if unfortunate_victim > len(Game["turn_order"]) - 1:
        unfortunate_victim = 0

    Game["turn_order"][unfortunate_victim]["plus"] = True
    Game["plus_stack"] += 2



def plus_four_to_next(turn_index):
    unfortunate_victim = turn_index + 1

    if unfortunate_victim > len(Game["turn_order"]) - 1:
        unfortunate_victim = 0

    Game["turn_order"][unfortunate_victim]["plus"] = True
    Game["plus_stack"] += 4

    change_color()




def plus_take_turn(turn_index):
    while True:
        try:

            self = Game["turn_order"][turn_index]


            print(f"There are {len(Game['deck'])} cards left in the game deck.")

            turn_list = []

            for i in Game["turn_order"]:
                turn_list.append(i["name"])

            print(f"The current turn order: {turn_list}")

            print(f"The last played card is: ({Game['recent_card'][0]}, {Game['recent_card'][1]})\n")
            print(f"{self['name']}'s turn")

            print("You are currently plus'd. You may either only play a plus card or draw the pile")
            print(f"The current pile is {Game['plus_stack']} cards.")

            show_deck(turn_index)

            print("1. Play a card")
            print("2. Draw a card")
            choice = int(input("Input your choice: "))
            print("\n")

            if choice < 1 or choice > 2 or not choice:
                clear_screen()
                print("Invalid input. Please try again\n")
                continue
            if choice == 1:
                plus_play_card(turn_index)


                break
            if choice == 2:
                refresh_game_deck()
                draw_card(turn_index, Game["plus_stack"])
                Game["plus_stack"] = 0
                self["plus"] = False


                break


        except ValueError:
            clear_screen()
            print("\n\nInput a valid choice.")
            continue




def plus_play_card(turn_index):
    try:

        self = Game["turn_order"][turn_index]

        index = int(input("input the index of the card: "))
        print("")


        index -= 1

        if index < 0 or index > len(self["inventory"]):
            clear_screen()
            print("Input a valid index!")
            take_turn(turn_index)
            return


        icon = self["inventory"][index][1]

        if icon == "+2" or icon == "+4":

            # this runs if cards are valid

            # actually playing the card (adding to played deck)
            removed_item = self["inventory"].pop(index)
            Game["recent_card"] = removed_item
            Game["played_cards"].append(removed_item)

            # factoring in special cards i.e. color change

            if icon == "+2":
                plus_two_to_next(turn_index)
                self["plus"] = False

            if icon == "+4":
                plus_four_to_next(turn_index)
                self["plus"] = False

        else:
            clear_screen()
            print("\n\nPlease use a +2 card, or a +4 card.")
            take_turn(turn_index)

    except ValueError:
        clear_screen()
        print("Please input a valid index")
        take_turn(turn_index)


def check_win_condition(turn_index):

    self = Game["turn_order"][turn_index]

    if len(self["inventory"]) == 0:
        del Game["turn_order"][Game["turn_index"]]
        Game["turn_index"] -= 1


def menu():
    while True:

        print("Uno: The Card Game")
        print("-------------------------------")
        print("1. Play")
        print("2. How to Play")
        print("3. Exit\n")

        try:
            choice = int(input("Enter your choice: "))

            if choice < 0:
                clear_screen()
                print("Invalid input, please use a positive number\n")
                continue

            if choice > 3:
                clear_screen()
                print("Please input a number given in the choices\n")
                continue

            if choice == 1:
                play_game()
            if choice == 2:
                tutorial()


            if choice == 3:
                print("Thank you for Playing!")
                exit()

        except ValueError:
            clear_screen()
            print("\nPlease use a valid input\n")

            continue


def tutorial():
    print("------------------------")
    print("Tutorial")
    print("------------------------\n")

    print("In this game, the game begins with drawing an initial card.")
    print("Afterwards, every player takes their turn")
    print("They can either play a card, or draw from the pile")
    print("If they will play a card, the card must have the same icon or color as the recent card")

    print("\n\nFirst player to run out of cards, wins. Last player to run out of cards loses.")

    print("\n\nThat aside, there are special cards that have unique effects: \n")

    print("Block: When played, disables the next player's turn")
    print("Reverse: When played, reverses the turn order")
    print("Change color: You can force a color change by playing this")
    print("+2 or +4: Adds 2 cards, or 4 cards, to the next player's deck, respectively.\n\n")

    print("Special Mechanic: Plus cards\n")

    print("When someone plays a plus card, you can either choose to draw the cards or add to the 'stack'")
    print("For example, if a previous player plays a plus card, you can choose to play a plus card as well")
    print("Doing so effectively 'builds' a stack of plus cards, and the player that draws will end up drawing")
    print("an amount of cards equal to the stack you built.\n\n")


    print("How to use the program: \n")

    print("0. Follow the initial directions for setup")
    print("1. Use the numbers to input your choices (draw or play)")
    print("2. Cards are displayed in this format: [color, icon]")
    print("3. When selecting cards to play, cards are indexed starting from 1 (leftmost card) going to the right, adding 1 each time")
    print("That means that cards are arranged like this: [[card 1], [card 2], [card 3], etc.]")
    print("4.After taking your turn, pass it to the next person who is taking their turn\n\n")

    print("Other notes: \n")

    print("This is originally a card game, a recreation done as lab activity in CS :)")
    print("Some mechanics in the original game are modified to fit the program style")
    print("Due to the pass-and-play feature of the game, the 'uno call' mechanic has been removed")
    print("A played_cards deck is still implemented to enable card counting strategies\n\n")
    print("Enjoy the game!\n")

    return



def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


menu()
