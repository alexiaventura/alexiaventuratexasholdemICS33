# UI file for a Texas Hold 'Em game

import Project_Alexia_Ventura as Game
import tkinter as tk
import random


class THEGameUIPacker:
    """Creates the Texas Hold 'Em GUI class."""
    
    # The variable for anything directly placed onto the window
    master = 0

    def __init__(self):

        # Creates the window containing the game
        self.game_window()
        
        # Text box for the human player to choose the number of bots
        self.num_bots = tk.IntVar()

        # Label to tell the human player to choose the number of bots
        self.num_bots_label = tk.StringVar()

        # Label to denote the players' displayed money will be shown
        self.money_title = tk.StringVar()

        # Label to show how much money all players have
        self.money_values = tk.StringVar()

        # Keeps track of how many games have been started
        self.num_games = 1

        # Placeholder for the game's community cards
        self.game_community_cards = ''

        # Placeholder for showing the human player's ID and Round 1 hand
        self.your_player_label_1 = tk.StringVar()

        # Placeholder that displays who the bot player(s) is/are
        self.bot_players_label = tk.StringVar()

        # Placeholder for displaying the game's three community cards
        self.three_card_label = tk.StringVar()

        # Makes sure the human player's Round 1 hand isn't displayed more than once
        self.yourPlayerLabel = False

        # Placeholder for displaying which bot players in Round 1 didn't fold
        # (and what they bet, if at all)
        self.round_1_bots = tk.StringVar()

        # Placeholder for the human player's best 5-card hand in Round 2
        self.your_best_hand = ''

        # Placeholder for the game's Round 2 hands
        self.new_five_card_hands = ''

        # Placeholder for showing the human player's ID and Round 2 hand
        self.your_player_label_2 = tk.StringVar()

        # Makes sure the human player's Round 2 hand isn't displayed more than once
        self.yourPlayerLabel2 = False

        # Placeholder for displaying the game's two community cards
        self.two_card_label = tk.StringVar()

        # Placeholder for containing the players who don't fold in Rounds 1 and 2
        self.finishing_players = []

        # Keeps track of the game's players
        self.game_players = []

        # Keeps track of the players' money amounts from previous games
        self.previous_money = {}

        # Placeholder for displaying players' money amounts from previous games
        self.previous_money_label = tk.StringVar()

        # Placeholder for displaying the winner(s)' prize
        self.display_prize = tk.StringVar()

        # Placeholder for displaying the winner(s)
        self.display_winner = tk.StringVar()

        # Placeholder for whether the human player folded in Round 1 or not
        self.round1Continue = True

        # Placeholder for displaying which bot players in Round 2 didn't fold
        # (and what they bet)
        self.round_2_bots = tk.StringVar()

        # Creates an instance of a player
        self.num_bots_label_creation()

        # Placeholder for the human player's ID and hand
        self.your_player = ''

        # Placeholder for the bot players' ID and hand
        self.bot_players = ''

        # Placeholder for prize money
        self.winner_prize = 0

        # Placeholder for the text displaying the human player's Round 1 decision
        self.round_1_decision = tk.StringVar()

        # Placeholder for string with the human player's Round 1 cards
        self.your_cards_round_1 = ''

        # Placeholder for string with the human player's Round 2 cards
        self.your_cards_round_2 = ''

        # Placeholder for when only one player wins
        self.winner = ''

        # Placeholder for the string displaying the human player's two cards
        self.two_card_string = ''

        # Placeholder for if the human folded or not
        self.human_folded = False

        # Placeholder for text that asks the human player how much they want to bet
        self.your_bet_label = tk.StringVar()

        # Placeholder for the human player's bet
        self.your_bet = tk.IntVar()

        # Placeholder for the human player's money to be assigned to this variable name
        self.your_money = ''

        # Boolean value for whether the human player's bet is valid or not
        self.valid_bet = False

        # Placeholder for each player's hand if they were considered for the prize
        self.final_player_hand = tk.StringVar()

        # Placeholder for displaying that the final players' information will be shown
        self.final_players_announcement = tk.StringVar()

        # Placeholder to ask how and if the human player wants to play again
        self.play_again_question = tk.StringVar()

        # Stores the bot players' decisions in Round 1
        self.round_1_bot_decisions = {}

        # Stores the bot players' decisions in Round 2
        self.round_2_bot_decisions = {}

        self.master.mainloop()

    def game_window(self):
        """Creates a window containing the Texas Hold 'Em game."""
        self.master = tk.Tk()

        # Title of window
        self.master.title("Texas Hold 'Em")
        
        # Size of window
        self.master.geometry('900x700')
        
        # Background color of window
        self.master.configure(background='green')
        
        # Resizable condition
        self.master.resizable(None, None)

    def num_bots_label_creation(self):
        """Displays what the human player needs to see to choose a number of bot players."""
        self.num_bots_label.set("How many bot players do you want to play with?")
        tk.Label(self.master, textvariable=self.num_bots_label).pack()

        tk.Entry(self.master, textvariable=self.num_bots).pack()

        tk.Button(self.master, text="Submit Number of Bots", command=self.start_playing).pack()

        self.master.update()

    def start_playing(self):
        """Runs an entire Texas Hold 'Em game."""

        # Makes sure that the human player selected to play with at least 1 bot player
        # and did not choose a non-integer value nor an integer that's greater than 3
        assert type(self.num_bots.get()) == int
        assert 2 <= self.num_bots.get() <= 4

        # Creates the game's deck of cards
        game_deck = Game.creating_card_deck()

        # Creates all the players (the bot players and the human player) depending
        # on how many games might have been played previously with the same bot players
        if self.num_games > 1:
            money = {}
            for player_id in self.previous_money:
                money[player_id] = self.previous_money[player_id]
            self.game_players = Game.creating_players(self.num_bots.get() + 1, game_deck, money)
        else:
            self.game_players = Game.creating_players(self.num_bots.get() + 1, game_deck, 10)

        # Placeholder for the text displaying the players' money
        string_money = "All players and their money: "

        # Initializing values for making sure the players' money values are displayed neatly
        last_iteration = len(self.game_players)
        num_iterations = 0

        # Creates the string that will display the players' money values
        for player in self.game_players:
            string_money += f'Player {player.player_id}: ${player.money}'

            # Adds a newline character between different players' money amounts
            # (to make it look neater on the GUI)
            num_iterations += 1
            if num_iterations != last_iteration:
                string_money += ', '

        # Displays the players' money amounts
        self.money_values.set(string_money)
        tk.Label(self.master, textvariable=self.money_values).pack()

        # Assigns the human player their ID, hand of cards, and amount of money
        self.your_player = self.game_players[-1]
        self.your_money = self.your_player.money

        # Assigns each of the bot players their ID and hand of cards
        self.bot_players = self.game_players[:]
        self.bot_players.pop()

        # Creates bot player label
        bot_ids = []
        for player in self.bot_players:
            bot_ids.append(player.player_id)
        bot_id_string = 'Bot Player ID(s): ' + ', '.join(bot_ids)
        self.bot_players_label.set(bot_id_string)
        tk.Label(self.master, textvariable=self.bot_players_label).pack()

        # Placeholders for card hand strings
        three_card_string = ''

        if len(self.game_players) > 1:
            # Round 1 begins
            # Creating the game's community cards
            self.game_community_cards = Game.five_community_cards(game_deck)

            # Randomly uses three of the community cards for the first round
            max_num = len(self.game_community_cards) - 1

            three_community_cards = []

            for card in range(3):
                random_index = random.randint(0, max_num)
                community_card = self.game_community_cards[random_index]
                three_community_cards.append(community_card)
                self.game_community_cards.remove(community_card)
                max_num -= 1

            five_card_hands = []

            # Displaying first three community cards
            filtered_three_cards = []
            for card in three_community_cards:
                filtered_three_cards.append(card.suit_and_value)
                three_card_string = 'First Three Community Cards: ' + ', '.join(filtered_three_cards)

            self.three_card_label.set(three_card_string)
            tk.Label(self.master, textvariable=self.three_card_label).pack()

            # Displaying the human player's five-card hand
            for player in self.game_players:

                for card in three_community_cards:
                    player.hand.append(card)

                type_hand = Game.determine_hand(player.hand, player.player_id)
                rank_name = Game.display_rank(type_hand)

                if player.player_id == self.your_player.player_id:
                    filtered_your_cards = []
                    for card in player.hand:
                        filtered_your_cards.append(card.suit_and_value)
                        self.your_cards_round_1 = f"Your (Player {self.your_player.player_id}'s)"
                        self.your_cards_round_1 += f" 5-card hand ({rank_name}): "
                        self.your_cards_round_1 += ', '.join(filtered_your_cards)
                    five_card_hands.append(type_hand)
                    self.your_player_label_1.set(self.your_cards_round_1)
                    tk.Label(self.master, textvariable=self.your_player_label_1).pack()
                else:
                    five_card_hands.append(type_hand)
            
            continuing_players = []
            continuing_player_ids = []
            round_1_bots_string = ''
            # Bot players will make their decisions first
            for hand in five_card_hands:
                player_decision = Game.decision_criteria(hand)
                if player_decision != 'Fold':
                    for player in self.bot_players:
                        if hand[0] == player.player_id:
                            continuing_players.append(player)
                            continuing_player_ids.append(player.player_id)
            round_1_bots_string += 'These bot players chose to continue in Round 1: '
            round_1_bots_string += ', '.join(continuing_player_ids)
            round_1_bots_string += '. What would you like to do?'
            self.round_1_bots.set(round_1_bots_string)
            tk.Label(self.master, textvariable=self.round_1_bots).pack()
            
            # Displays label and buttons for the human player to make a decision in Round 1
            self.decision_buttons(1, continuing_players)

    def human_bets(self, round_number, continuing_players):
        """Adjusts the money amounts of all players who bet and allows these players to continue playing."""

        self.your_bet_label.set("How much do you want to bet?")

        tk.Label(self.master, textvariable=self.your_bet_label).pack()

        tk.Entry(self.master, textvariable=self.your_bet).pack()

        tk.Button(self.master, text="Submit Your Bet",
                  command=lambda: self.check_bet(round_number, self.your_bet.get(), continuing_players)).pack()

    def human_folds(self, round_number, continuing_players):
        """Prevents the human player from continuing to play the game if they fold."""
        
        if round_number == 1:
            self.round_1_decision.set('You chose to fold. The game will continue without you.')
            tk.Label(self.master, textvariable=self.round_1_decision).pack()
            self.master.update()
            round_1_bet = Game.adjust_money(continuing_players, False, round_number,
                                            self.your_player.player_id, self.num_bots.get() + 1)
            self.winner_prize += round_1_bet
            self.round1Continue = False
            self.human_folded = True
            self.round_2_starts(continuing_players)

        elif round_number == 2:
            self.find_winner(continuing_players)

    def human_checks(self, round_number, continuing_players):
        """Allows players to continue playing after checking instead of betting any money in Round 1."""
        self.round_1_decision.set("You chose to check.")
        tk.Label(self.master, textvariable=self.round_1_decision).pack()
        self.master.update()

        # Adjusts bot players' money (excluding human player)
        round_1_bet = Game.adjust_money(continuing_players, False, round_number,
                                        self.your_player.player_id, continuing_players)
        self.winner_prize += round_1_bet

        # Adds the human player into list of continuing players after the other players bet
        continuing_players.append(self.your_player)

        self.round_2_starts(continuing_players)

    def check_bet(self, round_number, your_bet, continuing_players):
        """Verifies that the human player can bet the amount of money they want to."""
        # Makes sure that the human player did not choose a non-integer value
        # nor a nonzero integer that's greater than what they can bet (if they have
        # no more money in Round 2, then they can continue the game without
        # actually betting by clicking on "Bet" (because "Fold" will take them
        # out of the game)
        
        if 0 < your_bet <= self.your_money:
            self.valid_bet = True

            if round_number == 1 and self.valid_bet:
                continuing_players.append(self.your_player)
                round_1_bet = Game.adjust_money(continuing_players, your_bet, round_number,
                                                self.your_player.player_id, self.num_bots.get() + 1)
                self.winner_prize += round_1_bet
                self.round_1_decision.set('You chose to bet.')
                tk.Label(self.master, textvariable=self.round_1_decision).pack()
                self.round_2_starts(continuing_players)
            elif round_number == 2 and self.valid_bet:
                # Players who didn't fold in Round 2 will bet money if
                # they're able to, and all bet money in Round 2 is
                # added to the bet money from Round 1
                round_2_players = []

                # Removing the empty string
                self.finishing_players.pop()

                for player_hand in self.finishing_players:
                    for player in self.game_players:
                        if player_hand[0] == player.player_id:
                            round_2_players.append(player)
                round_2_bet = Game.adjust_money(round_2_players, your_bet, round_number,
                                                self.your_player.player_id, self.num_bots.get() + 1)
                self.winner_prize += round_2_bet

                self.find_winner(continuing_players)    
            
        else:
            self.valid_bet = False
            return self.valid_bet

    def find_winner(self, continuing_players):
        """Finds the winner(s) of the Texas Hold 'Em game."""
        # Depending on how many players won, the money is distributed
        # to the winner(s) and the winning player's or winning players'
        # IDs are displayed
        # If there is more than 1 winner, the money is equally divided
        # and rounded to 2 decimal places for simplicity with reading
        # the results of the code (even if the number displayed
        # visually throws out or adds in a penny)

        # Displays the prize that the winner(s) of the game will receive
        display_prize_string = f'The winner(s) will get this money: ${self.winner_prize}'
        self.display_prize.set(display_prize_string)
        tk.Label(self.master, textvariable=self.display_prize).pack()
        
        if len(self.finishing_players) != 0 and len(self.finishing_players) != 1:
            finding_winner = Game.get_winner(self.finishing_players, 'User')
            winner_string = f'Winning player ID(s): {finding_winner}'
            self.display_winner.set(winner_string)
            tk.Label(self.master, textvariable=self.display_winner).pack()

            # Code for if there is more than 1 winner
            if ', ' in finding_winner:
                winner_keys = finding_winner.split(', ')
                for winner_key in winner_keys:
                    for player in self.game_players:
                        if winner_key == player.player_id:
                            player.money += round(self.winner_prize / len(winner_keys), 2)

            # Code for if there is only one winner
            else:
                for player in self.game_players:
                    if finding_winner == player.player_id:
                        player.money += self.winner_prize

        # Code for when everyone folded except 1 person in Round 2
        elif len(self.finishing_players) == 1:
            for player in self.game_players:
                if self.finishing_players[0][0] == player.player_id:
                    player.money += self.winner_prize
                    self.winner = player

        # Code for when everyone folded in Round 2, so
        # everyone is refunded their money from betting in Round 1
        else:
            for player in self.game_players:
                if self.winner_prize != 0:
                    player.money = round(self.winner_prize / len(self.game_players), 2)

        final_cards = []
        final_players_string = ''
        final_players_announcement_string = "7-card hand and best rank of bots who didn't fold in Rounds 1 and 2:"
        self.final_players_announcement.set(final_players_announcement_string)
        tk.Label(self.master, textvariable=self.final_players_announcement).pack()

        iteration = 0
        displayed_final_info = False
        
        for player in self.finishing_players:
            if iteration != len(continuing_players) - 1:
                for continuing_player in continuing_players:   
                    if continuing_player.player_id == player[0]:
                        if continuing_player.player_id != self.your_player.player_id:
                            for hand in self.new_five_card_hands:
                                if continuing_player.player_id == hand[0]:
                                    rank_name = Game.display_rank(hand)
                            final_players_string += f'Player {continuing_player.player_id} ({rank_name}): '
                            for card in continuing_player.hand:
                                final_cards.append(card.suit_and_value)
                            final_players_string += ', '.join(final_cards) + ' '
                            final_cards = []
            iteration += 1

            # If the human player folds in Round 1, this code makes the window display correct
            if not displayed_final_info:
                self.final_player_hand.set(final_players_string)
                tk.Label(self.master, textvariable=self.final_player_hand).pack()

                # Saving information about amount of money per player if it's
                # game 2 or higher
                # Have to sort it, so start with creating the dictionary itself
                not_sorted_previous_money = {}
                keys = []
                for game_player in self.game_players:
                    not_sorted_previous_money[game_player.player_id] = game_player.money

                for key in not_sorted_previous_money:
                    keys.append(key)

                ordered_keys = sorted(keys)

                for player_id in not_sorted_previous_money:
                    for key in ordered_keys:
                        if player_id == key:
                            self.previous_money[player_id] = not_sorted_previous_money[player_id]

                # Displaying the money that each player has after the game is over
                previous_money_strings = []
                for player_id in self.previous_money:
                    previous_money_string = f'Player {player_id}: ${self.previous_money[player_id]}'
                    previous_money_strings.append(previous_money_string)
                self.previous_money_label.set("Players' money: " + ', '.join(previous_money_strings))
                tk.Label(self.master, textvariable=self.previous_money_label).pack()

                self.play_again()

                displayed_final_info = True
    
    def decision_buttons(self, round_number, continuing_players):
        """Creates the label and buttons for the user to make a decision while playing."""

        tk.Button(self.master, text="Bet", command=lambda: self.human_bets(round_number, continuing_players)).pack()
        tk.Button(self.master, text="Fold", command=lambda: self.human_folds(round_number, continuing_players)).pack()
        if round_number == 1:
            tk.Button(self.master, text="Check",
                      command=lambda: self.human_checks(round_number, continuing_players)).pack()

    def round_2_starts(self, continuing_players):
        """Starts Round 2 of the Texas Hold 'Em game."""
        # Round 2 begins
        # Displaying two more community cards

        # Will contain each player's best 5-card hands for Round 2
        self.new_five_card_hands = []
        
        filtered_two_cards = []
        for card in self.game_community_cards:
            filtered_two_cards.append(card.suit_and_value)
            self.two_card_string = 'Last Two Community Cards: ' + ', '.join(filtered_two_cards)

        self.two_card_label.set(self.two_card_string)
        tk.Label(self.master, textvariable=self.two_card_label).pack()

        # Displaying the 7-card hands of each player who didn't fold in Round 1
        # (their 2 cards and the 5 community cards), as well as the best possible 5-card
        # hand for each of these players given these 7 cards
        for continuing_player in continuing_players:
            for card in self.game_community_cards:
                continuing_player.hand.append(card)
            best_hand = Game.hand_combinations(continuing_player.hand, continuing_player.player_id)
            rank_name = Game.display_rank(best_hand)
            if continuing_player.player_id == self.your_player.player_id:
                filtered_your_cards = []
                for card in continuing_player.hand:
                    filtered_your_cards.append(card.suit_and_value)
                    self.your_cards_round_2 = f"Your (Player {self.your_player.player_id}'s) 7-card hand"
                    self.your_cards_round_2 += f" (Best 5-card hand: {rank_name}): "
                    self.your_cards_round_2 += ', '.join(filtered_your_cards)
                self.your_player_label_2.set(self.your_cards_round_2)

            best_hand = Game.hand_combinations(continuing_player.hand, continuing_player.player_id)

            if self.round_1_decision == 'You chose to fold. The game will continue without you.':
                self.human_folded = True
            
            if best_hand[0] == self.your_player.player_id and self.human_folded:
                self.your_best_hand = best_hand
            else:
                self.new_five_card_hands.append(best_hand)

        tk.Label(self.master, textvariable=self.your_player_label_2).pack()

        # Determining which bot players will fold in Round 2
        finishing_player_ids = []
        round_2_bots_string = ''
        for hand in self.new_five_card_hands:
            player_decision = Game.decision_criteria(hand)
            if player_decision != 'Fold':
                self.finishing_players.append(hand)
                finishing_player_ids.append(hand[0])
        # Removing the human player's ID from the finishing_player_ids list
        for player_id in finishing_player_ids[:]:
            if player_id == self.your_player.player_id:
                finishing_player_ids.remove(player_id)
        self.finishing_players.append(self.your_best_hand)
        round_2_bots_string += 'These bot players chose to continue in Round 2: '
        if len(finishing_player_ids) == 0:
            round_2_bots_string += 'None'
        else:
            round_2_bots_string += ', '.join(finishing_player_ids)
        if self.round1Continue:
            round_2_bots_string += '. What would you like to do?'
        self.round_2_bots.set(round_2_bots_string)
        tk.Label(self.master, textvariable=self.round_2_bots).pack()

        # Displays label and buttons for the human player to make a decision in Round 1
        if self.round1Continue:
            self.decision_buttons(2, continuing_players)
        else:
            self.find_winner(continuing_players)

    def play_again(self):
        asked_question = 'Do you want to play again with the same players or start over?'
        self.play_again_question.set(asked_question)
        tk.Label(self.master, textvariable=self.play_again_question).pack()
        tk.Button(self.master, text="Play With Same Players", command=lambda: self.restart_gaming('Same')).pack()
        tk.Button(self.master, text="Start Over", command=lambda: self.restart_gaming('Start Over')).pack()

    def restart_gaming(self, decision):
        if decision == 'Same':
            self.num_games += 1
            self.master.destroy()
            self.game_window()

            # Clearing or adjusting all the following for the next game
            self.money_title = tk.StringVar()
            self.money_values = tk.StringVar()
            self.num_games += 1
            self.game_community_cards = ''
            self.your_player_label_1 = tk.StringVar()
            self.bot_players_label = tk.StringVar()
            self.three_card_label = tk.StringVar()
            self.yourPlayerLabel = False
            self.round_1_bots = tk.StringVar()
            self.your_best_hand = ''
            self.new_five_card_hands = ''
            self.your_player_label_2 = tk.StringVar()
            self.yourPlayerLabel2 = False
            self.two_card_label = tk.StringVar()
            self.finishing_players = []
            self.game_players = []
            self.previous_money_label = tk.StringVar()
            self.display_prize = tk.StringVar()
            self.display_winner = tk.StringVar()
            self.round1Continue = True
            self.round_2_bots = tk.StringVar()
            self.your_player = ''
            self.bot_players = ''
            self.winner_prize = 0
            self.round_1_decision = tk.StringVar()
            self.your_cards_round_1 = ''
            self.your_cards_round_2 = ''
            self.winner = ''
            self.two_card_string = ''
            self.human_folded = False
            self.your_bet_label = tk.StringVar()
            self.your_bet = tk.IntVar()
            self.your_money = ''
            self.valid_bet = False
            self.final_player_hand = tk.StringVar()
            self.final_players_announcement = tk.StringVar()
            self.play_again_question = tk.StringVar()
            
            self.start_playing()

        elif decision == 'Start Over':
            self.master.destroy()
            THEGameUIPacker()


if __name__ == "__main__":
    texas_hold_em_game = THEGameUIPacker()
