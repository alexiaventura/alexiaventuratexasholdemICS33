# Alexia Ventura's code for ICS 33 Project

# Modules that are needed for this program
import random
import itertools


# Creating a class that represents a player
class Player:
    def __init__(self, player_id, hand, money):
        self.player_id = player_id
        self.hand = hand
        self.money = money


# Creating a class that represents a card
class PlayingCard:
    def __init__(self, suit_and_value):
        self.suit_and_value = suit_and_value


def creating_card_deck():
    """Creates a deck of cards."""
    
    # Possible suits (S = spades, H = hearts, D = diamonds, C = clubs)
    suits = ['S', 'H', 'D', 'C']

    # List that will contain all the cards of the deck
    deck_of_cards = []

    # Creates each unique card that is added to the deck of cards
    # Possible values (2-10, 11 = J, 12 = Q, 13 = K, 1 = A)
    for suit in suits:
        for value in range(1, 14):
            card = PlayingCard(str(suit) + str(value))
            deck_of_cards.append(card)

    return deck_of_cards


def random_two_cards(deck_of_cards):
    """Randomly selects two cards for a player's hand."""

    player_hand = []

    for card_creation in range(2):
        max_num = len(deck_of_cards) - 1
        random_index = random.randint(0, max_num)
        random_card = deck_of_cards[random_index]
        player_hand.append(random_card)
        deck_of_cards.remove(random_card)
    
    return player_hand


def creating_players(n_player, deck_of_cards, money):
    """Creates two-card hands for all participating players."""

    # n_player: number of players

    duplicates = []
    all_players = []

    # Code for when it is not the first game
    # Players are prevented from playing more games if they
    # have no more money
    # (Due to a bug I had that caused duplicate players) As a precaution,
    # potential duplicate players are filtered out
    if type(money) == dict:
        for player_id in money:
            player_hand = random_two_cards(deck_of_cards)
            determined_money = money[player_id]
            ready_player = Player(player_id, player_hand, determined_money)
            if ready_player.money > 0:
                duplicates.append(ready_player)
                all_players = list(set(duplicates))

        player_ids = []
        for ready_player in all_players:
            player_ids.append(int(ready_player.player_id))
        sorted_player_ids = sorted(player_ids)

        copy_all_players = all_players[:]
        all_players = []

        for player_id in sorted_player_ids:
            for ready_player in copy_all_players:
                if int(player_id) == int(ready_player.player_id):
                    all_players.append(ready_player)

    # Code for when it is the very first game (all players
    # are created using the number of players given)
    else:
        for player in range(n_player):
            player_hand = random_two_cards(deck_of_cards)

            # Player ID is determined based on the loop iterations
            player_id = str(player + 1)

            ready_player = Player(player_id, player_hand, money)
            all_players.append(ready_player)

    return all_players


def decision_criteria(player_hand):
    """Sets the conditions for what will cause a bot player to fold. (Smarter Bots Function)"""

    # Bot players fold if they have a high card below 10
    if player_hand[1][0] == 9 and sum(player_hand[1][1]) < 10 and sum(player_hand[1][1]) != 1:
        player_decision = 'Fold'
    else:
        player_decision = 'Not Fold'

    return player_decision


def five_community_cards(deck_of_cards):
    """Randomly selects five community cards for the game."""

    # Creating a list that will contain the five community cards
    community_cards = []

    for card_creation in range(5):
        max_num = len(deck_of_cards) - 1
        random_index = random.randint(0, max_num)
        community_card = deck_of_cards[random_index]
        community_cards.append(community_card)
        deck_of_cards.remove(community_card)

    return community_cards


def determine_hand(hand, player_id):
    """Determines what rank the hand is through splitting the card identification into 2 parts: suit and value."""

    # This function only works for hands that have 5 cards
    assert len(hand) == 5

    suits = []
    value_filter = []
    values = []

    # Separating the suits from the values
    for card in hand:
        if type(card) != str:
            suits.append(card.suit_and_value[0])
            card_value = card.suit_and_value.split(card.suit_and_value[0])
            value_filter.append(card_value[1])
        else:
            suits.append(card[0])
            card_value = card.split(card[0])
            card_value.remove('')
            value_filter.append(card_value)

    # Converting the values (in the form of strings) to integers
    if type(card) != str:
        for element in value_filter:
            values.append(int(element))
    else:
        for card_list in value_filter:
            for element in card_list:
                values.append(int(element))

    # Sorting the values from lowest to highest value
    values.sort()

    # Making the aces (represented by integer 1) higher in value than the other values 
    num_aces = values.count(1)
    if num_aces != 0:
        for ace in range(num_aces):
            values.remove(1)
            values.append(1)

    # Determining the rank of the hand
    is_straight_or_flush = straights_flushes(suits, values)
    if is_straight_or_flush == [False, None]:
        # Not a royal flush, straight flush, flush, nor straight
        has_same_values = not_straight_or_flush(values)
        if has_same_values == [False, None]:
            # Not a pair nor three of a kind nor four of a kind
            # Also not any possible winning hand other than high card
            high_card_result = high_card_function(values)
            player_hand = high_card_result
        else:
            # Is a pair, three of a kind, four of a kind, full house, or two pair
            player_hand = has_same_values
    else:
        # Is a royal flush, straight flush, flush, or straight
        player_hand = is_straight_or_flush

    # List that contains player's ID, the rank of the player's hand, and
    # what suits and/or values caused the player to get that rank for their hand
    players_and_ranks_list = [player_id, [player_hand[1], player_hand[0]]]

    return players_and_ranks_list


