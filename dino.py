import pygame


# innciamos pygame
pygame.init()

# definir colores 
BLANCO = (255,255,255)
NEGRO = (0,0,0)

# size pantalla
info = pygame.display.Info()
ANCHO_PANTALLA = info.current_w
ALTO_PANTALLA = info.current_h

# crear ventana
pantalla =pygame.display.set_mode((ANCHO_PANTALLA,ALTO_PANTALLA))
pygame.display.set_caption("DINO GAME")

reloj = pygame.time.Clock()


# el dinosaurio
class Dino(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('dino.png').convert_alpha()
        self.rect =self.image.get_rect()
        self.rect.x = 50           
        self.rect.y = ALTO_PANTALLA - self.rect.height
        self.jump = False
        self.velocidad_jump = 15

    def update(self):
        if self.jump:
            self.rect.y -= self.velocidad_jump
            self.velocidad_jump -= 1      
            if self.velocidad_jump < -15:
                self.jump = False
                self.velocidad_jump = 15

    def jumping(self):
        if not self.jump:
            self.jump = True
#spike el cactus
class cactus(pygame.sprite.Sprite):
    def __init__(self,velocidad):
        super().__init__()
        self.image = pygame.image.load('cactus.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = ANCHO_PANTALLA
        self.rect.y = ALTO_PANTALLA - self.rect.height + 20
        self.speed = velocidad

    def update(self):
        self.rect.x -= self.speed
        if self.rect.x < -20:
            self.kill



all_sprites = pygame.sprite.Group()
obstaculos = pygame.sprite.Group()
trex = Dino()
all_sprites.add(trex)

contador_cactus = 0

font = pygame.font.SysFont('Sans',50)

Score = 0

def mostrar_game_over():
    pantalla.fill(BLANCO)
    text_game_over = font.render("GAME OVER", True, NEGRO)
    text_score = font.render(f'SCORE:{Score}', True, NEGRO)
    text_retry = font.render("PRESS [Y] TO RETRY", True, NEGRO)
    pantalla.blit(text_game_over, (ANCHO_PANTALLA // 2 - text_game_over.get_width() // 2, ALTO_PANTALLA // 2 - text_game_over.get_height() // 2))
    pantalla.blit(text_score, (ANCHO_PANTALLA // 2 - text_score.get_width() // 2, ALTO_PANTALLA // 2 + text_game_over.get_height() // 2))
    pantalla.blit(text_retry, (ANCHO_PANTALLA // 2 - text_retry.get_width() // 2, ALTO_PANTALLA // 3 - text_retry.get_height() // 3))
    pygame.display.flip()
 
  # esperar hasta que se presione espacio para reiniciar
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_y:
                esperando = False

# función para reiniciar el juego
def reiniciar_juego():
    global all_sprites, obstaculos, trex, contador_cactus, Score
    all_sprites.empty()
    obstaculos.empty()
    trex = Dino()
    all_sprites.add(trex)
    contador_cactus = 0
    Score = 0



#bucle principal 
ejecutando = True
while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
            print ("salir")
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                trex.jumping()
                print=("salto")

#control de cactus
    if contador_cactus > 40:
        speed_spike = 10 + (Score // 100)
        spike = cactus(speed_spike)
        all_sprites.add(spike)
        obstaculos.add(spike)
        contador_cactus = 0
    contador_cactus += 1    

    all_sprites.update()

#lo que te mata
    colisiones = pygame.sprite.spritecollide(trex, obstaculos, False)
    for spike in obstaculos:
        hitbox_trex = trex.rect.inflate(-10,-10)
        if hitbox_trex.colliderect(spike.rect):
            colisiones = True
            break   
    if colisiones:
        ejecutando = False
        print = ("murido")
        mostrar_game_over()
        reiniciar_juego()
        ejecutando = True

    Score += 1
    pantalla.fill(BLANCO)       

    all_sprites.draw(pantalla)

#le puntaje
    text_score = font.render(f'SCORE:{Score}',True,NEGRO)
    pantalla.blit(text_score,(230, 10))

 
    pygame.display.flip()

    reloj.tick(30)

pygame.quit()   

#miguel ha jugado 104 37 veces dino game 


# pantalla game over y volver a jugar (completed) 
# que tenga la pantalla completa(completed) 
# que pueda elgir el presonaje 
# 
#   
