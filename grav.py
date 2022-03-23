import math
import pygame
import sys

class Constants:
    G = 6.67 * 10**-11
    TimeStep = 0.01

class Vector2d:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        return Vector2d(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Vector2d(self.x - other.x, self.y - other.y)

    def __mul__(self, multiplier):
        return Vector2d(self.x * multiplier, self.y * multiplier)

    def __truediv__(self, divisor):
        return Vector2d(self.x / divisor, self.y / divisor)

    def length(self):
        return math.sqrt(math.pow(self.x, 2) + math.pow(self.y, 2))

    def normalized(self):
        return self / self.length()

class CelestialObject:
    def __init__(self, mass, radius, position, velocity):
        self.mass = mass
        self.radius = radius
        self.position = position
        self.velocity = velocity

    def UpdatePosition(self):
        self.position += self.velocity * Constants.TimeStep

    def UpdateVelocity(self, otherCelestialObjects):
        acceleration = Vector2d(0, 0)
        for celestialBody in otherCelestialObjects:
            if celestialBody.position == self.position: continue
            offsetVector = celestialBody.position - self.position
            distance = offsetVector.length()
            side = offsetVector.normalized()
            force = Constants.G * celestialBody.mass / math.pow(distance, 2)

            #print(force, " ", offsetVector.x, " ", offsetVector.y)

            acceleration += side * force
        self.velocity += acceleration * Constants.TimeStep

class Universe:
    def __init__(self):
        self.bodies = []

    def AddBody(self, body):
        self.bodies.append(body)

    def StartSimulation(self):
        screenWidth = 1500
        screenHeight = 1000

        pygame.init()
        window = pygame.display.set_mode((screenWidth, screenHeight))

        while True:
            window.fill((64,64,64))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            for body in self.bodies:
                pygame.draw.circle(window, (255, 255, 255), [body.position.x + (screenWidth / 2), body.position.y + (screenHeight / 2)], body.radius, 0)
                body.UpdateVelocity(self.bodies)

            for body in self.bodies:
                body.UpdatePosition()
            
            pygame.display.update()

universe = Universe()
universe.AddBody(CelestialObject(1e14, 10, Vector2d(0, 100), Vector2d(5, 0)))
universe.AddBody(CelestialObject(1e14, 10, Vector2d(0, -100), Vector2d(-5, 0)))
universe.AddBody(CelestialObject(1e14, 10, Vector2d(100, 0), Vector2d(0, -5)))
universe.AddBody(CelestialObject(1e14, 10, Vector2d(-100, 0), Vector2d(0, 5)))
universe.StartSimulation()

input()