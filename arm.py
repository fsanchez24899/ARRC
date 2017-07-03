from RRT import Node, C_Space, RRT

### Constants ###

""" Cup constants """
RADIUS = 5.0
TOLERANCE = .5

""" Grid constants """
PARTITION = 10.0
TABLE_WIDTH = 16.0
TABLE_HEIGHT = 7.0

""" Arm constants """
TRIANGLE_LENGTH = RADIUS*4*2
### Cup index: (x-shift,y-shift) where shift is from center of cup ###
TEN_CUP_MAP = {1: (0,TRIANGLE_LENGTH*(3.0**.5)/2.0-RADIUS),
               2: (-1.0*RADIUS,TRIANGLE_LENGTH*(3.0**.5)/2.0-3.0*RADIUS)
               3: (RADIUS,TRIANGLE_LENGTH*(3.0**.5)/2.0-3.0*RADIUS)
               4: 
               5: (0,0)
               6:
               7: 
               8:
               9:
               10: }

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
        self.center = center  # coordinates of center
        self.circle = Circle(center,CUP_RADIUS+TOLERANCE)  ## Circle object to represent cup
        self.live = live
    def kill(self):
        self.live = False
        self.center = ## deadzone coordinate

""" Arm Class """
class Arm(object):
    TRIANGLE_LENGTH = 4*2*Cup.CUP_RADIUS
    def __init__(self, center, orientation=0):
        self.center = grid.GRID_CENTER  ### x,y coordinate of center of Equilateral Triangle
        self.orientation = orientation  ### angle of rotation off of perfect vertical like so: ∆, positive is clockwise
        self.cups = grid.cups
        self.targets = grid.targets


""" Game Class """
class Game(object):
    def __init__(self, rack="FULLRACK"):
        self.cups = []  ## all cups in game
        self.rack = rack  ## current rack
    def rerack_target_locations(cups, command):
      ## Return list of locations for cups in 'command' rerack
      num_live = 0  ## number of cups still in play
      for cup in self.cups:
        if cup.live:
          num_live += 1
      rack = None  ## desired rerack
      for statement in Reracks.RERACKS:
          if command == statement:
              rack = statement
      if rack != 0:
          locations = RERACK_MAP[RERACKS[rack]]
          if len(locations)!=num_live:
              ## Ask User to try different rerack
              print "Bad Input"
              return
          else:
              self.rack = rack
              return locations
      elif rack is None:
          ## No change
          return
      else:
          ## Ask User to try different command
          print "Bad Input"
          return







