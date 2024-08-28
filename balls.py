import pygame
import numpy as np
import itertools
import math

pygame.init()

class Ball:
    def __init__(self, pos, radius, init_vel, color, mass = None):
        self.x = pos[0]
        self.y = pos[1]

        self.radius = radius
        self.v = init_vel

        if mass == None:
            self.mass = self.m_from_r()
        else:
            self.mass = mass

        self.color = color

    def kinetic_energy(self):
        return 0.5*self.mass*np.linalg.norm(self.v)**2
    
    def pos(self, pos):
        self.x = pos[0]
        self.y = pos[1]

    def m_from_r(self):
        return 4/3 * np.pi * self.radius**3
    
    def r_from_m(self):
        return (3/4 * self.mass / np.pi)**(1/3)

def coll(ball_1, ball_2):
    m1, m2 = ball_1.mass, ball_2.mass
    v1, v2 = np.array(ball_1.v), np.array(ball_2.v)
    v_rel = np.linalg.norm(v1 - v2)

    overlap = ball_1.radius + ball_2.radius - np.linalg.norm(np.array([ball_1.x, ball_1.y]) - np.array([ball_2.x, ball_2.y]))
    t_overlap = overlap / v_rel
    # print(f't_overlap = {t_overlap}')

    pos1 = np.array([ball_1.x, ball_1.y]) - v1 * t_overlap 
    pos2 = np.array([ball_2.x, ball_2.y]) - v2 * t_overlap 

    # print(f'radius1 + radius2 = {ball_1.radius + ball_2.radius}')
    # print(f'pos1 - pos2 = {np.linalg.norm(pos1-pos2)}')

    n = (pos1 - pos2) / np.linalg.norm(pos1 - pos2)
    t = np.array([-n[1], n[0]])

    # Velocities along the normal direction
    v1_n = np.dot(v1, n)
    v2_n = np.dot(v2, n)

    # Velocities along the tangential direction
    v1_t = np.dot(v1, t)
    v2_t = np.dot(v2, t)

    # New normal velocities after collision
    v1_n_new = (v1_n * (m1 - m2) + 2 * m2 * v2_n) / (m1 + m2)
    v2_n_new = (v2_n * (m2 - m1) + 2 * m1 * v1_n) / (m1 + m2)

    # Combine new velocities
    v1_new = v1_n_new * n + v1_t * t
    v2_new = v2_n_new * n + v2_t * t

    ball_1.pos(pos1)
    ball_2.pos(pos2)

    ball_1.v = v1_new
    ball_2.v = v2_new

    return ball_1, ball_2

screen_width = 500

win = pygame.display.set_mode((screen_width, screen_width)) #width, height

pygame.display.set_caption("First Game")
clock = pygame.time.Clock()

run = True
is_moving = False
collision = True

theta = np.random.uniform(0, 2*np.pi, 3)

ball_1 = Ball([100,250], 20, [5*np.cos(theta[0]), 5*np.sin(theta[0])], (255, 0, 0), mass = 2)
ball_2 = Ball([400,250], 30, [5*np.cos(theta[1]), 5*np.sin(theta[1])], (0, 0, 255), mass = 6)
ball_3 = Ball([250,250], 40, [5*np.cos(theta[2]), 5*np.sin(theta[2])], (0, 255, 0), mass = 16)
ball_4 = Ball([250,100], 30, [5*np.cos(theta[2]), 5*np.sin(theta[2])], (255, 255, 0), mass = 6)
ball_5 = Ball([250,350], 30, [5*np.cos(theta[2]), 5*np.sin(theta[2])], (0, 255, 255), mass = 6)
ball_6 = Ball([250,450], 30, [5*np.cos(theta[2]), 5*np.sin(theta[2])], (255, 0, 255), mass = 6)

balls = [ball_1, ball_2, ball_3, ball_4, ball_5, ball_6]

