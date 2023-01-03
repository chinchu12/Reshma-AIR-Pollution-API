# make a HTTP request to  a  web page using Python
import requests
from pprint import pprint
#import DateTime to convert Unix time to DateTime format
import datetime
import time
from matplotlib import pyplot as plt
#store the  API KEY  to the base  url  from the Open Weather Website=(8d9b93dcdfeb252a161af9227264d88c)
#retrive input from relevant city name from user, based on city name display LATITUDE  nad LONGITUDE

def get_avg_aqi_for_date(datex,data):
    aqi_sum = 0
    count = 0
    for x in data["list"]:
        if datetime.datetime.fromtimestamp(int(x['dt'])).strftime('%Y-%m-%d') == datex:
            count += 1
            aqi_sum = aqi_sum + int(x['main']['aqi'])
    avg_aqi = aqi_sum/count
    return avg_aqi

def get_aqi_data():
    city = input('Enter your city : ')
    # city = "london"
    url1 = 'http://api.openweathermap.org/data/2.5/weather?q={}&APPID=8d9b93dcdfeb252a161af9227264d88c'.format(city)
    try:
        res = requests.get(url1)
        data = res.json()
        latitude= data['coord']['lat']
        longitude = data['coord']['lon']
        print('Latitude : {}'.format(latitude))
        print('longitude :{}'.format(longitude))
        startdate = input("Enter start date(DD/MM/YYY):")
        enddate = input("Enter end date(DD/MM/YYYY):")
        #Input the relevant STARTDATE and ENDDATE to find the pollution 
#Useing DateTime function to convert Unix time to DateTime format
        # startdate = "25/11/2022"
        # enddate = "26/12/2022"
        startdate_split = startdate.split("/")
        enddate_split = enddate.split("/")
        startDateTime = datetime.datetime(int(startdate_split[2]),int(startdate_split[1]),int(startdate_split[0]),0,0)
        endDateTime = datetime.datetime(int(enddate_split[2]),int(enddate_split[1]),int(enddate_split[0]),23,59)
        if startDateTime < endDateTime:    
            startdate_utc = time.mktime(startDateTime.timetuple())
            enddate_utc = time.mktime(endDateTime.timetuple())
            url2 = f'http://api.openweathermap.org/data/2.5/air_pollution/history?lat={int(latitude)}&lon={int(longitude)}&start={int(startdate_utc)}&end={int(enddate_utc)}&appid=8d9b93dcdfeb252a161af9227264d88c&units=metric'
            res = requests.get(url2)
            data = res.json()
            return startdate,enddate,data
        else:
            print("Please provide start date lesser than the end date")
    except Exception as e:
        print("Exception during getting data from api", e)

def get_graph_data(data):
    all_dates = []
    graph_data = {}

    for x in data['list']:
        # print(datetime.datetime.fromtimestamp(int(x['dt'])).strftime('%Y-%m-%d'))
        if datetime.datetime.fromtimestamp(int(x['dt'])).strftime('%Y-%m-%d') not in all_dates:
            all_dates.append(datetime.datetime.fromtimestamp(int(x['dt'])).strftime('%Y-%m-%d'))

    # print(all_dates)
    for date in all_dates:
        avg_aqi = get_avg_aqi_for_date(date,data)
        graph_data[date] = avg_aqi

    # print(graph_data) 
    return graph_data

def run():
    startdate,enddate,data = get_aqi_data()
    graph_data = get_graph_data(data)
    x = list(graph_data.keys())
    # print(x)
    y = list(graph_data.values())
    # print(y)
    plt.plot(x,y)
    plt.xlabel("Date")
    plt.ylabel("AQI")
    plt.title(f"Graph of AQI data between {startdate} and {enddate}")
    plt.show()

run()