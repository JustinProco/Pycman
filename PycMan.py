import pygame
import os
import random
pygame.init()
pygame.mixer.init() #Used for handling sounds

pygame.display.set_caption("Pycman")
FPS = 150   #Changes the speed the game runs at: Can be adjusted
PACMAN_VELOCITY = 1 #Pixles
################################
FRAME_COUNT = 1     #Counts the number of frames that have passed since the program was launched. Will be used as a timer
VULNERABLE_GHOSTS = 0  #will track if the ghosts should be vulnerable or not. 0 for false, 1 for true
VULNERABLE_TIMER = -5000 #tracks what frame the ghosts became vulnerable at, will occurr when a super pellet has been consumed


RED_PRISON_TIMER = -5000
RED_IN_PRISON = 0  #0 if it is not in prison. 1 if it is

BLUE_PRISON_TIMER = -5000
BLUE_IN_PRISON = 0  #0 if it is not in prison. 1 if it is

PINK_PRISON_TIMER = -5000
PINK_IN_PRISON = 0  #0 if it is not in prison. 1 if it is

YELLOW_PRISON_TIMER = -5000
YELLOW_IN_PRISON = 0  #0 if it is not in prison. 1 if it is
################################

PACMAN_WIDTH = 41
PACMAN_HEIGHT = 41
PELLET_WIDTH = 7
PELLET_HEIGHT = 7
SUPER_PELLET_WIDTH = 21
SUPER_PELLET_HEIGHT = 21
MAP_ARRAY = [[0 for i in range(761)] for j in range(761)] #Underlying map that contains the track
PELLET_ARRAY = [[0 for i in range(27)] for j in range(30)] #Map that holds the locations of all the pellets

PELLET_X_LIST = [0]
PELLET_Y_LIST = [0]
SUPER_PELLET_X_LIST = [0]
SUPER_PELLET_Y_LIST = [0]



PACMAN_GFPF = 15 #Constant, number of game-frames per Pacman-frame
PACMAN_GIF = {
    0: "PcM_fr0.png",
    1: "PcM_fr3.png"
}

"""
#Probabbly won't need
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
BLUE = (0,0,255)
ORANGE = (255,165,0)
"""

global MAP_IMAGE
global PACMAN_SPAWN_X
global PACMAN_SPAWN_Y
global movement_direction
lives = 2
PELLET_IMAGE = pygame.image.load(os.path.join('Assets', 'Pellet.png'))
SUPER_PELLET_IMAGE = pygame.image.load(os.path.join('Assets', 'Super Pellet.png'))
PELLET_TOKEN = pygame.transform.scale(PELLET_IMAGE, (PELLET_WIDTH, PELLET_HEIGHT))
SUPER_PELLET_TOKEN = pygame.transform.scale(SUPER_PELLET_IMAGE, (SUPER_PELLET_WIDTH, SUPER_PELLET_HEIGHT))

#images for enemy ghosts
GHOST_RED_IMAGE = pygame.image.load(os.path.join('Assets', 'red_ghost.png'))
GHOST_YELLOW_IMAGE = pygame.image.load(os.path.join('Assets', 'yellow_ghost.png'))
GHOST_PINK_IMAGE = pygame.image.load(os.path.join('Assets', 'pink_ghost.png'))
GHOST_BLUE_IMAGE = pygame.image.load(os.path.join('Assets', 'blue_ghost.png'))
GHOST_VULNERABLE_IMAGE = pygame.image.load(os.path.join('Assets', 'vulnerable_ghost.png'))

GAME_OVER_IMAGE = pygame.image.load(os.path.join('Assets', 'Game Over.png'))


#create the tokens for the ghosts
RED_GHOST_TOKEN = pygame.transform.scale(GHOST_RED_IMAGE, (PACMAN_WIDTH-4, PACMAN_HEIGHT-4))  #Scale the image to 100x100 and be the same size as pacman
YELLOW_GHOST_TOKEN = pygame.transform.scale(GHOST_YELLOW_IMAGE, (PACMAN_WIDTH-4, PACMAN_HEIGHT-4))  #Scale the image to 100x100 and be the same size as pacman
PINK_GHOST_TOKEN = pygame.transform.scale(GHOST_PINK_IMAGE, (PACMAN_WIDTH-4, PACMAN_HEIGHT-4))  #Scale the image to 100x100 and be the same size as pacman
BLUE_GHOST_TOKEN = pygame.transform.scale(GHOST_BLUE_IMAGE, (PACMAN_WIDTH-4, PACMAN_HEIGHT-4))  #Scale the image to 100x100 and be the same size as pacman
GHOST_VULNERABLE_TOKEN_1 = pygame.transform.scale(GHOST_VULNERABLE_IMAGE, (PACMAN_WIDTH-4, PACMAN_HEIGHT-4))  #Scale the image to 100x100 and be the same size as pacman

#game over screen image
GAME_OVER = pygame.transform.scale(GAME_OVER_IMAGE, (780, 900))




#variables to track ghost movement
red_movement_block = "none"     #contains the direction of the movement of where the red ghost is being blocked or stops the red ghost from looping in one corner or moving back and forth
red_last_move = "none"      #contains the direction of the last move of the ghost
red_num_of_moves = 0        #contains the number of moves taken by the red ghost

pink_movement_block = "none"     #contains the direction of the movement of where the pink ghost is being blocked or stops the pink ghost from looping in one corner or moving back and forth
pink_last_move = "none"      #contains the direction of the last move of the ghost
pink_num_of_moves = 0        #contains the number of moves taken by the pink ghost. Increments every frame

yellow_movement_block = "none"     #contains the direction of the movement of where the yellow ghost is being blocked or stops the yellow ghost from looping in one corner or moving back and forth
yellow_last_move = "none"      #contains the direction of the last move of the ghost
yellow_num_of_moves = 0        #contains the number of moves taken by the yellow ghost. Increments every frame

blue_movement_block = "none"     #contains the direction of the movement of where the blue ghost is being blocked or stops the blue ghost from looping in one corner or moving back and forth
blue_last_move = "none"      #contains the direction of the last move of the ghost
blue_num_of_moves = 0        #contains the number of moves taken by the blue ghost. Increments every frame


#sound effects and music #.wav files for sound effects, mp3 or wav for music that will play throughout the entire game
death_sound = pygame.mixer.Sound(os.path.join('Assets', 'death_sound.wav'))
starting_theme = pygame.mixer.Sound(os.path.join('Assets', 'starting_theme.wav'))
movement_sound = pygame.mixer.Sound(os.path.join('Assets', 'movement_sound.wav'))




