import math

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
    TABLE_HEIGHT = TRIANGLE_LENGTH*(3.0**.5)/2.0+8.0*RADIUS  ## triangle plus 4 cups over
    TABLE_WIDTH = TRIANGLE_LENGTH+16.0*RADIUS  ## triangle plus 4 cups each sude

    """ Rerack constants """
    ## user input codes to rack name
    ## TODO: Alexa output to rack names
    RERACKS_NAME = {'':'FULLRACK',
                    '':'THREETWOONE',
                    'sidecar':'SIDECAR',
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
                  'SIDECAR':[2,4,5,7,8],
                  'WIZARDSTAFF':[],
                  'TWOBYTWO':[],
                  'PLAYBUTTON':[],
                  'STOPLIGHT':[],
                  'GENTLEMANS':[],
                  'CENTER':[]
                    }
    ## rerack name to center position and rotaiton [pos_x, pos_y, rot]
    ## TODO: Fill center position/orientaiton of every rack by measuring table
    RERACK_LOCS = {'FULLRACK':[],
                   'THREETWOONE':[],
                   'SIDECAR':[CENTER,1.0472],
                   'WIZARDSTAFF':[],
                   'TWOBYTWO':[],
                   'PLAYBUTTON':[],
                   'STOPLIGHT':[],
                   'GENTLEMANS':[],
                   'CENTER':[]
                    }

""" Tuning Variable Class """
class Tuners(object):
    TUNING = [1,1.1*((Constants.TABLE_WIDTH**2+Constants.TABLE_HEIGHT**2)**.5)/(2.0*math.pi)]  ## use to tune distance metric, sum should be 1
    RESOLUTION = 15  ## use to tune line search
    EPSILON = 2  ## use to tune new node finding
    DELTA = .3  ## use to tune goal finding
    PHI = 1  ## use to tune end state
    ITERATIONS = 500  ## use to tune runtime 

