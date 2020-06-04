from display import *
from matrix import *
from gmath import *
import random

def scanline_convert(polygons, i, screen, zbuffer ):
    color = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]

    points = [polygons[i], polygons[i + 1], polygons[i + 2]]

    top = points[points.index(max(points, key=lambda x:int(x[1])))]
    points.remove(top)

    bottom = points[points.index(min(points, key=lambda x:int(x[1])))]
    points.remove(bottom)

    middle = points.pop()

    x0 = bottom[0]
    x1 = bottom[0]

    y = bottom[1]

    z0 = bottom[2]
    z1 = middle[2]

    if top[1] != bottom[1]:
        dx0 = (top[0] - x0) / (top[1] - bottom[1])
        dz0 = (top[2] - z0) / (top[1] - bottom[1])
    else:
        dx0 = 0
        dz0 = 0

    if middle[1] != bottom[1]:
        dx1 = (middle[0] - x0) / (middle[1] - bottom[1])
        dz1 = (middle[2] - z0) / (middle[1] - bottom[1])
    else:
        dx1 = 0
        dz1 = 0


    while y < middle[1]:
        draw_line(int(x0), int(y), int(z0), int(x1), int(y), int(z1), screen, zbuffer, color)
        x0 += dx0
        x1 += dx1
        z0 += dz0
        z1 += dz1
        y += 1

    y = middle[1]
    x1 = middle[0]
    z1 = middle[2]

    if middle[1] != top[1]:
        dx1 = (top[0] - x1) / (top[1] - middle[1])
        dz1 = (top[2] - z1) / (top[1] - middle[1])
    else:
        dx1 = 0
        dz1 = 0


    while y < top[1]:
        draw_line(int(x0), int(y), int(z0), int(x1), int(y), int(z1), screen, zbuffer, color)
        x0 += dx0
        x1 += dx1
        z0 += dz0
        z1 += dz1
        y += 1


def add_polygon( polygons, x0, y0, z0, x1, y1, z1, x2, y2, z2 ):
    add_point(polygons, x0, y0, z0)
    add_point(polygons, x1, y1, z1)
    add_point(polygons, x2, y2, z2)

def draw_polygons( polygons, screen, zbuffer, color ):
    if len(polygons) < 2:
        print('Need at least 3 points to draw')
        return

    point = 0
    while point < len(polygons) - 2:

        normal = calculate_normal(polygons, point)[:]
        #print normal
        if normal[2] > 0:
            scanline_convert(polygons, point, screen, zbuffer)
        point+= 3


def add_box( polygons, x, y, z, width, height, depth ):
    x1 = x + width
    y1 = y - height
    z1 = z - depth

    #front
    add_polygon(polygons, x, y, z, x1, y1, z, x1, y, z)
    add_polygon(polygons, x, y, z, x, y1, z, x1, y1, z)

    #back
    add_polygon(polygons, x1, y, z1, x, y1, z1, x, y, z1)
    add_polygon(polygons, x1, y, z1, x1, y1, z1, x, y1, z1)

    #right side
    add_polygon(polygons, x1, y, z, x1, y1, z1, x1, y, z1)
    add_polygon(polygons, x1, y, z, x1, y1, z, x1, y1, z1)
    #left side
    add_polygon(polygons, x, y, z1, x, y1, z, x, y, z)
    add_polygon(polygons, x, y, z1, x, y1, z1, x, y1, z)

    #top
    add_polygon(polygons, x, y, z1, x1, y, z, x1, y, z1)
    add_polygon(polygons, x, y, z1, x, y, z, x1, y, z)
    #bottom
    add_polygon(polygons, x, y1, z, x1, y1, z1, x1, y1, z)
    add_polygon(polygons, x, y1, z, x, y1, z1, x1, y1, z1)

def add_sphere(polygons, cx, cy, cz, r, step ):
    points = generate_sphere(cx, cy, cz, r, step)

    lat_start = 0
    lat_stop = step
    longt_start = 0
    longt_stop = step

    step+= 1
    for lat in range(lat_start, lat_stop):
        for longt in range(longt_start, longt_stop):

            p0 = lat * step + longt
            p1 = p0+1
            p2 = (p1+step) % (step * (step-1))
            p3 = (p0+step) % (step * (step-1))

            if longt != step - 2:
                add_polygon( polygons, points[p0][0],
                             points[p0][1],
                             points[p0][2],
                             points[p1][0],
                             points[p1][1],
                             points[p1][2],
                             points[p2][0],
                             points[p2][1],
                             points[p2][2])
            if longt != 0:
                add_polygon( polygons, points[p0][0],
                             points[p0][1],
                             points[p0][2],
                             points[p2][0],
                             points[p2][1],
                             points[p2][2],
                             points[p3][0],
                             points[p3][1],
                             points[p3][2])


