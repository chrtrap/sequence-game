import pygame
import os
import numpy as np
from sequence import *
import random
import time

# COLORS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (110, 110, 110)
GREEN = (0, 255, 0)
LIGHT_GREEN = (0, 120, 0)
DARK_GREEN = (0,100,0)
RED = (255, 0, 0)
LIGHT_RED = (120, 0, 0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
LIGHT_BLUE = (173,216,230)
DARK_BLUE = (0,0, 80)


cards = make_cards()

spades = cards[:12]
hearts = cards[12:24]
diamonds = cards[24:36]
clubs = cards[36:48]

cards_w_j = cards + ["HJ","SJ","CJ","DJ"]
deck = cards_w_j + cards_w_j          

board = make_board()

inv_card = reverse_dict()

def check_sqrs_card(card, board):
    dic = card_dict()
    listi = []
    for pos in dic[card]:
        if board[pos[:2]] == 0:
            listi.append(pos)
    return listi

def limit_add_jack_sqrs(board,J):
    listi = []
    for i in range(10):
        for j in range(10):
            if board[i,j] == 0:
                if check_locked((i,j), board, 1) or check_locked((i,j), board, 2):
                    listi.append((i,j,J))
    return listi


img_card_dict = {"A":"ace","K":"king", "Q": "queen", "J": "jack",
            "D":"diamonds","S":"spades","C":"clubs","H":"hearts","F":"F"}
for i in range(1,10):
    img_card_dict[str(i+1)] = i+1




WIDTH, HEIGHT = 1400, 750

pygame.font.init() 
myfont = pygame.font.SysFont('Calibri', 30)
textsurface = myfont.render('Played card:', False, WHITE)

FPS = 60


WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Sequence")


BOARD_IMAGE = pygame.image.load(os.path.join("PNG-cards-1.3","sequence_board_c.png"))
BOARD = pygame.transform.scale(BOARD_IMAGE,(1000,700))

LOGO_IMAGE = pygame.image.load(os.path.join("PNG-cards-1.3","seq_logo.png"))
LOGO = pygame.transform.scale(LOGO_IMAGE,(700,100))

def load_card_image(color, number, size):
    if size == "b":
        size = (140,200)
    else:
        size = (70,100)
    if color == "F":
        CARD_IMAGE = pygame.image.load(os.path.join("PNG-cards-1.3","black_joker.png"))
        CARD = pygame.transform.scale(CARD_IMAGE,size)
    else:
        CARD_IMAGE = pygame.image.load(os.path.join("PNG-cards-1.3",str(number)+"_of_"+str(color)+".png"))
        CARD = pygame.transform.scale(CARD_IMAGE,size)
    return CARD


def draw_hand(hand):
    no = 0
    col1 = 0
    col2 = 0
    for card in hand:
        if no <= 2:
            WIN.blit(load_card_image(img_card_dict[card[0]],img_card_dict[card[1:]],"b"),(1065,20+col1*110))
            col1 += 1
        elif no >= 3 and no <= 5:
            WIN.blit(load_card_image(img_card_dict[card[0]],img_card_dict[card[1:]],"b"),(1215,20+col2*110))
            col2 += 1
        else:
            WIN.blit(load_card_image(img_card_dict[card[0]],img_card_dict[card[1:]],"b"),(1140,-20+col2*110))
        no += 1
    pygame.display.update()

def draw_board(start_game, player_turn, mouse):
    large_font = pygame.font.Font(None, 50)
    title = pygame.font.Font(None, 80)
    WIN.fill(DARK_GREEN)
    played_button = large_font.render("Played card:", True, WHITE)
    played_button_rect = played_button.get_rect()
    played_button_rect.center = (1230,570)
    WIN.blit(played_button,played_button_rect)
    WIN.blit(BOARD,(20,20))
    if start_game == -1:
        pygame.draw.rect(WIN, LIGHT_GREEN, (350,187,700,375))
        WIN.blit(LOGO,(350,193))
        pygame.draw.rect(WIN, BLACK, (350,187,700,106),3)
        pygame.draw.rect(WIN, BLACK, (350,187,700,375),5)
        

        text_button = large_font.render("Player to start:", True, WHITE)
        text_button_rect = text_button.get_rect()
        text_button_rect.center = (700, 440)

        tit_button = title.render("Start Game", True, WHITE)
        tit_button_rect = tit_button.get_rect()
        tit_button_rect.center = (700, 350)

        com_button = large_font.render("Computer", True, WHITE)
        com_button_rect = com_button.get_rect()
        com_button_rect.center = (555, 500)
        
        pla_button = large_font.render("Player", True, WHITE)
        pla_button_rect = pla_button.get_rect()
        pla_button_rect.center = (845, 500)
        if 530 <= mouse[0] <= 530+340 and 300 <= mouse[1] <= 300+100: 
            pygame.draw.rect(WIN,LIGHT_RED,[530,300,340,100])
            pygame.draw.rect(WIN,BLACK,[530,300,340,100],2)  
        else: 
            pygame.draw.rect(WIN,RED,[530,300,340,100])
            pygame.draw.rect(WIN,BLACK,[530,300,340,100],2)
        if player_turn == 2: 
            pygame.draw.rect(WIN,GRAY,[460,470,190,60])
            pygame.draw.rect(WIN,BLACK,[460,470,190,60],2)  
        else: 
            pygame.draw.rect(WIN,GREEN,[460,470,190,60])
            pygame.draw.rect(WIN,BLACK,[460,470,190,60],2)
        if player_turn == 1: 
            pygame.draw.rect(WIN,GRAY,[750,470,190,60])
            pygame.draw.rect(WIN,BLACK,[750,470,190,60],2)  
        else: 
            pygame.draw.rect(WIN,GREEN,[750,470,190,60])
            pygame.draw.rect(WIN,BLACK,[750,470,190,60],2)
        WIN.blit(text_button,text_button_rect)
        WIN.blit(tit_button,tit_button_rect)
        WIN.blit(com_button, com_button_rect)
        WIN.blit(pla_button, pla_button_rect)
    if start_game == -2:
        pygame.draw.rect(WIN, LIGHT_GREEN, (350,187,700,375))
        WIN.blit(LOGO,(350,193))
        pygame.draw.rect(WIN, BLACK, (350,187,700,106),3)
        pygame.draw.rect(WIN, BLACK, (350,187,700,375),5)
        tit_button = title.render("Play Again", True, WHITE)
        tit_button_rect = tit_button.get_rect()
        tit_button_rect.center = (700, 350)

        if 530 <= mouse[0] <= 530+340 and 300 <= mouse[1] <= 300+100: 
            pygame.draw.rect(WIN,LIGHT_RED,[530,300,340,100])
            pygame.draw.rect(WIN,BLACK,[530,300,340,100],2)  
        else: 
            pygame.draw.rect(WIN,RED,[530,300,340,100])
            pygame.draw.rect(WIN,BLACK,[530,300,340,100],2)

        if player_turn == 2:
            text_button = large_font.render("Too bad! You lost!", True, WHITE)
        elif player_turn == 1:
            text_button = large_font.render("WOW! You won!", True, WHITE)
        text_button_rect = text_button.get_rect()
        text_button_rect.center = (700, 440)

        WIN.blit(tit_button,tit_button_rect)
        WIN.blit(text_button,text_button_rect)
    pygame.display.update()

def hand_mouse(mouse):
    if 1140 <= mouse[0] <= 1140+140 and 330-20 <= mouse[1] <= 330-20+200: 
        return 7
    elif 1075+140 <= mouse[0] <= 1075+140*2 and 20+110*2 <= mouse[1] <= 20+200+110*2: 
        return 6
    elif 1075+140 <= mouse[0] <= 1075+140*2 and 20+110 <= mouse[1] <= 20+200+110: 
        return 5
    elif 1075+140 <= mouse[0] <= 1075+140*2 and 20 <= mouse[1] <= 20+200: 
        return 4
    elif 1065 <= mouse[0] <= 1065+140 and 20+110*2 <= mouse[1] <= 20+200+110*2: 
        return 3
    elif 1065 <= mouse[0] <= 1065+140 and 20+110 <= mouse[1] <= 20+200+110: 
        return 2
    elif 1065 <= mouse[0] <= 1065+140 and 20 <= mouse[1] <= 20+200: 
        return 1
    else:
        return -1 #may be wrong?

def show_board_with_chips(chips,state, board):
    WIN.blit(BOARD,(20,20))
    for pos in chips:
        if pos[2] == 2:
            #pygame.draw.ellipse(WIN, LIGHT_GREEN, (20+100*pos[1],20+70*pos[0],100,70), 5)
            s = pygame.Surface((100,70))  # the size of your rect
            s.set_alpha(128)                # alpha level
            s.fill(LIGHT_GREEN)           # this fills the entire surface
            WIN.blit(s, (20+100*pos[1],20+70*pos[0])) 
        elif state != 1 or check_locked(pos[:2],board,1):
            if pos == chips[-1]:
                s = pygame.Surface((100,70))  # the size of your rect
                s.set_alpha(128)                # alpha level
                s.fill(DARK_BLUE)           # this fills the entire surface
                WIN.blit(s, (20+100*pos[1],20+70*pos[0])) 
            else:
                #pygame.draw.ellipse(WIN, BLUE, (20+100*pos[1],20+70*pos[0],100,70), 5)
                s = pygame.Surface((100,70))  # the size of your rect
                s.set_alpha(128)                # alpha level
                s.fill(BLUE)           # this fills the entire surface
                WIN.blit(s, (20+100*pos[1],20+70*pos[0])) 


def show_options(choice, hand, chips, dict, board):
    state = 0
    if hand[choice-1] in ["HJ","SJ"]:
        state = 1
    show_board_with_chips(chips,state, board)
    positions = []
    for pos in dict[hand[choice-1]]:
        if state == 1:
            if board[pos[:2]] == 1 and not check_locked(pos[:2], board, 1):
                #pygame.draw.ellipse(WIN, RED, (20+100*pos[1],20+70*pos[0],100,70), 5)
                s = pygame.Surface((100,70))  # the size of your rect
                s.set_alpha(128)                # alpha level
                s.fill(RED)           # this fills the entire surface
                WIN.blit(s, (20+100*pos[1],20+70*pos[0])) 
                positions.append(pos)
        elif board[pos[:2]] == 0:
            #pygame.draw.ellipse(WIN, YELLOW, (20+100*pos[1],20+70*pos[0],100,70), 5)
            s = pygame.Surface((100,70))  # the size of your rect
            s.set_alpha(128)                # alpha level
            s.fill(YELLOW)           # this fills the entire surface
            WIN.blit(s, (20+100*pos[1],20+70*pos[0])) 
            positions.append(pos)
    return positions

def place_chip(mouse, pos, chips, empty_board, com_dict, hand, deck):
    for opt in pos:
        if 20+100*opt[1] <= mouse[0] <= 20+100*opt[1]+100 and 20+70*opt[0] <= mouse[1] <= 20+70*opt[0]+70:
            played_card = inv_card[opt[:2]]
            if opt[2] in ["HJ", "SJ"]:
                for i, chip in enumerate(chips):
                    if chip[:2] == opt[:2]:
                        chips.pop(i)
                        break
                empty_board[opt[0],opt[1]] = 0
            else:
                chips.append((opt[0],opt[1],2))
                empty_board[opt[0],opt[1]] = 2
                com_dict["HJ"] = list_pos_pos(empty_board, 2, "HJ")
                com_dict["SJ"] = list_pos_pos(empty_board, 2, "SJ")
            com_dict[played_card] = check_sqrs_card(played_card, empty_board)
            com_dict["DJ"] = limit_add_jack_sqrs(empty_board, "DJ")
            com_dict["CJ"] = limit_add_jack_sqrs(empty_board, "CJ")
            for i,card in enumerate(hand):
                if card == opt[2]:
                    hand[i] = deck.pop(0)
                    hand[-1], hand[i] = hand[i], hand[-1]
                    break
            show_board_with_chips(chips,0,empty_board)
            return True
def main():
    run = True
    start_game = -1
    player_turn = 1
    while run:
        mouse = pygame.mouse.get_pos()
        if start_game == -2:
            draw_board(start_game, player_turn, mouse)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if 530 <= mouse[0] <= 530+340 and 300 <= mouse[1] <= 300+100: 
                        start_game = -1
        if start_game == -1:
            draw_board(start_game,player_turn, mouse)
            empty_board = make_empty_board()
            com_dict = card_dict()
            com_dict["DJ"] = limit_add_jack_sqrs(empty_board, "DJ")
            com_dict["CJ"] = limit_add_jack_sqrs(empty_board, "CJ")
            player_dict = card_dict()
            player_dict["HJ"] = [(i,j,"HJ") for i in range(10) for j in range(10)]
            player_dict["SJ"] = [(i,j,"SJ") for i in range(10) for j in range(10)]
            chips = []
            choice = -2
            playing_deck = deck
            random.shuffle(playing_deck)
            com_hand = playing_deck[:7]
            playing_deck = playing_deck[7:]
            player_hand = playing_deck[:7]
            playing_deck = playing_deck[7:]
            mouse = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if 530 <= mouse[0] <= 530+340 and 300 <= mouse[1] <= 300+100: 
                        start_game = 0
                    if 460 <= mouse[0] <= 460+190 and 470 <= mouse[1] <= 470+60: 
                        player_turn = 1
                    if 750 <= mouse[0] <= 750+190 and 470 <= mouse[1] <= 470+60: 
                        player_turn = 2
        if start_game == 0:
            start_game = 1
            draw_board(start_game,player_turn,mouse)
            draw_hand(player_hand)
        if start_game == 1 and player_turn == 2:
            for i, c in enumerate(player_hand):
                if check_dead_card(c, empty_board):
                    player_hand[i] = playing_deck.pop(0)
                    break
            draw_hand(player_hand)
            mouse = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if player_turn == 2:
                        if choice == -2:
                            pos = []
                        choice = hand_mouse(mouse)
                        if choice in [i for i in range(1,8)]:
                            pos = show_options(choice, player_hand, chips, player_dict, empty_board)
                        if place_chip(mouse, pos, chips, empty_board, com_dict, player_hand, playing_deck):
                            com_score, player_score, com_points, player_points = seq_points(empty_board)
                            if com_points >= 2 or player_points >= 2:
                                start_game = -2
                            draw_hand(player_hand)
                            player_turn = 1
        if start_game == 1 and player_turn == 1:
            for i, c in enumerate(com_hand):
                if check_dead_card(c, empty_board):
                    com_hand[i] = playing_deck.pop(0)
                    break
            pos, played_card, real_card = eval_pos(com_hand,empty_board, com_dict)
            time.sleep(1) #######################################################
            if real_card not in ["HJ","SJ"]:
                chips.append((pos[0],pos[1],1))
                empty_board[pos[0],pos[1]] = 1
            else:
                for i, chip in enumerate(chips):
                    if chip[:2] == pos:
                        chips.pop(i)
                        break
                empty_board[pos[0],pos[1]] = 0
                com_dict["HJ"] = list_pos_pos(empty_board, 2, "HJ")
                com_dict["SJ"] = list_pos_pos(empty_board, 2, "SJ")
            com_dict[played_card] = check_sqrs_card(played_card, empty_board)
            com_dict["DJ"] = limit_add_jack_sqrs(empty_board, "DJ")
            com_dict["CJ"] = limit_add_jack_sqrs(empty_board, "CJ")
            for i,card in enumerate(com_hand):
                if card == real_card:
                    com_hand[i] = playing_deck.pop(0)
                    break
            WIN.blit(load_card_image(img_card_dict[real_card[0]],img_card_dict[real_card[1:]],"s"),(1190,600))
            show_board_with_chips(chips,0, empty_board)
            com_score, player_score, com_points, player_points = seq_points(empty_board)
            if com_points >= 2 or player_points >= 2:
                start_game = -2
            player_turn = 2
            choice = -2
    pygame.quit()


if __name__ == "__main__":
    main()