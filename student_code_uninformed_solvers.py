
from solver import *

class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here

        if self.currentState.state == self.victoryCondition:
            return True

        #find all possible moves
        all_movables = self.gm.getMovables()

        #if there are things in that list 
        if all_movables:
            for move in all_movables:
                self.gm.makeMove(move)#make da move 
                new_state = GameState(self.gm.getGameState(), self.currentState.depth + 1, move)  #set child state 
                self.currentState.children.append(new_state) # add the child state to the current state's child list
                new_state.parent = self.currentState  #the parent of new state is the current state
                self.gm.reverseMove(move)  

            for child in self.currentState.children: # look at the children of current state
                if child not in self.visited: # if not visited, set to visited 
                    self.visited[child] = True
                    self.gm.makeMove(child.requiredMovable)
                    self.currentState = child

                    break

        else: #if there are nothing in move list, go back to parent 
            self.gm.reverseMove(self.currentState.requiredMovable)

                

class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)
    
        


    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        
        if self.currentState.state == self.victoryCondition:  # move found, check if won
            return True
        
        all_movables = self.gm.getMovables()  # returns a list of movable Statements
        
        if all_movables:
            for move in all_movables: # now you have all the child state added to your child list, and all the new states have the current state added as parent 
                self.gm.makeMove(move) 
                new_state = GameState(self.gm.getGameState(), self.currentState.depth+1, move)
                self.currentState.children.append(new_state) 
                new_state.parent = self.currentState 
                self.gm.reverseMove(move)  
            

            for child in self.currentState.children: # look at the children of current state
                if child not in self.visited: # if not visited, set to visited 
                    self.visited[child] = True
                    self.gm.makeMove(child.requiredMovable)
                    self.currentState = child

                    break
                
        else: 
            while self.currentState.parent is not None and len(self.currentState.parent.children)==self.currentState.parent.nextChildToVisit:
                self.gm.reverseMove(self.currentState.requiredMovable)
                self.currentState = self.currentState.parent

            if self.currentState.parent is not None and len(self.currentState.parent.children)>self.currentState.parent.nextChildToVisit: 
                #if there are siblings, move back to parent and make sibling moves
                self.gm.reverseMove(self.currentState.requiredMovable)
                self.gm.makeMove(self.currentState.children[self.currentState.nextChildToVisit].requiredMovable)
                self.currentState = self.currentState.parent.children[self.currentState.parent.nextChildToVisit]
                



        
                
                

            

          
            
        

                



        
        
