from math import atan2
from sympy import Symbol, solve, Eq
from numpy import linspace, array, float64, cos, sin, sign, pi
from numpy.linalg import norm
   
def arc_center(x_0, y_0, x_1, y_1, m_0):

    a = -m_0
    b = 1

    x = Symbol('x', real=True)
    y = Symbol('y', real=True)

    eq1 = Eq(b*x -a*y - (b*x_0-a*y_0), 0)
    eq2 = Eq((x_0 - x_1)*x + (y_0 - y_1)*y  -  .5*(x_0**2 + y_0**2 - x_1**2 - y_1**2), 0)

    sol = solve([eq1, eq2], x, y)        
    
    x_c = [v for v in sol.values()][0]
    y_c = [v for v in sol.values()][1]

    return (x_c, y_c)

def get_arc_points(x_0, y_0, x_1, y_1, x_c, y_c, x_prev, y_prev, pts=10):
    start_angle = get_angle_two_points(x_c, y_c, x_0, y_0)

    ang_from_prev = get_angle_two_points(x_c, y_c, x_0, y_0)  - get_angle_two_points(x_c, y_c, x_prev, y_prev) 

    delta_angle_1 = get_angle_two_vecs(x_0-x_c, y_0-y_c, x_1-x_c, y_1-y_c)
    delta_angle_2 = -sign(delta_angle_1)*(2*pi-abs(delta_angle_1))
    
    delta_angle = delta_angle_1 if sign(delta_angle_1) == sign(ang_from_prev) else delta_angle_2
    
    end_angle = start_angle + delta_angle
    
    angles = linspace(start_angle, end_angle, pts)   
    radius = norm(array([x_0-x_c, y_0-y_c]).astype(float64))

    x = list([x_c + radius*cos(angle) for angle in angles])
    y = list([y_c + radius*sin(angle) for angle in angles])

    return x, y

def get_angle_two_points(x_0, y_0, x_1, y_1):
    return atan2(y_1-y_0, x_1-x_0)

def get_angle_two_vecs(x_0, y_0, x_1, y_1):

    ang_0 = get_angle_two_points(0, 0, x_0, y_0)
    ang_1 = get_angle_two_points(0, 0, x_1, y_1)
    ang = ang_1 - ang_0

    return ang
