# 📈 Live Crypto Wallpaper

This Python script fetches real-time cryptocurrency market data (from CoinDCX), generates a custom wallpaper showing the coin's current status, and automatically sets it as your desktop background on Windows.

## 🛠 Features

- Fetches live price data from the [CoinDCX API](https://api.coindcx.com/exchange/ticker).
- Displays key stats: **Bid**, **High**, **Last Price**, **24h Change**, and **Profit/Loss** since your **buying price**.
- Updates every 10 seconds.
- Sets a dynamically generated image as your desktop wallpaper.
- The image text font changes to red when in loss and bright green when profiting.
- Uses your local timezone (`Asia/Kolkata` in this case) for timestamps.

## 🖼 Example Output

- A black background image with white and green/red text showing the coin status and time.

## 📁 File Structure

```
.
├── coin_data.json         # Stores latest fetched coin data
├── my_market.txt          # Stores your selected coin and buying price
├── wallpaper.png          # Generated wallpaper image
├── main.py                # Main script file (your code)
└── README.md              # This file
```

## 📝 Prerequisites

- Python 3.x
- Windows OS (uses Windows API to change wallpaper)
- Install the required Python libraries:

```bash
pip install requests pillow pytz
```

## 🧾 Setup

1. **Create `my_market.txt`**

Create a file named `my_market.txt` in the same directory as the script. Format:

```
coin=NOTINR
buying_price=2.14
```

Replace `NOTINR` with your preferred market (e.g., `BTCINR`, `ETHINR`, etc.) and the `buying_price` with your entry point.

2. **Font File**

Ensure `arial.ttf` is available in the script directory. If not, you can either:
- Copy it from `C:\Windows\Fonts\arial.ttf`
- Or change the font path in the script

## ▶️ Usage

Run the script:

```bash
python main.py
```

It will:
- Continuously fetch the latest price every 10 seconds
- Update `wallpaper.png` with the latest data
- Set the image as your desktop wallpaper

## 🔁 Auto Start (Optional)

To make it run on startup:
- Create a shortcut to the Python script
- Place it in `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup`

## ⚠️ Notes

- This works **only on Windows** (uses `ctypes.windll`).
- You can stop the script by pressing `Ctrl+C` in the terminal.

## 📃 License

This project is open source under the MIT License. Feel free to use and modify!