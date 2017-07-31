import math
from random import uniform
from vectors import Vector, Polygon, Circle
from arm import *

TUNING = [1,1]  ## use to Tune distance metric
RESOLUTION = 1  ## use to tune line search
EPSILON = 1  ## use to tune new node finding
DELTA = 1  ## use to tune goal finding
PHI = 1  ## use to tune end state
ITERATIONS = 500  ## use to tune runtime 

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
        return dist*TUNING[0]+rot*TUNING[1]
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
top = Polygon(Vector(0,Constants.TABLE_HEIGHT+Constants.RADIUS-Constants.TRIANGLE_LENGTH*(3.0**.5)/6.0),
    [Vector(Constants.TABLE_WIDTH/2.0,Constants.TABLE_HEIGHT-Constants.TRIANGLE_LENGTH*(3.0**.5)/6.0),
    Vector(-Constants.TABLE_WIDTH/2.0,Constants.TABLE_HEIGHT-Constants.TRIANGLE_LENGTH*(3.0**.5)/6.0),
    Vector(Constants.TABLE_WIDTH/2.0,Constants.TABLE_HEIGHT+2.0*Constants.RADIUS-Constants.TRIANGLE_LENGTH*(3.0**.5)/6.0),
    Vector(-Constants.TABLE_WIDTH/2.0,Constants.TABLE_HEIGHT+2.0*Constants.RADIUS-Constants.TRIANGLE_LENGTH*(3.0**.5)/6.0)])
bot = Polygon(Vector(0,-Constants.TRIANGLE_LENGTH*(3.0**.5)/6.0-Constants.RADIUS),
    [Vector(Constants.TABLE_WIDTH/2.0,-Constants.TRIANGLE_LENGTH*(3.0**.5)/6.0),
    Vector(-Constants.TABLE_WIDTH/2.0,-Constants.TRIANGLE_LENGTH*(2.0**.5)/6.0),
    Vector(Constants.TABLE_WIDTH/2.0,-Constants.TRIANGLE_LENGTH*(3.0**.5)/6.0-2.0*Constants.RADIUS)
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
barrier = [top, left, bot, right]

""" C_Space Class """
class C_Space(object):
    def __init__(self, shape, obstacles):
        ## shape is blob of cups, obstacles is list of Polygon/Circle obstacles in R2
        ## barriers is edge of map represented by polygons above
        self.shape = shape
        self.obstacles = obstacles
        self.barriers = barrier
    def point_collision(self, vec):
        ''' determine if configuration vec collides with any obstacle '''
        ## determine if triangle is in bounds
        top = Vector(vec.x,vec.y+Constants.TRIANGLE_LENGTH*(3.0**.5)/3.0)
        left = Vector(vec.x+Constants.TRIANGLE_LENGTH/2.0,vec.y-(TRIANGLE_LENGTH*(3.0**.5)/6.0))
        right = Vector(vec.x-Constants.TRIANGLE_LENGTH/2.0,vec.y-(TRIANGLE_LENGTH*(3.0**.5)/6.0))
        triangle = Polygon(vec.x,vec.y,[top,left,right],vec.a)
        for edge in self.barriers:
            if edge.is_collision(triangle):
                return True
        ## dtermine if blob of cups is colliding
        shape = Polygon(self.shape.center,self.shape.vertices,self.shape.rotation)
        shape.translate(Vector(vec.x-shape.center.x,vec.y-shape.center.y))
        shape.rotate_around(triangle.center,vec.a)
        for obstacle in obstacles:
            if obstacle is Circle:
                if shape is Circle:
                    if obstacle.is_circle_collision(shape):
                        return True
                elif shape is Polygon:
                    if obstacle.is_poly_collision(shape):
                        return True
            elif obstacle is Polygon:
                if shape is Circle:
                    if shape.is_poly_collision(obstacle):
                        return True
                elif shape is Polygon:
                    if shape.is_collision(obstacle):
                        return True
            else:
                return None
        return False
    def line_collision(self, start, end):
        ''' determines if line segment intersects with obstacle via sampling '''
        resolution = RESOLUTION  ## sample resolution in form of max distance allowed between samples
        direction = start.scalar(-1).add(end)
        norm = direction.metric(Vector_3(0,0,0))
        samp = start
        scale = resolution
        while samp.metric(end)>resolution:
            norm = norm.scalar(scale)
            next = start.add(norm)
            if point_collision(next):
                return False
            scale+=resolution
        return True 

""" RRT Class """
class RRT(object):
    def __init__(self, root, c_space):
        ## root is root node, c_space gives collision function, nodes is tree in dictionary representation
        self.nodes = [root]
        self.c_space = c_space
    def select_rand(self):
        ''' select new random point to explore '''
        new_x = random.uniform(a,b) ### FILL a,b
        new_y = random.uniform(c,d) ### FILL c,d
        new_rotation = random.uniform(0,math.pi)
        return Vector_3(new_x, new_y, new_rotation)
    def find_nearest_node(self, vertex):
        ''' find node in vertex nearest to "vertex" '''
        min_dist = float(infty)
        min_node = None
        for node in self.nodes:
            dist = vertex.data.metric(node.data)
            if dist < min_dist:
                min_dist = dist
                min_node = node
        return min_node
    def new_node(self, vertex, point):
        ''' find the new node by moving form nearest (vertex) to rand (point) RETURNS VEC3 POINT!!! '''
        vec = vertex.data
        direction = vec.scalar(-1).add(point)
        mag = direction.metric(Vector_3(0,0,0))
        mag*=EPSILON
        return vec.add(direction.scalar(mag))
    def expand_tree(self):
        ''' expand tree by finding nearest viable node '''
        viable = False
        new_point = select_rand()
        while not viable:
            if self.c_space.point_collision(new_point):
                new_point = select_rand()
            else:
                viable = True
        nearest = find_nearest_node(new_point)
        new_node = new_node(nearest,new_point)
        if not self.c_space.line_collision(nearest.data,new_node):
            self.nodes.append(Node(new_node, [], nearest))
        else:
            expand_tree()
    def find_goal(self, target):
        ''' find goal region given target x,y coordinates '''
        ## TODO: Fix this and maybe move it to a different place (game class?)
        x = Vector_3(target[0],target[1],root.data.a)
        valid = not self.c_space.point_collision(x):
        if valid:    
            return x
        else:
            count = 1
            while not valid:
                if count%2 == 0:
                    new_x = x.add(Vector_3(0,0,DELTA*count))
                else:
                    new_x = x.add(Vector_3(0,0,DELTA*-1*count))
                valid = not self.c_space.point_collision(new_x)
            return new_x
    def find_path(self, target):
        ''' return the shortest valid path to target from root by expanding RRT '''
        ## TODO: Finish implementing this
        target = find_goal(target)
        recent = self.nodes[-1]
        itera = 1
        while recent.data.metric(target)>PHI and itera<ITERATIONS:
            expand_tree()
            recent = self.nodes[-1]
            itera+=1
        if itera = ITERATIONS:
            ## RRT failed (TODO: what to do next?)
        else:
            self.nodes.append(Node(target, [], recent))  ## adds target to tree
            ## find path by backtracking (every node only has 1 parent)
            path = []
            current = self.nodes[-1]
            while current != nodes[0]
                path.append(current)  ## will never append root config
                current = current.parent
            states = []
            for node in path[::-1]:
                states.append(node.data)
            return states  ## returns states in form of Vector_3 objects
            ## TODO: do path smoothing (if necessary)









