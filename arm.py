import math
import RRT
from vectors import *

""" Constants Class """
class Constants(object):

    """ Cup constants """
    RADIUS = 5.0
    TOLERANCE = .5

    """ Arm constants """
    CORNER_SHIFT = RADIUS*(3.0**.5-1.0)
    TRIANGLE_LENGTH = 4.0*RADIUS*2.0+2*CORNER_SHIFT
    CENTER = (0,0)
    ## all label locations based on properly oriented 10-rack coordinate system
    ## distances are shifts away from center of triangle
    TEN_CUP_MAP = {1: (0,TRIANGLE_LENGTH*(3.0**.5)/3.0-2.0*RADIUS),
                   2: (RADIUS,RADIUS*(3.0**.5)),
                   3: (-RADIUS,RADIUS*(3.0**.5)),
                   4: (2.0*RADIUS,0),
                   5: (0,0),
                   6: (-2.0*RADIUS,0),
                   7: (TRIANGLE_LENGTH/2.0-CORNER_SHIFT-RADIUS,-(TRIANGLE_LENGTH*(3.0**.5)/6.0-RADIUS)),
                   8: (TRIANGLE_LENGTH/2.0-CORNER_SHIFT-3.0*RADIUS,-(TRIANGLE_LENGTH*(3.0**.5)/6.0-RADIUS)),
                   9: (-(TRIANGLE_LENGTH/2.0-CORNER_SHIFT-3.0*RADIUS),-(TRIANGLE_LENGTH*(3.0**.5)/6.0-RADIUS)),
                   10: (-(TRIANGLE_LENGTH/2.0-CORNER_SHIFT-RADIUS),-(TRIANGLE_LENGTH*(3.0**.5)/6.0-RADIUS))}

    """ Game constants """
    TABLE_HEIGHT = TRIANGLE_LENGTH*(3.0**.5)/2.0+6.0*RADIUS
    TABLE_WIDTH = TRIANGLE_LENGTH+12.0*RADIUS

    """ Rerack constants """
    ## user input codes to rack name
    ## TODO: Alexa output to rack names
    RERACKS_NAME = {'':'FULLRACK',
                    '':'THREETWOONE',
                    '':'SIDECAR',
                    '':'WIZARDSTAFF',
                    '':'TWOBYTWO',
                    '':'PLAYBUTTON',
                    '':'STOPLIGHT',
                    '':'GENTLEMANS',
                    '':'CENTER'
                    }
    ## rerack name to label list
    ## lists label in order of increasing y-coordinate with lowest x-coordinate tie breaker
    ## TODO: use ARRC notebook drawing to map these to labels from TEN_CUP_MAP
    RERACK_MAP = {'FULLRACK':[],
                  'THREETWOONE':[],
                  'SIDECAR':[],
                  'WIZARDSTAFF':[],
                  'TWOBYTWO':[],
                  'PLAYBUTTON':[],
                  'STOPLIGHT':[],
                  'GENTLEMANS':[],
                  'CENTER':[]
                    }
    ## rerack name to center position and rotaiton [pos,rot]
    ## TODO: Fill center position/orientaiton of every rack
    RERACK_LOCS = {'FULLRACK':[],
                   'THREETWOONE':[],
                   'SIDECAR':[],
                   'WIZARDSTAFF':[],
                   'TWOBYTWO':[],
                   'PLAYBUTTON':[],
                   'STOPLIGHT':[],
                   'GENTLEMANS':[],
                   'CENTER':[]
                    }

""" Cup Class """
class Cup(object):
    def __init__(self, iden, center, label, live=True):
        self.iden = iden  ## unique ID number
        self.center = center  ## coordinates of center AS A VECTOR
        self.circle = Circle(center,Constants.RADIUS+Constants.TOLERANCE)  ## Circle object to represent cup
        self.live = live
        self.label = label  ## label of magnet to which cup is assigned
        self.radius = Constants.RADIUS
        self.ncs = self.get_compatible_coords()  ## gui stuff
    def kill(self):
        ''' kill a cup and reset it '''
        self.live = False
        self.center = None  ## deadzone coordinate
        self.circle = None
    def get_compatible_coords(self):
        ''' get coordinates for gui '''
        gui_shift = 500
        return [gui_shift+self.center[0]-self.radius, gui_shift+self.center[1]-self.radius, gui_shift+self.center[0]+self.radius, gui_shift+self.center[1]+self.radius]


