import pygame, random
from pygame.locals import*
from sys import exit
pygame.init()

#Caracteristicas;
largura = 1200
altura = 600
tela = pygame.display.set_mode((largura,altura))
velicidade = 10
velocidade_jogo = 10

barra_largura = 2 * largura
barra_altura = 40

game_window = pygame.display.set_mode([largura, altura])
pygame.display.set_caption('Space Run')

fundo = pygame.image.load('screen/ceu_format.png')
fundo = pygame.transform.scale(fundo,[largura, altura])

pygame.mixer.music.set_volume (0.6)
mscInicio = pygame.mixer.music.load('sons/M83 - Midnight City.mp3')
pygame.mixer.music.play(-1)

icon= pygame.image.load('screen/icon.webp')
pygame.display.set_icon(icon)

#Classes:
class Jogador(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_voo = [pygame.image.load('sprites/nave_1.png').convert_alpha(),
                          pygame.image.load('sprites/nave_2.png').convert_alpha(),
                          pygame.image.load('sprites/nave_3.png').convert_alpha(),
                          pygame.image.load('sprites/nave_4.png').convert_alpha(),
                          ]
        self.image_fall = pygame.image.load('sprites/nave_3.png').convert_alpha()
        self.image = pygame.image.load('sprites/nave_2.png').convert_alpha()
        self.rect = pygame.Rect(100, 100, 100, 100)
        self.mask = pygame.mask.from_surface(self.image)
        self.current_image = 0


    def update(self, *args):
        def move_player(self):
            key = pygame.key.get_pressed()
            if key[pygame.K_LEFT]:
                self.rect[0] -= velocidade_jogo
            if key[pygame.K_RIGHT]:
                self.rect[0] += velocidade_jogo
                self.current_image = (self.current_image + 1) % len (self.image_voo)
                self.image = self.image_voo [self.current_image]
                self.image = pygame.transform.scale (self.image,[110, 110] )
        move_player(self)
        self.rect[1] += velicidade

        def voo(self):
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE]:
                self.rect[1] -= 30
                self.image = pygame.image.load('sprites/nave_3.png').convert_alpha()
                self.image = pygame.transform.scale(self.image, [110, 110])
                
        voo(self)

        def queda(self):
            key = pygame.key.get_pressed()
            if not pygame.sprite.groupcollide(grupoPlayer, grupoChao, False, False) and not key[pygame.K_SPACE]:
                self.image = self.image_fall
                self.image = pygame.transform.scale(self.image, [110, 110])
        
        queda(self)

