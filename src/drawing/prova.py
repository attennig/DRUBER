# import pygame module in this program
import pygame

pygame.init()

white = (255, 255, 255)

X = 400
Y = 400

display_surface = pygame.display.set_mode((X, Y))

pygame.display.set_caption('Image')

image = pygame.image.load("drone.png")



running = 1
x= 5
y = 5
while running:
    x +=1
    y +=1
    display_surface.fill(white)
    display_surface.blit(image, (x, y))
    #pygame.display.flip()
    pygame.display.update()