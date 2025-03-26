import pygame
pygame.font.init()
window = pygame.display.set_mode((800,800))
FONT = pygame.font.SysFont("comicsans",60,bold = True)
napravlenie = ""
class Plitka():
    def __init__(self,w,h,color,x,y, number):
        self.w = w
        self.h = h
        self.color = color
        self.x = x
        self.y = y
        self.number = number

    def draw(self):
        pygame.draw.rect(window,(255,0,0),(self.x,self.y,self.w,self.h),5)
        number_text = FONT.render(str(self.number),True,(0,0,255))
        window.blit(number_text,(self.x, self.y) )
    def move(self):
        global napravlenie
        if napravlenie == "down":
            if self.y <= 600:
                self.y += 1
        if napravlenie == "up":
            if self.y >= 0:
                self.y -= 1
        if napravlenie == "left":
            if self.x >= 0:
                self.x -= 1
        if napravlenie == "right":
            if self.x <= 600:
                self.x += 1
plitka1 = Plitka(200,200,(255,0,0), 0, 0, 2)
plitka2 = Plitka(200,200,(255,0,0), 600,600, 2)
plitki = []
plitki.append(plitka1)
plitki.append(plitka2)

while True:
    window.fill((0,255,0))
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                napravlenie = "down"
            if event.key == pygame.K_w:
                napravlenie = "up"
            if event.key == pygame.K_a:
                napravlenie = "left"
            if event.key == pygame.K_d:
                napravlenie = "right"

    for i in plitki:
        i.draw()
        i.move()
    # plitki.draw()
    # plitki.move()
    pygame.display.update()
