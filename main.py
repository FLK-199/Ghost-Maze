import pygame
import numpy
from inimigo import *
from player import *
from fase import *
from chave import *
from caminhos import *

pygame.init()
pygame.mixer.init()

numpy.random.seed()

#controle da janela
icone = pygame.image.load(resource_path("imagens/icone.png"))
pygame.display.set_icon(icone)
pygame.display.set_caption("Ghost Maze")
tela = pygame.display.set_mode((600, 600))
FPS = pygame.time.Clock()

tempo = 0.0

#criação do player
p1 = Player(290, 420)

#chaves
chave1 = chave(-1,-1,1)
chave2 = chave(-1,-1,2) 
chave3 = chave(-1,-1,3)

#nimigos
inimigos = []

#Sprites
porta = Porta()
escuro = Escuridao()
todos_sprites = pygame.sprite.Group()
todos_sprites.add(escuro)

#sons
som_pega_chave = pygame.mixer.Sound(resource_path("sons/pegou chave.wav"))
som_pega_chave.set_volume(0.5)
som_troca_sala = pygame.mixer.Sound(resource_path("sons/trocando de sala.wav"))
som_troca_sala.set_volume(0.3)
som_andar = pygame.mixer.Sound(resource_path("sons/andando.wav"))
som_andar.set_volume(0.7)
som_toma_dano = pygame.mixer.Sound(resource_path("sons/dano.wav"))
som_toma_dano.set_volume(1.0)
trilha_sonora = pygame.mixer.Sound(resource_path("sons/trilha4.wav"))
trilha_sonora.set_volume(0.3)


canal_soundtrack = pygame.mixer.Channel(0)
canal_soundtrack.play(trilha_sonora,-1)
canal_andar = pygame.mixer.Channel(1)
canal_troca_sala = pygame.mixer.Channel(2)
canal_toma_dano = pygame.mixer.Channel(3)

#variaveis globais
jogando = True
num = 1
n_chaves_coletadas = 0
i = 2
j = 2

fase = Tilemap(resource_path("fases/fase" + str(i) + str(j) + ".txt"))

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
    for v in range(quantidade):
        inimigos.append(Inimigo(numpy.random.normal(375,5),numpy.random.uniform(0,2*math.pi),numpy.random.normal(0.75 + n_chaves_coletadas*0.35,0.25)))

tela_inicial = True

imagem_menu = pygame.image.load(resource_path("imagens/tela_inicial.jpeg"))

imagem_menu_rect = imagem_menu.get_rect()

while tela_inicial:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            tela_inicial = False
    tela.blit(imagem_menu, imagem_menu_rect)
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LSHIFT] or teclas[pygame.K_w] or teclas[pygame.K_a] or teclas[pygame.K_s] or teclas[pygame.K_d]:
        tela_inicial = False

    pygame.display.flip()


#loop principal
while jogando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jogando = False

    acumuladores_tempo()
    pygame.display.set_caption("Ghost Maze (" + str(i) + "," + str(j) + ")")

    teclas = pygame.key.get_pressed()
    tela.fill((154, 139, 119))
    
    if teclas[pygame.K_0]:
        p1.coletou_chave1 = True
        p1.coletou_chave2 = True
        p1.coletou_chave3 = True
        n_chaves_coletadas = 3

    #carrega as fases
    if i >= 0 and i < 5 and j >= 0 and j < 5:
        fase.desenhar(tela)
        p1.move(teclas, Tilemap.blocos_colisao(fase))
        tocar_quando_anda()
    else:
        fase.desenhar(tela)
        p1.move(teclas, Tilemap.blocos_colisao(fase))
        tocar_quando_anda()


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

        if i >= 0 and i < 5 and j >= 0 and j < 5:
            fase = Tilemap(resource_path("fases/fase" + str(i) + str(j) + ".txt"))
        else:
            fase = Tilemap(resource_path("fases/fase_branca.txt"))
            
        if p1.assombrado and not (i,j) == (2,2):
            spawnar_inimigos(5*n_chaves_coletadas)
    else:
        if (i,j) != (2,2):
            escuro.reescalona(lerp(1.55+p1.campo_de_visao_offset,1.0+p1.campo_de_visao_offset,1.0 - p1.fadeout_escuridao/1.25))
            escuro.reposiciona(p1.x + p1.width/2,p1.y + p1.height/2)
        
    if (i,j) == (2,2):
        #Tudo isso so precisa ser feito uma vez
        p1.assombrado = False
        porta.desenhar_portao(tela, n_chaves_coletadas)
        escuro.reescalona(2.75)
        escuro.reposiciona(300, 300)

        if p1.coletou_chave3:
            jogando = False
            
    elif (i,j) == (0,4):
        
        (ci,cj) = fase.posicao_chave1()
        chave1.alterar_posicao(ci,cj)
        
        if not p1.coletou_chave1:
            chave1.desenhar(tela)
            if p1.hitbox.colliderect(chave1.hitbox):
                som_pega_chave.play()
                n_chaves_coletadas += 1
                p1.upgrade_chave1()

    elif (i,j) == (2,0):
        
        (ci,cj) = fase.posicao_chave2()
        chave2.alterar_posicao(ci,cj)
        
        if not p1.coletou_chave2:
            chave2.desenhar(tela)
            if p1.hitbox.colliderect(chave2.hitbox):
                som_pega_chave.play()
                n_chaves_coletadas += 1
                p1.upgrade_chave2()

    elif (i,j) == (4,3):
        
        (ci,cj) = fase.posicao_chave3()
        chave3.alterar_posicao(ci,cj)
        if not p1.coletou_chave3:
            chave3.desenhar(tela)
            if p1.hitbox.colliderect(chave3.hitbox):
                som_pega_chave.play()
                n_chaves_coletadas += 1
                p1.upgrade_chave3()       

    p1.draw(tela,tempo)
    
    #parte dos inimigos
    todos_sprites.draw(tela)
    for oponente in inimigos:
        oponente.movimento(p1)
        oponente.draw(tela,tempo)
        if not p1.dando_dash and p1.hitbox.colliderect(oponente.hitbox):
            canal_toma_dano.play(som_toma_dano)
            if p1.coletou_chave3:
                p1.desfazer_chave3()
                n_chaves_coletadas -=1
            elif p1.coletou_chave2:
                p1.desfazer_chave2()
                n_chaves_coletadas -=1
            elif p1.coletou_chave1:
                p1.desfazer_chave1()
                n_chaves_coletadas -=1
            p1.alterar_posicao(290,420)
            i = 2
            j = 2
            inimigos.clear()
            fase = Tilemap(resource_path("fases/fase" + str(i) + str(j) + ".txt"))

    p1.draw_hud(tela)
    desenha_tela_de_transicao()
    pygame.display.update()
    FPS.tick(60)

tela_final = True

imagem_tela_final = pygame.image.load(resource_path("imagens/tela_final.jpeg"))
imagem_final_rect = imagem_tela_final.get_rect()

while tela_final and p1.coletou_chave3:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            tela_final = False
    tela.blit(imagem_tela_final, imagem_final_rect)
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LSHIFT] or teclas[pygame.K_w] or teclas[pygame.K_a] or teclas[pygame.K_s] or teclas[pygame.K_d]:
        tela_inicial = False

    pygame.display.flip()   

pygame.quit()