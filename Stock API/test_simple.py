print("Step 1: Script started")
try:
    import flask
    print(f"Step 2: Flask version {flask.__version__} found")
except ImportError:
    print("Step 2: Flask NOT found")

try:
    import yfinance
    print("Step 3: yfinance found")
except ImportError:
    print("Step 3: yfinance NOT found")

print("Step 4: Attempting to print a message every second...")
import time
while True:
    print("ALIVE...")
    time.sleep(1)