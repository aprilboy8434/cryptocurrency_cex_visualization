**After installing Postgres, you must log in as Postgres from the command line.**
```
   $ sudo -su postgres
   $ psql
```
**hange Postgres password via command**
```
   ALTER USER postgres PASSWORD '****************';
```

**Create Database**
```
  CREATE DATABASE "rebalancer"
  ENCODING 'UTF8'
  LC_COLLATE = 'en_US.UTF-8'
  LC_CTYPE = 'en_US.UTF-8';
 ```

**Switch to created database**
```
   \c rebalancer
```

**Create table**
```
   CREATE TABLE assetBalanceLog (
   timestamp timestamp NOT NULL DEFAULT NOW(),
   balance FLOAT NOT NULL,
   amount FLOAT NOT NULL,
   name VARCHAR ( 50 ) );
```

