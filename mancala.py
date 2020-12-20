import random, copy, sys

def new_game():
    #MAIN Function
    #starts a new game

    #choose players from valid inputs 
    players = choose_players()

    #initialize game board
    board = [['0','4','4','4','4','4','4'],['0','4','4','4','4','4','4']]
    winner = 'none'
    display_board(board, players)

    #start taking turns until there is a winner 
    while winner == 'none':
        winner, board = handle_turn(players, board) 

    #Game is over, Congratulate Winner. 
    if winner == 0:
        print ('Player 1 wins!')
    elif winner == 1:
        print ('Player 2 wins!')
    else:
        print('Draw.')

    print('GAME OVER') 

def choose_players():
    #checks that the player inputs are valid
    #returns a two item list of strings: random, minimax, alphabeta, or human
    
    #sys.argv are the loading arguments 
    if len(sys.argv) !=3:
        print('Wrong number of arguments. Try Again.')
        print('Must be like "python3 mancala.py human human"')
        exit()

    player_one = sys.argv[1].lower().strip()
    player_two = sys.argv[2].lower().strip()
    
    if player_one != "random" and player_one != "minimax" and player_one !="alphabeta" and player_one != "human":  
        print('Invalid entry for Player 1. Must be: human, random, minimax, or alphabeta')
        print('Try Again') 
        exit()
    elif player_two != "random" and player_two != "minimax" and player_two !="alphabeta" and player_two != "human":  
        print('Invalid entry for Player 2. Must be: human, random, minimax, or alphabeta')
        print('Try Again') 
        exit()

    #if everything looks good:
    print('*** NEW GAME ***\n')

    return [player_one, player_two]

def display_board(board_state, players = ['','']):
    
    if len(set(board_state[0][1:])) == 1 and board_state[0][1] == '4': #if this is initial setup
        print('\nBegin!\n\n')
        print('Player Two: ' + str(players[1]))
        print('Pos:' + '\t' + '  1' + '\t' + ' 2'+ '\t' + ' 3' + '\t' + ' 4' + '\t' + ' 5' + '\t' + ' 6')

    ### Gameboard: ________________________________________________________________________________________
    print( '      || ' + '(' + board_state[1][1] + ')' + '\t' + '(' + board_state[1][2] + ')'+ '\t' + '(' + board_state[1][3] + ')' + '\t' + '(' + board_state[1][4] + ')' + '\t' + '(' + board_state[1][5] + ')' + '\t' + '(' + board_state[1][6]+ ') ||')

    print('    ' + board_state[1][0] + ' ||\t\t\t\t\t    || ' + board_state[0][0])

    print( '      || ' + '(' + board_state[0][6] + ')' + '\t' + '(' + board_state[0][5] + ')'+ '\t' + '(' + board_state[0][4] + ')' + '\t' + '(' + board_state[0][3] + ')' + '\t' + '(' + board_state[0][2] + ')' + '\t' + '(' + board_state[0][1]+ ') ||')
    ######``````````````````````````````````````````````````````````````````````````````````````````````````

    if len(set(board_state[0][1:])) == 1 and board_state[0][1] == '4': #if this is initial setup
        print('Pos:' + '\t' + '  6' + '\t' + ' 5'+ '\t' + ' 4' + '\t' + ' 3' + '\t' + ' 2' + '\t' + ' 1')
        print('Player One: ' + str(players[0]))

def handle_turn(players, board_state): 
    #play full cycle of turns. Player one, check winner, player two, check winner. 
    #inputs are a list of strings designating types of player 1 and player 2 and the current board state. 
    #returns winner and new board state

    #player one goes first 
    turn = 0

    while turn < 2: #loop twice

        last_stone_loc = 0
        while last_stone_loc == 0: 
            #find player's options 
            available_pos = get_available_pos(turn, board_state)

            #call player type function 
            if players[turn] == 'human': 
                last_stone_loc, board_state  = play_human(turn, board_state, available_pos)
            elif players[turn] =='random':
                last_stone_loc, board_state = play_random(turn, board_state, available_pos)
            elif players[turn] =='minimax':
                last_stone_loc, board_state = play_minimax(turn, copy.deepcopy(board_state), available_pos)
            elif players[turn] =='alphabeta':
                last_stone_loc, board_state = play_alphabeta(turn, copy.deepcopy(board_state), available_pos)

            #get out of function if there is a winner by the end of the move
            winner = check_winner(board_state) 
            if winner != 'none': 
                return winner, board_state

        turn +=1 

    return 'none', board_state


