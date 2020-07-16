import pygame
import time

class Environment:
    def __init__(self,width,height):
        self.width=width
        self.height=height
        pygame.display.set_caption('Snake Game')
        self.display=pygame.display.set_mode((width,height))
        self.bg=pygame.transform.scale(pygame.image.load("media/background.jpg"),(width,height))
        self.display.blit(self.bg,(0,0))
        pygame.display.update()


if __name__ == '__main__':
    pygame.init()
    env = Environment(600,400)
    game_over = False
    while not game_over:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                game_over=True
            print(event)
                
    pygame.quit()
    quit()



        

