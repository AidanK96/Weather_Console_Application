# -*- coding: utf-8 -*-
import json
import urllib.request
"""
Function for creating the menu, called within menuChoice
"""
def menuText():
    
    print("[Welcome to the weather app]")
    print("Please press the corresponding key for the function you would like to use")
    print("1: The temperature in Bath at 10am on Wednesday \n2: Does the pressure in Edinburgh fall below 1000(millibars) on Friday\n3: Cardiff median temperature for the week")
    print("4: City with the highest recorded wind speed this week\n5: Will it snow in any cities\n6: Median temperature of all cities combined\n\nPress q to exit")

"""
Function for calling menu, takes user input and executes function depending on choice, Throws error and goes back to start if invalid option.
"""
def menuChoice():
    
    menuText()
    userInput = input()
    
    if userInput == '1':
        option1()
    elif userInput == '2':
        option2()
    elif userInput == '3':  
        option3()
    elif userInput == '4':
        option4()
    elif userInput == '5':
        option5()
    elif userInput == '6':
        option6()
    elif userInput.lower() == 'q':
        exit
    else:
        print("Incorrect formatting or entry")
        menuChoice()
"""
Function for saving the output file,takes location and filename from user.
"""        
def save_file(output):
        print("Please enter filepath for the output file")
        path = input()
        print("Please enter the file name for the output file")
        file_name = input()
        f = open(f'{path}\{file_name}', 'w')
        f.write(output)
        f.close()
"""
Function for checking the temperature in Bath at a specific date and time within 1 hour periods.
Takes user inputted URL, date and time. Uses urllib to create the rerquest from the API, creates json object within json_data after reading and decoding the url.
Sets temperature using json_data at the date and time, displays 'temperature'. Provides user file explorer popup to save file to desired location.
"""
def option1():
    try:
        print("Please provide api URL for weather in Bath e.g. http://weather-api.eba-jgjmjs6p.eu-west-2.elasticbeanstalk.com/api/weather/1/bath/")
        api_url = input()
        print("Enter date e.g. wednesday, monday, friday")
        date = input().lower()
        print("Enter time e.g. 1 for 1am, 13 for 1pm")
        time= int(input())
        with urllib.request.urlopen(api_url) as url :
            json_data = json.loads(url.read().decode())
            temperature = (json_data[date][time]['temperature'])
            #Creates JSON object for output, puts the output temperature to that JSON object. 
            json_output = {"Temperature": temperature}
            output = json.dumps(json_output)
            print(output)
            save_file(output)
            menuChoice()
    except Exception:
        print("Error detected, please ensure formatting is correct")
        menuChoice()
"""
Function for checking if the pressure(millibars) will fall below 1000 in edinburgh on a specific day. 
Uses same function to add API URL create json object as previous method.
Goes through each line in json_data with the specific date, checks if pressure is less than 1000.
"""
def option2():
    try:
        print("Please provide api URL for weather in Edinburgh e.g. http://weather-api.eba-jgjmjs6p.eu-west-2.elasticbeanstalk.com/api/weather/1/edinburgh/")
        api_url = input()
        print("Enter date e.g. wednesday, monday, friday")
        date = input().lower()
        #Opens the provided api url using the urllib library then uses the JSON.loads function to read information from URL and decode.
        with urllib.request.urlopen(api_url) as url :
            json_data = json.loads(url.read().decode())
            for line in json_data[date]:
                if line['pressure'] <1000:
                    answer = True
                else: 
                    answer = False
            #After pressure has been checked for the specific day create JSON object with answer(true/false), prints output and save_file function called.
            json_output = {"Pressure": answer}
            output = json.dumps(json_output)
            print(output)
            save_file(output)
            menuChoice()
    except Exception:
        print("Error detected, please ensure formatting is correct")
        menuChoice()