def initiate_map_1():
    global PELLET_X_LIST
    global PELLET_Y_LIST
    global SUPER_PELLET_X_LIST
    global SUPER_PELLET_Y_LIST
    global MAP_ARRAY
    global PACMAN_SPAWN_X
    global PACMAN_SPAWN_Y
    global MAP_IMAGE
    MAP_ARRAY = [[0 for i in range(761)] for j in range(761)] #reset from previous run
    PELLET_ARRAY = [[0 for i in range(27)] for j in range(30)] #reset from previous run
    PACMAN_SPAWN_X = 345
    PACMAN_SPAWN_Y = 590
    MAP_IMAGE = pygame.image.load(os.path.join('Assets', 'Map.png')).convert()
    #Horizontal paths, all chanels are 47 pixles wide/tall, meaning 24 is the center pixle
    #1 @24
    for x in range(24,307+1):
        MAP_ARRAY[x][24] = 1
    #2 @127
    for x in range(24,667+1):
        MAP_ARRAY[x][127] = 1
    #3 @204
    for x in range(24,152+1):
        MAP_ARRAY[x][204] = 1
    #4 @358
    for x in range(0,229+1):    #teleportation path
        MAP_ARRAY[x][358] = 1
    #5 @512
    for x in range(24,307+1):
        MAP_ARRAY[x][512] = 1
    #6 @590
    for x in range(24,75+1):
        MAP_ARRAY[x][590] = 1
    #7 @667
    for x in range(24,152+1):
        MAP_ARRAY[x][667] = 1
    #8 @744
    for x in range(24,667+1):
        MAP_ARRAY[x][744] = 1
    #9 @204
    for x in range(229,307+1):
        MAP_ARRAY[x][204] = 1
    #10 @281
    for x in range(229,461+1):
        MAP_ARRAY[x][281] = 1
    #11 @435
    for x in range(229,461+1):
        MAP_ARRAY[x][435] = 1
    #12 @590
    for x in range(152,538+1):
        MAP_ARRAY[x][590] = 1
    #13 @667
    for x in range(229,307+1):
        MAP_ARRAY[x][667] = 1
    #14 @24
    for x in range(384,667+1):
        MAP_ARRAY[x][24] = 1
    #15 @204
    for x in range(384,461+1):
        MAP_ARRAY[x][204] = 1
    #16 @512
    for x in range(384,667+1):
        MAP_ARRAY[x][512] = 1
    #17 @667
    for x in range(384,461+1):
        MAP_ARRAY[x][667] = 1
    #18 @204
    for x in range(538,667+1):
        MAP_ARRAY[x][204] = 1
    #19 @358
    for x in range(461,690+1):  #teleportaion path
        MAP_ARRAY[x][358] = 1
    #20 @590
    for x in range(616,667+1):
        MAP_ARRAY[x][590] = 1
    #21 @667
    for x in range(538,667+1):
        MAP_ARRAY[x][667] = 1

    #Vertical paths
    #1 @24
    for y in range(24,204+1):
        MAP_ARRAY[24][y] = 1
    #2 @152
    for y in range(24,667+1):
        MAP_ARRAY[152][y] = 1
    #3 @307
    for y in range(24,127+1):
        MAP_ARRAY[307][y] = 1
    #4 @384
    for y in range(24,127+1):
        MAP_ARRAY[384][y] = 1
    #5 @538
    for y in range(24,667+1):
        MAP_ARRAY[538][y] = 1
    #6 @667
    for y in range(24,204+1):
        MAP_ARRAY[667][y] = 1
    #7 @229
    for y in range(127,204+1):
        MAP_ARRAY[229][y] = 1
    #8 @461
    for y in range(127,204+1):
        MAP_ARRAY[461][y] = 1
    #9 @307
    for y in range(204,281+1):
        MAP_ARRAY[307][y] = 1
    #10 @384
    for y in range(204,281+1):
        MAP_ARRAY[384][y] = 1
    #11 @229
    for y in range(281,512+1):
        MAP_ARRAY[229][y] = 1
    #12 @461
    for y in range(281,512+1):
        MAP_ARRAY[461][y] = 1
    #13 @24
    for y in range(512,590+1):
        MAP_ARRAY[24][y] = 1
    #14 @307
    for y in range(512,590+1):
        MAP_ARRAY[307][y] = 1
    #15 @384
    for y in range(512,590+1):
        MAP_ARRAY[384][y] = 1
    #16 @667
    for y in range(512,590+1):
        MAP_ARRAY[667][y] = 1
    #17 @75
    for y in range(590,667+1):
        MAP_ARRAY[75][y] = 1
    #18 @229
    for y in range(590,667+1):
        MAP_ARRAY[229][y] = 1
    #19 @461
    for y in range(590,667+1):
        MAP_ARRAY[461][y] = 1
    #20 @616
    for y in range(590,667+1):
        MAP_ARRAY[616][y] = 1
    #21 @24
    for y in range(667,744+1):
        MAP_ARRAY[24][y] = 1
    #22 @307
    for y in range(667,744+1):
        MAP_ARRAY[307][y] = 1
    #23 @384
    for y in range(667,744+1):
        MAP_ARRAY[384][y] = 1
    #24 @667
    for y in range(667,744+1):
        MAP_ARRAY[667][y] = 1
    PELLET_X_LIST = [24, 50, 75, 101, 126, 152, 178, 203, 229, 255, 281, 307, 332, 358, 384, 409, 435, 461, 486, 512, 538, 564, 590, 616, 641, 667]
    PELLET_Y_LIST = [24, 50, 76, 101, 127, 152, 178, 204, 229, 255, 281, 306, 332, 358, 383, 409, 435, 460, 486, 512, 538, 564, 590, 615, 641, 667, 692, 718, 744]
    #The x and y list hold the column/row pixle numbers for each possible pellet.
    #This means we check a 26x29 array rather than the 761x761 map array for a pellet.
    SUPER_PELLET_X_LIST = [24, 667] #These few Super pellets can be done manually,
    SUPER_PELLET_Y_LIST = [76, 590] #i'm just doing them like this for consistancy
    
    #Places the pellets on the map so they can be detected by the moving Pacman character
    for i in PELLET_X_LIST:
        for j in PELLET_Y_LIST:
            if MAP_ARRAY[i][j] == 1: #Only places a pellet on the map if it intersects with the laid out track of 1's
                MAP_ARRAY[i][j] = 2
                
    for i in SUPER_PELLET_X_LIST:
        for j in SUPER_PELLET_Y_LIST:
            MAP_ARRAY[i][j] = 3 #Inserts the super pellets on the map. Should overwrite the regular pellets if laid out correctly





