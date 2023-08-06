# -*- coding: utf-8 -*-
"""Module priority
Object about the management of the data about the project and priority
"""
from .running import Running


class Priority:
    def __init__(self, newTimeActivity, newImportance):
        self.timeActivity = newTimeActivity
        self.importance = newImportance

    def activity(self):
        """
        @return the name of the Activity
        """
        return self.importance.activity()
        
    def points(self):
        """
        @return the points of the Activity
        """
        return int(self.importance.importance()) * int(self.timeActivity.days())
             
    def __str__(self):
        return "Priority:{0}".format(self.name() ) 
    
    def __repr__(self):
        return "Priority[{0}]-[{1}]".format(self.name() , str (  self.importance.importance() ) )


"""
TODO rewrite test
class RewriteTestPriority(unittest.TestCase):

    def test_points(self):
        priority = Priority( TimeActivity ( date ), importance) 
        result = priority.points()
        expected = 10
        self.assertEqual(result, expected)
"""
