import pygame
import math

display = 600

pygame.init()
pygame.mixer.init()

class Inimigo():
    def __init__(self,raio,angulo):
        self.x = 300 + raio*math.cos(angulo)
        self.y = 300 + raio*math.sin(angulo)
        self.width = 20
        self.height = 20
        self.velocidade = 1
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        #Sprite temporario
        self.sprite = pygame.image.load("imagens/dash2.png").convert_alpha()
    def draw(self,tela):
        tela.blit(self.sprite,(self.x,self.y))
    def movimento(self,player):
        direcao_y = (player.y - self.y)
        direcao_x = (player.x - self.x)
        comprimento = math.sqrt(direcao_x**2 + direcao_y**2)
        direcao_real_y = self.velocidade*direcao_y/comprimento
        direcao_real_x = self.velocidade*direcao_x/comprimento
        self.x += direcao_real_x
        self.y += direcao_real_y
        self.hitbox.y = self.y
        self.hitbox.x = self.x


