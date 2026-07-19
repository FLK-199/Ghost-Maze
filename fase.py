import pygame

# Tamanho em pixels de cada "quadradinho" da grade
TAMANHO_TILE = 30

class Tilemap:
    def __init__(self, caminho_arquivo):
        self.blocos = []              # Guarda os retângulos de colisão
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
                elif caractere == 'I':
                    self.inimigos.append((px, py))
                elif caractere == '1':
                    self.chave1 = (px, py)
                elif caractere == '2':
                    self.chave2 = (px, py)
                elif caractere == '3':
                    self.chave3 = (px, py)

    def desenhar(self, tela):
        for bloco in self.blocos:
            # Desenha cada bloco (você pode substituir por uma imagem/sprite depois)
            pygame.draw.rect(tela, (0, 90, 50), bloco)
            # Desenha uma borda escura para dar efeito de blocos separados
            #pygame.draw.rect(tela, (50, 50, 50), bloco, 2)

        #desenha a chave 1
        if self.chave1 != (-1,-1):
            pygame.draw.rect(tela, (255, 0, 0), (self.chave1[0], self.chave1[1], TAMANHO_TILE, TAMANHO_TILE))
        #desenha a chave 2
        if self.chave2 != (-1,-1):
            pygame.draw.rect(tela, (0, 255, 0), (self.chave2[0], self.chave2[1], TAMANHO_TILE, TAMANHO_TILE))
        #desenha a chave 3
        if self.chave3 != (-1,-1):
            pygame.draw.rect(tela, (0, 0, 255), (self.chave3[0], self.chave3[1], TAMANHO_TILE, TAMANHO_TILE))

    def desenhar_portao(self, tela):
        pygame.draw.rect(tela, (100, 100, 100), (240, 150, 120, 210))

    def blocos_colisao(self):
        return self.blocos