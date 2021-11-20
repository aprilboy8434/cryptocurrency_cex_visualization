# exchange_coin_visualization
This is a simple one that uses Grafina to visualize cryptocurrency from the Bitkub exchange. This service will make a request to the Bitkub API from your wallet and save the response to Postgresql. Grafina will retrieve data from Postgresql and display the graph.
# Requirement package 
- Install grafana
sudo apt-get install -y adduser libfontconfig1
wget https://dl.grafana.com/oss/release/grafana_8.2.5_amd64.deb
sudo dpkg -i grafana_8.2.5_amd64.deb
REMARK :: Change current version from https://grafana.com/grafana/download?edition=oss

- Install package
sudo apt install postgresql
sudo apt install pip
sudo pip install psycopg2
sudo pip install python-daemon


#   how to start

1. Configure database by following the instructions in the file init database notes.txt.

2. cd to cryptocurrency_cex_visualization then git submodule
$ git submodule update --init --recursive

3. copy file observerConfig.ini to observerConfig{username}.ini

4. run app 
$ ./walletObserver.py observerConfig.ini
