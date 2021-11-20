1. After installing Postgres, you must log in as Postgres from the command line.
$ sudo -su postgres
$ psql

2. hange Postgres password via command
ALTER USER postgres PASSWORD '****************';

3. Create Database

CREATE DATABASE "rebalancer"
  ENCODING 'UTF8'
  LC_COLLATE = 'en_US.UTF-8'
  LC_CTYPE = 'en_US.UTF-8';

4. Switch to created database
\c rebalancer

5. Create table
CREATE TABLE assetBalanceLog (
	timestamp timestamp NOT NULL DEFAULT NOW(),
	balance FLOAT NOT NULL,
    amount FLOAT NOT NULL,
    name VARCHAR ( 50 )
);

