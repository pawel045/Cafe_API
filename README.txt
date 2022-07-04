# Cafe_API

It is a full-featured REST API with a cafe database.

Documentation below:

API Cafe

GET:
Get all Cafes
http://127.0.0.1:5000/all

Get a random Cafe
http://127.0.0.1:5000/random

Get Cafes by location
http://127.0.0.1:5000/search?loc={location_name}
Query Params
e.g. loc=Warsaw


PATCH
Patch a price of coffee from database. You will need to provide id of the cafe to patch as a route.
http://127.0.0.1:5000/update-price/22?new_price={value}
Query Params
e.g. new_price=11 PLN

POST
Post New Cafe - adds a new cafe entry to the database.
http://127.0.0.1:5000/add/name={name}?map_url={map_url}...

Body
name                  Caffe Nero
map_url               https://www.google.com/maps/place/Kawiarnia+Kafka
img_url               https://b.zmtcdn.com/data/pictures/9/10903789/0990b9bf233eddcfdbc73c54261ba603.jpg
location              Warsaw
seats                 50
has_toilet            1
has_wifi              1
has_sockets           1
can_take_calls        1
coffee_price          10 PLN

DEL
Delete a Cafe by Id from database - You will need do provide the id of the cafe to delete 
as a route. You will alsko need to provide a valid API KEY for this operation allowed.
http://127.0.0.1:5000/report-closed/{cafe_id}?api_key={value}

Query Params
api_key             {value} (you can find it in the source code)
