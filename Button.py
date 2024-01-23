import pygame as pg

class Button:
    def __init__(self, x, y, image, scale):
        comprimento = image.get_width()
        altura = image.get_height()
        self.image = pg.transform.scale(image, (int(comprimento*scale),int(altura*scale)))
        self.rect = self.image.get_rect()
        self.rect.topright = (x,y)
        self.clicked = False
    
    def Action(self, tela):
        action = False
        
        # get mouse position
        pos  = pg.mouse.get_pos()

        # check mouse over 
        if(self.rect.collidepoint(pos)):
            if(pg.mouse.get_pressed()[0] == 1 and self.clicked == False):
                self.clicked = True
                action = True
        
        if(pg.mouse.get_pressed()[0] == 0):
            self.clicked = False

        # show icon on screen
        tela.blit(self.image,(self.rect.x,self.rect.y))
    
        return action
    
    def Show(self, tela):
        tela.blit(self.image,(self.rect.x,self.rect.y))