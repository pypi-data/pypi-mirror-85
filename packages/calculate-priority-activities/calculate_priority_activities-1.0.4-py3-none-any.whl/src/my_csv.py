# -*- coding: utf-8 -*-
"""Module priority
Object about the management of the data about the project and priority
"""

class CSV:

    def __init__(self, newPriority):
        self.priority = newPriority

    def activity(self):
        return self.priority.activity()
        
    def points(self):
        return self.priority.points()

    def __str__(self):
        return "CSV:{0}".format(self.name() ) 
    
    def __repr__(self):
        return "CSV[{0}]-[{1}]".format(self.name() ,  self.points() ) 


