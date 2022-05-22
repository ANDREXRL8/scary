import random
import pygame
from pygame.locals import *
from sys import exit
import os


# definindo tamanho da tela/janela
TELA_LARGURA = 640
TELA_ALTURA = 480

#controlando velocidade do jogo
SPEED = 10
GAME_SPEED = 5

CHAO_LARGURA = 2 * TELA_LARGURA
CHAO_ALTURA = 10

PRETO = (0, 0, 0) #cor da background da janela

tela = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA)) #criando a janela
pygame.display.set_caption('Sexta feira 13') #titulo da tela

sprite_sheet = pygame.image.load(os.path.join('sprites', 'fantasma2.png')).convert_alpha() #convert_alpha serve desconsiderar o bits transparentes

class Fantasma(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.imagens_fantasma = []
        for i in range(6):
            img = sprite_sheet.subsurface((i * 64,0), (64, 64)) # o subsurface serve para recortar a sprite_sheet
            self.imagens_fantasma.append(img) # adicionando dentro da lista

        self.index_lista = 0
        self.image = self.imagens_fantasma[self.index_lista]
        self.rect = self.image.get_rect()
        self.rect.center = (25,440) #posição que o fantasma vai começar no jogo


        self.speed = SPEED
        self.mask = pygame.mask.from_surface(self.image)

    
    def update(self):

        def move_player(self):
            key = pygame.key.get_pressed()
            if key[pygame.K_d]:
                self.rect[0] += GAME_SPEED
            if key[pygame.K_a]:
                self.rect[0] -= GAME_SPEED
        move_player(self)

        def fly_up(self):
            key = pygame.key.get_pressed()
            if key[pygame.K_w]:
                self.rect[1] -= 10
        fly_up(self)

        def fly_down(self):
            key = pygame.key.get_pressed()
            if key[pygame.K_x]:
                self.rect[1] += 10
        fly_down(self)

        
        if self.index_lista > 2:
            self.index_lista = 0
        self.index_lista += 0.25
        self.image = self.imagens_fantasma[int(self.index_lista)]  

#colocando os frames do fantasma dentro de um grupo
frames_fantasmas = pygame.sprite.Group()
player = Fantasma()
frames_fantasmas.add(player)

class Chao(pygame.sprite.Sprite):
    def __init__(self, xpos):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(os.path.join('sprites', 'ground.png'))
        self.image = pygame.transform.scale(self.image, (CHAO_LARGURA, CHAO_ALTURA))

        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        self.rect[1] = TELA_ALTURA - CHAO_ALTURA #posição Y

    def update(self):
        self.rect[0] -= GAME_SPEED 

def fora_tela(sprite):
    # verifica quando o objeto sai da tela
    return sprite.rect[0] < -(sprite.rect[2])

chaoGroup = pygame.sprite.Group()
for i in range(2):
    chao = Chao(CHAO_LARGURA * i)
    chaoGroup.add(chao)


class Abobora(pygame.sprite.Sprite):
    def __init__(self, xpos, ysize):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join('sprites', 'abobora01.png'))
        self.image = pygame.transform.scale(self.image, [40, 40])
        self.rect = pygame.Rect(100, 50, 50, 50)
        self.rect[0] = xpos
        self.mask = pygame.mask.from_surface(self.image)
        self.rect[1] = TELA_ALTURA - ysize

    def update(self, *args):
        self.rect[0] -= GAME_SPEED

class Coins(pygame.sprite.Sprite):
    def __init__(self, xpos, ysize):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join('sprites', 'coin.png'))
        self.image = pygame.transform.scale(self.image, [40, 40])
        self.rect = pygame.Rect(50, 50, 50, 50)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect[0] = xpos
        self.rect[1] = TELA_ALTURA - ysize

    def update(self, *args):
        self.rect[0] -= GAME_SPEED

def get_random_aboboras(xpos):
    size = random.randint(64, 480)   #150x150
    abobora = Abobora(xpos, size)
    return abobora

def get_random_coins(xpos):
    size = random.randint(32, 380)
    coin = Coins(xpos, size)
    return coin

coinsGroup = pygame.sprite.Group()
for i in range(2):
    coin = get_random_coins(TELA_LARGURA* i + 10)
    coinsGroup.add(coin)

aboboraGroup = pygame.sprite.Group()
for i in range(2):
    abob = get_random_aboboras(TELA_LARGURA * i + 10)
    aboboraGroup.add(abob)


#função para desenhar instancias do grupo
def draw():
    frames_fantasmas.draw(tela)
    chaoGroup.draw(tela)
    aboboraGroup.draw(tela)
    coinsGroup.draw(tela)

#função para atualizar instancias do grupo
def update():
    frames_fantasmas.update()
    chaoGroup.update()
    aboboraGroup.update()
    coinsGroup.update()


relogio = pygame.time.Clock() # FPS do jogo

pygame.font.init()
placar = 0
while True:
    relogio.tick(30)
    tela.fill(PRETO) #pintado de preto a tela

    fonte = pygame.font.SysFont('Arial', 35)
    contador = fonte.render(f'{placar}', True, [255,255,255]) 
    tela.blit(contador, [550, 50])

    #definindo eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()


    if fora_tela(chaoGroup.sprites()[0]):
        chaoGroup.remove(chaoGroup.sprites()[0])

        new_chao = Chao(CHAO_LARGURA - 20)
        chaoGroup.add(new_chao)


    if fora_tela(aboboraGroup.sprites()[0]):
        aboboraGroup.remove(aboboraGroup.sprites()[0])
        newAbobora = get_random_aboboras(TELA_LARGURA * 1)
        aboboraGroup.add(newAbobora)

        for i in range(100):
            newCoin = get_random_coins(TELA_LARGURA * i)
            coinsGroup.add(newCoin)


    if pygame.sprite.groupcollide(frames_fantasmas, coinsGroup, False, True):
        placar += 1


    if placar % 5 == 0 and placar != 0:
        GAME_SPEED += 0.02

    if pygame.sprite.groupcollide(frames_fantasmas, aboboraGroup, False, False):
        print("GAME OVERR")
        break
        
    if placar == 50:
        print('Voce ganhou')
        break

    desenhar = draw()
    desenhar
    atualizar = update()
    atualizar

    gameloop = True

    pygame.display.flip() #atualizando a tela

