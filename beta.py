import os
import csv
import time
import requests
import json
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from PIL import Image, ImageDraw, ImageFont
import ctypes
import pytz

buying_price = 2.25
coin = "NOTINR"
csv_file_path = 'coin_data.csv'
json_file_path = 'coin_data.json'
image_path = 'wallpaper.png'


def fetch_coin_data():
    url = "https://api.coindcx.com/exchange/ticker"
    response = requests.get(url)
    data = response.json()
    coin_data = next((item for item in data if item["market"] == coin), None)
    if coin_data:
        last_price = round(float(coin_data["last_price"]), 3)
        timestamp = datetime.now().timestamp()

        # Save to CSV
        with open(csv_file_path, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, last_price])

        # Save to JSON
        coin_details = {
            "market": coin_data["market"],
            "last_price": last_price,
            "high": round(float(coin_data["high"]), 3),
            "change_24_hour": round(float(coin_data["change_24_hour"]), 3),
            "bid": round(float(coin_data["bid"]), 3)
        }
        with open(json_file_path, 'w') as file:
            json.dump(coin_details, file, indent=4)


def create_graph():
    now = datetime.now()
    one_hour_ago = now - timedelta(hours=1)
    timestamps, prices = []

    with open(csv_file_path, 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)

    # Filter rows to keep only the last hour data
    rows = [row for row in rows if datetime.fromtimestamp(float(row[0])) > one_hour_ago]

    # Update the CSV file to keep only the last hour data
    with open(csv_file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)

    for row in rows:
        timestamps.append(datetime.fromtimestamp(float(row[0])))
        prices.append(float(row[1]))

    plt.figure(figsize=(5, 3), facecolor='black')
    ax = plt.gca()
    ax.set_facecolor('black')
    ax.plot(timestamps, prices, color='white')
    ax.spines['top'].set_color('white')
    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.spines['right'].set_color('white')
    ax.tick_params(axis='x', colors='black')
    ax.tick_params(axis='y', colors='black')

    for spine in ax.spines.values():
        spine.set_edgecolor('white')

    plt.xticks([])
    plt.yticks([])
    plt.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05)
    graph_path = 'graph.png'
    plt.savefig(graph_path, bbox_inches='tight', pad_inches=0, transparent=True)
    plt.close()
    return graph_path


def create_image_with_text(data, image_path, graph_path):
    width, height = 1920, 1200
    image = Image.new('RGB', (width, height), color=(0, 0, 0))
    draw = ImageDraw.Draw(image)

    try:
        font_path = "arial.ttf"
        font = ImageFont.truetype(font_path, 40)
        small_font = ImageFont.truetype(font_path, 20)
    except IOError:
        print("Error: Font file not found or cannot be loaded.")
        font = ImageFont.load_default()
        small_font = ImageFont.load_default()

    india_time = datetime.now(pytz.timezone("Asia/Kolkata")).strftime('%d-%m-%y %H:%M:%S')

    title_text = "NOT-COIN"
    info_text = (f"Bid: ₹{data['bid']}\nHigh: ₹{data['high']}\nLast Price: ₹{data['last_price']}\n"
                 f"Change 24h: {data['change_24_hour']}%")
    time_text = india_time

    title_position = (width // 2, 100)
    info_bbox = draw.textbbox((0, 0), info_text, font=font)
    info_position = ((width - (info_bbox[2] - info_bbox[0])) // 2, (height - (info_bbox[3] - info_bbox[1])) // 2)
    time_bbox = draw.textbbox((0, 0), time_text, font=small_font)
    time_position = (20, height - (time_bbox[3] - time_bbox[1]) - 20)

    draw.text((title_position[0] - draw.textbbox((0, 0), title_text, font=font)[2] // 2, title_position[1]), title_text,
              fill=(255, 255, 255), font=font)

    if float(data['last_price']) >= buying_price:
        draw.text(info_position, info_text, fill=(165, 224, 38), font=font)
    else:
        draw.text(info_position, info_text, fill=(255, 0, 0), font=font)

    draw.text(time_position, time_text, fill=(165, 224, 38), font=small_font)

    graph_image = Image.open(graph_path)
    graph_position = (width // 2 - graph_image.width // 2, info_position[1] + info_bbox[3] - info_bbox[1] + 20)
    image.paste(graph_image, graph_position)

    image.save(image_path)


class Main:
    def __init__(self):
        path = os.path.abspath(image_path)
        ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 0)


def update_wallpaper():
    try:
        with open(json_file_path, 'r') as file:
            data = json.load(file)
    except Exception as e:
        print(f"Error loading JSON file: {e}")
        return

    try:
        graph_path = create_graph()
        create_image_with_text(data, image_path, graph_path)
    except Exception as e:
        print(f"Error creating image: {e}")
        return

    try:
        Main()
    except Exception as e:
        print(f"Error setting wallpaper: {e}")
        return


if __name__ == '__main__':
    if not os.path.exists(csv_file_path):
        with open(csv_file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['timestamp', 'last_price'])  # Write header row

    while True:
        fetch_coin_data()
        update_wallpaper()
        time.sleep(10)
