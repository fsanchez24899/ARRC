import math

## TODO: fix comment descriptions of methods to use ''' instead of ##

""" 2D Vector Class """
## TODO: consider updating vector functions to update the object instead of returning new vector
class Vector(object):
    def __init__(self, x, y):
        ## x and y are coordinates of a point
        self.x = x
        self.y = y
    def add(self, other):
        ## get vector added to other
        dx = self.x+other.x
        dy = self.y+other.y
        return Vector(dx,dy)
    def scalar(self, c):
        ## get vector multiplied by scalar
        cx = c*self.x
        cy = c*self.y
        return Vector(cx, cy)
    def mag(self):
        ## vector magnitude
        return ((self.x)**2+(self.y)**2)**.5
    def slope(self):
        ## slope of line
        return (float(self.y)/float(self.x))
    def dot(self, other):
        ## dot product of self and other
        return self.x*other.x+self.y*other.y
    def angle(self, other):
        ## angle between self and other
        dot = self.dot(other)
        return math.acos(float(dot)/(float(self.mag()*other.mag())))
    def ortho(self):
        ## get normal vector
        return Vector(-self.y, self.x)
    def normalize(self):
        ## get unit vector
        return Vector(float(self.x)/self.mag(), float(self.y)/self.mag())
    def rotate(self, angle):
        ## get vector rotated by angle using rotation matrix
        # print "Type: "+str(type(angle))+" and value: "+str(angle)
        new_x = math.cos(angle)*self.x + -math.sin(angle)*self.y
        new_y = math.sin(angle)*self.x + math.cos(angle)*self.y
        return Vector(new_x, new_y)
    def orientation(self, v1):
        ## find clockwise/cunterclockwise orientaiton of self and v1 (for use in Convex Hull)
        if self.slope() == v1.slope():
            return 0  ## colinear
        elif self.slope() < v1.slope():
            return -1  ## counterclockwise
        elif self.slope() > v1.slope():
            return 1  ## clockwise

""" Polygon Class """
## Convex Polygons only (no circles; see below)
class Polygon(object):
    def __init__(self, center, vertices, rotation=0):
        ## center and vertices (list) are vectors
        self.center = center
        self.vertices = vertices
        self.rotation = rotation
    def rotate(self, angle):
        ## update polygon to be rotated about its center by angle
        new_vertices = []
        cen_flip = self.center.scalar(-1.0)
        for vertex in self.vertices:
            point = vertex.add(cen_flip)
            new_point = point.rotate(angle)
            new_vertex = new_point.add(self.center)
            new_vertices.append(new_vertex)
        self.vertices = new_vertices
        self.rotation = angle
    def rotate_around(self, point, angle):
        ## update polygon to be rotated about a point by angle
        new_vertices = []
        point_flip = point.scalar(-1.0)
        cen_flip = self.center.scalar(-1.0)
        shift1 = self.center.add(point_flip)
        shift2 = shift1.rotate(angle)
        shift_final = shift2.add(point)
        for vertex in self.vertices:
            p = vertex.add(cen_flip)
            new_point = p.rotate(angle)
            new_vertex = new_point.add(shift_final)
            new_vertices.append(new_vertex)
        self.center = shift_final
        self.vertices = new_vertices
        self.rotation = angle
    def translate(self, shift):
        ## update polygon to be translated by vector "shift"
        new_vertices = []
        for vertex in self.vertices:
            new_vertex = vertex.add(shift)
            new_vertices.append(new_vertex)
        new_center = self.center.add(shift)
        self.center = new_center
        self.vertices = new_vertices
    def normals(self):
        ## list of normal vectors
        edges = []
        for i in range(len(self.vertices)-1):
            flip = self.vertices[i].scalar(-1)
            edges.append(self.vertices[i+1].add(flip))
        flipper = self.vertices[-1].scalar(-1)
        edges.append(self.vertices[0].add(flipper))
        normals = set()
        for edge in edges:
            if edge.ortho().scalar(-1) not in normals: 
                normals.add(edge.ortho())
        return normals
    def min_max_proj(self, axis):
        ## find min/max vertices of projection onto axis (vector)
        min_ind = 0
        max_ind = 0
        min_proj = self.vertices[0].dot(axis)
        max_proj = self.vertices[0].dot(axis)
        for i in range(1,len(self.vertices)):
            proj = self.vertices[i].dot(axis)
            if proj < min_proj:
                min_proj = proj
                min_ind = i
            if proj > max_proj:
                max_proj = proj
                max_ind = i
        min_vertex = self.vertices[min_ind]
        max_vertex = self.vertices[max_ind]
        return (min_vertex, max_vertex)
    def is_collision(self, other):
        ## check if self and other collide
        total_normals = self.normals() | other.normals()
        for axis in total_normals:
            min_1, max_1 = self.min_max_proj(axis)
            min_2, max_2 = other.min_max_proj(axis)
            if not(min_1<max_2 and min_2<max_1):
                return False
        return True