def hand_combinations(seven_card_hand, player_id):
    """Finds all possible 5-card hands a player could have given their 2 cards and the 5 community cards."""

    # This function only works for hands that have 7 cards
    assert len(seven_card_hand) == 7

    # Using the combinations function to find all possible 5-card combinations with the 7 available cards    
    # Documentation (itertools.combinations(iterable,r)):
    # https://docs.python.org/release/3.10.4/library/itertools.html?highlight=combinations%20permutations
    combination_result = itertools.combinations([0, 1, 2, 3, 4, 5, 6], 5)
    five_card_combinations = list(combination_result)
    
    # Append each five-card combination into a list of combinations
    # per player. 5 of the 7 cards are randomly combined to create a
    # possible 5-card hand.
    all_combinations = []
    created_hand = []
    iteration = 1
    for combination in five_card_combinations:
        for index in combination:
            created_hand.append(seven_card_hand[index])
        all_combinations.append(created_hand)
        created_hand = []
        iteration += 1

    possible_hands = []

    # Finding what rank each possible 5-card hand is
    for combination in all_combinations:
        type_hand = determine_hand(combination, player_id)
        possible_hands.append(type_hand)

    # Finding the best 5-card hand out of all possible 5-card hands
    best_hand = get_winner(possible_hands, 'Combinations')

    return [player_id, best_hand]


def not_straight_or_flush(values):
    """Tests for conditions when a 5-card hand is not any straight or
    flush, nor requires using the high card function."""

    # Finding unique values and the number of cards per value (helps with separating the different types
    # of possible winning hands)

    unique_values_list = []

    for value in values:
        if value not in unique_values_list:
            unique_values_list.append(value)

    num_cards_per_value = []
    value_count = {}

    for value in unique_values_list:
        num_cards_per_value.append(values.count(value))
        value_count[value] = values.count(value)

    # Tried moving this higher to avoid a "referenced before assignment" error
    type_hand = False
    rank = None

    if len(unique_values_list) == 2:

        # Full House (three cards with same value, two cards of same value
        # that's different from the previous three cards' value)        
        if 2 in num_cards_per_value and 3 in num_cards_per_value:
            type_hand = unique_values_list
            rank = 3

        # Four of a kind (four cards have matching values and can be of any suit)
        elif 4 in num_cards_per_value and 1 in num_cards_per_value:
            for value in value_count:
                if value_count[value] == 4:
                    type_hand = [value]
            rank = 2

    elif len(unique_values_list) == 3:

        # Three of a kind (three cards have matching values and can be of any suit)        
        if 3 in num_cards_per_value and num_cards_per_value.count(1) == 2:
            for value in value_count:
                if value_count[value] == 3:
                    type_hand = [value]
            rank = 6

        # Two Pairs (two pairs of cards have matching values and can be of any suit)
        elif num_cards_per_value.count(2) == 2:
            two_pair_values = []
            for value in value_count:
                if value_count[value] == 2:
                    two_pair_values.append(value)
            type_hand = two_pair_values
            rank = 7

    elif len(unique_values_list) == 4:

        # Pair (two cards have matching values and can be of any suit)
        if 2 in num_cards_per_value and num_cards_per_value.count(1) == 3:
            for value in value_count:
                if value_count[value] == 2:
                    type_hand = [value]
            rank = 8

    return [type_hand, rank]


