# -*- coding: utf-8 -*-
"""Module importance
Object about the management of the data about the project and importance
"""

from .row_importance import RowImportance


class GroupImportance:
    
    def __init__(self):
        pass

    def rows(self, reader):
        """
        @return the importance data of the Activities
        """
        result = []
        for row in reader:
            result.append ( RowImportance(row) )
        return result


