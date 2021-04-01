set global sql_mode='STRICT_ALL_TABLES';
create database if not exists `ny_data`;
use `ny_data`;
grant all on `ny_data`.* to 'ny_data'@'%' identified by 'nyc^3!';
