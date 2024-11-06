import pygame
import os 

# iniciar pygame
pygame.init()
pygame.mixer.init()
# definir colores 
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

# tamaño de pantalla
info = pygame.display.Info()
ANCHO_PANTALLA = info.current_w
ALTO_PANTALLA = info.current_h

ruta_assets = 'assets'

# cargar archivos de sonido
sonido_salto = pygame.mixer.Sound(os.path.join(ruta_assets, 'salto.wav'))
sonido_colision = pygame.mixer.Sound(os.path.join(ruta_assets, 'colision.wav'))
sonido_game_over = pygame.mixer.Sound(os.path.join(ruta_assets, 'game_over.wav'))
pygame.mixer.music.load(os.path.join(ruta_assets, 'musica_fondo.wav'))  # cargar música de fondo
pygame.mixer.music.play(-1)  # reproducir música de fondo en bucle


# función para mostrar pantalla de selección de personajes
def seleccionar_personaje():
    seleccionando = True
    personajes = [os.path.join(ruta_assets, 'dino.png'), os.path.join(ruta_assets, 'mario.png')]
    seleccionado = 0
    while seleccionando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_m:
                    seleccionado = (seleccionado - 1) % len(personajes)
                if evento.key == pygame.K_d:
                    seleccionado = (seleccionado + 1) % len(personajes)
                if evento.key == pygame.K_RETURN:
                    seleccionando = False
        pantalla.fill(BLANCO)
        personaje_image = pygame.image.load(personajes[seleccionado])
        pantalla.blit(personaje_image, (ANCHO_PANTALLA // 2 - personaje_image.get_width() // 2, ALTO_PANTALLA // 2 - personaje_image.get_height() // 2))
        # Mostrar instrucciones
        font = pygame.font.SysFont('Sans', 30)
        text_instr = font.render("Presiona D para Dinosaurio o M para Mario", True, NEGRO)
        pantalla.blit(text_instr, (ANCHO_PANTALLA // 2 - text_instr.get_width() // 2, ALTO_PANTALLA // 2 + personaje_image.get_height()))
        pygame.display.flip()
    return personajes[seleccionado]

# el dinosaurio y mario
class Dino(pygame.sprite.Sprite):
    def __init__(self, imagen):
        super().__init__()
        self.image = pygame.image.load(imagen).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = ALTO_PANTALLA - self.rect.height
        self.jump = False
        self.velocidad_jump = 15

        # Animaciones para Dino y Mario
        if 'dino' in imagen:
            self.sprites_caminata = [pygame.image.load(f"dino{i}.png") for i in range(1, 5)]
        elif 'mario' in imagen:
            self.sprites_caminata = [pygame.image.load(f"mario{i}.png") for i in range(1, 5 )]

        self.indice_sprite = 0

    def update(self):
        if self.jump:
            self.rect.y -= self.velocidad_jump
            self.velocidad_jump -= 1
            if self.velocidad_jump < -15:
                self.jump = False
                self.velocidad_jump = 15

        # Animación de caminata
        self.indice_sprite = (self.indice_sprite + 1) % len(self.sprites_caminata)
        self.image = self.sprites_caminata[self.indice_sprite]

    def jumping(self):
        if not self.jump:
            self.jump = True
            sonido_salto.play()
# el cactus
class Cactus(pygame.sprite.Sprite):
    def __init__(self, velocidad):
        super().__init__()
        self.image = pygame.image.load('cactus.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = ANCHO_PANTALLA
        self.rect.y = ALTO_PANTALLA - self.rect.height + 20
        self.speed = velocidad

    def update(self):
        self.rect.x -= self.speed
        if self.rect.x < -20:
            self.kill()

# función para mostrar pantalla de Game Over
def mostrar_game_over():
    pantalla.fill(BLANCO)
    text_game_over = font.render("GAME OVER", True, NEGRO)
    text_score = font.render(f'SCORE:{Score}', True, NEGRO)
    text_retry = font.render("PRESS [Y] TO RETRY", True, NEGRO)
    pantalla.blit(text_game_over, (ANCHO_PANTALLA // 2 - text_game_over.get_width() // 2, ALTO_PANTALLA // 2 - text_game_over.get_height() // 2))
    pantalla.blit(text_score, (ANCHO_PANTALLA // 2 - text_score.get_width() // 2, ALTO_PANTALLA // 2 + text_game_over.get_height() // 2))
    pantalla.blit(text_retry, (ANCHO_PANTALLA // 2 - text_retry.get_width() // 2, ALTO_PANTALLA // 3 - text_retry.get_height() // 3))
    pygame.display.flip()
    sonido_game_over.play()

    # esperar hasta que se presione espacio para reiniciar
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_y :
                esperando = False

# función para reiniciar el juego
def reiniciar_juego():
    global all_sprites, obstaculos, trex, contador_cactus, Score
    all_sprites.empty()
    obstaculos.empty()
    trex = Dino(imagen_personaje)
    all_sprites.add(trex)
    contador_cactus = 0
    Score = 0

# seleccionar personaje antes de empezar
imagen_personaje = seleccionar_personaje()

all_sprites = pygame.sprite.Group()
obstaculos = pygame.sprite.Group()
trex = Dino(imagen_personaje)
all_sprites.add(trex)

contador_cactus = 0

font = pygame.font.SysFont('Sans', 50)

Score = 0

# bucle principal
ejecutando = True
while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
            print("salir")
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                trex.jumping()
                print("salto")
              

    # control de cactus
    if contador_cactus > 40:
        speed_spike = 10 + (Score // 100)
        spike = Cactus(speed_spike)
        all_sprites.add(spike)
        obstaculos.add(spike)
        contador_cactus = 0
    contador_cactus += 1    

    all_sprites.update()

    # lo que te mata
    colisiones = pygame.sprite.spritecollide(trex, obstaculos, False)
    for spike in obstaculos:
        hitbox_trex = trex.rect.inflate(-10, -10)
        if hitbox_trex.colliderect(spike.rect):
            colisiones = True
            break   
    if colisiones:
        ejecutando = False
        print("murido")
        sonido_colision.play()
        mostrar_game_over()
        reiniciar_juego()
        ejecutando = True

    Score += 1
    pantalla.fill(BLANCO)       

    all_sprites.draw(pantalla)

    # puntaje
    text_score = font.render(f'SCORE:{Score}', True, NEGRO)
    pantalla.blit(text_score, (230, 10))

    pygame.display.flip()
    reloj.tick(25)

pygame.quit()













