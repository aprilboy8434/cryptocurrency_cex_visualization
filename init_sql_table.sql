CREATE USER rebalanceadmin WITH PASSWORD '******' CREATEDB;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO rebalanceadmin;

CREATE DATABASE "rebalancer"
  WITH OWNER "rebalanceadmin"
  ENCODING 'UTF8'
  LC_COLLATE = 'en_US.UTF-8'
  LC_CTYPE = 'en_US.UTF-8';

\c rebalancer

CREATE TABLE assetBalanceLog (
	timestamp timestamp NOT NULL DEFAULT NOW(),
	balance FLOAT NOT NULL,
    amount FLOAT NOT NULL,
    name VARCHAR ( 50 )
);