class Chão(pygame.sprite.Sprite):
    def __init__(self, xpos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('sprites/barra.webp').convert_alpha()
        self.image = pygame.transform.scale(self.image,(barra_largura, barra_altura))
        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        self.rect[1] = altura - barra_altura

    def update(self, *args):
        self.rect[0] -=  velocidade_jogo

class Obstaculos(pygame.sprite.Sprite):
    def __init__(self, xpos, ysize):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('sprites/obstaculo.png').convert_alpha() 
        self.image = pygame.transform.scale(self.image, [150, 150])
        self.rect = pygame.Rect(100, 100, 100, 100)
        self.rect[0] = xpos
        self.mask = pygame.mask.from_surface(self.image)
        self.rect[1] = altura - ysize
        
    def update(self, *args):
        self.rect[0] -= velocidade_jogo
        

class Moeda(pygame.sprite.Sprite):
    def __init__(self, xpos, ysize):

        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('sprites/moeda.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, [45, 45])
        self.rect = pygame.Rect(100, 100, 20, 20)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect[0] = xpos
        self.rect[1] = altura - ysize
        
         
    def update (self, *args):
        self.rect[0] -= velocidade_jogo
        
def randomObstaculos (xpos):
    tam = random.randint(120, 550)
    meteoro = Obstaculos(xpos, tam)
    return meteoro

def randomMoedas (xpos):
    tam_2 = random.randint(100, 600)
    moeda = Moeda(xpos, tam_2)
    return moeda

def foraTela (sprite):
    return sprite.rect[0] < -(sprite.rect[2])

pygame.init()

#Grupos:
grupoPlayer = pygame.sprite.Group()
player = Jogador()
grupoPlayer.add(player)

grupoChao = pygame.sprite.Group()
for c in range(2):
    chao = Chão(largura * c)
    grupoChao.add(chao)

grupoMoedas = pygame.sprite.Group()
for c in range(10):
    moeda = randomMoedas(largura * c + 700)
    grupoMoedas.add(moeda)

grupoObstaculo = pygame.sprite.Group()
for c in range(2):
    obstaculo = randomObstaculos(largura * c + 700)
    grupoObstaculo.add(obstaculo)

gameloop = True
def draw():
    grupoPlayer.draw(game_window)
    grupoChao.draw(game_window)
    grupoObstaculo.draw(game_window)
    grupoMoedas.draw(game_window)

def update():
    grupoChao.update()
    grupoPlayer.update()
    grupoObstaculo.update()
    grupoMoedas.update()

clock = pygame.time.Clock()
placar = 0

#Tela de inicio:
play_game = pygame.image.load('screen/opengame.jpg')
play_game = pygame.transform.scale(play_game, (largura, altura))

instr = pygame.image.load('screen/instruçoes.png')
instr = pygame.transform.scale(instr, (largura, altura))

inicio = True
openInstruçoes = False

while inicio:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == KEYDOWN:
            if event.key == K_RETURN:
                inicio = False
            

            elif event.key == K_i:  
                openInstruçoes = True

    if openInstruçoes:
        game_window.blit(instr, (0, 0))
    else:
        game_window.blit(play_game, (0, 0))
    
    
    pygame.display.flip()

#Loop principal do jogo:
while gameloop:
    clock.tick(35)
    game_window.blit(fundo, (0, 0))
    font = pygame.font.Font('fonte.ttf', 25)
    text = font.render('PLACAR', True, [255,255,255])
    game_window.blit(text, [1100, 20])
    contador = font.render(f'{placar}', True, [255,255,255])
    game_window.blit(contador, [1125, 50])


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() 
            break
    
    if foraTela(grupoChao.sprites()[0]):
        grupoChao.remove(grupoChao.sprites()[0])
        chaoNew = Chão (largura - 30)
        grupoChao.add (chaoNew)

    if foraTela(grupoObstaculo.sprites()[0]): 
        grupoObstaculo.remove(grupoObstaculo.sprites()[0])
        obstaculoNew = randomObstaculos (largura * 1.4)
        grupoObstaculo.add(obstaculoNew)
        
        moeda0 = randomMoedas(largura * 2.0)
        moeda1 = randomMoedas(largura * 2.2)
        moeda2 = randomMoedas(largura * 2.4)
        moeda3 = randomMoedas(largura * 3.8)
        
        grupoMoedas.add(moeda0)
        grupoMoedas.add(moeda1)
        grupoMoedas.add(moeda2)
        grupoMoedas.add(moeda3)


        def get_random_obstacles_and_coins(xpos):
            tam_obstaculo = random.randint(120, 550)
            tam_moeda = random.randint(100, 600)

            while tam_obstaculo - 150 < tam_obstaculo < tam_moeda + 150:  
                tam_obstaculo = random.randint (120, 550)  

                meteoro = Obstaculos(xpos, tam_obstaculo)
                moeda = Moeda(xpos, tam_moeda)

                return moeda, meteoro
        
    if pygame.sprite.groupcollide(grupoPlayer, grupoChao, False, False):
        velicidade = 0
    else:
        velicidade = 10

    if pygame.sprite.groupcollide(grupoPlayer, grupoMoedas, False, True):
        placar += 1

    if placar % 1 == 0 and placar != 0:
        velocidade_jogo += 0.03
        
       
#Game Over:
    if pygame.sprite.groupcollide(grupoPlayer, grupoObstaculo, False, False):
        pygame.mixer.music.pause()

        coll_sound = pygame.mixer.Sound('sons/effect.mp3')
        coll_sound.set_volume(0.3)
        coll_sound.play()

        end_game = pygame.image.load('screen/overGame.png')
        end_game= pygame.transform.scale(end_game, (largura, altura))

        morreu = True
        while morreu:
          tela.fill((0,0,0))
          for event in pygame.event.get():
             if event.type == QUIT:
              pygame.quit ()
              exit()
             if event.type == KEYDOWN:
              if event.key == K_r:
                pygame.quit ()
                exit()
             
          game_window.blit(end_game, (0, 0))

    
          pygame.display.flip()
          pygame.display.update()
 
        break



    





    update()
    draw()
    pygame.display.flip ()
    pygame.display.update()