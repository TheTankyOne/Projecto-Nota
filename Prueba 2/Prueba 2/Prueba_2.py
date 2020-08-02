import pygame
from pygame.locals import *
import sys
# init debe ser declarado al inicio para que se pueda utilizar en todo el código
pygame.init()

ventana_x = 640
ventana_y = 480
DISPLAYSURF = pygame.display.set_mode((ventana_x,ventana_y))#, DOUBLEBUF)
pygame.display.set_caption('Map Rendering Demo')
FPSCLOCK = pygame.time.Clock()

class heroe(object):

	def __init__(self, x, y, fuente):
		self.x = x
		self.y = y
		fuente += "/"
		self.Dimi = pygame.image.load("Dimi.png")
		self.ancho = self.Dimi.get_width()
		self.alto = self.Dimi.get_height()
		self.velocidad = 5

	def draw(self, cuadro):
		cuadro.blit(self.Dimi,(self.x,self.y))

	def se_mueve_segun(self, k, iz, de, ar, ab):
		if k[iz] and self.x > self.velocidad:
			self.x -= self.velocidad

		if k[de] and self.x < ventana_x - self.ancho - self.velocidad:
			self.x += self.velocidad

		if k[ar] and self.y > self.velocidad:
			self.y -= self.velocidad

		if k[ab] and self.y < ventana_y - self.alto - self.velocidad:
			self.y += self.velocidad

def repintar_cuadro_juego():

	map_data = [
	[1, 1, 1, 1, 1, 1, 1],
	[1, 0, 0, 0, 0, 0, 0],
	[1, 0, 0, 0, 0, 0, 0],
	[1, 0, 0, 0, 0, 0, 0],
	[1, 0, 0, 0, 0, 0, 0],
	[1, 0, 0, 0, 0, 0, 0],
	[1, 0, 0, 0, 0, 0, 0]
	]               #the data for the map expressed as [row[tile]].
	
	wall = pygame.image.load('wall.png').convert_alpha()  #load images
	grass = pygame.image.load('grass.png').convert_alpha()
	
	TILEWIDTH = 64  #holds the tile width and height
	TILEHEIGHT = 64
	TILEHEIGHT_HALF = TILEHEIGHT//2
	TILEWIDTH_HALF = TILEWIDTH//2
	
	DISPLAYSURF.fill((0,0,0))
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
			centered_x = DISPLAYSURF.get_rect().centerx + iso_x # quiere el ancho de la ventana, pero el valor queda sobreestimado
			centered_y = DISPLAYSURF.get_rect().centery//2 + iso_y # quiere la mitad del alto, pero el valor lo aleja hacia abajo
			DISPLAYSURF.blit(tileImage, (centered_x, centered_y)) # Integra el bloque, pero no se muestra correctamente.
			

			# No se como, pero funcionó asi -> todo lo anterior reemplaza el fondo
def dimitri():
	# self NO VA ACÁ, self es una clausula para usarse dentro de una clase, y hace referencia a sus propios atributos
	dimi.draw(DISPLAYSURF)
		
dimi = heroe(ventana_x/2,ventana_y/2,"")

while True:

	FPSCLOCK.tick(30)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()

	teclas = pygame.key.get_pressed()
	dimi.se_mueve_segun(teclas,pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s)
	repintar_cuadro_juego()
	dimitri()
	pygame.display.update()
	pygame.display.flip()

