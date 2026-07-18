import pygame

display = 600

class Player():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 20
        self.color = (150,150,230)
        self.velocidade = 2
        self.dando_dash = False
        self.dash_progresso = 0.0
        self.dash_tempo_maximo = 0.25
        self.dash_recarga = 0.0

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

    def draw(self, tela):
        pygame.draw.rect(tela, self.color, (self.x, self.y, self.width, self.height))

    def move(self, teclas, blocos):
        futuro_rect = pygame.Rect(self.x, self.y, self.width, self.height)

        dx = 0
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
