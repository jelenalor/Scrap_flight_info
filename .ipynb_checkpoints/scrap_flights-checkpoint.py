
#
# Author - JLor
#

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from optparse import OptionParser

import numpy as np
import pandas as pd
import time
import datetime
from datetime import timedelta

# REFERENCE

#
# A big thank you for tutorial: https://dzone.com/articles/make-python-surf-the-web-for-you-and-send-best-fli
# The code below uses the logic as per tutorial
# Bus is adjusted to reflect my own needs
#

# Command Line Parser

parser = OptionParser()
parser.add_option("-n", "--numRuns", dest="num",
                  help="number of runs")
parser.add_option("-t", "--timeSleep", dest="time",
                  help="time to sleep between runs (in seconds)")

(options, args) = parser.parse_args()


# SUPPORT FUNCTIONS

#Setting ticket types paths
return_ticket = "//label[@id='flight-type-roundtrip-label-hp-flight']"
one_way_ticket = "//label[@id='flight-type-one-way-label-hp-flight']"
multi_ticket = "//label[@id='flight-type-multi-dest-label-hp-flight']"

def ticket_chooser(ticket):
    try:
        ticket_type = browser.find_element_by_xpath(ticket)
        ticket_type.click()
    except Exception as e:
        pass
    
def nonstop():
    advanced_option = browser.find_element_by_xpath("//a[@id='flight-advanced-options-hp-flight']")
    advanced_option.click()
    time.sleep(1)
    flight_type = browser.find_element_by_xpath("//label[@id='advanced-flight-nonstop-label-hp-flight']")
    flight_type.click() 

def dep_country_chooser(dep_country):
    fly_from = browser.find_element_by_xpath("//input[@id='flight-origin-hp-flight']")
    time.sleep(1)
    fly_from.clear()
    time.sleep(1.5)
    fly_from.send_keys('  ' + dep_country)
    time.sleep(2)
    first_item = fly_from.find_element_by_xpath("//a[@id='aria-option-0']")
    time.sleep(1.5)
    first_item.click()
    
def arrival_country_chooser(arrival_country):
    fly_to = browser.find_element_by_xpath("//input[@id='flight-destination-hp-flight']")
    time.sleep(1)
    fly_to.clear()
    time.sleep(1.5)
    fly_to.send_keys('  ' + arrival_country)
    time.sleep(2)
    first_item = browser.find_element_by_xpath("//a[@id='aria-option-0']")
    time.sleep(1.5)
    first_item.click()
    
def dep_date_chooser(month, day, year):
    dep_date_button = browser.find_element_by_xpath("//input[@id='flight-departing-hp-flight']")
    dep_date_button.clear()
    dep_date_button.send_keys(month + '/' + day + '/' + year)
    
def return_date_chooser(month, day, year):
    return_date_button = browser.find_element_by_xpath("//input[@id='flight-returning-hp-flight']")
    for i in range(11):
        return_date_button.send_keys(Keys.BACKSPACE)
    return_date_button.send_keys(month + '/' + day + '/' + year)
    
def search():
    search = browser.find_element_by_xpath("//button[@class='btn-primary btn-action gcw-submit']")
    search.click()
    time.sleep(15)
    print('Web results are ready!')
    
    
