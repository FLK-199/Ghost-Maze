import pygame
import numpy
from inimigo import *
from player import *
from fase import *

pygame.init()
pygame.mixer.init()

numpy.random.seed()

#controle da janela
pygame.display.set_caption("Teste 1")
tela = pygame.display.set_mode((600, 600))
FPS = pygame.time.Clock()

tempo = 0.0

#criação do player
p1 = Player(290, 420)

#nimigos
inimigos = []

#Sprites
escuro = Escuridao()
todos_sprites = pygame.sprite.Group()
todos_sprites.add(escuro)

#sons
som_troca_sala = pygame.mixer.Sound("sons/trocando de sala.wav")
som_troca_sala.set_volume(0.3)
som_andar = pygame.mixer.Sound("sons/andando.wav")
som_andar.set_volume(0.7)
som_toma_dano = pygame.mixer.Sound("sons/dano.wav")
som_toma_dano.set_volume(1.0)
trilha_sonora = pygame.mixer.Sound("sons/trilha sonora.wav")
trilha_sonora.set_volume(0.3)


canal_soundtrack = pygame.mixer.Channel(0)
canal_soundtrack.play(trilha_sonora,-1)
canal_andar = pygame.mixer.Channel(1)
canal_troca_sala = pygame.mixer.Channel(2)
canal_toma_dano = pygame.mixer.Channel(3)

#variaveis globais
jogando = True
num = 1
i = 2
j = 2

def lerp(a,b,t):
    return (a + (b-a)*t)

def clamp(x,a,b):
    return max(a,min(x,b))

#Transicoes de tela
superficie_transicao = pygame.Surface((600, 600))
superficie_transicao.fill((0, 0, 0))

trocando_de_tela = False
tempo_total_de_transicao = 0.7
transicao_de_tela=0.0

def acumuladores_tempo():
    global transicao_de_tela, trocando_de_tela, tempo_total_de_transicao, tempo
    tempo += 1/60
    if trocando_de_tela:
        transicao_de_tela += 1/60
        if transicao_de_tela >= tempo_total_de_transicao:
            trocando_de_tela = False
            transicao_de_tela = 0.0

def desenha_tela_de_transicao():
    global trocando_de_tela, transicao_de_tela, tempo_total_de_transicao, superficie_transicao, tela

    if trocando_de_tela:
        superficie_transicao.fill((0, 0, 0))
        superficie_transicao.set_alpha(lerp(255,0,transicao_de_tela/tempo_total_de_transicao))
        tela.blit(superficie_transicao,(0,0))

def tocar_quando_anda():
    som_andar.set_volume(clamp(lerp(0,0.15,p1.tempo_andando/0.75),0,0.15))
    if not canal_andar.get_busy() and (teclas[pygame.K_a] or teclas[pygame.K_d] or teclas[pygame.K_w] or teclas[pygame.K_s]):
        canal_andar.play(som_andar, loops=-1)
    elif not (teclas[pygame.K_a] or teclas[pygame.K_d] or teclas[pygame.K_w] or teclas[pygame.K_s]):
        canal_andar.stop()       

def spawnar_inimigos(quantidade):
    for i in range(quantidade):
        inimigos.append(inimigos.append(Inimigo(numpy.random.normal(315,5),numpy.random.uniform(0,2*math.pi))))

#loop principal
while jogando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jogando = False

    acumuladores_tempo()
    pygame.display.set_caption("Teste 1 (" + str(i) + "," + str(j) + ")")

    teclas = pygame.key.get_pressed()
    tela.fill((154, 139, 119))

    #carrega as fases
    if i >= 0 and i < 5 and j >= 0 and j < 5:
        fase = Tilemap("fases/fase"+ str(i) + str(j) + ".txt")
        fase.desenhar(tela)
        p1.move(teclas, Tilemap.blocos_colisao(fase))
        tocar_quando_anda()
    else:
        fase = Tilemap("fases/fase_branca.txt")
        fase.desenhar(tela)
        p1.move(teclas, Tilemap.blocos_colisao(fase))
        tocar_quando_anda()

    p1.draw(tela,tempo)

    if p1.borda_colisao():
        canal_troca_sala.play(som_troca_sala)
        trocando_de_tela = True
        inimigos.clear()
        #parede da esquerda
        if p1.x < 0:
            p1.alterar_posicao((600-p1.width)+p1.x, p1.y)
            j -= 1
        #parede da direita
        elif p1.x + p1.width > 600:
            p1.alterar_posicao(abs((600-p1.width)-p1.x), p1.y)
            j += 1
        #parede de cima
        elif p1.y < 0:
            p1.alterar_posicao(p1.x, (600-p1.height)+p1.y)
            i -= 1
        #parede de baixo
        elif p1.y + p1.height > 600:
            p1.alterar_posicao(p1.x, abs((600-p1.height)-p1.y))
            i += 1    
    if i == 2 and j == 2:
        #Tudo isso so precisa ser feito uma vez
        escuro.reescalona(2.75)
        escuro.reposiciona(300,300)
        fase.desenhar_portao(tela)

    escuro.reescalona(lerp(1.55+p1.campo_de_visao_offset,1.0+p1.campo_de_visao_offset,1.0 - p1.fadeout_escuridao/1.25))
    escuro.reposiciona(p1.x + p1.width/2,p1.y + p1.height/2)

    todos_sprites.draw(tela)
    for oponente in inimigos:
        oponente.movimento(p1)
        oponente.draw(tela)
        if not p1.dando_dash and p1.hitbox.colliderect(oponente.hitbox):
            canal_toma_dano.play(som_toma_dano)
            p1.alterar_posicao(300,300)
            i = 1
            j = 2
            inimigos.clear()
    p1.draw_hud(tela)
    desenha_tela_de_transicao()
    pygame.display.update()
    FPS.tick(60)

pygame.quit()