def initiate_map_2():
    global PELLET_X_LIST
    global PELLET_Y_LIST
    global SUPER_PELLET_X_LIST
    global SUPER_PELLET_Y_LIST
    global MAP_ARRAY
    global PACMAN_SPAWN_X
    global PACMAN_SPAWN_Y
    global MAP_IMAGE
    MAP_ARRAY = [[0 for i in range(761)] for j in range(761)] #reset from previous run
    PELLET_ARRAY = [[0 for i in range(27)] for j in range(30)] #reset from previous run
    PACMAN_SPAWN_X = 345
    PACMAN_SPAWN_Y = 435
    MAP_IMAGE = pygame.image.load(os.path.join('Assets', 'Map2.png')).convert()
    #Horizontal paths
    #1 @ 24
    for x in range(24,667+1):
        MAP_ARRAY[x][24] = 1
    #2 @ 101
    for x in range(101, 256+1):
        MAP_ARRAY[x][101] = 1
    #3 @ 127
    for x in range(24,101+1):
        MAP_ARRAY[x][127] = 1
    #4 @ 152
    for x in range(333, 410+1):
        MAP_ARRAY[x][152] = 1
    #5 @ 178 
    for x in range(101, 152+1):
        MAP_ARRAY[x][178] = 1
    #6 @ 178
    for x in range(230, 256+1):
        MAP_ARRAY[x][178] = 1
    #7 @ 178
    for x in range(410, 461+1):
        MAP_ARRAY[x][178] = 1
    #8 @ 178
    for x in range(539, 590+1):
        MAP_ARRAY[x][178] = 1
    #9 @ 255
    for x in range(24, 667+1):
        MAP_ARRAY[x][255] = 1
    #10 @ 281
    for x in range(333, 358+1):
        MAP_ARRAY[x][281] = 1

    #11 @ 358			#Teleportation path
    for x in range(0, 152+1):
        MAP_ARRAY[x][358] = 1
    #12 @ 358			# Teleportation path
    for x in range(539, 690+1):
        MAP_ARRAY[x][358] = 1
        
    #13 @ 435
    for x in range(230, 461+1):
        MAP_ARRAY[x][435] = 1
    #14 @ 487
    for x in range(152, 539+1):
        MAP_ARRAY[x][487] = 1
    #15 @ 512
    for x in range(24, 178+1):
        MAP_ARRAY[x][512] = 1
    #16 @ 512
    for x in range(539, 667+1):
        MAP_ARRAY[x][512] = 1
    #17 @ 564
    for x in range(178, 307+1):
        MAP_ARRAY[x][564] = 1
    #18 @ 564
    for x in range(384, 410+1):
        MAP_ARRAY[x][564] = 1
    #19 @ 589
    for x in range(256, 307+1):
        MAP_ARRAY[x][589] = 1
    #20 @ 589
    for x in range(487, 590+1):
        MAP_ARRAY[x][589] = 1
    #21 @ 641
    for x in range(24, 178+1):
        MAP_ARRAY[x][641] = 1
    #22 @ 641
    for x in range(307, 487+1):
        MAP_ARRAY[x][641] = 1
    #23 @ 666
    for x in range(256, 307+1):
        MAP_ARRAY[x][666] = 1
    #24 @ 666
    for x in range(564, 590+1):
        MAP_ARRAY[x][666] = 1
    #25 @ 744
    for x in range(24, 384+1):
        MAP_ARRAY[x][744] = 1
    #26 @ 744
    for x in range(487, 667+1):
        MAP_ARRAY[x][744] = 1

    #Vertical paths
    #1 @24
    for y in range(24,255+1):
        MAP_ARRAY[24][y] = 1
    #2 @24
    for y in range(512, 744+1):
        MAP_ARRAY[24][y] = 1
    #3 @101
    for y in range(101, 178+1):
        MAP_ARRAY[101][y] = 1
    #4 @101
    for y in range(589, 666+1):
        MAP_ARRAY[101][y] = 1
    #5 @152
    for y in range(24, 512+1):
        MAP_ARRAY[152][y] = 1
    #6 @178
    for y in range(487, 744+1):
        MAP_ARRAY[178][y] = 1
    #7 @204
    for y in range(24, 101+1):
        MAP_ARRAY[204][y] = 1
    #8 @230
    for y in range(178, 487+1):
        MAP_ARRAY[230][y] = 1
    #9 @256
    for y in range(101, 178+1):
        MAP_ARRAY[256][y] = 1
    #10 @256
    for y in range(564, 589+1):
        MAP_ARRAY[256][y] = 1
    #11 @256
    for y in range(666, 744+1):
        MAP_ARRAY[256][y] = 1
    #12 @281
    for y in range(564, 589+1):
        MAP_ARRAY[281][y] = 1
    #13 @307
    for y in range(487, 744+1):
        MAP_ARRAY[307][y] = 1
    #14 @333
    for y in range(24,281+1):
        MAP_ARRAY[333][y] = 1
    #15 @358
    for y in range(255, 281+1):
        MAP_ARRAY[358][y] = 1
    #16 @384
    for y in range(487, 744+1):
        MAP_ARRAY[384][y] = 1
    #17 @410
    for y in range(24,178+1):
        MAP_ARRAY[410][y] = 1
    #18 @461
    for y in range(24, 487+1):
        MAP_ARRAY[461][y] = 1
    #19 @487
    for y in range(487, 744+1):
        MAP_ARRAY[487][y] = 1
    #20 @539
    for y in range(24, 178+1):
        MAP_ARRAY[539][y] = 1
    #21 @539
    for y in range(255, 589+1):
        MAP_ARRAY[539][y] = 1
    #22 @564
    for y in range(178, 255+1):
        MAP_ARRAY[564][y] = 1
    #23 @564
    for y in range(666, 744+1):
        MAP_ARRAY[564][y] = 1
    #24 @590
    for y in range(24, 178+1):
        MAP_ARRAY[590][y] = 1
    #25 @590
    for y in range(589, 666+1):
        MAP_ARRAY[590][y] = 1
    #26 @667
    for y in range(24, 255+1):
        MAP_ARRAY[667][y] = 1
    #27 @667
    for y in range(512, 744+1):
        MAP_ARRAY[667][y] = 1
    PELLET_X_LIST = [24, 50, 75, 101, 126, 152, 178, 204, 230, 256, 281, 307, 333, 358, 384, 410, 435, 461, 487, 512, 539, 564, 590, 616, 641, 667]
    PELLET_Y_LIST = [24, 50, 76, 101, 127, 152, 178, 204, 229, 255, 281, 306, 332, 358, 383, 409, 435, 460, 487, 512, 538, 564, 589, 615, 641, 666, 692, 718, 744]
    #The x and y list hold the column/row pixle numbers for each possible pellet.
    #This means we check a 26x29 array rather than the 761x761 map array for a pellet.
    #Places the pellets on the map so they can be detected by the moving Pacman character
    for i in PELLET_X_LIST:
        for j in PELLET_Y_LIST:
            if MAP_ARRAY[i][j] == 1: #Only places a pellet on the map if it intersects with the laid out track of 1's
                MAP_ARRAY[i][j] = 2
                
    MAP_ARRAY[101][589] = 3 #Inserts the super pellets on the map. Should overwrite the regular pellets if laid out correctly                
    MAP_ARRAY[256][178] = 3 #Inserts the super pellets on the map. Should overwrite the regular pellets if laid out correctly                
    MAP_ARRAY[667][255] = 3 #Inserts the super pellets on the map. Should overwrite the regular pellets if laid out correctly                
    MAP_ARRAY[667][666] = 3 #Inserts the super pellets on the map. Should overwrite the regular pellets if laid out correctly












#ghost movement



