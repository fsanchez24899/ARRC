import math
from random import uniform
from vectors import Vector, Polygon, Circle
from variables import Constants, Tuners

""" Node Class """
class Node(object):
    def __init__(self, coordinate, children, parent):
        ''' coordinate is point in C-Space, children is list of Nodes, parent is Node '''
        self.data = coordinate
        self.children = children
        self.parent = parent

""" 3D Vector Class """
## Represents R2x[0,2pi) with special metric
class Vector_3(object):
    def __init__(self, x, y, a):
        ## a is angle
        self.x = x
        self.y = y
        self.a = a
    def add(self, other):
        ''' get vector that adds other to self '''
        x = self.x+other.x
        y = self.y+other.y
        a = self.a+other.a
        return Vector_3(x,y,a)
    def metric(self, other):
        ''' give distance between self and other in this space '''
        ''' give higher weight to translation over rotation through "tuning" parameters'''
        dist = ((other.x-self.x)**2+(other.y-self.y)**2)**.5
        rot = abs(other.a-self.a)
        return dist*Tuners.TUNING[0]+rot*Tuners.TUNING[1]
    def normalize(self):
        ''' normalize self '''
        mag = self.metric(Vector_3(0,0,0))
        x = self.x/mag
        y = self.y/mag
        a = self.a/mag
        return Vector_3(x,y,a)
    def scalar(self,c):
        ''' multiply by scalar '''
        x = self.x*c
        y = self.y*c
        a = self.a*c
        return Vector_3(x,y,a)

""" Fix Barriers """
## Rectangles on barrier 1 cup thick
def fix_barriers():
    top = Polygon(Vector(0,Constants.TABLE_HEIGHT+Constants.RADIUS-Constants.TRIANGLE_LENGTH*(3.0**.5)/6.0),
        [Vector(Constants.TABLE_WIDTH/2.0,Constants.TABLE_HEIGHT-Constants.TRIANGLE_LENGTH*(3.0**.5)/6.0),
        Vector(-Constants.TABLE_WIDTH/2.0,Constants.TABLE_HEIGHT-Constants.TRIANGLE_LENGTH*(3.0**.5)/6.0),
        Vector(Constants.TABLE_WIDTH/2.0,Constants.TABLE_HEIGHT+2.0*Constants.RADIUS-Constants.TRIANGLE_LENGTH*(3.0**.5)/6.0),
        Vector(-Constants.TABLE_WIDTH/2.0,Constants.TABLE_HEIGHT+2.0*Constants.RADIUS-Constants.TRIANGLE_LENGTH*(3.0**.5)/6.0)])
    bot = Polygon(Vector(0,-Constants.TRIANGLE_LENGTH*(3.0**.5)/6.0-Constants.RADIUS),
        [Vector(Constants.TABLE_WIDTH/2.0,-Constants.TRIANGLE_LENGTH*(3.0**.5)/6.0),
        Vector(-Constants.TABLE_WIDTH/2.0,-Constants.TRIANGLE_LENGTH*(2.0**.5)/6.0),
        Vector(Constants.TABLE_WIDTH/2.0,-Constants.TRIANGLE_LENGTH*(3.0**.5)/6.0-2.0*Constants.RADIUS),
        Vector(-Constants.TABLE_WIDTH/2.0,-Constants.TRIANGLE_LENGTH*(3.0**.5)/6.0-2.0*Constants.RADIUS)])
    left = Polygon(Vector(Constants.TABLE_WIDTH/2.0+Constants.RADIUS,0),
        [Vector(Constants.TABLE_WIDTH/2.0,Constants.TABLE_HEIGHT-Constants.TRIANGLE_LENGTH*(3.0**.5)/6.0),
        Vector(Constants.TABLE_WIDTH/2.0+2.0*Constants.RADIUS,Constants.TABLE_HEIGHT-Constants.TRIANGLE_LENGTH*(3.0**.5)/6.0),
        Vector(Constants.TABLE_WIDTH/2.0,-Constants.TRIANGLE_LENGTH*(3.0**.5)/6.0),
        Vector(Constants.TABLE_WIDTH/2.0+2.0*Constants.RADIUS,-Constants.TRIANGLE_LENGTH*(3.0**.5)/6.0)])
    right = Polygon(Vector(-(Constants.TABLE_WIDTH/2.0+Constants.RADIUS),0),
        [Vector(-Constants.TABLE_WIDTH/2.0,Constants.TABLE_HEIGHT-Constants.TRIANGLE_LENGTH*(3.0**.5)/6.0),
        Vector(-(Constants.TABLE_WIDTH/2.0+2.0*Constants.RADIUS),Constants.TABLE_HEIGHT-Constants.TRIANGLE_LENGTH*(3.0**.5)/6.0),
        Vector(-Constants.TABLE_WIDTH/2.0,-Constants.TRIANGLE_LENGTH*(3.0**.5)/6.0),
        Vector(-(Constants.TABLE_WIDTH/2.0+2.0*Constants.RADIUS),-Constants.TRIANGLE_LENGTH*(3.0**.5)/6.0)])
    barriers = [top, left, bot, right]
    return barriers

