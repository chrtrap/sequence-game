import itertools
from queue import Empty
import numpy as np

def make_cards():
    colors = ["S","H","D","C"]
    numbers = [str(num) for num in range(2,11)] + ["Q", "K", "A"]

    cards = [col+num for col in colors for num in numbers]
    return cards

cards = make_cards()

spades = cards[:12]
hearts = cards[12:24]
diamonds = cards[24:36]
clubs = cards[36:48]

def changeCaps(string):
    if not isinstance(string, str):
        return string
    stringo = ''
    for c in string:
        if c.islower():
            stringo += c.upper()
        else:
            stringo += c
    return stringo


def make_board():
    board = np.empty(dtype="object",shape=(10,10))
    board[0,0] = "F"
    board[0,9] = "F"
    board[9,0] = "F"
    board[9,9] = "F"

    i = 1
    j = 0
    f_count = 0
    for card in reversed(diamonds):
        if board[i,j] == "F":
            f_count += 1
            j += 1
        if f_count > 0:
            board[i,j] = card
            j += 1
        else:
            board[i,j] = card
            i += 1

    board_cards = spades + diamonds + clubs[::-1] + hearts[::-1] + spades + diamonds + clubs[::-1] + hearts[::-1]
    count = 0

    row, col = 0, 9

    for i in range(1,9):
        board[row+i, col] = board_cards[count]
        cur_row = row+i
        count += 1
    row = cur_row +1
    for i in range(1,9):
        board[row, col-i] = board_cards[count]
        cur_col = col-i
        count += 1
    col = cur_col -1
    for i in range(1,9):
        board[row-i, col] = board_cards[count]
        cur_row = row-i
        count += 1
    row = cur_row -1
    for i in range(1,9):
        board[row,col+i] = board_cards[count]
        cur_col = col+i
        count += 1
    col = cur_col
    row += 1
    lth = 8
    for _ in range(4):
        for i in range(lth):
            board[row+i, col] = board_cards[count]
            cur_row = row+i
            count += 1
        row = cur_row
        for i in range(1,lth):
            board[row, col-i] = board_cards[count]
            cur_col = col-i
            count += 1
        col = cur_col
        for i in range(1,lth):
            board[row-i, col] = board_cards[count]
            cur_row = row-i
            count += 1
        row = cur_row
        lth -= 1
        for i in range(1,lth):
            board[row,col+i] = board_cards[count]
            cur_col = col+i
            count += 1
        col = cur_col
        row += 1
        lth -= 1
    return board                  

board = make_board()

def make_empty_board():
    test_board = np.zeros((10,10))
    test_board[0,0] = 3
    test_board[9,0] = 3
    test_board[0,9] = 3
    test_board[9,9] = 3
    return test_board

def card_dict():
    dic = {}
    for card in cards:
        dic[card] = [(i,j,card) for i in range(10) for j in range(10) if board[i,j]==card]
    dic["DJ"] = [(i,j, "DJ") for i in range(10) for j in range(10)]
    dic["CJ"] = [(i,j, "CJ") for i in range(10) for j in range(10)]
    dic["HJ"] = []
    dic["SJ"] = []
    return dic

card_sqrs = card_dict()

def reverse_dict():
    dic = {}
    for i in range(10):
        for j in range(10):
            dic[(i,j)] = board[i,j]
    return dic

inv_card = reverse_dict()

def list_pos_pos(chip_board, number, card):
    listi = []
    for i in range(10):
        for j in range(10):
            if chip_board[i,j] == number:
                if number in [1,2] and not check_locked((i,j),chip_board, number):
                    listi.append((i,j,card))
                elif number == 0:
                    listi.append((i,j,card))
    return listi


