import os
import json
import time
import requests
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import ctypes
import pytz

# buying_price = 2.14
# coin = "NOTINR"


def read_variables(filename):
    variables = {}
    with open(filename, 'r') as file:
        for line in file:
            key, value = line.strip().split('=')
            variables[key] = value
    return variables

def fetch_coin_data():
    url = "https://api.coindcx.com/exchange/ticker"
    response = requests.get(url)
    # print(response)
    data = response.json()
    # print(data)
    # Find the NOTINR trading pair
    coin_data = next((item for item in data if item["market"] == coin), None)
    if coin_data:
        coin_details = {
            "market": coin_data["market"],
            "last_price": round(float(coin_data["last_price"]), 3),
            "high": round(float(coin_data["high"]), 3),
            "change_24_hour": round(float(coin_data["change_24_hour"]), 1),
            "bid": round(float(coin_data["bid"]), 3)
        }

        with open('coin_data.json', 'w') as file:
            json.dump(coin_details, file, indent=4)


# Function to create an image with text from JSON
def create_image_with_text(data, image_path):
    width, height = 1920, 1200  # Adjust as needed
    image = Image.new('RGB', (width, height), color=(0, 0, 0))
    draw = ImageDraw.Draw(image)

    # Load a true type or open type font file, and create a font object.
    try:
        font_path = "arial.ttf"  # Adjust this path if needed
        font = ImageFont.truetype(font_path, 40)
        small_font = ImageFont.truetype(font_path, 20)  # Smaller font for the time
    except IOError:
        print("Error: Font file not found or cannot be loaded.")
        font = ImageFont.load_default()
        small_font = ImageFont.load_default()

    # Get current time in the "Asia/Kolkata" timezone
    india_time = datetime.now(pytz.timezone("Asia/Kolkata")).strftime('%d-%m-%y %H:%M:%S')

    # Text content
    title_text = data['market']
    position = len(title_text) -3
    title_text = title_text[:position] + ' ' + title_text[position:]
    info_text = (f"Bid: ₹{data['bid']}\nHigh: ₹{data['high']}\nLast Price: ₹{data['last_price']}\n"
                 f"Change 24h: {data['change_24_hour']}%\nChange: {round(data['last_price'] - buying_price, 2)}")
    time_text = india_time

    # Calculate positions
    title_position = (width // 2, 100)  # Centered at the top
    info_bbox = draw.textbbox((0, 0), info_text, font=font)
    info_position = ((width - (info_bbox[2] - info_bbox[0])) // 2, (height - (info_bbox[3] - info_bbox[1])) // 2)
    time_bbox = draw.textbbox((0, 0), time_text, font=small_font)
    time_position = (20, height - (time_bbox[3] - time_bbox[1]) - 20)

    # Draw the title at the top
    draw.text((title_position[0] - draw.textbbox((0, 0), title_text, font=font)[2] // 2, title_position[1]), title_text,
              fill=(255, 255, 255), font=font)

    # Draw the information text
    if float(data['last_price']) >= buying_price:
        draw.text(info_position, info_text, fill=(165, 224, 38), font=font)
    else:
        draw.text(info_position, info_text, fill=(255, 0, 0), font=font)

    # Draw the time in the bottom right corner
    draw.text(time_position, time_text, fill=(165, 224, 38), font=small_font)

    image.save(image_path)


class Main:
    def __init__(self):
        current_directory = os.path.dirname(os.path.abspath(__file__))

        path = os.path.join(current_directory, 'wallpaper.png')
        ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 0)


def update_wallpaper():
    json_file_path = 'coin_data.json'
    # Get the current directory where your Python script is located
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Construct the full path to your 'wallpaper.png' file
    image_path = os.path.join(current_directory, 'wallpaper.png')
    print(image_path)

    try:
        with open(json_file_path, 'r') as file:
            data = json.load(file)
    except Exception as e:
        print(f"Error loading JSON file: {e}")
        return

    try:
        create_image_with_text(data, image_path)
    except Exception as e:
        print(f"Error creating image: {e}")
        return

    try:
        application = Main()
    except Exception as e:
        print(f"Error setting wallpaper: {e}")
        return


if __name__ == '__main__':
    filename = 'my_market.txt'
    market_data = read_variables(filename)
    coin = market_data.get('coin')
    buying_price = float(market_data.get('buying_price'))

    while True:
        fetch_coin_data()
        update_wallpaper()
        time.sleep(10)  # Update every 10 sec
