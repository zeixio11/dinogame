import pygame

# Configuración inicial
pygame.init()
ancho, alto =700,700
pantalla = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("Animación de caminar automática")

# Cargar los sprites de caminata     
sprites_caminata = [pygame.image.load(f"dino{i}.png") for i in range(1, 3)]
indice_sprite = 0
x, y = 500, 500  # Posición inicial del personaje
velocidad = 5
direccion = 1  # 1 significa derecha, -1 significa izquierda

# Animación de caminata
reloj = pygame.time.Clock()
corriendo = True
while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False

    # Actualizar posición y dirección
    x += velocidad * direccion
    indice_sprite = (indice_sprite + 1) % len(sprites_caminata)

    # Cambiar de dirección si llega al borde
    if x > ancho - 100 or x < 0:  # Ajusta el 100 al ancho del sprite
        direccion *= -1  # Cambiar de dirección

    # Dibujar en pantalla
    pantalla.fill((255, 255, 255))  # Fondo blanco
    sprite_actual = sprites_caminata[indice_sprite]

    # Reflejar el sprite según la dirección
    if direccion == -1:
        sprite_actual = pygame.transform.flip(sprite_actual, True, False)

    pantalla.blit(sprite_actual, (x, y))
    pygame.display.flip()
    reloj.tick(10)  # Controla la velocidad de la animación

pygame.quit()

import os
import pygame

# iniciar pygame
pygame.init()
pygame.mixer.init()

# definir colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

# tamaño de pantalla
ANCHO_PANTALLA = 700
ALTO_PANTALLA = 700

# ruta de la carpeta assets
ruta_assets = 'assets'

# cargar archivos de sonido
sonido_salto = pygame.mixer.Sound(os.path.join(ruta_assets, 'salto.wav'))
sonido_colision = pygame.mixer.Sound(os.path.join(ruta_assets, 'colision.wav'))
sonido_game_over = pygame.mixer.Sound(os.path.join(ruta_assets, 'game_over.wav'))
pygame.mixer.music.load(os.path.join(ruta_assets, 'musica_fondo.wav'))  # cargar música de fondo
pygame.mixer.music.play(-1)  # reproducir música de fondo en bucle

# crear ventana
pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pygame.display.set_caption("DINO GAME")
reloj = pygame.time.Clock()

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
            self.sprites_caminata = [pygame.image.load(os.path.join(ruta_assets, f"dino{i}.png")) for i in range(1, 3)]
        elif 'mario' in imagen:
            self.sprites_caminata = [pygame.image.load(os.path.join(ruta_assets, f"mario{i}.png")) for i in range(1, 3)]

        self.ind