def seq_points(chip_board):
    score_own = 0
    score_opp = 0
    own_points = 0
    opp_points = 0
    last_seq = 0
    for row in chip_board:
        if 1 not in row and 2 not in row:
            continue
        i_points_own = 0
        i_points_opp = 0
        i_score_own = 0
        i_score_opp = 0
        i_last_seq = 0
        for i in range(6):
            check = row[i:i+5]
            count_own = np.count_nonzero((check == 1) | (check == 3))
            count_opp = np.count_nonzero((check == 2) | (check == 3))
            if count_own > 1 and 2 not in check:
                if count_own == 5:
                    i_points_own = 100000
                    i_score_own = 1
                if count_own == 4:
                    i_points_own += 5000
                i_points_own += count_own*5
            elif count_opp > 1 and 1 not in check:
                if count_opp == 5:
                    i_points_opp = 1000000
                    i_score_opp = 1
                if count_opp == 4:
                    i_points_opp += 50000
                    i_last_seq += 100000
                i_points_opp += count_opp*5
        own_points += min(i_points_own, 100000)
        opp_points += min(i_points_opp, 1000000)
        score_own += i_score_own
        score_opp += i_score_opp 
        if i_points_opp < 1000000:
            last_seq += i_last_seq
    for idx in range(10):
        col = chip_board[:,idx]
        if 1 not in col and 2 not in col:
            continue
        i_points_own = 0
        i_points_opp = 0
        i_score_own = 0
        i_score_opp = 0
        i_last_seq = 0
        for i in range(6):
            check = col[i:i+5]
            count_own = np.count_nonzero((check == 1) | (check == 3))
            count_opp = np.count_nonzero((check == 2) | (check == 3))
            if count_own > 1 and 2 not in check:
                if count_own == 5:
                    i_points_own = 100000
                    i_score_own = 1
                if count_own == 4:
                    i_points_own += 5000
                i_points_own += count_own*5
            elif count_opp > 1 and 1 not in check:
                if count_opp == 5:
                    i_points_opp = 1000000
                    i_score_opp = 1
                if count_opp == 4:
                    i_points_opp += 50000
                    i_last_seq += 100000
                i_points_opp += count_opp*5
        own_points += min(i_points_own, 100000)
        opp_points += min(i_points_opp, 1000000)
        score_own += i_score_own
        score_opp += i_score_opp
        if i_points_opp < 1000000:
            last_seq += i_last_seq
    diags = []
    for i in range(6):
        diags.append(np.diagonal(chip_board[i:10,0:10-i]))
        if i != 0:
            diags.append(np.diagonal(chip_board[0:10-i,i:10]))
            diags.append(np.diagonal(np.fliplr(chip_board)[0:10-i,i:10]))
        diags.append(np.diagonal(np.fliplr(chip_board)[i:10,0:10-i]))
    for row in diags:
        if 1 not in row and 2 not in row:
            continue
        i_points_own = 0
        i_points_opp = 0
        i_score_own = 0
        i_score_opp = 0
        i_last_seq = 0
        for i in range(len(row)-4):
            check = row[i:i+5]
            count_own = np.count_nonzero((check == 1) | (check == 3))
            count_opp = np.count_nonzero((check == 2) | (check == 3))
            if count_own > 1 and 2 not in check:
                if count_own == 5:
                    i_points_own = 100000
                    i_score_own = 1
                if count_own == 4:
                    i_points_own += 5000
                i_points_own += count_own*5
            elif count_opp > 1 and 1 not in check:
                if count_opp == 5:
                    i_points_opp = 1000000
                    i_score_opp = 1
                if count_opp == 4:
                    i_points_opp += 50000
                    i_last_seq += 100000
                i_points_opp += count_opp*5
        own_points += min(i_points_own, 100000)
        opp_points += min(i_points_opp, 1000000)
        score_own += i_score_own
        score_opp += i_score_opp
        if i_points_opp < 1000000:
            last_seq += i_last_seq
    if score_opp == 1:
        opp_points += last_seq
    return own_points, opp_points, score_own, score_opp

def check_locked(pos, chip_board, number):
    l = 0
    r = 0
    u = 0
    d = 0
    for i in range(pos[1]):
        if chip_board[pos[0],pos[1]-1-i] in [number,3]:
            l += 1 
        else:
            break
    for i in range(9-pos[1]):
        if chip_board[pos[0],pos[1]+1+i] in [number,3]:
            r += 1 
        else:
            break
    for i in range(9-pos[0]):
        if chip_board[pos[0]+1+i,pos[1]] in [number,3]:
            d += 1 
        else:
            break
    for i in range(pos[0]):
        if chip_board[pos[0]-1-i,pos[1]] in [number,3]:
            u += 1 
        else:
            break
    if l+r >= 4 or d+u >= 4: #####CHECK########
        return True
    ul = 0
    dr = 0
    dl = 0
    ur = 0
    for i in range(min(pos[0], pos[1])):
        if chip_board[pos[0]-1-i,pos[1]-1-i] in [number,3]:
            ul += 1 
        else:
            break
    for i in range(min(9-pos[0], 9-pos[1])):
        if chip_board[pos[0]+1+i,pos[1]+1+i] in [number,3]:
            dr += 1 
        else:
            break
    for i in range(min(9-pos[0], pos[1])):
        if chip_board[pos[0]+1+i,pos[1]-1-i] in [number,3]:
            dl += 1 
        else:
            break
    for i in range(min(pos[0], 9-pos[1])):
        if chip_board[pos[0]-1-i,pos[1]+1+i] in [number,3]:
            ur += 1 
        else:
            break
    if ul+dr >= 4 or dl+ur >= 4:
        return True
    return False

