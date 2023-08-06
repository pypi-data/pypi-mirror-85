import os
from pickle import load, dump
from math import atan2, isclose
from math import sqrt as msqrt
from sympy import Symbol, solve, Eq, sqrt
from numpy import linspace, array, float64, cos, sin, sign, pi
from numpy.linalg import norm

ARCLINE_FILE = os.path.join(os.path.dirname(__file__), 'arcline.pkl')

def get_3point_ang(a, b, c):
    ang = atan2(c[1]-b[1], c[0]-b[0]) - atan2(a[1]-b[1], a[0]-b[0])

    if ang < 0:
        ang += 2*pi
    
    if ang > pi:
        ang = 2*pi - ang

    return ang

def get_arc_line_points(x_0, y_0, x_1, y_1, x_prev, y_prev, r_curve, pts=10, sym_sols=None):
    
    start_angle = get_line_ori(x_0, y_0, x_prev, y_prev)
    
    x_c_multi = [x_0 + r_curve*cos(start_angle + s*pi/2) for s in [1, -1]]
    y_c_multi = [y_0 + r_curve*sin(start_angle + s*pi/2) for s in [1, -1]]

    x_c = None
    y_c = None
    i_center = None
    for i_c, (x, y) in enumerate(zip(x_c_multi, y_c_multi)):
        if x_c is None or norm([x_1-x, y_1-y]) < norm([x_1-x_c, y_1-y_c]):
            x_c = x
            y_c = y
            i_center = i_c
    
    x = Symbol('x', real=True)
    y = Symbol('y', real=True)
    x_c_sym = Symbol('x_c_sym', real=True)
    y_c_sym = Symbol('y_c_sym', real=True)
    x_1_sym = Symbol('x_1_sym', real=True)
    y_1_sym = Symbol('y_1_sym', real=True)
    r_curve_sym = Symbol('r_curve_sym', real=True)

    if sym_sols is None and os.path.exists(ARCLINE_FILE) is False:
        eq_circle = Eq((x - x_c_sym)**2 + (y - y_c_sym)**2, r_curve_sym**2)
        eq_perp = Eq((y - y_c_sym)/(x - x_c_sym), -(x - x_1_sym)/(y - y_1_sym))
        sym_sols = solve([eq_circle, eq_perp], x, y)
        
        with open(ARCLINE_FILE, 'wb') as fid:
            dump(sym_sols, fid)

    elif os.path.exists(ARCLINE_FILE) is True:
        with open(ARCLINE_FILE, 'rb') as fid:
            sym_sols = load(fid)

    # Substitute for symbols in the symbolic solution
    sols = [tuple([eq.subs([(x_c_sym, x_c), (y_c_sym, y_c), (x_1_sym, x_1), (y_1_sym, y_1), (r_curve_sym, r_curve)]) for eq in sym_sol]) for sym_sol in sym_sols]

    # Get the best solution (i.e. the one with the smallest arc length)
    # best_sol = None
    # for sol in sols:
    #     if best_sol is None or get_3point_ang((x_0, y_0), (x_c, y_c), (sol[0], sol[1])) < get_3point_ang((x_0, y_0), (x_c, y_c), (best_sol[0], best_sol[1])):
    #         best_sol = sol    
    best_sol = _get_best_sol(x_0, y_0, x_1, y_1, x_c, y_c, x_prev, y_prev, r_curve, sols)

    try:
        x_tan = float(best_sol[0])
        y_tan = float(best_sol[1])
    except TypeError:
        raise TypeError(type(best_sol[0]))
    
    # Figure out how many points in the arc and line (scale by length)
    arc_length = r_curve * get_3point_ang((x_0, y_0), (x_c, y_c), (x_tan, y_tan))
    line_length = norm([x_1 - x_tan, y_1 - y_tan])
    line_pts = round(pts/(arc_length/line_length + 1))
    arc_pts = pts - line_pts if line_pts < pts else 1

    # Generate the points
    x_arc, y_arc = get_arc_points(x_0, y_0, x_tan, y_tan, x_c, y_c, x_prev, y_prev, arc_pts, direction='ccw')
    x_line, y_line = get_line_points(x_tan, y_tan, x_1, y_1, line_pts)

    return list(x_arc) + list(x_line), list(y_arc) + list(y_line), x_c, y_c, x_tan, y_tan, sym_sols, start_angle, i_center

def _get_best_sol(x_0, y_0, x_1, y_1, x_c, y_c, x_prev, y_prev, r_curve, sols, i_center=1):
    angs = []
    for sol in sols:
        x_tan = float(sol[0])
        y_tan = float(sol[1])


        x_arc, y_arc = get_arc_points(x_0, y_0, x_tan, y_tan, x_c, y_c, x_prev, y_prev, 100)

        start_ang = abs(get_3point_ang((x_prev, y_prev), (x_0, y_0), (x_arc[1], y_arc[1])))
        end_ang = abs(get_3point_ang((x_arc[-2], y_arc[-2]), (x_tan, y_tan), (x_1, y_1)))

        angs.append(min([start_ang, end_ang]))
        
    return sols[angs.index(max(angs))] if i_center == 1 else sols[angs.index(min(angs))]

