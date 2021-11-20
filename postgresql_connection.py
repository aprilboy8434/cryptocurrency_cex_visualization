import os
import psycopg2
from config_parser_helper import configParserHelper

class PostgresqlConnection(object):
    
    
    def __init__( self, databaseConfigFilePath, ):

        self.databaseInfoDict = configParserHelper( configJsonFilePath = databaseConfigFilePath, section='postgresql' )

        self.databaseConnection = None

    def connect( self ):
        """ Connect to the PostgreSQL database server """
        
        assert self.databaseConnection is None, "Already connect..."
        try:

            # connect to the PostgreSQL server
            print('Connecting to the PostgreSQL database...')
            self.databaseConnection = psycopg2.connect(**self.databaseInfoDict)
            
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def close( self, isCommit = True ):
        
        #   if already closed return none
        if self.databaseConnection.closed:
            return None

        #   if is commit is true 
        if isCommit:
            #   commit 
            self.databaseConnection.commit()
        #   do close 
        self.databaseConnection.close()

        self.databaseConnection = None
