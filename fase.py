import pygame
from chave import *
from caminhos import *

# Tamanho em pixels de cada "quadradinho" da grade
TAMANHO_TILE = 30

chao = pygame.image.load(resource_path("imagens/chao.png")) 
parede = pygame.image.load(resource_path("imagens/arbusto1.png")) 
porta_sprite = pygame.image.load(resource_path("imagens/porta.png"))
porta_sprite1 = pygame.image.load(resource_path("imagens/portao1.png"))
porta_sprite2 = pygame.image.load(resource_path("imagens/portao2.png"))
porta_sprite3 = pygame.image.load(resource_path("imagens/portao3.png"))   

class Tilemap:
    def __init__(self, caminho_arquivo):
        self.blocos = []   
        self.bloco_invisivel = []           # Guarda os retângulos de colisão
        self.espaco_chao = []         # Espaco do chao, pra desenhar os blocos de chao depois
        self.inimigos = []            # Guarda as posições dos inimigos
        self.chave1 = (-1,-1)  
        self.chave2 = (-1,-1)
        self.chave3 = (-1,-1)

        self.carregar_mapa(caminho_arquivo)

    def carregar_mapa(self, caminho_arquivo):
        with open(caminho_arquivo, 'r') as arquivo:
            linhas = arquivo.readlines()

        # Percorre linha por linha (eixo Y)
        for linha_index, linha in enumerate(linhas):
            # Percorre caractere por caractere da linha (eixo X)
            for coluna_index, caractere in enumerate(linha.strip()):
                
                # Converte as coordenadas da grade (matriz) para PIXELS na tela
                px = coluna_index * TAMANHO_TILE
                py = linha_index * TAMANHO_TILE

                if caractere == 'X':
                    # Cria um retângulo para o bloco sólido
                    bloco = pygame.Rect(px, py, TAMANHO_TILE, TAMANHO_TILE)
                    self.blocos.append(bloco)
                elif caractere == "x":
                    bloco = pygame.Rect(px, py, TAMANHO_TILE, TAMANHO_TILE)
                    self.bloco_invisivel.append(bloco)
                elif caractere == 'I':
                    self.inimigos.append((px, py))
                elif caractere == '1':
                    self.chave1 = (px, py)
                    bloco = pygame.Rect(px, py, TAMANHO_TILE, TAMANHO_TILE)
                    self.espaco_chao.append(bloco)
                elif caractere == '2':
                    self.chave2 = (px, py)
                    bloco = pygame.Rect(px, py, TAMANHO_TILE, TAMANHO_TILE)
                    self.espaco_chao.append(bloco)
                elif caractere == '3':
                    self.chave3 = (px, py)
                    bloco = pygame.Rect(px, py, TAMANHO_TILE, TAMANHO_TILE)
                    self.espaco_chao.append(bloco)
                elif caractere == ".":
                    #Nao da nada, o bloco so um retangulo.
                    bloco = pygame.Rect(px, py, TAMANHO_TILE, TAMANHO_TILE)
                    self.espaco_chao.append(bloco)

    def desenhar(self, tela):
        for superficie in self.espaco_chao:
            pygame.draw.rect(tela, (0, 90, 50), superficie)
            tela.blit(chao,superficie)
        for bloco in self.blocos:
            pygame.draw.rect(tela, (0, 90, 50), bloco)
            tela.blit(parede,bloco)
        for bloco in self.bloco_invisivel:
            pygame.draw.rect(tela, (0, 90, 50), bloco)
            tela.blit(chao,bloco)

    def blocos_colisao(self):
        return self.blocos + self.bloco_invisivel
    
    def posicao_chave1(self):
            return self.chave1
        
    def posicao_chave2(self):
            return self.chave2
        
    def posicao_chave3(self):
            return self.chave3
    
class Porta():
    def __init__(self):
        self.chaves = 0
        self.hitbox = pygame.Rect(240, 150, 120, 210)

    def desenhar_portao(self, tela, num_chaves_coletadas):
        if num_chaves_coletadas == 0:
            tela.blit(porta_sprite, (240, 150))
        elif num_chaves_coletadas == 1:
            tela.blit(porta_sprite1, (240, 150))
        elif num_chaves_coletadas == 2:
            tela.blit(porta_sprite2, (240, 150))
        elif num_chaves_coletadas == 3:
            tela.blit(porta_sprite3, (240, 150))