def generate_sphere( cx, cy, cz, r, step ):
    points = []

    rot_start = 0
    rot_stop = step
    circ_start = 0
    circ_stop = step

    for rotation in range(rot_start, rot_stop):
        rot = rotation/float(step)
        for circle in range(circ_start, circ_stop+1):
            circ = circle/float(step)

            x = r * math.cos(math.pi * circ) + cx
            y = r * math.sin(math.pi * circ) * math.cos(2*math.pi * rot) + cy
            z = r * math.sin(math.pi * circ) * math.sin(2*math.pi * rot) + cz

            points.append([x, y, z])
            #print 'rotation: %d\tcircle%d'%(rotation, circle)
    return points

def add_torus(polygons, cx, cy, cz, r0, r1, step ):
    points = generate_torus(cx, cy, cz, r0, r1, step)

    lat_start = 0
    lat_stop = step
    longt_start = 0
    longt_stop = step

    for lat in range(lat_start, lat_stop):
        for longt in range(longt_start, longt_stop):

            p0 = lat * step + longt;
            if (longt == (step - 1)):
                p1 = p0 - longt;
            else:
                p1 = p0 + 1;
            p2 = (p1 + step) % (step * step);
            p3 = (p0 + step) % (step * step);

            add_polygon(polygons,
                        points[p0][0],
                        points[p0][1],
                        points[p0][2],
                        points[p3][0],
                        points[p3][1],
                        points[p3][2],
                        points[p2][0],
                        points[p2][1],
                        points[p2][2] )
            add_polygon(polygons,
                        points[p0][0],
                        points[p0][1],
                        points[p0][2],
                        points[p2][0],
                        points[p2][1],
                        points[p2][2],
                        points[p1][0],
                        points[p1][1],
                        points[p1][2] )


def generate_torus( cx, cy, cz, r0, r1, step ):
    points = []
    rot_start = 0
    rot_stop = step
    circ_start = 0
    circ_stop = step

    for rotation in range(rot_start, rot_stop):
        rot = rotation/float(step)
        for circle in range(circ_start, circ_stop):
            circ = circle/float(step)

            x = math.cos(2*math.pi * rot) * (r0 * math.cos(2*math.pi * circ) + r1) + cx;
            y = r0 * math.sin(2*math.pi * circ) + cy;
            z = -1*math.sin(2*math.pi * rot) * (r0 * math.cos(2*math.pi * circ) + r1) + cz;

            points.append([x, y, z])
    return points

def add_cylinder(polygons, cx, cy, cz, r, h, step):
    b1 = [] #top
    b2 = [] #bottom
    add_circle(b1, cx, cy, cz, r, step); #let b1 equal the points that are in this circle
    add_circle(b2, cx, cy, cz+h, r, step); #let b2 equal the points that are in this circle

    #base
    for p in range(0, len(b1)-1):
        add_polygon(polygons,         #
                    b1[p][0],
                    b1[p][1],
                    b1[p][2],
                    cx,
                    cy,
                    cz,
                    b1[p+1][0],
                    b1[p+1][1],
                    b1[p+1][2])
        add_polygon(polygons,
                    cx,
                    cy,
                    cz+h,
                    b2[p][0],
                    b2[p][1],
                    b2[p][2],
                    b2[p+1][0],
                    b2[p+1][1],
                    b2[p+1][2])

    #body
    for p in range(0, len(b1)-1):
        #front side
        add_polygon(polygons,
                    b1[p][0],
                    b1[p][1],
                    b1[p][2],
                    b1[p+1][0],
                    b1[p+1][1],
                    b1[p+1][2],
                    b2[p+1][0],
                    b2[p+1][1],
                    b2[p+1][2])
        add_polygon(polygons,
                    b1[p][0],
                    b1[p][1],
                    b1[p][2],
                    b2[p+1][0],
                    b2[p+1][1],
                    b2[p+1][2],
                    b2[p][0],
                    b2[p][1],
                    b2[p][2])
        #back side
        add_polygon(polygons,
                    b1[p+1][0],
                    b1[p+1][1],
                    b1[p+1][2],
                    b1[p][0],
                    b1[p][1],
                    b1[p][2],
                    b2[p][0],
                    b2[p][1],
                    b2[p][2])
        add_polygon(polygons,
                    b1[p+1][0],
                    b1[p+1][1],
                    b1[p+1][2],
                    b2[p][0],
                    b2[p][1],
                    b2[p][2],
                    b2[p+1][0],
                    b2[p+1][1],
                    b2[p+1][2])


