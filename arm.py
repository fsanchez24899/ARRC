import math
import RRT
from vectors import *
from variables import Constants, Tuners


""" Cup Class """
class Cup(object):
    def __init__(self, iden, center, label, live=True):
        self.iden = iden  ## unique ID number
        self.center = center  ## coordinates of center AS A VECTOR
        self.circle = Circle(center,Constants.RADIUS+Constants.TOLERANCE)  ## Circle object to represent cup
        self.live = live
        self.label = label  ## label of magnet to which cup is assigned
    #    self.ncs = self.get_compatible_coords()  ## gui stuff
    def __str__(self):
        return str(self.iden)
    def __hash__(self):
        return hash(str(self))
    def __eq__(self, other):
        return self.iden == other.iden and self.circle.center == other.circle.center
    def kill(self):
        ''' kill a cup and reset it '''
        self.live = False
        self.circle = None
    #def get_compatible_coords(self):
    #    ''' get coordinates for gui '''
    #    gui_shift = 500
    #    return [gui_shift+self.circle.center[0]-self.circle.r, gui_shift+self.circle.center[1]-self.circle.r, gui_shift+self.circle.center[0]+self.circle.r, gui_shift+self.circle.center[1]+self.circle.r]


""" Arm Class """
class Arm(object):
    def __init__(self, center):
        self.triangle = RRT.gen_triangle(Vector(center[0],center[1]))
        self.pcups = {}  ## cups currentluy picked up mapped to by magnet label to which they are locked
    def move(self, target):
        ''' translate triangle center to "target" (given as Vector_3) '''
        ## TODO: implement actually moving the arm
        goal = Vector(target.x,target.y)
        self.triangle.translate(goal)
        self.triangle.rotate(target.a)
        for cup in self.pcups.values():
            cup.circle.translate(goal)
            cup.circle.rotate_around(self.triangle.center, target.a)
    def lock(self, label, cup):
        ''' lock magnet "label" to pick up cup '''
        ## TODO: Implement actually locking the magnet
        self.pcups[label] = cup
    def unlock_all(self):
        ## unlock all magnets and drop cups
        ## TODO: Implement turning off magnets
        for label in self.pcups:
            self.pcups[label].label = None
            del self.pcups[label]

""" Team Class """
class Team(object):
    def __init__(self, rack="FULLRACK"):
        self.cups = {}  ## all cups in game mapped by ID 
        self.field_cups = {}  ## all cups on field (not locked on triangle) mapped by ID
        self.rack = rack  ## current rack
        self.arm = Arm(Constants.CENTER)  ## triangle arm initialized to starting position
        ## initialize starting rack
        shift = Vector(Constants.CENTER[0],Constants.CENTER[1])
        letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
        for i in range(1,11):
            coords = Constants.TEN_CUP_MAP[i]
            coord = Vector(coords[0],coords[1])
            final = coord.add(shift)
            cup = Cup(letters[i-1],final,i)
            self.cups[letters[i-1]] = cup
    def rerack_target_labels(self, command):
        ''' Return list of labels for cups in 'command' rerack in triangle coordinates, or return failure '''
        ## TODO: Fix "bad input" stuff to be useful in play
        num_live = 0  ## number of cups still in play
        for cup in self.cups.values():
            if cup.live:
              num_live += 1
        rack = None  ## desired rerack
        for statement in Constants.RERACKS_NAME.values():
            if command == statement:
                rack = statement
        if rack != 0:
            labels = Constants.RERACK_MAP[rack]
            if len(labels)!=num_live:
                ## Ask User to try different rerack
                print "Impossible Rack"
                return False
            else:
                self.rack = rack
                return labels
        else:
            ## Ask User to try different command
            print "Bad Input"
            return False
    def kill_cup(self, cup_id):
        cup = self.cups[cup_id]
        #l = None
        #for label in self.arm.pcups:
        #    if self.arm.pcups[label].iden = cup_id:
        #        l = label
        #if l is not None:
        #    cup.kill()
        #    del self.arm.pcups[label]
        # del self.arm.pcups[cup.label]
        cup.kill()
    def move_cups_to_field(self):
        for cup in self.cups.values():
            if cup.live:
                self.field_cups[cup.iden] = cup
    def generate_obstacles(self):
        obstacles = []
        for cup in self.field_cups.values():
            obstacles.append(cup.circle)
        return obstacles
    def pickup(self, cac, tot):
        ## cac is cup as circle object and tot is target on triangle in vector form
        ## generate c_space
        f_cups = self.arm.pcups.values()
        polys = []
        for i in f_cups:
            polys.append(i.circle)
        if len(polys) == 0:
            shape = None
        else:
            shape = convex_hull(polys)
        obstacles = self.generate_obstacles()
        space = RRT.C_Space(shape, obstacles)
        ## goal finding
        new_cen = cac.center.add(tot.scalar(-1.0))
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
                    rot = Tuners.DELTA*count
                else:
                    rot = -1.0*Tuners.DELTA*count
                triangle.rotate_around(shift, rot)
                valid = not space.point_collision(RRT.Vector_3(triangle.center.x,triangle.center.y,triangle.rotation))
            goal = RRT.Vector_3(triangle.center.x,triangle.center.y,triangle.rotation)
        ## generate RRT and get path
        root = RRT.Node(RRT.Vector_3(self.arm.triangle.center.x,self.arm.triangle.center.y,self.arm.triangle.rotation), [], None)
        tree = RRT.RRT(root,space)
        path = tree.find_path(goal)
        ## move robot usinf path
        ## TODO: Fill here -move robot and -pickup cup
        self.arm.move(goal)
    def rerack(self, command):
        ''' Perform all necessary actions to rerack game state '''
        ## Feed command input as processed command (i.e. "FULLRACK")
        target_list = self.rerack_target_labels(command)
        if target_list == False:
            ## rerack failed try again
            ## TODO: Fill here
            print "Rerack fail"
            return
        self.move_cups_to_field()
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
            target_on_triangle = Constants.TEN_CUP_MAP[label]
            tot_as_vec = Vector(target_on_triangle[0],target_on_triangle[1])
            cup_as_circle = cup.circle
            self.pickup(cup_as_circle, tot_as_vec)
            self.arm.lock(i,cup)
            cup.label = i
            del self.field_cups[cup.iden]
            i+=1
        ## move arm to final position
        ## TODO: Fill using Constants.RERACK_LOCS
        final = Constants.RERACK_LOCS[command]
        self.arm.move(Vector_3(final[0],final[1],final[2]))
        # drop all cups
        self.arm.unlock_all()

""" Game Function """
def game():
    ## initialize teams
    red_team = Team()
    blue_team = Team()
    ## loop
    in_game = True
    while in_game:
        ## look for unstated changes
        ## TODO: check magnets for a removed cup
        ## look for stated commands
        ## TODO: take user input
        command = str(raw_input("Input here: "))
        #print str(command[-1])
        if "kill" in command:
            if "red team" in command:
                red_team.kill_cup("A")
                red_team.kill_cup("B")
                red_team.kill_cup("C")
                red_team.kill_cup("D")
                red_team.kill_cup("E")
            elif "blue team" in command:
                blue_team.kill_cup(command[-1])
            else:
                print "Try Again"
        elif "rerack" in command:
            if "red team" in command:
                command = command[16:]
                #print command
                red_team.rerack(command)
            elif "blue team" in command:
                command = command[17:]
                blue_team.rerack(command)
            else:
                print "Try Again"
        elif "end_game" in command:
            in_game = False
            print "Game Over"

game()

#kill red team 



