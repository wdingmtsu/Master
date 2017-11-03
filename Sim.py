#!/usr/bin/env python3
#Author:  Ryan Florida
#Purpose: This program simulates our first M&M modeling project, without death
#         and without immigration.
from random import sample

#Some parameters.
NUM_OF_MM    = 63
START        = 8
ROW          = 21
COL          = 16

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#Class of MM's, this is a simple and unneccessary class, but it aids in
#readability and can be improved upon in order to aid in future generalization.
class MM(object):
    #Tells us if the M&M is infected or not (1 represents infected, 0 represents
    #not). Do not worry too much about the double underscores before and after
    #the variable name, this is just a conventional measure to let the users
    #know that this is private class data.
    __infected__ = 0

################################## Accessors ###################################
    #This method tells us if the current M&M is infected or not.
    def Infected(self):
        return self.__infected__

################################### Mutators ###################################
    #This method infects the current M&M.
    def Infect(self):
        self.__infected__ = 1


#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#This class represents our cup of M&M's
class Cup(object):
    #Here we are just making a list of M&M's, we subtract START from the initial
    #size here because we know there will be that many initial infecteds.
    __candy__ = [MM() for _ in range(NUM_OF_MM - START)]

    #This method represents us tossing the M&M's onto the grid and then removes
    #the infected M&M's.
    def TossCandy(self, grid):
        grid.CountCandy(self)
        self.RemoveInfected(grid)

################################## Accessors ###################################
    #This method just tells us how many susceptibles remain.
    def Size(self):
        return len(self.__candy__)

    #This method yields true when all of our M&M's are infected.
    def IsEmpty(self):
        return self.Size() == 0

################################### Mutators ###################################
    #This method removes the infecteds from the population. There is a very
    #different way to approach this method, but I saw a shortcut, so I took it;
    #my shortcut is the reason we are not actually referencing the MM class
    #objects themselves to test and see which are infected.
    def RemoveInfected(self, grid):
        self.__candy__ = self.__candy__[grid.NumOfInfected():]


#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#Class that creates a ROWxCOL grid
class Grid(object):
    #This is our grid
    __grid__            = [[0]*COL for _ in range(ROW)]
    #This is the number of infected present on the grid.
    __num_of_infected__ = 1
    #This is the toss number that we are on.
    __toss__            = 0
    #This is the number of newly infected M&M's on the grid.
    __newly_infected__  = START + 1
    #This is a table that will be used for a nice display at the end of all
    #tosses.
    __table__           = {}

    #Basic constructor. Here we are just picking START random locations on our
    #grid and assigning them numbers 1 through START.
    def __init__(self):
        initial_spots = sample(range(ROW*COL), START)
        for spot in initial_spots:
            row = spot//COL
            col = spot%COL
            self.__grid__[row][col] = self.__num_of_infected__
            self.__num_of_infected__ += 1
        self.Display()

################################## Accessors ###################################
    #As the name implies, this method just displays our grid.
    def Display(self):
        print("Grid after %d iteration(s) with %d infecteds"\
                %(self.__toss__, self.__num_of_infected__-1))
        self.__table__[self.__toss__] = self.__num_of_infected__ - 1
        for row in self.__grid__:
            for item in row:
                print('%-5d' %item, end = '')
            print()
        print()

    #This method just displays our final results.
    def Results(self):
        print("Table of Results:\nIteration        Number of Infecteds")
        for (iteration, infecteds) in self.__table__.items():
            print("%-23d %2d" %(iteration, infecteds))

    #This method returns the change in the number of infecteds between each
    #subsequent toss.
    def NumOfInfected(self):
        change = self.__num_of_infected__ - self.__newly_infected__
        self.__newly_infected__ = self.__num_of_infected__
        return change

