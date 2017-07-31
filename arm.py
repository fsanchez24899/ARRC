import math
from RRT import Node, C_Space, RRT
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


    """ Rerack constants """
    ## user input codes to rack name
    ## TODO: Alexa output to rack names
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
    def get_compatible_coords(self):
        ''' get coordinates for gui '''
        gui_shift = 500
        return [gui_shift+self.center[0]-self.radius, gui_shift+self.center[1]-self.radius, gui_shift+self.center[0]+self.radius, gui_shift+self.center[1]+self.radius]


""" Arm Class """
class Arm(object):
    def __init__(self, center, orientation=0):
        self.center = center  ## x,y coordinate of center of Equilateral Triangle
        self.orientation = orientation  ## angle of rotation off of perfect vertical 
                                        #like so: triangle, positive is clockwise
        self.pcups = {}  ## cups currentluy picked up mapped to by magnet label to which they are locked
    def move(self, target, rotation):
        ''' translate triangle center to "target" (given as Vector) and rotate as given '''
        pass
    def lock(self, label):
        ''' lock magnet "label" to pick up cup '''
        ## TODO: when a cup is picked up update its label
        pass

""" Game Class """
class Game(object):
    def __init__(self, rack="FULLRACK"):
        self.cups = {}  ## all cups in game mapped by ID 
        self.rack = rack  ## current rack
        self.triangle = Arm(Constants.CENTER)  ## triangle arm initialized to starting position
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
        num_live = 0  ## number of cups still in play
        for cup in self.cups.values():
            if cup.live:
              num_live += 1
        rack = None  ## desired rerack
        for statement in Constants.RERACKS:
            if command == statement:
                rack = statement
        if rack != 0:
            labels = Constants.RERACK_MAP[Constants.RERACKS[rack]]
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
        ''' Perform all necessary actions to rerack game state '''
        ## only to be called if rerack_target_labels was successful    
        def pickup(self, cup_id, label):
            ''' move triange to pickup cup with id "cup_id" using magnet "label" and update game state accordingly '''
            ## TODO: call robot movement stuff here
            init_tar = self.cups[cup_id].center
            coord = Constants.TEN_CUP_MAP[label]
            shift = Vector(coord[0],coord[1])
            fin_tar = init_tar.add(shift)
            # move triangle center to fin_tar
            # self.triangle.move(fin_tar)
            # self.triangle.lock(label)
            # self.triangle.pcups[label] = self.cups[cup_id]







