from RRT import Node, C_Space, RRT
from vectors import *

### Constants ###

""" Cup constants """
RADIUS = 5.0
TOLERANCE = .5

""" Arm constants """
TRIANGLE_LENGTH = RADIUS*4*2
CENTER = """ PICK VALUE  """
## Cup index: (x-shift,y-shift) where shift is from center of cup ##
## all locations based on properly oriented 10-rack coordinate system (aka shifts away from center of triangle)
TEN_CUP_MAP = {1: (0,TRIANGLE_LENGTH*(3.0**.5)/2.0-RADIUS),
               2: (-1.0*RADIUS,TRIANGLE_LENGTH*(3.0**.5)/2.0-3.0*RADIUS),
               3: (RADIUS,TRIANGLE_LENGTH*(3.0**.5)/2.0-3.0*RADIUS),
               4: None,
               5: (0,0),
               6: None,
               7: None,
               8: None,
               9: None,
               10: None}

""" Game constants """


""" Rerack Class """
class Reracks(object):
    ## user input codes to rack name
    RERACKS = {'':'FULLRACK',
               '':'THREETWOONE',
               '':'SIDECAR',
               '':'WIZARDSTAFF',
               '':'TWOBYTWO',
               '':'PLAYBUTTON',
               '':'STOPLIGHT',
               '':'GENTLEMANS',
               '':'CENTER'
               }
    ## rerack name to locations list
    ## locations lists list cup coordinates in order of increasing y-coordinate with lowest x-coordinate tie breaker
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

""" Cup Class """
class Cup(object):
    CUP_RADIUS = RADIUS
    def __init__(self, iden, center, live=True):
        self.iden = iden  ## unique ID number
        self.center = center  ## coordinates of center AS VECTOR
        self.circle = Circle(center,Cup.CUP_RADIUS+TOLERANCE)  ## Circle object to represent cup
        self.live = live
        self.radius = Cup.CUP_RADIUS
        self.ncs = self.get_compatible_coords()
    def kill(self):
        self.live = False
        self.center = None ## deadzone coordinate
    def get_compatible_coords(self):
        gui_shift = 500
        return [gui_shift+self.center[0]-self.radius, gui_shift+self.center[1]-self.radius, gui_shift+self.center[0]+self.radius, gui_shift+self.center[1]+self.radius]


""" Arm Class """
class Arm(object):
    def __init__(self, center, orientation=0):
        self.center = CENTER  ### x,y coordinate of center of Equilateral Triangle
        self.orientation = orientation  ### angle of rotation off of perfect vertical 
                                        #like so: triangle, positive is clockwise
        self.pcups = {}  ## cups currentluy picked up mapped to by magnet label to which they are locked
    def move(self, target):
        ## move triangle center to "target" (given as Vector)
        pass
    def lock(self, label):
        ## lock magnet "label" to pick up cup
        pass

""" Game Class """
class Game(object):
    def __init__(self, rack="FULLRACK"):
        self.cups = {}  ## all cups in game
        self.rack = rack  ## current rack
        self.triangle = Arm(CENTER)  ## triangle arm initialized to starting position
        ## initialize starting rack
        shift = Vector(self.triangle[0],self.triangle[1])
        for i in range(1,11):
            coords = TEN_CUP_MAP[i]
            coord = Vector(coords[0],coords[1])
            final = coord.add(shift)
            cup = Cup(i,final)
            self.cups[i] = cup
    def rerack_target_labels(self, command):
        ## Return list of labels for cups in 'command' rerack in triangle coordinates, or return failure
        num_live = 0  ## number of cups still in play
        for cup in self.cups.values():
            if cup.live:
              num_live += 1
        rack = None  ## desired rerack
        for statement in Reracks.RERACKS:
            if command == statement:
                rack = statement
        if rack != 0:
            labels = RERACK_MAP[RERACKS[rack]]
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
    def rerack(self, command):
        ## only to be called if rerack_target_labels was successful    
        def pickup(self, cup_id, label):
            ## move triange to pickup cup with id "cup_id" using magnet "label" and update game state accordingly
            ## TODO: call robot movement stuff here
            init_tar = self.cups[cup_id].center
            coord = TEN_CUP_MAP[label]
            shift = Vector(coord[0],coord[1])
            fin_tar = init_tar.add(shift)
            # move triangle center to fin_tar
            # self.triangle.move(fin_tar)
            # self.triangle.lock(label)
            # self.triangle.pcups[label] = self.cups[cup_id]







