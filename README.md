# README

Multiple data sets from nyc, state, and aggregators of NY state and NYC covid data. A set of scripts to look at the data.

Open Source Python Library: https://github.com/xmunoz/sodapy

https://github.com/thecityny/covid-19-nyc-data
https://github.com/nychealth/coronavirus-data

## Initialize App

TODO: automate all of this.

1. `make up`
1. `make sh`
1. `python manage.py runscript load_station_data` to populate DB with subway data.
1. `docker exec -it ny_data_db_1 psql postgres -U postgres -w postgres` to inspect DB. 


## Environment Setup

~~~
docker pull debian:buster-slim
docker image ls
~~~

Add S3 and a frontend container

~~~
docker image prune
~~~


## Development Notes

#### Setting up Application
1. Create a working flask application (hello world)
2. Mount that application in a Dockerfile
3. Get docker-compose working with the dockerfile
4. Connect a mysql container to the flask app in compose.


### Used
[Wait for It](https://github.com/vishnubob/wait-for-it)


## MTA Info 

[Static File Page](http://web.mta.info/developers/developer-data-terms.html#data)

Download and Parse Stations.csv google-transit/ to map stop_id to an actual station name. Probably need a psql table to store this.


## coronavirus-data  

NYC Health Data set. Updated daily (on a 3 day lag) or updated weekly on Thursday


## NY State Data

https://dev.socrata.com/foundry/health.data.ny.gov/xdss-u53e

API Developer Portal: https://health.data.ny.gov/profile/edit/developer_settings

App Token: On the dashboard
Secret Token: On the dashboard

~~~sh
curl "https://health.data.ny.gov/resource/xdss-u53e.csv?%24limit=5000&%24%24app_token={}"
curl "https://health.data.ny.gov/resource/xdss-u53e.json?%24limit=50&%24%24app_token={}" | jq .
curl "https://health.data.ny.gov/resource/xdss-u53e.json?test_date=2020-11-11" | jq .
~~~

Works in browser (browser handles encoding for you)
~~~sh
https://health.data.ny.gov/resource/xdss-u53e.json?$query=select distinct county
~~~

With curl (P.S. Remember to escape the $ in the query params)
~~~sh
curl "https://health.data.ny.gov/resource/xdss-u53e.json?\$query=select%20distinct%20county" | jq .
curl "https://health.data.ny.gov/resource/xdss-u53e.json?\$select=distinct%20county" | jq .


curl "https://health.data.ny.gov/resource/xdss-u53e.json?\$where=county%20=%20%27Westchester%27" | jq .
# Haven't figured out full SQL text yet
curl "https://health.data.ny.gov/resource/xdss-u53e.json?\$query=SELECT * WHERE county = 'Westchester' ORDER BY test_date DESC" | jq .
curl "https://health.data.ny.gov/resource/xdss-u53e.json?\$query=SELECT%20*%20WHERE%20county%20%3D%20%27Westchester%27%20ORDER%20BY%20test_date%20DESC" | jq .
~~~

By zip ER visits
~~~sh
curl "https://data.cityofnewyork.us/resource/2nwg-uqyg.json" | jq .
curl "https://data.cityofnewyork.us/resource/2nwg-uqyg.json?\$query=SELECT * WHERE mod_zcta = '10025' ORDER BY date DESC" | jq .
~~~


## NYC Open Data

https://data.cityofnewyork.us/browse?category=Health&q=covid


## covid-19-nyc-data

THE CITY NY aggregation of multiple data sets. Most files are no longer updated.


## Other

List of other NY open data sets

~~~sh
curl "https://data.cityofnewyork.us/resource/uiay-nctu.json?open_date=2020-10-29" | jq .
~~~

## Resources:

https://medium.com/@_blahblahblah
https://github.com/blahblahblah-/goodservice
https://api.mta.info/#/landing