#
# Move the red ghost based on the screen and detect if there is a collision with the player
# The movement is "random" based on the amount of frames the ghost has been on the screen
# Every frame increments the (GHOST COLOR)_num_of_moves Based on the value of that it will move in different directions
# Before making a move it will look to see if the move is possible, if not it will look to the next possible move
# It records the previous move so that it cannot get stuck moving between left and right or up and down.
# Once it moves up it is unable to move down, and can only go left or right. Then it will reevaluate all possible moves on the next frame
#
def move_blue_ghost(player, blue_ghost, red_ghost, yellow_ghost, pink_ghost):
    global movement_block
    global blue_last_move
    global blue_num_of_moves
    global lives
    global movement_direction
    global VULNERABLE_GHOSTS


    #########################
    global FRAME_COUNT
    global BLUE_PRISON_TIMER
    global BLUE_IN_PRISON

    randReleaseTimer = 0
    #########################


    #######################HANDLES GHOST TELEPORTING#######################################################
    if blue_ghost.x == 0 and blue_ghost.y == 358:   #handles teleporting from side to side
        blue_ghost.x = 690

    if blue_ghost.x == 689 and blue_ghost.y == 358: #handles teleporting from side to side
        blue_ghost.x = 0
    #######################HANDLES GHOST TELEPORTING#####################################################

    if blue_num_of_moves % 3 == 0:
        if blue_last_move != "up" and MAP_ARRAY[blue_ghost.x][blue_ghost.y+1] != 0:      #moving down
            blue_ghost.y = blue_ghost.y+1
            blue_last_move = "down"
            blue_num_of_moves +=1

        elif blue_last_move != "right" and MAP_ARRAY[blue_ghost.x-1][blue_ghost.y] != 0:    #moving left
            blue_ghost.x = blue_ghost.x-1
            blue_last_move = "left"
            blue_num_of_moves +=1

        elif blue_last_move != "down" and MAP_ARRAY[blue_ghost.x][blue_ghost.y-1] != 0:    #moving up
            blue_ghost.y = blue_ghost.y-1
            blue_last_move = "up"
            blue_num_of_moves +=1
        
        elif blue_last_move != "left" and MAP_ARRAY[blue_ghost.x+1][blue_ghost.y] != 0:    #moving right
            blue_ghost.x = blue_ghost.x+1
            blue_last_move = "right"
            blue_num_of_moves +=1
            
    elif blue_num_of_moves %2 == 0:
        if blue_last_move != "left" and MAP_ARRAY[blue_ghost.x+1][blue_ghost.y] != 0:    #moving right
            blue_ghost.x = blue_ghost.x+1
            blue_last_move = "right"
            blue_num_of_moves +=2
            
        elif blue_last_move != "down" and MAP_ARRAY[blue_ghost.x][blue_ghost.y-1] != 0:    #moving up
            blue_ghost.y = blue_ghost.y-1
            blue_last_move = "up"
            blue_num_of_moves +=1

        #elif blue_last_move != "right" and MAP_ARRAY[blue_ghost.x-1][blue_ghost.y] != 0:    #moving left
            #blue_ghost.x = blue_ghost.x-1
            #blue_last_move = "left"
            #blue_num_of_moves +=2

        elif blue_last_move != "up" and MAP_ARRAY[blue_ghost.x][blue_ghost.y+1] != 0:      #moving down
            blue_ghost.y = blue_ghost.y+1
            blue_last_move = "down"
            blue_num_of_moves +=1
        else:
            blue_num_of_moves += 1
            
    else:
        if blue_last_move != "left" and MAP_ARRAY[blue_ghost.x+1][blue_ghost.y] != 0:    #moving right
            blue_ghost.x = blue_ghost.x+1
            blue_last_move = "right"
            blue_num_of_moves += 2

        #elif blue_last_move != "up" and MAP_ARRAY[blue_ghost.x][blue_ghost.y+1] != 0:      #moving down
            #blue_ghost.y = blue_ghost.y+1
            #blue_last_move = "down"
            #blue_num_of_moves += 2
            
        elif blue_last_move != "down" and MAP_ARRAY[blue_ghost.x][blue_ghost.y-1] != 0:    #moving up
            blue_ghost.y = blue_ghost.y-1
            blue_last_move = "up"
            blue_num_of_moves += 1

        elif blue_last_move != "right" and MAP_ARRAY[blue_ghost.x-1][blue_ghost.y] != 0:    #moving left
            blue_ghost.x = blue_ghost.x-1
            blue_last_move = "left"
            blue_num_of_moves += 2
        else:
            blue_num_of_moves += 1



    #WIN.blit(BLUE_GHOST_TOKEN, (blue_ghost.x+22, blue_ghost.y+22))


    if VULNERABLE_GHOSTS == 0:
        
        WIN.blit(BLUE_GHOST_TOKEN, (blue_ghost.x+26, blue_ghost.y+22))

        if player.colliderect(blue_ghost):
            print("Collision")
            #reset the positions of the ghosts when you collide with one
            reset_ghost_postions(red_ghost, yellow_ghost, blue_ghost, pink_ghost)
            player.x = PACMAN_SPAWN_X
            player.y = PACMAN_SPAWN_Y
            movement_direction = "STATIONARY"
            #play the death sound
            death_sound.play()
            pygame.time.delay(2000)
            #decrement the life counter
            lives -= 1


    elif BLUE_IN_PRISON != 0:
        blue_ghost.x = 350
        blue_ghost.y = 365

        WIN.blit(GHOST_VULNERABLE_TOKEN_1, (blue_ghost.x, blue_ghost.y))

        randReleaseTimer = ghost_prison_timer()

        #print("RANDOM NUM ", randReleaseTimer)

        if randReleaseTimer <=2:
            blue_ghost.x = 350
            blue_ghost.y = 281
            BLUE_IN_PRISON = 0
        
    else:
        #blue_ghost.x = 350
        #blue_ghost.y = 281
        WIN.blit(GHOST_VULNERABLE_TOKEN_1, (blue_ghost.x+26, blue_ghost.y+22))

        if player.colliderect(blue_ghost):
            print("Collision - YELLOW VULNERABLE")
            blue_last_move = " "
            #global YELLOW_PRISON_TIMER = FRAME_COUNT
            blue_ghost.x = 350
            blue_ghost.y = 281
            BLUE_IN_PRISON = 1




    #------------Old collision and vulnerability method below-------------



    #if VULNERABLE_GHOSTS == 0:
        #WIN.blit(BLUE_GHOST_TOKEN, (blue_ghost.x+26, blue_ghost.y+22))
    #else:
        #WIN.blit(GHOST_VULNERABLE_TOKEN_1, (blue_ghost.x+26, blue_ghost.y+22))
    
    #if player.colliderect(blue_ghost):
        #decrement the life counter
        #if life counter is less than or equal to 0, the game is over
        #display ther user's score and a game over screen
        #print("Collision")
        #reset_ghost_postions(red_ghost, yellow_ghost, blue_ghost, pink_ghost)
        #player.x = PACMAN_SPAWN_X
        #player.y = PACMAN_SPAWN_Y
        #movement_direction = "STATIONARY"
        #play the death noise with a brief pause while it plays
        #death_sound.play()
        #pygame.time.delay(2000)
        #move the ghosts back to the starting position
        #decrement the lives counter
        #lives -= 1











#
# Move the red ghost based on the screen and detect if there is a collision with the player
# The movement is "random" based on the amount of frames the ghost has been on the screen
# Every frame increments the (GHOST COLOR)_num_of_moves Based on the value of that it will move in different directions
# Before making a move it will look to see if the move is possible, if not it will look to the next possible move
# It records the previous move so that it cannot get stuck moving between left and right or up and down.
# Once it moves up it is unable to move down, and can only go left or right. Then it will reevaluate all possible moves on the next frame
#
def move_yellow_ghost(player, yellow_ghost, red_ghost, pink_ghost, blue_ghost):
    global movement_block
    global yellow_last_move
    global yellow_num_of_moves
    global lives
    global movement_direction
    global VULNERABLE_GHOSTS


    #########################
    global FRAME_COUNT
    global YELLOW_PRISON_TIMER
    global YELLOW_IN_PRISON

    randReleaseTimer = 0
    #########################

    #######################HANDLES GHOST TELEPORTING#######################################################
    if yellow_ghost.x == 0 and yellow_ghost.y == 358:   #handles teleporting from side to side
        yellow_ghost.x = 690

    if yellow_ghost.x == 689 and yellow_ghost.y == 358: #handles teleporting from side to side
        yellow_ghost.x = 0
    #######################HANDLES GHOST TELEPORTING#####################################################

    if yellow_num_of_moves % 3 == 0:
        if yellow_last_move != "up" and MAP_ARRAY[yellow_ghost.x][yellow_ghost.y+1] != 0:      #moving down
            yellow_ghost.y = yellow_ghost.y+1
            yellow_last_move = "down"
            yellow_num_of_moves +=1

        elif yellow_last_move != "left" and MAP_ARRAY[yellow_ghost.x+1][yellow_ghost.y] != 0:    #moving right
            yellow_ghost.x = yellow_ghost.x+1
            yellow_last_move = "right"
            yellow_num_of_moves +=1

        elif yellow_last_move != "down" and MAP_ARRAY[yellow_ghost.x][yellow_ghost.y-1] != 0:    #moving up
            yellow_ghost.y = yellow_ghost.y-1
            yellow_last_move = "up"
            yellow_num_of_moves +=1
        
        elif yellow_last_move != "right" and MAP_ARRAY[yellow_ghost.x-1][yellow_ghost.y] != 0:    #moving left
            yellow_ghost.x = yellow_ghost.x-1
            yellow_last_move = "left"
            yellow_num_of_moves +=1
            
    elif yellow_num_of_moves %2 == 0:

        if yellow_last_move != "right" and MAP_ARRAY[yellow_ghost.x-1][yellow_ghost.y] != 0:    #moving left
            yellow_ghost.x = yellow_ghost.x-1
            yellow_last_move = "left"
            yellow_num_of_moves +=2
            
        elif yellow_last_move != "down" and MAP_ARRAY[yellow_ghost.x][yellow_ghost.y-1] != 0:    #moving up
            yellow_ghost.y = yellow_ghost.y-1
            yellow_last_move = "up"
            yellow_num_of_moves +=1

        elif yellow_last_move != "right" and MAP_ARRAY[yellow_ghost.x-1][yellow_ghost.y] != 0:    #moving left
            yellow_ghost.x = yellow_ghost.x-1
            yellow_last_move = "left"
            yellow_num_of_moves +=2

        elif yellow_last_move != "up" and MAP_ARRAY[yellow_ghost.x][yellow_ghost.y+1] != 0:      #moving down
            yellow_ghost.y = yellow_ghost.y+1
            yellow_last_move = "down"
            yellow_num_of_moves +=1

        elif yellow_last_move != "left" and MAP_ARRAY[yellow_ghost.x+1][yellow_ghost.y] != 0:    #moving right
            yellow_ghost.x = yellow_ghost.x+1
            yellow_last_move = "right"
            yellow_num_of_moves +=2
        
        else:
            yellow_num_of_moves += 1
            
    else:
        if yellow_last_move != "right" and MAP_ARRAY[yellow_ghost.x-1][yellow_ghost.y] != 0:    #moving left
            yellow_ghost.x = yellow_ghost.x-1
            yellow_last_move = "left"
            yellow_num_of_moves += 2

        elif yellow_last_move != "up" and MAP_ARRAY[yellow_ghost.x][yellow_ghost.y+1] != 0:      #moving down
            yellow_ghost.y = yellow_ghost.y+1
            yellow_last_move = "down"
            yellow_num_of_moves += 2
            
        elif yellow_last_move != "down" and MAP_ARRAY[yellow_ghost.x][yellow_ghost.y-1] != 0:    #moving up
            yellow_ghost.y = yellow_ghost.y-1
            yellow_last_move = "up"
            yellow_num_of_moves += 1

        elif yellow_last_move != "left" and MAP_ARRAY[yellow_ghost.x+1][yellow_ghost.y] != 0:    #moving right
            yellow_ghost.x = yellow_ghost.x+1
            yellow_last_move = "right"
            yellow_num_of_moves += 2
        else:
            yellow_num_of_moves += 1



    #WIN.blit(YELLOW_GHOST_TOKEN, (yellow_ghost.x+22, yellow_ghost.y+22))


    if VULNERABLE_GHOSTS == 0:
        
        WIN.blit(YELLOW_GHOST_TOKEN, (yellow_ghost.x+26, yellow_ghost.y+22))

        if player.colliderect(yellow_ghost):
            print("Collision")
            #reset the positions of the ghosts when you collide with one
            reset_ghost_postions(red_ghost, yellow_ghost, blue_ghost, pink_ghost)
            player.x = PACMAN_SPAWN_X
            player.y = PACMAN_SPAWN_Y
            movement_direction = "STATIONARY"
            #play the death sound
            death_sound.play()
            pygame.time.delay(2000)
            #decrement the life counter
            lives -= 1


    elif YELLOW_IN_PRISON != 0:
        yellow_ghost.x = 350
        yellow_ghost.y = 365

        WIN.blit(GHOST_VULNERABLE_TOKEN_1, (yellow_ghost.x, yellow_ghost.y))

        randReleaseTimer = ghost_prison_timer()

        #print("RANDOM NUM ", randReleaseTimer)

        if randReleaseTimer <=2:
            yellow_ghost.x = 350
            yellow_ghost.y = 281
            YELLOW_IN_PRISON = 0
        
    else:
        #yellow_ghost.x = 350
        #yellow_ghost.y = 281
        WIN.blit(GHOST_VULNERABLE_TOKEN_1, (yellow_ghost.x+26, yellow_ghost.y+22))

        if player.colliderect(yellow_ghost):
            print("Collision - YELLOW VULNERABLE")
            yellow_last_move = " "
            #global YELLOW_PRISON_TIMER = FRAME_COUNT
            yellow_ghost.x = 350
            yellow_ghost.y = 281
            YELLOW_IN_PRISON = 1


    #------------Old collision and vulnerability method below-------------



    

    #if VULNERABLE_GHOSTS == 0:
        #WIN.blit(YELLOW_GHOST_TOKEN, (yellow_ghost.x+26, yellow_ghost.y+22))
    #else:
        #WIN.blit(GHOST_VULNERABLE_TOKEN_1, (yellow_ghost.x+26, yellow_ghost.y+22))
    
    #if player.colliderect(yellow_ghost):
        #decrement the life counter
        #if life counter is less than or equal to 0, the game is over
        #display ther user's score and a game over screen
        #print("Collision")
        #reset_ghost_postions(red_ghost, yellow_ghost, blue_ghost, pink_ghost)
        #player.x = PACMAN_SPAWN_X
        #player.y = PACMAN_SPAWN_Y
        #movement_direction = "STATIONARY"
        #play the death sound with a brief pause
        #death_sound.play()
        #pygame.time.delay(2000)
        #lives -= 1
        







