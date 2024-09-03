import numpy as np

class Ball:
    """ 
    Define a Ball object with properties such as position, velocity, radius, mass, and color.
    """    
    def __init__(self, pos, radius, init_vel, color, mass=None):
        """ 
        Constructor for the Ball class. Initializes a Ball object with a given position, radius, 
        initial velocity, color, and optionally a mass.

        Args:
            pos (list): Initial position of the ball [x, y].
            radius (float): Radius of the ball.
            init_vel (list): Initial velocity of the ball [vx, vy].
            color (tuple): Color of the ball in RGB format.
            mass (float, optional): Mass of the ball. If not provided, it is calculated based on the radius.
        """        
        self.x = pos[0]  # x-coordinate of the ball's position
        self.y = pos[1]  # y-coordinate of the ball's position

        self.radius = radius  # Radius of the ball
        self.v = init_vel  # Initial velocity of the ball as a 2D vector [vx, vy]

        # If mass is not provided, calculate it based on the radius using the method m_from_r
        if mass is None:
            self.mass = self.m_from_r()  # Calculate mass assuming the ball is a sphere with uniform density
        else:
            self.mass = mass  # Use the provided mass

        self.color = color  # Color of the ball, stored as an RGB tuple

    def kinetic_energy(self):
        """ 
        Calculate and return the kinetic energy of the ball.

        Returns:
            float: Kinetic energy of the ball.
        """        
        # Kinetic energy is given by 0.5 * mass * velocity^2
        return 0.5 * self.mass * np.linalg.norm(self.v)**2
    
    def pos(self, pos):
        """ 
        Update the ball's position.

        Args:
            pos (list): New position of the ball [x, y].
        """        
        self.x = pos[0]  # Update x-coordinate
        self.y = pos[1]  # Update y-coordinate

    def m_from_r(self):
        """ 
        Calculate the mass of the ball based on its radius, assuming the ball is a sphere 
        with uniform density.

        Returns:
            float: Calculated mass of the ball.
        """        
        # Mass is calculated using the volume of a sphere formula: (4/3) * pi * r^3
        return 4/3 * np.pi * self.radius**3
    
    def r_from_m(self):
        """ 
        Calculate the radius of the ball based on its mass, assuming the ball is a sphere 
        with uniform density.

        Returns:
            float: Calculated radius of the ball.
        """        
        # Radius is derived from the mass using the formula: r = (3/4 * m / pi)^(1/3)
        return (3/4 * self.mass / np.pi)**(1/3)
