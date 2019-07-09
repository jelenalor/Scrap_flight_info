# Scrap_flight_info
 Code to scrap flights info
 
 
My code to scrap flight prices and details
 
Currently set up to get data for return flights from flights from New York to London 
departing the day after the programme is run and returning a week after departure.

 
I run the program few times a day to build up the time series data about flight prices

To run:

python scrap_flights.py -n 4 -t 10800

n -> number of runs
t -> time between runs in seconds
for example, the code above will scrap the prices every 3 hours for 4 times

