# README

Multiple data sets from nyc, state, and aggregators of NY state and NYC covid data. A set of scripts to look at the data.

Open Source Python Library: https://github.com/xmunoz/sodapy

https://github.com/thecityny/covid-19-nyc-data
https://github.com/nychealth/coronavirus-data

## Initialize App

TODO: automate all of this.

1. `make up`
1. `make sh`
1. `python manage.py migrate`
1. `python manage.py runscript load_station_data`
1. `python manage.py runscript ace_data`

Useful commands:

1. `make web` Connect to the running web container
1. `make db` Connect to the running db container


## Environment Setup

~~~
docker pull debian:buster-slim
docker image ls
~~~

Add S3 and a frontend container

~~~
docker image prune
~~~

## How to migrate

1. `make sh`
1. `python manage.py makemigrations realtime_subway`
1. `python manage.py sqlmigrate realtime_subway 0003`
1. `python manage.py migrate`
1. `python manage.py showmigrations`

https://docs.djangoproject.com/en/3.2/topics/migrations/#squashing-migrations


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


## NYC Legislator

http://webapi.legistar.com/Home/Examples
https://council.nyc.gov/data/
https://github.com/NewYorkCityCouncil/

`API Key in LastPass`

1. Get all Events
    - http://webapi.legistar.com/Help/Api/GET-v1-Client-Events
1. Find your Event
1. Get all EventItems for that Event
    - http://webapi.legistar.com/Help/Api/GET-v1-Client-Events-EventId-EventItems_AgendaNote_MinutesNote_Attachments
1. Get the vote record for that EventItem 
    - http://webapi.legistar.com/Help/Api/GET-v1-Client-EventItems-EventItemId-Votes
1. Search for your council members name/id?


App Idea:

1. 20 latest votes page
1. Search page
1. Track record page
    - By vote how a specific council member voted
1. Legislation lookup page
    - Lookup a specific legislation and see the full vote

Notes:
- Store all votes the API has hit in data store to not constantly spam (votes should be static)
- Get new city council members once a week? month? year? 
- Django App with views to handle all of this.


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
http://mtadatamine.s3-website-us-east-1.amazonaws.com/#/landing
http://web.mta.info/developers/developer-data-terms.html#data
https://new.mta.info/coronavirus/ridership


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
https://github.com/jonthornton/MTAPI
https://medium.com/analytics-vidhya/the-hitchhikers-guide-to-gtfs-with-python-e9790090952a
https://transitfeeds.com/
https://github.com/CUTR-at-USF/awesome-transit/blob/master/README.md