def play_human(player, board_state, available_pos):
    #prompt, verify, and execute human player's move 
    #input is an integer 0 or 1 designating player one or two, board state, and list of integers 1-6 of available positions 
    #returns the location of the last stone and the new board state

    #prompt for choice
    print('')
    if player == 0: 
        pos = str(input('Player One, choose a position: ')).strip()
    else:
        pos = str(input('Player Two, choose a position: ')).strip()

    #verify choice selection is available 
    while pos not in available_pos:
        if str(pos).lower() == 'exit' or str(pos).lower() == 'end' :
            print('GAME OVER') 
            exit() 
        pos = str(input('That choice isnt available. Choose a position: ')).strip()

    #exectue move 
    last_stone_loc, board_state = execute_selection(board_state, player,int(pos))
    display_board(board_state)
    
    return last_stone_loc, board_state

    
def get_available_pos(player, board_state):
    #returns a list of integers (1-6) that the player can choose during their turn
    #input is an integer 0 or 1 designating player one or two and the board state
    available_pos = []

    #loop through pits 1-6 to see which are not empty
    for i in range(1,7): #note: i = 1 to 6  
        if board_state[player][i] != '0':
            available_pos.append(str(i))
    
    return available_pos


def toggle(input):
    #input is a intiger 0 or 1 
    #returns an intiger 0 or 1 
    if input == 0:
        return 1 
    elif input == 1:
        return 0 


def execute_selection(board_state, player, pos):
    #moves beans on a temporary game board based on the player and their move selection 
    #inputs are integers 0 or 1 for player one and two and 1-6 for pit selection 
    #returns the final game state and the integer location that the last stone was dropped 

    def switch_sides(side):
        #updates and returns indices when pits cross over to the other side of the board 
        pos = 7 #because the first thing to do is deduct one from selection

        if side == 0:
            side = 1 
        else: 
            side = 0 
        
        return side, pos

    def opposite_pit(pos):
        #returns the index position of the opposing pit from input 
        if pos == 0:
            return 0 
        else:
            return 7 - pos
        
    side = player
    stone = int(board_state[side][pos])
    board_state[side][pos] = '0'

    while stone > 0:
        #when the store is reaches, start dropping stones on other side 
        if pos == 0: 
            side, pos = switch_sides(side)
        
        pos -= 1 
        if pos > 0 or side == player: #don't lay stone in opponent's store
            board_state[side][pos] = str(int(board_state[side][pos]) + 1)
            stone -= 1 

    #check for empty pit on your side and stone in opponent's pit: 
    #1. landed in a 0 space. 
    #2. landed on your side. 
    #3. landed not in your store. 
    #4. opponent has stones across the way.
    if board_state[side][pos] == '1' and side == player and pos != 0 and board_state[toggle(side)][opposite_pit(pos)] != '0':
        total = int(board_state[toggle(side)][opposite_pit(pos)]) + int(board_state[side][pos])
        board_state[toggle(side)][opposite_pit(pos)] = '0'
        board_state[side][pos] = '0'
        board_state[side][0] = str(int(board_state[side][0]) + total)

    #return the final board state and the pos of the last stone
    return pos, board_state 


def check_winner(board_state):
    #check the whole game board for a winner. Either a player's store has 24 stones or no stones of their side 
    winner = 'none' 

    if int(board_state[0][0]) >= 25:
        winner = 0
    elif int(board_state[1][0]) >= 25:
        winner = 1

    #if someone's side is empty, slide all stones over to the store on their side. Then make comparison
    if board_state[0][1:] == ['0','0','0','0','0','0'] or board_state[1][1:] == ['0','0','0','0','0','0']:
        for i in range(1,7):
            board_state[0][i] = str(int(board_state[0][0]) + int(board_state[0][i]))
            board_state[1][i] = str(int(board_state[1][0]) + int(board_state[1][i]))

        if int(board_state[0][0]) > int(board_state[1][0]):
            winner = 0
        elif int(board_state[0][0]) < int(board_state[1][0]):
            winner = 1 
        elif int(board_state[0][0]) == int(board_state[1][0]):
            winner = 'Draw' 

    return winner


def play_random(player, board_state, available_pos):
    #plays a random move out of available positions
    #input is an integer 0 or 1 designating player one or two and list of available positions 1-6
    #returns the location of the last stone

    #choose random choice 
    pos = random.choice(available_pos)

    #exectue move 
    last_stone_loc, board_state = execute_selection(board_state, player,int(pos))
    print('')
    print('Random player chose ' + str(pos))
    display_board(board_state)
    
    return last_stone_loc, board_state


