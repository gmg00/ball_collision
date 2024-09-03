import pygame
import numpy as np
import itertools
from functions import coll  # Import the collision function from an external module
from Ball import Ball  # Import the Ball class from an external module

pygame.display.init()  # Initialize the display module of Pygame

screen_width = 500  # Set the screen width (and height, since the window is square)

# Create a window with the specified width and height
win = pygame.display.set_mode((screen_width, screen_width))  # width, height

pygame.display.set_caption("First Game")  # Set the window title
clock = pygame.time.Clock()  # Create a clock object to manage frame rate

# Create a semi-transparent surface to leave a trail effect behind the moving balls
trail_surface = pygame.Surface((screen_width, screen_width))
trail_surface.set_alpha(255)  # Set the transparency (0-255, where 255 is fully opaque)

# Generate random initial directions for six balls
theta = np.random.uniform(0, 2*np.pi, 6)

# Create six Ball objects with random initial directions and assign them different properties
ball_1 = Ball([100,250], 20, [5*np.cos(theta[0]), 5*np.sin(theta[0])], (255, 0, 0), mass=2)
ball_2 = Ball([400,250], 30, [5*np.cos(theta[1]), 5*np.sin(theta[1])], (0, 0, 255), mass=6)
ball_3 = Ball([250,250], 40, [5*np.cos(theta[2]), 5*np.sin(theta[2])], (0, 255, 0), mass=16)
ball_4 = Ball([250,100], 30, [5*np.cos(theta[3]), 5*np.sin(theta[3])], (255, 255, 0), mass=6)
ball_5 = Ball([250,350], 30, [5*np.cos(theta[4]), 5*np.sin(theta[4])], (0, 255, 255), mass=6)
ball_6 = Ball([250,450], 30, [5*np.cos(theta[5]), 5*np.sin(theta[5])], (255, 0, 255), mass=6)

# Store all the balls in a list for easier management
balls = [ball_1, ball_2, ball_3, ball_4, ball_5, ball_6]

# Calculate the initial kinetic energy of the system by summing the kinetic energies of all balls
k_e = 0
for ball in balls:
    k_e += ball.kinetic_energy()
print(f'initial kinetic energy = {k_e}')

# Initialize the main loop variables
run = True  # Controls the main loop
is_moving = False  # Controls whether the balls are moving or paused
collision = True  # Controls whether collision detection is active

# Main loop for the simulation
while run:
    clock.tick(60)  # Limit the frame rate to 60 FPS
    pygame.display.set_caption("Ball collision - FPS: {}".format(int(clock.get_fps())))  # Update the window title with FPS
    for event in pygame.event.get():  # Event handling loop
        if event.type == pygame.QUIT:  # If the user closes the window, exit the loop
            run = False

    # Check if the space key is pressed to toggle the ball movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        is_moving = not is_moving  # Toggle the movement state
        pygame.time.delay(100)  # Add a short delay to prevent rapid toggling

    # If the balls are moving, proceed with the simulation
    if is_moving:
        # Check for collisions between every pair of balls
        if collision:
            for pair in itertools.combinations(balls, 2):  # Generate all unique pairs of balls
                ball_1, ball_2 = pair
                pos1 = np.array([ball_1.x, ball_1.y])
                pos2 = np.array([ball_2.x, ball_2.y])
                v_rel = np.linalg.norm(np.array(ball_1.v) - np.array(ball_2.v))  # Relative velocity

                # Check if the balls are close enough to collide
                if np.linalg.norm(pos1-pos2) < ball_1.radius + ball_2.radius:
                    ball_1, ball_2 = coll(ball_1, ball_2)  # Handle the collision using the coll function
                    
                    # Recalculate the total kinetic energy after the collision
                    k_e = 0
                    for ball in balls:
                        k_e += ball.kinetic_energy()

        # Update the position and velocity of each ball, and check for boundary collisions
        for ball in balls:
            # Check for collisions with the screen boundaries and adjust position and velocity accordingly
            if ball.x > screen_width - ball.radius:  # Right boundary
                overlap = np.abs(ball.x - screen_width + ball.radius)
                ball.x -= overlap
                ball.y -= overlap / ball.v[0] * ball.v[1]
                ball.v[0] = -ball.v[0]  # Reverse the x-velocity

            elif ball.x < ball.radius:  # Left boundary
                overlap = np.abs(ball.radius - ball.x)
                ball.x += overlap
                ball.y -= overlap / ball.v[0] * ball.v[1]
                ball.v[0] = -ball.v[0]  # Reverse the x-velocity

            elif ball.y > screen_width - ball.radius:  # Bottom boundary
                overlap = np.abs(ball.y - screen_width + ball.radius)
                ball.y -= overlap
                ball.x -= overlap / ball.v[1] * ball.v[0]
                ball.v[1] = -ball.v[1]  # Reverse the y-velocity

            elif ball.y < ball.radius:  # Top boundary
                overlap = np.abs(ball.radius - ball.y)
                ball.y += overlap
                ball.x -= overlap / ball.v[1] * ball.v[0]
                ball.v[1] = -ball.v[1]  # Reverse the y-velocity

            # Update the ball's position based on its velocity
            ball.x += ball.v[0]
            ball.y += ball.v[1]

    # Draw the trail surface and the balls
    win.blit(trail_surface, (0, 0))  # Draw the trail surface on the window
    for ball in balls:  # Draw each ball on the screen
        pygame.draw.circle(win, ball.color, (ball.x, ball.y), ball.radius)

    # Update the display to show the new frame
    pygame.display.update()

pygame.quit()  # Quit Pygame after exiting the loop
