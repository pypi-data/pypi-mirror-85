import time
import pygame as pg

tempo = time.process_time()
pg.init()
screen = pg.display.set_mode((1000,600))
fonte = pg.font.SysFont(None, 40)
msg = "Dumbdan is Comming Soon..."
texto = fonte.render(msg, 1, (255, 255, 255))

sent = True
while sent:

    for event in pg.event.get():
        if event.type == pg.QUIT or tempo > 5: 
            sent = False

    screen.fill((0,0,0))
    screen.blit(texto, (600,300))
    pg.display.flip()
    pg.display.update()
    tempo = time.process_time()
    

pg.quit()
