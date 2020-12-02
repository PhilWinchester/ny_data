set global sql_mode='STRICT_ALL_TABLES';
create database if not exists `nyc`;
use `nyc`;
grant all on `nyc`.* to 'nyc'@'%' identified by 'nyc^3!';