""" Generate Triangle """
def gen_triangle(vec):
    ## vec is center
    top = Vector(vec.x,vec.y+Constants.TRIANGLE_LENGTH*(3.0**.5)/3.0)
    left = Vector(vec.x+Constants.TRIANGLE_LENGTH/2.0,vec.y-(Constants.TRIANGLE_LENGTH*(3.0**.5)/6.0))
    right = Vector(vec.x-Constants.TRIANGLE_LENGTH/2.0,vec.y-(Constants.TRIANGLE_LENGTH*(3.0**.5)/6.0))
    triangle = Polygon(vec,[top,left,right])
    return triangle

""" C_Space Class """
class C_Space(object):
    def __init__(self, shape, obstacles):
        ## shape is blob of cups, obstacles is list of Polygon/Circle obstacles in R2
        ## barriers is edge of map represented by polygons above
        self.shape = shape
        self.obstacles = obstacles
        self.barriers = fix_barriers()
    def point_collision(self, vec):
        ''' determine if configuration vec collides with any obstacle '''
        ## determine if triangle is in bounds
        triangle = gen_triangle(Vector(vec.x,vec.y))
        triangle.rotate(vec.a)
        for edge in self.barriers:
            if edge.is_collision(triangle):
                return True
        ## determine if blob of cups is colliding
        if self.shape is not None:
            shape = Polygon(self.shape.center,self.shape.vertices,self.shape.rotation)
            shape.translate(Vector(vec.x-shape.center.x,vec.y-shape.center.y))
            shape.rotate_around(triangle.center,vec.a)
            for obstacle in self.obstacles:
                if type(obstacle) == Circle:
                    if type(shape) == Circle:
                        if obstacle.is_circle_collision(shape):
                            return True
                    elif type(shape) == Polygon:
                        if obstacle.is_poly_collision(shape):
                            return True
                elif type(obstacle) == Polygon:
                    if type(shape) == Circle:
                        if shape.is_poly_collision(obstacle):
                            return True
                    elif type(shape) == Polygon:
                        if shape.is_collision(obstacle):
                            return True
                else:
                    return None
        return False
    def line_collision(self, start, end):
        ''' determines if line segment intersects with obstacle via sampling '''
        resolution = Tuners.RESOLUTION  ## sample resolution in form of max distance allowed between samples
        direction = start.scalar(-1).add(end)
        #norm = direction.metric(Vector_3(0,0,0))
        #direction = direction.scalar(1.0/float(norm))
        samp = start
        scale = 1.0/float(resolution)
        #dist = samp.metric(end)
        for i in range(resolution):
            temp = samp.metric(end)
            direction = direction.scalar(scale)
            next = start.add(direction)
            if self.point_collision(next):
                return False
            scale+=(1.0/float(resolution))
        return True 

""" RRT Class """
class RRT(object):
    def __init__(self, root, c_space):
        ## root is root node, c_space gives collision function, nodes is tree in dictionary representation
        self.nodes = [root]
        self.c_space = c_space
    def select_rand(self):
        ''' select new random point to explore '''
        new_x = uniform(-Constants.TABLE_WIDTH/2.0,Constants.TABLE_WIDTH/2.0) ### TODO: Fill a,b
        new_y = uniform(-Constants.TABLE_HEIGHT*(3.0**.5)/6.0,Constants.TABLE_HEIGHT-Constants.TABLE_HEIGHT*(3.0**.5)/6.0) ### TODO: Fill c,d
        new_rotation = uniform(0,2*math.pi)
        return Vector_3(new_x, new_y, new_rotation)
    def find_nearest_node(self, vertex):
        ''' find node in vertex nearest to "vertex" '''
        min_dist = float("inf")
        min_node = None
        for node in self.nodes:
            dist = vertex.metric(node.data)
            if dist < min_dist:
                min_dist = dist
                min_node = node
        return min_node
    def new_node(self, vertex, point):
        ''' find the new node by moving form nearest (vertex) to rand (point) RETURNS VEC3 POINT!!! '''
        vec = vertex.data
        direction = vec.scalar(-1).add(point)
        mag = direction.metric(Vector_3(0,0,0))
        mag/=Tuners.EPSILON
        return vec.add(direction.scalar(1.0/float(mag)))
    def expand_tree(self):
        ''' expand tree by finding nearest viable node '''
        viable = False
        new_point = self.select_rand()
        while not viable:
            if self.c_space.point_collision(new_point):
                new_point = self.select_rand()
            else:
                viable = True
        nearest = self.find_nearest_node(new_point)
        new_node = self.new_node(nearest,new_point)
        if not self.c_space.line_collision(nearest.data,new_node):
            self.nodes.append(Node(new_node, [], nearest))
        else:
            self.expand_tree()
    def find_path(self, target):
        ## target given as Vec_3
        ''' return the shortest valid path to target from root by expanding RRT '''
        recent = self.nodes[-1]
        itera = 1
        while recent.data.metric(target)>Tuners.PHI and itera<Tuners.ITERATIONS:
            self.expand_tree()
            recent = self.nodes[-1]
            itera+=1
        if itera == Tuners.ITERATIONS:
            ## RRT failed (TODO: what to do next?)
            print "RRT Failed"
            return []
        else:
            self.nodes.append(Node(target, [], recent))  ## adds target to tree
            ## find path by backtracking (every node only has 1 parent)
            path = []
            current = self.nodes[-1]
            while current != self.nodes[0]:
                path.append(current)  ## will never append root config
                current = current.parent
            states = []
            for node in path[::-1]:
                states.append(node.data)
            return states  ## returns states in form of Vector_3 objects
            ## TODO: do path smoothing (if necessary)









