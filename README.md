# exchange_coin_visualization
This is a simple one that uses Grafina to visualize coins from the Bitkub exchange.
This service will make a request to the Bitkub API from your wallet and save the response to Postgresql. Grafina will retrieve data from Postgresql and display the graph.

# Requirement package 
- Install grafana
https://grafana.com/grafana/download

- Install package
sudo apt install postgresql
sudo pip install psycopg2
sudo pip install python-daemon


#   how to start

setup database with file ini_sql_table.sql

git submodule --init --recursive

copy file observerConfig.ini to observerConfig{username}.ini


./walletObserver.py observerConfig.ini
