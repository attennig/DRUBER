import pygame
from src.config import *

class Draw:
    def __init__(self, simulation):
        self.scale = lambda x: x * WINDOW_SIZE / simulation.AoI_SIZE
        pygame.init()
        # window initialization
        self.display_surface = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        pygame.display.set_caption(f"Simulation n.{simulation.n}")
        self.writer = pygame.font.SysFont(FONT_FAMILY,FONT_SIZE)


    def drawEnvironment(self, simulation, t):
        self.display_surface.fill(BACKGROUND_COLOR)
        label = self.writer.render(f"t: {t}", 1, FONT_COLOR)
        self.display_surface.blit(label, (1, 1))
        for wID in simulation.wayStations.keys():
            scaledX = self.scale(simulation.wayStations[wID].x)
            scaledY = self.scale(simulation.wayStations[wID].y)
            for unit in range(simulation.wayStations[wID].capacity):
                self.drawIMG(WS_IMAGE_PATH, scaledX+(unit*WS_SIZE), scaledY, WS_SIZE, WS_OFFSET)
            nDrones = 0
            for uID in simulation.drones.keys():
                if simulation.drones[uID].currentStation.ID == wID:
                    scaledX = self.scale(simulation.drones[uID].currentStation.x)
                    scaledY = self.scale(simulation.drones[uID].currentStation.y)
                    if simulation.drones[uID].isRecharging: self.drawIMG(RECHARGING_DRONE_IMAGE_PATH, scaledX+(nDrones*WS_SIZE), scaledY, DRONE_SIZE, DRONE_OFFSET)
                    else: self.drawIMG(DRONE_IMAGE_PATH, scaledX+(nDrones*WS_SIZE), scaledY, DRONE_SIZE, DRONE_OFFSET)
                    nDrones += 1
            nDeliveries = 0
            for dID in simulation.deliveries.keys():
                if simulation.deliveries[dID].currentStation.ID == wID:
                    scaledX = self.scale(simulation.deliveries[dID].currentStation.x)
                    scaledY = self.scale(simulation.deliveries[dID].currentStation.y)
                    self.drawIMG(PARCEL_IMAGE_PATH, scaledX+(nDeliveries*WS_SIZE), scaledY, PARCEL_SIZE, PARCEL_OFFSET)
                    nDeliveries += 1
        pygame.display.update()
        pygame.time.delay(GIF_INTERVAL)
        if SAVE: pygame.image.save(self.display_surface, f"{OUT_FOLDER}/scenario{simulation.n}_frame{t}.png")



    def drawIMG(self, path, x, y, size, offset):
        image = pygame.image.load(path)
        image = pygame.transform.scale(image, (size, size))
        self.display_surface.blit(image, (x-offset, y-offset))
