import math
from random import uniform
from vectors import Vector, Polygon, Circle

""" Node Class """
class Node(object):
    def __init__(self, coordinate, children, parent):
        ## coordinate is pointi n C-Space, children is list of Nodes, parent is Node
        self.data = coordinate
        self.children = children
        self.parent = parent

""" C_Space Class """
class C_Space(object):
    def __init__(self, obstacles, tuning):
        ## list of Polygon/Circle obstacles in C-Space, tuning parameters
        self.obstacles = obstacles
        self.tuning = tuning
    def metric(self, a, b):
        ## give distance between two points in C-space
        ## give higher weight to translation over rotation through "tuning" parameters
        dist = ((a[0]-b[0])**2+(a[1]-b[1])**2)**.5
        rot = abs(a[2]-b[2])
        return dist.self.tuning[0]+rot*self.tuning[1]
    def point_collision(self, shape):
        ## determine if configuration "shape" collides with any obstacle
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
        ## determines if line segment intersects with obstacle
        pass

""" RRT Class """
class RRT(object):
    def __init__(self, root, c_space):
        ## root is root node, c_space gives collision function, nodes is tree in dictionary representation
        self.nodes = [root]
        self.edges = []
        self.c_space = c_space
    def select_rand(self):
        ## select new random point to explore
        new_x = random.uniform(a,b) ### FILL
        new_y = random.uniform(c,d) ### FILL
        new_rotation = random.uniform(0,math.pi)
        return [new_x, new_y, new_rotation]
    def find_nearest_node(self, vertex):
        ## find node in vertex nearest to "verterx"
        min_dist = float(infty)
        min_node = None
        for node in self.nodes:
            self.c_space.metric(node.data,vertex.data)
            if dist < min_dist:
                min_dist = dist
                min_node = node
        return min_node
    def expand_tree(self):
        ## expand tree by finding nearest viable node
        new_point = select_rand()
        nearest = find_nearest_node(new_point)