#
# Move the red ghost based on the screen and detect if there is a collision with the player
# The movement is "random" based on the amount of frames the ghost has been on the screen
# Every frame increments the (GHOST COLOR)_num_of_moves Based on the value of that it will move in different directions
# Before making a move it will look to see if the move is possible, if not it will look to the next possible move
# It records the previous move so that it cannot get stuck moving between left and right or up and down.
# Once it moves up it is unable to move down, and can only go left or right. Then it will reevaluate all possible moves on the next frame
#
def move_pink_ghost(player, pink_ghost, red_ghost, yellow_ghost, blue_ghost):
    global movement_block
    global pink_last_move
    global pink_num_of_moves
    global lives
    global movement_direction
    global VULNERABLE_GHOSTS


    #########################
    global FRAME_COUNT
    global PINK_PRISON_TIMER
    global PINK_IN_PRISON

    randReleaseTimer = 0
    #########################

    #######################HANDLES GHOST TELEPORTING#######################################################
    if pink_ghost.x == 0 and pink_ghost.y == 358:   #handles teleporting from side to side
        pink_ghost.x = 690

    if pink_ghost.x == 689 and pink_ghost.y == 358: #handles teleporting from side to side
        pink_ghost.x = 0
    #######################HANDLES GHOST TELEPORTING#####################################################
    


    if pink_num_of_moves % 3 == 0:
        if pink_last_move != "up" and MAP_ARRAY[pink_ghost.x][pink_ghost.y+1] != 0:      #moving down
            pink_ghost.y = pink_ghost.y+1
            pink_last_move = "down"
            pink_num_of_moves +=1

        elif pink_last_move != "right" and MAP_ARRAY[pink_ghost.x-1][pink_ghost.y] != 0:    #moving left
            pink_ghost.x = pink_ghost.x-1
            pink_last_move = "left"
            pink_num_of_moves +=1

        elif pink_last_move != "down" and MAP_ARRAY[pink_ghost.x][pink_ghost.y-1] != 0:    #moving up
            pink_ghost.y = pink_ghost.y-1
            pink_last_move = "up"
            pink_num_of_moves +=1
        
        elif pink_last_move != "left" and MAP_ARRAY[pink_ghost.x+1][pink_ghost.y] != 0:    #moving right
            pink_ghost.x = pink_ghost.x+1
            pink_last_move = "right"
            pink_num_of_moves +=1
            
    elif pink_num_of_moves %2 == 0:
        if pink_last_move != "left" and MAP_ARRAY[pink_ghost.x+1][pink_ghost.y] != 0:    #moving right
            pink_ghost.x = pink_ghost.x+1
            pink_last_move = "right"
            pink_num_of_moves +=2
            
        elif pink_last_move != "down" and MAP_ARRAY[pink_ghost.x][pink_ghost.y-1] != 0:    #moving up
            pink_ghost.y = pink_ghost.y-1
            pink_last_move = "up"
            pink_num_of_moves +=1

        elif pink_last_move != "right" and MAP_ARRAY[pink_ghost.x-1][pink_ghost.y] != 0:    #moving left
            pink_ghost.x = pink_ghost.x-1
            pink_last_move = "left"
            pink_num_of_moves +=2

        elif pink_last_move != "up" and MAP_ARRAY[pink_ghost.x][pink_ghost.y+1] != 0:      #moving down
            pink_ghost.y = pink_ghost.y+1
            pink_last_move = "down"
            pink_num_of_moves +=1
        else:
            pink_num_of_moves += 1
            
    else:
        if pink_last_move != "left" and MAP_ARRAY[pink_ghost.x+1][pink_ghost.y] != 0:    #moving right
            pink_ghost.x = pink_ghost.x+1
            pink_last_move = "right"
            pink_num_of_moves += 2

        #elif pink_last_move != "up" and MAP_ARRAY[pink_ghost.x][pink_ghost.y+1] != 0:      #moving down
            #pink_ghost.y = pink_ghost.y+1
            #pink_last_move = "down"
            #pink_num_of_moves += 2
            
        elif pink_last_move != "down" and MAP_ARRAY[pink_ghost.x][pink_ghost.y-1] != 0:    #moving up
            pink_ghost.y = pink_ghost.y-1
            pink_last_move = "up"
            pink_num_of_moves += 1

        elif pink_last_move != "right" and MAP_ARRAY[pink_ghost.x-1][pink_ghost.y] != 0:    #moving left
            pink_ghost.x = pink_ghost.x-1
            pink_last_move = "left"
            pink_num_of_moves += 2
        else:
            pink_num_of_moves += 1



    #WIN.blit(PINK_GHOST_TOKEN, (pink_ghost.x+22, pink_ghost.y+22))


    if VULNERABLE_GHOSTS == 0:
        
        WIN.blit(PINK_GHOST_TOKEN, (pink_ghost.x+26, pink_ghost.y+22))

        if player.colliderect(pink_ghost):
            print("Collision")
            #reset the positions of the ghosts when you collide with one
            reset_ghost_postions(red_ghost, yellow_ghost, blue_ghost, pink_ghost)
            player.x = PACMAN_SPAWN_X
            player.y = PACMAN_SPAWN_Y
            movement_direction = "STATIONARY"
            #play the death sound
            death_sound.play()
            pygame.time.delay(2000)
            #decrement the life counter
            lives -= 1


    elif PINK_IN_PRISON != 0:
        pink_ghost.x = 350
        pink_ghost.y = 365

        WIN.blit(GHOST_VULNERABLE_TOKEN_1, (pink_ghost.x, pink_ghost.y))
        randReleaseTimer = ghost_prison_timer()

        #print("RANDOM NUM ", randReleaseTimer)

        if randReleaseTimer <=2:
            pink_ghost.x = 350
            pink_ghost.y = 281
            PINK_IN_PRISON = 0
        
    else:
        #red_ghost.x = 350
        #red_ghost.y = 281
        WIN.blit(GHOST_VULNERABLE_TOKEN_1, (pink_ghost.x+26, pink_ghost.y+22))

        if player.colliderect(pink_ghost):
            print("Collision - PINK VULNERABLE")
            pink_last_move = " "
            #global PINK_PRISON_TIMER = FRAME_COUNT
            pink_ghost.x = 350
            pink_ghost.y = 281
            PINK_IN_PRISON = 1


    #------------Old collision and vulnerability method below-------------

    #if VULNERABLE_GHOSTS == 0:
        #WIN.blit(PINK_GHOST_TOKEN, (pink_ghost.x+26, pink_ghost.y+22))
    #else:
        #WIN.blit(GHOST_VULNERABLE_TOKEN_1, (pink_ghost.x+26, pink_ghost.y+22))


    
    #if player.colliderect(pink_ghost):
        #decrement the life counter
        #if life counter is less than or equal to 0, the game is over
        #display ther user's score and a game over screen
        #print("Collision")
        #reset_ghost_postions(red_ghost, yellow_ghost, blue_ghost, pink_ghost)
        #player.x = PACMAN_SPAWN_X
        #player.y = PACMAN_SPAWN_Y
        #movement_direction = "STATIONARY"
        #play the death noise
        #death_sound.play()
        #pygame.time.delay(2000)
        #lives -= 1




