import pygame
import random
pygame.font.init()
window = pygame.display.set_mode((800,800))
game = True
FONT = pygame.font.SysFont("comicsans",60,bold = True)
napravlenie = ""
moving = False

clock = pygame.time.Clock()
class Plitka():
    COLORS = [
        (237, 229, 218),
        (238, 225, 201),
        (243, 178, 122),
        (246, 150, 101),
        (247, 124, 95),
        (247, 95, 59),
        (237, 208, 115),
        (237, 204, 99),
        (236, 202, 80),
    ]
    def __init__(self,w,h,color,x,y, number):
        self.w = w
        self.h = h
        self.color = color
        self.x = x
        self.y = y
        self.number = number
        self.rec = pygame.Rect(self.x,self.y,200,200)
    def pos_create(self):
        x_pos = random.randint(1,4)
        y_pos = random.randint(1,4)
        if x_pos == 1:
            self.x = 0
        elif x_pos == 2:
            self.x = 200
        elif x_pos == 3:
            self.x = 400
        elif x_pos == 4:
            self.x = 600
        if y_pos == 1:
            self.y = 0
        elif y_pos == 2:
            self.y = 200
        elif y_pos == 3:
            self.y = 400
        elif y_pos == 4:
            self.y = 600
    def move(self):
        global napravlenie
        global moving
        if napravlenie == "down":
            print(self.rec.y)
            if self.rec.y <= 600 and moving == True:
                self.rec.y += 10
            #else:
                #moving = False
        if napravlenie == "up":
            if self.rec.y >= 0:
                # moving = True
                self.rec.y -= 10
            #else:
                #moving = False
        if napravlenie == "left":
            if self.rec.x >= 0:
                # moving = True
                self.rec.x -= 10
            #else:
                #moving = False
        if napravlenie == "right":
            if self.rec.x <= 600:
                # moving = True
                self.rec.x += 10
            #else:
                #moving = False
    def draw(self):
        pygame.draw.rect(window,(237, 229, 218),self.rec)
        number_text = FONT.render(str(self.number),True,(119, 110, 101))
        window.blit(number_text,(self.rec.x, self.rec.y) )
plitka1 = Plitka(200,200,(237, 229, 218), 0, 0,2)
plitka2 = Plitka(200,200,(237, 229, 218), 600,600,2)
plitki = []
plitki.append(plitka1)
plitki.append(plitka2)
def create_grid():
    for line in range(1,4):
        y = line * 200
        pygame.draw.line(window,(187, 173, 160),(0,y),(800,y), 10)
    for stolb in range(1,4):
        x = stolb * 200
        pygame.draw.line(window,(187, 173, 160),(x,0),(x,800),10)
    pygame.draw.rect(window,(187, 173, 160),(0,0,800,800),10)
while game:
    window.fill((205, 192, 180))
    create_grid()
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN :
                
                if event.key == pygame.K_s and moving == False:
                        moving = True
                        napravlenie = "down"
                        print(napravlenie)
                        print(moving)
                        plitka3 = Plitka(200,200,(0,150,0),0,0,2)
                        plitka3.pos_create()
                        plitki.append(plitka3)
                if event.key == pygame.K_w and moving == False:
                        napravlenie = "up"
                if event.key == pygame.K_a and moving == False:
                        napravlenie = "left"
                if event.key == pygame.K_d and moving == False:
                        napravlenie = "right"
        if event.type == pygame.QUIT:
            game = False
    if plitka1.rec.colliderect(plitka2.rec):
        if plitka1.number == plitka2.number:
            plitka1.number = plitka1.number * 2
            plitki.remove(plitka2)
    else:
        moving = False
    
    for i in plitki:
        i.draw()
        i.move()
    # plitki.draw()
    # plitki.move()
    clock.tick(40)
    pygame.display.update()
    # plitki.move()
    pygame.display.update()