def play_minimax(player, board_state, available_pos):
    #plays and executes a minimax optimal move
    #input is an integer 0 or 1 designating player one or two as minimax, the current board state, and a list of available positions for minimax player.
    #returns the location of the last stone and the real board state

    sub_available_pos = available_pos
    sub_last_stone = 0
    utility_list = [] 
    depth, max_depth = 0, 6 #even depth ends on max_val (takes about 2-3 sec/move)

    #find optimal choice
    for move in sub_available_pos:
        depth = 0
        #get subsequent board state 
        sub_last_stone, sub_board = execute_selection(copy.deepcopy(board_state), player,int(move))

        #if this move resulted in a stone landing in your store, call max function b/c it's your turn again
        if sub_last_stone == 0:
            utility_list.append ((move, maximum_move(player, sub_board, depth+1, max_depth)))
        else: 
            utility_list.append ((move, minimum_move(toggle(player), sub_board, depth+1, max_depth)))

    #sort utility list based on value in descending order
    utility_list.sort(key=lambda x: x[1], reverse=True) 
    pos = utility_list[0][0]

    #exectue move for real 
    last_stone_loc, board_state = execute_selection(board_state, player,int(pos))
    print('')
    print('Minimax player chose ' + str(pos))
    display_board(board_state)

    return last_stone_loc, board_state


def minimum_move (side, board_state, depth, max_depth):
    #support function for minimax player
    #simulates an opponent's move. 'side' input is the side index of the minimum player
    #returns the integer value of this board_state's utility [-1,1]
    
    utility_list = []

    #check for subsequent winner 
    sub_winner = check_winner(board_state) #returns 0 or 1 
    if sub_winner == side:  #if the winner is the opponent
        util = -1.0
    elif sub_winner == toggle(side): 
        util = 1.0
    elif sub_winner == 'Draw':
        util = 0.0
    elif depth == max_depth:
        #calculate utility of this intermediate state
        #minimax's store minus opponent's store divided by 25. range from [-1, 1]
        util = (float(board_state[toggle(side)][0]) - float(board_state[side][0]))/25
    elif sub_winner == 'none': #else, game is still going
        #find available moves 
        sub_avail_pos = get_available_pos(side, board_state)
        for move in sub_avail_pos:
            sub_last_stone, sub_board = execute_selection(copy.deepcopy(board_state), side ,int(move))
        
            #if move ended in minimum player's store, then repeat turn 
            if sub_last_stone == 0:
                utility_list.append ((move, minimum_move(side, sub_board, depth+1, max_depth)))
            else: 
                #fill utility list with moves and their values 
                utility_list.append ((move, maximum_move(toggle(side), sub_board, depth+1, max_depth)))
            
        #sort utility_list in ascending order
        utility_list.sort(key=lambda x: x[1], reverse=False) 
        util = utility_list[0][1]

    return util


def maximum_move (side, board_state, depth, max_depth):
    #support function for minimax player. It's a mirror of minimum_move
    #simulates a maximum move. 'side' input is the side index of the maximizing player player (i.e. minimax player) 
    #returns the integer value of this board_state's utility [-1,1]
    
    utility_list = []

    #check for subsequent winner 
    sub_winner = check_winner(board_state) #returns 0 or 1 
    if sub_winner == side:  #if the winner is the maximum player
        util = 1.0
    elif sub_winner == toggle(side): 
        util = -1.0
    elif sub_winner == 'Draw':
        util = 0.0
    elif depth == max_depth:
        #calculate utility of this intermediate state
        #minimax's store minus opponent's store divided by 25. Range is [-1, 1]
        util = (float(board_state[side][0]) - float(board_state[toggle(side)][0]))/25
    elif sub_winner == 'none': #else, game is still going
        #find available moves 
        sub_avail_pos = get_available_pos(side, board_state)
        for move in sub_avail_pos:
            sub_last_stone, sub_board = execute_selection(copy.deepcopy(board_state), side ,int(move))
        
            #if move ended in maximum player's store, then repeat turn 
            if sub_last_stone == 0:
                utility_list.append ((move, maximum_move(side, sub_board, depth+1, max_depth)))
            else: 
                #fill utility list with moves and their values 
                utility_list.append ((move, minimum_move(toggle(side), sub_board, depth + 1, max_depth)))
            
        #sort utility_list in ascending order
        utility_list.sort(key=lambda x: x[1], reverse=True) 
        util = utility_list[0][1]
    
    return util


def play_alphabeta(player, board_state, available_pos):
    #plays and executes an optimal move using minimax and alphabeta pruning
    #input is an integer 0 or 1 designating player one or two, the board state, and a list of available positions for minimax player.
    #returns the location of the last stone and the real board state

    sub_available_pos = available_pos
    sub_last_stone = 0
    utility_list = [] 
    depth, max_depth = 0, 10 #even depth ends on max_val (takes about 8 sec/move)

    #find optimal choice
    for move in sub_available_pos:
        depth = 0
        #get subsequent board state 
        sub_last_stone, sub_board = execute_selection(copy.deepcopy(board_state), player,int(move))

        #if this move resulted in a stone landing in your store, call max function b/c it's your turn again
        if sub_last_stone == 0:
            utility_list.append ((move, a_b_maximum_move(player, sub_board, -2.0, 2.0, depth+1, max_depth)))
        else: 
            utility_list.append ((move, a_b_minimum_move(toggle(player), sub_board,-2.0, 2.0, depth+1, max_depth)))

    #sort utility list based on value in descending order
    utility_list.sort(key=lambda x: x[1], reverse=True) 
    pos = utility_list[0][0]

    #exectue move for real 
    last_stone_loc, board_state = execute_selection(board_state, player,int(pos))
    print('')
    print('AlphaBeta player chose ' + str(pos))
    display_board(board_state)

    return last_stone_loc, board_state


