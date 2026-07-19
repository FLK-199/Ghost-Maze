import pygame
import math
from caminhos import *

display = 600

pygame.init()
pygame.mixer.init()

frames_inimigos = []
frames_inimigos.append(pygame.image.load(resource_path("imagens/inimigo_sprite1.png")))
frames_inimigos.append(pygame.image.load(resource_path("imagens/inimigo_sprite2.png")))
frames_inimigos.append(pygame.image.load(resource_path("imagens/inimigo_sprite3.png")))
frames_inimigos.append(pygame.image.load(resource_path("imagens/inimigo_sprite4.png")))

anispeed = 2.5

class Inimigo():
    def __init__(self,raio,angulo,velo_inicial):
        self.x = 300 + raio*math.cos(angulo)
        self.y = 300 + raio*math.sin(angulo)
        self.width = 20
        self.height = 20
        self.velocidade = velo_inicial
        self.escala_sprite = 1.0
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        #Sprite temporario
        self.sprite = pygame.image.load(resource_path("imagens/dash2.png")).convert_alpha()
        #Recebe info do player pra mover ate ele
        #self.player_x = 300
        #self.player_y = 300

    def draw(self,tela,time):
        index = int((time * anispeed) % 3)
        frame_atual = frames_inimigos[index]
        frame_atual = pygame.transform.scale_by(frame_atual,self.escala_sprite)
        tela.blit(frame_atual, (self.x, self.y))
    
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


