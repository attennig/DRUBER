import pygame
import pygame.gfxdraw
import time
WINDOW_SIZE = 700
BACKGROUND_COLOR = (255, 255, 255)
WS_SIZE = 50
WS_OFFSET = WS_SIZE/2
WS_IMAGE_PATH = "../gui/figures/waystation_unit.png"
DRONE_SIZE = 25
DRONE_IMAGE_PATH = "../gui/figures/drone.png"
DRONE_OFFSET = WS_SIZE/2
PARCEL_SIZE = 25
PARCEL_IMAGE_PATH = "../gui/figures/parcel.png"
PARCEL_OFFSET = 0

class Draw:
    def __init__(self, simulation):
        self.scale = lambda x: x * WINDOW_SIZE / simulation.AoI_SIZE
        pygame.init()
        self.initWindow()
        self.initializeEnvironment(simulation)

    def initWindow(self):
        self.display_surface = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        pygame.display.set_caption('Simulation')
        self.display_surface.fill(BACKGROUND_COLOR)



    def initializeEnvironment(self, simulation):
        for wID in simulation.wayStations.keys():
            scaledX = self.scale(simulation.wayStations[wID].x)
            scaledY = self.scale(simulation.wayStations[wID].y)
            for unit in range(simulation.wayStations[wID].capacity):
                self.drawIMG(WS_IMAGE_PATH, scaledX+(unit*WS_SIZE), scaledY, WS_SIZE, WS_OFFSET)
            nDrones = 0
            for uID in simulation.drones.keys():
                if simulation.drones[uID].homeWS.ID == wID:
                    scaledX = self.scale(simulation.drones[uID].homeWS.x)
                    scaledY = self.scale(simulation.drones[uID].homeWS.y)
                    self.drawIMG(DRONE_IMAGE_PATH, scaledX+(nDrones*WS_SIZE), scaledY, DRONE_SIZE, DRONE_OFFSET)
                    nDrones += 1
            nDeliveries = 0
            for dID in simulation.deliveries.keys():
                if simulation.deliveries[dID].src.ID == wID:
                    scaledX = self.scale(simulation.deliveries[dID].src.x)
                    scaledY = self.scale(simulation.deliveries[dID].src.y)
                    self.drawIMG(PARCEL_IMAGE_PATH, scaledX+(nDeliveries*WS_SIZE), scaledY, PARCEL_SIZE, PARCEL_OFFSET)
                    nDeliveries += 1
        pygame.display.update()
        pygame.time.delay(1000)
        pygame.image.save(self.display_surface, f"../gui/figures/out/scenario{simulation.n}out.png")



    def drawIMG(self, path, x, y, size, offset):
        image = pygame.image.load(path)
        image = pygame.transform.scale(image, (size, size))
        self.display_surface.blit(image, (x-offset, y-offset))