import pygame

display = 600
pygame.init()
pygame.mixer.init()


def lerp(a,b,t):
    return (a + (b-a)*t)

#Forca x ficar entre a e b, corta o valor pra a se for menor, e corta pra b se for maior
def clamp(x,a,b):
    return max(a,min(x,b))

class Player():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 20
        self.color = (150,150,230)
        self.velocidade = 2
        self.velocidade_sem_dash = 2
        self.velocidade_com_dash = 9
        self.dando_dash = False
        self.dash_progresso = 0.0
        self.dash_tempo_maximo = 0.35
        self.dash_recarga = 0.0
        self.tempo_de_recarga_por_dash = 3.0
        self.quantidade_maxima_de_dashes = 2
        self.contagem_de_dashes = -1
        self.som_de_dash = pygame.mixer.Sound("sons/dash.wav")
        self.som_de_recarga = pygame.mixer.Sound("sons/recarga de dash.wav")

    def alterar_posicao(self, x, y):
        self.x = x
        self.y = y
    def borda_colisao(self):
        if (self.x < 0 or 
            self.y < 0 or
            self.x + self.width > display or
            self.y + self.height > display):
            return True
        return False
    def gerencia_dash(self):
        if self.dando_dash:
            self.dash_progresso = clamp(self.dash_progresso + 1/60,0,self.dash_tempo_maximo)
            self.velocidade = lerp(self.velocidade_com_dash,self.velocidade_sem_dash,self.dash_progresso/self.dash_tempo_maximo)
            if self.dash_progresso == self.dash_tempo_maximo:
                self.dando_dash = False
                self.dash_progresso = 0.0
        else:
            self.dash_recarga = clamp(self.dash_recarga - 1/60,0.0,self.tempo_de_recarga_por_dash*self.quantidade_maxima_de_dashes)
            if self.dash_recarga <= self.tempo_de_recarga_por_dash*self.contagem_de_dashes:
                self.som_de_recarga.play(0)
                self.contagem_de_dashes -= 1
            self.velocidade = self.velocidade_sem_dash

    def draw(self, tela):
        pygame.draw.rect(tela, self.color, (self.x, self.y, self.width, self.height))
        pygame.draw

    def move(self, teclas, blocos):
        self.gerencia_dash()
        futuro_rect = pygame.Rect(self.x, self.y, self.width, self.height)

        dx = 0
        if teclas[pygame.K_LSHIFT] and not self.dando_dash and self.dash_recarga <= (self.quantidade_maxima_de_dashes - 1)*self.tempo_de_recarga_por_dash:
            self.dash_recarga += self.tempo_de_recarga_por_dash
            self.contagem_de_dashes += 1
            if self.contagem_de_dashes == 0:
                self.contagem_de_dashes += 1
            self.dash_progresso = 0.0
            self.dando_dash = True
            self.som_de_dash.play(0)
        if teclas[pygame.K_a]:
            dx -= self.velocidade
        if teclas[pygame.K_d]:
            dx += self.velocidade

        futuro_rect.x += dx
        colidiu_x = False
        for bloco in blocos:
            if futuro_rect.colliderect(bloco):
                colidiu_x = True
                break
        
        if not colidiu_x:
            self.x += dx

        futuro_rect.x = self.x

        dy = 0
        if teclas[pygame.K_w]:
            dy -= self.velocidade
        if teclas[pygame.K_s]:
            dy += self.velocidade

        futuro_rect.y += dy
        colidiu_y = False
        for bloco in blocos:
            if futuro_rect.colliderect(bloco):
                colidiu_y = True
                break

        if not colidiu_y:
            self.y += dy


class Escuridao(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image_original = pygame.image.load("imagens/circulo.png").convert_alpha() 
        self.image = pygame.image.load("imagens/circulo.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (-1200, -1200)

    def reposiciona(self , novox, novoy):
        self.rect.x = novox
        self.rect.y = novoy
    def reescalona(self, x, y):
        nova_largura = int(1200*x)
        nova_altura = int(1200*y)
        #Estica a imagem de um jeito maneiro, seila como q ele faz
        self.image = pygame.transform.smoothscale(self.image_original,(nova_largura,nova_altura))
        self.rect = self.image.get_rect()
        self.rect.center = (-1200,-1200)
