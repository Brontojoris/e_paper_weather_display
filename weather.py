# This little program is for the Waveshare 7.3
# inch 4 colour epaper display
# It uses OpenWeatherMap API to display weather info
import sys
import os
import requests

from dotenv import load_dotenv
from datetime import datetime
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

import json
from io import BytesIO
import csv

# Search lib folder for display driver modules
sys.path.append('lib')
from waveshare_epd import epd7in3g
epd = epd7in3g.EPD()

picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
icondir = os.path.join(picdir, 'icon')
fontdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'font')

load_dotenv()

# define function for checking internet connection
def internet_connection(url):
    global internet_icon_file
    try:
        response = requests.get(url, timeout=5)
        print('Checking for Internet connectivity.')
        internet_icon_file = 'internet.png'
        return True
    except requests.ConnectionError:
        internet_icon_file = 'warning.png'
        return False

# define function for writing image and sleeping for 5 min.
def write_to_screen(image):
    print('Writing to file.')
    # Write to screen
    h_image = Image.new('1', (epd.width, epd.height), 255)
    # Open the template
    screen_output_file = Image.open(os.path.join(picdir, image))
    # Initialize the drawing context with template as background
    h_image.paste(screen_output_file, (0, 0))
    epd.init()
    epd.display(epd.getbuffer(h_image))
    # Sleep
    time.sleep(2)
    epd.sleep()

# define function for displaying error
def display_error(error_source):
    # Display an error
    print('Error in the', error_source, 'request.')
    # Initialize drawing
    error_image = Image.new('1', (epd.width, epd.height), 255)
    # Initialize the drawing
    draw = ImageDraw.Draw(error_image)
    draw.text((100, 150), error_source +' ERROR', font=font50, fill=black)
    draw.text((100, 300), 'Retrying in 30 seconds', font=font22, fill=black)
    current_time = datetime.now().strftime('%H:%M')
    draw.text((300, 365), 'Last Refresh: ' + str(current_time), font = font50, fill=black)
    # Save the error image
    error_image_file = 'error.png'
    error_image.save(os.path.join(picdir, error_image_file))
    # Close error image
    error_image.close()
    # Write error to screen
    write_to_screen(error_image_file)

# Set the fonts
font22 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 22)
font30 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 30)
font35 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 35)
font50 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 50)
font60 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 60)
font70 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 70)
font80 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 80)
font90 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 90)
font100 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 100)
font160 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 160)
font180 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 180)
font200 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 200)
font220 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 220)
font240 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 240)
font260 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 260)

# Set the colors
black = 'rgb(0,0,0)'
white = 'rgb(255,255,255)'
grey = 'rgb(235,235,235)'

# Initialize and clear screen
print('Initializing and clearing screen.')
epd.init()
epd.Clear()

API_KEY = os.getenv('API_KEY')
LOCATION = os.getenv('LOCATION')
LATITUDE = os.getenv('LATITUDE')
LONGITUDE = os.getenv('LONGITUDE')
UNITS = os.getenv('UNITS')
CSV_OPTION = os.getenv('CSV_OPTION') # if csv_option == True, a weather data will be appended to 'record.csv'

BASE_URL = 'https://api.openweathermap.org/data/3.0/onecall?'
URL = BASE_URL + 'lat=' + LATITUDE + '&lon=' + LONGITUDE + '&units=' + UNITS +'&appid=' + API_KEY

