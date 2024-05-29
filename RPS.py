def player(prev_play, opponent_history=[], my_history=[],
           play_order=[{
              "RR": 0,
              "RP": 0,
              "RS": 0,
              "PR": 0,
              "PP": 0,
              "PS": 0,
              "SR": 0,
              "SP": 0,
              "SS": 0,
          }]
           ):
    global counter, abbie_count, kris_count, gap, win, loss, winrate, flag, mrugesh_count
    if "counter" not in globals():
        counter = 0
    if "mrugesh_count" not in globals():
        mrugesh_count = 0
    if "flag" not in globals():
        flag = 0 
    if "abbie_count" not in globals():
        abbie_count = 0
    if "kris_count" not in globals():
        kris_count = 0
    if "gap_count" not in globals():
        gap = 0
    if "win" not in globals():
        win = 0
    if "loss" not in globals():
        loss = 0
    if "winrate" not in globals():
        winrate = 0
    counter_moves = {'P': 'S', 'R': 'P', 'S': 'R'}
    counter_moves_2 = {'P': 'R', 'R': 'S', 'S': 'P'}
    if not prev_play:
        prev_play = "R"
    if not my_history:
        my_history.append("R")
    opponent_history.append(prev_play)

    # One step ahead of opponent's previous move
    # win
    if my_history[-1] == "R" and opponent_history[-1] == "S":
        win += 1
    elif my_history[-1] == "P" and opponent_history[-1] == "R":
        win += 1
    elif my_history[-1] == "S" and opponent_history[-1] == "P":
        win += 1
    
    # loss
    elif my_history[-1] == "P" and opponent_history[-1] == "S":
        loss += 1
    elif my_history[-1] == "S" and opponent_history[-1] == "R":
        loss += 1
    elif my_history[-1] == "R" and opponent_history[-1] == "P":
        loss += 1    

    if flag == 0 and win and loss > 0:
        winrate = win/(win+loss) * 100
        if winrate < 40 and len(my_history) > 30:
            flag = 1

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
    # ----- KRIS
    if len(my_history) > 2 and flag == 0:
        if opponent_history[-1] == counter_moves[my_history[-2]]:
            kris_count+=1
            if kris_count > 10:
                guess = counter_moves_2[my_history[-1]]
        else:
            kris_count = 0

    # ----- ABBIE
    last_two = "".join(my_history[-2:])
    if len(last_two) == 2:
        play_order[0][last_two] += 1

    potential_plays = [
    prev_play + "R",
    prev_play + "P",
    prev_play + "S",
    ]
    sub_order = {
    k: play_order[0][k]
    for k in potential_plays if k in play_order[0]
    }

    prediction = max(sub_order, key=sub_order.get)[-1:]
    

    if len(my_history) >= 1 and flag == 0:
        if my_history[-1] == prediction:
            abbie_count+=1
            gap = 0
        else:
            gap+=1
            if gap > 1:
                abbie_count = 0
        if abbie_count > 25:
            guess = counter_moves_2[prediction]
            kris_count = 0
    
    # # ----- MRUGESH

    last_ten = my_history[-10:]
    most_frequent = max(set(last_ten), key=last_ten.count)
    if counter_moves[most_frequent] == opponent_history[-1]:
        mrugesh_count+=1
        if mrugesh_count > 3:
            guess = counter_moves_2[most_frequent]
    else:
        mrugesh_count = 0
    if len(my_history) == 1000:
        play_order=[{
              "RR": 0,
              "RP": 0,
              "RS": 0,
              "PR": 0,
              "PP": 0,
              "PS": 0,
              "SR": 0,
              "SP": 0,
              "SS": 0,
          }]
        counter = 0
        mrugesh_count = 0
        flag = 0 
        abbie_count = 0
        kris_count = 0
        gap = 0
        win = 0
        loss = 0
        winrate = 0
        my_history.clear()
        opponent_history.clear()
    my_history.append(guess)
    return guess

# Attempt at Markov Model
    # Transition Matrix with Labels:
# #          |      ROCK   |   PAPER   |   SCISSORS
# # ----------------------------------------------
# # ME. ROCK     |    0.0   |    0.0    |    0.0
# # ME. PAPER    |    0.0   |    0.0    |    0.0
# # ME. SCISSORS |    0.0   |    0.0    |    0.0

# def player(prev_play, opponent_history = [], my_history = []):
#     transition_matrix = [[0.33, 0.33, 0.33], 
#                              [0.33, 0.33, 0.33], 
#                              [0.33, 0.33, 0.33]]

#     if not prev_play:
#         prev_play = "P"
#     opponent_history.append(prev_play)

#     update_transition_matrix(transition_matrix, prev_play, opponent_history, my_history)
#     normalize_transition_matrix(transition_matrix)
    
#     guess = make_decision(transition_matrix)
#     my_history.append(guess)
#     return guess

# # ---------------------------------------------------------------------------------------

# def update_transition_matrix(transition_matrix, prev_play, opponent_history, my_history):
#     if len(opponent_history) > 1 and len(my_history) > 1:
#         my_last_play = my_history[-1]
#         m = convert_matrix(my_last_play)
#         o = convert_matrix(prev_play)

#         # winning
#         if m == 0 and o == 2:
#             transition_matrix[m][o] +=1
#         elif m == 1 and o == 0:
#             transition_matrix[m][o] +=1
#         elif m == 2 and o == 1:
#             transition_matrix[m][o] +=1
        
#         # losing
#         if m == 0 and o == 1:
#             transition_matrix[m][o] -=1
#         elif m == 1 and o == 2:
#             transition_matrix[m][o] -=1
#         elif m == 2 and o == 0:
#             transition_matrix[m][o] -=1

        
        
#     else:
#         return

# # ---------------------------------------------------------------------------------------

# def normalize_transition_matrix(transition_matrix):
#     for row in transition_matrix:
#         total_prob = sum(row)
#         if total_prob != 0:
#             row[:] = [prob / total_prob for prob in row]

# def convert_matrix(var): # Converting to numbers for matrix
#     # print("VAR: " + var + " <--")
#     if var == "R":
#         converted = 0
#     elif var == "P":
#         converted = 1
#     elif var == "S":
#         converted = 2
#     return converted

# def make_decision(transition_matrix):
#     # Greedy approach
#     ROCK, PAPER, SCISSORS = 0, 1, 2
#     counter = {"R": "P", "P": "S", "S": "R"}
#     prediction = 0
#     for row in [ROCK, PAPER, SCISSORS]:
#         for column in [ROCK, PAPER, SCISSORS]:
#             if transition_matrix[row][column] > prediction:
#                 prediction = transition_matrix[row][column]
#                 opponent_move = column
#     if opponent_move == 0:
#         guess = "R"
#     elif opponent_move == 1:
#         guess = "P"
#     elif opponent_move == 2:
#         guess = "S"
#     guess = counter[guess]
#     return guess