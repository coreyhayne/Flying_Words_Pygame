import pygame
import random
from pygame.locals import *

pygame.init() #initializes pygame

#names game in display
win = pygame.display.set_mode((800,600))
pygame.display.set_caption("Flying Words")
pygame.display.flip()

#adds sounds to the game
gameover_sound = pygame.mixer.Sound("Sound Effects\\gameover.mp3")
point_sound = pygame.mixer.Sound("Sound Effects\\add_point.mp3")
point_sound.set_volume(0.5)
wrong_sound = pygame.mixer.Sound("Sound Effects\\wrong.mp3")
wrong_sound.set_volume(0.5)
background_sound = pygame.mixer.Sound("Sound Effects\\background.mp3")
background_sound.set_volume(0.5)
background_sound.play(loops=1)
gameover_sound_played = False

#Allows for word to show up on a random y_position for each new word
def get_random_y_position():
    return random.randint(50,450)

#gets a new word from the list of words
def update_word():
    return random.choice(words)

#Game over screen
def show_game_over_screen(screen,font,points):
    background_sound.stop()
    screen.fill((255,255,255))
    game_over_text = font.render("Game Over", True, (0,0,0))
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
    points_text = font.render(f"Total Points: {points}", True, (255,0,0))
    screen.blit(points_text, (SCREEN_WIDTH // 2 - points_text.get_width() // 2, SCREEN_HEIGHT // 2))
    pygame.display.flip()
    #Added to make gameover sound play and not loop
    global gameover_sound_played
    if not gameover_sound_played:
        gameover_sound.play()
        gameover_sound_played = True


SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 500

RED = (255,0,0)
BLACK = (0,0,0)
GREEN = (0,255,0)

file_path = "all_words.txt"
background_path = "Assets\\background.jpeg"
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
background = pygame.image.load(background_path)

#Opens file containing words and splits them
with open(file_path, 'r') as file:
    words = file.read().splitlines()

word = update_word()


typed_word = ""  #keeps track of characters player has typed

font = pygame.font.Font(None,36)
text_surface = font.render(word, True, (0,0,0))
points = 0
correct_typing = True
x_position = 0
y_position = get_random_y_position()

run = True
while run:
    
    screen.blit(background, (0,0)) #background image

    #Shows points on screen
    points_screen = font.render(f"Points: {points}", True, RED)
    screen.blit(points_screen, (10,10))
    
    #loop for events happening in game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        #runs if player clicks a key
        elif event.type == pygame.KEYDOWN:
            #updates typed word and checks if length of typed_word < length of word and if chars match or not
            if event.unicode.isalpha():
                if len(typed_word) < len(word):
                    if event.unicode == word[len(typed_word)]:
                        typed_word += event.unicode
                    else:
                        typed_word = ""
                        wrong_sound.play()
    
    #checks if typed_word is same length of word and resets to a new word
    if len(typed_word) == len(word):
        if typed_word == word:
            points += 1
            point_sound.play()
            word = update_word()
            typed_word = ""
            color = BLACK
            x_position = 0
            y_position = get_random_y_position()

    #Allows for changing each character and gets widths of each character in the word
    char_widths = [font.render(char, True, BLACK).get_width() for char in word]
    total_width = sum(char_widths)
    current_x = x_position

    #updates color of each character in word   
    for i, (char,char_width) in enumerate(zip(word,char_widths)):
        if i < len(typed_word):
            if typed_word[i] == char:
                color = GREEN
            else:
                color = BLACK
                correct_typing = False
        else:
            color = BLACK
        char_render = font.render(char, True, color)
        screen.blit(char_render, (current_x, y_position))
        current_x += char_width

    #Scrolls the text
    x_position += 3

    #Game over if word reaches end of screen
    if x_position > (SCREEN_WIDTH - total_width):
        show_game_over_screen(screen,font,points)

    #updates contents in screen
    pygame.display.flip()

    #makes 60 fps
    pygame.time.Clock().tick(60)

#ends pygame
pygame.quit()