def straights_flushes(suits, values):
    """Tests for conditions when a 5-card hand is a type of straight or flush."""

    num_same_suits = suits.count(suits[0])

    # Royal flush (straight flush with values 10 to Ace)
    if num_same_suits == 5 and values == [10, 11, 12, 13, 1]:
        type_hand = [10, 11, 12, 13, 1]
        rank = 0

    # Possible straight flush
    elif num_same_suits != 5 and values == [10, 11, 12, 13, 1]:
        type_hand = [10, 11, 12, 13, 1]
        rank = 1

    else:
        type_hand = 'Not a royal flush'

    # Checks if hand is a straight flush, flush, or straight
    if type_hand == 'Not a royal flush':
        # Checking if the cards are of increasing order
        increasing_order = False
        previous_value = values[0]
        verified_values = 0

        for value in values:
            if value != values[0]:
                if value > previous_value and value == previous_value + 1:
                    verified_values += 1
                previous_value = value

        # Adjusted by -1 because of the value != values[0] condition
        if verified_values == len(values) - 1:
            increasing_order = True

        # Straight flush (straight of same suit)
        if num_same_suits == 5 and increasing_order is True:
            type_hand = values
            rank = 1

        # Flush (five cards of same suit)
        elif num_same_suits == 5 and increasing_order is False:
            type_hand = values
            rank = 4

        # Straight (five cards in increasing value, for any suit)
        elif num_same_suits != 5 and increasing_order is True:
            type_hand = values
            rank = 5

        # Not any type of straight or flush
        else:
            type_hand = False
            rank = None

    return [type_hand, rank]


def high_card_function(values):
    """When no player has all other possible winning hands, a winner
    is chosen based on if they have the highest card of all players"""

    # Returns the highest value to be used in the get_winner function
    
    # An ace is highest in value if any hands have it
    # Otherwise, the maximum value (excluding 1) is found
    if 1 not in values:
        highest_value = max(values)
    else:
        highest_value = 1

    rank = 9

    return [[highest_value], rank]


def get_winner(list_hands, magic_word):
    """Determines who is the winner in a game of Texas Hold 'Em or what possible 5-card hand is the best."""
    
    # Dictionary where the key is a player's ID and the value is
    # the rank of the player's card
    players_and_ranks = {}

    # Differentiates using this function for finding a winner and for finding the best 5-card hand
    # The magic_word is the string representing what the function is being used for.
    # 'Combinations': finding the best 5-card hand for a player in Round 2
    # 'User': used as a general word for finding the winner of the game

    list_index = 0
    iteration = 0
    for player_hand in list_hands:
        if magic_word == 'Combinations':
            players_and_ranks[str(list_index)] = player_hand[1]
            list_index += 1
        elif magic_word == 'User' and iteration != len(list_hands) - 1:
            players_and_ranks[player_hand[0]] = player_hand[1]
        iteration += 1

    # Creating a list that will connect ranks of players' hands with
    # what values had caused the ranks
    ranks_and_causes = []

    for player_id in players_and_ranks:
        ranks_and_causes.append(players_and_ranks[player_id])

    # Creating a list that helps with finding the winning player(s)
    # through examining their rank(s)
    player_ranks = []

    for rank_and_cause in ranks_and_causes:
        for index_position in range(len(rank_and_cause)):
            if index_position == 0:
                player_ranks.append(rank_and_cause[index_position])

    # Finding the smallest rank, meaning the player(s) with the best hand
    if len(player_ranks) != 0:
        winning_rank = min(player_ranks)

    # Creating a list of the player or players who have the best hand
    num_winning_players = []

    for player_id in players_and_ranks:
        if players_and_ranks[player_id][0] == winning_rank:
            num_winning_players.append(player_id)

    winning_player_list = []

    # There's only one 5-card hand that can clearly be stated as the best one for a player
    # (no ties in rank with other possible 5-card hands)
    if len(num_winning_players) == 1 and magic_word == 'Combinations':
        for winner in num_winning_players:
            winning_hand = players_and_ranks[winner]            
        for winner in winning_player_list:
            winning_player_list.append(ranks_and_causes[winner])

    # If there is only one player who has a winning hand, then that player is the winner
    # of the game
    elif len(num_winning_players) == 1 and magic_word == 'User':
        winning_player = num_winning_players[0]

    # Code for potentially breaking a tie
    else:
        sums_dict = {}
        sums_list = []
        for possible_winner in num_winning_players:
            calculated_sum = sum(players_and_ranks[possible_winner][1])
            sums_dict[possible_winner] = calculated_sum
            sums_list.append(calculated_sum)

        # Making sure that an ace is always counted as the highest value
        if 1 not in sums_list:
            max_sum = max(sums_list)
        else:
            max_sum = 1

        if sums_list.count(max_sum) == 1:
            # After using the tiebreaker code, a single winner
            # was finally determined through seeing
            # that it has the higher values for an
            # equally-ranked hand
            for player_id in sums_dict:
                if sums_dict[player_id] == max_sum:
                    winning_player = player_id

        else:
            # Multiple players tied, and there can't be
            # any tie-breaking, so all these players won
            for player_id in sums_dict:
                if sums_dict[player_id] == max_sum:
                    winning_player_list.append(player_id)
            winning_player = ', '.join(winning_player_list)

    # Returning different information depending on the usage of the function
    if magic_word == 'Combinations' and len(winning_player_list) != 0:
        return players_and_ranks[winning_player_list[0]]
    elif magic_word == 'Combinations' and len(winning_player_list) == 0 and len(num_winning_players) == 1:
        return winning_hand
    elif magic_word == 'User':
        return winning_player


