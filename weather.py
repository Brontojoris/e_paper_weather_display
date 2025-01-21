# IN PROGRESS VERSION
# This little program is for the Waveshare 7.3g
# inch 4 colour epaper display
# It uses OpenWeatherMap API to display weather info
import sys
import os
import requests
import math

from dotenv import load_dotenv
import csv
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

load_dotenv()

# Automatically add the 'lib' directory relative to the script's location
script_dir = os.path.dirname(os.path.abspath(__file__))
lib_path = os.path.join(script_dir, 'lib')
sys.path.append(lib_path)
from waveshare_epd import epd7in3g
epd = epd7in3g.EPD()

# User defined configuration
API_KEY = os.getenv('API_KEY')
LOCATION = os.getenv('LOCATION')
LATITUDE = os.getenv('LATITUDE')
LONGITUDE = os.getenv('LONGITUDE')
UNITS = os.getenv('UNITS')
CSV_OPTION = os.getenv('CSV_OPTION') # if csv_option == True, a weather data will be appended to 'record.csv'

BASE_URL = f'https://api.openweathermap.org/data/3.0/onecall'
FONT_DIR = os.path.join(os.path.dirname(__file__), 'font')
PIC_DIR = os.path.join(os.path.dirname(__file__), 'pic')
ICON_DIR = os.path.join(PIC_DIR, 'icon')

# Initialize display
epd = epd7in3g.EPD()
epd.init()
#epd.Clear()

# Logging configuration for both file and console
LOG_FILE = 'weather_display.log'
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Use RotatingFileHandler for log rotation
file_handler = RotatingFileHandler(LOG_FILE, maxBytes=1_000_000, backupCount=3)  # 1MB file size, 3 backups
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))
logger.addHandler(file_handler)

# Stream handler for logging to console
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))
logger.addHandler(console_handler)

logger.info("Weather display script started.")

# Set fonts with specific sizes to match the old behavior
def font(size):
    try:
        return ImageFont.truetype(os.path.join(FONT_DIR, 'Font.ttc'), size)
    except Exception as e:
        logging.error(f"FONTERROR: {e}")

COLORS = {'black': 'rgb(0,0,0)', 'white': 'rgb(255,255,255)', 'grey': 'rgb(235,235,235)' }


def get_suffix(day):
    if day in [1, 21, 31]:
        return "st"
    elif day in [2, 22]:
        return "nd"
    elif day in [3, 23]:
        return "rd"
    else:
        return "th"

# Fetch weather data
def fetch_weather_data():
    url = f"{BASE_URL}?lat={LATITUDE}&lon={LONGITUDE}&units={UNITS}&appid={API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        logging.info("Weather data fetched successfully.")
        return response.json()
    except requests.RequestException as e:
        logging.error(f"Failed to fetch weather data: {e}")
        raise

# Process weather data
def process_weather_data(data):
    try:
        current = data['current']
        daily = data['daily'][0]
        weather_data = {
            "temp_current": current['temp'],
            "feels_like": current['feels_like'],
            "humidity": current['humidity'],
            "wind": current['wind_speed'],
            "report": daily['summary'],
            "icon_code": current['weather'][0]['icon'],
            "temp_max": daily['temp']['max'],
            "temp_min": daily['temp']['min'],
            "precip_percent": daily['pop'] * 100,
        }
        logging.info("Weather data processed successfully.")
        return weather_data
    except KeyError as e:
        logging.error(f"Error processing weather data: {e}")
        raise

# Save weather data to CSV
def save_to_csv(weather_data):
    if not CSV_OPTION:
        return
    try:
        with open('records.csv', 'a', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([
                datetime.now().strftime('%Y-%m-%d %H:%M'),
                LOCATION,
                weather_data["temp_current"],
                weather_data["feels_like"],
                weather_data["temp_max"],
                weather_data["temp_min"],
                weather_data["humidity"],
                weather_data["precip_percent"],
                weather_data["wind"]
            ])
        logging.info("Weather data appended to CSV.")
    except IOError as e:
        logging.error(f"Failed to save data to CSV: {e}")

# Generate display image
def generate_display_image(weather_data):
    try:
        template = Image.open(os.path.join(PIC_DIR, 'template.png'))
        draw = ImageDraw.Draw(template)
        icon_path = os.path.join(ICON_DIR, f"{weather_data['icon_code']}.png")
        icon_image = Image.open(icon_path) if os.path.exists(icon_path) else None

        if icon_image:
            template.paste(icon_image, (20, 30))

        temp_current = math.floor(weather_data['temp_current'])
        feels_like   = math.floor(weather_data['feels_like'])
        temp_max     = math.floor(weather_data['temp_max'])
        temp_min     = math.floor(weather_data['temp_min'])
        report       = weather_data['report']

        # Main Current Temp shown center, and larget
        draw.text((235, 1), f"{temp_current}°", font=font(220), fill=COLORS['black'])

        # Feels like shown inside house icon in bottom left
        draw.text((72, 380), f"{feels_like}", font=font(60), fill=COLORS['black'])

        # Daily forecasted max/min temps
        draw.text((664, 38),  f"{temp_max}°", font=font(80), fill=COLORS['black'])
        draw.text((664, 138), f"{temp_min}°", font=font(80), fill=COLORS['black'])

        # Print weather report
        max_line_width = 550
        #draw.text((235, 210 ),  f"{report}", font=font(80), fill=COLORS['black'])

        # Set the font and font size
        report_font = ImageFont.truetype(os.path.join(FONT_DIR, 'Font.ttc'), 56)

        # Split the text into lines
        lines = []
        words = report.split()
        line = ""
        for word in words:
            if report_font.getsize(line + " " + word)[0] > max_line_width:
                lines.append(line)
                line = word
            else:
                if line:
                    line += " "
                line += word
        lines.append(line)
        y = 230  # adjust this value to change the starting y position
        for line in lines:
            draw.text((235, y), line, font=report_font, fill=COLORS['black'])  # adjust the x position as needed
            y += report_font.getsize(line)[1] + 10  # adjust the line spacing as needed


        # DEBUGGING AID: Draw some lines to figure out the boundaries
        #draw.line((235, 200, 235+max_line_width, 200), fill="red", width=2)
        #draw.line((235+max_line_width, 200, 235+max_line_width, 400), fill="red", width=2)

        # Print last update data and time in bottom corner
        date = datetime.now()
        current_time = date.strftime("%a %d") + get_suffix(date.day) + ", " + date.strftime("%I:%M %p")
        draw.text((500, 450), f"Last updated {current_time}", font=font(20), fill=COLORS['black'])

        logging.info("Display image generated successfully.")
        return template
    except Exception as e:
        logging.error(f"Error generating display image: {e}")
        raise

# Display image on screen
def display_image(image):
    try:
        h_image = Image.new('RGB', (epd.width, epd.height), epd.WHITE)
        h_image.paste(image, (0, 0))
        h_image.save('display_image.bmp')  # Save the image to a file
        epd.display(epd.getbuffer(h_image))
        logging.info("Image displayed on e-paper successfully.")
    except Exception as e:
        logging.error(f"Failed to display image: {e}")
        raise

# Main function
def main():
    try:
        data = fetch_weather_data()
        weather_data = process_weather_data(data)
        save_to_csv(weather_data)
        image = generate_display_image(weather_data)
        display_image(image)
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
