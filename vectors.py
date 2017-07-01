import math

""" 2D Vector Class """
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
        cx = c*x
        cy = c*y
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
        ## get vector rotated by angle
        new_x = math.cos(angle)*self.x + -math.sin(angle)*self.y
        new_y = math.sin(angle)*self.x + math.cos(angle)*self.y
        return Vector(new_x, new_y)
    def orientation(self, v1):
        ## find clockwise/cunterclockwise orientaiton of self and v1
        if self.slope() = v1.slope():
            return 0  ## colinear
        elif self.slope() < v1.slope()
            return -1  ## counterclockwise
        elif self.slope() > v1.slope():
            return 1  ## clockwise

""" Polygon Class """
## Convex Polygons only (no circles see below)
class Polygon(object):
    def __init__(self, center, vertices, rotation=0):
        ## center and vertices (list) are vectors
        self.center = center
        self.vertices = vertices
        self.rotation = rotation
    def rotate(self, angle):
        ## get polygon rotated by angle
        new_vertices = []
        for vertex in self.vertices:
            new_vertex = vertex.rotate(angle)
            new_vertices.append(new_vertex)
        return Polygon(center, new_vertices, angle)
    def translate(self, shift):
        ## get polygon translated by vector "shift"
        new_vertices = []
        for vertex in self.vertices:
            new_vertex = vertex.add(shift)
            new_vertices.append(new_vertex)
        new_center = center.add(shift)
        return Polygon(new_center, new_vertices, self.rotation)
    def normals(self):
        ## list of normal vectors
        edges = []
        for i in range(len(self.vertices-1)):
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
        total_normals = self.normals() + other.normals()
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
        ## get circle translated by shift
        new_center = self.center.add(shift)
        return Polygon(new_center, self.r)
    def is_poly_collision(self, other):
        ## checks if circle intersects with a polygon
        connectors = []
        flip = self.center.scalar(-1)
        for point in other.vertices:
            egde = point.add(flip)
            connectors.append(edge)
        normals = other.normals()
        for edge in connectors:
            if edge.scalar(-1) not in normals:
                normals.add(edge)
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
        vertices.append(self.center.add(Vector((self.r/((3.0)**.5)),self.r)))  # top left
        vertices.append(self.center.add(Vector((self.r/((3.0)**.5)),-self.r)))  # bottom left
        vertices.append(self.center.add(Vector(-(self.r/((3.0)**.5)),self.r)))  # top right
        vertices.append(self.center.add(Vector(-(self.r/((3.0)**.5)),-self.r)))  # bottom right
        vertices.append(self.center.add(Vector((2.0*self.r/((3.0)**.5)),0)))  # right
        vertices.append(self.center.add(Vector(-(2.0*self.r/((3.0)**.5)),0))) # left
        return Polygon(self.center, vertices)

def compare(a,b):
    ## compare two vectors
    ans = a.orientation(b)
    if ans = 0:
        if a.mag() >= b.mag():
            return 1
        else:
            return -1
    else:
        return ans

def convex_hull(polygons):
    ## find convex full surrounding list of Polygons using Graham's scan
    points = []
    for poly in polygons:
        temp = poly.vertices
        for point in temp:
            points.append(point)
    p0 = min(points, key=lambda x: (x.y,x.x))
    points.remove(p0)
    p0_ = p0.scalar(-1.0)
    for point in points:
        point.add(p0_)
    s_points = sorted(points, cmp=compare)
    stack = [Vector(0,0)]
    for i in range(2):
        stack.append(s_points[i])
    for i in range(2, len(s_points)-1):
        right = True
        while right:
            first = stack[-2].add(stack[-3].scalar(-1))
            second = stack[-1].add(stack[-2].scalar(-1))
            check = first.orientation(second)
            if check == -1:
                right = False
            stack.pop(-1)
        stack.append(s_points[i])
    ans = []
    for point in stack:
        ans.append(point.add(p0))
    return ans