def eval_pos(hand, chip_board, dict):
    real_hand = []
    add_jacks = 0
    rem_jack = 0
    for card in hand:
        if card in ["HJ","SJ"] and len(dict[card]) > 0 and rem_jack == 0:
            real_hand.append(card)
            get = real_hand[0], real_hand[-1]
            real_hand[-1], real_hand[0] = get
            rem_jack = 1
        elif card not in ["DJ", "CJ","HJ","SJ"]:
            real_hand.append(card)
        elif add_jacks == 0 and card in ["DJ", "CJ"]:
            real_hand.append(card)
            add_jacks = 1
    own_eval, opp_eval, own_score, opp_score = seq_points(chip_board)
    best_dif = -100000000000000000000
    if own_eval < 105000 and opp_eval < 1050000 and len(real_hand) > 3:
        pick_cards = [(dict[i[0]], dict[i[1]], dict[i[2]]) for i in itertools.combinations(real_hand,3)]
        for picks in pick_cards:
            combinations = list(itertools.product(*picks))
            for combi in combinations:
                cost = 0
                fail = 0
                old1 = chip_board[combi[0][:2]]
                old2 = chip_board[combi[1][:2]]
                old3 = chip_board[combi[2][:2]]
                for pos in combi:
                    if pos[2] in ["CJ","DJ"]:
                        if chip_board[pos[:2]] != 0:
                            fail = 1
                            break
                        chip_board[pos[:2]] = 1
                        cost += 30000
                    elif pos[2] in ["HJ","SJ"]:
                        if chip_board[pos[:2]] != 2 or check_locked(pos[:2],chip_board, 2):
                            fail = 1
                            break
                        chip_board[pos[:2]] = 0
                        cost += 15000
                    else:
                        if chip_board[pos[:2]] != 0:
                            fail = 1
                            break
                        chip_board[pos[:2]] = 1
                if fail == 1:
                    chip_board[combi[0][:2]] = old1
                    chip_board[combi[1][:2]] = old2
                    chip_board[combi[2][:2]] = old3
                    continue
                own_eval, opp_eval, own_score, opp_score = seq_points(chip_board)
                dif = own_eval - opp_eval - cost
                if dif >= best_dif:
                    best_dif = dif
                    best_dif_combi = combi
                for pos in combi:
                    if pos[2] in ["HJ","SJ"]:
                        chip_board[pos[:2]] = 2
                    else:
                        chip_board[pos[:2]] = 0
        if "HJ" in hand or "SJ" in hand:
            color = "H"
            if "SJ" in hand:
                color = "S"
            positions = dict["HJ"]
            squares = card_dict()
            for pos in positions:
                add_j = 0
                for card in hand:
                    check = 0
                    cost = 15000
                    if card in ["CJ","DJ"] and add_j == 0:
                        chip_board[pos[:2]] = 1
                        check = 1
                        add_j = 1
                        cost += 30000
                    elif card not in ["HJ","SJ"]:
                        for p in squares[card]:
                            if p[:2] == pos[:2]:
                                chip_board[pos[:2]] = 1
                                check = 1
                    if check == 1:
                        own_eval, opp_eval, own_score, opp_score = seq_points(chip_board)
                        dif = own_eval - opp_eval - cost
                        if dif >= best_dif:
                            best_dif = dif
                            best_dif_combi = [(pos[0],pos[1],color+"J")]
                        chip_board[pos[:2]] = 2            
        best_dif = -100000000000000000000
        for pos in best_dif_combi:
            cost = 0
            if pos[2] in ["CJ","DJ"]:
                if chip_board[pos[:2]] != 0:
                    continue
                chip_board[pos[:2]] = 1
                cost += 30000
            elif pos[2] in ["HJ","SJ"]:
                chip_board[pos[:2]] = 0
                cost += 15000
            else:
                if chip_board[pos[:2]] != 0:
                    continue
                chip_board[pos[:2]] = 1
            own_eval, opp_eval, own_score, opp_score = seq_points(chip_board)
            dif = own_eval - opp_eval - cost
            if dif >= best_dif:
                best_dif = dif
                best_dif_pos = pos
            if pos[2] in ["HJ","SJ"]:
                chip_board[pos[:2]] = 2
            else:
                chip_board[pos[:2]] = 0
    else:
        for card in real_hand:
            if card in ["CJ","DJ"]:
                for i in range(10):
                    for j in range(10):
                        if chip_board[i,j] == 0:
                            chip_board[i,j] = 1
                            own_eval, opp_eval, own_score, opp_score = seq_points(chip_board)
                            if own_score == 2:
                                return (i,j), inv_card[(i,j)], card
                            dif = own_eval - opp_eval - 30000
                            if dif >= best_dif:
                                best_dif = dif
                                best_dif_pos = (i,j,card)
                            chip_board[i,j] = 0
            elif card in ["HJ","SJ"]:
                for i in range(10):
                    for j in range(10):
                        if chip_board[i,j] == 2:
                            if check_locked((i,j),chip_board, 2):
                                continue
                            chip_board[i,j] = 0
                            own_eval, opp_eval, own_score, opp_score = seq_points(chip_board)
                            if own_score == 2:
                                return (i,j), inv_card[(i,j)], card
                            dif = own_eval - opp_eval - 15000
                            if dif >= best_dif:
                                best_dif = dif
                                best_dif_pos = (i,j,card)
                            chip_board[i,j] = 2 
            else:
                for pos in dict[card]:
                    if chip_board[pos[:2]] != 0:
                        continue
                    chip_board[pos[:2]] = 1
                    own_eval, opp_eval, own_score, opp_score = seq_points(chip_board)
                    if own_score == 2:
                        return pos[:2], inv_card[pos[:2]], pos[2]
                    dif = own_eval - opp_eval
                    if dif >= best_dif:
                        best_dif = dif
                        best_dif_pos = pos
                    chip_board[pos[:2]] = 0 
    return best_dif_pos[:2], inv_card[best_dif_pos[:2]], best_dif_pos[2]

