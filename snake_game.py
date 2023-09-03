import pygame
import random
from enum import Enum
from collections import namedtuple

pygame.init()

font=pygame.font.Font("C:\\Users\\vivsw\\OneDrive\\Desktop\\pygame\\arial.ttf",25)

class Direction(Enum):
    RIGHT=1
    LEFT=2
    UP=3
    DOWN=4 

Point=namedtuple('Point','x,y')

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
GREEN2 = (109,113,46)
BLUED = (0, 0, 255)
BLUEL = (0, 100, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
ORANGE=(255,165,0)
BLOCK_SIZE=20
SPEED=10
class SnakeGame:

    def __init__(self,w=640,h=480):
        self.w=w
        self.h=h

        self.display=pygame.display.set_mode((self.w,self.h))
        pygame.display.set_caption("Snake Game")
        self.clock=pygame.time.Clock()

        self.direction=Direction.RIGHT

        self.head=Point(self.w//2,self.h//2)
        self.snake=[self.head,Point(self.head.x-BLOCK_SIZE,self.head.y),Point(self.head.x-2*BLOCK_SIZE,self.head.y)]

        self.score=0
        self.food=None
        self._place_food()

    def _place_food(self):
        x=random.randint(0,(self.w-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        y=random.randint(0,(self.h-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        self.food=Point(x,y)
        if self.food in self.snake or x<=BLOCK_SIZE or y<=BLOCK_SIZE or y>=self.h-BLOCK_SIZE or x>=self.w-BLOCK_SIZE:
            self._place_food()

    def play_step(self):

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()

            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_LEFT:
                    self.direction=Direction.LEFT
                elif event.key==pygame.K_RIGHT:
                    self.direction=Direction.RIGHT
                elif event.key==pygame.K_UP:
                    self.direction=Direction.UP
                elif event.key==pygame.K_DOWN:
                    self.direction=Direction.DOWN

        
        self._move(self.direction)
        self.snake.insert(0,self.head)

        game_over=False
        if self._is_collision():
            game_over=True
            return game_over,self.score


        if self.head==self.food:
            self.score+=1
            self._place_food()

        else:
            self.snake.pop() 

        self._update_ui()
        self.clock.tick(SPEED)
        
        
        return game_over,self.score
    

    def _is_collision(self):
        if self.head.x > self.w-BLOCK_SIZE or self.head.x <0 or self.head.y>self.h-BLOCK_SIZE or self.head.y<0:
            return True
        
        if self.head in self.snake[1:]:
            return True
        
        return False
    


    
    def _update_ui(self):
        self.display.fill(BLACK)

        pygame.draw.rect(self.display, GREEN2 ,pygame.Rect(self.head.x,self.head.y,BLOCK_SIZE,BLOCK_SIZE))
        for pt in self.snake[1:]:
            pygame.draw.rect(self.display, GREEN ,pygame.Rect(pt.x,pt.y,BLOCK_SIZE,BLOCK_SIZE))
            #pygame.draw.rect(self.display, BLUEL ,pygame.Rect(pt.x+4,pt.y+4,12,12))

        pygame.draw.rect(self.display, RED ,pygame.Rect(self.food.x,self.food.y,BLOCK_SIZE,BLOCK_SIZE))
        scorecard=font.render("Score: "+str(self.score),True,WHITE)
        self.display.blit(scorecard,[0,0])
        pygame.display.flip()

    def _move(self,direction):
        x=self.head.x
        y=self.head.y
        if direction==Direction.RIGHT:
            x+=BLOCK_SIZE
        elif direction==Direction.LEFT:
            x-=BLOCK_SIZE
        elif direction==Direction.DOWN:
            y+=BLOCK_SIZE
        elif direction==Direction.UP:
            y-=BLOCK_SIZE
        
        self.head=Point(x,y)


if __name__=="__main__":
    game=SnakeGame()

    while True:
        game_over,score=game.play_step()

        if (game_over==True):
            
            break
            
    
    print("Final Score ",score)
    
    pygame.quit()