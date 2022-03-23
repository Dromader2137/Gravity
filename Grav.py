import pygame

import math

class Vector:

	def __init__ (self, x, y):		self.x = x

		self.y = y

		

	def __add__ (self, sec):

		return Vector(self.x + sec.x, self.y + sec.y)

		

	def __sub__ (self, sec):

		return Vector(self.x - sec.x, self.y - sec.y)

		

	def __mul__(self, sec):

		return Vector(self.x * sec, self.y * sec)

		

	def __truediv__ (self, sec):

		return Vector(self.x / sec, self.y / sec)

	

	def length(self):

		return math.sqrt(self.x*self.x + self.y*self.y)

		

	def magnitude(self):

		return self / self.length()

class CelestialBody:

	def __init__ (self, mass, radius, position, velocity):

		self.mass = mass

		self.radius = radius

		self.position = position

		self.velocity = velocity

		

	def UpdateVelocity(self, others, step):

		acceleration = Vector(0, 0)

		for body in others:

			if body == self: return

			positionVector = (body.position - self.position)

			dst = positionVector.length()

			mag = positionVector.magnitude()

			force = self.mass * body.mass * 200 / (dst*dst)

			acceleration += mag * force / self.mass

			print(dst, " ", force, " ", mag.x)

		self.velocity += acceleration * step

			

	def UpdatePosition(self, step):

		self.position += self.velocity * step

class Universe:

	def __init__ (self):

		self.planets = []

		

	def AddBody(self, body):

		self.planets.append(body)

		

	def StartSimulation(self):

		#pygame.init()

		

		#screen = pygame.display.set_mode((1080, 1920))

		#screen.fill((128,128,128))

		

		running = True

		

		for i in range(100):

			#screen.fill((128,128,128))

			

			#for event in pygame.event.get():

				#if event.type == pygame.QUIT:

					#running = False

			

			for body in self.planets:

				#pygame.draw.circle(screen, (255, 0, 0), [body.position.x + 540, body.position.y + 960], body.radius, 0)

				body.UpdateVelocity(self.planets, 1)

			

			for body in self.planets:

				body.UpdatePosition(1)

				

			#pygame.display.update()

				

universe = Universe()

universe.AddBody(CelestialBody(1000000, 40, Vector(0, 0), Vector(0, 0)))

universe.AddBody(CelestialBody(10000000, 40, Vector(100, 0), Vector(0, 0)))

universe.StartSimulation()

	

input()
