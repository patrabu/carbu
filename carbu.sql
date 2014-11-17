--
--    carbu.sql
--    ~~~~~~~~~~~
--    
--    This file contains the description of the tables for the CARBU database.
--    
--    :copyright: (c) 2014 by Patrick Rabu.
--    :license: GPL-3, see LICENSE for more details.    
--

-- Table USERS : users.
drop table if exists users;
create table users (
  id integer not null primary key,
  username text,
  password_hash text
);

-- Table CARS : cars.
drop table if exists cars;
create table cars (
    id integer not null primary key,
    name text,
    description text
);

-- Table REFILLS : refills.
drop table if exists refills;
create table refills (
    id integer not null primary key,
    datetime timestamp,
    mileage integer,
    quantity real,
    price real,
    car_id integer
);

