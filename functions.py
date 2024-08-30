import numpy as np

def coll(ball_1, ball_2):
    """ Manage collision between 2 balls.

    Args:
        ball_1 (Ball): ball1.
        ball_2 (Ball): ball2.

    Returns:
        Ball, Ball: ball1, ball2
    """    
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