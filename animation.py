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

