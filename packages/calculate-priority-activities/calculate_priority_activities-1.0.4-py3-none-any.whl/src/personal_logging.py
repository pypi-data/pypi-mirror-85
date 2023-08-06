# -*- coding: utf-8 -*-
"""Module personalLogging
Personal wrapping per logging
"""
import logging
import logging.config
import os

class PersonalLogging:

    def __init__(self):
        """
        It's not polite, but in the constructor I read the file
        TODO i read the file out the constructor and I will pass the result
        from https://stackoverflow.com/questions/53222413/python-configparser-raise-keyerror-key?rq=1
        TODO create decorator with different operation of the logger
        """
        #path = "/".join( ( os.path.abspath( __file__ ).replace( "\\", "/" ) ).split( "/" )[:-1])
        #logging.config.fileConfig( os.path.join ( path, "..\\resources\\config-log.ini" ), disable_existing_loggers=False ) # working in local
        #logging.config.fileConfig ( "config-log.ini", disable_existing_loggers=False) # working in local
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        # create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        #fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        # add the handlers to the logger
        self.logger.addHandler(ch)
        # TODO decorator it doesnt create file handler which logs even debug messages
        # fh = logging.FileHandler('spam.log')
        # fh.setLevel(logging.DEBUG)
        # create console handler with a higher log level
        # fh.setFormatter(formatter)
        # logger.addHandler(fh)


    def info(self, nameclass, method, msg):
        if msg is None:
            return self.logger.info( "'{0}'.'{1}': none".format (nameclass, method) )
        else:
            return self.logger.info( "'{0}'.'{1}': '{2}'".format( nameclass, method, msg))

    def warning(self, nameclass, method, msg):
        if msg is None:
            return self.logger.warning( "'{0}'.'{1}': none".format (nameclass, method) )
        else:
            return self.logger.warning( "'{0}'.'{1}': '{2}'".format( nameclass, method, msg))

    def debug(self, nameclass, method, msg): 
        if msg is None:
            return self.logger.debug ( "'{0}'.'{1}': none".format (nameclass, method) )
        else:
            return self.logger.debug ( "'{0}'.'{1}': '{2}'".format( nameclass, method, msg))


        
        
