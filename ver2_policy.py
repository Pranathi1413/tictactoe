import pygame
from pygame.locals import *
import numpy
import random

pygame.init()

screen_height = 300
screen_width = 300
line_width = 6
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Tic Tac Toe')

#define colours
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

#define font
font = pygame.font.SysFont(None, 40)

#define variables
clicked = False
player = 1
pos = (0,0)
markers = numpy.zeros((3,3), int)
game_over = False
winner = 0

PTF = numpy.zeros((3139, 9, 3139))
states = numpy.zeros((3139), int)
policy = numpy.zeros((3139), int)


#setup a rectangle for "Play Again" Option
again_rect = Rect(screen_width // 2 - 80, screen_height // 2, 160, 50)

#create empty 3 x 3 list to represent the grid
#for x in range (3):
 #       row = [0] * 3
  #      markers.append(row)



def draw_board():
        bg = (255, 255, 210)
        grid = (50, 50, 50)
        screen.fill(bg)
        for x in range(1,3):
                pygame.draw.line(screen, grid, (0, 100 * x), (screen_width,100 * x), line_width)
                pygame.draw.line(screen, grid, (100 * x, 0), (100 * x, screen_height), line_width)

def draw_markers():
        x_pos = 0
        for x in markers:
                y_pos = 0
                for y in x:
                        if y == 1:
                                pygame.draw.line(screen, red, (x_pos * 100 + 15, y_pos * 100 + 15), (x_pos * 100 + 85, y_pos * 100 + 85), line_width)
                                pygame.draw.line(screen, red, (x_pos * 100 + 85, y_pos * 100 + 15), (x_pos * 100 + 15, y_pos * 100 + 85), line_width)
                        if y == -1:
                                pygame.draw.circle(screen, green, (x_pos * 100 + 50, y_pos * 100 + 50), 38, line_width)
                        y_pos += 1
                x_pos += 1      


def check_game_over():
        global game_over
        global winner

        x_pos = 0
        for x in markers:
                #check columns
                if sum(x) == 3:
                        winner = 1
                        game_over = True
                if sum(x) == -3:
                        winner = 2
                        game_over = True
                #check rows
                if markers[0][x_pos] + markers [1][x_pos] + markers [2][x_pos] == 3:
                        winner = 1
                        game_over = True
                if markers[0][x_pos] + markers [1][x_pos] + markers [2][x_pos] == -3:
                        winner = 2
                        game_over = True
                x_pos += 1

        #check cross
        if markers[0][0] + markers[1][1] + markers [2][2] == 3 or markers[2][0] + markers[1][1] + markers [0][2] == 3:
                winner = 1
                game_over = True
        if markers[0][0] + markers[1][1] + markers [2][2] == -3 or markers[2][0] + markers[1][1] + markers [0][2] == -3:
                winner = 2
                game_over = True

        #check for tie
        if game_over == False:
                tie = True
                for row in markers:
                        for i in row:
                                if i == 0:
                                        tie = False
                #if it is a tie, then call game over and set winner to 0 (no one)
                if tie == True:
                        game_over = True
                        winner = 0



def draw_game_over(winner):

        if winner != 0:
                end_text = "Player " + str(winner) + " wins!"
        elif winner == 0:
                end_text = "You have tied!"

        end_img = font.render(end_text, True, blue)
        pygame.draw.rect(screen, green, (screen_width // 2 - 100, screen_height // 2 - 60, 200, 50))
        screen.blit(end_img, (screen_width // 2 - 100, screen_height // 2 - 50))

        again_text = 'Play Again?'
        again_img = font.render(again_text, True, blue)
        pygame.draw.rect(screen, green, again_rect)
        screen.blit(again_img, (screen_width // 2 - 80, screen_height // 2 + 10))

def mat_to_dec(mat):
        s = ""
        for i in range(3):
                for j in range(3):
                        s+=str(mat[i][j])
        return int(s,3)

def dec_to_mat(ind):
        s = numpy.base_repr(ind, 3)
        s = s.zfill(9)
        mat = numpy.zeros((3,3), int)
        c = 0
        for i in range(3):
                for j in range(3):
                        mat[i][j]=s[c]
                        c = c+1
        return mat

def dec_to_pos(dec):
        s = numpy.base_repr(dec, 3)
        s = s.zfill(2)
        x = int(s[0])
        y = int(s[1])
        return (x,y)

def pos_to_dec(pos):
        s = ""
        s+=str(pos[0])
        s+=str(pos[1])
        return int(s, 3)

def fill_prob():
        global states
        global PTF
        c = 0
        states[c] = 0
        c = c+1
        ind = 0        
        while(c < 3139):
                #print(ind)
                mat = dec_to_mat(states[ind])
                for i in range(9):
                        x,y = dec_to_pos(i)
                        #print(x, y)
                        if mat[x][y] == 0:
                                mat[x][y] = 1
                                for j in range(9):
                                        x1, y1 = dec_to_pos(j)
                                        if mat[x1][y1] == 0:
                                                mat[x1][y1] = 2
                                                #print(mat)
                                                dec = mat_to_dec(mat)
                                                if dec not in states:
                                                        #print(mat)
                                                        states[c] = dec
                                                        PTF[ind][i][c] = 1
                                                        c = c+1
                                                else:
                                                        index = numpy.where(states == dec)[0][0]
                                                        PTF[ind][i][index] = 1
                                                mat[x1][y1] = 0
                                mat[x][y] = 0
                ind = ind + 1
        for i in range(3139):
                for j in range(9):
                        s = numpy.count_nonzero(PTF[i][j]==1)
                        #print(s)
                        if s != 0:
                                PTF[i][j] = numpy.where(PTF[i][j]==1, PTF[i][j]/s, 0)
                                #psum = 0
                                #ind = 0
                                #for k in range(3139):
                                 #       if PTF[i][j][k] != 0:
                                  #              ind = k
                                   #             psum = psum + PTF[i][j][k]
                                #if psum < 1:
                                 #       PTF[i][j][ind] = PTF[i][j][ind] + 1 - psum


def make_policy():
        global policy
        for i in range(3139):
                mat = dec_to_mat(states[i])
                flag = 0
                while flag == 0:
                        posdec = random.randint(0, 8)
                        x,y = dec_to_pos(posdec)
                        if mat[x][y] == 0:
                                policy[i] = posdec
                                flag = 1
                        
        
#main loop
run = True
fill_prob()
make_policy()
while run:

        #draw board and markers first
        draw_board()
        draw_markers()
        num_act = 0
        
        #handle events
        for event in pygame.event.get():
                #handle game exit
                if event.type == pygame.QUIT:
                        run = False
                #run new game
                if game_over == False:
                        #check for mouseclick
                        if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
                                clicked = True
                        if event.type == pygame.MOUSEBUTTONUP and clicked == True:
                                clicked = False
                                if num_act < 4:
                                    markers[markers == -1] = 2
                                    istate = mat_to_dec(markers)
                                    istateind = numpy.where(states == istate)[0][0]
                                    posdec = policy[istateind]
                                    cell_x, cell_y = dec_to_pos(posdec)
                                    num_act = num_act + 1
                                    markers[cell_x][cell_y] = 1
                                    markers[markers == 2] = -1
                                    check_game_over()
                                    if game_over == True:
                                            pass
                                    else:
                                            action = pos_to_dec((cell_x, cell_y))
                                            #print(PTF[istateind][action])
                                            nstateind = numpy.random.choice(range(3139), 1, p=PTF[istateind][action])[0]
                                            nstate = states[nstateind]
                                            markers = dec_to_mat(nstate)
                                            markers[markers == 2] = -1
                                            check_game_over()
                                if num_act == 4:
                                    markers[markers == 0] = 1
                                    
                                        

        #check if game has been won
        if game_over == True:
                draw_game_over(winner)
                #check for mouseclick to see if we clicked on Play Again
                if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
                        clicked = True
                if event.type == pygame.MOUSEBUTTONUP and clicked == True:
                        clicked = False
                        pos = pygame.mouse.get_pos()
                        if again_rect.collidepoint(pos):
                                #reset variables
                                game_over = False
                                player = 1
                                pos = (0,0)
                                markers = numpy.zeros((3,3), int)
                                winner = 0
                                #create empty 3 x 3 list to represent the grid
                                

        #update display
        pygame.display.update()

pygame.quit()