def get_line_points(x_0, y_0, x_1, y_1, pts=10):
    return linspace(x_0, x_1, pts), linspace(y_0, y_1, pts)

def arc_center(x_0, y_0, x_1, y_1, m_0):
    """Returns the x and y coordinates of the center of curvature of an arc given the start and end coordinates, and the slope at the start.

    Parameters
    ----------
    x_0 : float
        Starting X coordinate
    y_0 : float
        Starting Y coordinate
    x_1 : float
        Ending X coordinate
    y_1 : float
        Ending Y coordinate
    m_0 : float
        Starting slop

    Returns
    -------
    list, list
        x and y coordinates of center of curvature

    """
    a = -m_0
    b = 1

    x = Symbol('x', real=True)
    y = Symbol('y', real=True)

    eq1 = Eq(b*x -a*y - (b*x_0-a*y_0), 0)
    eq2 = Eq((x_0 - x_1)*x + (y_0 - y_1)*y  -  .5*(x_0**2 + y_0**2 - x_1**2 - y_1**2), 0)

    sol = solve([eq1, eq2], x, y)        
    
    x_c = [v for v in sol.values()][0]
    y_c = [v for v in sol.values()][1]

    return x_c, y_c

def get_arc_points(x_0, y_0, x_1, y_1, x_c, y_c, x_prev, y_prev, pts=10, direction=None):
    """Returns points on an arc given the start and end points, center of curvature, and a third point through which the start tangent passes.

    Parameters
    ----------
    x_0 : float
        Starting X coordinate
    y_0 : float
        Starting Y coordinate
    x_1 : float
        Ending X coordinate
    y_1 : float
        Ending Y coordinate
    x_c : float
        X coordinate of center of curvature
    y_c : float
        Y coordinate of center of curvature
    x_prev : float
        X coordinate of point through which the start tangent passes
    y_prev : float
        Y coordinate point through which the start tangent passes
    pts : int, optional
        Number of points to return, by default 10

    Returns
    -------
    list, list
        x and y coordinate of points on the arc

    """
    start_angle = get_line_ori(x_c, y_c, x_0, y_0)

    ang_from_prev = get_line_ori(x_c, y_c, x_0, y_0)  - get_line_ori(x_c, y_c, x_prev, y_prev) 

    # ang_from_prev = get_3point_ang((x_0, y_0), (x_c, y_c), (x_1, y_1))
    
    # delta_angle_1 = get_3point_ang((x_0, y_0), (x_c, y_c), (x_1, y_1))    
    delta_angle_1 = get_line_ori(x_c, y_c, x_1, y_1)  - get_line_ori(x_c, y_c, x_0, y_0) 
    delta_angle_2 = -sign(delta_angle_1)*(2*pi-abs(delta_angle_1))
    
    if direction is None:
        delta_angle = delta_angle_1 if sign(delta_angle_1) == sign(ang_from_prev) else delta_angle_2
    elif direction == 'ccw':
        delta_angle = delta_angle_1 if delta_angle_1 > 0 else delta_angle_2
    elif direction == 'cw':
        delta_angle = delta_angle_1 if delta_angle_1 < 0 else delta_angle_2

    end_angle = start_angle + delta_angle
    
    angles = linspace(start_angle, end_angle, pts)   
    radius = norm(array([x_0-x_c, y_0-y_c]).astype(float64))

    x = list([x_c + radius*cos(angle) for angle in angles])
    y = list([y_c + radius*sin(angle) for angle in angles])

    return x, y

def get_line_ori(x_0, y_0, x_1, y_1):
    """Returns the orientation of a vector defined by two points in 2D space.

    Parameters
    ----------
    x_0 : float
        X coordinate of first point
    y_0 : float
        Y coordinate of first point
    x_1 : float
        X coordinate of second point
    y_1 : float
        Y coordinate of second point

    Returns
    -------
    float
        Orientation of the vector (radians)

    """
    
    return atan2(y_1-y_0, x_1-x_0)

def get_angle_two_vecs(x_0, y_0, x_1, y_1):
    """Returns the orientation between the two vectors defined from the origin to the two given points in 2D space.

    Parameters
    ----------
    x_0 : float
        X coordinate of first point
    y_0 : float
        Y coordinate of first point
    x_1 : float
        X coordinate of second point
    y_1 : float
        Y coordinate of second point

    Returns
    -------
    float
        Angle between the two vectors (radians)

    """
    ang_0 = get_line_ori(0, 0, x_0, y_0)
    ang_1 = get_line_ori(0, 0, x_1, y_1)
    ang = ang_1 - ang_0

    return ang
