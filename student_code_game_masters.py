from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()
        
    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        rep = []
        for x in range(1, 4):
            peg_tuple = []
            #go through all facts
            bindings = self.kb.kb_ask(parse_input("fact: (on ?x peg" + str(x) + ")"))
            if bindings:
                for item in bindings:
                    #extrat each component
                    disk_str = item['?x']
                    disk_num = int(disk_str[-1])
                    peg_tuple.append(disk_num)
                    #add to tuple
            peg_tuple.sort()
            rep.append(tuple(peg_tuple))

        return tuple(rep)

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        # Student code goes here
        disk = str(movable_statement.terms[0])
        pegi = str(movable_statement.terms[1])
        pegt = str(movable_statement.terms[2])


        # before the move, if disk a was on top of diskb, diskb becomes top of pegi, 
        ontop_bindings = self.kb.kb_ask(parse_input("fact: (ontop " + disk + " ?y)"))
        if ontop_bindings:
            new_top_disk = ontop_bindings[0]
            self.kb.kb_retract(parse_input("fact: (ontop " + disk + " " + new_top_disk['?y'] + ")"))
            self.kb.kb_assert(parse_input("fact: (top " + new_top_disk['?y'] + " " + pegi + ")"))
        #if before the move, disk a was the only disk on pegi, then pegi is now empty
        else:
            self.kb.kb_assert(parse_input("fact: (empty " + pegi + ")"))
        
        top_bindings = self.kb.kb_ask(parse_input("fact: (top " + " ?x" + " " + pegt + ")"))
        if top_bindings:
            old_top_disk = top_bindings[0]
            self.kb.kb_retract(parse_input("fact: (top " + old_top_disk['?x'] + " " + pegt + ")"))
            self.kb.kb_assert(parse_input("fact: (ontop " + disk + " " + old_top_disk['?x'] + ")"))
        #else, if pegt was empty, then we remove this fact
        else:
            self.kb.kb_retract(parse_input("fact: (empty " + pegt + ")"))

         #basic ones 
        self.kb.kb_retract(parse_input("fact: (top " + disk + " " + pegi + ")"))
        self.kb.kb_assert(parse_input("fact: (top " + disk + " " + pegt + ")"))
        self.kb.kb_retract(parse_input("fact: (on " + disk + " " + pegi + ")"))
        self.kb.kb_assert(parse_input("fact: (on " + disk + " " + pegt + ")"))

       

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        # Student code goes here
        # fact: (x tile1 pos1)
        # fact: (y tile1 pos1)

        rep = []
        row1 = []
        row2 = []
        row3 = []

        #adding row 1
        #add pos1 pos1 
        bindings = self.kb.kb_ask(parse_input("fact: (at ?tile pos1 pos1)"))
        if bindings:
            tile_binding = bindings[0]
            tile_str = tile_binding['?tile']
            if tile_str == "empty":
                tile_num = -1
            else:
                tile_num = int(tile_str[-1])
            row1.append(tile_num)

        #add pos2 pos1
        bindings = self.kb.kb_ask(parse_input("fact: (at ?tile pos2 pos1)"))
        if bindings:
            tile_binding = bindings[0]
            tile_str = tile_binding['?tile']
            if tile_str == "empty":
                tile_num = -1
            else:
                tile_num = int(tile_str[-1])
            row1.append(tile_num)

        bindings = self.kb.kb_ask(parse_input("fact: (at ?tile pos3 pos1)"))
        if bindings:
            tile_binding = bindings[0]
            tile_str = tile_binding['?tile']
            if tile_str == "empty":
                tile_num = -1
            else:
                tile_num = int(tile_str[-1])
            row1.append(tile_num)

        # adding row 2
        #add pos1 pos2
        bindings = self.kb.kb_ask(parse_input("fact: (at ?tile pos1 pos2)"))
        if bindings:
            tile_binding = bindings[0]
            tile_str = tile_binding['?tile']
            if tile_str == "empty":
                tile_num = -1
            else:
                tile_num = int(tile_str[-1])
            row2.append(tile_num)

        bindings = self.kb.kb_ask(parse_input("fact: (at ?tile pos2 pos2)"))
        if bindings:
            tile_binding = bindings[0]
            tile_str = tile_binding['?tile']
            if tile_str == "empty":
                tile_num = -1
            else:
                tile_num = int(tile_str[-1])
            row2.append(tile_num)

        bindings = self.kb.kb_ask(parse_input("fact: (at ?tile pos3 pos2)"))
        if bindings:
            tile_binding = bindings[0]
            tile_str = tile_binding['?tile']
            if tile_str == "empty":
                tile_num = -1
            else:
                tile_num = int(tile_str[-1])
            row2.append(tile_num)

        # add row 3
        #add pos1 pos3 
        bindings = self.kb.kb_ask(parse_input("fact: (at ?tile pos1 pos3)"))
        if bindings:
            tile_binding = bindings[0]
            tile_str = tile_binding['?tile']
            if tile_str == "empty":
                tile_num = -1
            else:
                tile_num = int(tile_str[-1])
            row3.append(tile_num)

        bindings = self.kb.kb_ask(parse_input("fact: (at ?tile pos2 pos3)"))
        if bindings:
            tile_binding = bindings[0]
            tile_str = tile_binding['?tile']
            if tile_str == "empty":
                tile_num = -1
            else:
                tile_num = int(tile_str[-1])
            row3.append(tile_num)

        bindings = self.kb.kb_ask(parse_input("fact: (at ?tile pos3 pos3)"))
        if bindings:
            tile_binding = bindings[0]
            tile_str = tile_binding['?tile']
            if tile_str == "empty":
                tile_num = -1
            else:
                tile_num = int(tile_str[-1])
            row3.append(tile_num)

        rep.append(tuple(row1))
        rep.append(tuple(row2))
        rep.append(tuple(row3))

        return tuple(rep)

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        tile =str(movable_statement.terms[0])
        xi = str(movable_statement.terms[1])
        yi = str(movable_statement.terms[2])
        xt = str(movable_statement.terms[3])
        yt = str(movable_statement.terms[4])
      

        self.kb.kb_retract(parse_input("fact: (at " + tile + " " + xi + " " + yi + ")"))
        self.kb.kb_retract(parse_input("fact: (at  empty " + xt + " " + yt + ")"))

        self.kb.kb_assert(parse_input("fact: (at " + tile + " " + xt + " " + yt + ")"))
        self.kb.kb_assert(parse_input("fact: (at  empty " + xi + " " + yi + ")"))



    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