#
# Move the red ghost based on the screen and detect if there is a collision with the player
# The movement is "random" based on the amount of frames the ghost has been on the screen
# Every frame increments the (GHOST COLOR)_num_of_moves Based on the value of that it will move in different directions
# Before making a move it will look to see if the move is possible, if not it will look to the next possible move
# It records the previous move so that it cannot get stuck moving between left and right or up and down.
# Once it moves up it is unable to move down, and can only go left or right. Then it will reevaluate all possible moves on the next frame
#
def move_red_ghost(player, red_ghost, pink_ghost, yellow_ghost, blue_ghost):
    #WIN.blit(RED_GHOST_TOKEN, Red_GHOST_RECT)
    
    #red_ghost.y = red_ghost.y+1

    global movement_block
    global red_last_move
    global red_num_of_moves
    global lives
    global movement_direction
    global VULNERABLE_GHOSTS

    #########################
    global FRAME_COUNT
    global RED_PRISON_TIMER
    global RED_IN_PRISON

    randReleaseTimer = 0
    #########################

    #######################HANDLES GHOST TELEPORTING#######################################################
    if red_ghost.x == 0 and red_ghost.y == 358:   #handles teleporting from side to side
        red_ghost.x = 690

    if red_ghost.x == 689 and red_ghost.y == 358: #handles teleporting from side to side
        red_ghost.x = 0
    #######################HANDLES GHOST TELEPORTING#####################################################
    

    if red_num_of_moves % 3 == 0:
        if red_last_move != "up" and MAP_ARRAY[red_ghost.x][red_ghost.y+1] != 0:      #moving down
            red_ghost.y = red_ghost.y+1
            red_last_move = "down"
            red_num_of_moves +=1

        elif red_last_move != "right" and MAP_ARRAY[red_ghost.x-1][red_ghost.y] != 0:    #moving left
            red_ghost.x = red_ghost.x-1
            red_last_move = "left"
            red_num_of_moves +=1

        elif red_last_move != "down" and MAP_ARRAY[red_ghost.x][red_ghost.y-1] != 0:    #moving up
            red_ghost.y = red_ghost.y-1
            red_last_move = "up"
            red_num_of_moves +=1
        
        elif red_last_move != "left" and MAP_ARRAY[red_ghost.x+1][red_ghost.y] != 0:    #moving right
            red_ghost.x = red_ghost.x+1
            red_last_move = "right"
            red_num_of_moves +=1
            
    elif red_num_of_moves %2 == 0:
        if red_last_move != "left" and MAP_ARRAY[red_ghost.x+1][red_ghost.y] != 0:    #moving right
            red_ghost.x = red_ghost.x+1
            red_last_move = "right"
            red_num_of_moves +=2
            
        elif red_last_move != "down" and MAP_ARRAY[red_ghost.x][red_ghost.y-1] != 0:    #moving up
            red_ghost.y = red_ghost.y-1
            red_last_move = "up"
            red_num_of_moves +=1

        elif red_last_move != "right" and MAP_ARRAY[red_ghost.x-1][red_ghost.y] != 0:    #moving left
            red_ghost.x = red_ghost.x-1
            red_last_move = "left"
            red_num_of_moves +=2

        elif red_last_move != "up" and MAP_ARRAY[red_ghost.x][red_ghost.y+1] != 0:      #moving down
            red_ghost.y = red_ghost.y+1
            red_last_move = "down"
            red_num_of_moves +=1
        else:
            red_num_of_moves += 1
            
    else:
        if red_last_move != "left" and MAP_ARRAY[red_ghost.x+1][red_ghost.y] != 0:    #moving right
            red_ghost.x = red_ghost.x+1
            red_last_move = "right"
            red_num_of_moves += 2

        #elif red_last_move != "up" and MAP_ARRAY[red_ghost.x][red_ghost.y+1] != 0:      #moving down
            #red_ghost.y = red_ghost.y+1
            #red_last_move = "down"
            #red_num_of_moves += 2
            
        elif red_last_move != "down" and MAP_ARRAY[red_ghost.x][red_ghost.y-1] != 0:    #moving up
            red_ghost.y = red_ghost.y-1
            red_last_move = "up"
            red_num_of_moves += 1

        elif red_last_move != "right" and MAP_ARRAY[red_ghost.x-1][red_ghost.y] != 0:    #moving left
            red_ghost.x = red_ghost.x-1
            red_last_move = "left"
            red_num_of_moves += 2
        else:
            red_num_of_moves += 1

     
    #WIN.blit(RED_GHOST_TOKEN, (red_ghost.x+26, red_ghost.y+22))

    if VULNERABLE_GHOSTS == 0:
        WIN.blit(RED_GHOST_TOKEN, (red_ghost.x+26, red_ghost.y+22))


        if player.colliderect(red_ghost):
            print("Collision")
            #reset the positions of the ghosts when you collide with one
            reset_ghost_postions(red_ghost, yellow_ghost, blue_ghost, pink_ghost)
            player.x = PACMAN_SPAWN_X
            player.y = PACMAN_SPAWN_Y
            movement_direction = "STATIONARY"
            #play the death sound
            death_sound.play()
            pygame.time.delay(2000)
            #decrement the life counter
            lives -= 1


    elif RED_IN_PRISON != 0:
        red_ghost.x = 350
        red_ghost.y = 365

        WIN.blit(GHOST_VULNERABLE_TOKEN_1, (red_ghost.x, red_ghost.y))

        randReleaseTimer = ghost_prison_timer()

        print("RANDOM NUM ", randReleaseTimer)

        if randReleaseTimer <=3:
            red_ghost.x = 350
            red_ghost.y = 281
            RED_IN_PRISON = 0
        
    else:
        #red_ghost.x = 350
        #red_ghost.y = 281
        WIN.blit(GHOST_VULNERABLE_TOKEN_1, (red_ghost.x+26, red_ghost.y+22))

        if player.colliderect(red_ghost):
            print("Collision - RED VULNERABLE")
            red_last_move = " "
            #global RED_PRISON_TIMER = FRAME_COUNT
            red_ghost.x = 350
            red_ghost.y = 281
            RED_IN_PRISON = 1

            
            #increment the score
    
            

        

    #change depending on if the ghost was vulnerable or not
    #if player.colliderect(red_ghost):
        #print("Collision")
        #reset the positions of the ghosts when you collide with one
        #reset_ghost_postions(red_ghost, yellow_ghost, blue_ghost, pink_ghost)
        #player.x = PACMAN_SPAWN_X
        #player.y = PACMAN_SPAWN_Y
        #movement_direction = "STATIONARY"
        #play the death sound
        #death_sound.play()
        #pygame.time.delay(2000)
        #decrement the life counter
        #lives -= 1




