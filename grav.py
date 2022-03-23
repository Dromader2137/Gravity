import math
import pygame
import sys

class Constants:
    G = 6.67 * 10**-11
    TimeStep = 0.005

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
        self.acceleration = Vector2d(0, 0)
        for celestialBody in otherCelestialObjects:
            if celestialBody.position == self.position: continue
            offsetVector = celestialBody.position - self.position
            distance = offsetVector.length()
            side = offsetVector.normalized()
            force = Constants.G * celestialBody.mass / math.pow(distance, 2)

            #print(force, " ", offsetVector.x, " ", offsetVector.y)

            self.acceleration += side * force
        self.velocity += self.acceleration * Constants.TimeStep

class Universe:
    def __init__(self):
        self.bodies = []

    def AddBody(self, body):
        self.bodies.append(body)

    def StartSimulation(self):
        screenWidth = 1500
        screenHeight = 1000
        simTime = 0

        pygame.init()
        window = pygame.display.set_mode((screenWidth, screenHeight))

        myFont = pygame.font.SysFont('Comic Sans MS', 30)

        while True:
            window.fill((5,5,5))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            for body in self.bodies:
                body.UpdateVelocity(self.bodies)
                pygame.draw.circle(window, (200, 200, 200), [body.position.x + (screenWidth / 2), body.position.y + (screenHeight / 2)], body.radius, 0)
                pygame.draw.line(window, (255, 0, 0), (body.position.x + (screenWidth / 2), body.position.y + (screenHeight / 2)), (body.position.x + (screenWidth / 2) + body.velocity.x, body.position.y + (screenHeight / 2) + body.velocity.y), 4)
                pygame.draw.line(window, (0, 128, 255), (body.position.x + (screenWidth / 2), body.position.y + (screenHeight / 2)), (body.position.x + (screenWidth / 2) + body.acceleration.x, body.position.y + (screenHeight / 2) + body.acceleration.y), 4)

            for body in self.bodies:
                body.UpdatePosition()

            simTime += Constants.TimeStep

            textSurface = myFont.render(str(int(simTime)) + "s", False, (200, 200, 200))
            window.blit(textSurface, (20, 20))
            
            pygame.display.update()

universe = Universe()
universe.AddBody(CelestialObject(4e15, 20, Vector2d(300, 0), Vector2d(0, -2)))
universe.AddBody(CelestialObject(4e15, 20, Vector2d(-300, 0), Vector2d(0, 2)))
universe.StartSimulation()

input()