# Create a semi-transparent surface to fade the trail
trail_surface = pygame.Surface((screen_width, screen_width))
trail_surface.set_alpha(255)  # Set the transparency (0-255, where 255 is opaque)

k_e = 0
for ball in balls:
    k_e += ball.kinetic_energy()
print(f'initial kinetic energy = {k_e}')

while run:
    clock.tick(60)
    pygame.display.set_caption("Ball collision - FPS: {}".format(int(clock.get_fps())))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE]:
        if is_moving == True:
            is_moving = False
        else: is_moving = True
        pygame.time.delay(100)

    # if keys[pygame.K_r]:
    #     win.fill((0, 0, 0))
    #     x = 100
    #     y = 250
    #     theta = np.random.uniform(0, 2*np.pi)
    #     v = [vel*np.cos(theta), vel*np.sin(theta)]

    if is_moving == True:
        if collision == True:
            for pair in itertools.combinations(balls, 2):
                ball_1, ball_2 = pair
                pos1 = np.array([ball_1.x, ball_1.y])
                pos2 = np.array([ball_2.x, ball_2.y])
                v_rel = np.linalg.norm(np.array(ball_1.v) - np.array(ball_2.v))
                if np.linalg.norm(pos1-pos2) < ball_1.radius + ball_2.radius:
                    
                    ball_1, ball_2 = coll(ball_1, ball_2)
                    # print(f'radius1 + radius2 = {ball_1.radius + ball_2.radius}')
                    # print(f'pos1 - pos2 = {np.linalg.norm(np.array([ball_1.x, ball_1.y])-np.array([ball_2.x, ball_2.y]))}')
                    k_e = 0
                    for ball in balls:
                        k_e += ball.kinetic_energy()
                    print(f'kinetic energy = {k_e}')
                    #is_moving = False

        # for ball in balls:
        #     if ball.x > screen_width - ball.radius or ball.x < ball.radius:
        #         overlap = np.abs()
        #         ball.v[0] = -ball.v[0]
        #     if ball.y > screen_width - ball.radius or ball.y < ball.radius:
        #         ball.v[1] = -ball.v[1]
            
        #     ball.x += ball.v[0]
        #     ball.y += ball.v[1]

        for ball in balls:
            if ball.x > screen_width - ball.radius:
                overlap = np.abs(ball.x - screen_width + ball.radius)
                ball.x -= overlap
                ball.y -= overlap / ball.v[0] * ball.v[1]
                ball.v[0] = -ball.v[0]
            elif ball.x < ball.radius:
                overlap = np.abs(ball.radius - ball.x)
                ball.x += overlap
                ball.y -= overlap / ball.v[0] * ball.v[1]
                ball.v[0] = -ball.v[0]

            elif ball.y > screen_width - ball.radius:
                overlap = np.abs(ball.y - screen_width + ball.radius)
                ball.y -= overlap
                ball.x -= overlap / ball.v[1] * ball.v[0]
                ball.v[1] = -ball.v[1]

            elif ball.y < ball.radius:
                overlap = np.abs(ball.radius - ball.y)
                ball.y += overlap
                ball.x -= overlap / ball.v[1] * ball.v[0]
                ball.v[1] = -ball.v[1]

            ball.x += ball.v[0]
            ball.y += ball.v[1]

    #win.fill((0, 0, 0))
    win.blit(trail_surface, (0, 0))
    for ball in balls:
        pygame.draw.circle(win, ball.color, (ball.x, ball.y), ball.radius)
    pygame.display.update()

pygame.quit()

#la velocità relativa prima dell'urto è costante. Posso trovare la distanza relativa tra le due palle e sottraendo i due raggi trovare
#la lunghezza di intersezione. Dopodiché con la velocità relativa e la lunghezza di intersezione tra le due palle calcolare il tempo al quale
#c'è stato il contatto. Posso riportare indietro le palle sulla loro traiettoria di una distanza uguale alla loro velocità per il tempo.