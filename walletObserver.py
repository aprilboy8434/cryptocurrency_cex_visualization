#!/usr/bin/env python
from ctypes import DEFAULT_MODE
import os
import argparse
import time
import json
import daemon 
from decimal import Decimal, ROUND_DOWN

from bitkub_connection.apiConnection import BitKubConnection, CallServerError
from postgresql_connection import PostgresqlConnection
from config_parser_helper import configParserHelper

import logging

isDevMode = True

ThaiBahtSymbol = 'THB'

class Asset(object):

    def __init__( self, name, expectedPercent ):

        self.name = name


class WalletObserver(object):
    def __init__( self, bitKubConnection, sqlConnection, observerIntervalTimeSec):
        
        self.apiConnection = bitKubConnection
        self.sqlConnection = sqlConnection
        self.observerIntervalTimeSec =  observerIntervalTimeSec

        assetNameToAssetId = dict()

    def generateAsset( self, assetNameList ):
        ''' generate new asset to posgresql
        '''
        curentCursor = self.sqlConnection.databaseConnection.cursor() 

        curentCursor.execute( 'SELECT * FROM asset;' )

        assetTupleList = curentCursor.fetchall()

        assetNameToAssetId = { assetName: assetId for assetId, assetName in assetTupleList }

        for assetName in assetNameList:

            if assetName in assetNameToAssetId:
                continue

            insertCommand = "INSERT INTO asset(assetname) VALUES ('{}')".format( assetName )
            
            curentCursor.execute( insertCommand )

        curentCursor.execute( 'SELECT * FROM asset;' )

        assetTupleList = curentCursor.fetchall()

        assetNameToAssetId = { assetName: assetId for assetId, assetName in assetTupleList }

        curentCursor.close()

        curentCursor = self.sqlConnection.databaseConnection.commit()

        return assetNameToAssetId

    def run( self ):
        
        while True:

            walletBalanceDict = self.apiConnection.getWalletBalance()

            #   filter out asset that have 0 value
            filteredWalletBalanceDict = { key : value for key, value in walletBalanceDict.items() if value > 0.0 }

            #assetNameToAssetId = self.generateAsset(  list( filteredWalletBalanceDict ) )

            tickerDict = self.apiConnection.getTicker()

            self.sqlConnection.connect() 

            curentCursor = self.sqlConnection.databaseConnection.cursor() 

            for assetName, assetBalance in filteredWalletBalanceDict.items():
                
                if assetName == ThaiBahtSymbol:
                    
                    assetAmount = assetBalance
                    
                else:

                    assetTickerDict = tickerDict.get( '{}_{}'.format( ThaiBahtSymbol, assetName ) )

                    if assetTickerDict == None:
                        continue

                    assetPrice = assetTickerDict['last']

                    assetAmount = assetBalance * assetPrice
                
                insertCommand = "INSERT INTO assetBalanceLog(name,balance,amount) VALUES ('{}',{},{})".format( assetName,assetBalance,assetAmount )
            
                curentCursor.execute( insertCommand )

            self.sqlConnection.close()
            time.sleep( self.observerIntervalTimeSec )

if __name__ == '__main__':
    
    # Instantiate the parser
    parser = argparse.ArgumentParser(description='This is wallet observer')

    # Required positional argument
    parser.add_argument(    'configJsonFilePath', type=str,
                            help='Json configuration file'  )

    args = parser.parse_args()

    logging.basicConfig(format='%(asctime)s [%(levelname)s] : %(funcName)s : %(message)s', level = logging.INFO)

    observerConfigDict = configParserHelper( args.configJsonFilePath, section='observerConfig' )

    databaseConnection = PostgresqlConnection( args.configJsonFilePath )

    bitKubConnection = BitKubConnection( observerConfigDict['apikey'], observerConfigDict['apisecret'] )


    if isDevMode:
        intervalSec = 5
    else:
        intervalSec = int( observerConfigDict['intervalminute'] ) * 60

    walletObserver = WalletObserver( bitKubConnection, databaseConnection, intervalSec )
    
    walletObserver.run()
