import pygame
from caminhos import *

class chave(pygame.sprite.Sprite):
    def __init__(self, x, y, numero_chave):
        super().__init__()
        self.x = x
        self.y = y
        self.chave_sprite = pygame.image.load(resource_path("imagens/chave.png")).convert_alpha() 
        self.numero_da_chave = numero_chave
        self.hitbox = pygame.Rect(self.x, self.y, 20, 20)

    def alterar_posicao(self, x, y):
        self.x = x
        self.hitbox.x = x
        self.y = y
        self.hitbox.y = y

    def desenhar(self, tela):
        #desenha a chave 1
        if self.numero_da_chave == 1:
            tela.blit(self.chave_sprite,(self.x,self.y))
        #desenha a chave 2
        if self.numero_da_chave == 2:
            tela.blit(self.chave_sprite,(self.x,self.y))
        #desenha a chave 3
        if self.numero_da_chave == 3:
            tela.blit(self.chave_sprite,(self.x,self.y))