# Scrap_flight_info
 *Code to scrap flights info*
 
<br>
A big thank you for the tutorial:  https://dzone.com/articles/make-python-surf-the-web-for-you-and-send-best-fli 
<br>
The code below uses the logic as per tutorial
But is adjusted to reflect my own needs
 
<br> 

The code currently is set up to get data for return flights from New York to London 
departing the day after the programme is run and returning a week after the departure.

I run the program few times a day to build up the time series data about flight prices.

<br>
Before running the code, set the folder called 'flights_data' in your file directory for files to get saved there <br>

<br>
**Dependencies** 
<br>
Selenium
Chromedriver <br>
(for your machine windows, linux, mac). Can be downloaded in:
http://chromedriver.chromium.org/ <br>



<br>
**To run:** <br>

*python scrap_flights.py -n 4 -t 10800*

<br>
Where: <br>
n -> number of runs <br>
t -> sleep time between runs in seconds <br>
for example, the code above will scrap the prices every 3 hours for 4 times <br>

<br>
<br>

**Output**
![Capture](https://user-images.githubusercontent.com/31029142/60921084-b4ca5180-a267-11e9-9c49-0f49866d503c.PNG)
