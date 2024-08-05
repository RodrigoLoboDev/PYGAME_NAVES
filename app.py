import pygame
import random

# Tamaño de la pantalla
ANCHO = 800
ALTO = 600

# FPS
FPS = 30

# Colores RGB
NEGRO = (0,0,0)
BLANCO = (255,255,255)
ROJO = (255,0,0)
H_FA2F2F = (250,47,47)
VERDE = (0,255,0)
AZUL = (0,0,255)
AZUL2 = (64,64,255)
H_50D2FE = (94,210,254)

class Jugador(pygame.sprite.Sprite):
    # Sprite del jugador
    def __init__(self):
        # Heredamos el init de la clase Sprite de pygame
        super().__init__()
        # Rectangulo (jugador)
        self.image = pygame.image.load('image/nave.png').convert()
        self.image.set_colorkey(AZUL2) #transparencia
        # Obtiene el rectangulo (sprite)
        self.rect = self.image.get_rect()
        self.radius = 22
        # pygame.draw.circle(self.image, VERDE, self.rect.center, self.radius)
        # Centrar el rectangulo (sprite)
        self.rect.center = (ANCHO // 2, ALTO - 50)
        # Velocidad del personaje (inicial)
        self.velocidad_x = 0
        self.velocidad_y = 0
    
    def update(self):
        # Velocidad predeterminada cada vuelta del bucle si no pulsas nada
        self.velocidad_x = 0
        self.velocidad_y = 0

        # Mantiene las teclas pulsadas
        teclas = pygame.key.get_pressed()

        # Mueve el personaje hacia la izquierda
        if teclas[pygame.K_a]:
            self.velocidad_x = -10
        # Mueve el personaje hacia la derecha
        if teclas[pygame.K_d]:
            self.velocidad_x = 10
        # Mueve el personaje hacia arriba
        if teclas[pygame.K_w]:
            self.velocidad_y = -10
        # Mueve el personaje hacia abajo
        if teclas[pygame.K_s]:
            self.velocidad_y = 10
        # Tecla space para el Disparo
        if teclas[pygame.K_SPACE]:
            jugador.disparo()
            # jugador.disparo2()
        
        # Actualiza la velocidad del personaje
        self.rect.x += self.velocidad_x
        self.rect.y += self.velocidad_y

        # Limita el margen izquierdo
        if self.rect.left < 0:
            self.rect.left = 0
        
        # Limita el margen derecho
        if self.rect.right > ANCHO:
            self.rect.right = ANCHO
        
        # Limita el margen arriba
        if self.rect.top < 0:
            self.rect.top = 0
        
        # Limita el margen abajo
        if self.rect.bottom > ALTO:
            self.rect.bottom = ALTO
    
    def disparo(self):
        bala = Disparos(self.rect.centerx, self.rect.top + 20)
        sprites_disparos.add(bala)
    
    def disparo2(self):
        bala = Disparos(self.rect.centerx + 23, self.rect.top + 30)
        sprites_disparos.add(bala)


class Enemigos(pygame.sprite.Sprite):
    # Sprite del enemigo
    def __init__(self):
        # Heredamos el init de la clase Sprite de pygame
        super().__init__()
        # Rectangulo (jugador)
        self.image = pygame.image.load('image/enemigo.png').convert()
        self.image.set_colorkey(NEGRO)
        # Obtiene el rectangulo (sprite)
        self.rect = self.image.get_rect()
        self.radius = 48
        # pygame.draw.circle(self.image, ROJO, self.rect.center, self.radius)
        # ubicacion aletoria
        self.rect.x = random.randrange(ANCHO - self.rect.width)
        self.rect.y = random.randrange(ALTO - self.rect.height)
        # Velocidad del enemigo (inicial)
        self.velocidad_x = random.randrange(2,7)
        self.velocidad_y = random.randrange(2,7)

    def update(self):
        # Actualiza la velocidad del enemigo
        self.rect.x += self.velocidad_x
        self.rect.y += self.velocidad_y

        # Limita el margen izquierdo
        if self.rect.left < 0:
            self.velocidad_x += 1
        
        # Limita el margen derecho
        if self.rect.right > ANCHO:
            self.velocidad_x -= 1
        
        # Limita el margen arriba
        if self.rect.top < 0:
            self.velocidad_y += 1
        
        # Limita el margen abajo
        if self.rect.bottom > ALTO:
            self.velocidad_y -= 1
    

class Disparos(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load('image/disparo.png').convert(), (10,20))
        self.image.set_colorkey(NEGRO)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x

    def update(self):
        self.rect.y -= 25
        if self.rect.bottom < 0:
            self.kill()


# Inicializacion de Pygame, creacion de la ventana, titulo y control de reloj
pygame.init()
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego de Naves")
clock = pygame.time.Clock() # para controlar los FPS

# Cargar imagen de fondo
fondo = pygame.image.load('image/fondo.jpg').convert()
#Música de fondo
pygame.mixer.music.load('sonido/intergalactic_odyssey.ogg')
pygame.mixer.music.play(-1)

#Sonido
sonido_arriba = pygame.image.load('sonido/volume_up.png')
sonido_abajo = pygame.image.load('sonido/volume_down.png')
sonido_mute = pygame.image.load('sonido/volume_muted.png')
sonido_max = pygame.image.load('sonido/volume_max.png')

# Fuentes
fuente = pygame.font.Font(None, 74)
fuente_menu = pygame.font.Font(None, 54)
fuente_creditos = pygame.font.Font(None, 36)

# Grupo de sprites e instanciaciones
sprites_jugador = pygame.sprite.Group()
sprites_enemigos = pygame.sprite.Group()
sprites_disparos = pygame.sprite.Group()

for x in range(random.randrange(1, 10)):
    enemigo = Enemigos()
    sprites_enemigos.add(enemigo)
# Si el jugador se crea al ultimo se pondra por encima de los enemigos
jugador = Jugador()
sprites_jugador.add(jugador)

# Bucle de juego
ejecutando = True
game_over = False
en_menu = True
win = False

while ejecutando:
    # Es lo que especifica la velocidad del bucle de juego
    clock.tick(FPS)
    # Eventos  
    for event in pygame.event.get():
        # Se cierra y termina el bucle
        if event.type == pygame.QUIT:
            ejecutando = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and en_menu:
                en_menu = False

    if en_menu:
        pantalla.blit(fondo, (0, 0))  # Fondo del menú
        titulo = fuente_menu.render("Presiona ENTER para comenzar", True, BLANCO)
        creditos = fuente_creditos.render("Juego hecho por: Lobo Jesus Luis Rodrigo", True, BLANCO)
        pantalla.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, ALTO // 2 - titulo.get_height() // 2))
        pantalla.blit(creditos, (ANCHO // 2 - creditos.get_width() // 2, ALTO // 2 + titulo.get_height()))
        pygame.display.flip()

        # Control del audio
        keys = pygame.key.get_pressed()
        #Baja volumen
        if keys[pygame.K_9] and pygame.mixer.music.get_volume() > 0.0:
            pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() - 0.01)
            pantalla.blit(sonido_abajo, (670, 20))
        elif keys[pygame.K_9] and pygame.mixer.music.get_volume() == 0.0:
            pantalla.blit(sonido_mute, (670, 20))

        #Sube volumen
        if keys[pygame.K_0] and pygame.mixer.music.get_volume() < 1.0:
            pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() + 0.01)
            pantalla.blit(sonido_arriba, (670, 20))
        elif keys [pygame.K_0] and pygame.mixer.music.get_volume() == 1.0:
                pantalla.blit(sonido_max, (670, 20))

        #Desactivar sonido
        elif keys[pygame.K_m]:
            pygame.mixer.music.set_volume(0.0)
            pantalla.blit(sonido_mute, (670, 20))

        #Reactivar sonido
        elif keys[pygame.K_COMMA]:
            pygame.mixer.music.set_volume(1.0)
            pantalla.blit(sonido_max, (670, 20))

    elif not en_menu and game_over == False and win == False:
        # Actualización de sprites
        sprites_jugador.update()
        sprites_enemigos.update()
        sprites_disparos.update()

        # Colisiones
        colision_nave = pygame.sprite.spritecollide(jugador, sprites_enemigos, False, pygame.sprite.collide_circle)

        colisiones = pygame.sprite.groupcollide(sprites_enemigos, sprites_disparos, False, True)

        for enemigo in colisiones:
            enemigo.image = pygame.image.load('image/explocion.png')
            enemigo.velocidad_y += 7

        if colision_nave:
            game_over = True
        
        if len(sprites_enemigos) == 0:
            win = True

        # Fondo de pantalla
        pantalla.blit(fondo, (0, 0))

        # Dibujo de sprites y formas geométricas
        sprites_jugador.draw(pantalla)
        sprites_enemigos.draw(pantalla)
        sprites_disparos.draw(pantalla)

        # Eliminar enemigos que se han salido de la pantalla
        for enemigo in sprites_enemigos:
            if enemigo.rect.top > ALTO:
                enemigo.kill()

    elif not en_menu and game_over == False and win:
        # Mostrar mensaje de "Fin del juego"
        texto = fuente.render("WINNER", True, VERDE)
        pantalla.blit(texto, (ANCHO // 2 - texto.get_width() // 2, ALTO // 2 - texto.get_height() // 2))
    
    else:
        # Mostrar mensaje de "Fin del juego"
        texto = fuente.render("Fin del juego", True, ROJO)
        pantalla.blit(texto, (ANCHO // 2 - texto.get_width() // 2, ALTO // 2 - texto.get_height() // 2))

    # Actualiza el contenido de la pantalla
    pygame.display.flip()

pygame.quit()