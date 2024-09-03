import numpy as np

def coll(ball_1, ball_2):
    """ Manage collision between 2 balls.

    Args:
        ball_1 (Ball): The first ball involved in the collision.
        ball_2 (Ball): The second ball involved in the collision.

    Returns:
        Ball, Ball: The two balls after their velocities and positions have been updated post-collision.
    """
    
    # Extract masses and velocities of the two balls
    m1, m2 = ball_1.mass, ball_2.mass  # Masses of ball_1 and ball_2
    v1, v2 = np.array(ball_1.v), np.array(ball_2.v)  # Convert velocities to numpy arrays for vector operations
    
    # Calculate the relative velocity magnitude between the two balls
    v_rel = np.linalg.norm(v1 - v2)
    
    # Calculate the overlap distance between the two balls
    overlap = ball_1.radius + ball_2.radius - np.linalg.norm(
        np.array([ball_1.x, ball_1.y]) - np.array([ball_2.x, ball_2.y])
    )
    
    # Determine the time of overlap, to resolve the collision by "rewinding" the balls
    t_overlap = overlap / v_rel
    
    # Rewind the positions of the balls to the moment of collision (just before overlap)
    pos1 = np.array([ball_1.x, ball_1.y]) - v1 * t_overlap
    pos2 = np.array([ball_2.x, ball_2.y]) - v2 * t_overlap
    
    # Calculate the collision normal vector (unit vector pointing from ball_2 to ball_1)
    n = (pos1 - pos2) / np.linalg.norm(pos1 - pos2)
    
    # Calculate the tangential vector (perpendicular to the normal)
    t = np.array([-n[1], n[0]])
    
    # Decompose the velocities of both balls into normal and tangential components
    v1_n = np.dot(v1, n)  # Normal component of ball_1's velocity
    v2_n = np.dot(v2, n)  # Normal component of ball_2's velocity
    v1_t = np.dot(v1, t)  # Tangential component of ball_1's velocity
    v2_t = np.dot(v2, t)  # Tangential component of ball_2's velocity
    
    # Compute the new normal velocities after collision using the 1D elastic collision formula
    v1_n_new = (v1_n * (m1 - m2) + 2 * m2 * v2_n) / (m1 + m2)
    v2_n_new = (v2_n * (m2 - m1) + 2 * m1 * v1_n) / (m1 + m2)
    
    # The tangential components remain unchanged after collision
    # Combine the new normal and unchanged tangential components to get the new velocities
    v1_new = v1_n_new * n + v1_t * t  # New velocity of ball_1
    v2_new = v2_n_new * n + v2_t * t  # New velocity of ball_2
    
    # Update the positions of the balls to their positions at the time of collision
    ball_1.pos(pos1)
    ball_2.pos(pos2)
    
    # Update the velocities of the balls to the newly calculated velocities
    ball_1.v = v1_new
    ball_2.v = v2_new
    
    # Return the updated ball objects
    return ball_1, ball_2