#set the ghosts in the prison for a random amount of time to add some more difficulty to the game
#all ghosts will be released at the same time for some additional difficulty since the map is kinda small and you have plenty of lives
def ghost_prison_timer():
    randNum = 0
    for x in range(10):
        randNum = random.randint(1,101)

    print("RAND NUM: ", randNum)
    return randNum


#
#draws the pellets on the map that the player will consume to gain points
#
def draw_pellets():
    pellets_on_screen = 0
    for i in PELLET_X_LIST: #Checks through
        for j in PELLET_Y_LIST:
            if MAP_ARRAY[i][j] == 2:
                WIN.blit(PELLET_TOKEN, (45+i-PELLET_WIDTH/2,41+j-PELLET_HEIGHT/2)) #(45:pixels from left to track, 41: pixels from top to track) + half track
                pellets_on_screen += 1
    for i in PELLET_X_LIST:
        for j in PELLET_Y_LIST:
            if MAP_ARRAY[i][j] == 3:
                WIN.blit(SUPER_PELLET_TOKEN, (45+i-SUPER_PELLET_WIDTH/2,41+j-SUPER_PELLET_HEIGHT/2)) #(45:pixels from left to track, 41: pixels from top to track) + half track
    return pellets_on_screen

#
#draws pacman based on the players current x and y positions
#
def draw_pacman(player, pacman_current_frame): #Should be done? Mabybe also dying animation idk
    PACMAN_IMAGE = pygame.image.load(os.path.join('Assets', 'Pacman Animation v2', PACMAN_GIF[pacman_current_frame]))
    global movement_direction
    if movement_direction == "LEFT" or movement_direction == "STATIONARY":  #Places current animation step (from dictonary) at player coords+-adjustment   player.x,player.y comes from pygame itself
        WIN.blit(pygame.transform.rotate(pygame.transform.scale(PACMAN_IMAGE, (PACMAN_WIDTH,PACMAN_HEIGHT)), 180),(player.x+25,player.y+21))
    if movement_direction == "RIGHT":
        WIN.blit(pygame.transform.scale(PACMAN_IMAGE, (PACMAN_WIDTH,PACMAN_HEIGHT)),(player.x+25,player.y+20))
    if movement_direction == "UP":
        WIN.blit(pygame.transform.rotate(pygame.transform.scale(PACMAN_IMAGE, (PACMAN_WIDTH,PACMAN_HEIGHT)), 90),(player.x+24,player.y+21))
    if movement_direction == "DOWN":
        WIN.blit(pygame.transform.rotate(pygame.transform.scale(PACMAN_IMAGE, (PACMAN_WIDTH,PACMAN_HEIGHT)), 270),(player.x+25,player.y+21))


#
#draw Ghosts over Pacman over Pellets over the Map
#
def draw_window(player, pacman_current_frame, red_ghost, pink_ghost, yellow_ghost, blue_ghost, score):
    global run
    global movement_direction
    global lives
    
    PACMAN_IMAGE = pygame.image.load(os.path.join('Assets', 'Pacman Animation v2', "PcM_fr0.png"))
    WIN.blit(MAP_IMAGE,(0,0))   #Places map
    pellets_on_screen = draw_pellets()
    draw_pacman(player, pacman_current_frame)

    #call the function to move each individueal ghost
    move_red_ghost(player, red_ghost, pink_ghost, yellow_ghost, blue_ghost)       #call the function to move the red ghost for this specific frame and detect collsion with the player
    move_pink_ghost(player, pink_ghost, red_ghost, yellow_ghost, blue_ghost)     #call the function to move the pink ghost for this specific frame and detect collsion with the player
    move_yellow_ghost(player, yellow_ghost, red_ghost, pink_ghost, blue_ghost)     #call the function to move the yellow ghost for this specific frame and detect collsion with the player
    move_blue_ghost(player, blue_ghost, red_ghost, yellow_ghost, pink_ghost)     #call the function to move the blue ghost for this specific frame and detect collsion with the player

    #display_surface = pygame.display.set_mode((300, 300))
    font = pygame.font.Font('freesansbold.ttf', 32)
    SCORE_TEXT_DISPLAY = font.render('Score: ', True, (255, 255, 255), (0,0,0)) #define the word, font color, and bacground color
    SCORE = str(score)  #turn the int score into a string
    SCORE_NUM_DISPLAY = font.render(SCORE, True, (255, 255, 255), (0,0,0))  #define the number, font color, and bacground color
    WIN.blit(SCORE_TEXT_DISPLAY, (25+280,825+20))       #display the word
    WIN.blit(SCORE_NUM_DISPLAY, (25+102+280,825+20))    #display the number

    if lives > 0:
        WIN.blit(pygame.transform.rotate(pygame.transform.scale(PACMAN_IMAGE, (PACMAN_WIDTH,PACMAN_HEIGHT)), 180),(25,825+20))
    if lives > 1:
        WIN.blit(pygame.transform.rotate(pygame.transform.scale(PACMAN_IMAGE, (PACMAN_WIDTH,PACMAN_HEIGHT)), 180),(25+60,825+20))





    
    pygame.display.update()     #Refresh screen
    if pellets_on_screen == 0:
        VICTORY = "YOU WIN!!!"
        FONTNAME = 'freesansbold.ttf'
        VICTORYCOLOR = (255, 255, 0)
        CENTERSCREENPOS = (390, 400)
        
        print("YOU WIN!!!")
        WIN.fill((0,0,1))
        font = pygame.font.Font(FONTNAME, 30)
        text_surface = font.render(VICTORY, True, VICTORYCOLOR)
        text_rect = text_surface.get_rect()
        text_rect.center = CENTERSCREENPOS
        WIN.blit(text_surface, text_rect)
        pygame.display.update()
        pygame.time.wait(5000)
        return pellets_on_screen #Tells def Main there are no more pellets on sreen
        #pygame.quit()
    

    elif lives < 0:
        #GAMEOVER = "Game Over -- Score:" + str(score) #Original score display
        GAMEOVER = "Score:" + str(score)
        FONTNAME = 'freesansbold.ttf'
        #GAMEOVERTXTCOLOR = (150, 150, 150) #This is the original gray color
        GAMEOVERTXTCOLOR = (255, 202, 24) #This is the gold color I added
        #CENTERSCREENPOS = (390, 400) #Original
        CENTERSCREENPOS = (390, 500)
        
        print("game over")
        #WIN.fill((0,0,1))
        WIN.blit(pygame.transform.scale(GAME_OVER_IMAGE, (387,293)),(196,100))
        font = pygame.font.Font(FONTNAME, 60)
        text_surface = font.render(GAMEOVER, True, GAMEOVERTXTCOLOR)
        text_rect = text_surface.get_rect()
        text_rect.center = CENTERSCREENPOS
        WIN.blit(text_surface, text_rect)
        pygame.display.update()
        pygame.time.wait(5000)
        pygame.quit()
        #sys.exit()
    