def compile_data():
    now = datetime.datetime.now()
    current_date = (str(now.year) + '-' + str(now.month) + '-' + str(now.day))
    current_time = (str(now.hour) + ':' + str(now.minute))
    
    global df
    global dictionary
    dictionary = {"current_date":[], "current_time":[],"departure_time": [], "arrival_time":[], "airline":[], "duration":[], "stops":[], \
                  "price":[], "dep_airport":[], "arr_airport":[], "operated_by":[], "other": []}

    
    #departure times
    dep_times = browser.find_elements_by_xpath("//span[@data-test-id='departure-time']")
    dictionary["departure_time"] = [value.text for value in dep_times]
    #arrival times
    arr_times = browser.find_elements_by_xpath("//span[@data-test-id='arrival-time']")
    dictionary["arrival_time"] = [value.text for value in arr_times]
    #airline name
    airlines = browser.find_elements_by_xpath("//span[@data-test-id='airline-name']")
    dictionary["airline"] = [value.text for value in airlines]

    #durations
    durations = browser.find_elements_by_xpath("//span[@data-test-id='duration']")
    dictionary["duration"] = [value.text for value in durations]
    
    #stops
    stops = browser.find_elements_by_xpath("//span[@class='number-stops']")
    dictionary["stops"] = [value.text for value in stops]
    
    #prices
    prices = browser.find_elements_by_xpath("//span[@data-test-id='listing-price-dollars']")
    dictionary["price"] = [value.text for value in prices]
    
    # Other details
    print("Opening flight details tabs")
    details = browser.find_elements_by_xpath("//a[@data-test-id='flight-details-link']")  
    # Open all details tabs, ensure there is enough sleep time
    for i in range(len(details)-1):
        details[i].click()
        if i != 30 or i != 40:
            time.sleep(2)
        else:
            time.sleep(10)  
            
    print("Details are open.. Collecting data")
    for i in range(len(details)-1): 
        dictionary["dep_airport"].append(browser.find_elements_by_xpath("//span[@data-test-id='details-departure-localName']")[i].text)
        dictionary["arr_airport"].append(browser.find_elements_by_xpath("//span[@data-test-id='details-arrival-localName']")[i].text)
        dictionary["operated_by"].append(browser.find_elements_by_xpath("//li[@data-test-id='details-airline-data']")[i].text)
        dictionary["other"].append(browser.find_elements_by_xpath("//li[@class='details-utility-item-value segment-info-details-item aircraft']")[i].text)
        dictionary["current_date"].append(current_date)
        dictionary["current_time"].append(current_time)
        time.sleep(1.5)
    
    print("Details collected... Updating for missing pricing")
    # Take first 45 items only -> the rest found to be expensive or business class
    for i in dictionary.keys():
        dictionary[i] = dictionary[i][:45]
    
    df = pd.DataFrame(dictionary)
    print('CSV file Created!')
    
now = datetime.datetime.now()
current_date = (str(now.year) + '-' + str(now.month) + '-' + str(now.day))
current_time = (str(now.hour) + ':' + str(now.minute))
start_date = now + timedelta(weeks = 1)
return_date = now + timedelta(weeks = 2)

dep = "New York"
arr = "London"
date = "".join(current_date.split("-"))
runs = int(options.num)
sleep_time = int(options.time)

if __name__ == '__main__': 
    for i in range(runs):   
        try:
            print("Scrapping began ...")
            browser = webdriver.Chrome(executable_path=r"C:\Users\kabachok\Documents\GitHUB\flights_data\chromedriver")
            link = 'https://www.expedia.com/'
            browser.get(link)
            time.sleep(5)
            #choose flights only
            flights_only = browser.find_element_by_xpath("//button[@id='tab-flight-tab-hp']")
            flights_only.click()
            nonstop()
            ticket_chooser(return_ticket)
            dep_country_chooser(dep)
            arrival_country_chooser(arr)
            dep_date_chooser(start_date.isoformat().split("-")[1], start_date.isoformat().split("-")[2][:2], start_date.isoformat().split("-")[0])
            return_date_chooser(return_date.isoformat().split("-")[1], return_date.isoformat().split("-")[2][:2], return_date.isoformat().split("-")[0])
            search()
            compile_data()
            df.to_csv('flights_data\\%s%s_flights_%s_%s.csv' %("".join(dep.split()), "".join(arr.split()), date, ".".join(current_time.split(":"))), \
                      index = False)

            print("CSV file saved - %s" %datetime.datetime.now())
            browser.quit()
            if i < (runs-1):
                print("Waiting for the next run...")
                time.sleep(sleep_time)
            else:
                print("Complete for today!")

        except Exception as e:
            print("Error occured", e)
            browser.quit()





