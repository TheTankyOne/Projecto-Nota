import pygame
from pygame.locals import *
import sys
import random
# init debe ser declarado al inicio para que se pueda utilizar en todo el código
pygame.init()
tutoriales = pygame.image.load("controles.png")
ventana_x = 1200
ventana_y = 700
DISPLAYSURF = pygame.display.set_mode((ventana_x,ventana_y))#, DOUBLEBUF)
pygame.display.set_caption('Map Rendering Demo')
FPSCLOCK = pygame.time.Clock()
class imagenes(object):
	def __init__(self,x,y,fuente):
		self.x = x
		self.y = y
		self.quieto = pygame.image.load("controles.png")
	def draw(self, cuadro):
		cuadro.blit(self.quieto, (self.x, self.y))
class personaje(object):

	def __init__(self, x, y, fuente, limite,salud):
		self.x = x
		self.y = y
		self.velocidad = 5
		#Atributos para salto
		self.ha_saltado = False
		self.impulso_salto = 10
		#Atributos para animación de Sprites
		self.va_izquierda = False
		self.va_derecha = False
		self.contador_pasos = 0
		fuente += "/"
		self.camina_izquierda = [pygame.image.load("img/"+fuente+"L1.png"),pygame.image.load("img/"+fuente+"L2.png"),pygame.image.load("img/"+fuente+"L3.png"),pygame.image.load("img/"+fuente+"L4.png"),pygame.image.load("img/"+fuente+"L5.png"),pygame.image.load("img/"+fuente+"L6.png"),pygame.image.load("img/"+fuente+"L7.png"),pygame.image.load("img/"+fuente+"L8.png"),pygame.image.load("img/"+fuente+"L9.png")]
		self.camina_derecha = [pygame.image.load("img/"+fuente+"R1.png"),pygame.image.load("img/"+fuente+"R2.png"),pygame.image.load("img/"+fuente+"R3.png"),pygame.image.load("img/"+fuente+"R4.png"),pygame.image.load("img/"+fuente+"R5.png"),pygame.image.load("img/"+fuente+"R6.png"),pygame.image.load("img/"+fuente+"R7.png"),pygame.image.load("img/"+fuente+"R8.png"),pygame.image.load("img/"+fuente+"R9.png")]
		self.quieto = pygame.image.load("img/"+fuente+"standing.png")
		self.ancho = self.quieto.get_width()
		self.alto = self.quieto.get_height()
		#Controles de desplazamiento automático
		self.camino = [self.x,limite,self.y,limite]
		self.salud = salud
		self.salud_inicial = salud
		self.zona_impacto = (self.x + int(self.ancho/5), self.y + int(self.alto / 5), int(self.ancho*(3/5)),int(self.alto*(3/5)))
	def villano_salud (self,extra):
		self.salud * [extra]
	def draw(self, cuadro):
		#Son 9 imágenes de la animación, para que cada una dure 3 vueltas de ciclo se multiplica por 3
		if self.contador_pasos + 1 > 27:
			self.contador_pasos = 0

		if self.va_izquierda:
			cuadro.blit(self.camina_izquierda[self.contador_pasos//3],(self.x,self.y))
			self.contador_pasos += 1
		elif self.va_derecha:
			cuadro.blit(self.camina_derecha[self.contador_pasos//3],(self.x,self.y))
			self.contador_pasos += 1
		else:
			cuadro.blit(self.quieto, (self.x,self.y))
		pygame.draw.rect(cuadro, (255,0,0), (self.x+5, self.y - 20, self.salud_inicial * 5, 10))
		pygame.draw.rect(cuadro, (0,71,0), (self.x+5, self.y - 20, self.salud * 5, 10))
		self.zona_impacto = (self.x + int(self.ancho/5), self.y + int(self.alto / 5), int(self.ancho*(3/5)),int(self.alto*(3/5)))
		pygame.draw.rect(cuadro, (250,0,0), self.zona_impacto,2)

	def se_mueve_segun(self, k, iz, de, ar, ab):
		if k[iz] and self.x > self.velocidad:
			self.x -= self.velocidad
			#Controles de animación
			self.va_izquierda = True
			self.va_derecha = False
		if k[de] and self.x < ventana_x - self.ancho - self.velocidad:
			self.x += self.velocidad
			#Controles de animación
			self.va_derecha = True
			self.va_izquierda = False
		if k[ar] and self.y > self.velocidad:
			self.y -= self.velocidad
		if k[ab] and self.y < ventana_y - self.alto - self.velocidad:
			self.y += self.velocidad
		
		#Controles de animación en caso de dejar de moverse en horizonal
		self.va_izquierda = False
		self.va_derecha = False
		self.contador_pasos = 0

	def se_mueve_solo(self,nivel, movement_random):	
		if movement_random == 1:
			if self.x + self.velocidad <= self.camino[1]:
				self.x += self.velocidad * nivel * 2.3
				#self.va_derecha = True
				#self.va_izquierda = False
			else:
				self.velocidad = self.velocidad * -1
				self.contador_pasos = 0
		if movement_random == 2:
			if self.x - self.velocidad >= self.camino[0]:
				self.x += self.velocidad * nivel * 2.3
				#self.va_izquierda = True
				#self.va_derecha = False
			else:
				self.velocidad = self.velocidad * -1
				self.contador_pasos = 0
		if movement_random == 3:
			if self.y - self.velocidad >= self.camino[3]:
				self.y += self.velocidad * nivel * 2.3
				self.velocidad = self.velocidad * -1
			else:
				self.velocidad = self.velocidad * -1
				self.contador_pasos = 0
		if movement_random == 4:
			if self.y + self.velocidad <= self.camino[2]:
				self.y += self.velocidad * nivel * 2.3
				self.velocidad = self.velocidad * -1
			else:
				self.velocidad = self.velocidad * -1
				self.contador_pasos = 0
					
	def se_encuentra_con(self,alguien):
		R1_ab = self.zona_impacto[1] + self.zona_impacto[3]
		R1_ar = self.zona_impacto[1]
		R1_iz = self.zona_impacto[0]
		R1_de = self.zona_impacto[0] + self.zona_impacto[2]
		R2_ab = alguien.zona_impacto[1] + alguien.zona_impacto[3]
		R2_ar = alguien.zona_impacto[1]
		R2_iz = alguien.zona_impacto[0]
		R2_de = alguien.zona_impacto[0] + alguien.zona_impacto[2]

		return R1_de > R2_iz and R1_iz < R2_de and R1_ar < R2_ab and R1_ab > R2_ar
	def es_golpeado(self):
		self.salud -= 1
#Clase Proyectil
# Modificada para aceptar disparo guiado por el mouse
class proyectil(object):
    def __init__(self, x, y, radio, color, destino):
        self.x = x
        self.y = y
        self.radio = radio
        self.color = color
        self.destino = destino
        # se calcula la PENDIENTE
        if self.destino[0] == self.x:
            self.m = None
        else:
            self.m = (destino[1] - y) / (destino[0] - x)
        # se almacena el valor del punto original
        self.x0 = self.x
        self.y0 = self.y
        # se establece una rapidez -> si deseas modificar la velocidad, modifica esta variable en su lugar
        self.rapidez = 34
        # se calcula la velocidad proporcionalmente para que se avanzara siempre en la misma rapidez
        self.velocidad = (self.rapidez * (destino[0] - x)) / (((destino[1] - y)**2 + (destino[0] - x)**2)**(0.5))
        self.zona_impacto = (self.x - self.radio, self.y - self.radio, self.radio*2, self.radio*2)

    def draw(self, cuadro):
        self.zona_impacto = (self.x - self.radio, self.y - self.radio, self.radio*2, self.radio*2)
        pygame.draw.circle(cuadro, self.color, (int(self.x), int(self.y)), int(self.radio))

    # funcion para realizar el movimiento del disparo en el eje x e y
    def se_mueve(self):
        # caso para los movimientos verticales
        if self.m == None:
            # caso si se dispara hacia arriba
            if self.destino[1] < self.y0:
                self.y -= self.rapidez
            # caso si se dispara hacia abajo
            else:
                self.y += self.rapidez
        # caso para el resto de movimientos
        else:
            # se crea nueva x 
            self.x += self.velocidad
            # se evalua la nueva y usando la ecuación de la recta correspondiente
            self.y = int(self.m * (self.x - self.x0) + self.y0)

    #Bala impacta a un personaje
    def impacta_a(self, alguien):
        if alguien.salud > 0:
            alguien.salud -= 1
        else:
            #alguien.es_visible = False
            del(alguien)

def crear_fondo():
	#Dibujar Héroe
	#heroe.draw(DISPLAYSURF)
	#Dibujar Villano
	#villano.draw(DISPLAYSURF)
	map_data = [
	[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	]               #the data for the map expressed as [row[tile]].
	
	wall = pygame.image.load('wall.png').convert_alpha()  #load images
	grass = pygame.image.load('grass.png').convert_alpha()
	
	TILEWIDTH = 64  #holds the tile width and height
	TILEHEIGHT = 64
	TILEHEIGHT_HALF = TILEHEIGHT//2
	TILEWIDTH_HALF = TILEWIDTH//2
	
	DISPLAYSURF.fill((254,1,154))
	for row_nb, row in enumerate(map_data):    #for every row of the map...
		for col_nb, tile in enumerate(row):

			if tile == 1:
				tileImage = wall
			else:
				tileImage = grass

			cart_x = row_nb * TILEWIDTH_HALF # numero fila por ancho del bloque
			cart_y = col_nb * TILEHEIGHT_HALF  # numero columna por alto del bloque
			iso_x = (cart_x - cart_y) # diferencia entre tamaños -> no tiene sentido
			iso_y = (cart_x + cart_y)//2 # la mitad de la suma de tamaños -> ni idea que es
			centered_x = DISPLAYSURF.get_rect().centerx + iso_x - 12 # quiere el ancho de la ventana, pero el valor queda sobreestimado
			centered_y = DISPLAYSURF.get_rect().centery//2 + iso_y - 210 # quiere la mitad del alto, pero el valor lo aleja hacia abajo
			DISPLAYSURF.blit(tileImage, (centered_x, centered_y)) # Integra el bloque, pero no se muestra correctamente.
def repintar_cuadro_juego():
	#Dibujar fondo del nivel
	crear_fondo()
	for bala in balas:
		bala.draw(DISPLAYSURF)
	#Dibujar Héroe
	heroe.draw(DISPLAYSURF)
	#Dibujar Villano
	villano.draw(DISPLAYSURF)
	puntos = texto_puntos.render('Puntaje: ' + str(puntaje), 1, (0, 0, 0))
	nivel_actual = texto_nivel.render('Nivel: ' + str(nivel), 1, (0, 0, 0))
	DISPLAYSURF.blit(puntos, (350, 10))
	DISPLAYSURF.blit(nivel_actual, (350, 30))
	#DISPLAYSURF.blit(nivel_actual, (350, 30))
	pygame.display.update()
def pint_tut():

	tuto.draw(DISPLAYSURF)
	#Se refresca la imagen	
# No se como, pero funcionó asi -> todo lo anterior reemplaza el fondo
def subir_nivel():
	global nivel
	global nivel_maximo
	global villano
	global musica_fondo
	global ventana
	global esta_jugando
	
	nivel += 1#Marca subida de nivel
	#Texto de subida de nivel
	texto = pygame.font.SysFont('comicsans',100)
	marcador = texto.render('GANASTE!', 1, (255,0,0))
	DISPLAYSURF.blit(marcador, (250 - (marcador.get_width()/2),200))
	pygame.display.update()
	pygame.time.delay(2000)
	#Se verifica si paso el ultimo nivel
	#En caso de pasar el ultimo nivel, gana el juego y termina el ciclo del juego (esta_jugando)
	if nivel >	 nivel_maximo:
		pygame.mixer.music.stop()
		esta_jugando = False
	#En caso de pasar un nivel intermedio, se actualiza el villano y la musica de acuerdo al nuevo nivel
	else:
		villano = villanos[nivel]
		
		#ver si es necesaria la consulta... observacion inicial NO SIRVE xd
		#if pygame.mixer.music.get_busy():
		##pygame.mixer.music.stop()
		##musica_fondo = pygame.mixer.music.load(ruta_musica[nivel])
		##pygame.mixer.music.play(-1)

repetir = True
while repetir:
	
	nivel =0
	nivel_maximo = 3
	puntaje = 0 
	texto_puntos = pygame.font.SysFont('comicsans', 20, True)
	texto_nivel = pygame.font.SysFont('comicsans', 20, True)
	texto_intro = pygame.font.SysFont('console', 20, True)
	texto_resultado = pygame.font.SysFont('console', 58, True)
	esta_en_intro = True
	gana = False
	personaje_intro = personaje(50, 150, "heroe", 700, 0)
	#personajes
	heroe = personaje(int(ventana_x/2 - 64),int(ventana_y/2),"heroe", ventana_x, 10)
	#villano = personaje(int(ventana_x/2 + 25),int(ventana_y/2 + 50),"villano",int(ventana_x/2 + 60))
	villanos = [personaje(ventana_x/2 + 143, random.randint(0,ventana_y), "villano", 800,13) , personaje(ventana_x/2 + 143,random.randint(0,ventana_y), "villano", 800,26),
             personaje(ventana_x/2 + 143,random.randint(0,ventana_y), "villano", 800, 49), personaje(ventana_x/2 + 143, random.randint(0,ventana_y), "villano", 800,66)]
	#salud_villano = villano_salud(nivel)
	villano = villanos[nivel]
	tuto = imagenes(ventana_x/2 - 152,ventana_y/2, "controles")
	
	#balas
	tanda_disparos = 0
	balas = []
	#sonido_bala = pygame.mixer.Sound('snd/bullet.wav')
	#sonido_golpe = pygame.mixer.Sound('snd/hit.wav')
	while esta_en_intro:
        # control de velocidad del juego
		FPSCLOCK.tick(27)
        # evento de boton de cierre de ventana
		for evento in pygame.event.get():
			if evento.type == pygame.QUIT:
				quit()

		DISPLAYSURF.fill((0, 0, 0))  # pinta el fondo de negro
		titulo = texto_intro.render('Dimitri´s colliseum', 1, (255, 0, 0))
		personaje_intro.se_mueve_solo(2,1)
		pint_tut()
		instrucciones = texto_intro.render(
            'Presione ENTER para continuar...', 1, (255, 255, 255))
		DISPLAYSURF.blit(titulo, ((ventana_x//2)-titulo.get_width()//2, 10))
		DISPLAYSURF.blit(instrucciones, ((ventana_x//2) - instrucciones.get_width()//2, 300))

		tecla = pygame.key.get_pressed()

		if tecla[pygame.K_RETURN]:
			esta_en_intro = False
			esta_jugando = True

		personaje_intro.draw(DISPLAYSURF)
		pygame.display.update()

	while esta_jugando:
		FPSCLOCK.tick(27)
		# evento de boton de cierre de ventana
		for evento in pygame.event.get():
			if evento.type == pygame.QUIT:
				pygame.quit()

		teclas = pygame.key.get_pressed()
		heroe.se_mueve_segun(teclas,pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s)
		random_movement = [1,2,3,4]
		movement_random = random.choice(random_movement)
		
		villano.se_mueve_solo(nivel, movement_random)
		if heroe.se_encuentra_con(villano):
			heroe.es_golpeado()
		
		
		if tanda_disparos > 0:
			tanda_disparos += 1
		if tanda_disparos > 3:
			tanda_disparos = 0

		maus = pygame.mouse.get_pressed()

        #contacto de proyectil con el villano
		for bala in balas:
			if villano.se_encuentra_con(bala):
				#sonido_golpe.play()  # al momento de impactar en el villano
				bala.impacta_a(villano)
				puntaje += 1
				balas.pop(balas.index(bala))  # se elimina la bala del impacto

            # movimiento de la bala dentro de los limites de la ventana
			if bala.x < ventana_x and bala.x > 0 and bala.y < ventana_y and bala.y > 0:
				bala.se_mueve() # se lanza la funcion de movimiento del disparo
			else:
				try:
					balas.pop(balas.index(bala))
					villano.x = random.randint(0,ventana_x)
					villano.y = random.randint(0,ventana_y)
				except:
					villano.x = random.randint(0,ventana_x)
					villano.y = random.randint(0,ventana_y)
					

        # capturar evento del disparo con el click (click izquierdo)
		if maus[0] and tanda_disparos == 0:
            # se captura la posicion (x,y) del mouse
			destino = pygame.mouse.get_pos()
			if len(balas) < 5:  # balas en pantalla
				balas.append(proyectil(round(heroe.x + heroe.ancho // 2), round(heroe.y + heroe.alto // 2), 6, (0, 153, 255), destino))
			#sonido_bala.play()  # al momento de disparar
			tanda_disparos = 1
		if villano.salud <= 0:
			subir_nivel()
		#Consulta para saber si perdimos
		if heroe.salud <= 0:
			esta_jugando = False
		repintar_cuadro_juego()
		    # Seccion de pantalla final
	final = True
	while final:
        # evento de boton de cierre de ventana
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quit()
		DISPLAYSURF.fill((0, 0, 0))  # pinta el fondo de negro
		titulo = texto_intro.render('JUEGO TERMINADO', 1, (255, 0, 0))
		if puntaje > 196 :
			resultado = texto_resultado.render('HAS GANADO!', 1, (255, 0, 0))
		else:
			resultado = texto_resultado.render('HAS PERDIDO!, GIT GUD SCRUB', 1, (255, 0, 0))
		pts = texto_intro.render('Puntaje Total: '+str(puntaje), 1, (255, 255, 255))
		instrucciones = texto_intro.render(
            'Presione ENTER para cerrar...', 1, (255, 255, 255))
		reintentar = texto_intro.render(
            'Presione R para volver al juego...', 1, (255, 255, 255))
		DISPLAYSURF.blit(titulo, ((ventana_x//2)-titulo.get_width()//2, 10))
		DISPLAYSURF.blit(resultado, ((ventana_x//2)-resultado.get_width()//2, 200))
		DISPLAYSURF.blit(pts, ((ventana_x//2)-titulo.get_width()//2, 100))
		DISPLAYSURF.blit(instrucciones, ((ventana_x//2) -
                               instrucciones.get_width()//2, 300))
		DISPLAYSURF.blit(reintentar, ((ventana_x//2)-reintentar.get_width()//2, 350))
		pygame.display.update()

		tecla = pygame.key.get_pressed()

		if tecla[pygame.K_RETURN]:
			repetir = False
			final = False

		if tecla[pygame.K_r]:
			repetir = True
			final = False
            # se asegura de eliminar los objetos de cada personaje
			del(heroe)
			del(villano)
		#pygame.display.flip()
pygame.quit()