#
# resets the positions of the ghosts after the player has collided with them to ther starting points
# this helps the player not have a chance to instantly collide with the ghosts again after an initial colliosn
#
def reset_ghost_postions(red_ghost, yellow_ghost, blue_ghost, pink_ghost):
    #reset each ghost to their initial positions
    red_ghost.x = 24
    red_ghost.y = 40

    yellow_ghost.x = 667
    yellow_ghost.y = 40

    blue_ghost.x = 667
    blue_ghost.y = 720

    pink_ghost.x = 24
    pink_ghost.y = 720
    




#    
# a timer to countdown to when the ghosts should no longer be vulnerable
# sets the value of VULNERABLE_GHOSTS to '0' or '1' based on if the ghosts should be vulnerable or not
#
def vulnerable_ghost_timer(frame, vulnerable_ghosts, vulnerable_frame_init):
    global FRAME_COUNT
    global VULNERABLE_GHOSTS
    global VULNERABLE_TIMER

    #print("VULNERABLE FRAME INIT: " ,VULNERABLE_TIMER)

    timer = FRAME_COUNT - VULNERABLE_TIMER

    if timer <= 800:
        VULNERABLE_GHOSTS = 1
    else:
        VULNERABLE_GHOSTS = 0

    #timer += 1




def main(map_choice):
    global lives
    global movement_direction
    if map_choice == 1:
        initiate_map_1()
    elif map_choice == 2:
        initiate_map_2()
    

    ################################
    global FRAME_COUNT
    global VULNERABLE_GHOSTS
    global VULNERABLE_TIMER

    FRAME_COUNT +=1

    ###COMMENTED OUT BECAUSE ITS ANNOYING TO HEAR EVERY TIME I TEST SOMETHING########
    starting_theme.play()
    pygame.time.delay(2500)
    #####################
    ################################


    
    movement_direction = "STATIONARY"
    score = 0



    pacman_frame_count = 0 #Count of how many game frames have passed FOR the game, used for cycling through the pacman animation
    pacman_current_frame = 0 #Current frame of the pacman animation cycle


    #create the red_ghost object and initialize its starting x and y location
    red_ghost = pygame.Rect(50, 50, PACMAN_WIDTH, PACMAN_HEIGHT)
    red_ghost.x = 24
    red_ghost.y = 40

    #create the pink_ghost object and initialize its starting x and y location
    pink_ghost = pygame.Rect(50, 50, PACMAN_WIDTH, PACMAN_HEIGHT)
    pink_ghost.x = 24
    pink_ghost.y = 720

    #create the yellow_ghost object and initialize its starting x and y location
    yellow_ghost = pygame.Rect(50, 50, PACMAN_WIDTH, PACMAN_HEIGHT)
    yellow_ghost.x = 667
    yellow_ghost.y = 40

    #create the blue_ghost object and initialize its starting x and y location
    blue_ghost = pygame.Rect(50, 50, PACMAN_WIDTH, PACMAN_HEIGHT)
    blue_ghost.x = 667
    blue_ghost.y = 720


    player = pygame.Rect(50, 50, PACMAN_WIDTH, PACMAN_HEIGHT)
    player.x = PACMAN_SPAWN_X  # Sets the starting coordinates for Pacman
    player.y = PACMAN_SPAWN_Y  #
    
    clock = pygame.time.Clock()     #Something something game clock something
    lives = 2
    game_over = False
    run = True
    
    while run and not game_over:
        clock.tick(FPS)
        for event in pygame.event.get():    #Checks for user updates
            if event.type == pygame.QUIT:   #Exit loop if red X is pressed
                run = False

##Pacman movement##
        keys_pressed = pygame.key.get_pressed() #gets all current pressed keys
        if keys_pressed[pygame.K_a] and MAP_ARRAY[player.x-1][player.y] != 0:   #If a is pressed (left)
            movement_direction = "LEFT"
        elif keys_pressed[pygame.K_d] and MAP_ARRAY[player.x+1][player.y] != 0: #If d is pressed (right)
            movement_direction = "RIGHT"
        elif keys_pressed[pygame.K_w] and MAP_ARRAY[player.x][player.y-1] != 0: #If w is pressed (up)
            movement_direction = "UP"
        elif keys_pressed[pygame.K_s] and MAP_ARRAY[player.x][player.y+1] != 0: #If s is pressed (down)
            movement_direction = "DOWN"

        if movement_direction == "LEFT" and MAP_ARRAY[player.x-1][player.y] != 0:   #If a is pressed (left)
            player.x -= PACMAN_VELOCITY
            pacman_frame_count +=1
            if player.x == 0 and player.y == 358:   #handles teleporting from side to side
                player.x = 690
        elif movement_direction == "RIGHT" and MAP_ARRAY[player.x+1][player.y] != 0:  #If d is pressed (right)
            player.x += PACMAN_VELOCITY
            pacman_frame_count +=1
            if player.x == 689 and player.y == 358: #handles teleporting from side to side
                player.x = 0
        elif movement_direction == "UP" and MAP_ARRAY[player.x][player.y-1] != 0:   #If w is pressed (up)
            player.y -= PACMAN_VELOCITY
            pacman_frame_count +=1
        elif movement_direction == "DOWN" and MAP_ARRAY[player.x][player.y+1] != 0: #If s is pressed (down)
            player.y += PACMAN_VELOCITY
            pacman_frame_count +=1

        if pacman_frame_count >= (2*PACMAN_GFPF)+1:    #Resets the frame counter that ticks every game-frame
            pacman_frame_count = 0
        if pacman_frame_count < PACMAN_GFPF:    #Determines the pacman-frame from the current-counted-game-frame
            pacman_current_frame = 0
        elif pacman_frame_count < 2*PACMAN_GFPF:
            pacman_current_frame = 1
###############

            

        if MAP_ARRAY[player.x][player.y] == 2:
            MAP_ARRAY[player.x][player.y] = 1
            score += 10
            ######################################
            movement_sound.play()       #play the sound that the player has consumed a pellet as they were moving
            ######################################
        elif MAP_ARRAY[player.x][player.y] == 3:
            MAP_ARRAY[player.x][player.y] = 1
            ################################
            movement_sound.play()   #play the sound that the player has consumed a pellet as they were moving
            VULNERABLE_TIMER = FRAME_COUNT
            #################################################

        ###########################################################################
        #print("VULNERABLE GHOSTS: ", VULNERABLE_GHOSTS)        #used to moitor a value in testing only
        vulnerable_ghost_timer(FRAME_COUNT, VULNERABLE_GHOSTS, VULNERABLE_TIMER)
        #print("VULNERABLE GHOSTS: ", VULNERABLE_GHOSTS)        #used to moitor a value in testing only
        ###########################################################################

        pellets_on_screen = draw_window(player, pacman_current_frame, red_ghost, pink_ghost, yellow_ghost, blue_ghost, score) #Calls the window function
        
        ########################
        FRAME_COUNT +=1
        print(FRAME_COUNT)  #this print statement is used to track the frame count of the game to narrow down where errors occur in testing
        #########################

        
        if pellets_on_screen == 0: #If the game was won, return to the Main program to repeat the map selection
            return True
        elif lives < 0:
            game_over = True    #stop game, display title card + score
    if game_over:
        print("game over")
        #display the game over screen
        #MAP_IMAGE = pygame.image.load(os.path.join('Assets', 'game_over.png')).convert()
        #WIN.blit(GAME_OVER, (365, 480))
        #move the player off the screen so they cannot move anymore
        #player.x = 0
        #player.y = 0
        

        
        return True     #tells the main program to repeate the game
    if not run:
        pygame.quit()           #shuts down the window
        return False    #tells the main program to finish

if __name__ == "__main__":  #checks if the program was launched directly
    run = True
    while run:
        map_choice = 0
        while map_choice != 1 and map_choice != 2 and map_choice != "exit":  #Input Check for map1 or map2
            map_choice = input("Type '1' for Map 1, '2' for Map 2, or \"exit\"\n")
            if map_choice == "1":
                map_choice = 1
            elif map_choice == "2":
                map_choice = 2
        if map_choice != "exit":
            WIN = pygame.display.set_mode((780, 900))
            run = main(map_choice)
        else:
            run = False



#https://www.youtube.com/watch?v=jO6qQDNa2UY&t=1574s
