#!/usr/bin/env python
import argparse
import time
from daemon import DaemonContext, pidfile

from bitkub_connection.apiConnection import BitKubConnection
from postgresql_connection import PostgresqlConnection
from config_parser_helper import configParserHelper

import logging

isDevMode = False

ThaiBahtSymbol = 'THB'

class WalletObserver(object):
    def __init__( self, bitKubConnection, sqlConnection, observerIntervalTimeSec):
        
        self.apiConnection = bitKubConnection
        self.sqlConnection = sqlConnection
        self.observerIntervalTimeSec =  observerIntervalTimeSec

    def run( self ):
        
        while True:
            
            #   get current wallet balance
            walletBalanceDict = self.apiConnection.getWalletBalance()

            #   filter out asset that have 0 value
            filteredWalletBalanceDict = { key : value for key, value in walletBalanceDict.items() if value > 0.0 }

            #   get current ticker
            tickerDict = self.apiConnection.getTicker()

            #   connect postgres
            self.sqlConnection.connect() 

            #   get db cursor
            #   TODO :: MOVE TO postgresql connection class
            curentCursor = self.sqlConnection.databaseConnection.cursor() 

            #   loop over wallet balance
            for assetName, assetBalance in filteredWalletBalanceDict.items():
                
                #   if thai bath asset amount is asset balance
                if assetName == ThaiBahtSymbol:
                    assetAmount = assetBalance
                
                #   otherwise compute amount
                else:
                    
                    #   get ticker
                    assetTickerDict = tickerDict.get( '{}_{}'.format( ThaiBahtSymbol, assetName ) )

                    #   continue if cannot find this asset in ticker 
                    if assetTickerDict == None:
                        continue
                    
                    #   git current price
                    assetPrice = assetTickerDict['last']

                    #   compute price
                    assetAmount = assetBalance * assetPrice
                
                #   insert to db
                insertCommand = "INSERT INTO assetBalanceLog(name,balance,amount) VALUES ('{}',{},{})".format( assetName,assetBalance,assetAmount )
                curentCursor.execute( insertCommand )

            #   clost connection it also commit 
            self.sqlConnection.close()

            #   sleep and wait to next round
            time.sleep( self.observerIntervalTimeSec )

if __name__ == '__main__':
    
    # Instantiate the parser
    parser = argparse.ArgumentParser(description='This is wallet observer')

    # Required positional argument
    parser.add_argument(    'configFilePath', type=str,
                            help='Json configuration file'  )


    args = parser.parse_args()

    observerConfigDict = configParserHelper( args.configFilePath, section='observerConfig' )

    #   get database connection
    databaseConnection = PostgresqlConnection( args.configFilePath )

    #   get api connection
    bitKubConnection = BitKubConnection( observerConfigDict['apikey'], observerConfigDict['apisecret'] )

    #   if dev mode change to 5 sec
    if isDevMode:
        intervalSec = 5

    #   otherwise follow from config
    else:
        intervalSec = int( observerConfigDict['intervalminute'] ) * 60

    #   construct observer
    walletObserver = WalletObserver( bitKubConnection, databaseConnection, intervalSec )

    with DaemonContext( pidfile=pidfile.TimeoutPIDLockFile( '/tmp/walletObserver.pid' ) ) as context:
        walletObserver.run()