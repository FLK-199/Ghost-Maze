import pygame

display = 600

pygame.init()
pygame.mixer.init()

frames_personagem = []
frames_personagem.append(pygame.image.load("imagens/player1.png"))
frames_personagem.append(pygame.image.load("imagens/player2.png"))
frames_personagem.append(pygame.image.load("imagens/player3.png"))

anispeed = 2.5

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
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        self.escala_sprite = 1.0
        #--------------Movimento--------------
        self.velocidade = 2
        self.velocidade_sem_dash = 2
        self.velocidade_com_dash = 9
        self.velocidade_escala = 1.0
        self.tempo_andando = 0.0
        #--------------Dashes--------------
        self.sem_dash = pygame.image.load("imagens/dash1.png").convert_alpha() 
        self.com_dash = pygame.image.load("imagens/dash2.png").convert_alpha() 
        self.dando_dash = False
        self.fadeout_escuridao = 0.0
        self.campo_de_visao_offset = 0.0
        self.dash_progresso = 0.0
        self.dash_tempo_maximo = 0.35
        self.dash_recarga = 0.0
        self.tempo_de_recarga_por_dash = 3.0
        self.pode_dar_dash = True
        self.contagem_de_dashes = 0
        #--------------Sons--------------
        self.som_de_dash = pygame.mixer.Sound("sons/dash.wav")
        self.som_de_recarga = pygame.mixer.Sound("sons/recarga de dash.wav")
        #--------------Chaves--------------
        self.coletou_chave1 = False
        self.coletou_chave2 = False
        self.coletou_chave3 = False

    def alterar_posicao(self, x, y):
        self.x = x
        self.y = y
        self.hitbox.x = x
        self.hitbox.y = y

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
            self.escala_sprite = lerp(0.25,1.0,self.dash_progresso/self.dash_tempo_maximo)
            if self.dash_progresso == self.dash_tempo_maximo:
                self.dando_dash = False
                self.dash_progresso = 0.0
        else:
            self.escala_sprite = 1.0
            self.fadeout_escuridao = clamp(self.fadeout_escuridao -1/60, 0,1.25)
            self.dash_recarga = clamp(self.dash_recarga - 1/60,0.0,self.tempo_de_recarga_por_dash)
            if self.dash_recarga <= 0.0 and not self.pode_dar_dash:
                self.som_de_recarga.play(0)
                self.pode_dar_dash = True
            self.velocidade = self.velocidade_sem_dash

    def draw(self, tela, time):
        index = int((time * anispeed) % 3)
        frame_atual = frames_personagem[index]
        frame_atual = pygame.transform.scale_by(frame_atual,self.escala_sprite)
        tela.blit(frame_atual, (self.x, self.y))

    def draw_hud(self, tela):
        if self.pode_dar_dash:
            tela.blit(self.com_dash,(10,10))
        else:
            tela.blit(self.sem_dash,(10,10))

    def move(self, teclas, blocos):
        self.gerencia_dash()
        futuro_rect = pygame.Rect(self.x, self.y, self.width, self.height)

        dx = 0
        if teclas[pygame.K_LSHIFT] and not self.dando_dash and self.dash_recarga <= 0.0 and self.pode_dar_dash:
            self.dash_recarga += self.tempo_de_recarga_por_dash
            self.fadeout_escuridao = 1.25
            self.dash_progresso = 0.0
            self.dando_dash = True
            self.pode_dar_dash = False
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
            self.hitbox.x = self.x

        futuro_rect.x = self.x

        dy = 0
        if teclas[pygame.K_w]:
            dy -= self.velocidade
        if teclas[pygame.K_s]:
            dy += self.velocidade

        if teclas[pygame.K_w] or teclas[pygame.K_a] or teclas[pygame.K_s] or teclas[pygame.K_d]:
            self.tempo_andando += 1/60
        else:
            self.tempo_andando = 0.0
            
        futuro_rect.y += dy
        colidiu_y = False
        for bloco in blocos:
            if futuro_rect.colliderect(bloco):
                colidiu_y = True
                break

        if not colidiu_y:
            self.y += dy
            self.hitbox.y = self.y

class Escuridao(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image_original = pygame.image.load("imagens/circulo.png").convert_alpha() 
        self.image = pygame.image.load("imagens/circulo.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.dimensoes_base = (1200,1200)
        self.dimensoes = [1200,1200]

    def reposiciona(self , novox, novoy):
        self.rect.x = novox - self.dimensoes[0]/2
        self.rect.y = novoy - self.dimensoes[1]/2

    def reescalona(self, fator_de_escala):
        #Estica a imagem de um jeito maneiro, seila como q ele faz
        self.dimensoes[0] = self.dimensoes_base[0]*fator_de_escala
        self.dimensoes[1] = self.dimensoes_base[1]*fator_de_escala
        self.image = pygame.transform.scale_by(self.image_original,fator_de_escala)
        self.rect = self.image.get_rect()