""" Arm Class """
class Arm(object):
    def __init__(self, center):
        self.triangle = RRT.gen_triangle(center)
        self.pcups = {}  ## cups currentluy picked up mapped to by magnet label to which they are locked
    def move(self, target, rotation):
        ''' translate triangle center to "target" (given as Vector) and rotate as given '''
        ## TODO: implement this
        pass
    def lock(self, label):
        ''' lock magnet "label" to pick up cup '''
        ## TODO: Implement this
        ## TODO: when a cup is picked up update its label
        pass

""" Game Class """
class Game(object):
    def __init__(self, rack="FULLRACK"):
        self.cups = {}  ## all cups in game mapped by ID 
        self.field_cups = {}  ## all cups on field (not locked on triangle) mapped by ID
        self.rack = rack  ## current rack
        self.arm = Arm(Constants.CENTER)  ## triangle arm initialized to starting position
        ## initialize starting rack
        shift = Vector(self.triangle.center.x, self.triangle.center.y)
        letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
        for i in range(1,11):
            coords = Constants.TEN_CUP_MAP[i]
            coord = Vector(coords[0],coords[1])
            final = coord.add(shift)
            cup = Cup(letters[i],final,i)
            self.cups[letters[i]] = cup
    def rerack_target_labels(self, command):
        ''' Return list of labels for cups in 'command' rerack in triangle coordinates, or return failure '''
        ## TODO: Fix "bad input" stuff to be useful in play
        num_live = 0  ## number of cups still in play
        for cup in self.cups.values():
            if cup.live:
              num_live += 1
        rack = None  ## desired rerack
        for statement in Constants.RERACKS_NAME:
            if command == statement:
                rack = statement
        if rack != 0:
            labels = Constants.RERACK_MAP[Constants.RERACKS_NAME[rack]]
            if len(labels)!=num_live:
                ## Ask User to try different rerack
                print "Bad Input"
                return
            else:
                self.rack = rack
                return labels
        else:
            ## Ask User to try different command
            print "Bad Input"
            return
    def move_cups_to_field(self):
        for cup in self.cups.values():
            if cup.live:
                self.field_cups[cup.iden] = cup
    def generate_obstacles(self):
        obstacles = []
        for cup in self.field_cups:
            obstacles.append(cup.circle)
        return obstacles
    def pickup(self, cac, tot):
        ## cac is cup as circle object and tot is target on triangle in vector form
        ## generate c_space
        polys = self.triangle.pcups.values()
        shape = convex_hull(polys)
        obstacles = generate_obstacles()
        space = RRT.C_Space(shape, obstacles)
        ## goal finding
        new_cen = cac.add(tot.scalar(-1.0))
        shift = new_cen.add(tot)
        init_goal = RRT.Vector_3(new_cen.x, new_cen.y, 0)
        valid = not space.point_collision(init_goal)
        triangle = RRT.gen_triangle(init_goal)
        if valid:    
            goal = init_goal
        else:
            rot = 0
            count = 1
            while not valid:
                if count%2 == 0:
                    rot = RRT.DELTA*count
                else:
                    rot = -1.0*RRT.DELTA*count
                triangle.rotate_around(shift, rot)
                valid = not space.point_collision(RRT.Vector_3(triangle.center.x,triangle.center.y,triangle.rotation))
            goal = RRT.Vector_3(triangle.center.x,triangle.center.y,triangle.rotation)
        ## generate RRT and get path
        root = RRT.Node(RRT.Vector_3(self.arm.triangle.center.x,self.arm.triangle.center.y,self.arm.triangle.rotation))
        tree = RRT.RRT(root,space)
        path = tree.find_path(goal)
        ## move robot
        ## TODO: Fill here -move robot and -pickup cup
        ## update game
        self.arm.triangle.translate(Vector(goal.x,goal.y))
        self.arm.triangle.rotate(goal.a)
        ## updates cups in main rerakcing method
    def rerack(self, command):
        ''' Perform all necessary actions to rerack game state '''
        target_list = rerack_target_labels(command)
        move_cups_to_field()
        ## get live cups in order of height
        heights = []
        for cup in self.field_cups.values():
            heights.append(cup)
        heights = sorted(heights, key=lambda x: x.center.y, reverse=True)
        ## pickup all cups in right order
        i = 0
        for cup in heights:
            ## pickup cups in height order
            label = target_list[i]
            i+=1
            target_on_triangle = Constants.TEN_CUP_MAP[label]
            tot_as_vec = Vector(target_on_triangle[0],target_on_triangle[1])
            cup_as_circle = cup.circle
            pickup(cup_as_circle, tot_as_vec)
            del self.field_cups[cup.iden]
        ## move arm to final position
        ## TODO: Fill using Constants.RERACK_LOCS






