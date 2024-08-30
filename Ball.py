import numpy as np

class Ball:
    """ Define object Ball.
    """    
    def __init__(self, pos, radius, init_vel, color, mass = None):
        """ Constructor of the class.

        Args:
            pos (list): initial position of the ball.
            radius (double): radius of the ball.
            init_vel (double): initial velocity.
            color (tuple): color of the ball.
            mass (double, optional): mass of the ball. Defaults to None.
        """        
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
        """ Compute kinetic energy.

        Returns:
            double: kinetic energy.
        """        
        return 0.5*self.mass*np.linalg.norm(self.v)**2
    
    def pos(self, pos):
        """ Modify ball's position.

        Args:
            pos (list): new position of the ball.
        """        
        self.x = pos[0]
        self.y = pos[1]

    def m_from_r(self):
        return 4/3 * np.pi * self.radius**3
    
    def r_from_m(self):
        return (3/4 * self.mass / np.pi)**(1/3)