"""
Function for checking the median temperature in Cardiff for the week. Takes the URL for the weather in the city of Cardiff.
Days list used to iterate within for loop. Function loops through each hour of each day, adds temperature to totaltemp.

"""               
def option3():
    try:
        print("Please provide api URL for weather in Cardiff e.g. http://weather-api.eba-jgjmjs6p.eu-west-2.elasticbeanstalk.com/api/weather/1/cardiff/")
        api_url = input()
        total_temp=0
        days = ['monday','tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        with urllib.request.urlopen(api_url) as url :
            json_data = json.loads(url.read().decode())    
            #Counts through each day in the week (from days list). Adds temp to total temp for each hour of each day.
            for day in days:      
                x=0               
                while x < 24:     
                    temperature = (json_data[day][x]['temperature'])                
                    total_temp+=int(temperature)
                    x+=1
        #After total temp has been populated, do maths and create JSON object for output. Saves JSON object. Returns to menu.
        result = int(total_temp/168)
        json_output = {"Temperature": result}
        output = json.dumps(json_output)
        print(output)
        save_file(output)
        menuChoice()
    except Exception:
        print("Error detected, please ensure formatting is correct")
        menuChoice()
"""
Function for checking the maximum windspeed recorded from the cities provided.  Takes the cities API, appends the cities to a list and then loops through them. 
"""
def option4():
    try:
        print("Please provide api URL for the cities e.g. http://weather-api.eba-jgjmjs6p.eu-west-2.elasticbeanstalk.com/api/cities/")
        city_url = input()
        print("Please provide api URL for the weather including your unique number e.g. http://weather-api.eba-jgjmjs6p.eu-west-2.elasticbeanstalk.com/api/weather/1/")
        weather_url = input()
        with urllib.request.urlopen(city_url) as url :
            json_data_cities = json.loads(url.read().decode())
            cities = [json_data_cities['cities']]
            city_names = []
            days = ['monday','tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
            i=0
            current_max = 0
            max_windspeed = 0
            #While loop to append all cities from API to cities_names
            while i < len(cities[0]):
                city_names.append(cities[0][i])
                i+=1
            #For loop, starts from 0 until the legnth of the city_names list. 
            for z in range (0,len(city_names)):           
                for city in cities:
                    weather_api = f'{weather_url}{city_names[z]}/'
                    with urllib.request.urlopen(weather_api) as url:
                        json_data = json.loads(url.read().decode())
                        for day in days:
                            x=0
                            while x < 24:     
                                wind_speed = (json_data[day][x]['wind_speed']) 
                                if wind_speed >= current_max:
                                    max_windspeed = wind_speed
                                    current_max = max_windspeed
                                    current_max_city = city_names[z]
                                    print(int(current_max),current_max_city)
                                x+=1
        json_output = {"Wind speed": current_max, "City" : current_max_city}
        output = json.dumps(json_output)
        save_file(output)
        menuChoice()
        print(json_output)
        menuChoice()                        
    except Exception:
        print("Error detected, please ensure formatting is correct")
        menuChoice()
"""
Function for checking if it can snow in any cities during the week provided by the API. Outputs a bool value after looping through cities and days.
"""
def option5():
    try:
        print("Please provide api URL for the cities e.g. http://weather-api.eba-jgjmjs6p.eu-west-2.elasticbeanstalk.com/api/cities/")
        city_url = input()
        print("Please provide api URL for the weather including your unique number e.g. http://weather-api.eba-jgjmjs6p.eu-west-2.elasticbeanstalk.com/api/weather/1/")
        weather_url = input()
        with urllib.request.urlopen(city_url) as url :
            json_data_cities = json.loads(url.read().decode())
            cities = [json_data_cities['cities']]
            city_names = []
            days = ['monday','tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
            i=0
            while i < len(cities[0]):
                city_names.append(cities[0][i])
                i+=1
            #ounts through the cities within the cities_names list starting from 0
            for z in range (0,len(city_names)):        
                #For loop for each city in cities, used to checl the temperature and precipitation for each hour to check bool value.
                for city in cities:
                    weather_api = f'{weather_url}{city_names[z]}/'
                    with urllib.request.urlopen(weather_api) as url :
                        json_data = json.loads(url.read().decode())
                        for day in days:
                            x=0
                            while x < 24:     
                                temperature = (json_data[day][x]['temperature']) 
                                precipitation = (json_data[day][x]['precipitation']) 
                                if int(temperature) < 2 and int(precipitation) > 0:
                                    snow = True   
                                    print(snow, city_names[z])
                                    json_output = {"Snow": snow}
                                    output = json.dumps(json_output)
                                    save_file(output)
                                    return menuChoice() 
                                elif int(temperature) > 2 and int(precipitation) >= 0:
                                    snow = False
                                x+=1      
        #If there is no snow save false value, return to menu.
        json_output = {"Snow": snow}
        output = json.dumps(json_output)
        save_file(output)
        print(snow)
        menuChoice()
    except Exception:
        print("Error detected, please ensure formatting is correct")
        menuChoice()
"""
Function for checking the median temperature of all cities combined for the week. A mix of option3 and option 5/6.
"""
def option6():
    try:
        print("Please provide api URL for the cities e.g. http://weather-api.eba-jgjmjs6p.eu-west-2.elasticbeanstalk.com/api/cities/")
        city_url = input()
        print("Please provide api URL for the weather including your unique number e.g. http://weather-api.eba-jgjmjs6p.eu-west-2.elasticbeanstalk.com/api/weather/1/")
        weather_url = input()
        with urllib.request.urlopen(city_url) as url :
            json_data_cities = json.loads(url.read().decode())
            cities = [json_data_cities['cities']]
            city_names = []
            days = ['monday','tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
            i=0
            total_temp=0
            #Same method to check through cities as function option5, instead checks for temperature.
            while i < len(cities[0]):
                city_names.append(cities[0][i])
                i+=1
            for z in range (0,len(city_names)):           
                for city in cities:
                    weather_api = f'{weather_url}{city_names[z]}/'
                    with urllib.request.urlopen(weather_api) as url :
                        json_data = json.loads(url.read().decode())
                        #Counts through each hour of each day, adding the temp for each hour to the total
                        for day in days:
                            x=0
                            while x < 24:    
                                temperature = (json_data[day][x]['temperature'])
                                total_temp+=int(temperature)
                                x+=1     
        #After total temp function has concoluded do math, convert to json object and save file
        result = float(total_temp/168/len(city_names))
        json_output = {"Temperature": result}
        output = json.dumps(json_output)
        print(output)
        save_file(output)
        menuChoice()
    except Exception:
        print("Error detected, please ensure formatting is correct")
        menuChoice()
"""

"""
menuChoice() #Startup menuchoice