""" Circle Class """
class Circle(object):
    def __init__(self, center, r):
        ## center is vector, r is number
        self.center = center
        self.r = r
    def translate(self, shift):
        ## update circle translated by shift
        new_center = self.center.add(shift)
        self.center = new_center
    def rotate_around(self, point, angle):
        ## update circle to be rotated around point by angle
        point_flip = point.scalar(-1.0)
        shift = self.center.add(point_flip)
        rot = shift.rotate(angle)
        final = point.add(rot)
        self.center = final
    def is_poly_collision(self, other):
        ## checks if circle intersects with a polygon
        connectors = []
        flip = self.center.scalar(-1)
        for point in other.vertices:
            edge = point.add(flip)
            connectors.append(edge)
        normals = other.normals()
        for edge2 in connectors:
            if edge2.scalar(-1) not in normals:
                normals.add(edge2)
        for axis in normals:
            proj_cen = self.center.dot(axis)
            min_other, max_other = other.min_max_proj(axis)
            min_cir = proj_cen-self.r
            max_cir = proj_cen+self.r
            if not(min_cir<max_other and min_other<max_cir):
                return False
            return True
    def is_circle_collision(self, other):
        ## checks if circle intersects with circle
        flip = self.center.scalar(-1)
        connector = other.center.add(flip)
        proj_cen_1 = self.center.dot(connector)
        proj_cen_2 = other.center.dot(connector)
        min_1 = proj_cen_1-self.r
        max_1 = proj_cen_1+self.r
        min_2 = proj_cen_2-other.r
        max_2 = proj_cen_2+other.r
        if not(min_1<max_2 and min_2<max_1):
            return False
        return True
    def decompose(self):
        ## decomposes circle into regular hexagon
        vertices = []
        vertices.append(self.center.add(Vector((self.r/((3.0)**.5)),self.r)))  # top left                 1  3
        vertices.append(self.center.add(Vector((self.r/((3.0)**.5)),-self.r)))  # bottom left           6      5    
        vertices.append(self.center.add(Vector(-(self.r/((3.0)**.5)),self.r)))  # top right               2  4
        vertices.append(self.center.add(Vector(-(self.r/((3.0)**.5)),-self.r)))  # bottom right
        vertices.append(self.center.add(Vector((2.0*self.r/((3.0)**.5)),0)))  # right
        vertices.append(self.center.add(Vector(-(2.0*self.r/((3.0)**.5)),0))) # left
        return Polygon(self.center, vertices)

def convex_hull(polygons):
    def compare(a,b):
        ## metric for comparing two vectors
        ans = a.orientation(b)
        if ans == 0:
            if a.mag() >= b.mag():
                return 1
            else:
                return -1
        else:
            return ans
    ## find convex full surrounding list of Polygons using Graham's scan
    ## return Hull as list of vector points in original coordinate system
    points = []
    for poly in polygons:
        if type(poly) == Circle:
            poly = poly.decompose()
        temp = poly.vertices
        for point in temp:
            points.append(point)
    if len(points) == 3:
        x_tot = 0
        y_tot = 0
        for point in points:
            x_tot += point.x
            y_tot += point.y
        cen = Vector(x_tot/3.0,y_tot/3.0)
        return Polygon(cen, points)
    if len(points) < 3:
        return None
    p0 = min(points, key=lambda x: (x.y,x.x))
    points.remove(p0)
    p0_ = p0.scalar(-1.0)
    for point in points:
        point.add(p0_)
    s_points = sorted(points, cmp=compare)
    floor = Vector(1,0)
    count = 0
    i = 0
    tot = len(s_points)
    while count<tot-1:  ## remove extra points of the same angle
        if s_points[i].angle(floor) == s_points[i+1].angle(floor):
            s_points.pop(i)
            i-=1
        i+=1
        count+=1
    stack = [Vector(0,0)]
    for i in range(1):
        stack.append(s_points[i])
    for i in range(1, len(s_points)-1):
        stack.append(s_points[i])
        prev = stack[-2]
        curr = stack[-1]
        next = s_points[i+1]
        first = curr.add(prev.scalar(-1.0))
        second = next.add(curr.scalar(-1.0))
        check = first.orientation(second)
        if check != -1:
            stack.pop(-1)
    ans = []
    for point in stack:
        ans.append(point.add(p0))
    ## find center of the hull
    x_tot = 0
    y_tot = 0
    for point in ans:
        x_tot += point.x
        y_tot += point.y
    cen = Vector(x_tot/float(len(ans)),y_tot/float(len(ans)))
    return Polygon(cen,ans)