def display_rank(player_hand):
    """Returns the rank of a player's hand, which is displayed when running the program."""
    
    if player_hand[1][0] == 0:
        rank_name = 'Royal Flush'
    elif player_hand[1][0] == 1:
        rank_name = 'Straight Flush'
    elif player_hand[1][0] == 2:
        rank_name = 'Four of a Kind'
    elif player_hand[1][0] == 3:
        rank_name = 'Full House'
    elif player_hand[1][0] == 4:
        rank_name = 'Flush'
    elif player_hand[1][0] == 5:
        rank_name = 'Straight'
    elif player_hand[1][0] == 6:
        rank_name = 'Three of a Kind'
    elif player_hand[1][0] == 7:
        rank_name = 'Two Pairs'
    elif player_hand[1][0] == 8:
        rank_name = 'Pair'
    elif player_hand[1][0] == 9:
        rank_name = 'High Card'
    return rank_name


def adjust_money(continuing_players, human_bet, round_number, human_id, agreeing_players):
    """Keeps track of the players who bet money in a round and how much was bet."""

    bet_money = 0

    # When calling this function, the argument for bet_money was initialized with the value 0

    # Makes sure that there are players who are making a bet, and that a player
    # has enough money to bet, before having every player bet $1
    # (If nobody bets or can bet, the returned value of bet_money is 0)

    if len(continuing_players) != 0:
        for continuing_player in continuing_players:
            if continuing_player.money >= human_bet and continuing_player.player_id == human_id and human_bet:
                continuing_player.money -= human_bet
                bet_money += human_bet
            else:
                bet_money += bot_bet(continuing_player, round_number, human_id,
                                     agreeing_players, len(continuing_players))

    return bet_money


def bot_bet(continuing_player, round_number, human_id, agreeing_players, num_continuing):
    """Determines the code used for a bot player, depending on the round."""

    # This function is applied to one bot player at a time

    bet_money = 0

    if round_number == 1:
        if continuing_player.player_id != human_id:
            bet_money = bot_logic(continuing_player, round_number, False, False)

    elif round_number == 2:
        if continuing_player.player_id != human_id:
            bet_money = bot_logic(continuing_player, round_number, agreeing_players, num_continuing)

    return bet_money


def bot_logic(continuing_player, round_number, agreeing_players, num_continuing):
    """Adjusts a bot player's money depending on the conditions."""

    bet_money = 0

    # This function is applied to one bot player at a time

    if round_number == 1:
        type_hand = determine_hand(continuing_player.hand, continuing_player.player_id)
    elif round_number == 2:
        type_hand = hand_combinations(continuing_player.hand, continuing_player.player_id)

    # (This excludes any hands that cause a bot to fold, because that was
    # already taken care of earlier in running the program)

    # For rank 9 (high cards) in Round 1, bots check because they're skeptical
    # about whether it's worth betting anything yet, which causes bet_money to
    # remain at 0
    if type_hand[1][0] == 9 and round_number == 1:
        pass

    # In Round 2, bots will bet $2 if they have a high card and less
    # than 50% of all players didn't fold for Round 2. Otherwise,
    # they will bet $1.
    elif type_hand[1][0] == 9 and round_number == 2:
        if agreeing_players and num_continuing:
            if num_continuing / agreeing_players < .5:
                continuing_player.money -= 2
                bet_money += 2
            else:
                continuing_player.money -= 1
                bet_money += 1
            
    # For rank 8 (pairs), bots bet $1 because they might have a decent
    # chance at winning
    elif type_hand[1][0] == 8:
        continuing_player.money -= 1
        bet_money += 1

    # For ranks 6 and 7 (three of a kind and two pairs respectively), bots bet
    # $2 (slightly more than pairs because these are better hands)
    elif type_hand[1][0] == 6 or type_hand[1][0] == 7:
        continuing_player.money -= 2
        bet_money += 2

    # For ranks 3, 4, and 5 (full house, flushes, and straights respectively),
    # bots bet $4 (slightly more than ranks 6 and 7 due to better hands)
    elif type_hand[1][0] == 3 or type_hand[1][0] == 4 or type_hand[1][0] == 5:
        continuing_player.money -= 4
        bet_money += 4

    # For ranks 0, 1, and 2 (royal flushes, straight flushes, and four of
    # a kind respectively), bots bet $5 (slightly more than ranks 3, 4, and
    # 5 due to these hands being very rare)
    elif type_hand[1][0] == 0 or type_hand[1][0] == 1 or type_hand[1][0] == 2:
        continuing_player.money -= 5
        bet_money += 5

    return bet_money