def check_dead_card(card, chip_board):
    if card in ["DJ", "HJ", "SJ", "CJ"]:
        return False
    if chip_board[card_sqrs[card][0][:2]] != 0 and chip_board[card_sqrs[card][1][:2]] != 0:
        return True
    return False

def game():
    cards = make_cards()
    empty_board = make_empty_board()
    card_sqrs = card_dict()
    cards_w_j = cards + ["DJ","HJ","SJ","CJ"]
    
    hand = []
    print("Add the seven dealt cards.")
    i=1
    while i <= 7:
        intp = str(input(str(i)+": "))
        card = changeCaps(intp)
        if card not in cards_w_j:
            print("Invalid card. Try again.")
            continue
        hand.append(card)
        i += 1
    cor = 0
    while cor != "Y":
        cor = 0
        print("This is your cards:")
        for i,card in enumerate(hand):
            print(str(i+1)+": "+card)
        print("Is this correct?")
        while cor not in ["Y","1","2","3","4","5","6","7"]:
            intp = input("Type y for yes or a number [1,7] to change card: ")
            cor = changeCaps(intp)
            if cor not in ["Y","1","2","3","4","5","6","7"]:
                print("Invalid input. Try again.")
        if cor != "Y":
            int_cor = int(cor) -1
            print("You are changing this card: "+hand[int_cor])
            new_card = 0
            while new_card not in cards_w_j:
                intp = str(input("Add the right card: "))
                new_card = changeCaps(intp)
                if new_card not in cards_w_j:
                    print("Invalid card. Try again.")
            hand[int_cor] = new_card
    int_no = 0
    while int_no not in [1,2]:
        starting_player = input("Which player starts? 1 or 2: ")
        int_no = int(starting_player)
        if int_no not in [1,2]:
            print("Invalid input. Try again.")
    own_score, opp_score = 0, 0
    if int_no ==2:
        print("Player 2 starts.")
        start = 2
        i=0
        while i == 0:
            intp = str(input("Card played by player 2: "))
            card = changeCaps(intp)
            if card not in cards_w_j:
                print("Invalid card. Try again.")
                continue
            j=0
            while j == 0:
                confirm = input("Confirm that "+card+" is the correct card by typing y or n: ")
                if confirm not in ["y","n"]:
                    print("Invalid input. Try again.")
                    continue
                if confirm == "n":
                    j = 1
                elif confirm == "y":
                    break
            if j == 1:
                continue
            i = 1
        if card in ["DJ","CJ"]:
            i = 0
            while i == 0:
                intp = str(input("On which card on the board was the chip placed: "))
                card = changeCaps(intp)
                if card not in cards:
                    print("Invalid card. Try again.")
                    continue
                j=0
                while j == 0:
                    confirm = input("Confirm that "+card+" is the correct card by typing y or n: ")
                    if confirm not in ["y","n"]:
                        print("Invalid input. Try again.")
                        continue
                    if confirm == "n":
                        j = 1
                    elif confirm == "y":
                        break
                if j == 1:
                    continue    
                i = 1
        if card in cards:
            print("Which position on the board does the card have? (D6 has the postion R1 C2)")
            pos1 = (card_sqrs[card][0][1],9-card_sqrs[card][0][0])
            pos2 = (card_sqrs[card][1][1],9-card_sqrs[card][1][0])
            print("1: R"+str(pos1[0]+1)+" C"+str(pos1[1]+1))
            print("2: R"+str(pos2[0]+1)+" C"+str(pos2[1]+1))
            int_no = 0
            while int_no not in [1,2]:
                pick = input("Pick 1 or 2: ")
                int_no = int(pick)
                if int_no not in [1,2]:
                    print("Invalid input. Try again.")
            if int_no == 1:
                empty_board[card_sqrs[card][0][:2]] = 2
                for J in ["HJ","SJ"]:
                    card_sqrs[J] = list_pos_pos(empty_board, 2, J)
            else:
                empty_board[card_sqrs[card][1][:2]] = 2
                for J in ["HJ","SJ"]:
                    card_sqrs[J] = list_pos_pos(empty_board, 2, J)
    else:
        print("Player 1 starts.")
        start = 1
    while own_score <= 1 and opp_score <= 1:
        if start == 2:
            print("Player 1's turn.")
        start = 2    
        i = 0
        while i == 0:
            for idx, c in enumerate(hand):
                if check_dead_card(c, empty_board):
                    print("The card "+c+" is dead. Draw a new card.")
                    j = 0
                    while j == 0:
                        intp = str(input("New card: "))
                        card = changeCaps(intp)
                        if card not in cards_w_j:
                            print("Invalid card. Try again.")
                            continue
                        z=0
                        while z == 0:
                            confirm = input("Confirm that "+card+" is the correct card by typing y or n: ")
                            if confirm not in ["y","n"]:
                                print("Invalid input. Try again.")
                                continue
                            if confirm == "n":
                                z = 1
                            elif confirm == "y":
                                break
                        if z == 1:
                            continue
                        hand[idx] = card
                        i = 1
                        j = 1
                    break
            if i == 1:
                i = 0
            else:
                i = 1        
        pos, pos_card, card = eval_pos(hand, empty_board, card_sqrs)
        real_pos = (pos[1],9-pos[0])
        if card in ["HJ","SJ"]:
            print("Player 1 removes the chip on "+str(pos_card)+" R"+str(real_pos[0]+1)+" C"+str(real_pos[1]+1)+" with "+str(card))
            empty_board[pos] = 0
            for J in ["HJ","SJ"]:
                    card_sqrs[J] = list_pos_pos(empty_board, 2, J)
        else:
            print("Player 1 places a chip on "+str(pos_card)+" R"+str(real_pos[0]+1)+" C"+str(real_pos[1]+1)+" with "+str(card))
            empty_board[pos] = 1
        own_score = seq_points(empty_board)[2]
        if own_score >= 2:
            break
        print("Player 1 draws a new card.")
        for idx, c in enumerate(hand):
            if c == card:
                i = 0
                while i == 0:
                    intp = str(input("New card: "))
                    new_card = changeCaps(intp)
                    if new_card not in cards_w_j:
                        print("Invalid card. Try again.")
                        continue
                    j=0
                    while j == 0:
                        confirm = input("Confirm that "+new_card+" is the correct card by typing y or n: ")
                        if confirm not in ["y","n"]:
                            print("Invalid input. Try again.")
                            continue
                        if confirm == "n":
                            j = 1
                        elif confirm == "y":
                            break
                    if j == 1:
                        continue
                    hand[idx] = new_card
                    i = 1
                break
        print("Player 2's turn.")
        i=0
        while i == 0:
            intp = str(input("Card played by player 2: "))
            card = changeCaps(intp)
            if card not in cards_w_j:
                print("Invalid card. Try again.")
                continue
            j=0
            while j == 0:
                confirm = input("Confirm that "+card+" is the correct card by typing y or n: ")
                if confirm not in ["y","n"]:
                    print("Invalid input. Try again.")
                    continue
                if confirm == "n":
                    j = 1
                elif confirm == "y":
                    break
            if j == 1:
                continue
            i = 1
        if card in ["HJ","SJ"]:
            i = 0
            while i == 0:
                intp = str(input("On which card on the board was the removed chip placed: "))
                rem_card = changeCaps(intp)
                if rem_card not in cards:
                    print("Invalid card. Try again.")
                    continue
                j=0
                while j == 0:
                    confirm = input("Confirm that "+rem_card+" is the correct card by typing y or n: ")
                    if confirm not in ["y","n"]:
                        print("Invalid input. Try again.")
                        continue
                    if confirm == "n":
                        j = 1
                    elif confirm == "y":
                        break
                if j == 1:
                    continue
                i = 1
            print("Which position on the board did the card have? (D6 has the postion R1 C2)")
            pos1 = (card_sqrs[rem_card][0][1],9-card_sqrs[rem_card][0][0])
            pos2 = (card_sqrs[rem_card][1][1],9-card_sqrs[rem_card][1][0])
            print("1: R"+str(pos1[0]+1)+" C"+str(pos1[1]+1))
            print("2: R"+str(pos2[0]+1)+" C"+str(pos2[1]+1))
            int_no = 0
            while int_no not in [1,2]:
                pick = input("Pick 1 or 2: ")
                int_no = int(pick)
                if int_no not in [1,2]:
                    print("Invalid input. Try again.")
            if int_no == 1:
                empty_board[card_sqrs[rem_card][0][:2]] = 0
                for J in ["HJ","SJ"]:
                    card_sqrs[J] = list_pos_pos(empty_board, 2, J)
            else:
                empty_board[card_sqrs[rem_card][1][:2]] = 0
                for J in ["HJ","SJ"]:
                    card_sqrs[J] = list_pos_pos(empty_board, 2, J)
        elif card in ["DJ","CJ"]:
            i = 0
            while i == 0:
                intp = str(input("On which card on the board was the chip placed: "))
                card = changeCaps(intp)
                if card not in cards:
                    print("Invalid card. Try again.")
                    continue
                j=0
                while j == 0:
                    confirm = input("Confirm that "+card+" is the correct card by typing y or n: ")
                    if confirm not in ["y","n"]:
                        print("Invalid input. Try again.")
                        continue
                    if confirm == "n":
                        j = 1
                    elif confirm == "y":
                        break
                if j == 1:
                    continue
                i = 1
        if card in cards:
            print("Which position on the board does the card have? (D6 has the postion R1 C2)")
            pos1 = (card_sqrs[card][0][1],9-card_sqrs[card][0][0]) 
            pos2 = (card_sqrs[card][1][1],9-card_sqrs[card][1][0])
            print("1: R"+str(pos1[0]+1)+" C"+str(pos1[1]+1))
            print("2: R"+str(pos2[0]+1)+" C"+str(pos2[1]+1))
            int_no = 0
            while int_no not in [1,2]:
                pick = input("Pick 1 or 2: ")
                int_no = int(pick)
                if int_no not in [1,2]:
                    print("Invalid input. Try again.")
            if int_no == 1:
                empty_board[card_sqrs[card][0][:2]] = 2
                for J in ["HJ","SJ"]:
                    card_sqrs[J] = list_pos_pos(empty_board, 2, J)
            else:
                empty_board[card_sqrs[card][1][:2]] = 2
                for J in ["HJ","SJ"]:
                    card_sqrs[J] = list_pos_pos(empty_board, 2, J)
        opp_score = seq_points(empty_board)[3]
    if own_score >= 2:
        return print("Game is finished. Player 1 won.")
    else: 
        return print("Game is finished. Player 2 won.")



