# Importing the needed modules
import pygame
from sys import exit
from classes import *
from random import choice

# Class used to represent the game instance
class Game():

    # Constants that represent the current game's state
    MAIN_MENU = 0
    PLAYING = 1
    GAME_OVER = 2

    def __init__(self, width, height, title='pygame'):
        pygame.init()
        
        # Basic setup, includes window sizing, title, sound etc
        self.SCREEN_WIDTH = width
        self.SCREEN_HEIGHT = height
        self.screen = pygame.display.set_mode((width, height))

        pygame.display.set_caption(title)
        pygame.mouse.set_visible(False)
        icon = pygame.image.load('./images/gameIcon.ico').convert_alpha()
        pygame.display.set_icon(icon)

        gameSound = pygame.mixer.Sound('./sounds/gameMusic.wav')
        gameSound.play(-1)
        gameSound.set_volume(0.3)

        self.clock = Clock(60)

        # Setting the background
        sky = Background('./images/background/sky.jpg', (0, 0), self.SCREEN_WIDTH)
        ground = Background('./images/background/ground.jpg', sky.rect.bottomleft, self.SCREEN_WIDTH)
        self.background = [sky, ground]

        # Setting all the needed text
        gameName = Text(150, (self.SCREEN_WIDTH / 2, 100), 'Runner')
        start = Text(70, (self.SCREEN_WIDTH / 2, gameName.rect.bottom + 50), 'Start')
        exit = Text(70, (self.SCREEN_WIDTH / 2, start.rect.bottom + 50), 'Exit')
        self.startText = pygame.sprite.Group(gameName, start, exit)

        gameOver = Text(150, (self.SCREEN_WIDTH / 2, 100), 'Game Over', 'Red')
        restart = Text(70, (self.SCREEN_WIDTH / 2, gameOver.rect.bottom + 50), 'Restart')
        menu = Text(70, (self.SCREEN_WIDTH / 2, restart.rect.bottom + 50), 'Main Menu')
        self.loseText = pygame.sprite.Group(gameOver, restart, menu)

        # Setting game states
        self.states = [
            [start.rect, exit.rect],
            [],
            [restart.rect, menu.rect]
        ]
        self.current_state = self.MAIN_MENU

        # Defining arrows for certain text that represents options
        self.arrows = TextArrows(self.states[self.current_state])

        # Defining the player as well as the player score
        self.player = pygame.sprite.GroupSingle( Player( (ground.rect.left + 50, ground.rect.top) ) )
        self.playerScore = PlayerScore(50, self.SCREEN_WIDTH)

        # Defining the group which will contain all the mobs
        self.mobs = pygame.sprite.Group()
        self.mobSpawn = None

    # Method that ends the game
    def quit(self):
        pygame.quit()
        exit()

    # Method that runs the game
    def run(self):
        while True:
            # Event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()

                elif self.current_state != self.PLAYING and event.type == pygame.KEYDOWN:
                    
                    self.background[0].speed = 1
                    self.background[1].speed = 1

                    if event.key == pygame.K_UP:
                        self.arrows.moveUp()

                    elif event.key == pygame.K_DOWN:
                        self.arrows.moveDown()

                    elif self.current_state == self.MAIN_MENU and event.key == pygame.K_RETURN and self.arrows.index:
                        self.quit()

                    elif self.current_state == self.GAME_OVER and event.key == pygame.K_RETURN and self.arrows.index:
                        self.current_state = self.MAIN_MENU
                        self.arrows.fillPositions(self.states[self.MAIN_MENU])

                    elif ( self.current_state == self.MAIN_MENU or self.current_state == self.GAME_OVER ) and event.key == pygame.K_RETURN and not self.arrows.index:
                        self.current_state = self.PLAYING
                        self.background[0].speed = 2
                        self.background[1].speed = 2
                        self.playerScore.start_time = pygame.time.get_ticks()

                        self.mobs.add(choice( [Mob('snail', (800, 300))] * 3 + [Mob('fly', (800, 200))]))
                        self.mobSpawn = pygame.time.get_ticks()
                
                elif self.current_state == self.PLAYING and event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        self.player.update(jump=True)
        
            # Loop background
            for bg in self.background:
                bg.update()
                bg.draw(self.screen)
            
            # Main menu state
            if self.current_state == self.MAIN_MENU:
                self.startText.draw(self.screen)
                self.arrows.draw(self.screen)
            
            # Game over state
            elif self.current_state == self.GAME_OVER:
                self.loseText.draw(self.screen)
                self.arrows.draw(self.screen)
            
            # Player is playing the game state
            else:
                self.player.update()
                self.player.draw(self.screen)

                self.playerScore.update(pygame.time.get_ticks())
                self.playerScore.draw(self.screen)

                self.mobs.update()
                self.mobs.draw(self.screen)

                if pygame.sprite.spritecollide(self.player.sprite, self.mobs, False):
                    self.mobs.empty()
                    self.current_state = self.GAME_OVER
                    self.arrows.fillPositions(self.states[self.GAME_OVER])
                
                if pygame.time.get_ticks() - self.mobSpawn > 1500:
                    self.mobs.add(choice( [Mob('snail', (800, 300))] * 3 + [Mob('fly', (800, 200))]))
                    self.mobSpawn = pygame.time.get_ticks()

            # Update the
            pygame.display.update()
            self.clock.tick()

# Indicator that this is the main script from which everything is ran
if __name__ == '__main__':
    game = Game(800, 400, 'Runner')
    game.run()