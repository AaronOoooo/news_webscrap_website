import smbus
import time
import requests

# I2C address of the LCD
LCD_ADDRESS = 0x3f

# Define some constants for LCD control
LCD_BACKLIGHT = 0x08
LCD_ENABLE = 0b00000100
LCD_COMMAND = 0
LCD_DATA = 0x40

# Define line addresses for the 16x2 LCD
LCD_LINE_1 = 0x80
LCD_LINE_2 = 0xC0

alpha_vantage_api_key = "H2KUSYTSJ33FB2CL"

# Function to initialize the LCD
def lcd_init():
    bus.write_byte(LCD_ADDRESS, LCD_COMMAND)
    time.sleep(0.1)

    # initialize 4-bit mode (2 lines)
    lcd_byte(0x33, LCD_COMMAND)
    lcd_byte(0x32, LCD_COMMAND)
    lcd_byte(0x06, LCD_COMMAND)
    lcd_byte(0x0C, LCD_COMMAND)
    lcd_byte(0x28, LCD_COMMAND)
    lcd_byte(0x01, LCD_COMMAND)
    time.sleep(0.1)

# Function to send a byte to the LCD
def lcd_byte(bits, mode):
    bits_high = mode | (bits & 0xF0) | LCD_BACKLIGHT
    bits_low = mode | ((bits << 4) & 0xF0) | LCD_BACKLIGHT

    # High bits
    bus.write_byte(LCD_ADDRESS, bits_high)
    lcd_toggle_enable(bits_high)

    # Low bits
    bus.write_byte(LCD_ADDRESS, bits_low)
    lcd_toggle_enable(bits_low)

# Function to toggle the enable bit for the LCD
def lcd_toggle_enable(bits):
    time.sleep(0.0005)
    bus.write_byte(LCD_ADDRESS, (bits | LCD_ENABLE))
    time.sleep(0.0005)
    bus.write_byte(LCD_ADDRESS, (bits & ~LCD_ENABLE))
    time.sleep(0.0005)

# Function to display text on the LCD
def lcd_string(message, line):
    message = message.ljust(16, " ")
    lcd_byte(line, LCD_COMMAND)
    for i in range(16):
        lcd_byte(ord(message[i]), LCD_DATA)

# Function to fetch stock prices
def get_stock_prices():
    symbols = ["AAPL", "GOOGL", "MSFT"]
    prices = []

    for symbol in symbols:
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={alpha_vantage_api_key}"

        try:
            response = requests.get(url)
            response.raise_for_status()  # Raises an HTTPError for bad responses
            data = response.json()
            
            # Extract the stock price from the Alpha Vantage response
            price = data.get("Global Quote", {}).get("05. price")
            if price:
                prices.append(f"{symbol}: {price}")
            else:
                print(f"Unable to retrieve price for {symbol} from the response.")
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data for {symbol}: {e}")

    return prices

# Main program
bus = smbus.SMBus(1)

try:
    lcd_init()

    # Fetch stock prices once
    prices = get_stock_prices()

    # Display fetched prices
    for price in prices:
        lcd_string(price, LCD_LINE_1)

    # Pause for a few seconds (adjust as needed)
    time.sleep(10)

except KeyboardInterrupt:
    pass

finally:
    bus.write_byte(LCD_ADDRESS, 0x01)  # Clear the display