while True:
    # Ensure there are no errors with connection
    error_connect = internet_connection('http://openweathermap.org')
    while error_connect == True:
        try:
            # HTTP request
            print('Attempting to connect to OWM.')
            response = requests.get(URL)
            print('Connection to OWM successful.')
            error_connect = None
        except:
            # Call function to display connection error
            print('Connection error.')
            display_error('CONNECTION')

    error = None
    while error == None:
        # Check status of code request
        if response.status_code == 200:
            print('Connection to Open Weather successful.')
            # get data in jason format
            data = response.json()

            # get current dict block
            current = data['current']
            # get current
            temp_current = current['temp']
            # get feels like
            feels_like = current['feels_like']
            # get humidity
            humidity = current['humidity']
            # get pressure
            wind = current['wind_speed']
            # get description
            weather = current['weather']
            report = weather[0]['description']
            # get icon url
            icon_code = weather[0]['icon']
            #icon_URL = 'http://openweathermap.org/img/wn/'+ icon_code +'@4x.png'

            # get daily dict block
            daily = data['daily']
            # get daily precip
            daily_precip_float = daily[0]['pop']
            #format daily precip
            daily_precip_percent = daily_precip_float * 100
            # get min and max temp
            daily_temp = daily[0]['temp']
            temp_max = daily_temp['max']
            temp_min = daily_temp['min']

            # Append weather data to CSV if csv_option == True
            if CSV_OPTION == True:
                # Get current year, month, date, and time
                current_year = datetime.now().strftime('%Y')
                current_month = datetime.now().strftime('%m')
                current_date = datetime.now().strftime('%d')
                current_time = datetime.now().strftime('%H:%M')
                #open the CSV and append weather data
                with open('records.csv', 'a', newline='') as csv_file:
                    writer = csv.writer(csv_file, delimiter=',')
                    writer.writerow([current_year, current_month, current_date, current_time,
                                     LOCATION,temp_current, feels_like, temp_max, temp_min,
                                     humidity, daily_precip_float, wind])
                print('Weather data appended to CSV.')

            # Set strings to be printed to screen
            string_location = LOCATION
            string_temp_current = format(temp_current, '.0f') + u'\N{DEGREE SIGN}'
            string_feels_like = format(feels_like, '.0f') +  u'\N{DEGREE SIGN}'
            string_humidity = 'Humidity: ' + str(humidity) + '%'
            string_wind = 'Wind: ' + format(wind, '.1f') + ' KPH'
            string_report = 'Now: ' + report.title()
            string_temp_max = format(temp_max, '>.0f') + u'\N{DEGREE SIGN}'
            string_temp_min = format(temp_min, '>.0f') + u'\N{DEGREE SIGN}'
            string_precip_percent = 'Precip: ' + str(format(daily_precip_percent, '.0f'))  + '%'

            # Set error code to false
            error = False

            '''
            print('Location:', LOCATION)
            print('Temperature:', format(temp_current, '.0f'), u'\N{DEGREE SIGN}F')
            print(format(feels_like, '.0f'), 'C')
            print('Humidity:', humidity)
            print('Wind Speed:', format(wind_speed, '.1f'), 'KPH')
            print('Report:', report.title())

            print('High:', format(temp_max, '.0f'), 'C')
            print('Low:', format(temp_min, '.0f'), 'C')
            print('Probabilty of Precipitation: ' + str(format(daily_precip_percent, '.0f'))  + '%')
            '''
        else:
            # Call function to display HTTP error
            display_error('HTTP')

    # Open template file
    template = Image.open(os.path.join(picdir, 'template.png'))
    # Initialize the drawing context with template as background
    draw = ImageDraw.Draw(template)

    # Draw top left box
    ## Open icon file
    icon_file = icon_code + '.png'
    icon_size = (250,250)
    icon_image = Image.open(os.path.join(icondir, icon_file))
    icon_image = icon_image.resize(icon_size)
    ### Paste the image
    template.paste(icon_image, (10, 15))
    ## Place a black rectangle outline
    #draw.rectangle((25, 20, 225, 180), outline=black)
    ## Draw text
    #draw.text((30, 200), string_report, font=font22, fill=black)
    #draw.text((30, 240), string_precip_percent, font=font30, fill=black)
    # Draw top right box
    draw.text((255, 30), string_temp_current, font=font200, fill=black)
    draw.text((62, 385), string_feels_like, font=font60, fill=black)
    # Draw bottom left box
    draw.text((664, 48), string_temp_max, font=font80, fill=black)
    #draw.rectangle((170, 385, 265, 387), fill=black)
    draw.text((664, 148), string_temp_min, font=font80, fill=black)
    # Draw bottom middle box
    #draw.text((345, 340), string_humidity, font=font30, fill=black)
    #draw.text((345, 400), string_wind, font=font30, fill=black)
    # Draw timestamp

	# Draw internet connection
    internet_icon = Image.open(os.path.join(icondir, internet_icon_file))
    template.paste(internet_icon, (600, 300))

    # Save the image for display as PNG
    screen_output_file = os.path.join(picdir, 'screen_output.png')
    template.save(screen_output_file)
    # Close the template file
    template.close()

    # Refresh clear screen to avoid burn-in at 3:00 AM
    if datetime.now().strftime('%H') == '03':
    	print('Clearning screen to avoid burn-in.')
    	epd.Clear()

    # Write to screen
    write_to_screen(screen_output_file)
