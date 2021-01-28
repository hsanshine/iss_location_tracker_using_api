import requests
import datetime as dt
import smtplib
import time

MY_CODE_MAIL = 'hamzamycode@gmail.com'
RC_MAIL = 'sanshinehamza@gmail.com'
GMAIL_SEVER = 'smtp.gmail.com'
MESSAGE = 'Subject: \n\n The iss is over head. Go out now! \n regards\n Your code.'
PASSWORD = 'nokiaham'


def send_message():
    with smtplib.SMTP(GMAIL_SEVER) as connection:
        connection.starttls()
        connection.login(MY_CODE_MAIL, PASSWORD)
        connection.sendmail(from_addr=MY_CODE_MAIL, to_addrs=RC_MAIL, msg='Subject: The ISS is over head\n\n'
                                                                          'Hey, go out now if you want to see the ISS\n'
                                                                          'regards\nYour Code!')


ERROR = 5
LAT = 37.566536
LON = 126.977966
DATE = dt.datetime.now().date()
OFFSET = '+09:00'  # i need to offset because the time in seoul is not the same as the time at utc (time zone change)
print(DATE)

parameters = {
    'lat': LAT,
    'lon': LON,
    'date': dt.datetime.now().date(),
    'offset': OFFSET
}


def get_sun_time():
    data = requests.get(url='https://api.met.no/weatherapi/sunrise/2.0/.json', params=parameters)
    data.raise_for_status()
    sun_times = data.json()
    print(sun_times)
    sunrise = sun_times['location']['time'][0]['sunrise']['time']
    sunset = sun_times['location']['time'][0]['sunset']['time']
    sunrise_time = sunrise.split('T')[1].split('+')[0]
    sunset_time = sunset.split("T")[1].split('+')[0]
    print('sunrise:', sunrise_time)
    print('sunset:', sunset_time)
    return (sunrise_time, sunset_time)


# check today's date and the date in memory, if they are diff, update today's date and get the new sun rise time
# if current time is btn sunset and sunrise (night time), then check if the space station is above
# if the space station is above seoul send me an email.

today = dt.datetime.now().date()
time_tuple = get_sun_time()
print(time_tuple)

print(dt.datetime.now().time())
print(today.year)
print(today.month)
print(today.day)  # if the day changes we update today


# while True:

def is_night_time():
    global today, time_tuple
    if today.day != dt.datetime.now().date().day:  # if the day changed we check the sun set sun rise times again
        today = dt.datetime.now().date()  # update the date for today
        time_tuple = get_sun_time()  # we get the sun rise time and sunset time for the new day
    sunrise_time = time_tuple[0]
    sunset_time = time_tuple[1]
    current_hour = dt.datetime.now().time().hour
    # current_min = dt.datetime.now().time().min
    if int(sunset_time.split(':')[0]) <= current_hour or current_hour <= int(sunrise_time.split(':')[0]):
        #print('is night time is true')
        return True
    else:
        #print('is night time is false')
        return False


def is_over_head():
    location = get_space_station_location()
    iss_lat = round(float(location['latitude']), 2)
    iss_lon = round(float(location['longitude']), 2)
    my_lat = LAT
    my_lon = LON
    print('my_latitude:', my_lat, '\tmy_longitude: ', my_lon)
    print('iss_latitude:', iss_lat, '\tiss_longitude: ', iss_lon,'\n')
    if abs(my_lat - iss_lat) <= ERROR and abs(my_lon - iss_lon) <= ERROR:
        # print('is over head is true')
        return True
    else:
        # print('is over head is false')
        return False


def get_space_station_location():
    data = requests.get(url='http://api.open-notify.org/iss-now.json')
    data.raise_for_status()
    location = data.json()['iss_position']
    latitude = location['latitude']
    longitude = location['longitude']
    return location


def check():
    return is_night_time() and is_over_head()


while True:
    if check():
        while is_over_head():
            send_message()
            time.sleep(60 * 1000)  # runs every 60 seconds when teh ISS is over head

# is_over_head()
# is_night_time()
# send_message()
