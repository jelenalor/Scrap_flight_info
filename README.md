# Scrap_flight_info
 Code to scrap flights info
 
 
*A big thank you for tutorial: https://dzone.com/articles/make-python-surf-the-web-for-you-and-send-best-fli*
*The code below uses the logic as per tutorial*
*But is adjusted to reflect my own needs*
 
<br> 
<br> 

The code currently is set up to get data for return flights from New York to London 
departing the day after the programme is run and returning a week after the departure.

I run the program few times a day to build up the time series data about flight prices.


**To run:** <br>

*python scrap_flights.py -n 4 -t 10800*

<br>
Where: <br>
n -> number of runs <br>
t -> time between runs in seconds <br>
for example, the code above will scrap the prices every 3 hours for 4 times <br>