def a_b_minimum_move (side, board_state, alpha, beta, depth, max_depth):
    #support function for alphabeta player
    #simulates an opponent's move. 'side' input is the side index of the minimum player
    #returns the integer value of this board_state's utility [-1,1]
    
    utility_list = []
    util = '' 

    #check for subsequent winner 
    sub_winner = check_winner(board_state) #returns 0 or 1 
    if sub_winner == side:  #if the winner is the opponent
        util = -1.0
    elif sub_winner == toggle(side): 
        util = 1.0
    elif sub_winner == 'Draw':
        util = 0.0
    elif depth == max_depth:
        #calculate utility of this intermediate state
        #minimax's store minus opponent's store divided by 25. range from [-1, 1]
        util = (float(board_state[toggle(side)][0]) - float(board_state[side][0]))/25
    elif sub_winner == 'none': #else, game is still going
        #find available moves 
        sub_avail_pos = get_available_pos(side, board_state)
        for move in sub_avail_pos:
            sub_last_stone, sub_board = execute_selection(copy.deepcopy(board_state), side ,int(move))
        
            #if move ended in minimum player's store, then repeat turn 
            if sub_last_stone == 0:
                utility_list.append ((move, a_b_minimum_move(side, sub_board, alpha, beta, depth+1, max_depth)))
            else: 
                #fill utility list with moves and their values 
                utility_list.append ((move, a_b_maximum_move(toggle(side), sub_board, alpha, beta, depth+1, max_depth)))

            #pruning 
            if utility_list[len(utility_list)-1][1] <= alpha: #if most recent value is smaller than alpha, don't worry about the rest of the options. 
                return utility_list[len(utility_list)-1][1]
            elif utility_list[len(utility_list)-1][1] < beta: 
                beta = utility_list[len(utility_list)-1][1]
                util = beta

    if util == '': #if no beta was crossed, sort to find best util. 
        #sort utility_list in ascending order
        utility_list.sort(key=lambda x: x[1], reverse=False) 
        util = utility_list[0][1]

    return util


def a_b_maximum_move (side, board_state, alpha, beta, depth, max_depth):
    #support function for alphabeta player. It's a mirror of a_b_minimum_move
    #simulates a maximum move. 'side' input is the side index of the maximizing player player (i.e. minimax player) 
    #returns the integer value of this board_state's utility [-1,1]
    
    utility_list = []
    util = ''

    #check for subsequent winner 
    sub_winner = check_winner(board_state) #returns 0 or 1 
    if sub_winner == side:  #if the winner is the maximum player
        util = 1.0
    elif sub_winner == toggle(side): 
        util = -1.0
    elif sub_winner == 'Draw':
        util = 0.0
    elif depth == max_depth:
        #calculate utility of this intermediate state
        #minimax's store minus opponent's store divided by 25. Range is [-1, 1]
        util = (float(board_state[side][0]) - float(board_state[toggle(side)][0]))/25
    elif sub_winner == 'none': #else, game is still going
        #find available moves 
        sub_avail_pos = get_available_pos(side, board_state)
        for move in sub_avail_pos:
            sub_last_stone, sub_board = execute_selection(copy.deepcopy(board_state), side ,int(move))
        
            #if move ended in maximum player's store, then repeat turn 
            if sub_last_stone == 0:
                utility_list.append ((move, a_b_maximum_move(side, sub_board, alpha, beta, depth+1, max_depth)))
            else: 
                #fill utility list with moves and their values 
                utility_list.append ((move, a_b_minimum_move(toggle(side), sub_board,alpha, beta, depth + 1, max_depth)))
            
            #pruning 
            if utility_list[len(utility_list)-1][1] >= beta: #if most recent value is greater than beta, don't worry about the rest of the move options. 
                return utility_list[len(utility_list)-1][1]
            elif utility_list[len(utility_list)-1][1] > alpha: 
                alpha = utility_list[len(utility_list)-1][1]
                util = alpha
    
    if util == '': #if no alpha was crossed, sort to find best util. 
        #sort utility_list in ascending order
        utility_list.sort(key=lambda x: x[1], reverse=True) 
        util = utility_list[0][1]

    return util

#Start New Game as defined above 
new_game()





