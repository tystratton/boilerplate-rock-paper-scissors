# MY FUNCTION
import random

def player(prev_play, opponent_history=[]):
    opponent_history.append(prev_play)
    # initial guess
    guess = "P"

    moves = ["R", "P", "S"]
    counter_moves = {'P': 'S', 'R': 'P', 'S': 'R'}
    counter_moves_2 = {'P': 'R', 'R': 'S', 'S': 'P'}
    global counter
    global my_history
    global play_order
    global pattern_count
    if 'play_order' not in globals():
        play_order= {
              "RR": 0,
              "RP": 0,
              "RS": 0,
              "PR": 0,
              "PP": 0,
              "PS": 0,
              "SR": 0,
              "SP": 0,
              "SS": 0,
          }
    if 'counter' not in globals():
        counter = 0  # Initialize turn list if it doesn't exist
    if "my_history" not in globals():
        my_history = [""]
    if "win_loss" not in globals():
        win_loss = [""]
    if "pattern_count" not in globals():
        pattern_count = 0
    # Finding my most frequent move from last 10
    last_ten = my_history[-10:]
    most_frequent = max(set(last_ten), key=last_ten.count)
    if most_frequent == "":
        most_frequent = "S"

    # One step ahead of opponent's previous move
    if counter == 0 and prev_play == "R":
        guess = "S"
        counter+=1
    elif counter == 0 and prev_play == "P":
        guess = "R"
        counter+=1
    elif counter == 0 and prev_play == "S":
        guess = "P"
        counter+=1
    # Two steps ahead of opponent's previous move
    elif counter == 1 and prev_play == "R":
        guess = "P"
        counter = 0
    elif counter == 1 and prev_play == "P":
        guess = "S"
        counter = 0
    elif counter == 1 and prev_play == "S":
        guess = "R"
        counter = 0

    if guess == most_frequent:
        guess = random.choice(moves)

    if len(my_history)> 4:
        last_two = "".join(opponent_history[-2:]) #SR
        play_order[last_two]+=1 # increase dictionary
        max_value = max(play_order.values()) # max value
        sorted_values = sorted(play_order.values(), reverse=True)
        second_highest_value = sorted_values[1] if len(sorted_values) > 3 else None
        if (max_value - second_highest_value) > 1:
            prediction = opponent_history[-1]
            guess = counter_moves[prediction]
        if opponent_history[-1] == counter_moves[my_history[-2]]:
            pattern_count+=1
            if pattern_count > 10:
                guess = counter_moves_2[my_history[-1]]
        else:
            pattern_count = 0

    my_history.append(guess)

    # reset all the variables
    if len(my_history) == 1001:
       play_order= {
              "RR": 0,
              "RP": 0,
              "RS": 0,
              "PR": 0,
              "PP": 0,
              "PS": 0,
              "SR": 0,
              "SP": 0,
              "SS": 0,
          } 
       counter = 0
       my_history = [""]
       pattern_count = 0
    return guess