################################### Mutators ###################################
    #This method will seem overwhelming upon first blush, but just realize that
    #all we are doing is picking a random spot on our grid, then we are
    #checking the spaces on the grid above, below, to the left, and to the
    #right of the square we are currently on. If the current square is
    #infected, then we just randomly move the M&M to the closest available
    #square. I realize the Boolean expression can probably be simplified, but
    #I have not taken the time to do that yet.
    def CountCandy(self, cup):
        self.__toss__ += 1
        positions = sample(range(ROW*COL), cup.Size())
        for position in positions:
            row = position//COL
            col = position%COL
            #Define some Boolean expressions.
            A = col > 0
            B = row > 0
            C = col < COL - 1
            D = row < ROW - 1
            #Testing environment of the current spot on the grid.
            if self.__grid__[row][col] == 0:
                if A and B and C and D:
                    c1 = self.__grid__[row-1][col] != 0
                    c2 = self.__grid__[row+1][col] != 0
                    c3 = self.__grid__[row][col-1] != 0
                    c4 = self.__grid__[row][col+1] != 0
                    if c1 or c2 or c3 or c4:
                        self.__grid__[row][col] = self.__num_of_infected__
                        self.__num_of_infected__ += 1
                elif not A:
                    if B and D:
                        c1 = self.__grid__[row-1][col] != 0
                        c2 = self.__grid__[row+1][col] != 0
                        c3 = self.__grid__[row][col+1] != 0
                        if c1 or c2 or c3:
                            self.__grid__[row][col] = self.__num_of_infected__
                            self.__num_of_infected__ += 1
                    elif not D:
                        c1 = self.__grid__[row-1][col] != 0
                        c2 = self.__grid__[row][col+1] != 0
                        if c1 or c2:
                            self.__grid__[row][col] = self.__num_of_infected__
                            self.__num_of_infected__ += 1
                elif not B:
                    if A and C:
                        c1 = self.__grid__[row+1][col] != 0
                        c2 = self.__grid__[row][col+1] != 0
                        c3 = self.__grid__[row][col-1] != 0
                        if c1 or c2 or c3:
                            self.__grid__[row][col] = self.__num_of_infected__
                            self.__num_of_infected__ += 1
                    elif not C:
                        c1 = self.__grid__[row+1][col] != 0
                        c2 = self.__grid__[row][col-1] != 0
                        if c1 or c2:
                            self.__grid__[row][col] = self.__num_of_infected__
                            self.__num_of_infected__ += 1
                elif not C:
                    if B and D:
                        c1 = self.__grid__[row-1][col] != 0
                        c2 = self.__grid__[row+1][col] != 0
                        c3 = self.__grid__[row][col-1] != 0
                        if c1 or c2 or c3:
                            self.__grid__[row][col] = self.__num_of_infected__
                            self.__num_of_infected__ += 1
                    elif not D:
                        c1 = self.__grid__[row-1][col] != 0
                        c2 = self.__grid__[row][col-1] != 0
                        if c1 or c2:
                            self.__grid__[row][col] = self.__num_of_infected__
                            self.__num_of_infected__ += 1
                elif A and C and (not D):
                    c1 = self.__grid__[row-1][col] != 0
                    c2 = self.__grid__[row][col-1] != 0
                    c3 = self.__grid__[row][col+1] != 0
                    if c1 or c2 or c3:
                        self.__grid__[row][col] = self.__num_of_infected__
                        self.__num_of_infected__ += 1
                elif not (A or B):
                        c1 = self.__grid__[row+1][col] != 0
                        c2 = self.__grid__[row][col+1] != 0
                        if c1 or c2:
                            self.__grid__[row][col] = self.__num_of_infected__
                            self.__num_of_infected__ += 1

            else:
                if A and B and C and D:
                    if self.__grid__[row-1][col] == 0:
                        self.__grid__[row-1][col] = self.__num_of_infected__
                        self.__num_of_infected__ += 1
                    elif self.__grid__[row][col-1] == 0:
                        self.__grid__[row][col-1] = self.__num_of_infected__
                        self.__num_of_infected__ += 1
                    elif self.__grid__[row+1][col] == 0:
                        self.__grid__[row+1][col] = self.__num_of_infected__
                        self.__num_of_infected__ += 1
                    elif self.__grid__[row][col+1] == 0:
                        self.__grid__[row][col+1] = self.__num_of_infected__
                        self.__num_of_infected__ += 1
                elif B and D and (not C):
                    if self.__grid__[row-1][col] == 0:
                        self.__grid__[row-1][col] = self.__num_of_infected__
                        self.__num_of_infected__ += 1
                    elif self.__grid__[row][col-1] == 0:
                        self.__grid__[row][col-1] = self.__num_of_infected__
                        self.__num_of_infected__ += 1
                    elif self.__grid__[row+1][col] == 0:
                        self.__grid__[row+1][col] = self.__num_of_infected__
                        self.__num_of_infected__ += 1
                elif B and D and (not A):
                    if self.__grid__[row-1][col] == 0:
                        self.__grid__[row-1][col] = self.__num_of_infected__
                        self.__num_of_infected__ += 1
                    elif self.__grid__[row+1][col] == 0:
                        self.__grid__[row+1][col] = self.__num_of_infected__
                        self.__num_of_infected__ += 1
                    elif self.__grid__[row][col+1] == 0:
                        self.__grid__[row][col+1] = self.__num_of_infected__
                        self.__num_of_infected__ += 1
                elif (not B) and A and C:
                    if self.__grid__[row][col-1] == 0:
                        self.__grid__[row][col-1] = self.__num_of_infected__
                        self.__num_of_infected__ += 1
                    elif self.__grid__[row+1][col] == 0:
                        self.__grid__[row+1][col] = self.__num_of_infected__
                        self.__num_of_infected__ += 1
                    elif self.__grid__[row][col+1] == 0:
                        self.__grid__[row][col+1] = self.__num_of_infected__
                        self.__num_of_infected__ += 1
                elif (not D) and A and C:
                    if self.__grid__[row-1][col] == 0:
                        self.__grid__[row-1][col] = self.__num_of_infected__
                        self.__num_of_infected__ += 1
                    elif self.__grid__[row][col-1] == 0:
                        self.__grid__[row][col-1] = self.__num_of_infected__
                        self.__num_of_infected__ += 1
                    elif self.__grid__[row][col+1] == 0:
                        self.__grid__[row][col+1] = self.__num_of_infected__
                        self.__num_of_infected__ += 1
                elif not (B or C):
                    if self.__grid__[row][col-1] == 0:
                        self.__grid__[row][col-1] = self.__num_of_infected__
                        self.__num_of_infected__ += 1
                    elif self.__grid__[row+1][col] == 0:
                        self.__grid__[row+1][col] = self.__num_of_infected__
                        self.__num_of_infected__ += 1
                elif not (B or D):
                    if self.__grid__[row-1][col] == 0:
                        self.__grid__[row-1][col] = self.__num_of_infected__
                        self.__num_of_infected__ += 1
                    elif self.__grid__[row][col+1] == 0:
                        self.__grid__[row][col+1] = self.__num_of_infected__
                        self.__num_of_infected__ += 1
                elif not (A or B):
                    if self.__grid__[row+1][col] == 0:
                        self.__grid__[row+1][col] = self.__num_of_infected__
                        self.__num_of_infected__ += 1
                    elif self.__grid__[row][col+1] == 0:
                        self.__grid__[row][col+1] = self.__num_of_infected__
                        self.__num_of_infected__ += 1
                elif not (C or D):
                    if self.__grid__[row-1][col] == 0:
                        self.__grid__[row-1][col] = self.__num_of_infected__
                        self.__num_of_infected__ += 1
                    elif self.__grid__[row][col-1] == 0:
                        self.__grid__[row][col-1] = self.__num_of_infected__
                        self.__num_of_infected__ += 1

        self.Display()

#*******************************************************************************
#0: Main
def main():
    #Create instance of Grid class
    grid = Grid()
    #Create instance of Cup class
    cup  = Cup()

    #While there are M&M's in the cup, toss them.
    while not cup.IsEmpty():
        cup.TossCandy(grid)

    #Display the results.
    grid.Results()


#Call Main.
main()