def add_circle( points, cx, cy, cz, r, step ):
    x0 = r + cx
    y0 = cy
    i = 1

    while i <= step:
        t = float(i)/step
        x1 = r * math.cos(2*math.pi * t) + cx;
        y1 = r * math.sin(2*math.pi * t) + cy;

        add_edge(points, x0, y0, cz, x1, y1, cz)
        x0 = x1
        y0 = y1
        i+= 1

def add_curve( points, x0, y0, x1, y1, x2, y2, x3, y3, step, curve_type ):

    xcoefs = generate_curve_coefs(x0, x1, x2, x3, curve_type)[0]
    ycoefs = generate_curve_coefs(y0, y1, y2, y3, curve_type)[0]

    i = 1
    while i <= step:
        t = float(i)/step
        x = t * (t * (xcoefs[0] * t + xcoefs[1]) + xcoefs[2]) + xcoefs[3]
        y = t * (t * (ycoefs[0] * t + ycoefs[1]) + ycoefs[2]) + ycoefs[3]
        #x = xcoefs[0] * t*t*t + xcoefs[1] * t*t + xcoefs[2] * t + xcoefs[3]
        #y = ycoefs[0] * t*t*t + ycoefs[1] * t*t + ycoefs[2] * t + ycoefs[3]

        add_edge(points, x0, y0, 0, x, y, 0)
        x0 = x
        y0 = y
        i+= 1


def draw_lines( matrix, screen, zbuffer, color ):
    if len(matrix) < 2:
        print('Need at least 2 points to draw')
        return

    point = 0
    while point < len(matrix) - 1:
        draw_line( int(matrix[point][0]),
                   int(matrix[point][1]),
                   matrix[point][2],
                   int(matrix[point+1][0]),
                   int(matrix[point+1][1]),
                   matrix[point+1][2],
                   screen, zbuffer, color)
        point+= 2

def add_edge( matrix, x0, y0, z0, x1, y1, z1 ):
    add_point(matrix, x0, y0, z0)
    add_point(matrix, x1, y1, z1)

def add_point( matrix, x, y, z=0 ):
    matrix.append( [x, y, z, 1] )


def draw_line( x0, y0, z0, x1, y1, z1, screen, zbuffer, color ):

    #swap points if going right -> left
    if x0 > x1:
        xt = x0
        yt = y0
        zt = z0
        x0 = x1
        y0 = y1
        z0 = z1
        x1 = xt
        y1 = yt
        z1 = zt

    x = x0
    y = y0
    z = z0
    A = 2 * (y1 - y0)
    B = -2 * (x1 - x0)
    wide = False
    tall = False

    if ( abs(x1-x0) >= abs(y1 - y0) ): #octants 1/8
        wide = True
        loop_start = x
        loop_end = x1
        dx_east = dx_northeast = 1
        dy_east = 0
        d_east = A
        distance = x1 - x + 1
        if ( A > 0 ): #octant 1
            d = A + B/2
            dy_northeast = 1
            d_northeast = A + B
        else: #octant 8
            d = A - B/2
            dy_northeast = -1
            d_northeast = A - B

    else: #octants 2/7
        tall = True
        dx_east = 0
        dx_northeast = 1
        distance = abs(y1 - y) + 1
        if ( A > 0 ): #octant 2
            d = A/2 + B
            dy_east = dy_northeast = 1
            d_northeast = A + B
            d_east = B
            loop_start = y
            loop_end = y1
        else: #octant 7
            d = A/2 - B
            dy_east = dy_northeast = -1
            d_northeast = A - B
            d_east = -1 * B
            loop_start = y1
            loop_end = y

    if distance != 0:
        dz = (z1 - z0) / distance
    else:
        dz = 0

    while ( loop_start < loop_end ):
        plot( screen, zbuffer, color, x, y, 0 )
        if ( (wide and ((A > 0 and d > 0) or (A < 0 and d < 0))) or
             (tall and ((A > 0 and d < 0) or (A < 0 and d > 0 )))):

            x+= dx_northeast
            y+= dy_northeast
            d+= d_northeast
        else:
            x+= dx_east
            y+= dy_east
            d+= d_east
        z += dz
        loop_start+= 1
    plot( screen, zbuffer, color, x, y, 0 )
